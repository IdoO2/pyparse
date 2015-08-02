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
from qmodel import Tree
from parser import Parser

class PyOutline(QMainWindow):
    '''
    Handles UI: creates window, layout, adds a tree
    '''

    def __init__(self):
        QMainWindow.__init__(self)
        self.__buildMenu()

    def buildWindow(self, tree, model):
        self.__model = model
        self.content = QVBoxLayout()
        self.content.addWidget(tree)
        self.setCentralWidget(tree)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Code browser')

    def __buildMenu(self):
        file_menu = self.menuBar().addMenu('File')
        action_open = file_menu.addAction('Open file')
        action_open.setShortcut('Ctrl+O')
        action_open.triggered.connect(self.openFile)

    def openFile(self):
        filename, type = QFileDialog.getOpenFileName(self, 'Open file for inspection', os.getenv('HOME'))

        self.__model.setFileName(filename)

        with open(filename, 'r') as f:
            data = f.read()
            self.setWindowTitle(data[:10])
