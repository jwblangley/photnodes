import warnings

from PySide6 import QtCore, QtWidgets, QtGui


class ImageCanvas(QtWidgets.QScrollArea):
    def __init__(self, size):
        super().__init__()

        self.width, self.height = size
        self.scale = 1

        self.qImgCache = None
        self.qImgBufferCache = None

        self.setWidgetResizable(False)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet("QScrollArea {background-color: #303030}")

        self.label = QtWidgets.QLabel()
        self.label.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored
        )
        self.label.setScaledContents(True)
        self.setWidget(self.label)

        self.pixmap = QtGui.QPixmap(self.width, self.height)
        self.pixmap.fill(QtGui.QColor("white"))
        self.qImgCache = self.pixmap.toImage()
        self.label.setPixmap(self.pixmap)

        self.painter = QtGui.QPainter(self.pixmap)

        self.actionZoomIn = QtGui.QAction("Zoom in", self)
        self.actionZoomIn.setShortcut(QtGui.QKeySequence.ZoomIn)
        self.actionZoomIn.triggered.connect(lambda: self.zoomLabel(factor=1.1))

        self.actionZoomOut = QtGui.QAction("Zoom out", self)
        self.actionZoomOut.setShortcut(QtGui.QKeySequence.ZoomOut)
        self.actionZoomOut.triggered.connect(lambda: self.zoomLabel(factor=1 / 1.1))

        self.zoomLabel()

    def destroy(self):
        self.painter.end()
        super().destroy()
        del self

    def zoomLabel(self, factor=None):
        if factor is not None:
            self.scale *= factor
        self.label.resize(self.width * self.scale, self.height * self.scale)

    def updateLabel(self):
        self.label.setPixmap(self.pixmap)

    def paintImage(self, qImg=None, qImgBuffer=None, cachedOnly=False):
        # Buffer must be kept in memory prior to usage

        if cachedOnly:
            if qImg is not None or qImgBuffer is not None:
                warnings.warn("Using cached image, when new image is provided")

            self.painter.drawImage(0, 0, self.qImgCache)
        else:
            if qImg is None:
                raise RuntimeError("Image to paint is not given")
            if qImgBuffer is None:
                raise RuntimeError("Image buffer to paint is not given")

            self.qImgCache = qImg
            self.qImgBufferCache = qImgBuffer

            self.painter.drawImage(0, 0, qImg)

        self.updateLabel()
