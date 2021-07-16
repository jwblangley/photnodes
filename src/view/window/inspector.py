from PySide6 import QtCore, QtWidgets, QtGui

class Inspector(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.setFixedWidth(400)

        self.label = QtWidgets.QLabel("Inspector")
        self.layout.addWidget(self.label)

        self.layout.addStretch()
