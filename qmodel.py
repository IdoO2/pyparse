from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Tree(QStandardItemModel):

    def __init__(self, tree):
        QStandardItemModel.__init__(self)
        self.root = QStandardItem()
        self.addBranches(tree)

    def addBranches(self, branches, parent=None):
        '''
        Accepts either branch name as string
        or tree structure as object:
        [root item1 item2 ... itemN]
        Possibly recursive
        '''
        parent = parent if parent else self.root
        for branch in branches:
            if isinstance(branch, str):
                item = QStandardItem(branch)
                parent.appendRow(item)
            else:
                item = QStandardItem(branch[0])
                self.appendRow(item)
                self.addBranches(branch[1:], item)
