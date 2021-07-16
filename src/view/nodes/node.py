from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore
from view.nodes.header import Header

from view.utils import getTextSize

MARGIN = 5
ROUNDNESS = 0

class BaseNode(QtWidgets.QGraphicsItem):

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
        self.sockets = {}

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

        for socket in self.sockets[::]:
            socket.destroy()

        self.scene().removeItem(self)
        del self

    def mouseMoveEvent(self, event):
        for node in self.scene().selectedItems():
            if isinstance(node, BaseNode):
                for socket in node.sockets.values():
                    for connection in socket.connections:
                        connection.updatePath()
        super().mouseMoveEvent(event)

    def getHeight(self):
        return sum([s.h + s.margin for s in self.sockets.values() if not s.name.startswith("_")]) + self.header.h + self.margin

    def getWidth(self):
        headerWidth = self.margin + getTextSize(self.header.text).width()
        return max([headerWidth] + [s.w + s.margin + getTextSize(s.displayName).width() for s in self.sockets.values()])

    def addSocket(self, socket):
        assert socket.name not in self.sockets, "Duplicate socket name"

        yOffset = self.getHeight()
        xOffset = self.margin / 2

        socket.setParentItem(self)
        socket.node = self
        self.sockets[socket.name] = socket

        if socket.isInput:
            socket.setY(yOffset)
        else:
            socket.setY(yOffset)

        self.updateSize()

    def updateSize(self):
        self.h = self.getHeight()
        self.w = self.getWidth()

        xOffset = self.margin / 2
        for socket in self.sockets.values():
            if socket.isInput:
                socket.setX(self.boundingRect().left() - socket.w + xOffset)
            else:
                socket.setX(self.boundingRect().right() + xOffset)
