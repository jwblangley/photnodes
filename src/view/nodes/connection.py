from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

LINE_THICKNESS = 2

class Connection(QtWidgets.QGraphicsPathItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.lineColor = QtGui.QColor(10, 10, 10)
        self.thickness = LINE_THICKNESS

        self.sourceSocket = None  # A Knob.
        self.targetSocket = None  # A Knob.

        self.sourcePos = QtCore.QPointF(0, 0)
        self.targetPos = QtCore.QPointF(0, 0)

        self.curv1 = 0.6
        self.curv3 = 0.4

        self.curv2 = 0.2
        self.curv4 = 0.8

        self.setAcceptHoverEvents(True)

    def updatePath(self):
        if self.sourceSocket is not None:
            self.sourcePos = self.sourceSocket.mapToScene(self.sourceSocket.boundingRect().center())

        if self.targetSocket is not None:
            self.targetPos = self.targetSocket.mapToScene(self.targetSocket.boundingRect().center())

        path = QtGui.QPainterPath()
        path.moveTo(self.sourcePos)

        dx = self.targetPos.x() - self.sourcePos.x()
        dy = self.targetPos.y() - self.sourcePos.y()

        ctrl1 = QtCore.QPointF(self.sourcePos.x() + dx * self.curv1,
                               self.sourcePos.y() + dy * self.curv2)
        ctrl2 = QtCore.QPointF(self.sourcePos.x() + dx * self.curv3,
                               self.sourcePos.y() + dy * self.curv4)
        path.cubicTo(ctrl1, ctrl2, self.targetPos)
        self.setPath(path)

    def paint(self, painter, option, widget):
        self.setPen(QtGui.QPen(self.lineColor, self.thickness))
        self.setBrush(QtCore.Qt.NoBrush)
        self.setZValue(1)
        super().paint(painter, option, widget)

    def destroy(self):
        # TODO
        del self

    def isValid(self):
        return self.sourceSocket is not None and self.targetSocket is not None
