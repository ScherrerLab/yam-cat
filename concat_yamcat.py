import numpy as np
from pathlib import Path
import cv2
from tqdm import tqdm
import click
import os
from warnings import warn
from typing import *

views = ['front', 'back', 'left', 'right']  # all the camera views
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

def merge(subdir: Path, fps: int):
    """
    Concatenates the videos from all the views into a single video and compresses using mp4v

    Parameters
    ----------
    subdir: Path
        full path to the dir that contains the vids for all the views
    fps: int
        framerate
    """
    # output filename for the merged vid
    merged_fname = subdir.joinpath(f'{subdir.stem}_merged.avi').as_posix()

    # skip if a file already exists with the merged filename
    if os.path.isfile(merged_fname):
        warn(f"Merged vid exists for following subdir, skipping: {subdir.stem}")
        return

    # store the VideoCapture objs for each view in a dict for convenience
    caps: Dict[str, cv2.VideoCapture] = dict.fromkeys(views)

    # create capture objects for each view
    for view in views:
        path = list(subdir.glob(f"{view}*"))[0]  # so that it's agnostic to .avi, .mp4 etc. whatever extension
        caps[view] = cv2.VideoCapture(path)

    # dicts to store each frame as they are read
    frame = dict.fromkeys(views)
    rval = dict.fromkeys(views)  # the boolean rval

    video_writer: cv2.VideoWriter = None

    while True:
        for view in views:  # read the frame for each view
            rval[view], frame[view] = caps[view].read()

            # if there is no frame from a view, assume the entire recording is finished
            if not rval[view]:  # when a video ends
                if video_writer is not None:
                    video_writer.release()  # release the video writer

                    for cap in list(caps.values()):  # release all the readers
                        cap.release()
                break  # exit the loop

        # create a video writer
        if video_writer is None:
            width = frame['front'].shape[0] + frame['back'].shape[0]
            height = frame['front'].shape[1] + frame['back'].shape[1]

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')

            video_writer = cv2.VideoWriter(
                subdir.joinpath(f'{subdir.stem}_merged.avi').as_posix(),
                fourcc,
                fps,
                (width, height),
                isColor=True
            )

        merged_frame = np.vstack(
            np.hstack(frame['front'], frame['back']),
            np.hstack(frame['left'],  frame['right'])
        )

        video_writer.write(cv2.cvtColor(merged_frame, cv2.COLOR_RGB2BGR))


@click.command()
@click.option('--parent-dir', type=str)
@click.option('--fps', type=str)
def main(parent_dir: str, fps: int):
    parent_dir = Path(parent_dir)

    for subdir in tqdm(parent_dir.glob('*')):
        if os.path.isfile(subdir):
            continue

        merge(subdir, fps)
