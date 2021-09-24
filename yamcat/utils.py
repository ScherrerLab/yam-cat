from pypylon import pylon
from typing import *
import yaml
from pathlib import Path


def get_basler_camera_guids() -> List[str]:
    """

    Returns
    -------
    List of GUIDs for each of the basler cameras
    """
    tlFactory = pylon.TlFactory.GetInstance()
    devices = tlFactory.EnumerateDevices()

    guids = [dev.GetDeviceGUID() for dev in devices]

    return guids


def get_default_config() -> dict:
    return yaml.load(Path(__file__).parent.joinpath('config.yaml'))
