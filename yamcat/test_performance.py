# -*- coding: utf-8 -*-
"""
Tests the speed of image updates for an ImageItem and RawImageWidget.
The speed will generally depend on the type of data being shown, whether
it is being scaled and/or converted by lookup table, and whether OpenGL
is used by the view widget
"""

## Add path to library (just for examples; you do not need this)
import argparse
import sys

import numpy as np

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore, QT_LIB
from time import perf_counter
import threading
import queue
import cv2
from pypylon import pylon

pg.setConfigOption('imageAxisOrder', 'row-major')

import VideoTemplate_pytemplate as ui_template

try:
    import cupy as cp
    pg.setConfigOption("useCupy", True)
    _has_cupy = True
except ImportError:
    cp = None
    _has_cupy = False

try:
    import numba
    _has_numba = True
except ImportError:
    numba = None
    _has_numba = False

try:
    from pyqtgraph.widgets.RawImageWidget import RawImageGLWidget
except ImportError:
    RawImageGLWidget = None

parser = argparse.ArgumentParser(description="Benchmark for testing video performance")
parser.add_argument('--cuda', default=False, action='store_true', help="Use CUDA to process on the GPU", dest="cuda")
parser.add_argument('--dtype', default='uint8', choices=['uint8', 'uint16', 'float'], help="Image dtype (uint8, uint16, or float)")
parser.add_argument('--frames', default=3, type=int, help="Number of image frames to generate (default=3)")
parser.add_argument('--image-mode', default='mono', choices=['mono', 'rgb'], help="Image data mode (mono or rgb)", dest='image_mode')
parser.add_argument('--levels', default=None, type=lambda s: tuple([float(x) for x in s.split(',')]), help="min,max levels to scale monochromatic image dynamic range, or rmin,rmax,gmin,gmax,bmin,bmax to scale rgb")
parser.add_argument('--lut', default=False, action='store_true', help="Use color lookup table")
parser.add_argument('--lut-alpha', default=False, action='store_true', help="Use alpha color lookup table", dest='lut_alpha')
parser.add_argument('--size', default='512x512', type=lambda s: tuple([int(x) for x in s.split('x')]), help="WxH image dimensions default='512x512'")
args = parser.parse_args(sys.argv[1:])

if RawImageGLWidget is not None:
    # don't limit frame rate to vsync
    sfmt = QtGui.QSurfaceFormat()
    sfmt.setSwapInterval(0)
    QtGui.QSurfaceFormat.setDefaultFormat(sfmt)

app = pg.mkQApp("Video Speed Test Example")

win = QtGui.QMainWindow()
win.setWindowTitle('pyqtgraph example: VideoSpeedTest')
ui = ui_template.Ui_MainWindow()
ui.setupUi(win)
win.show()

if RawImageGLWidget is None:
    ui.rawGLRadio.setEnabled(False)
    ui.rawGLRadio.setText(ui.rawGLRadio.text() + " (OpenGL not available)")
else:
    ui.rawGLImg = RawImageGLWidget()
    ui.stack.addWidget(ui.rawGLImg)

# read in CLI args
ui.cudaCheck.setChecked(args.cuda and _has_cupy)
ui.cudaCheck.setEnabled(_has_cupy)
ui.numbaCheck.setChecked(_has_numba and pg.getConfigOption("useNumba"))
ui.numbaCheck.setEnabled(_has_numba)
ui.framesSpin.setValue(args.frames)
ui.widthSpin.setValue(args.size[0])
ui.heightSpin.setValue(args.size[1])
ui.dtypeCombo.setCurrentText(args.dtype)
ui.rgbCheck.setChecked(args.image_mode=='rgb')
ui.maxSpin1.setOpts(value=255, step=1)
ui.minSpin1.setOpts(value=0, step=1)
levelSpins = [ui.minSpin1, ui.maxSpin1, ui.minSpin2, ui.maxSpin2, ui.minSpin3, ui.maxSpin3]
if args.cuda and _has_cupy:
    xp = cp
else:
    xp = np
if args.levels is None:
    ui.scaleCheck.setChecked(False)
    ui.rgbLevelsCheck.setChecked(False)
else:
    ui.scaleCheck.setChecked(True)
    if len(args.levels) == 2:
        ui.rgbLevelsCheck.setChecked(False)
        ui.minSpin1.setValue(args.levels[0])
        ui.maxSpin1.setValue(args.levels[1])
    elif len(args.levels) == 6:
        ui.rgbLevelsCheck.setChecked(True)
        for spin,val in zip(levelSpins, args.levels):
            spin.setValue(val)
    else:
        raise ValueError("levels argument must be 2 or 6 comma-separated values (got %r)" % (args.levels,))
ui.lutCheck.setChecked(args.lut)
ui.alphaCheck.setChecked(args.lut_alpha)


#ui.graphicsView.useOpenGL()  ## buggy, but you can try it if you need extra speed.

vb = pg.ViewBox()
ui.graphicsView.setCentralItem(vb)
vb.setAspectLocked()
img = pg.ImageItem()
vb.addItem(img)



def noticeNumbaCheck():
    pg.setConfigOption('useNumba', _has_numba and ui.numbaCheck.isChecked())

ui.numbaCheck.toggled.connect(noticeNumbaCheck)


ptr = 0
lastTime = perf_counter()
fps = None

def update():
    global ui, ptr, lastTime, fps, LUT, img

    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if not grabResult.GrabSucceeded():
        print("Couldn't grab frame :(")
        print(grabResult.ErrorDescription)
        return

    # Access the image data
    image = converter.Convert(grabResult)
    gray = image.GetArray()

    img.setImage(gray)
    ui.stack.setCurrentIndex(0)

    now = perf_counter()
    dt = now - lastTime
    lastTime = now
    if fps is None:
        fps = 1.0/dt
    else:
        s = np.clip(dt*3., 0, 1)
        fps = fps * (1-s) + (1.0/dt) * s
    ui.fpsLabel.setText('%0.2f fps' % fps)
    app.processEvents()  ## force complete redraw for every plot

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    pg.exec()
