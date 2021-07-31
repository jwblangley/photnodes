from PySide6 import QtCore
from PySide6 import QtGui
from PySide6 import QtWidgets

from controller.node_map import NODE_CATEGORIES


def _createTreeViewModel():
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

        self.nodeTreeModel = _createTreeViewModel()

        self.filterModel = QtCore.QSortFilterProxyModel()
        self.filterModel.setSourceModel(self.nodeTreeModel)
        self.filterModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filterModel.setRecursiveFilteringEnabled(True)
        self.filterModel.setFilterFixedString("")

        self.setWindowTitle("New Node")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.searchEdit = QtWidgets.QLineEdit()
        self.searchEdit.textChanged.connect(self.updateFilter)
        self.layout.addWidget(self.searchEdit)

        self.nodeTreeView = QtWidgets.QTreeView()
        self.nodeTreeView.setModel(self.filterModel)
        self.nodeTreeView.setHeaderHidden(True)
        self.nodeTreeView.expandAll()
        self.nodeTreeView.doubleClicked.connect(self.treeViewItemDoubleClicked)
        self.layout.addWidget(self.nodeTreeView)

        self.searchEdit.setFocus()

    def acceptNode(self, item):
        self.selectedNode = item.data()
        self.accept()

    def updateFilter(self, filterText):
        self.filterModel.setFilterFixedString(filterText)

        # Select top child
        idx = self.filterModel.index(0, 0)
        while self.filterModel.hasChildren(idx):
            idx = self.filterModel.index(0, 0, idx)
        self.nodeTreeView.setCurrentIndex(idx)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            idx = self.nodeTreeView.currentIndex()

            item = self.nodeTreeModel.itemFromIndex(self.filterModel.mapToSource(idx))

            if self.filterModel.hasChildren(idx):
                if self.nodeTreeView.isExpanded(idx):
                    self.nodeTreeView.collapse(idx)
                else:
                    self.nodeTreeView.expand(idx)
            elif not self.nodeTreeModel.hasChildren(self.filterModel.mapToSource(idx)):
                self.acceptNode(item)

        return super().keyPressEvent(event)

    def treeViewItemDoubleClicked(self, idx):
        if not self.filterModel.hasChildren(idx):
            item = self.nodeTreeModel.itemFromIndex(self.filterModel.mapToSource(idx))

            self.acceptNode(item)
