from PySide6 import QtWidgets

from view.nodes.starting_node import StartingNode


class SolidColorNode(StartingNode):

    def __init__(self, **kwargs):
        super().__init__("Solid color", **kwargs)

        # Define node

        # Define inspector widget
        self.inspector_widget = QtWidgets.QWidget()
        self.iw_layout = QtWidgets.QVBoxLayout()
        self.iw_layout.setSpacing(10)
        self.inspector_widget.setLayout(self.iw_layout)

        self.color_picker_layout = QtWidgets.QHBoxLayout()
        self.color_picker_layout.setSpacing(10)
        self.iw_layout.addLayout(self.color_picker_layout)

        self.color_picker_label = QtWidgets.QLabel("Colour:")
        self.color_picker_layout.addWidget(self.color_picker_label)
