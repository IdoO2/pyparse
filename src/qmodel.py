# Library; make this more granular
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import path as ospath

# Represents an item in the tree
# Adds to QStandardItem a method to recursively add branche hierarchies
class TreeItem(QStandardItem):
    def addBranches(self, branches, parent=None):
        """
        Accepts either branch name as string
        or tree structure as a list of strings:
        [rootItem item1 item2 ... itemN]
        Strings in list are converted to TreeItems
        """
        parent = parent if parent else self
        for branch in branches:
            if isinstance(branch, tuple):
                item = TreeItem(branch[0])
                item_data = TreeItem(branch[1]['type'])
                parent.appendRow([item, item_data])
            else:
                item = TreeItem(branch[0][0])
                item_data = TreeItem(branch[0][1]['type'])
                parent.appendRow([item, item_data])
                self.addBranches(branch[1:], item)

class Tree(QStandardItemModel):
    """
    Model to hold the tree structure
    On instanciation sets filename as header
    and builds tree structure
    The method `addRow` should be delegated to TreeItem
    (ie self.invisibleRootItem should be instance of TreeItem)
    """
    def __init__(self, tree, filename):
        QStandardItemModel.__init__(self)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Symbol', 'Details'])
        if not tree:
            return
        self.__addBranches(tree)

    def __addBranches(self, branches, parent=None):
        """
        Use to fully build tree
        Must be done on a clean tree
        This method itself sets the first level and calls TreeItem
        for sub-levels
        """
        parent = parent if parent else self.invisibleRootItem()
        for branch in branches:
            if isinstance(branch, tuple):
                item = TreeItem(branch[0])
                item_data = TreeItem(branch[1]['type'])
                parent.appendRow([item, item_data])
            elif isinstance(branch, list):
                item = TreeItem(branch[0][0])
                item_data = TreeItem(branch[0][1]['type'])
                parent.insertRow(0, [item, item_data])
                item.addBranches(branch[1:], item)
            else:
                raise ValueError

    def setFileName(self, filename):
        """
        Set filename in column header
        """
        path, name = ospath.split(filename)
        title = 'Inspecting "{}" ({})'.format(name, path)
        self.setHorizontalHeaderLabels([title])

    def setBranches(self, branches):
        """
        Pass fully built tree to populate tree
        Clears existing tree if data exists,
        use with care
        """
        # :delete existing data
        self.clear()
        self.__addBranches(branches)
