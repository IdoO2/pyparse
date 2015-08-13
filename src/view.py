# Note on performance: in our case, consider setting `uniformRowHeights = True`

# Example file:
# 1. class Master():
# 2.   randval = 0
# 3.   def __init__(self):
# 4.     self.randval = 1
# 5.     def change():
# 6.       self.randval = 3

data = [
    ['Master',
        'randval', ['__init__',
            'change']]
]

# Example mapping found in `parser`
# We will need a mapping from file string to model,
# for two reasons:
# - when a line / line are updated, wee need to find the model reference easily
# - we need to uniquely identify possible homographs
# Note: this means frequent updating; “extreme” case: user deletes 30 lines
# Workflow:
# - user changes line 3
# - lookup mapping: line 3 holds (-2, 1)
# - lookup model at [3-2][1]
# - if symbol is modified, update model
# Example 2:
# - user changes line 4
# - nothing found: reparse lines from 3 to 4 to extract symbols
# Example 3:
# - user deletes line 3
# - reparse lines 3-2 to 3
# - update model at [3-2][1] accordingly
# - lookup mapping for children of 3
# - recurse on line 5


# Helpers
import inspect
from pprint import pprint

# Libraries
import sys
import os
from PyQt5.QtWidgets import (QTreeView, QApplication,
                            QMainWindow, QWidget, QVBoxLayout,
                            QFileDialog)
from PyQt5.QtCore import QDir, Qt, QStringListModel

# Application
from parsermoc import Parser
from qmodel import Tree

class PyOutline(QMainWindow):
    """ Handles UI: creates window, layout, adds a tree """

    def __init__(self):
        """ Create window, set parser and model instances
        """
        QMainWindow.__init__(self)

        # Parser instance
        self.__data = Parser()

        # Model
        self.__model = Tree(self.__data.getSymbolTree(), '')

        # View
        self.__tree = QTreeView()
        self.__tree.setModel(self.__model)

        # Window layout with tree
        self.__buildWindow()

    def __buildWindow(self):
        """ Create window

            Sets default window title,
            adds menu bar items,
            actually lays out the window,
            stores the model for further update
        """
        self.__buildMenu()
        self.content = QVBoxLayout()
        self.content.addWidget(self.__tree)
        self.setCentralWidget(self.__tree)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle()

    def __buildMenu(self):
        """ Add menu bar elements

            With related event-action bindings
        """
        # File
        file_menu = self.menuBar().addMenu('&File')
        action_open = file_menu.addAction('&Open file')
        action_open.setShortcut('Ctrl+O')
        action_open.triggered.connect(self.openFile)

        action_export = file_menu.addAction('Export to &XMI')
        action_export.triggered.connect(self.createXmi)

        # View
        view_menu =self.menuBar().addMenu('&View')
        action_collapse = view_menu.addAction('&Collapse all')
        action_collapse.triggered.connect(self.collapseAll)

        action_expand = view_menu.addAction('&Expand all')
        action_expand.triggered.connect(self.expandAll)


    def openFile(self):
        """ Menu action: open file

           Provide file chooser
           Given file, set file name for view and text for parser
        """
        filename, type = QFileDialog.getOpenFileName(self, 'Open file for inspection', os.getenv('HOME'))

        # Implementation note: it is the parser’s responsibility to
        # check if file is valid Python
        # Should we lock the file before reading?
        if not os.path.isfile(filename) or not os.access(filename, os.R_OK):
            return

        self.__model.setFileName(filename)
        self.setWindowTitle(filename)

        with open(filename, 'r') as f:
            data = f.read()

    def setWindowTitle(self, *filename):
        """ Set a normalised window title

            Based on file name & application name
        """
        if len(filename) is 0:
            super().setWindowTitle('PyParse')
        else:
            super().setWindowTitle(filename[0] + ' — Pyparse')

    def collapseAll(self):
        """ Collapse all tree levels """
        self.__tree.collapseAll()

    def expandAll(self):
        """ Expand all tree levels """
        self.__tree.expandAll()

    def createXmi(self):
        """ Create XMI file """
        pass

# Launch application
app = QApplication(sys.argv)
ui = PyOutline()
ui.show()

sys.exit(app.exec_())
