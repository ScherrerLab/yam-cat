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
from params import Params
from utils import get_acquire_subprocess_path, get_default_config, get_tiscam_serial_numbers
import threading
from pyqtgraph import ImageView, mkQApp
from PyQt5 import QtCore
import numpy as np

logger = logging.getLogger()


class ArduinoTrigger(Process):
    def __init__(
            self,
            address: str,
            pin: int,
    ):
        """
        Process for communicating with the Arduino to provide the camera trigger signal

        Parameters
        ----------
        address: str
            Address of the arduino, example: `/dev/ttyACM0`
        pin: int
            Arduino pin for sending the 5V trigger square waves
        """
        super().__init__()

        logger.info(f'Connecting to Arduino at: {address}, pin#: {pin}')
        self.board = Arduino(address)
        self.pin = int(pin)

        self.board.digital[self.pin].write(0)
        # self.reset_pin()

        self.fps: int = None
        logger.info(f'Yay Arduino is connected!')

    def set_fps(self, fps: int):
        """
        Set the framerate

        Parameters
        ----------
        fps: int
            Framerate (frames per second)

        Returns
        -------

        """
        self.fps = fps

        # because square wave pulses
        # high for first half, low for second half
        self.delay = (1 / fps) / 2

        logger.info(f'Arduino trigger is set to: {fps}Hz')

    def run(self) -> None:
        logger.info(f'Started trigger')
        while True:
            self.board.digital[self.pin].write(1)
            time.sleep(self.delay)
            self.board.digital[self.pin].write(0)
            time.sleep(self.delay)

    def reset_pin(self):
        """
        Reset the arduino, turn off the trigger signal.
        """
        self.board.digital[self.pin].write(0)

    # def terminate(self) -> None:
    #     self.reset_pin()
    #     super(ArduinoTrigger, self).terminate()


class Writer(Process):
    def __init__(
            self,
            camera_name: str,
            queue: Queue,
            output_path: Union[Path, str],
            fps: int,
            fourcc: str = 'mp4v',
            dims: Tuple[int, int] = (1024, 1024),
            preview: bool = True,
            preview_position: Tuple[int] = None,
            preview_size: Tuple[int] = None,
            queue_preview: Queue = None
    ):
        """
        Process for writing the video to disk. Preview is  WIP.

        Parameters
        ----------
        camera_name: str
            Camera name, used for the video filename

        queue: Queue
            multiprocessing Queue that the camera process dumps frame into

        output_path: str
            full output path for the resultant video file

        fps: int
            framerate for video playback, usually same as that set for the trigger

        fourcc: str
            fourcc code for video codec

        dims: Tuple[int, int]
            dimensions for the resultant video

        preview: bool
            Show video preview, WIP

        preview_position
        preview_size
        queue_preview
        """
        super().__init__()
        self.queue = queue
        self.camera_name = camera_name
        self.output_path = str(output_path)

        self.fourcc = cv2.VideoWriter_fourcc(*fourcc)

        self.dims = dims

        self.video_writer = cv2.VideoWriter(
            output_path,
            self.fourcc,
            int(fps),
            self.dims,
            isColor=True
        )
        logger.info(f'Writer ready for: {self.camera_name}')

        self.preview = preview

        if self.preview:
            self.image_view = ImageView()
            self.image_view.setFixedSize(*preview_size)
            self.image_view.move(*preview_position)
            self.image_view.show()

        self.queue_preview = queue_preview

    def run(self) -> None:
        while True:
            data = self.queue.get()

            bpp = 4
            dtype = np.uint8

            img_mat = np.ndarray((self.dims[1], self.dims[0], bpp), buffer=data, dtype=dtype)

            frame = cv2.cvtColor(img_mat, cv2.COLOR_BGRA2BGR)

            if frame is None:
                print("Video writer finished")
                return

            self.video_writer.write(frame)

            # if self.preview:
            #     self.image_view.setImage(frame)
            #     time.sleep(0.01)
            # else:
            # self.queue_preview.put(frame)
            # time.sleep(0.05)


class VideoDisplayQThread(QtCore.QThread):
    def __init__(
            self,
            camera_name: str,
            queue: Queue,
            position: Tuple[int, int],
            size: Tuple[int, int]
    ):
        super().__init__()
        self.camera_name = camera_name
        self.queue = queue
        self.position = position
        # self.app = mkQApp(self.camera_name)

        self.image_view = ImageView()
        self.image_view.setFixedSize(*size)
        self.image_view.move(*position)
        self.image_view.show()

        # self.app.exec()

    def update_frame(self):
        # frame = self.queue.get()
        frame = np.random.rand(1024, 1024)

        # downsample by 2
        self.image_view.setImage(frame[::2, ::2])
        # self.app.processEvents()

    def run(self) -> None:
        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(0)
        while True:
            self.update_frame()


