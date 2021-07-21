from PySide6 import QtGui
from PySide6 import QtWidgets

from controller.node_map import NODE_CLASS_MAP

from view.window.image_canvas import ImageCanvas
from view.window.inspector import Inspector
from view.window.node_canvas import NodeCanvas

CANVAS_SIZE = (1, 1)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Layout
        self.setWindowTitle("Photnodes")

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(10)
        self.widget.setLayout(self.layout)

        self.nodeCanvas = NodeCanvas()
        self.layout.addWidget(self.nodeCanvas, 1, 0, 1, 2)

        self.leftImageCanvas = ImageCanvas(CANVAS_SIZE)
        self.layout.addWidget(self.leftImageCanvas, 0, 0)

        self.rightImageCanvas = ImageCanvas(CANVAS_SIZE)
        self.layout.addWidget(self.rightImageCanvas, 0, 1)

        self.inspector = Inspector()
        self.layout.addWidget(self.inspector, 0, 2, 2, 1)

        # Menu and Actions
        self.fileMenu = self.menuBar().addMenu("File")
        self.insertMenu = self.menuBar().addMenu("Insert")

        self.newNodeAction = QtGui.QAction("New node", self)
        self.newNodeAction.setShortcut(QtGui.QKeySequence("Ctrl+Space"))
        self.newNodeAction.triggered.connect(self.newNodeEvent)
        self.insertMenu.addAction(self.newNodeAction)

        self.showMaximized()

    def newNodeEvent(self):
        dialog = QtWidgets.QInputDialog()
        dialog.setOption(QtWidgets.QInputDialog.UseListViewForComboBoxItems)

        node_clases = {k.TITLE: k for k, v in NODE_CLASS_MAP.items()}

        dialog.setComboBoxItems(node_clases.keys())
        dialog.setWindowTitle("New node type")
        dialog.textValueSelected.connect(
            lambda t: QtWidgets.QApplication.instance().controller.new_node(
                node_clases[t]
            )
        )
        dialog.exec()
