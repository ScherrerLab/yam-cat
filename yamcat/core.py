from pypylon import pylon
import cv2
from multiprocessing import Process, Queue
from typing import *
from pathlib import Path


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
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()

        self.fps = 50  # framerate
        self.duration = 60  # duration in seconds

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

    def run(self) -> None:
        self.camera.StartGrabbingMax(self.nframes_grab)

        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if not grabResult.GrabSucceeded():
                print(f"Couldn't grab frame\n{grabResult.ErrorDescription()}")
                return

            image = self.converter.Convert(grabResult)
            frame = image.getArray()

            self.queue.put(frame)


class Writer(Process):
    def __init__(
            self,
            queue: Queue,
            output_path: str,
            video_params: dict = None
    ):
        super().__init__()
        self.queue = queue
        self.output_path = output_path

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

    def run(self) -> None:
        while True:
            frame = self.queue.get()

            if frame is None:
                print("Video writer finished")
                return

            self.video_writer.write(frame)
