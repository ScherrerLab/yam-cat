from typing import *
import yaml
from pathlib import Path
import sys
import gi

gi.require_version("Gst", "1.0")
gi.require_version("Tcam", "0.1")

from gi.repository import GLib, GObject, Gst, Tcam


def get_tiscam_serial_numbers():
    """
    Print information about all  available devices
    """

    Gst.init([])

    sample_pipeline = Gst.parse_launch("tcambin name=source ! fakesink")

    if not sample_pipeline:
        print("Unable to create pipeline")
        sys.exit(1)

    source = sample_pipeline.get_by_name("source")

    serials = source.get_device_serials_backend()

    serials = [s.split('-')[0] for s in serials]

    return serials


# def get_basler_camera_guids() -> List[str]:
#     """
#     Returns
#     -------
#     List[str]
#         List of GUIDs for each of the basler cameras
#     """
#     tlFactory = pylon.TlFactory.GetInstance()
#     devices = tlFactory.EnumerateDevices()
#
#     guids = [dev.GetDeviceGUID() for dev in devices]
#
#     return guids
#
#
# def get_basler_camera_serial_numbers() -> List[int]:
#     """
#     Returns
#     -------
#     List[int]
#         List of serial numbers for each of the basler cams
#     """
#     tlFactory = pylon.TlFactory.GetInstance()
#     devices = tlFactory.EnumerateDevices()
#
#     serial_numbers = [int(dev.GetSerialNumber()) for dev in devices]
#
#     return serial_numbers


def get_default_config() -> dict:
    """
    Returns
    -------
    dict
        Default configuration of for yamcat from the yaml file.
    """
    return yaml.safe_load(
        open(Path(__file__).parent.joinpath('config.yaml'), 'r')
    )


def get_acquire_subprocess_path() -> str:
    return f'{Path(__file__).parent.joinpath("save_stream.py")}'
