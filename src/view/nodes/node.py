from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

from view.utils import getTextSize

from view.theme import theme


class BaseNode(QtWidgets.QGraphicsItem):
    def __init__(self, title, **kwargs):
        super().__init__(**kwargs)

        self.title = title

        self.x = theme.unit_width(0)
        self.y = theme.unit_height(0)
        self.w = theme.unit_width(2)
        self.h = theme.unit_height(2)

        self.padding = theme.spacing(0.5)
        self.roundness = theme.unit_width(0)

        self.fillColor = QtGui.QColor(theme.palette["secondary_dark"])

        self.header = None
        self.sockets = {}

        self.inspectorWidget = QtWidgets.QWidget()
        self.attributeVars = None

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.setCursor(QtCore.Qt.SizeAllCursor)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        # Disable multiple selection
        if event.modifiers() == QtCore.Qt.ControlModifier:
            event.ignore()
        self.scene().clearSelection()

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
                    s.h + 2 * self.padding
                    for s in self.sockets.values()
                    if not s.name.startswith("_")
                ]
            )
            + self.header.h
        )

    def onDeselect(self):
        self.inspectorWidget.setParent(None)
        inspector = QtWidgets.QApplication.instance().window.inspector
        inspector.titleLabel.setText("Inspector")

    def getWidth(self):
        headerWidth = getTextSize(self.header.text).width() + 2 * self.padding
        return max(
            [headerWidth]
            + [
                getTextSize(s.displayName).width() + 2 * self.padding
                for s in self.sockets.values()
            ]
        )

    def addSocket(self, socket):
        assert socket.name not in self.sockets, "Duplicate socket name"

        yOffset = self.getHeight()

        socket.setY(yOffset + self.padding)
        socket.setParentItem(self)
        socket.node = self
        self.sockets[socket.name] = socket

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
        if self.attributeVars is None:
            raise NotImplementedError("attributeVars should be set by subclasses")
        for name in self.attributeVars:
            value = getattr(self, name)
            QtWidgets.QApplication.instance().controller.pass_attribute(
                self, name, value
            )
