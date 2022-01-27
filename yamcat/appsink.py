#!/usr/bin/env python3

# Copyright 2017 The Imaging Source Europe GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# This example will show you how to enable trigger-mode
# and how to trigger images with via software trigger.
#
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

import sys
import gi
import time

gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")
gi.require_version("GstVideo", "1.0")

from gi.repository import Tcam, Gst, GstVideo

framecount = 0

def callback(appsink, queue):
    """
    This function will be called in a separate thread when our appsink
    says there is data for us. user_data has to be defined
    when calling g_signal_connect. It can be used to pass objects etc.
    from your other function to the callback.
    """
    sample = appsink.emit("pull-sample")

    if sample:

        buf = sample.get_buffer()
        caps = sample.get_caps()
        mem = buf.get_all_memory()

        success, info = mem.map(Gst.MapFlags.READ)

        if success:
            data = info.data
            mem.unmap(info)

            # bpp = 4
            # dtype = np.uint8
            # bla = caps.get_structure(0).get_value('height')
            # if( caps.get_structure(0).get_value('format') == "BGRx" ):
            #     bpp = 4
            #
            # if(caps.get_structure(0).get_value('format') == "GRAY8" ):
            #     bpp = 1
            #
            # if(caps.get_structure(0).get_value('format') == "GRAY16_LE" ):
            #     bpp = 1
            #     dtype = np.uint16
            #
            # img_mat = np.ndarray(
            #     (caps.get_structure(0).get_value('height'),
            #      caps.get_structure(0).get_value('width'),
            #      bpp),
            #     buffer=data,
            #     dtype=dtype)

            queue.put(data)

            global framecount

            print(framecount, end='\r')
            framecount += 1
        # success, info = mem.map(Gst.MapFlags.READ)
        # try:
        #     (ret, buffer_map) = gst_buffer.map(Gst.MapFlags.READ)
        #
        #     video_info = GstVideo.VideoInfo()
        #     video_info.from_caps(caps)
        #
        #     stride = video_info.finfo.bits / 8
        #
        #     pixel_offset = int(video_info.width / 2 * stride +
        #                        video_info.width * video_info.height / 2 * stride)
        #
        #     # this is only one pixel
        #     # when dealing with formats like BGRx
        #     # pixel_data will have to consist out of
        #     # pixel_offset   => B
        #     # pixel_offset+1 => G
        #     # pixel_offset+2 => R
        #     # pixel_offset+3 => x
        #     pixel_data = buffer_map.data[pixel_offset]
        #     timestamp = gst_buffer.pts
        #
        #     global framecount
        #
        #     output_str = "Captured frame {}, Pixel Value={} Timestamp={}".format(framecount,
        #                                                                          pixel_data,
        #                                                                          timestamp)
        #
        #     print(output_str, end="\r")  # print with \r to rewrite line
        #
        #     framecount += 1

        # finally:
        #     mem.unmap(buffer_map)

    return Gst.FlowReturn.OK


def main():

    Gst.init(sys.argv)  # init gstreamer

    # this line sets the gstreamer default logging level
    # it can be removed in normal applications
    # gstreamer logging can contain verry useful information
    # when debugging your application
    # see https://gstreamer.freedesktop.org/documentation/tutorials/basic/debugging-tools.html
    # for further details
    Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)

    serial = '40120421'

    pipeline = Gst.parse_launch("tcambin name=source"
                                " ! videoconvert"
                                " ! appsink name=sink")

    # test for error
    if not pipeline:
        print("Could not create pipeline.")
        sys.exit(1)

    queue = Queue()

    writer = Writer(
        camera_name='front',
        queue=queue,
        output_path='/home/labuser/test-yamcat-mouse/test_vid.avi',
        fps=60,
        fourcc='mp4v',
        dims=(2048, 1536),
        preview=False
    )

    writer.start()

    # The user has not given a serial, so we prompt for one
    if serial is not None:
        source = pipeline.get_by_name("source")
        source.set_property("serial", serial)

    sink = pipeline.get_by_name("sink")

    # tell appsink to notify us when it receives an image
    sink.set_property("emit-signals", True)

    # tell appsink what function to call when it notifies us
    sink.connect("new-sample", callback, queue)

    pipeline.set_state(Gst.State.PLAYING)

    print("Press Ctrl-C to stop.")

    # We wait with this thread until a
    # KeyboardInterrupt in the form of a Ctrl-C
    # arrives. This will cause the pipline
    # to be set to state NULL
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.set_state(Gst.State.NULL)


if __name__ == "__main__":
    main()
