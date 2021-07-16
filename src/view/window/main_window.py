from PySide6 import QtWidgets

from view.window.node_canvas import NodeCanvas

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(10)
        self.widget.setLayout(self.layout)

        self.node_canvas = NodeCanvas()
        self.layout.addWidget(self.node_canvas,0,1)

        self.resize(600,600)
