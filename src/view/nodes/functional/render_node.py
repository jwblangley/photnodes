from PySide6 import QtWidgets
from PySide6 import QtGui
from view.inputs.text_input import TextInput
from view.nodes.socket import Socket

from view.nodes.terminal_node import TerminalNode

from view.theme import theme


DEFAULT_GAMMA = 2.2


class RenderNode(TerminalNode):
    TITLE = "Output"

    def __init__(self, **kwargs):
        super().__init__(RenderNode.TITLE, **kwargs)

        # Define vars
        self.attributeVars = ["gamma"]

        self.gamma = DEFAULT_GAMMA

        # Define node
        self.addSocket(Socket("test", "test", True, 1))

        # Define inspector widget
        self.inspectorWidget = QtWidgets.QWidget()
        self.iwLayout = QtWidgets.QVBoxLayout()
        self.iwLayout.setSpacing(theme.spacing(1))
        self.inspectorWidget.setLayout(self.iwLayout)

        self.gammaPicker = TextInput(
            "Gamma:",
            self.gamma,
            lambda value: self.setAttribute("gamma", float(value)),
            validator=QtGui.QDoubleValidator(),
        )
        self.iwLayout.addWidget(self.gammaPicker)
