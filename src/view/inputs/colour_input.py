from PySide6 import QtCore, QtWidgets, QtGui

from view.theme import theme


class ColorInput(QtWidgets.QWidget):
    def __init__(self, label, default, callback):
        super().__init__()

        self.label = label
        self.default = default
        self.callback = callback

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSpacing(theme.spacing(1))
        self.setLayout(self.layout)

        self.colorDialog = QtWidgets.QColorDialog()
        self.colorDialog.colorSelected.connect(self.colorChosen)

        self.colorPickerLabel = QtWidgets.QLabel(label)
        self.layout.addWidget(self.colorPickerLabel)

        self.colorPickerVisual = QtWidgets.QLabel()
        self.colorPickerVisual.setCursor(QtCore.Qt.PointingHandCursor)
        self.colorPickerVisual.setSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored
        )
        self.colorPickerVisual.mousePressEvent = lambda e: self.colorDialog.show()
        self.layout.addWidget(self.colorPickerVisual)

        self.visualPixmap = QtGui.QPixmap(
            self.colorPickerVisual.width(), theme.spacing(2)
        )
        self.visualPixmap.fill(self.default)
        self.colorPickerVisual.setPixmap(self.visualPixmap)

    def colorChosen(self, color):
        self.visualPixmap.fill(color)
        self.colorPickerVisual.setPixmap(self.visualPixmap)
        self.callback(color)
