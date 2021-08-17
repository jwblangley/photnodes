import os

from PySide6 import QtWidgets

from view.theme import theme


class FileInput(QtWidgets.QWidget):
    def __init__(self, label, default, callback):
        super().__init__()

        self.label = label
        self.callback = callback
        if default is None or default == "":
            self.default = "Choose file"
        else:
            self.default = default

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(theme.spacing(1))
        self.setLayout(self.layout)

        self.fileLabel = QtWidgets.QLabel(self.label)
        self.layout.addWidget(self.fileLabel)

        self.fileButton = QtWidgets.QPushButton(str(self.default))
        self.fileButton.clicked.connect(self.openFileDialog)
        self.layout.addWidget(self.fileButton)

    def openFileDialog(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")
        self.fileButton.setText(os.path.basename(path))
        self.callback(path)
