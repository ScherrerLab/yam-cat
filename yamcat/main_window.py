from PyQt5 import QtWidgets, QtGui, QtCore
from mainwindow_pytemplate import Ui_MainWindow
from pathlib import Path
from typing import *
from functools import wraps
import traceback
from logging import getLogger
from utils import *
from params import CameraConfig, Params
from core import Operator
import os


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

        self.ui.lineEditArduinoAddress.setText(get_default_config()['arduino']['address'])
        self.ui.pushButtonConnectArduino.clicked.connect(self.connect_arduino)

        self.ui.comboBoxVideoFormat.addItems(list(get_default_config()['video-formats'].keys()))

        self.ui.lineEditParentDir.textEdited.connect(self.validate_path)
        self.ui.lineEditVideoSubDir.textEdited.connect(self.validate_path)
        self.ui.spinBoxNumericalSuffix.valueChanged.connect(self.validate_path)

        self.ui.pushButtonPrime.clicked.connect(self.prime)
        self.ui.pushButtonRecord.clicked.connect(self.record)
        self.ui.pushButtonAbort.clicked.connect(self.abort)

    def scan_cameras(self):
        self.ui.listWidgetCameraGUID.clear()
        self.ui.listWidgetCameraName.clear()

        self.ui.listWidgetCameraGUID.addItems(self.operator.camera_guids)

        # populate camera name and GUID list widget
        for i in range(len(self.operator.camera_guids)):
            self.ui.listWidgetCameraName.addItem('')

        # TODO: make them editable
        for ix in range(len(self.operator.camera_guids)):
            item_cam_name = self.ui.listWidgetCameraName.item(ix)
            guid = self.operator.camera_guids[ix]
            cam_name = self.operator.camera_names[guid]
            item_cam_name.setText(cam_name)

    def camera_config_changed(self):
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
        for ix in range(0, self.ui.listWidgetCameraGUID.count()):
            guid = self.ui.listWidgetCameraGUID.item(ix).text()
            name = self.ui.listWidgetCameraName.item(ix).text()

            if name == '':
                raise KeyError(
                    f'`Camera Name` not defined for camera with GUID:\n{guid}\n\n'
                    f'Please enter a camera name for all cameras.'
                )

            camera_configs.append(
                CameraConfig(name=name, guid=guid, trigger_line=0)
            )

        return camera_configs

    @present_exceptions('Parameters error', 'Error validating parameters')
    def get_params(self, *args, **kwargs):
        dims = self.ui.comboBoxResolution.currentText().split('x')

        params = Params(
            arduino_address=self.ui.lineEditArduinoAddress.text(),
            camera_configs=self.get_camera_configs(),
            duration=self.ui.spinBoxDuration.value(),
            video_format=self.ui.comboBoxVideoFormat.currentText(),
            framerate=self.ui.comboBoxFramerate.currentText(),
            width=dims[0],
            height=dims[1],
            destination_dir=self._construct_full_destination_dir()
        )

        return params

    def _construct_full_destination_dir(self) -> Path:
        parent_dir = self.ui.lineEditParentDir.text()
        num_subdir_suffix = self.ui.spinBoxNumericalSuffix.value()

        if num_subdir_suffix > -1:
            subdir_suffix = '-' + str(num_subdir_suffix)
        else:
            subdir_suffix = ''

        video_subdir = self.ui.lineEditVideoSubDir.text()

        return Path(os.path.join(parent_dir, f'{video_subdir}{subdir_suffix}'))

    def validate_path(self):
        """
        Validate the path to the dir to save the videos to make sure videos aren't overwritten
        """

        if self.operator.arduino_trigger is None:
            return

        path = self._construct_full_destination_dir()
        if path.is_dir():
            self.ui.labelPathStatus.setText("<b>Path exists! Change parent dir + subdir combination.</b>")
            self.ui.pushButtonPrime.setEnabled(False)
        else:
            self.ui.labelPathStatus.setText("<b>Path is ok!</b>")
            self.ui.pushButtonPrime.setEnabled(True)

    @present_exceptions()
    def prime(self, *args, **kwargs):
        if self.ui.lineEditParentDir.text() == '':
            raise ValueError("You must set a parent dir")

        if self.ui.lineEditVideoSubDir.text() == '':
            raise ValueError("You must set a subdir")

        self.operator.params = self.get_params()
        self.operator.arduino_trigger.set_fps(
            self.operator.params.framerate
        )
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

        if self.ui.checkBoxNumericalSuffix.isChecked():
            self.ui.spinBoxNumericalSuffix.setValue(
                self.ui.spinBoxNumericalSuffix.value() + 1
            )

    def start_preview(self):
        pass

    def end_preview(self):
        pass

    def highlight_preview(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec()
