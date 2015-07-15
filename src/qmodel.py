# Library; make this more granular
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Represents an item in the tree
# Adds to QStandardItem a method to recursively add branche hierarchies
class TreeItem(QStandardItem):
    def addBranches(self, branches, parent=None):
        '''
        Accepts either branch name as string
        or tree structure as a list of strings:
        [rootItem item1 item2 ... itemN]
        Strings in list are converted to TreeItems
        '''
        parent = parent if parent else self
        for branch in branches:
            if isinstance(branch, str):
                item = TreeItem(branch)
                parent.appendRow(item)
            else:
                item = TreeItem(branch[0])
                parent.appendRow(item)
                self.addBranches(branch[1:], item)

class Tree(QStandardItemModel):
    '''
    Model to hold the tree structure
    On instanciation sets filename as header
    and builds tree structure
    The method `addRow` should be delegated to TreeItem
    (ie self.invisibleRootItem should be instance of TreeItem)
    '''
    def __init__(self, tree, filename):
        QStandardItemModel.__init__(self)
        self.setHorizontalHeaderLabels([filename])
        self.__addBranches(tree)

    def __addBranches(self, branches, parent=None):
        parent = parent if parent else self.invisibleRootItem()
        for branch in branches:
            if isinstance(branch, str):
                item = TreeItem(branch)
                parent.appendRow(item)
            else:
                item = TreeItem(branch[0])
                parent.insertRow(0, item)
                item.addBranches(branch[1:], item)

    def addRow(self, index, branch, parent=None):
        '@see TreeItem.addBranches'
        item = TreeItem(branch)
        if parent and isinstance(parent, TreeItem):
            parent.insertRow(index, item)
        else: # root
            assert 0 <= index <= self.rowCount()
            # @todo: Use a TreeItem as root invisible item
            self.invisibleRootItem().insertRow(index, item)