class VideoDisplay(Process):
    def __init__(
            self,
            camera_name: str,
            queue: Queue,
            position: Tuple[int, int],
            size: Tuple[int, int]
    ):
        super().__init__()
        self.camera_name = camera_name
        self.queue = queue
        self.position = position
        self.app = mkQApp(self.camera_name)

        self.image_view = ImageView()
        self.image_view.setFixedSize(*size)
        self.image_view.move(*position)
        self.image_view.show()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(0)

        self.app.exec()

    def update_frame(self):
        frame = self.queue.get()
        self.image_view.setImage(frame)
        self.app.processEvents()


class POpenThread:
    """
    Wrapper for the Acquisition Subprocess to attach a callback function when the acquisition process has finished
    """
    def __init__(self):
        self.proc = None

    def runInThread(self, callback: callable, cmd: List[str]):
        """
        Runs `cmd` in a subprocess and then runs the `callback` function
        when the subprocess has finished.
        """
        self.proc = subprocess.Popen(cmd, env=os.environ.copy())
        self.proc.wait()
        callback()
        return

    def start(self, callback, cmd):
        # popen_thread = POpenThread()

        thread = threading.Thread(target=self.runInThread,
                                  args=(callback, cmd))
        thread.start()

        return self.proc


class Operator:
    """
    Operates the various processes for acquisition from multiple cameras and writing
    to disk and keeps track of parameters.
    """
    def __init__(self):
        self.arduino_trigger: ArduinoTrigger = None

        self.camera_guids: List[str] = get_tiscam_serial_numbers()
        self.camera_names: dict = dict.fromkeys(self.camera_guids)
        default_config = get_default_config()
        for guid in self.camera_guids:
            self.camera_names[guid] = default_config['camera-names'][guid]

        self.params: Params = None

        self.acquire_subprocesses: Dict[str, subprocess.Popen] = dict.fromkeys(self.camera_guids)

        self.record_finished_counter = 0

        self.parent_ui = None

    def connect_arduino(self, addr: str):
        """
        Connect to the arduino

        Parameters
        ----------
        addr: str
            Address of the arduino, example: `/dev/ttyACM0`

        """
        pin = get_default_config()['arduino']['pin']
        self.arduino_trigger = ArduinoTrigger(address=addr, pin=pin)

    def prime(self):
        """
        Prime the cameras for frame grabbing.

        Launches the Acquisition subprocesses for each camera

        Returns
        -------

        """
        os.makedirs(self.params.destination_dir, exist_ok=True)

        cameras_to_use = list()

        for cc in self.params.camera_configs:
            cameras_to_use.append(cc.guid)

        for cc_guid in cameras_to_use:
            if cc_guid not in self.camera_guids:
                raise KeyError(
                    f"You have asked to prime the following camera: {cc.guid}.\n"
                    f"But it is not connected or available.\n"
                    f"The following cameras are available:\n"
                    f"{self.camera_guids}"
                )

        for guid in cameras_to_use:
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

            self.acquire_subprocesses[guid] = POpenThread().start(
                callback=self.record_finished,
                cmd=['python', get_acquire_subprocess_path()] + args
            )

        time.sleep(1)

        logger.info("** Cameras Primed **")

    def de_prime(self):
        """
        Cleans up acquisition subprocesses
        """
        self._kill_subprocesses()

    def _kill_subprocesses(self):
        for sp in self.acquire_subprocesses.values():
            os.killpg(os.getpgid(sp.pid), signal.SIGTERM)

        self.acquire_subprocesses: Dict[str, subprocess.Popen] = dict.fromkeys(self.camera_guids)

    def record(self):
        """
        Starts the trigger signal from the Arduino process, which in turn begins frame grabbing
        in the acquisition subprocess.
        """
        self.arduino_trigger.start()
        self.record_finished_counter = 0

    def record_finished(self):
        """
        Callback function, called when an acquisition subprocess has finished.
        """
        print(f"Recording finished, {self.record_finished_counter}")
        self.record_finished_counter += 1
        if self.record_finished_counter == len(self.acquire_subprocesses.keys()):
            self.record_finished_all()

    def record_finished_all(self):
        """
        Called when all acquisition subprocesses have finished.
        Resets the Arduino.
        """
        self.record_finished_counter = 0
        self._reset_arduino()

        if self.parent_ui is not None:
            self.parent_ui.record_finished()

    def abort_record(self):
        self._reset_arduino()
        self._kill_subprocesses()

    def _reset_arduino(self):
        self.arduino_trigger.reset_pin()
        self.arduino_trigger.terminate()
        # self.arduino_trigger.close()

        time.sleep(3)
        self.connect_arduino(self.params.arduino_address)
