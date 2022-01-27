
# Add path to python-common/TIS.py to the import path
import sys
import cv2
import numpy as np
import os
from yamcat.tis import TIS, SinkFormats
import time
from collections import namedtuple
from multiprocessing import Queue
from yamcat.core import Writer
import sys
from multiprocessing import Process, Queue
import logging
from datetime import datetime
import click
from yamcat.core import Writer, VideoDisplayQThread
from pprint import pprint
from time import sleep
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject


def exception_hook(exc_type, exc_value, traceback):
    logging.error("EXCEPTION ENCOUNTERED", exc_info=(exc_type, exc_value, traceback))


# This sample shows, how to get an image in a callback and use trigger or software trigger
# needed packages:
# pyhton-opencv
# pyhton-gst-1.0
# tiscamera


class CustomData:
    ''' Example class for user data passed to the on new image callback function
    '''

    def __init__(self, newImageReceived, image):
        self.newImageReceived = newImageReceived
        self.image = image
        self.busy = False


CD = CustomData(False, None)


def on_new_image(tis, userdata):
    '''
    Callback function, which will be called by the TIS class
    :param tis: the camera TIS class, that calls this callback
    :param userdata: This is a class with user data, filled by this call.
    :return:
    '''
    # Avoid being called, while the callback is busy
    if userdata.busy is True:
        return

    userdata.busy = True
    userdata.newImageReceived = True
    userdata.image = tis.Get_image()
    userdata.busy = False


class Main(QObject):
    def __init__(self,
                 device_guid,
                 camera_name,
                 fps,
                 duration,
                 trigger_line,
                 video_output_path,
                 fourcc,
                 dims,
                 preview_position,
                 preview_size):
        super().__init__()
        log_level = 'DEBUG'
        log_format = "%(asctime)s %(levelname)s %(pathname)s %(lineno)s \n %(message)s "
        log_file = f'/home/lab/{datetime.now().strftime("acquire_%Y-%m-%d_%H.%M.%S-%f")}.ycl'

        logging.basicConfig(
            level=log_level,
            format=log_format,
            filename=log_file,
            filemode='w'
        )

        sys.excepthook = exception_hook


        tis = TIS()

        # The following line opens and configures the video capture device.
        tis.openDevice("40120423", 2048, 1536, "120/1", SinkFormats.BGRA, False)

        # The next line is for selecting a device, video format and frame rate.
        #if not Tis.selectDevice():
        #        quit(0)

        #Tis.List_Properties()
        tis.Set_Image_Callback(on_new_image, CD)

        # Tis.Set_Property("Trigger Mode", "Off") # Use this line for GigE cameras
        tis.Set_Property("Trigger Mode", False)
        CD.busy = True # Avoid, that we handle image, while we are in the pipeline start phase
        # Start the pipeline
        tis.Start_pipeline()

        # Tis.Set_Property("Trigger Mode", "On") # Use this line for GigE cameras
        tis.Set_Property("Trigger Mode", True)
        tis.Set_Property("Trigger Polarity", "Rising Edge")

        CD.busy = False  # Now the callback function does something on a trigger

        # Remove comment below in oder to get a propety list.
        # Tis.List_Properties()

        # In case a color camera is used, the white balance automatic must be
        # disabled, because this does not work good in trigger mode
        tis.Set_Property("Whitebalance Auto", False)
        tis.Set_Property("Whitebalance Red", 64)
        tis.Set_Property("Whitebalance Green", 50)
        tis.Set_Property("Whitebalance Blue", 64)


        # Query the gain auto and current value :
        print("Gain Auto : %s " % tis.Get_Property("Gain Auto").value)
        print("Gain : %d" % tis.Get_Property("Gain").value)

        # Check, whether gain auto is enabled. If so, disable it.

        if tis.Get_Property("Gain Auto").value :
            tis.Set_Property("Gain Auto", False)
            print("Gain Auto now : %s " % tis.Get_Property("Gain Auto").value)

        tis.Set_Property("Gain", 0)

        # Now do the same with exposure. Disable automatic if it was enabled
        # then set an exposure time.
        if tis.Get_Property("Exposure Auto").value :
            tis.Set_Property("Exposure Auto", False)
            print("Exposure Auto now : %s " % tis.Get_Property("Exposure Auto").value)

        #Tis.Set_Property("Exposure Time", 7000)

        error = 0
        print('Press Esc to stop')
        lastkey = 0
        #cv2.namedWindow('Window',cv2.WINDOW_NORMAL)

        queue = Queue()

        writer = Writer(
            camera_name='test',
            queue=queue,
            output_path='/home/kushal/test-is-trigger.avi',
            fps=100,
            fourcc='mp4v',
            dims=(2048, 1536),
            preview=False
            # preview_size=preview_size,
            # preview_position=preview_position,
            # queue_preview=queue_preview
        )
        writer.start()

        nframes_current = 0
        nframes_total = duration * fps
        while nframes_total < nframes_current:
            #time.sleep(1)
            #Tis.Set_Property("Software Trigger",1) # Send a software trigger

            # Wait for a new image. Use 10 tries.
            #tries = 10
            #while CD.newImageReceived is False and tries > 0:
            #        time.sleep(0.1)
            #        tries -= 1

            # Check, whether there is a new image and handle it.
            if CD.newImageReceived is True:
                CD.newImageReceived = False
                #print(CD.image)
                #print(CD.image.shape)
                img = cv2.cvtColor(CD.image, cv2.COLOR_BGRA2BGR)
                queue.put(img)
                nframes_current += 1


                #cv2.imshow('Window', CD.image)
            #else:
            #print("No image received")

            #lastkey = cv2.waitKey(10)

        # Stop the pipeline and clean ip
        tis.Stop_pipeline()
        print('Program ends')


@click.command()
@click.option('--device-guid', type=str)
@click.option('--camera-name', type=str)
@click.option('--fps', type=int)
@click.option('--duration', type=int)
@click.option('--trigger-line', type=int)
@click.option('--video-output-path', type=str)
@click.option('--fourcc', type=str)
@click.option('--dims', type=str)
@click.option('--preview-position', type=str)
@click.option('--preview-size', type=str)
def main(
        device_guid,
        camera_name,
        fps,
        duration,
        trigger_line,
        video_output_path,
        fourcc,
        dims,
        preview_position,
        preview_size
):
    return Main(
        device_guid,
        camera_name,
        fps,
        duration,
        trigger_line,
        video_output_path,
        fourcc,
        dims,
        preview_position,
        preview_size
    )


if __name__ == '__main__':
    app = QApplication([])
    main()

    app.exec()
