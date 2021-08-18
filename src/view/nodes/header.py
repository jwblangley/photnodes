from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

from view.utils import getTextSize

from view.theme import theme


DISPLAY_ICON_WIDTH = theme.unit_width(6)
DISPLAY_ICON_HEIGHT = theme.unit_height(2)
DISPLAY_ICON_RADIUS = theme.unit_height(2) - 2

HEIGHT = theme.unit_height(4)


class Header(QtWidgets.QGraphicsItem):
    def __init__(self, node, text, **kwargs):
        super().__init__(**kwargs)

        self.node = node
        self.text = text

        self.h = HEIGHT
        self.fillColor = QtGui.QColor(theme.palette["primary"])
        self.textColor = QtGui.QColor(theme.palette["primary_text"])
        self.selectTextColor = QtGui.QColor(theme.palette["highlight"])
        self.displayIconBackgroundColor = QtGui.QColor(theme.palette["primary"])
        self.noDisplayIconColor = QtGui.QColor(theme.palette["secondary"])
        self.displayIconColor = QtGui.QColor(theme.palette["highlight"])

        self.displayedLeft = False
        self.displayedRight = False

    def boundingRect(self):
        nodeRect = self.node.boundingRect()
        return QtCore.QRect(
            self.x(),
            self.y() - DISPLAY_ICON_HEIGHT,
            nodeRect.width(),
            self.h + DISPLAY_ICON_HEIGHT,
        )

    def paint(self, painter, option, widget):
        # Paint box
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        width = self.node.boundingRect().width()
        bbox = QtCore.QRect(self.x(), self.y(), width, self.h)
        painter.drawRoundedRect(bbox, self.node.roundness, self.node.roundness)

        # Paint display icons
        if self.displayedLeft or self.displayedRight:
            x = self.x() + width - DISPLAY_ICON_WIDTH
            y = self.y() - DISPLAY_ICON_HEIGHT
            bbox = QtCore.QRect(x, y, DISPLAY_ICON_WIDTH, DISPLAY_ICON_HEIGHT)
            painter.setBrush(QtGui.QBrush(self.displayIconBackgroundColor))
            painter.drawRoundedRect(bbox, self.node.roundness, self.node.roundness)

            displayBrush = QtGui.QBrush(self.displayIconColor)
            noDisplayBrush = QtGui.QBrush(self.noDisplayIconColor)

            painter.setBrush(displayBrush if self.displayedLeft else noDisplayBrush)
            painter.drawEllipse(
                x + (DISPLAY_ICON_WIDTH - DISPLAY_ICON_RADIUS * 2) / 3,
                y + (DISPLAY_ICON_HEIGHT - DISPLAY_ICON_RADIUS) / 2,
                8,
                8,
            )
            painter.setBrush(displayBrush if self.displayedRight else noDisplayBrush)
            painter.drawEllipse(
                x
                + DISPLAY_ICON_RADIUS
                + 2 * (DISPLAY_ICON_WIDTH - DISPLAY_ICON_RADIUS * 2) / 3,
                y + (DISPLAY_ICON_HEIGHT - DISPLAY_ICON_RADIUS) / 2,
                8,
                8,
            )

        # Paint text
        if self.node.isSelected():
            painter.setPen(QtGui.QPen(self.selectTextColor))
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
