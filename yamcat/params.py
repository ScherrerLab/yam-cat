from typing import *
from pathlib import Path
import os
from utils import get_default_config


class CameraConfig():
    def __init__(
            self,
            guid: str,
            name: str,
            trigger_line: int = -1,
    ):
        """
        Camera configuration parameters
        Parameters
        ----------
        guid: str
            Camera GUID

        trigger_line: int
            Trigger line that the camera expects the trigger signal from

        name: str
            User defined camera name

        preview_position: tuple
            WIP
        preview_size: tuple
            WIP
        """
        self.name: str = name
        self.guid: str = guid
        self.trigger_line: int = trigger_line
        # self.preview_position = tuple(map(int, preview_position))
        # self.preview_size = tuple(map(int, preview_size))

    def __repr__(self):
        return f"name: {self.name}\n" \
               f"guid: {self.guid}\n" \
               f"trigger_line: {self.trigger_line}\n"


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
            destination_dir: Union[Path, str],
    ):
        """
        All parameters for multi-camera acquisition.

        Parameters
        ----------
        arduino_address: str
            Address to the arduino, example: `/dev/ttyACM0`

        camera_configs: List[CameraConfig]
            List of CameraConfig instances that correspond to each camera

        duration: int
            Acquisition duration in seconds

        video_format: str
            Video format, just the fourcc specification

        framerate: int
            framerate for acquisition & playback

        width: int
            Video with used for all cameras

        height: int
            Video height used for all cameras

        destination_dir: str
            Directory within which to store videos from each camera
        """
        if not os.path.exists(arduino_address):
            raise FileNotFoundError(f'Arduino address is not valid:\n{arduino_address}')
        else:
            self.arduino_address: str = arduino_address

        self.camera_configs: List[CameraConfig] = camera_configs

        self.duration: int = duration
        self.video_format: str = video_format
        self.framerate: int = int(framerate)
        self.width: int = width
        self.height: int = height

        # if not os.access(parent_dir, os.):
        #     raise PermissionError(
        #         f'You do not have permission to write to the specified parent directory:\n{parent_dir}'
        #     )
        #
        # else:

        self.destination_dir: Path = Path(destination_dir)

        self.video_extension = get_default_config()['video-formats'][self.video_format]

    def get_camera_config(self, name: str = None, guid: str = None) -> CameraConfig:
        """
        Get the `CameraConfig` instance by specifying either the user-defined camera name or the camera GUID

        Returns
        -------
        CameraConfig
        """
        if (name == None) and (guid == None):
            raise ValueError('Must specify `name` or `guid` of camera')

        if guid is not None:
            for camera_config in self.camera_configs:
                if getattr(camera_config, 'guid') == guid:
                    return camera_config
        else:
            for camera_config in self.camera_configs:
                if getattr(camera_config, 'name') == name:
                    return camera_config

        raise KeyError('Camera config not found with given information')

    def get_device_guids(self) -> List[str]:
        """
        Get a list of GUIDs for all currently connected cameras
        """
        guids = []
        for camera_config in self.camera_configs:
            guids.append(camera_config.guid)

        return guids

    def to_dict(self, device_guid: str) -> dict:
        """
        Get the parameters organized as a dictionary for one specific camera

        Parameters
        ----------
        device_guid: str
            The device for which to return the parameters along with the corresponding CameraConfig parameters

        Returns
        -------
        dict
            Parameters organized in a dictionary
        """
        camera_config = self.get_camera_config(guid=device_guid)

        d = \
            {
                'device-guid': device_guid,
                'camera-name': camera_config.name,
                'trigger-line': camera_config.trigger_line,
                # 'preview-position': f'{camera_config.preview_position[0]},{camera_config.preview_position[1]}',
                # 'preview-size': f'{camera_config.preview_size[0]},{camera_config.preview_size[1]}',
                'fps': self.framerate,
                'duration': self.duration,
                'video-output-path': self.destination_dir.joinpath(f'{camera_config.name}.{self.video_extension}'),
                'fourcc': self.video_format,
                'dims': f'{self.width},{self.height}'
            }

        return d

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
