#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This File implements the specific code for handling a Python File.
PreProcess of a file and scanning structure are defined here.
"""

import pdb
import re
from .conf import *
from .common import *
from .python_type import *
from .python_code_line import CodeLine
from .python_common import *

class PythonFile(File) :

    """Specific code for handling a Python file"""

    __sublime_line_endings = {'Unix': '\n', 'Windows': '\c\r'}
    __line_end = '\n'
    __text_lines = []
    __indent = {'type': 'spaces', 'value': 1}

    ### CONSTRUCTOR

    def __init__(self) :
        """Adds missing attributes used in a Python file"""
        super().__init__()
        self.IDENT = ''      # indentation size
        self.CCODE = [] # clean code results of preprocess
        self.SCODE = [] # scan file content and returns code structure

    ### PRIVATE METHOD

    def __preProcess(self, txt, tab_len) :
        """Preprocessing a file:
            . tabulations are changed in whitespaces
            . multiline are changed in one line"""
        print ('line end', self.LINE_END)
        arr_txt = txt.replace('\t', ' ' * tab_len).split(self.LINE_END)
        i = 0

        while (i < len(arr_txt)) :
            offset, lines = self.__multiLine(arr_txt[i:], "", 0, 0)
            arr_txt[i] = lines[0]
            for x in range(1, offset+1) :
                arr_txt[i+x] = ''
            i += 1
        return arr_txt

    def __multiLine(self, data, res, count, itir) :
        open_parenth = count + data[0].count('(')
        clos_parenth = data[0].count(')')
        if data[0] == '' :
            return itir, [res] + itir * ['']
        if data[0][-1] == '\\' :
            return self.__multiLine(data[1:], res + data[0][:-1], open_parenth - clos_parenth, itir + 1)
        elif open_parenth - clos_parenth == 0 :
            return itir, [res + data[0]] + itir * ['']
        else :
            return self.__multiLine(data[1:], res + data[0] + " ", open_parenth - clos_parenth, itir + 1)


    def __setIndent(self) :
        if self.LINE_END == '\n' :
            res = re.findall('\n[^\n#:]*: *\n( *)', self.ICODE)
        elif self.LINE_END == '\c\r' :
            res = re.findall('\c\r[^\c\r#:]*: *\c\r( *)', self.ICODE)

        for i in (sorted(res)) :
            if i != '' : return len(i)
        return 4

    ### PUBLIC METHOD

    def process(self, fname, fpath) :
        """Adds missing attributes used in a Python file"""
        super().process(fname, fpath)
        self.IDENT = self.__setIndent()      # indentation size
        self.CCODE = self.__preProcess(self.ICODE, self.IDENT) # clean code results of preprocess
        print (self.LINE_END.join(self.CCODE))
        self.SCODE = self.scanCode(self.CCODE) # scan file content and returns code structure


    # under work...
    def scanCode(self, ccode) :
        """Scan a file code and return an array reprensting the file structure"""
        CodeLine.indent = self.IDENT # set ident for codeline

        res = []
        fifo = [None] # stores the context (ie the current symbol). first is global
        sym = lambda: fifo[-1] # current symbol
        clas = lambda: fifo[1] if len(fifo) > 1 and type(fifo[1]) is Class else None
        #accessors depending on symbol presence:
        add = lambda l: sym().addCode(l) if type(sym()) in CLIST else res.append(l)
        cont = lambda: sym().id if type(sym()) in CLIST else 0
        styp = lambda: sym().stype if type(sym()) in CLIST else None

        i = 0

        while i < len(ccode) :
            try :
                l = CodeLine(i+1, ccode[i], cont())
                i += 1
                l.show()

                typ, lvl = l.getVariable()
####
                if styp() in [SYM_CLASS, SYM_FCT_MUL] + SYM_MET_MUL and lvl == 0 \
                 and typ not in SYM_NEG :
                    sym().updateEline()
                    l.context = 0
                    fifo = [None]
                if styp() in SYM_MET_MUL and lvl == 1 \
                 and typ not in SYM_NEG :
                    sym().updateEline()
                    fifo.pop()
                    l.context = cont()
####
                if typ in [SYM_CLASS, SYM_FCT_MUL] :
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l)
                    fifo.append(tmp)
                    l.context = cont()
                    res.append(tmp)
                    continue
                if typ in SYM_MET_MUL :
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l, cont())
                    fifo.append(tmp)
                    l.context = cont()
                    clas().addCode(l)
                    # res.append(tmp)
                    continue
####
                if typ in SYM_ONE and typ not in SYM_MET_ONE :
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l)
                    res.append(tmp)
                    l.context = res[-1].id
                    tmp.updateEline()
                    continue
                if typ in SYM_ONE and typ in SYM_MET_ONE :
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l, cont())
                    l.context = tmp.id
                    clas().addCode(l)
                    tmp.updateEline()
                    continue
####
                if typ == SYM_GLO_VAR :
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l)
                    res.append(tmp)
                    continue
                if typ == SYM_ATTR_CLASS :
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l, clas().id)
                    tmp.updateEline()
                    clas().addCode(l)
                    continue
####
                if clas():
                    clas().addCode(l)
                else : add(l)
            except:
                print ('error', l.show())
                pass
####
        for x in res :
            if type(x) in CLIST :
                x.updateEline()
        return res

    def getSymbolTree(self, start='', end=''):
        """ Return symbol tree """
        req_global = [
            ['Import', 'import', "10"],
            ['Variable', 'variable', "11"],
            ['Fonction', 'function', "12,13"],
            ['Classes', 'class', "14"],
        ]
        req_class = [
            ['Attribut', 'class_attr', "30"],
            ['Constructeur', 'method', '22,25'],
            ['Methode Publique', 'method', '20,23'],
            ['Methode Privé', 'method', '21,24']
        ]
        res = []

        for lib, tab, l in req_global :
            tmp_arr = []
            tmp_ins = None
            if tab not in ['class'] :
                arr = self.DBC.getGlobalSymbols([l, self.ID, tab])
                if not arr : continue
                for x in arr :
                    tmp_ins = CDIC[int(x[2])]()
                    tmp_ins.load(x)
                    tmp_arr.append(tmp_ins.symbRepr())
                res.append([lib] + tmp_arr)
                continue
            elif tab in ['class'] :
                arr = self.DBC.getGlobalSymbols([l, self.ID, tab])
                if not arr : continue
                for x in arr :
                    id_class = x[0]
                    tmp_ins = CDIC[int(x[2])]()
                    tmp_ins.load(x)
                    tmp_arr.append(tmp_ins.symbRepr())
                    for lib2, tab2, l in req_class :
                        tmp_arr2 = []
                        for z in self.DBC.getClassSymbols([l, self.ID, tab2, id_class]) :
                            tmp_ins = CDIC[int(z[2])]()
                            tmp_ins.load(z)
                            tmp_arr2.append(tmp_ins.symbRepr())
                        if not tmp_arr2 : continue
                        tmp_arr.append([lib2] + tmp_arr2)
                    res.append([lib] + [tmp_arr])
            if not arr : continue
        return res
