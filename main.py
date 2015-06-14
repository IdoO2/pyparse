import sys
from PyQt5.QtWidgets import (QApplication,
                             QMainWindow, QWidget, QVBoxLayout,
                             QTreeWidget, QTreeWidgetItem)


class PyOutline(QMainWindow):

    def __init__(self):
        super().__init__()

        self.buildWindow()

    def buildWindow(self):
        self.content = QVBoxLayout()
        self.content.addWidget(self.buildTree())
        #self.setLayout(self.content)
        self.setCentralWidget(self.buildTree())

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Some file')
        self.show()

    def buildTree(self):
        tree = QTreeWidget()
        tree.setColumnCount(1);
        items = []
        for x in self.fakeGetElements():
            if isinstance(x, list):
                sub = []
                for y in x:
                    le = QTreeWidgetItem()
                    le.setText(0, y)
                    sub += [le]
                    items += sub
            elif isinstance(x, dict):
                # Just one iteration
                for title, sublist in x.items():
                    inner = QTreeWidgetItem()
                    inner.setText(0, title)
                    sub = []
                    for z in sublist:
                        le = QTreeWidgetItem(inner)
                        le.setText(0, z)
                        sub += [le]
                    tree.insertTopLevelItem(0, inner);
                    inner.setExpanded(True)
            else:
                it = QTreeWidgetItem()
                it.setText(0, x)
                tree.insertTopLevelItem(0, it);
            #tree.insertTopLevelItems(0, items);
        return tree

    def fakeGetElements(self):
        return [
            { 'className': [
                'method1',
                'method2',
                'attribute1',
                'attribute2'
            ] }
        ]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyOutline()
    sys.exit(app.exec_())
