from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

LINE_THICKNESS = 2

CURVE1 = 0.6
CURVE2 = 0.2
CURVE3 = 0.4
CURVE4 = 0.8


class Connection(QtWidgets.QGraphicsPathItem):
    def __init__(self, sourceSocket=None, targetSocket=None, **kwargs):
        super().__init__(**kwargs)

        self.setCursor(QtCore.Qt.PointingHandCursor)

        self.lineColor = QtGui.QColor(10, 10, 10)
        self.selectedColor = QtGui.QColor(0, 0, 255)
        self.thickness = LINE_THICKNESS

        self.sourceSocket = sourceSocket
        self.targetSocket = targetSocket

        self.sourcePos = QtCore.QPointF(0, 0)
        self.targetPos = QtCore.QPointF(0, 0)

        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

    def paint(self, painter, option, widget):
        if self.isSelected():
            self.setPen(QtGui.QPen(self.selectedColor, self.thickness))
        else:
            self.setPen(QtGui.QPen(self.lineColor, self.thickness))

        self.setBrush(QtCore.Qt.NoBrush)
        self.setZValue(1)

        # Remove selection box
        option.state &= ~QtWidgets.QStyle.State_Selected
        super().paint(painter, option, widget)

    def destroy(self):
        if self.sourceSocket is not None and self in self.sourceSocket.connections:
            self.sourceSocket.connections.remove(self)
        if self.targetSocket is not None and self in self.targetSocket.connections:
            self.targetSocket.connections.remove(self)

        self.scene().removeItem(self)

    def mousePressEvent(self, event):
        # Disable multiple selection
        if event.modifiers() == QtCore.Qt.ControlModifier:
            event.ignore()
        self.scene().clearSelection()

    def _repeat_eq(self, other):
        if not isinstance(other, Connection):
            return False

        return (
            self.sourceSocket is not None
            and self.targetSocket is not None
            and other.sourceSocket is not None
            and other.targetSocket is not None
            and self.sourceSocket == other.sourceSocket
            and self.targetSocket == other.targetSocket
        )

    def isRepeat(self):
        assert self.sourceSocket is not None, "No source socket"
        return len(list(filter(self._repeat_eq, self.sourceSocket.connections))) > 0

    def canCreate(self):
        return (
            self.sourceSocket is not None
            and self.targetSocket is not None
            and (
                (self.sourceSocket.isInput and not self.targetSocket.isInput)
                or (self.targetSocket.isInput and not self.sourceSocket.isInput)
            )
            and self.sourceSocket.node != self.targetSocket.node
            and len(self.sourceSocket.connections) < self.sourceSocket.maxConnections
            and len(self.targetSocket.connections) < self.targetSocket.maxConnections
            and not self.isRepeat()
        )

    def updatePath(self):
        assert self.sourceSocket is not None, "No source socket for connection"

        self.sourcePos = self.sourceSocket.mapToScene(
            self.sourceSocket.boundingRect().right(),
            self.sourceSocket.boundingRect().center().y(),
        )

        if self.targetSocket is not None:
            self.targetPos = self.targetSocket.mapToScene(
                self.targetSocket.boundingRect().left(),
                self.targetSocket.boundingRect().center().y(),
            )

        path = QtGui.QPainterPath()
        path.moveTo(self.sourcePos)

        dx = self.targetPos.x() - self.sourcePos.x()
        dy = self.targetPos.y() - self.sourcePos.y()

        ctrl1 = QtCore.QPointF(
            self.sourcePos.x() + dx * CURVE1, self.sourcePos.y() + dy * CURVE2
        )
        ctrl2 = QtCore.QPointF(
            self.sourcePos.x() + dx * CURVE3, self.sourcePos.y() + dy * CURVE4
        )

        path.cubicTo(ctrl1, ctrl2, self.targetPos)
        self.setPath(path)
