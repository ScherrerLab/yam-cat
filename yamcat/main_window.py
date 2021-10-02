from PyQt5 import QtWidgets, QtGui, QtCore
from .mainwindow_pytemplate import Ui_MainWindow
from pathlib import Path
from typing import *
from functools import wraps
import traceback
from logging import getLogger
from .utils import *
from .params import CameraConfig, Params
from .core import Operator


MODE_ARDUINO_CONNECTED = 'MODE_ARDUINO_CONNECTED'
MODE_START_PREVIEW = 'MODE_START_PREVIEW'
MODE_END_PREVIEW = 'MODE_END_PREVIEW'
MODE_PRIMED = 'MODE_PRIMED'
MODE_DE_PRIME = 'MODE_DE_PRIME'
MODE_RECORD = 'MODE_RECORD'
MODE_RECORD_FINISHED = 'MODE_RECORD_FINISHED'


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


def unpack_args(params: dict):
    return [
        arg for arggroup in [
            arggroup.split(' ') for arggroup in [
                f'--{k} {v}' for (k, v) in params.items()
            ]
        ] for arg in arggroup
    ]


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.operator = Operator()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.scan_cameras()
        self.ui.pushButtonReScanCameras.clicked.connect(self.scan_cameras)

        self.ui.listWidgetCameraName.itemChanged.connect(self.camera_config_changed)
        self.ui.listWidgetCameraName.itemClicked.connect(self.highlight_preview)

        self.ui.listWidgetCameraGUID.itemClicked.connect(self.highlight_preview)
        self.ui.listWidgetTriggerLine.itemClicked.connect(self.highlight_preview)

        self.ui.lineEditArduinoAddress.setText(get_default_config()['arduino']['address'])

    def scan_cameras(self):
        self.ui.listWidgetCameraGUID.clear()
        self.ui.listWidgetTriggerLine.clear()
        self.ui.listWidgetCameraName.clear()

        self.ui.listWidgetCameraGUID.addItems(self.operator.camera_guids)

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

    def set_ui_mode(self, mode: str):
        if mode == MODE_ARDUINO_CONNECTED:
            self.ui.pushButtonPreview.setEnabled(True)
            self.ui.pushButtonPrime.setEnabled(True)
            self.ui.pushButtonRecord.setEnabled(False)
            self.ui.pushButtonAbort.setEnabled(False)

        if mode == MODE_START_PREVIEW:
            self.ui.pushButtonPreview.setEnabled(True)
            self.ui.pushButtonPreview.setText('End Preview')
            self.ui.pushButtonPreview.setChecked(True)
            self.ui.pushButtonPrime.setEnabled(False)
            self.ui.pushButtonRecord.setEnabled(False)
            self.ui.pushButtonAbort.setEnabled(False)

        if mode == MODE_END_PREVIEW:
            self.ui.pushButtonPreview.setEnabled(True)
            self.ui.pushButtonPreview.setText('Preview')
            self.ui.pushButtonPreview.setChecked(False)
            self.ui.pushButtonPrime.setEnabled(True)
            self.ui.pushButtonRecord.setEnabled(False)
            self.ui.pushButtonAbort.setEnabled(False)

        if mode == MODE_PRIMED:
            self.ui.pushButtonPreview.setEnabled(False)
            self.ui.pushButtonPrime.setEnabled(True)
            self.ui.pushButtonPrime.setText('De-Prime')
            self.ui.pushButtonPrime.setChecked(True)
            self.ui.pushButtonRecord.setEnabled(True)
            self.ui.pushButtonAbort.setEnabled(False)

        if mode == MODE_DE_PRIME:
            self.ui.pushButtonPreview.setEnabled(False)
            self.ui.pushButtonPrime.setEnabled(True)
            self.ui.pushButtonPrime.setText('Prime')
            self.ui.pushButtonPrime.setChecked(False)
            self.ui.pushButtonRecord.setEnabled(False)
            self.ui.pushButtonAbort.setEnabled(False)

        if mode == MODE_RECORD:
            self.ui.pushButtonPreview.setEnabled(False)
            self.ui.pushButtonPrime.setEnabled(False)
            self.ui.pushButtonRecord.setEnabled(False)
            self.ui.pushButtonAbort.setEnabled(True)

        if mode == MODE_RECORD_FINISHED:
            self.ui.pushButtonPreview.setEnabled(True)
            self.ui.pushButtonPrime.setEnabled(True)
            self.ui.pushButtonRecord.setEnabled(False)
            self.ui.pushButtonAbort.setEnabled(False)

            if self.ui.checkBoxNumericalSuffix.isChecked():
                self.ui.spinBoxNumericalSuffix.setValue(
                    self.ui.spinBoxNumericalSuffix.value() + 1
                )

    def connect_arduino(self):
        self.operator.params = self.get_params()
        self.operator.connect_arduino(
            self.operator.params.arduino_address
        )

        self.set_ui_mode(MODE_ARDUINO_CONNECTED)

    @present_exceptions('Camera Config Error', 'Error setting camera configuration')
    def get_camera_configs(self, *args, **kwargs) -> List[CameraConfig]:
        camera_configs = []
        for ix in self.ui.listWidgetCameraGUID.count():
            guid = self.ui.listWidgetCameraGUID.item(ix).text()
            name = self.ui.listWidgetCameraName.item(ix).text()
            trigger_line = self.ui.listWidgetTriggerLine.item(ix).text()

            if name == '':
                raise KeyError(
                    f'`Camera Name` not defined for camera with GUID:\n{guid}\n\n'
                    f'Please enter a camera name for all cameras.'
                )

            if trigger_line == '':
                raise KeyError(
                    f'`Trigger Line` not defined for camera with GUID:\n{guid}\n\n'
                    f'Please enter the numerical trigger line for all cameras.'
                )

            try:
                trigger_line = int(trigger_line)
            except TypeError:
                raise TypeError(
                    f'`Trigger Line` for camera with the following GUID must be an integer number:\n{guid}\n\n'
                    f'Please enter a numerical trigger line for all cameras. You have entered:\n{trigger_line}'
                )

            camera_configs.append(
                CameraConfig(name=name, guid=guid, trigger_line=trigger_line)
            )

        return camera_configs

    @present_exceptions('Parameters error', 'Error validating parameters')
    def get_params(self, *args, **kwargs):
        params = Params(
            arduino_address=self.ui.lineEditArduinoAddress.text(),
            camera_configs=self.get_camera_configs(),
            duration=self.ui.spinBoxDuration.value(),
            video_format=self.ui.comboBoxVideoFormat.currentText(),
            framerate=self.ui.spinBoxFramerate.value(),
            width=self.ui.spinBoxWidth.value(),
            height=self.ui.spinBoxHeight.value(),
            parent_dir=self.ui.lineEditParentDir.value(),
            auto_create_subdirs=self.ui.checkBoxNumericalSuffix.isChecked(),
            auto_create_subdirs_index=self.ui.spinBoxNumericalSuffix(),
            video_subdir=self.ui.lineEditVideoSubDir.text()
        )

        return params

    def prime(self):
        self.operator.params = self.get_params()
        self.operator.prime()
        self.set_ui_mode(MODE_PRIMED)

    def record(self):
        self.operator.record()
        self.set_ui_mode(MODE_RECORD)

    def record_finished(self):
        self.set_ui_mode(MODE_RECORD_FINISHED)

    def abort(self):
        self.operator.abort_record()
        self.set_ui_mode(MODE_DE_PRIME)
        self.set_ui_mode(MODE_ARDUINO_CONNECTED)

    def start_preview(self):
        pass

    def end_preview(self):
        pass

    def highlight_preview(self):
        pass
