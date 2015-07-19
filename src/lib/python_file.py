#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This File implements the specific code for handling a Python File.
PreProcess of a file and scanning structure are defined here.
"""

import re
import sqlite3
from conf import *
from common import *
from python_type import *
from python_code_line import CodeLine
from python_common import *

class PythonFile (File) :

    """Specific code for handling a Python file"""

    ### CONSTRUCTOR

    def __init__(self, fname, fpath, code, dbcon, ident) :
        """Adds missing attributes used in a Python file"""
        super().__init__(fname, fpath, code, dbcon)
        self.IDENT = ident      # indentation size
        self.CCODE = self.__preProcess(code, ident) # clean code results of preprocess
        self.SCODE = self.scanCode(self.CCODE) # scan file content and returns code structure

    ### PRIVATE METHOD

    def __preProcess(self, txt, tab_len) :
        """Preprocessing a file:
            . tabulations are changed in whitespaces
            . multiline are changed in one line"""
        txt = txt.replace('\t', ' ' * tab_len).split('\n')
        i = 0

        while (i < len(txt)) :
            #si la déclaration est sur plusieurs lignes on la traite
            if txt[i].replace(' ', '') and re.findall(r'\\|\(', txt[i][-1]) :
                result = self.__multiLine(txt, i, txt[i][-1])
                txt[i] = result['line']
                #on ajoute des lignes vides
                for i in range(i+1, result['idx']+1) :
                    txt[i] = ''
                i += 1
                continue
            i += 1

    return '\n'.join(txt)

    def __multiLine(self, txt, i, patern) :
        """Process multiline instruction.
        Return a dic with end declaration index and concat line"""
        if patern == '\\' and txt[i+1][-1] == '\\' :
            txt[i+1] = txt[i][:-1] + ' ' + txt[i+1]
            return self.__multiLine(txt, i + 1, patern)
        elif patern == '(' and ')' not in txt[i+1] :
            txt[i+1] = txt[i][:-1] + ' ' + txt[i+1]
            return self.__multiLine(txt, i + 1, patern)
        elif patern == '\\' :
            txt[i] = txt[i][:-1] + ' ' + txt[i+1]
            return { 'idx': i + 1, 'line': txt[i] }
        elif patern == '(' :
            txt[i] = txt[i] + ' ' + txt[i+1]
            return { 'idx': i + 1, 'line': re.sub('\(|\)| {2}', '', txt[i]) }
        else :
            PC.LOG("UNK: " + txt[i])

    ### PUBLIC METHOD

    # under work...
    def scanCode(self, ccode) :
        """Scan a file code and return an array reprensting the file structure"""
        CodeLine.indent = self.IDENT # set ident for codeline

        arr = ccode.split("\n") ; res = []
        fifo = [None] # stores the context (ie the current symbol). first is global
        sym = lambda: fifo[-1] # current symbol
        #accessors depending on symbol presence:
        add = lambda l: sym().addCode(l) if type(sym()) in CLIST else res.append(l)
        cont = lambda: sym().id if type(sym()) in CLIST else 0
        styp = lambda: sym().stype if type(sym()) in CLIST else None
        i = 0

        while i < len(arr) :
            l = CodeLine(i+1, arr[i], cont())
            i += 1

            typ, lvl = l.getVariable()

####
            if styp() in [SYM_CLASS, SYM_FCT_MUL] + SYM_MET_MUL and lvl == 0 \
             and typ not in SYM_NEG :
                fifo = [None]
            if styp() in SYM_MET_MUL and lvl == 1 \
             and typ not in SYM_NEG :
                fifo.pop()
####
            if typ in [SYM_CLASS, SYM_FCT_MUL] :
                tmp = CDIC[typ](self.ID, l, self.DBCON)
                fifo.append(tmp)
                res.append(tmp)
                continue
            if typ in SYM_MET_MUL :
                tmp = CDIC[typ](self.ID, l, self.DBCON, cont())
                fifo.append(tmp)
                res.append(tmp)
                continue
####
            if typ in SYM_ONE and typ not in SYM_MET_ONE :
                res.append(CDIC[typ](self.ID, l, self.DBCON))
                continue
            if typ in SYM_ONE and typ in SYM_MET_ONE :
                res.append(CDIC[typ](self.ID, l, self.DBCON, cont()))
                continue
####
            if typ == SYM_GLO_VAR :
                res.append(CDIC[typ](self.ID, l, self.DBCON))
                continue
            if typ == SYM_ATTR_CLASS :
                res.append(CDIC[typ](self.ID, l, self.DBCON, cont()))
                continue
####
            add(l)
        return res

### Object Testing
if __name__ == '__main__':
    DB_CONN = sqlite3.connect(':memory:')
    fd = open(DB_STRUCT, 'r')
    DB_CONN.executescript(fd.read())
    fd.close()

    # for f in ['very_simple.py'] :
    for f in ['simple_oo.py', 'very_simple.py', 'complex.py'] * 50 :
        fd = open(TEST_DIRECTORY + f, 'r')
        test = PythonFile(f, TEST_DIRECTORY, fd.read(), DB_CONN, 4)
        fd.close()
        # for l in test.SCODE :
            # if type(l) in [Class, Function] : l.show()
            # print(l)
            # l.show()
            # print(l.stype)
