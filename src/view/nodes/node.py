from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore
from view.nodes.header import Header

from view.utils import getTextSize

MARGIN = 6
ROUNDNESS = 0

class Node(QtWidgets.QGraphicsItem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.x = 0
        self.y = 0
        self.w = 10
        self.h = 10

        self.margin = MARGIN
        self.roundness = ROUNDNESS

        self.fillColor = QtGui.QColor(220, 220, 220)

        self.header = None

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.setCursor(QtCore.Qt.SizeAllCursor)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)

    def boundingRect(self):
        return QtCore.QRect(self.x, self.y, self.w, self.header.h)

    def paint(self, painter, option, widget):
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        bbox = self.boundingRect()
        painter.drawRoundedRect(self.x, self.y, bbox.width(), self.h, self.roundness, self.roundness)

    def destroy(self):
        # Destroy header
        if self.header is not None:
            self.header.destroy()

        self.scene().removeItem(self)
        del self

    def addHeader(self, header):
        self.header = header
        self.header.node = self
        self.header.setParentItem(self)
        self.updateSize()

    def updateSize(self):
        totalHeight = self.header.h + self.margin
        self.h = totalHeight

        headerWidth = self.margin + getTextSize(self.header.text).width()
        maxWidth = headerWidth
        self.w = maxWidth
