from pypylon import pylon
import cv2
from multiprocessing import Process, Queue
from typing import *
from pathlib import Path
from pyfirmata import Arduino, util
import time
import logging


logger = logging.getLogger()


class ArduinoTrigger(Process):
    def __init__(
            self,
            address: str,
            pin: int,
            fps: int,
    ):
        super().__init__()

        logger.info(f'Connecting to Arduino at: {address}, pin#: {pin}')
        self.board = Arduino(address)
        self.pin = pin

        self.board.digital[self.pin].write(0)
        # self.reset_pin()

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

    def kill(self) -> None:
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

        fps = int(50)

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


class Manager(Process):
    def __init__(
            self,
            apl: List[Acquire],
            arduino_trigger: ArduinoTrigger
    ):
        super().__init__()
        self.apl = apl
        self.arduino_trigger = arduino_trigger
        logger.info("Started Manager")

    def run(self) -> None:
        logger.info("Manager is running")
        # just sleeps until all acquisition processes have finished
        while all(map(lambda x: not x, [p.is_alive() for p in self.apl])):
            time.sleep(1)
            logger.info("Manager is sleeping")

        self.arduino_trigger.kill()
        logger.info('Manager killed ArduinoTrigger process')
