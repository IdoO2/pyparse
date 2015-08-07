#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This File implements the specific code for handling a Python File.
PreProcess of a file and scanning structure are defined here.
"""

import re
from .conf import *
from .common import *
from .python_type import *
from .python_code_line import CodeLine
from .python_common import *

class PythonParser (Parser) :

    """Specific code for handling a Python file"""

    __sublime_line_endings = {'Unix': '\n', 'Windows': '\c\r'}
    __line_end = '\n'
    __text_lines = []
    __indent = {'type': 'spaces', 'value': 1}

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
        return txt

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

    def __setLineEndings(self, full_text):
        """ Set line endings (unix or windows)

            Must be one of `Unix` or `Windows`
        """
        find_le = re.compile('(\n|\c\r)')
        le_found = find_le.match(full_text)
        if le_found is None:
            return
        if '\n' in le_found.group(0):
            self.__line_end = self.__sublime_line_endings['Unix']
        else:
            self.__line_end = self.__sublime_line_endings['Windows']

    def __setIndent(self):
        """ Determine indentation one character at a time
            Sets self.__indent, a dict with keys <str>type, <int>value
            Alternative to __setIndentRegex
        """
        for line in self.__text_lines:
            if line[0] is '\t':
                self.__indent['type'] = 'tabs'
                break
            if line[0] is ' ':
                i = 1
                while line[i] is ' ':
                    i += 1
                    self.__indent['value'] = i
            break

    def __setIndentRegex(self):
        """ Determine indentation using a regex
            Sets self.__indent, a dict with keys <str>type, <int>value
            Alternative to __setIndent
        """
        for line in self.__text_lines:
            ##indentRegex = '(?<=:' + le + ')^\s+'
            find_space = re.compile('^\s+')
            space_found = find_space.match(line)
            if space_found is None:
                continue
            else:
                if '\t' in space_found.group(0):
                    self.__indent['type'] = 'tabs'
                else:
                    self.__indent['value'] = len(space_found.group(0))
                break



    ### PUBLIC METHOD

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
            l = CodeLine(i+1, ccode[i], cont())
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
                tmp = CDIC[typ](self.ID, l)
                fifo.append(tmp)
                l.context = cont()
                res.append(tmp)
                continue
            if typ in SYM_MET_MUL :
                tmp = CDIC[typ](self.ID, l, cont())
                fifo.append(tmp)
                l.context = cont()
                clas().addCode(l)
                res.append(tmp)
                continue
####
            if typ in SYM_ONE and typ not in SYM_MET_ONE :
                res.append(CDIC[typ](self.ID, l))
                l.context = res[-1].id
                continue
            if typ in SYM_ONE and typ in SYM_MET_ONE :
                res.append(CDIC[typ](self.ID, l, cont()))
                l.context = res[-1].id
                clas().addCode(l)
                continue
####
            if typ == SYM_GLO_VAR :
                res.append(CDIC[typ](self.ID, l))
                continue
            if typ == SYM_ATTR_CLASS :
                res.append(CDIC[typ](self.ID, l, cont()))
                clas().addCode(l)
                continue
####
            if clas():
                clas().addCode(l)
            else : add(l)
####
        for x in res :
            if type(x) in CLIST :
                x.updateEline()
        return res

    def getSymbolTree(self):
        """ Return symbol tree """
        return [
            ['Master',
                'randval', ['__init__',
                    'change']]
        ]

    def updateWith(self, file_contents):
        """ Receive full text, raw, from UI

            Diffs current state of file with incoming state
            Triggers relevant actions on change
            Obviously the current state of this function is utterly broken
            (doesn’t handle line number changes)
        """
        if len(self.__text_lines) is 0:
            # No text? -> Initial population
            self.__setLineEndings(file_contents)
            self.__text_lines = file_contents.split(self.__line_end)
            self.__setIndent()

        new_state = file_contents.split(self.__line_end)
        for idx in range(len(new_state)):
            if new_state[idx] != self.__text_lines[idx]:
                print(new_state[idx])
                pass # ... on to model
