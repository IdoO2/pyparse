# Note on performance: in our case, consider setting `uniformRowHeights = True`

# Test
# This tree would be represented as
# branch1
#   b1s1
#   b1s2
#   subbranch1
#     b1s1s1
#     b1s1s2
data = [
    [
        'branch1',
        'b1s1', 'b1s2', ['subbranch1',
            'b1s1s1', 'b1s1s2']
    ]
]

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
mapping = [
    [(0, 0)],
    [(-1, 0)],
    [(-2, 1)],
    [None],
    [(-2, 0)],
    [None]
]

# Helpers
import inspect
from pprint import pprint

# Libraries
import sys
from PyQt5.QtWidgets import (QTreeView, QApplication,
                            QMainWindow, QWidget, QVBoxLayout)
from PyQt5.QtCore import QDir, Qt, QStringListModel

# Application
from qmodel import Tree

class PyOutline(QMainWindow):
    '''
    Handles UI: creates window, layout, adds a tree
    '''
    def buildWindow(self, tree):
        self.content = QVBoxLayout()
        self.content.addWidget(tree)
        self.setCentralWidget(tree)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Code browser')

# Run Qt application
if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = PyOutline()

    # Model
    data = Tree(data, 'Some file')

    # Test operations
    data.addRow(1, 'NewBranch') # Test: add item at root index 1
    data.addRow(0, 'NewSubBranch', data.item(1)) # Test: add items at item index 0 of root index 2

    # View
    tree = QTreeView()
    tree.setModel(data)

    # Test operation
    data.item(1).setData('SubItemName', Qt.DisplayRole) # Test: change text of root index 1

    ui.buildWindow(tree)
    ui.show()

    sys.exit(app.exec_())
