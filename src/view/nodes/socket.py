from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore
from view.nodes.connection import Connection

from view.utils import getTextSize

MARGIN = 5

class Socket(QtWidgets.QGraphicsItem):

    def __init__(self, name, displayName, isInput, **kwargs):
        super().__init__(**kwargs)

        self.name = name
        self.displayName = displayName
        self.isInput = isInput

        self.x = 0
        self.y = 0
        self.w = 10
        self.h = 10

        self.margin = MARGIN

        self.labelColor = QtGui.QColor(10, 10, 10)
        self.fillColor = QtGui.QColor(130, 130, 130)
        self.highlightColor = QtGui.QColor(255, 255, 0)

        self.node = None
        self.connections = []

        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QtCore.QRect(self.x, self.y, self.w, self.h)

    def paint(self, painter, option, widget):
        # Paint box
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        bbox = self.boundingRect()
        painter.drawRect(bbox)

        # Paint text
        textSize = getTextSize(self.displayName, painter=painter)
        if self.isInput:
            x = bbox.right() + self.margin
        else:
            x = bbox.left() - self.margin - textSize.width()
        y = bbox.bottom()

        painter.setPen(QtGui.QPen(self.labelColor))
        painter.drawText(x, y, self.displayName)

    def destroy(self):
        self.node.scene().removeItem(self)
        del self

    def connectTo(self, other):
        if other is self:
            return

        connection = Connection()
        connection.sourceSocket = self
        connection.targetSocket = other

        if not connection.isValid():
            raise RuntimeError("Invalid connection")

        self.connections.append(connection)
        other.connections.append(connection)

        self.scene().addItem(connection)
