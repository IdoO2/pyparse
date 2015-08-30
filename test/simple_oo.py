#!/usr/bin/env python
from Tkinter import Button, Frame,\
Label, Pack
from pdb import set_trace
# Libraries
import re
import sys
import os
from PyQt5.QtWidgets import (QTreeView, QApplication,
                            QMainWindow, QWidget, QVBoxLayout,
                            QFileDialog, QAbstractItemView, QAction, qApp)
from PyQt5.QtCore import QDir, Qt, QStringListModel
from PyQt5.QtGui import QIcon


def main1() : return 0


def main2() :
	print ()
	print ()

class ClickCounter(Frame):

	def main3(self) : return
	def main4(self) :
		return

    def click(self):
        self.count += 1
        self.label['text'] = 'Number of clicks: %d' % self.count

    def createWidgets(self):
        self.label = Label(self, text='here have been no clicks yet')
        self.label.pack()
        self.button = Button(self, text='click me', command=self.click)
        self.button.pack()

    def __init__(self, master=None):
        Frame.__init__(self, master)
        Pack.config(self)
        self.createWidgets()
        self.count = 0
