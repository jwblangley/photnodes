from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore
from view.nodes.connection import Connection

from view.utils import getTextSize

MARGIN = 5

class Socket(QtWidgets.QGraphicsItem):

    def __init__(self, name, displayName, isInput, maxConnections=float("inf"), **kwargs):
        super().__init__(**kwargs)

        self.name = name
        self.displayName = displayName
        self.isInput = isInput
        self.maxConnections = maxConnections

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
        self.highlighting = False

        self.setAcceptHoverEvents(True)

        self.tempNewCon = None
        self.lastBelow = None

    def boundingRect(self):
        return QtCore.QRect(self.x, self.y, self.w, self.h)

    def paint(self, painter, option, widget):
        # Paint box
        if self.highlighting:
            painter.setBrush(QtGui.QBrush(self.highlightColor))
        else:
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
        self.scene().removeItem(self)
        for con in self.connections[::]:
            con.destroy()
        del self

    def hoverEnterEvent(self, event):
        self.highlighting = True
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.highlighting = False
        self.update()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.tempNewCon = Connection(sourceSocket=self)
            self.tempNewCon.targetPos = event.scenePos()
            self.tempNewCon.updatePath()
            self.scene().addItem(self.tempNewCon)

    def mouseMoveEvent(self, event):
        if self.tempNewCon is not None:
            self.tempNewCon.targetPos = event.scenePos()
            self.tempNewCon.updatePath()

            # Highlight socket below
            self.tempNewCon.setVisible(False)
            below = self.scene().itemAt(event.scenePos(), QtGui.QTransform())
            self.tempNewCon.setVisible(True)
            if isinstance(below, Socket) and below is not self:
                self.lastBelow = below
                below.highlighting = True
                below.update()
            else:
                if self.lastBelow is not None:
                    self.lastBelow.highlighting = False
                    self.lastBelow.update()
                    self.lastBelow = None

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.tempNewCon.setVisible(False)
            target = self.scene().itemAt(event.scenePos(), QtGui.QTransform())
            self.tempNewCon.setVisible(True)

            if isinstance(target, Socket) and target is not self:
                self.connectTo(target, connection=self.tempNewCon)
            else:
                self.tempNewCon.destroy()
            self.tempNewCon=None


    def connectTo(self, other, connection=None):
        if other is self:
            return

        if connection is None:
            connection = Connection()

        connection.sourceSocket = self
        connection.targetSocket = other

        if not connection.canCreate():
            connection.destroy()
            print("No connection")
            return

        self.connections.append(connection)
        other.connections.append(connection)

        if connection not in self.scene().items():
            self.scene().addItem(connection)
