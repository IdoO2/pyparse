#!/usr/bin/python3
# -*- coding: utf-8 -*-

import inspect
from pprint import pprint

import re

import sublime, sublime_plugin

from Pyparse.parsermoc import Parser

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
