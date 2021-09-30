import os
import subprocess
import signal
import cv2
from multiprocessing import Process, Queue
from typing import *
from pathlib import Path
from pyfirmata import Arduino, util
import time
import logging
from pypylon import pylon
from .params import Params, CameraConfig
from utils import get_basler_camera_guids, get_acquire_subprocess_path, get_default_config
import threading

logger = logging.getLogger()


class ArduinoTrigger(Process):
    def __init__(
            self,
            address: str,
            pin: int,
    ):
        super().__init__()

        logger.info(f'Connecting to Arduino at: {address}, pin#: {pin}')
        self.board = Arduino(address)
        self.pin = pin

        self.board.digital[self.pin].write(0)
        # self.reset_pin()

        self.fps: int = None

    def set_fps(self, fps):
        self.fps = fps

        # because square wave pulses
        # high for first half, low for second half
        self.delay = (1 / fps) / 2
        logger.info(f'Arduino is ready')

    def run(self) -> None:
        logger.info(f'Started trigger')
        while True:
            self.board.digital[self.pin].write(1)
            time.sleep(self.delay)
            self.board.digital[self.pin].write(0)
            time.sleep(self.delay)

    def reset_pin(self):
        self.board.digital[self.pin].write(0)

    def terminate(self) -> None:
        self.reset_pin()
        super(ArduinoTrigger, self).kill()


class Writer(Process):
    def __init__(
            self,
            camera_name: str,
            queue: Queue,
            output_path: Union[Path, str],
            fps: int,
            fourcc: str = 'mp4v',
            dims: Tuple[int, int] = (1024, 1024)
    ):
        super().__init__()
        self.queue = queue
        self.camera_name = camera_name
        self.output_path = str(output_path)

        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(
            output_path,
            self.fourcc,
            fps,
            dims,
            isColor=True
        )
        logger.info(f'Writer ready for: {self.camera_name}')

    def run(self) -> None:
        while True:
            frame = self.queue.get()

            if frame is None:
                print("Video writer finished")
                return

            self.video_writer.write(frame)


class Operator:
    def __init__(self):
        self.arduino_trigger: ArduinoTrigger = None
        self.arduino_address: str = None

        self.tl_factory: pylon.TlFactory = pylon.TlFactory.GetInstance()
        self.camera_guids: List[str] = get_basler_camera_guids()

        self.params: Params = None

        self.acquire_subprocesses: Dict[str, subprocess.Popen] = dict.fromkeys(self.camera_guids)

        self.record_finished_counter = 0

        self.parent_ui = None

    def connect_arduino(self, addr: str):
        pin = get_default_config()['arduino_pin']
        self.arduino_trigger = ArduinoTrigger(address=addr, pin=pin)

    def popenAndCall(self, onExit, *popenArgs, **popenKWArgs):
        """
        From:
        https://stackoverflow.com/questions/2581817/python-subprocess-callback-when-cmd-exits

        Runs a subprocess.Popen, and then calls the function onExit when the
        subprocess completes.

        Use it exactly the way you'd normally use subprocess.Popen, except include a
        callable to execute as the first argument. onExit is a callable object, and
        *popenArgs and **popenKWArgs are simply passed up to subprocess.Popen.
        """
        class POpenThread:
            def runInThread(thread, onExit, popenArgs, popenKWArgs):
                thread.proc = subprocess.Popen(*popenArgs, **popenKWArgs)
                thread.proc.wait()
                onExit()
                return

        popen_thread = POpenThread()

        thread = threading.Thread(target=popen_thread.runInThread,
                                  args=(onExit, popenArgs, popenKWArgs))
        thread.start()

        return popen_thread.proc

    def prime(self):
        for guid in self.camera_guids:
            params_dict = self.params.to_dict(device_guid=guid)
            name = params_dict['camera-name']
            args = self.params.to_args(params_dict)

            logger.info(
                f'Priming camera:'
                f'\n\t{name}'
                f'\n\t{guid}'
            )
            # sp = subprocess.Popen(
            #     ['python', get_acquire_subprocess_path()] + args, env=os.environ.copy()
            # )

            self.acquire_subprocesses[guid] = self.popenAndCall()

        time.sleep(3)

        logger.info("** Cameras Primed **")

    def de_prime(self):
        self._kill_subprocesses()

    def _kill_subprocesses(self):
        for sp in self.acquire_subprocesses.values():
            os.killpg(os.getpgid(sp.pid), signal.SIGTERM)

        self.acquire_subprocesses: Dict[str, subprocess.Popen] = dict.fromkeys(self.camera_guids)

    def record(self):
        self.arduino_trigger.start()
        self.record_finished_counter = 0

    def record_finished(self):
        self.record_finished_counter += 1
        if self.record_finished_counter == len(self.acquire_subprocesses.keys()):
            self.record_finished_all()

    def record_finished_all(self):
        self.record_finished_counter = 0
        self._reset_arduino()

        if self.parent_ui is not None:
            self.parent_ui.record_finished()

    def abort_record(self):
        self._reset_arduino()
        self._kill_subprocesses()

    def _reset_arduino(self):
        self.arduino_trigger.terminate()
        self.arduino_trigger.close()

        time.sleep(3)
        self.connect_arduino(self.arduino_address)
