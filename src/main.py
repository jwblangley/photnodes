from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

import sys
from view.nodes.connection import Connection
from view.nodes.flow_node import FlowNode
from view.nodes.header import Header

from view.nodes.node import BaseNode
from view.nodes.socket import Socket
from view.nodes.starting_node import StartingNode
from view.nodes.terminal_node import TerminalNode


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

    def addNode(self, node):
        if node not in self.scene.items():
            self.scene.addItem(node)

    def populate(self):
        n1 = StartingNode("Input file")
        self.addNode(n1)

        n2 = FlowNode("Operation")
        n2.addSocket(Socket("in", "test in", True))
        n2.addSocket(Socket("out", "test out", False))
        self.addNode(n2)

        n3 = TerminalNode("Output file")
        self.addNode(n3)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.populate()
    window.show()
    sys.exit(app.exec_())
