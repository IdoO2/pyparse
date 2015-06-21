# Based on C++ Qt documentation found at
# http://doc.qt.io/qt-5/qtreeview.html

# Note on performance: in our case, consider setting `uniformRowHeights = True`

# Helpers
import inspect
from pprint import pprint

# Libraries
import sys
from PyQt5.QtWidgets import (QTreeView, QApplication,
                            QMainWindow, QWidget, QVBoxLayout)
from PyQt5.QtCore import QDir, Qt, QStringListModel

# from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem)

# Application
#from model import TreeItem, TreeModel

from qmodel import Tree


class PyOutline(QMainWindow):

    def __init__(self):
        super().__init__()

    def buildWindow(self, tree):
        self.content = QVBoxLayout()
        self.content.addWidget(tree)
        self.setCentralWidget(tree)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Some file')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    view = PyOutline()

    data = [
        'root',
        [
            'branch1', 'b1s1', 'b1s2',
            ['subbranch1', 'b1s1s1', 'b1s1s2']
        ]
    ]

    # data = TreeModel('Filename', None)
    data = Tree(data)

    # root = TreeItem('root', None)
    # child = TreeItem('ooga', root)
    # root.appendChild(child)

    # # Test with ListModel: apprently doesn’t display children
    # root = QStringListModel()
    # child = QStringListModel(['one', 'two', 'three'], root)
    # treeData = QStringListModel(['four', 'five', 'six'], child)

    tree = QTreeView()
    tree.setModel(data)

    #pprint(inspect.getmembers(tree))

    view.buildWindow(tree)
    view.show()

    sys.exit(app.exec_())
