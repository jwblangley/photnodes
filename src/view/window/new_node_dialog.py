from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from controller.node_map import NODE_CATEGORIES


def createTreeViewModel():
    nodeTreeModel = QtGui.QStandardItemModel()
    rootNode = nodeTreeModel.invisibleRootItem()

    boldFont = QtGui.QFont()
    boldFont.setBold(True)

    for category in NODE_CATEGORIES:
        categoryItem = QtGui.QStandardItem(category)
        categoryItem.setFont(boldFont)
        categoryItem.setEditable(False)
        rootNode.appendRow(categoryItem)

        for nodeClass in NODE_CATEGORIES[category]:
            nodeClassItem = QtGui.QStandardItem(nodeClass.TITLE)
            nodeClassItem.setData(nodeClass)
            nodeClassItem.setEditable(False)
            categoryItem.appendRow(nodeClassItem)

    return nodeTreeModel


class NewNodeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.selectedNode = None

        self.setWindowTitle("New Node")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.searchEdit = QtWidgets.QLineEdit()
        self.layout.addWidget(self.searchEdit)

        self.nodeTreeModel = createTreeViewModel()

        self.nodeTreeView = QtWidgets.QTreeView()
        self.nodeTreeView.setModel(self.nodeTreeModel)
        self.nodeTreeView.setHeaderHidden(True)
        self.nodeTreeView.expandAll()
        self.nodeTreeView.doubleClicked.connect(self.treeViewItemSelected)
        self.layout.addWidget(self.nodeTreeView)

        self.searchEdit.setFocus()

    def acceptNode(self, item):
        self.selectedNode = item.data()
        self.accept()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            index = self.nodeTreeView.currentIndex()
            item = self.nodeTreeModel.itemFromIndex(index)

            if item.rowCount() > 0:
                if self.nodeTreeView.isExpanded(index):
                    self.nodeTreeView.collapse(index)
                else:
                    self.nodeTreeView.expand(index)
            else:
                self.acceptNode(item)

        return super().keyPressEvent(event)

    def treeViewItemSelected(self, index):
        item = self.nodeTreeModel.itemFromIndex(index)
        if item.rowCount() == 0:
            self.acceptNode(item)
