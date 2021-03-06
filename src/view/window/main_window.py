from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from view.window.image_canvas import ImageCanvas
from view.window.inspector import Inspector
from view.window.new_node_dialog import NewNodeDialog
from view.window.node_canvas import NodeCanvas

from view.nodes.node import BaseNode
from view.nodes.connection import Connection

CANVAS_SIZE = (1, 1)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.statusSceneSource = None

        # Layout
        self.setWindowTitle("Photnodes")

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        self.statusLabel = QtWidgets.QLabel()
        self.statusLabel.mousePressEvent = self.statusLabelPressEvent
        self.statusBar().addPermanentWidget(self.statusLabel)

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
        self.selectionMenu = self.menuBar().addMenu("Selection")

        self.newNodeAction = QtGui.QAction("New node", self)
        self.newNodeAction.setShortcut(QtGui.QKeySequence("Ctrl+Space"))
        self.newNodeAction.triggered.connect(self.newNodeEvent)
        self.insertMenu.addAction(self.newNodeAction)

        self.deleteSelectionAction = QtGui.QAction("Delete", self)
        self.deleteSelectionAction.setShortcut(QtGui.QKeySequence.Delete)
        self.deleteSelectionAction.triggered.connect(self.deleteSelectionEvent)
        self.deleteSelectionAction.setEnabled(False)
        self.selectionMenu.addAction(self.deleteSelectionAction)

        self.showMaximized()

    def showStatus(self, status, sceneSource=None):
        self.statusLabel.setText(status)
        self.statusLabel.setVisible(True)

        if sceneSource is not None:
            self.statusSceneSource = sceneSource
            self.statusLabel.setCursor(QtCore.Qt.PointingHandCursor)

    def clearStatus(self):
        self.statusLabel.setVisible(False)
        self.statusSceneSource = None
        self.statusLabel.setCursor(QtCore.Qt.ArrowCursor)

    def statusLabelPressEvent(self, e):
        if self.statusSceneSource is not None:
            self.nodeCanvas.selectItem(self.statusSceneSource, centerInScene=True)

    def newNodeEvent(self):
        dialog = NewNodeDialog()

        if dialog.exec_():
            QtWidgets.QApplication.instance().controller.new_node(dialog.selectedNode)

    def setIsItemSelected(self, value):
        self.deleteSelectionAction.setEnabled(value)

    def deleteSelectionEvent(self):
        controller = QtWidgets.QApplication.instance().controller

        for item in self.nodeCanvas.selectedItems():
            if isinstance(item, BaseNode):
                controller.remove_node(item)
            elif isinstance(item, Connection):
                controller.pass_remove_connection(item)
                item.destroy()
            else:
                raise RuntimeError("Unknown item to delete")
