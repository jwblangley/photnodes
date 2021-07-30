from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

from view.utils import getTextSize

MARGIN = 5
ROUNDNESS = 0


class BaseNode(QtWidgets.QGraphicsItem):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)

        self.title = title

        self.x = 0
        self.y = 0
        self.w = 10
        self.h = 10

        self.margin = MARGIN
        self.roundness = ROUNDNESS

        self.fillColor = QtGui.QColor(220, 220, 220)

        self.header = None
        self.sockets = {}

        self.inspectorWidget = QtWidgets.QWidget()
        self.allVars = None

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.setCursor(QtCore.Qt.SizeAllCursor)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)

    def itemChange(self, change, value):
        if change == QtWidgets.QGraphicsItem.ItemSelectedChange:
            inspector = QtWidgets.QApplication.instance().window.inspector

            if value:
                inspector.layout.addWidget(self.inspectorWidget)
                inspector.titleLabel.setText(f"Inspector: {self.title}")
            else:
                self.onDeselect()

        return super().itemChange(change, value)

    def boundingRect(self):
        return QtCore.QRect(self.x, self.y, self.getWidth(), self.getHeight())

    def paint(self, painter, option, widget):
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        bbox = self.boundingRect()
        painter.drawRoundedRect(
            self.x, self.y, bbox.width(), self.h, self.roundness, self.roundness
        )

    def destroy(self):
        # Destroy header
        if self.header is not None:
            self.header.destroy()

        for socket in self.sockets.values():
            socket.destroy()

        self.scene().removeItem(self)

        if self.isSelected():
            self.onDeselect()

    def mouseMoveEvent(self, event):
        for node in self.scene().selectedItems():
            if isinstance(node, BaseNode):
                for socket in node.sockets.values():
                    for connection in socket.connections:
                        connection.updatePath()
        super().mouseMoveEvent(event)

    def getHeight(self):
        return (
            sum(
                [
                    s.h + s.margin
                    for s in self.sockets.values()
                    if not s.name.startswith("_")
                ]
            )
            + self.header.h
            + self.margin
        )

    def onDeselect(self):
        self.inspectorWidget.setParent(None)
        inspector = QtWidgets.QApplication.instance().window.inspector
        inspector.titleLabel.setText("Inspector")

    def getWidth(self):
        headerWidth = self.margin + getTextSize(self.header.text).width()
        return max(
            [headerWidth]
            + [
                s.w + s.margin + getTextSize(s.displayName).width()
                for s in self.sockets.values()
            ]
        )

    def addSocket(self, socket):
        assert socket.name not in self.sockets, "Duplicate socket name"

        yOffset = self.getHeight()

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

        for socket in self.sockets.values():
            if socket.isInput:
                socket.setX(self.boundingRect().left() - socket.w)
            else:
                socket.setX(self.boundingRect().right())

    def setAttribute(self, name, value):
        setattr(self, name, value)
        QtWidgets.QApplication.instance().controller.pass_attribute(self, name, value)

    def passAllAttributes(self):
        if self.allVars is None:
            raise NotImplementedError("allVars should be set by subclasses")
        for name in self.allVars:
            value = getattr(self, name)
            QtWidgets.QApplication.instance().controller.pass_attribute(
                self, name, value
            )
