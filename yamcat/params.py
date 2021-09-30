from typing import *
from pathlib import Path
import os
from .utils import get_default_config


class CameraConfig():
    def __init__(self, guid: str, trigger_line: int, name: str = None):
        self.name: str = None
        self.guid: str = guid
        self.trigger_line: int = trigger_line


class Params():
    def __init__(
            self,
            arduino_address: str,
            camera_configs: List[CameraConfig],
            duration: int,
            video_format: str,
            framerate: int,
            width: int,
            height: int,
            parent_dir: str,
            auto_create_subdirs: bool,
            auto_create_subdirs_index: int,
            video_subdir: str
    ):
        if not os.path.isfile(arduino_address):
            raise FileNotFoundError(f'Arduino address is not valid:\n{arduino_address}')
        else:
            self.arduino_address: str = arduino_address

        self.camera_configs: List[CameraConfig] = camera_configs

        self.duration: int = duration
        self.video_format: str = video_format
        self.framerate: int = framerate
        self.width: int = width
        self.height: int = height

        if not os.access(parent_dir, os.W_OK):
            raise PermissionError(
                f'You do not have permission to write to the specified parent directory:\n{parent_dir}'
            )

        else:
            if not os.path.isdir(parent_dir):
                os.makedirs(parent_dir, exist_ok=True)

            self.parent_dir: str = parent_dir

        self.auto_create_subdirs: bool = auto_create_subdirs
        if auto_create_subdirs_index:
            self.auto_create_subdirs_index: str = '-' + str(auto_create_subdirs)
        else:
            self.auto_create_subdirs_index: str = ''

        self.video_subdir: str = video_subdir

        self.destination_dir: Path = Path(
            os.path.join(self.parent_dir, f'{video_subdir}{self.auto_create_subdirs_index}')
        )

        self.video_extension = get_default_config()[self.video_format]

    def get_camera_config(self, name: str = None, guid: str = None):
        if (name == None) and (guid == None):
            raise ValueError('Must specify `name` or `guid` of camera')

        if guid is not None:
            name = None
            attr = 'guid'
        else:
            attr = 'name'

        for camera_config in self.camera_configs:
            if getattr(self.camera_configs, attr) == locals()[attr]:
                return camera_config

        return KeyError('Camera config not found with given information')

    def get_device_guids(self) -> List[str]:
        guids = []
        for camera_config in self.camera_configs:
            guids.append(camera_config.guid)

        return guids

    def to_dict(self, device_guid: str) -> dict:
        camera_config = self.get_camera_config(guid=device_guid)

        d = \
            {
                'device-guid': device_guid,
                'camera-name': camera_config.name,
                'trigger-line': camera_config.trigger_line,
                'fps': self.framerate,
                'duration': self.duration,
                'video-output-path': self.destination_dir.joinpath(f'{camera_config.name}.{self.video_extension}'),
                'fourcc': self.video_format,
                'dims': f'{self.width},{self.height}'
            }

    def to_args(self, params_dict: dict) -> List[str]:
        """
        Parameters
        ----------
        params_dict: dict
            params dict returned by Params.to_dict()

        Returns
        -------
        List[str]
            Returns a list of args formatted for the acquire_subprocess

        """

        return [
            arg for arggroup in [
                arggroup.split(' ') for arggroup in [
                    f'--{k} {v}' for (k, v) in params_dict.items()
                ]
            ] for arg in arggroup
        ]
