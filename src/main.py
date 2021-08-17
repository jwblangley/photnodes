import sys

import torch

from PySide6 import QtWidgets

from qt_material import apply_stylesheet
from controller.controller import Controller

from view.window.main_window import Window
from view.theme import theme

if __name__ == "__main__":
    torch.autograd.set_grad_enabled(False)

    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme=theme.qt_material_theme)

    window = Window()
    controller = Controller(window)

    app.window = window
    app.controller = controller

    controller.initialise()

    app.window.show()
    sys.exit(app.exec_())
