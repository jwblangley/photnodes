from PySide6 import QtWidgets
from PySide6 import QtGui
from view.inputs.text_input import TextInput

from view.nodes.starting_node import StartingNode


class ImageFileNode(StartingNode):
    TITLE = "Image File"

    def __init__(self, **kwargs):
        super().__init__(ImageFileNode.TITLE, **kwargs)

        # Define vars
        self.allVars = ["path", "gammaDecode"]

        self.path = ""
        self.gammaDecode = 1.0

        # Define node

        # Define inspector widget
        self.inspectorWidget = QtWidgets.QWidget()
        self.iwLayout = QtWidgets.QVBoxLayout()
        self.iwLayout.setSpacing(10)
        self.inspectorWidget.setLayout(self.iwLayout)

        self.pathPicker = TextInput(
            "Path:",
            self.path,
            lambda value: self.setAttribute("path", value),
        )
        self.iwLayout.addWidget(self.pathPicker)

        self.gammaDecodePicker = TextInput(
            "Decoding gamma:",
            self.gammaDecode,
            lambda value: self.setAttribute("gammaDecode", float(value)),
            validator=QtGui.QDoubleValidator(),
        )
        self.iwLayout.addWidget(self.gammaDecodePicker)
