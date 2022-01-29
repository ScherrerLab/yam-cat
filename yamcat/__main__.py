import sys
import logging
from datetime import datetime
from PyQt5 import QtWidgets
from main_window import MainWindow


log_level = 'DEBUG'
log_format = "%(asctime)s %(levelname)s %(pathname)s %(lineno)s \n %(message)s "
log_file = f'/home/labuser/yamcat-logs/{datetime.now().strftime("%Y-%m-%d_%H.%M.%S-%f")}.ycl'

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

app = QtWidgets.QApplication([])

mw = MainWindow()
mw.show()

app.exec()
