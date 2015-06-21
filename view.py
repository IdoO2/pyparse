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
