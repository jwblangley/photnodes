from PySide6 import QtCore, QtWidgets, QtGui

class TextInput(QtWidgets.QWidget):
    def __init__(self, text, default, callback, validator=None):
        super().__init__()

        self.text = text
        self.default = default
        self.callback = callback
        self.validator = validator

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.titleLabel = QtWidgets.QLabel(self.text)
        self.layout.addWidget(self.titleLabel)

        self.inputField = QtWidgets.QLineEdit(str(self.default))
        self.inputField.setValidator(self.validator)
        self.inputField.textChanged.connect(self.callback)
        self.layout.addWidget(self.inputField)
