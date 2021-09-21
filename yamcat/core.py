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

        self.board.digital[pin].write(0)

        self.fps = fps

        # because square wave pulses
        # high for first half, low for second half
        self.delay = (1 / fps) / 2

    def run(self) -> None:
        logger.info(f'Started trigger')
        while True:
            self.board.digital[self.pin].write(1)
            time.sleep(self.delay)
            self.board.digital[self.pin].write(0)
            time.sleep(self.delay)


class Acquire(Process):
    def __init__(
            self,
            camera_name: str,
            queue: Queue,
            fps: int,
            duration: int,
    ):
        super().__init__()
        self.queue = queue
        self.camera_name = camera_name

        logger.info(f'Connecting to camera: {self.camera_name}')
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()

        self.fps = 50  # framerate
        self.duration = 60  # duration in seconds

        self.camera.Width.SetValue(1024)
        self.camera.Height.setValue(1024)

        # number of frames to grab
        self.nframes_grab = fps * duration

        self.camera.MaxNumBuffer = 100

        self.camera.TriggerSelector.SetValue('FrameStart')
        self.camera.TriggerMode.SetValue('On')
        self.camera.TriggerSource.SetValue('Line2')  # for old cam 1920, black wire
        self.camera.TriggerActivation.SetValue('RisingEdge')

        self.converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        logger.info(f'Camera ready: {camera_name}')

    def run(self) -> None:
        self.camera.StartGrabbingMax(self.nframes_grab)

        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if not grabResult.GrabSucceeded():
                logger.info(f"{self.camera_name}: Couldn't grab frame\n{grabResult.ErrorDescription()}")
                return

            image = self.converter.Convert(grabResult)
            frame = image.getArray()

            self.queue.put(frame)

        self.queue.put(None)


class Writer(Process):
    def __init__(
            self,
            camera_name: str,
            queue: Queue,
            output_path: Union[Path, str],
            video_params: dict = None
    ):
        super().__init__()
        self.queue = queue
        self.camera_name = camera_name
        self.output_path = str(output_path)

        if video_params is None:
            self.video_params = {
                'fourcc': 'X264',
                'fps': 50,
                'dims': (1024, 1024)
            }
        else:
            self.video_params = video_params

        self.fourcc = cv2.VideoWriter_fourcc(*"fourcc")
        self.video_writer = cv2.VideoWriter(
            output_path,
            self.fourcc,
            self.video_params['fps'],
            self.video_params['dims'],
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

    def run(self) -> None:
        # just sleeps until all acquisition processes have finished
        while all(map(lambda x: not x, [p.is_alive() for p in self.apl])):
            time.sleep(1)

        self.arduino_trigger.kill()
        logger.info('Manager killed ArduinoTrigger process')
