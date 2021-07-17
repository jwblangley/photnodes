from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

from view.utils import getTextSize


class Header(QtWidgets.QGraphicsItem):
    def __init__(self, node, text, **kwargs):
        super().__init__(**kwargs)

        self.node = node
        self.text = text
        self.h = 20
        self.fillColor = QtGui.QColor(90, 90, 90)
        self.textColor = QtGui.QColor(240, 240, 240)

    def boundingRect(self):
        nodeRect = self.node.boundingRect()
        return QtCore.QRect(self.x(), self.y(), nodeRect.width(), self.h)

    def paint(self, painter, option, widget):
        # Paint box
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        bbox = self.boundingRect()
        painter.drawRoundedRect(bbox, self.node.roundness, self.node.roundness)

        # Paint text
        if self.node.isSelected():
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 255)))
        else:
            painter.setPen(QtGui.QPen(self.textColor))

        textSize = getTextSize(self.text, painter=painter)
        painter.drawText(
            self.x() + self.node.margin,
            self.y() + (self.h + textSize.height() / 2) / 2,
            self.text,
        )

    def destroy(self):
        self.node.scene().removeItem(self)
        del self
