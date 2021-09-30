from typing import *
from pathlib import Path
import os


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

        self.camera_configs: List[CameraConfig]

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
            self.auto_create_subdirs_index: int = auto_create_subdirs
        else:
            self.auto_create_subdirs_index = None

        self.video_subdir: str = video_subdir

        self.destination_dir: Path = Path(
            os.path.join(self.parent_dir, video_subdir)
        )
