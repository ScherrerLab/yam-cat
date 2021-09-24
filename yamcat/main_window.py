from PyQt5 import QtWidgets, QtGui, QtCore
from .mainwindow_pytemplate import Ui_MainWindow
import yaml
from pathlib import Path
from typing import *
from functools import wraps
import traceback
from logging import getLogger
from .utils import *


# from mesmerize qdialogs
def present_exceptions(title: str = 'error', msg: str = 'The following error occurred.'):
    """
    Use to catch exceptions and present them to the user in a QMessageBox warning dialog.
    The traceback from the exception is also shown.

    This decorator can be stacked on top of other decorators.

    Example:

    .. code-block: python

            @present_exceptions('Error loading file')
            @use_open_file_dialog('Choose file')
                def select_file(self, path: str, *args):
                    pass


    :param title:       Title of the dialog box
    :param msg:         Message to display above the traceback in the dialog box
    :param help_func:   A helper function which is called if the user clicked the "Help" button
    """

    def catcher(func):
        @wraps(func)
        def fn(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                tb = traceback.format_exc()

                mb = QtWidgets.QMessageBox()
                mb.setIcon(QtWidgets.QMessageBox.Warning)
                mb.setWindowTitle(title)
                mb.setText(msg)
                mb.setInformativeText(f"{e.__class__.__name__}: {e}")
                mb.setDetailedText(tb)
                mb.setStandardButtons(
                    QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Help
                )

                getLogger().info(
                    f"{e.__class__.__name__}: {e}\n"
                    f"{traceback.format_exc()}"
                )
        return fn
    return catcher


class CameraConfig():
    def __init__(self, guid: str, trigger_line: int, name: str = None):
        self.guid: str = guid
        self.trigger_line: int = trigger_line
        self.name: str = None


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.scan_cameras()
        self.ui.pushButtonReScanCameras.clicked.connect(self.scan_cameras)

        self.ui.listWidgetCameraName.itemChanged.connect(self.camera_config_changed)
        self.ui.listWidgetCameraName.itemClicked.connect(self.highlight_preview)

        self.ui.listWidgetCameraGUID.itemClicked.connect(self.highlight_preview)
        self.ui.listWidgetTriggerLine.itemClicked.connect(self.highlight_preview)

        self.camera_guids: List[str] = None

    def scan_cameras(self):
        self.camera_guids = get_basler_camera_guids()

        self.ui.listWidgetCameraGUID.clear()
        self.ui.listWidgetTriggerLine.clear()
        self.ui.listWidgetCameraName.clear()

        self.ui.listWidgetCameraGUID.addItems(self.camera_guids)

        # Use the config yaml to set default trigger lines for the cameras using their GUIDs
        for cg in self.camera_guids:
            self.ui.listWidgetTriggerLine.addItems(get_default_config()['camera_guids'][cg])

        # populate camera name list widget
        for i in range(len(self.camera_guids)):
            self.ui.listWidgetCameraGUID.addItem(str(i))

        # make them editable
        for item in self.ui.listWidgetCameraName.items():
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

        for item in self.ui.listWidgetCameraGUID.items():
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

        for item in self.ui.listWidgetTriggerLine.items():
            item.item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    def camera_config_changed(self):
        pass

    def help_filenames(self):
        pass

    def get_savedir(self) -> Path:
        parent_dir = self.ui.lineEditParentDir.text()
        subdir = self.ui.lineEditVideoSubDir.text()

        if self.ui.checkBoxNumericalSuffix.isChecked():
            suffix = self.ui.spinBoxNumericalSuffix
        else:
            suffix = ''

        savedir = Path(parent_dir).join(f'{subdir}-{suffix}')

        return savedir

    def record(self):
        pass

    def abort(self):
        pass

    def preview(self):
        pass

    def highlight_preview(self):
        pass
