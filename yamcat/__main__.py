import sys
from core import ArduinoTrigger, Acquire, Writer, Manager
from multiprocessing import Queue
import logging
from datetime import datetime


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

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(log_format)

root_logger = logging.getLogger()

root_logger.addHandler(console)
root_logger.addHandler(
    logging.StreamHandler(sys.stdout)
)
root_logger.addHandler(
    logging.StreamHandler(sys.stderr)
)


if __name__ == '__main__':
    q_left = Queue()
    q_right = Queue()

    arduino_trigger = ArduinoTrigger(address='/dev/ttyACM0', pin=9, fps=50)

    acquire_left = Acquire('left', q_left, fps=50, duration=60)
    acquire_right = Acquire('right', q_right, fps=50, duration=60)

    manager = Manager(apl=[acquire_left, acquire_right], arduino_trigger=arduino_trigger)

    writer_left = Writer(q_left, '/home/lab/vid_left.mp4', video_params=None)
    writer_right = Writer(q_right, '/home/lab/vid_right.mp4', video_params=None)

    writer_left.start()
    writer_right.start()

    acquire_left.start()
    acquire_right.start()

    arduino_trigger.start()

    manager.start()
