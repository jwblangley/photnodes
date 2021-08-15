from PySide6 import QtCore, QtWidgets, QtGui


class TextInput(QtWidgets.QWidget):
    def __init__(self, label, default, callback, validator=None):
        super().__init__()

        self.label = label
        self.default = default
        self.callback = callback
        self.validator = validator

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.textLabel = QtWidgets.QLabel(self.label)
        self.layout.addWidget(self.textLabel)

        self.inputField = QtWidgets.QLineEdit(str(self.default))
        self.inputField.setValidator(self.validator)
        self.inputField.textChanged.connect(self.callback)
        self.layout.addWidget(self.inputField)
