import sys
from core import ArduinoTrigger, Acquire, Writer, Manager
from multiprocessing import Queue
import logging
from datetime import datetime
from pypylon import pylon
import time

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


if __name__ == '__main__':
    q_left = Queue()
    q_right = Queue()

    arduino_trigger = ArduinoTrigger(address='/dev/ttyACM0', pin=10, fps=50)

    tlFactory = pylon.TlFactory.GetInstance()
    devices = tlFactory.EnumerateDevices()

    acquire_left = Acquire(devices[0], 'left', q_left, fps=50, duration=60, trigger_line=4)
    acquire_right = Acquire(devices[1], 'right', q_right, fps=50, duration=60, trigger_line=2)

    manager = Manager(apl=[acquire_left, acquire_right], arduino_trigger=arduino_trigger)

    writer_left = Writer('left', q_left, '/home/lab/vid_left.avi', video_params=None)
    writer_right = Writer('right', q_right, '/home/lab/vid_right.avi', video_params=None)

    writer_left.start()
    writer_right.start()

    acquire_left.start()
    # acquire_right.start()

    #arduino_trigger.start()

    root_logger.info("Sleeping")
    while True:
        time.sleep(1)

    # while all(map(lambda x: not x, [acquire_left.is_alive(), acquire_right.is_alive()])):
    #     time.sleep(1)

    root_logger.info("waiting for acquisition to finish")

    arduino_trigger.kill()
    root_logger.info('Killed ArduinoTrigger process')

