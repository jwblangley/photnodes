from PySide6 import QtWidgets
from PySide6 import QtCore

ZOOM_FACTOR = 1.1


class NodeCanvas(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.layout.addWidget(self.view, 0, 0)

    def wheelEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.view.scale(ZOOM_FACTOR, ZOOM_FACTOR)
            elif event.angleDelta().y() < 0:
                self.view.scale(1 / ZOOM_FACTOR, 1 / ZOOM_FACTOR)

        super().wheelEvent(event)

    def addNode(self, node):
        if node not in self.scene.items():
            self.scene.addItem(node)

    def selectedItems(self):
        return self.scene.selectedItems()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_1:
            if len(self.selectedItems()) == 1:
                QtWidgets.QApplication.instance().controller.set_left_selected_node(
                    self.selectedItems()[0]
                )
        if event.key() == QtCore.Qt.Key_2:
            if len(self.selectedItems()) == 1:
                QtWidgets.QApplication.instance().controller.set_right_selected_node(
                    self.selectedItems()[0]
                )
