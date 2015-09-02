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
    print("showSymb", line)
    s = NC.initClient("127.0.0.1", 1254)
    qry = 'SHOW' + str(line)
    s.sendall((qry + '\n').encode('utf-8'))
    s.close()

class SublimeServer(object) :

    def __init__ (self, UI) :
        self.UI = UI
        self.UI.stUse = True

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

