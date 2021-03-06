#!/usr/bin/env python3.4
#!-*- coding: utf8 -*-

# Libraries
import re
import sys
import os
from PyQt5.QtWidgets import (QTreeView, QApplication,
                            QMainWindow, QWidget, QVBoxLayout,
                            QFileDialog, QAbstractItemView, QAction, qApp,
                            QMessageBox)

# ST mode specific
st_mode = (len(sys.argv) == 2 and sys.argv[1] == '--sublime')
if st_mode:
    from threading import Thread
    from sublime_text.gui_side import SublimeServer, showSymb

# Application
from qmodel import Tree
from parser.python_file import PythonFile
from exporter import Xmi

class PyTreeView(QTreeView) :
    __st_mode = False
    def __init__(self, with_st):
        super(QTreeView, self).__init__()
        self.__st_mode = with_st

    def mouseDoubleClickEvent(self, event):
        if not self.__st_mode:
            return
        row_data = self.currentIndex().data()
        line_nb = re.search('\[(\d*)\]', row_data)
        if line_nb:
            showSymb(line_nb.group(1))


class PyOutline(QMainWindow):
    """ Handles UI: creates window, layout, adds a tree """

    __xmi = None
    __basepath = ''

    def __init__(self, with_st):
        """ Create window, set parser and model instances
        """
        QMainWindow.__init__(self)

        # Parser instance
        self.__data = PythonFile()

        # Model
        self.model = Tree([], '')

        # View
        self.__tree = PyTreeView(with_st)
        self.__tree.setUniformRowHeights(True)
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
        # x_pos, y_pos, width, height
        self.setGeometry(450, 150, 400, 550)
        self.setCentralWidget(self.__tree)
        self.setWindowTitle()
        self.statusBar()
        self.__buildMenu()

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

        if not fullpath:
            return

        if not os.path.isfile(fullpath) or not os.access(fullpath, os.R_OK):
            self.showMessage('This file doesn’t appear to be valid')
            print('Unable to open `{}`'.format(fullpath))
            return

        filepath, filename = os.path.split(fullpath)

        self.setWindowTitle(filename)
        self.model.setFileName(fullpath)

        self.__data = PythonFile()
        try:
            self.__data.process(filename, filepath + '/')
        except RuntimeError as em:
            print('Error while parsing file: {}'.format(em))
            self.showMessage('Sorry, an error has occurred while processing this file')

        try:
            self.model.setBranches(self.__data.getSymbolTree())
        except ValueError as em:
            print('Error while parsing tree: {}'.format(em))
            self.showMessage('Sorry, an error has occurred while processing this file')

        self.__tree.resizeColumnToContents(0)

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
        self.__tree.resizeColumnToContents(0)

    def createXmi(self):
        """ Create XMI file """
        msg = 'Sorry, we were unable to process your request'
        root = self.__basepath if self.__basepath != '' else os.getenv('HOME')
        filename, type = QFileDialog.getSaveFileName(self, 'Open file for inspection', root)

        path, name = os.path.split(filename)
        if not os.access(path, os.R_OK):
            self.showMessage('Sorry, this file couldn’t be written to')
            return

        if self.__xmi is None:
            self.__xmi = Xmi()
        try:
            self.__xmi.setTree(self.__data.getSymbolTree())
            self.__xmi.write(filename)
            self.statusBar().showMessage('{} successfully written'.format(name), 6000)
            return True
        except ValueError as em:
            print('bad format for data: {}'.format(em))
        except RuntimeError as em:
            print('should not be here: {}'.format(em))
        except OSError as em:
            msg = 'Sorry, we were unable to write to this file'
            print('inform: problem writing file {}'.format(em))
        self.showMessage(msg)

    def showMessage(self, text):
        """ Display a message to the user

            Only option is to say OK
        """
        dialog = QMessageBox(self)
        dialog.setText(text)
        dialog.exec_()

# Launch application
app = QApplication(sys.argv)
ui = PyOutline(st_mode)

if st_mode:
    server = SublimeServer(ui)
    thd = Thread(target=server.run)
    thd.setDaemon(True)
    thd.start()

ui.show()

sys.exit(app.exec_())
