from multiprocessing import Process, Queue
from pypylon import pylon

from pypylon import pylon


class Grab(Process):
    def __init__(self):
        super().__init__()
        # Number of images to be grabbed.
        self.countOfImagesToGrab = 100

        # The exit code of the sample application.
        exitCode = 0

        # Create an instant camera object with the camera device found first.
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        self.camera.Open()

        # Print the model name of the camera.
        print("Using device ", self.camera.GetDeviceInfo().GetModelName())

        # demonstrate some feature access
        new_width = self.camera.Width.GetValue() - self.camera.Width.GetInc()
        if new_width >= self.camera.Width.GetMin():
            self.camera.Width.SetValue(new_width)

        # The parameter MaxNumBuffer can be used to control the count of buffers
        # allocated for grabbing. The default value of this parameter is 10.
        self.camera.MaxNumBuffer = 5

    def run(self) -> None:
        # Start the grabbing of c_countOfImagesToGrab images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        self.camera.StartGrabbingMax(self.countOfImagesToGrab)

        # Camera.StopGrabbing() is called automatically by the RetrieveResult() method
        # when c_countOfImagesToGrab images have been retrieved.
        while self.camera.IsGrabbing():
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            # Image grabbed successfully?
            if grabResult.GrabSucceeded():
                # Access the image data.
                print("SizeX: ", grabResult.Width)
                print("SizeY: ", grabResult.Height)
                img = grabResult.Array
                print("Gray value of first pixel: ", img[0, 0])
            else:
                print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
            grabResult.Release()
        self.camera.Close()

g = Grab()

g.start()
