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

    def __process(self, data) :
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
        """ Attempts to make sense of information from incoming requests

            Data is space separated
            The first four characters of idata indicate expected operation
        """
        idata.replace('\n', '')
        action = idata[0:4]
        qry = idata[4:]

        if action == "PROC":
            # Expected: `filename full/path/to/file_folder`
            # Fortunately file names never include spaces
            spc_sep_parts = qry.split()
            return self.__process([
                spc_sep_parts[0],
                ' '.join(spc_sep_parts[1:])
            ])
        elif action == "UPDT" :
            return self.__update(qry.split())
        else :
            return "ERROR " + idata

    def run(self) :
        NC.initTServer(1255, process=self.serverProcess)

