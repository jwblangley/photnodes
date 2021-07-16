from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtCore

import sys
from view.nodes.connection import Connection
from view.nodes.header import Header

from view.nodes.node import BaseNode
from view.nodes.socket import Socket
from view.nodes.starting_node import StartingNode

def viewMouseMoveEvent(self, event):
    QtWidgets.QGraphicsView.mouseMoveEvent(self, event)
    if self.scene().selectedItems():
        self.update()

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
        self.view.mouseMoveEvent = lambda event: viewMouseMoveEvent(self.view, event)
        self.layout.addWidget(self.view, 0, 0)

        self.resize(600,600)

    def populate(self):
        n1 = StartingNode()
        s1 = Socket("test1", "r", False)
        n1.addSocket(s1)
        s2 = Socket("test", "really big test socket", False)
        n1.addSocket(s2)
        self.addNode(n1)

        # n2 = Node()
        # s2 = Socket("test", "test socket", True, 1)
        # n2.addSocket(s2)
        # self.addNode(n2)

        # s1.connectTo(s2)

    def addNode(self, node):
        if node not in self.scene.items():
            self.scene.addItem(node)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.populate()
    window.show()
    sys.exit(app.exec_())
