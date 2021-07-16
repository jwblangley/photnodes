from PySide6 import QtWidgets
from view.window.image_canvas import ImageCanvas
from view.window.inspector import Inspector

from view.window.node_canvas import NodeCanvas

CANVAS_SIZE = (500, 500)

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Photnodes")

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(10)
        self.widget.setLayout(self.layout)

        self.node_canvas = NodeCanvas()
        self.layout.addWidget(self.node_canvas,1,0,1,2)

        self.left_image_canvas = ImageCanvas(CANVAS_SIZE)
        self.layout.addWidget(self.left_image_canvas,0,0)

        self.right_image_canvas = ImageCanvas(CANVAS_SIZE)
        self.layout.addWidget(self.right_image_canvas,0,1)

        self.inspector = Inspector()
        self.layout.addWidget(self.inspector, 0,2,2,1)

        self.showMaximized()

    def closeEvent(self, event):
        self.left_image_canvas.destroy()
        self.right_image_canvas.destroy()
