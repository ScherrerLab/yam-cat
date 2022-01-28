#!/usr/bin/env python3

# Copyright 2019 The Imaging Source Europe GmbH
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
# This example will show you how to save a video stream to a file
#

import time
import sys
import gi
import click
from pathlib import Path
import os

gi.require_version("Tcam", "0.1")
gi.require_version("Gst", "1.0")

from gi.repository import Tcam, Gst


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
    Gst.init(sys.argv)  # init gstreamer

    # this line sets the gstreamer default logging level
    # it can be removed in normal applications
    # gstreamer logging can contain verry useful information
    # when debugging your application
    # see https://gstreamer.freedesktop.org/documentation/tutorials/basic/debugging-tools.html
    # for further details
    Gst.debug_set_default_threshold(Gst.DebugLevel.WARNING)

    serial = device_guid
    dims = tuple(map(int, dims.split(',')))

    # pipeline = Gst.parse_launch("tcambin name=bin"
    #                             " ! video/x-raw,format=BGRx,width=2048,height=1536,framerate=60/1"
    #                             " ! tee name=t"
    #                             " ! queue"
    #                             " ! videoconvert"
    #                             " ! ximagesink"
    #                             " t."
    #                             " ! queue"
    #                             " ! videoconvert"
    #                             " ! avimux"
    #                             " ! filesink name=fsink")

    # to save a video without live view reduce the pipeline to the following:

    pipeline = Gst.parse_launch(f"tcambin name=bin"
                                f" ! video/x-raw,format=BGRx,width={dims[0]},height={dims[1]},framerate={fps}/1"
                                f" ! videoconvert"
                                f" ! avimux"
                                f" ! filesink name=fsink")

    # serial is defined, thus make the source open that device
    if serial is not None:
        camera = pipeline.get_by_name("bin")
        camera.set_property("serial", serial)

    parent_dir = Path(video_output_path).parent

    if not os.path.isdir(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    file_location = video_output_path

    fsink = pipeline.get_by_name("fsink")
    fsink.set_property("location", file_location)

    pipeline.set_state(Gst.State.PLAYING)

    print("Press Ctrl-C to stop.")

    stop_time = duration + time.time()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        pipeline.set_state(Gst.State.NULL)


if __name__ == "__main__":
    main()
