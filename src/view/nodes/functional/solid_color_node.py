from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore
from view.inputs.colour_input import ColorInput
from view.inputs.text_input import TextInput

from view.nodes.starting_node import StartingNode


class SolidColorNode(StartingNode):

    def __init__(self, **kwargs):
        super().__init__("Solid color", **kwargs)

        # Define vars
        self.chosenColor = QtGui.QColor()
        self.width = 0
        self.height = 0

        # Define node

        # Define inspector widget
        self.inspectorWidget = QtWidgets.QWidget()
        self.iwLayout = QtWidgets.QVBoxLayout()
        self.iwLayout.setSpacing(10)
        self.inspectorWidget.setLayout(self.iwLayout)

        self.colorPicker = ColorInput("Colour:", self.chosenColor, lambda value: setattr(self, "chosenColor", value))
        self.iwLayout.addWidget(self.colorPicker)

        self.widthPicker = TextInput("Width:", self.width, lambda value: setattr(self, "width", int(value)), validator=QtGui.QIntValidator())
        self.iwLayout.addWidget(self.widthPicker)

        self.heightPicker = TextInput("Height:", self.height, lambda value: setattr(self, "height", int(value)), validator=QtGui.QIntValidator())
        self.iwLayout.addWidget(self.heightPicker)
