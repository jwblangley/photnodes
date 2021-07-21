import warnings

from PySide6 import QtCore, QtWidgets, QtGui

ZOOM_FACTOR = 1.1


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

        self.zoomLabel()

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomLabel(factor=ZOOM_FACTOR)
            elif event.angleDelta().y() < 0:
                self.zoomLabel(factor=1 / ZOOM_FACTOR)

        super().wheelEvent(event)

    def zoomLabel(self, factor=None):
        if factor is not None:
            self.scale *= factor
        self.label.resize(self.width * self.scale, self.height * self.scale)

    def paintImage(self, qImg=None, qImgBuffer=None, cachedOnly=False):
        # Buffer must be kept in memory prior to usage

        if cachedOnly:
            if qImg is not None or qImgBuffer is not None:
                warnings.warn("Using cached image, when new image is provided")

            qImg = self.qImgCache
        else:
            if qImg is None:
                if qImgBuffer is not None:
                    warnings.warn("Image buffer provided with no image. Ignored")
                self.label.setVisible(False)
                return
            elif qImgBuffer is None:
                raise RuntimeError("Image buffer to paint is not given")

            self.qImgCache = qImg
            self.qImgBufferCache = qImgBuffer

        self.width = qImg.width()
        self.height = qImg.height()

        pixmap = QtGui.QPixmap(self.width, self.height)
        pixmap.fill(QtGui.QColor("black"))

        painter = QtGui.QPainter(pixmap)
        painter.drawImage(0, 0, qImg)
        painter.end()

        self.label.setPixmap(pixmap)
        self.zoomLabel()
        self.label.setVisible(True)
