from pypylon import pylon
import cv2
from multiprocessing import Process, Queue
from typing import *
from pathlib import Path


class Writer(Process):
    def __init__(
            self,
            queue: Queue,
            fps: int,
            duration: int,
            output_path: Union[Path, str]
    ):
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

        self.output_path = output_path

    def run(self):
        self.camera.StartGrabbingMax(self.nframes_grab)

        while self.camera.IsGrabbing():
            grabbed = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabbed.GrabSucceeded():
                # put frame in queue
                pass