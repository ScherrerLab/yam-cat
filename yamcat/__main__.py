import sys
from core import ArduinoTrigger, Acquire, Writer, Manager
from multiprocessing import Queue
import logging
from datetime import datetime
from pypylon import pylon
import time
import subprocess
import os


log_level = 'DEBUG'
log_format = "%(asctime)s %(levelname)s %(pathname)s %(lineno)s \n %(message)s "
log_file = f'/home/lab/{datetime.now().strftime("%Y-%m-%d_%H.%M.%S-%f")}.ycl'

logging.basicConfig(
    level=log_level,
    format=log_format,
    filename=log_file,
    filemode='w'
)


def exception_hook(exc_type, exc_value, traceback):
    logging.error("EXCEPTION ENCOUNTERED", exc_info=(exc_type, exc_value, traceback))


sys.excepthook = exception_hook

# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# console.setFormatter(log_format)

root_logger = logging.getLogger()

# root_logger.addHandler(console)
root_logger.addHandler(
    logging.StreamHandler(sys.stdout)
)
root_logger.addHandler(
    logging.StreamHandler(sys.stderr)
)


def unpack_args(params: dict):
    return [
        arg for arggroup in [
            arggroup.split(' ') for arggroup in [
                f'--{k} {v}' for (k, v) in params.items()
            ]
        ] for arg in arggroup
    ]


if __name__ == '__main__':
    q_left = Queue()
    q_right = Queue()

    arduino_trigger = ArduinoTrigger(address='/dev/ttyACM0', pin=10, fps=50)

    tlFactory = pylon.TlFactory.GetInstance()
    devices = tlFactory.EnumerateDevices()

    guids = ['2676016BC31A', '267601CA59E7']
    trigger_lines = [4, 2]

    acquire_params_left = \
        {
            'device-guid':  guids[0],
            'camera-name':  'left',
            'fps':          50,
            'duration':     60,
            'trigger-line': trigger_lines[0],
            'video-output-path': '/home/lab/vidleft.avi',
            'fourcc':       'mp4v',
            'dims':         '1024,1024'
        }

    acquire_params_right = acquire_params_left.copy()
    acquire_params_right.update(
        {
            'device-guid': guids[1],
            'camera-name': 'right',
            'trigger-line': trigger_lines[1],
            'video-output-path': '/home/lab/vidright.avi',
        }
    )

    args_left = unpack_args(acquire_params_left)
    args_right = unpack_args(acquire_params_right)

    acquire_subproc_path = '/home/lab/repos/yam-cat/yamcat/acquire_subprocess.py'

    # subprocess.run(['/home/lab/python-venvs/yamcat/bin/python',
    #                 acquire_subproc_path] + args_left, capture_output=True)
    # subprocess.run(['/home/lab/python-venvs/yamcat/bin/python',
    #                 acquire_subproc_path] + args_right, capture_output=True)

    subprocess.Popen(
        ['python', acquire_subproc_path] + args_left, env=os.environ.copy()
    )

    subprocess.Popen(
        ['python', acquire_subproc_path] + args_right, env=os.environ.copy()
    )

    time.sleep(5)

    arduino_trigger.start()
    #
    # root_logger.info("Sleeping")
    # while True:
    #     time.sleep(1)
    #
    # # while all(map(lambda x: not x, [acquire_left.is_alive(), acquire_right.is_alive()])):
    # #     time.sleep(1)
    #
    # root_logger.info("waiting for acquisition to finish")
    #
    # arduino_trigger.kill()
    # root_logger.info('Killed ArduinoTrigger process')
    #
