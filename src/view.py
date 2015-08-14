#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Daniel PATERSON

# Note on performance: in our case, consider setting `uniformRowHeights = True`

# Example file:
# 1. class Master():
# 2.   randval = 0
# 3.   def __init__(self):
# 4.     self.randval = 1
# 5.     def change():
# 6.       self.randval = 3

data = [['Import', ['Tkinter [2]', 'Button', 'Frame', 'Label', 'Pack'], ['pdb [3]', 'set_trace']], ['Variable', 'a [38]'], ['Fonction', 'main1 [5]', 'main2 [7]', 'test [33]'], ['Classes', ['ClickCounter [11]', ['Attribut', 'count + [18]', 'label[]  [19]', 'label  [22]', 'button  [24]', 'count  [31]'], ['Constructeur', '__init__ [27]'], ['Methode Publique', 'main3 [13]', 'main4 [14]', 'click [17]', 'createWidgets [21]']]]]


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
import pdb

# Libraries
import re
import sys
import os
from PyQt5.QtWidgets import (QTreeView, QApplication,
                            QMainWindow, QWidget, QVBoxLayout,
                            QFileDialog, QAbstractItemView, QAction, qApp)
from PyQt5.QtCore import QDir, Qt, QStringListModel
from PyQt5.QtGui import QIcon


# Application
from qmodel import Tree
from parser.python_file import PythonFile
from parser.db_toolkit import DBC
from exporter import Xmi

class PyOutline(QMainWindow):
    """ Handles UI: creates window, layout, adds a tree """

    __xmi = None

    def __init__(self):
        """ Create window, set parser and model instances
        """
        QMainWindow.__init__(self)

        # Parser instance
        self.__data = DBC()

        # Model
        self.__model = Tree(data, '')

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
        content = QVBoxLayout()
        content.addWidget(self.__tree)
        self.setLayout(content)
        self.setGeometry(300, 300, 300, 150)
        self.setCentralWidget(self.__tree)
        self.setWindowTitle()
        #self.menuBar()

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

        action_exit = file_menu.addAction('&Quit')
        action_exit.triggered.connect(self.close)

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
        filepath, _type = QFileDialog.getOpenFileName(self, 'Open file for inspection', os.getenv('HOME'))

        if not os.path.isfile(filepath) or not os.access(filepath, os.R_OK):
            return

        filename = re.findall(r'[^/\\]+$', filepath)[0]

        self.__model.setFileName(filename)
        self.setWindowTitle(filename)
        print(self.__model)
        # pfile = PythonFile(filename, filepath)
        # pfile.process()

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
        if self.__xmi is None:
            self.__xmi = Xmi()
        try:
            self.__xmi.setTree(self.__data.getSymbolTree())
            self.__xmi.write('somewhere.xmi')
        except ValueError:
            pass # inform: bad format for data
        except RuntimeError:
            pass # inform: but should not be here
        except OSError:
            pass # inform: problem writing file

# Launch application
app = QApplication(sys.argv)
ui = PyOutline()
ui.show()

sys.exit(app.exec_())
