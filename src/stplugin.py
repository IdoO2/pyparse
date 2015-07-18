#!/usr/bin/python3
# -*- coding: utf-8 -*-

import inspect
from pprint import pprint

import re

import sublime, sublime_plugin

from Pyparse.parsermoc import Parser


class pyparse_markCommand(sublime_plugin.TextCommand):
    """pyparse_mark:
    A st commands used for sending a file to analyzer"""
    def run (self, edit) :
        # get some interesting var:
        vdic = self.view.window().extract_variables()
        # get code from current file:
        icode = self.view.substr(sublime.Region(0, self.view.size()))
        # get ident size from settings:
        ident = self.view.settings().get("tab_size")

        print (vdic, icode, ident) # print var

        #link to analyzer not done yet
        # pfile = PythonFile(vdic["file_name"], vdic["file_path"], icode, ident)

class pyparse_unmarkCommand(sublime_plugin.TextCommand):
    """pyparse_unmark:
    A st commands used for deleting a file registered in the analyzer"""
    # link to the analyzer not done yet
    def run (self, edit) :
        print ('pyparse_unmark')
        # get some interesting var:
        vdic = self.view.window().extract_variables()
        print (vdic["file_name"], vdic["file_path"])


class TransmitUpdates(sublime_plugin.EventListener):

    def __init__(self):
        super(sublime_plugin.EventListener, self).__init__()
        self.__browser = None

    def on_activated(self, view):
        self.__browser = Parser(self.__getWholeFile(view), view.line_endings())

    def on_pre_save(self, view):
        self.__browser.updateWith(self.__getWholeFile(view))

    def __getWholeFile(self, view):
        whole_file = sublime.Region(0, view.size() - 1)
        return view.substr(whole_file)


