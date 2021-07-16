from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

LINE_THICKNESS = 2

CURVE1 = 0.6
CURVE2 = 0.2
CURVE3 = 0.4
CURVE4 = 0.8

class Connection(QtWidgets.QGraphicsPathItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lineColor = QtGui.QColor(10, 10, 10)
        self.deleteColor = QtGui.QColor(255,0,0)
        self.thickness = LINE_THICKNESS

        self.sourceSocket = None  # A Knob.
        self.targetSocket = None  # A Knob.

        self.sourcePos = QtCore.QPointF(0, 0)
        self.targetPos = QtCore.QPointF(0, 0)

        self.canDelete = False

        self.setAcceptHoverEvents(True)

    def paint(self, painter, option, widget):
        if self.canDelete:
            self.setPen(QtGui.QPen(self.deleteColor, self.thickness))
        else:
            self.setPen(QtGui.QPen(self.lineColor, self.thickness))
        self.setBrush(QtCore.Qt.NoBrush)
        self.setZValue(1)
        super().paint(painter, option, widget)

    def destroy(self):
        if self in self.sourceSocket.connections:
            self.sourceSocket.connections.remove(self)
        if self in self.targetSocket.connections:
            self.targetSocket.connections.remove(self)

        self.scene().removeItem(self)
        del self

    def hoverEnterEvent(self, event):
        if QtWidgets.QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            self.canDelete = True
            self.setCursor(QtCore.Qt.PointingHandCursor)
            self.update()

        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.canDelete = False
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.update()

        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton and self.canDelete:
            self.destroy()

    def canCreate(self):
        return (
            self.sourceSocket is not None
            and self.targetSocket is not None
            and not self.sourceSocket.isInput
            and self.targetSocket.isInput
            and len(self.sourceSocket.connections) < self.sourceSocket.maxConnections
            and len(self.targetSocket.connections) < self.targetSocket.maxConnections
        )

    def updatePath(self):
        if self.sourceSocket is not None:
            self.sourcePos = self.sourceSocket.mapToScene(self.sourceSocket.boundingRect().center())

        if self.targetSocket is not None:
            self.targetPos = self.targetSocket.mapToScene(self.targetSocket.boundingRect().center())

        path = QtGui.QPainterPath()
        path.moveTo(self.sourcePos)

        dx = self.targetPos.x() - self.sourcePos.x()
        dy = self.targetPos.y() - self.sourcePos.y()

        ctrl1 = QtCore.QPointF(self.sourcePos.x() + dx * CURVE1,
                               self.sourcePos.y() + dy * CURVE2)
        ctrl2 = QtCore.QPointF(self.sourcePos.x() + dx * CURVE3,
                               self.sourcePos.y() + dy * CURVE4)
        path.cubicTo(ctrl1, ctrl2, self.targetPos)
        self.setPath(path)
