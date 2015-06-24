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
    [(0, 0, 'Master | class')],
    [(-1, 0, 'randval | func')],
    [(-2, 1, '__init_ | func')],
    [None],
    [(-2, 0, 'change | func')],
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

class Parser():
    'Simple POC for parser I/O'
    map = [
        [0, 0, 'Master | class'],
        [-1, 0, 'randval | func'],
        [-2, 1, '__init_ | func'],
        None,
        [-2, 0, 'change | func'],
        None
    ]

    def loop(self):
        'For testing purposes takes user input to update model'
        while True:
            update = input('Make a change (format: `3 def __init__(self, newarg):i`):')
            lst = self.parseArgs(update)
            if not lst:
                continue
            line, val, rel_idx, loc_idx, idx, txt = lst
            if idx == 0:
                if txt is not val:
                    data.item(idx).setText(val)
            else:
                parent_idx = line + rel_idx
                parent = data.item(parent_idx)
                parent.child(loc_idx).setText(val)

    def parseArgs(self, update):
        '''
        Very basic arguments parsing:
        input format is `3 some code`
        where `3` is a line number and the rest is the content of the line
        Returns
        - int line number
        - str val
        - int rel_idx relation of line to previous lines
        - in local_idx index of symbol in its scope
        - idx idx actual index in list
        - str txt redundant with val while parser doesn’t parse
        '''
        line = int(update[0])
        val = update[2:]

        if line >= len(self.map) or self.map[line] is None:
            return False

        rel_idx = int(self.map[line][0])
        local_idx = int(self.map[line][1])
        idx = self.map[line][rel_idx + local_idx]
        txt = self.map[line][2]
        return line, val, rel_idx, local_idx, idx, txt


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

    run = Parser()
    run.loop()

    sys.exit(app.exec_())
