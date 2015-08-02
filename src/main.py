#
# Controller file and user-facing interface for parser
#

# Libraries
import sys
from PyQt5.QtWidgets import (QTreeView, QApplication,
                            QMainWindow, QWidget, QVBoxLayout)
from PyQt5.QtCore import QDir, Qt, QStringListModel

# Application
from view import PyOutline
from parsermoc import Parser
from qmodel import Tree

class Pyparse():

    """
    """

    def __init__(self, fulltext):
        self.__plaintext = fulltext

    def update(self, fulltext):
        '''
        Set raw text data for class
        Raw text is a piece of python source code
        expected to be a full file
        Should call parser?
        '''
        self.__plaintext = fulltext
        # Test calls
        self.__model.addRow(1, 'NewBranch') # Test: add item at root index 1
        self.__model.addRow(0, 'NewSubBranch', self.__model.item(1)) # Test: add items at item index 0 of root index 2
        self.__model.item(1).setData(fulltext, Qt.DisplayRole) # Test: change text of root index 1

    def parse(self):
        '''
        Call parser on text
        '''
        self.__data = Parser()
        self.__data.updateWith(self.__plaintext)
        return str(self.__data)

    def export(self, *fmt):
        '''
        Export data in format
        '''
        return str(self.__data.getSymbolTree())

    def gui(self):
        """ Lauch the application user interface

            Builds the application and view,
            injects the model
        """
        # Model
        self.__model = Tree(self.__data.getSymbolTree(), 'Some random file')

        app = QApplication(sys.argv)
        ui = PyOutline()

        # View
        tree = QTreeView()
        tree.setModel(self.__model)

        ui.buildWindow(tree, self.__model)
        ui.show()

        sys.exit(app.exec_())

# Test
psr = Pyparse('ooga')
psr.parse()
psr.gui()
psr.update('ooga')
