#!/usr/bin/env python3.4
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

# data = [['Import', ['Tkinter [2]', 'Button', 'Frame', 'Label', 'Pack'], ['pdb [3]', 'set_trace']], ['Variable', 'a [38]'], ['Fonction', 'main1 [5]', 'main2 [7]', 'test [33]'], ['Classes', ['ClickCounter [11]', ['Attribut', 'count + [18]', 'label[]  [19]', 'label  [22]', 'button  [24]', 'count  [31]'], ['Constructeur', '__init__ [27]'], ['Methode Publique', 'main3 [13]', 'main4 [14]', 'click [17]', 'createWidgets [21]']]]]


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

data = [
  ['Import',
    ['sqlite3 [10]', ''],
    ['.conf [11]', '*']
  ],
  ['Classes',
    ['DBC [13]',
      ['Constructeur', '__init__ [17]'],
      ['Methode Publique', 'addSymbol [73]', 'addFile [80]', 'getFileID [87]', 'getSymbolID [95]', 'updateEndLine [103]', 'updateSymbol [111]', 'getGlobalSymbols [121]', 'getClassSymbols [130]', 'close [139]'],
      ['Methode Privé', '__save [26]', '__select [37]', '__getSymbols [47]', '__getGlobalSymbol [54]', '__getClassSymbol [61]']],
     ['DBCZ [143]',
      ['Constructeur', '__init__ [147]']]
   ]
]

data = [['Import', ['re,sys [5]', ''], ['type_code [6]', '*'], ['time [7]', 'timezone'], ['types [8]', 'NoneType', 'TypeType']], ['Variable', 'test1 [10]', 'test2 [13]', 'a [17]', 'b [22]', 'c [24]', 'M [28]', 'rdic [51]', 'msg [249]', 'fd [253]'], ['Fonction', 'cleanLine [35]', 'execReg [42]', 'onliner [46]', 'onliner2 [47]'], ['Classes', ['Test1 [73]'], ['Test [76]', ['Constructeur', '__init__ [77]'], ['Methode Publique', 'test [79]']], ['CCode [81]', ['Attribut', 'varType [84]', 'include [88]', 'define [89]', 'typedef [90]', 'fonction [91]', 'vars [92]', 'txt [93]', 'symbol [94]'], ['Constructeur', '__init__ [83]'], ['Methode Publique', 'showSymbol [241]'], ['Methode Privé', '__preProcess [105]', '__addInclude [147]', '__addDefine [152]', '__addTypedef [165]', '__addFunction [174]', '__addVariable [183]', '__isTyped [206]', '__getSymbol [211]', '__setUse [227]']]]]




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
import network_common as NC
from threading import Thread

class SublimeServer(object) :

    def __init__ (self, UI) :
        self.UI = UI

    def __process(self, data) :
        print (data)
        filename = data[0]
        filepath = data[1]
        fullpath = filepath + '/' + filename

        self.UI.setWindowTitle(filename)
        self.UI.data = PythonFile()
        self.UI.data.process(filename, filepath + '/')
        self.UI.model.setFileName(fullpath)
        self.UI.model.setBranches(self.UI.data.getSymbolTree())
        return "PROCESS OK"

    def __update(self, data) :
        filename = ''
        filepath = ''
        fullpath = filepath + '/' + filename

        self.UI.data = PythonFile()
        self.UI.data.process(filename, filepath + '/')
        self.UI.model.setFileName(fullpath)
        self.UI.model.setBranches(self.UI.data.getSymbolTree())
        return "UPDT OK"

    def serverProcess(self, idata, add_data) :
    # on récupère la donnée et on dirige les requêtes vers les bonnes fonctions
        idata.replace('\n', '')
        op = idata[0:4]
        qry = idata[4:]

        if op == "PROC" :
            return self.__process(qry.split())
        elif op == "UPDT" :
            return self.__update(qry.split())
        else :
            return "ERROR " + idata

    def run(self) :
        NC.initTServer(1255, process=self.serverProcess)


class PyOutline(QMainWindow):
    """ Handles UI: creates window, layout, adds a tree """

    __xmi = None
    __basepath = ''

    def __init__(self):
        """ Create window, set parser and model instances
        """
        QMainWindow.__init__(self)

        # Parser instance
        self.__data = PythonFile()

        # Model
        self.__model = Tree([], '')

        # View
        self.__tree = QTreeView()
        self.__tree.setModel(self.model)

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
        self.setGeometry(300, 300, 300, 150)
        self.setCentralWidget(self.__tree)
        self.setWindowTitle()
        # self.__buildMenu()
        #self.model.setBranches([])
        self.model.setBranches(self.data.getSymbolTree())
        #self.model.setBranches([])

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
        action_exit.setShortcut('Ctrl+Q')
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
        fullpath, type_ = QFileDialog.getOpenFileName(self, 'Open file for inspection', os.getenv('HOME'))

        if not os.path.isfile(fullpath) or not os.access(fullpath, os.R_OK):
            return

        filepath, filename = os.path.split(fullpath)

        self.setWindowTitle(filename)
        self.data = PythonFile()
        self.data.process(filename, filepath + '/')
        self.model.setFileName(fullpath)
        self.model.setBranches(self.data.getSymbolTree())

    def setWindowTitle(self, *filename):
        """ Set a normalised window title

            Based on file name & application name
        """
        if len(filename) is 0:
            super().setWindowTitle('PyParse')
        else:
            path, name = os.path.split(filename[0])
            self.__basepath = path
            super().setWindowTitle('{} ({}) — Pyparse'.format(name, path))

    def collapseAll(self):
        """ Collapse all tree levels """
        self.__tree.collapseAll()

    def expandAll(self):
        """ Expand all tree levels """
        self.__tree.expandAll()

    def createXmi(self):
        """ Create XMI file """
        #filename, type = QFileDialog.getOpenFileName(self, 'Open file for inspection', os.getenv('HOME'))
        root = self.__basepath != '' if self.__basepath != '' else os.getenv('HOME')
        filename, type = QFileDialog.getSaveFileName(self, 'Open file for inspection', root)

        path, name = os.path.split(filename)
        if not os.access(path, os.R_OK):
            return

        if self.__xmi is None:
            self.__xmi = Xmi()
        try:
            self.__xmi.setTree(self.data.getSymbolTree())
            self.__xmi.write(filename)
        except ValueError:
            pass # inform: bad format for data
        except RuntimeError:
            pass # inform: but should not be here
        except OSError:
            pass # inform: problem writing file

# Launch application
app = QApplication(sys.argv)
ui = PyOutline()

server = SublimeServer(ui)
thd = Thread(target=server.run)
thd.setDaemon(True)
thd.start()


ui.show()

sys.exit(app.exec_())
