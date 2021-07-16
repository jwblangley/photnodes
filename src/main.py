from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

import sys

from node import Node


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(10)
        self.widget.setLayout(self.layout)

        self.scene = QtWidgets.QGraphicsScene()

        self.view = QtWidgets.QGraphicsView(self.scene)
        self.layout.addWidget(self.view, 0, 0)

        self.resize(600,600)

    def populate(self):
        n = Node()
        self.addNode(n)

    def addNode(self, node):
        if node not in self.scene.items():
            self.scene.addItem(node)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.populate()
    window.show()
    sys.exit(app.exec_())
