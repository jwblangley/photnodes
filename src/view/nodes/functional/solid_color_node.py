from PySide6 import QtWidgets
from PySide6 import QtGui
from view.inputs.colour_input import ColorInput
from view.inputs.text_input import TextInput

from view.nodes.starting_node import StartingNode


class SolidColorNode(StartingNode):
    TITLE = "Solid color"

    def __init__(self, **kwargs):
        super().__init__(SolidColorNode.TITLE, **kwargs)

        # Define vars
        self.allVars = ["color", "width", "height"]

        self.color = QtGui.QColor()
        self.width = 0
        self.height = 0

        # Define node

        # Define inspector widget
        self.inspectorWidget = QtWidgets.QWidget()
        self.iwLayout = QtWidgets.QVBoxLayout()
        self.iwLayout.setSpacing(10)
        self.inspectorWidget.setLayout(self.iwLayout)

        self.colorPicker = ColorInput(
            "Colour:",
            self.color,
            lambda value: self.setAttribute("color", value),
        )
        self.iwLayout.addWidget(self.colorPicker)

        self.widthPicker = TextInput(
            "Width:",
            self.width,
            lambda value: self.setAttribute("width", int(value)),
            validator=QtGui.QIntValidator(),
        )
        self.iwLayout.addWidget(self.widthPicker)

        self.heightPicker = TextInput(
            "Height:",
            self.height,
            lambda value: self.setAttribute("height", int(value)),
            validator=QtGui.QIntValidator(),
        )
        self.iwLayout.addWidget(self.heightPicker)
