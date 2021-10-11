from PyQt5 import QtCore, QtWidgets
from multiprocessing import Process, Queue
import numpy as np
import pyqtgraph as pg
import VideoTemplate_pytemplate as ui_template
from threading import Thread
from PyQt5.QtCore import QProcess, QThread


class VideoDisplay(QThread):
    def __init__(self):
        QThread.__init__(self)
        # QThread.__init__(self)
        # super(VideoDisplay, self).__init__()

        self.app = pg.mkQApp("Video Speed Test Example")

        self.win = QtWidgets.QMainWindow()
        self.ui = ui_template.Ui_MainWindow()
        self.ui.setupUi(self.win)
        self.win.show()

        self.vb = pg.ViewBox()
        self.ui.graphicsView.setCentralItem(self.vb)
        self.vb.setAspectLocked()
        self.img = pg.ImageItem()
        self.vb.addItem(self.img)

    def make_data(self) -> np.ndarray:
        return np.random.rand(1024, 1024)

    def update(self):
        self.img.setImage(self.make_data())
        self.ui.stack.setCurrentIndex(0)
        self.app.processEvents()

    def run(self) -> None:
        while True:
            self.update()
        # timer = QtCore.QTimer()
        # timer.timeout.connect(self.update)
        # timer.start(0)


preview = VideoDisplay()
preview.start()
preview.app.exec()
# preview.app.exec()
