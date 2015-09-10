#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

import sys
import os
sys.path.append(sys.path.append(\
  os.sep.join(os.getcwd().split(os.sep)[:os.getcwd().split(os.sep).index('pyparse')]+['pyparse' + os.sep]))) #fixing python path


from src.parser.python_file import PythonFile
import src.sublime_text.network_common as NC


def showSymb(line) :
    try:
        s = NC.initClient("127.0.0.1", 1254)
        query = 'SHOW{}\n'.format(line).encode('utf-8')
        s.sendall(query)
        s.close()
    except RuntimeError as em:
        print('Connection error: {}'.format(em))

class SublimeServer(object) :

    def __init__ (self, UI) :
        self.UI = UI

    def __process(self, fullpath) :
        filepath, filename = os.path.split(fullpath)

        self.UI.setWindowTitle(filename)
        self.UI.data = PythonFile()
        self.UI.data.process(filename, filepath + '/')
        self.UI.model.setFileName(fullpath)
        self.UI.model.setBranches(self.UI.data.getSymbolTree())
        return '200'

    def serverProcess(self, idata, add_data) :
        """ Attempts to make sense of information from incoming requests

            The first four characters of idata indicate expected operation
        """
        action, query = idata[:4], idata[4:]

        if action != "PROC":
            return '500'

        return self.__process(query)

    def run(self) :
        NC.initTServer(1255, process=self.serverProcess)
