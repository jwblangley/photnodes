import sys

from PySide6 import QtWidgets

from view.window.main_window import Window

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
