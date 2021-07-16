from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

class Node(QtWidgets.QGraphicsItem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.x = 0
        self.y = 0
        self.w = 10
        self.h = 10

        self.margin = 6
        self.roundness = 0

        self.fillColor = QtGui.QColor(220, 220, 220)

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.setCursor(QtCore.Qt.SizeAllCursor)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)

    def boundingRect(self):
        rect = QtCore.QRect(self.x, self.y, self.w, self.h)
        return rect

    def paint(self, painter, option, widget):
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        bbox = self.boundingRect()
        painter.drawRoundedRect(self.x, self.y, bbox.width(), self.h, self.roundness, self.roundness)

    def destroy(self):
        self.scene().removeItem(self)
        del self
