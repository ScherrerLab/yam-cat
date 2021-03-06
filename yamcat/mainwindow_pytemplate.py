# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './mainwindow_pytemplate.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(463, 918)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBoxHardware = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxHardware.setObjectName("groupBoxHardware")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBoxHardware)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBoxHardware)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_3.addWidget(self.label_12)
        self.lineEditArduinoAddress = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEditArduinoAddress.setObjectName("lineEditArduinoAddress")
        self.horizontalLayout_3.addWidget(self.lineEditArduinoAddress)
        self.pushButtonConnectArduino = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButtonConnectArduino.setCheckable(False)
        self.pushButtonConnectArduino.setObjectName("pushButtonConnectArduino")
        self.horizontalLayout_3.addWidget(self.pushButtonConnectArduino)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByMouse)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.verticalLayout_7.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBoxHardware)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.listWidgetCameraName = QtWidgets.QListWidget(self.groupBox_3)
        self.listWidgetCameraName.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.listWidgetCameraName.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.listWidgetCameraName.setAlternatingRowColors(True)
        self.listWidgetCameraName.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidgetCameraName.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidgetCameraName.setObjectName("listWidgetCameraName")
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraName.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraName.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraName.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraName.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraName.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraName.addItem(item)
        self.verticalLayout.addWidget(self.listWidgetCameraName)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.listWidgetCameraGUID = QtWidgets.QListWidget(self.groupBox_3)
        self.listWidgetCameraGUID.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.listWidgetCameraGUID.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.listWidgetCameraGUID.setAlternatingRowColors(True)
        self.listWidgetCameraGUID.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidgetCameraGUID.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidgetCameraGUID.setObjectName("listWidgetCameraGUID")
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraGUID.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraGUID.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraGUID.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraGUID.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraGUID.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidgetCameraGUID.addItem(item)
        self.verticalLayout_2.addWidget(self.listWidgetCameraGUID)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.pushButtonReScanCameras = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButtonReScanCameras.setObjectName("pushButtonReScanCameras")
        self.verticalLayout_4.addWidget(self.pushButtonReScanCameras)
        self.verticalLayout_7.addWidget(self.groupBox_3)
        self.verticalLayout_6.addWidget(self.groupBoxHardware)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_8.addWidget(self.label_8)
        self.spinBoxDuration = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxDuration.setEnabled(False)
        self.spinBoxDuration.setMinimum(1)
        self.spinBoxDuration.setMaximum(9999999)
        self.spinBoxDuration.setProperty("value", 60)
        self.spinBoxDuration.setObjectName("spinBoxDuration")
        self.horizontalLayout_8.addWidget(self.spinBoxDuration)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_8.addWidget(self.label_11)
        self.comboBoxVideoFormat = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxVideoFormat.setEnabled(False)
        self.comboBoxVideoFormat.setObjectName("comboBoxVideoFormat")
        self.comboBoxVideoFormat.addItem("")
        self.comboBoxVideoFormat.addItem("")
        self.comboBoxVideoFormat.addItem("")
        self.horizontalLayout_8.addWidget(self.comboBoxVideoFormat)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.verticalLayout_5.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.comboBoxFramerate = QtWidgets.QComboBox(self.groupBox)
        self.comboBoxFramerate.setObjectName("comboBoxFramerate")
        self.comboBoxFramerate.addItem("")
        self.comboBoxFramerate.addItem("")
        self.comboBoxFramerate.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBoxFramerate)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.comboBoxResolution = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxResolution.sizePolicy().hasHeightForWidth())
        self.comboBoxResolution.setSizePolicy(sizePolicy)
        self.comboBoxResolution.setObjectName("comboBoxResolution")
        self.comboBoxResolution.addItem("")
        self.comboBoxResolution.addItem("")
        self.horizontalLayout_4.addWidget(self.comboBoxResolution)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_5.addWidget(self.label_7)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setToolTip("")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_5.addWidget(self.label_9)
        self.lineEditParentDir = QtWidgets.QLineEdit(self.groupBox)
        self.lineEditParentDir.setObjectName("lineEditParentDir")
        self.horizontalLayout_5.addWidget(self.lineEditParentDir)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setToolTip("")
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_7.addWidget(self.label_10)
        self.lineEditVideoSubDir = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditVideoSubDir.sizePolicy().hasHeightForWidth())
        self.lineEditVideoSubDir.setSizePolicy(sizePolicy)
        self.lineEditVideoSubDir.setObjectName("lineEditVideoSubDir")
        self.horizontalLayout_7.addWidget(self.lineEditVideoSubDir)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setToolTip("")
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_2.addWidget(self.label_13)
        self.spinBoxNumericalSuffix = QtWidgets.QSpinBox(self.groupBox)
        self.spinBoxNumericalSuffix.setEnabled(True)
        self.spinBoxNumericalSuffix.setMinimum(-1)
        self.spinBoxNumericalSuffix.setMaximum(999)
        self.spinBoxNumericalSuffix.setProperty("value", 1)
        self.spinBoxNumericalSuffix.setObjectName("spinBoxNumericalSuffix")
        self.horizontalLayout_2.addWidget(self.spinBoxNumericalSuffix)
        self.checkBoxNumericalSuffix = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxNumericalSuffix.setChecked(True)
        self.checkBoxNumericalSuffix.setObjectName("checkBoxNumericalSuffix")
        self.horizontalLayout_2.addWidget(self.checkBoxNumericalSuffix)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_9.addWidget(self.label_14)
        self.labelPathStatus = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelPathStatus.setFont(font)
        self.labelPathStatus.setText("")
        self.labelPathStatus.setObjectName("labelPathStatus")
        self.horizontalLayout_9.addWidget(self.labelPathStatus)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem5)
        self.verticalLayout_5.addLayout(self.horizontalLayout_9)
        self.verticalLayout_6.addWidget(self.groupBox)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButtonPreview = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPreview.setEnabled(False)
        self.pushButtonPreview.setCheckable(True)
        self.pushButtonPreview.setObjectName("pushButtonPreview")
        self.horizontalLayout_6.addWidget(self.pushButtonPreview)
        self.pushButtonPrime = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPrime.setEnabled(False)
        self.pushButtonPrime.setCheckable(True)
        self.pushButtonPrime.setObjectName("pushButtonPrime")
        self.horizontalLayout_6.addWidget(self.pushButtonPrime)
        self.pushButtonRecord = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRecord.setEnabled(False)
        self.pushButtonRecord.setObjectName("pushButtonRecord")
        self.horizontalLayout_6.addWidget(self.pushButtonRecord)
        self.pushButtonAbort = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonAbort.setEnabled(False)
        self.pushButtonAbort.setObjectName("pushButtonAbort")
        self.horizontalLayout_6.addWidget(self.pushButtonAbort)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.verticalLayout_8.addLayout(self.verticalLayout_6)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 463, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEditArduinoAddress, self.pushButtonConnectArduino)
        MainWindow.setTabOrder(self.pushButtonConnectArduino, self.listWidgetCameraName)
        MainWindow.setTabOrder(self.listWidgetCameraName, self.listWidgetCameraGUID)
        MainWindow.setTabOrder(self.listWidgetCameraGUID, self.pushButtonReScanCameras)
        MainWindow.setTabOrder(self.pushButtonReScanCameras, self.spinBoxDuration)
        MainWindow.setTabOrder(self.spinBoxDuration, self.comboBoxVideoFormat)
        MainWindow.setTabOrder(self.comboBoxVideoFormat, self.comboBoxFramerate)
        MainWindow.setTabOrder(self.comboBoxFramerate, self.comboBoxResolution)
        MainWindow.setTabOrder(self.comboBoxResolution, self.lineEditParentDir)
        MainWindow.setTabOrder(self.lineEditParentDir, self.lineEditVideoSubDir)
        MainWindow.setTabOrder(self.lineEditVideoSubDir, self.spinBoxNumericalSuffix)
        MainWindow.setTabOrder(self.spinBoxNumericalSuffix, self.checkBoxNumericalSuffix)
        MainWindow.setTabOrder(self.checkBoxNumericalSuffix, self.pushButtonPreview)
        MainWindow.setTabOrder(self.pushButtonPreview, self.pushButtonPrime)
        MainWindow.setTabOrder(self.pushButtonPrime, self.pushButtonRecord)
        MainWindow.setTabOrder(self.pushButtonRecord, self.pushButtonAbort)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "yam-cat | Yet Another Multi Camera Acquisition Tool"))
        self.groupBoxHardware.setTitle(_translate("MainWindow", "Hardware Params"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Arduino"))
        self.label_12.setText(_translate("MainWindow", "Arduino Address:"))
        self.lineEditArduinoAddress.setPlaceholderText(_translate("MainWindow", "/dev/ttyX"))
        self.pushButtonConnectArduino.setText(_translate("MainWindow", "Connect"))
        self.label_3.setText(_translate("MainWindow", "Ususually something like:\n"
"\n"
"/dev/ttyACM0\n"
"\n"
"Running this in the terminal can help you find the right address:\n"
"\n"
"ll /dev/ttyACM*"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Camera"))
        self.label.setToolTip(_translate("MainWindow", "Give a name for the cameras, the camera name is used as a prefix for the video files.\n"
"You may drag and drop items in this list so that camera names and GUIDs correspond."))
        self.label.setText(_translate("MainWindow", "Camera Name"))
        self.listWidgetCameraName.setToolTip(_translate("MainWindow", "<html><head/><body><p>Give a name for the cameras, the camera name is used as a prefix for the video files.</p></body></html>"))
        __sortingEnabled = self.listWidgetCameraName.isSortingEnabled()
        self.listWidgetCameraName.setSortingEnabled(False)
        item = self.listWidgetCameraName.item(0)
        item.setText(_translate("MainWindow", "a"))
        item = self.listWidgetCameraName.item(1)
        item.setText(_translate("MainWindow", "b"))
        item = self.listWidgetCameraName.item(2)
        item.setText(_translate("MainWindow", "c"))
        item = self.listWidgetCameraName.item(3)
        item.setText(_translate("MainWindow", "d"))
        item = self.listWidgetCameraName.item(4)
        item.setText(_translate("MainWindow", "e"))
        item = self.listWidgetCameraName.item(5)
        item.setText(_translate("MainWindow", "f"))
        self.listWidgetCameraName.setSortingEnabled(__sortingEnabled)
        self.label_2.setToolTip(_translate("MainWindow", "<html><head/><body><p>Unique hardware identifier for the camera.</p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Camera GUID"))
        self.listWidgetCameraGUID.setToolTip(_translate("MainWindow", "<html><head/><body><p>Unique hardware identifier for the camera.</p></body></html>"))
        __sortingEnabled = self.listWidgetCameraGUID.isSortingEnabled()
        self.listWidgetCameraGUID.setSortingEnabled(False)
        item = self.listWidgetCameraGUID.item(0)
        item.setText(_translate("MainWindow", "u"))
        item = self.listWidgetCameraGUID.item(1)
        item.setText(_translate("MainWindow", "v"))
        item = self.listWidgetCameraGUID.item(2)
        item.setText(_translate("MainWindow", "w"))
        item = self.listWidgetCameraGUID.item(3)
        item.setText(_translate("MainWindow", "x"))
        item = self.listWidgetCameraGUID.item(4)
        item.setText(_translate("MainWindow", "y"))
        item = self.listWidgetCameraGUID.item(5)
        item.setText(_translate("MainWindow", "z"))
        self.listWidgetCameraGUID.setSortingEnabled(__sortingEnabled)
        self.pushButtonReScanCameras.setToolTip(_translate("MainWindow", "Re-scan for cameras if you\'ve connected/disconnected cameras."))
        self.pushButtonReScanCameras.setText(_translate("MainWindow", "Re-scan cameras"))
        self.groupBox.setTitle(_translate("MainWindow", "Recording Params"))
        self.label_8.setText(_translate("MainWindow", "Duration:"))
        self.spinBoxDuration.setSuffix(_translate("MainWindow", " seconds"))
        self.label_11.setText(_translate("MainWindow", "Video format:"))
        self.comboBoxVideoFormat.setItemText(0, _translate("MainWindow", "raw"))
        self.comboBoxVideoFormat.setItemText(1, _translate("MainWindow", "h264"))
        self.comboBoxVideoFormat.setItemText(2, _translate("MainWindow", "h265"))
        self.label_4.setText(_translate("MainWindow", "Framerate:"))
        self.comboBoxFramerate.setItemText(0, _translate("MainWindow", "30"))
        self.comboBoxFramerate.setItemText(1, _translate("MainWindow", "60"))
        self.comboBoxFramerate.setItemText(2, _translate("MainWindow", "120"))
        self.label_6.setText(_translate("MainWindow", "Resolution:"))
        self.comboBoxResolution.setItemText(0, _translate("MainWindow", "2048x1536"))
        self.comboBoxResolution.setItemText(1, _translate("MainWindow", "1920x1080"))
        self.label_7.setText(_translate("MainWindow", "Save path"))
        self.label_5.setText(_translate("MainWindow", "The final filename will look like this:\n"
"\n"
"parent_dir/subdir-suffix/camera-name.avi"))
        self.label_9.setText(_translate("MainWindow", "Parent dir:"))
        self.lineEditParentDir.setToolTip(_translate("MainWindow", "This would be for something like an overarching experiment."))
        self.lineEditParentDir.setText(_translate("MainWindow", "/home/labuser/"))
        self.lineEditParentDir.setPlaceholderText(_translate("MainWindow", "/path/to/parent_dir"))
        self.label_10.setText(_translate("MainWindow", "Subdir name:"))
        self.lineEditVideoSubDir.setToolTip(_translate("MainWindow", "This is a subdir that is created under parent dir.\n"
"For something like \"mouse\""))
        self.label_13.setText(_translate("MainWindow", "Subdir suffix:"))
        self.spinBoxNumericalSuffix.setToolTip(_translate("MainWindow", "This will add a numerical suffix to the subdir.\n"
"Useful for something like mosue ID\n"
"\n"
"Disabled if set to -1"))
        self.checkBoxNumericalSuffix.setToolTip(_translate("MainWindow", "Automatically increment this number after each recording"))
        self.checkBoxNumericalSuffix.setText(_translate("MainWindow", "Auto-increment"))
        self.label_14.setToolTip(_translate("MainWindow", "This examines the all the path params (parent dir, subdir, suffix) and validates them live."))
        self.label_14.setText(_translate("MainWindow", "Path status:"))
        self.pushButtonPreview.setText(_translate("MainWindow", "Preview"))
        self.pushButtonPrime.setToolTip(_translate("MainWindow", "Get the camera ready for recording"))
        self.pushButtonPrime.setText(_translate("MainWindow", "Prime"))
        self.pushButtonRecord.setText(_translate("MainWindow", "Record"))
        self.pushButtonAbort.setText(_translate("MainWindow", "Abort"))
