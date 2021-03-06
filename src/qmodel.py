# Library; make this more granular
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import path as ospath

class Tree(QStandardItemModel):
    """
    Model to hold the tree structure
    On instanciation sets filename as header
    and builds tree structure
    The method `addRow` should be delegated to TreeItem
    (ie self.invisibleRootItem should be instance of TreeItem)
    """
    __columns = ['Symbol', 'Details (type, params, line)']
    def __init__(self, tree, filename):
        QStandardItemModel.__init__(self)
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(self.__columns)
        # Initialising with an empty tree is accepted
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
                item = QStandardItem(branch[0])
                item_data = QStandardItem(self.__buildSymbolData(branch[1]))
                parent.appendRow([item, item_data])
            elif isinstance(branch, list):
                item = QStandardItem(branch[0][0])
                item_data = QStandardItem(self.__buildSymbolData(branch[0][1]))
                parent.appendRow([item, item_data])
                self.__addBranches(branch[1:], item)
            else:
                raise ValueError('Misformatted tree')

    def __buildSymbolData(self, branch_data):
        """ Build a string from the attributes of given symbol"""
        datastr = []
        if 'visibility' in branch_data:
            datastr.append(branch_data['visibility'])
        datastr.append(branch_data['type'])
        if 'signature' in branch_data:
            signature = ', '.join(branch_data['signature'])
            if signature:
                datastr.append('({})'.format(signature))
        datastr.append('[{}]'.format(branch_data['line']))
        return ' '.join(datastr)

    def setFileName(self, filename):
        """
        Set filename in column header
        """
        path, name = ospath.split(filename)
        title = 'Inspecting "{}" ({})'.format(name, path)

    def setBranches(self, branches):
        """ Pass fully built tree to populate tree

        Clears existing tree if data exists,
        use with care
        """
        if not branches:
            raise ValueError('`branches` parameter empty')
        self.clear()
        self.__addBranches(branches)
        self.setHorizontalHeaderLabels(self.__columns)
