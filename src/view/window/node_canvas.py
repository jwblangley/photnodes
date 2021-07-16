from PySide6 import QtWidgets

from view.nodes.starting_node import StartingNode
from view.nodes.flow_node import FlowNode
from view.nodes.terminal_node import TerminalNode

from view.nodes.socket import Socket

class NodeCanvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.layout.addWidget(self.view, 0, 0)

        self.populate()

    def addNode(self, node):
        if node not in self.scene.items():
            self.scene.addItem(node)

    # For testing
    def populate(self):
        n1 = StartingNode("Input file")
        self.addNode(n1)

        n2 = FlowNode("Operation")
        n2.addSocket(Socket("in", "test in", True))
        n2.addSocket(Socket("out", "test out", False))
        self.addNode(n2)

        n3 = TerminalNode("Output file")
        self.addNode(n3)
