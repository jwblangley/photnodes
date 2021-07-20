from PySide6 import QtWidgets
from PySide6 import QtGui
from view.inputs.colour_input import ColorInput
from view.inputs.text_input import TextInput

from view.nodes.terminal_node import TerminalNode

DEFAULT_GAMMA = 2.2


class RenderNode(TerminalNode):
    TITLE = "Output"

    def __init__(self, **kwargs):
        super().__init__(RenderNode.TITLE, **kwargs)

        # Define vars
        self.allVars = ["gamma"]

        self.gamma = DEFAULT_GAMMA

        # Define node

        # Define inspector widget
        self.inspectorWidget = QtWidgets.QWidget()
        self.iwLayout = QtWidgets.QVBoxLayout()
        self.iwLayout.setSpacing(10)
        self.inspectorWidget.setLayout(self.iwLayout)

        self.gammaPicker = TextInput(
            "Gamma:",
            self.gamma,
            lambda value: self.setAttribute("gamma", int(value)),
            validator=QtGui.QDoubleValidator(),
        )
        self.iwLayout.addWidget(self.gammaPicker)
