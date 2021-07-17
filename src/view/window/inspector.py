from PySide6 import QtCore, QtWidgets


class Inspector(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()

        self.setAlignment(QtCore.Qt.AlignTop)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.setFixedWidth(400)

        self.widget = QtWidgets.QWidget()
        self.setWidget(self.widget)
        self.setWidgetResizable(True)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.layout.setSpacing(10)
        self.widget.setLayout(self.layout)

        self.titleLabel = QtWidgets.QLabel("Inspector")
        self.layout.addWidget(self.titleLabel)
