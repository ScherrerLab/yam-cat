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


def get_basler_camera_serial_numbers() -> List[int]:
    tlFactory = pylon.TlFactory.GetInstance()
    devices = tlFactory.EnumerateDevices()

    serial_numbers = [int(dev.GetSerialNumber()) for dev in devices]

    return serial_numbers


def get_default_config() -> dict:
    return yaml.safe_load(
        open(Path(__file__).parent.joinpath('config.yaml'), 'r')
    )


def get_acquire_subprocess_path() -> str:
    return f'{Path(__file__).parent.joinpath("acquire_subprocess.py")}'
