from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore
from view.nodes.header import Header

from view.utils import getTextSize

MARGIN = 5
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
        self.sockets = []

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.setCursor(QtCore.Qt.SizeAllCursor)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)

    def boundingRect(self):
        return QtCore.QRect(self.x, self.y, self.w, self.h)

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

    def addSocket(self, socket):
        assert socket.name not in [s.name for s in self.sockets], "Duplicate socket name"

        yOffset = sum([s.h + s.margin for s in self.sockets]) + self.header.h + self.margin
        xOffset = self.margin / 2

        self.sockets.append(socket)
        socket.setParentItem(self)
        self.updateSize()

        if socket.isInput:
            socket.setPos(self.boundingRect().left() - socket.w + xOffset, yOffset)
        else:
            socket.setPos(self.boundingRect().right() + xOffset, yOffset)


    def updateSize(self):
        totalHeight = self.header.h + self.margin + sum([s.h + s.margin for s in self.sockets])
        self.h = totalHeight

        headerWidth = self.margin + getTextSize(self.header.text).width()
        maxWidth = max([headerWidth] + [s.w + s.margin + getTextSize(s.displayName).width() for s in self.sockets])
        self.w = maxWidth
