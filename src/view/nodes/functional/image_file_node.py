from PySide6 import QtWidgets
from view.inputs.file_input import FileInput

from view.nodes.starting_node import StartingNode

from view.theme import theme


class ImageFileNode(StartingNode):
    TITLE = "Image File"

    def __init__(self, **kwargs):
        super().__init__(ImageFileNode.TITLE, **kwargs)

        # Define vars
        self.allVars = ["path"]

        self.path = ""

        # Define node

        # Define inspector widget
        self.inspectorWidget = QtWidgets.QWidget()
        self.iwLayout = QtWidgets.QVBoxLayout()
        self.iwLayout.setSpacing(theme.spacing(1))
        self.inspectorWidget.setLayout(self.iwLayout)

        self.pathPicker = FileInput(
            "Path:",
            self.path,
            lambda value: self.setAttribute("path", value),
        )
        self.iwLayout.addWidget(self.pathPicker)
