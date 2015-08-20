#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This file implements 2 general class usable for every languages:
    . Symbol: base class of every symbol (based on the db table 'symbol')
    . File: base class of every file (based on the db table 'file')
"""

from .db_toolkit import DBC
from .conf import *
# from pprint import pprint
import re

class Symbol(object) :

    """Common operations and attributes shared by every symbols in every languages"""

    ### CONSTRUCTOR

    def __init__(self) :
        """Basic constructor: initialized attributes and Symbol registered"""
        self.DBC = DBC()
        self.id = None          # ID of the symbol
        self.id_file = None  # ID of the file
        self.stype = None  # type of symbol like analyzed in first line
        self.iline = None # first line
        self.eline = None # last line
        self.uline = []         # use line
        self.code = []      # array of CodeLine instance: store the contains of the symbol


    def load(self, data) :
        """Basic constructor: initialized attributes and Symbol registered"""
        self.id = data[0]
        self.id_file = data[1]
        self.stype = data[2]
        self.iline = data[3]
        self.eline = data[4]

    def register(self, id_file, code) :
        """Basic constructor: initialized attributes and Symbol registered"""
        self.id = None          # ID of the symbol
        self.id_file = id_file  # ID of the file
        self.stype = code.type  # type of symbol like analyzed in first line
        self.iline = code.nline # first line
        self.eline = code.nline # last line
        self.uline = []         # use line
        self.code = [code]      # array of CodeLine instance: store the contains of the symbol
        self.__save()       # register in db the symbol


    ### PRIVATE METHODS

    def __save(self) :
        """Register a Symbol in databse using the Connection instance self.dbcon"""
        values = [str(self.id_file), str(self.stype), str(self.iline)]
        res = self.DBC.addSymbol(values)
        if not res : LOG('Err on register')
        else :
            self.id = self.__getID() # sets id when it's correctly registered

    def __getID(self) :
        """Gets current file ID in database"""
        values = [self.id_file, self.iline]
        return self.DBC.getSymbolID(values)

    ### PUBLIC METHODS

    def show(self) :
    # def __str__(self) :
        """Prints line-number and initial-code of each CodeLine stored in Symbol"""
        string = ''
        for x in self.code :
            string += x.show() + '\n'
        return string[:-1]

    def showSym(self) :
        """Prints attributes of the current Symbol (use mostly in debugg)"""
        return ''

    def updateEline(self) :
        """Updates Symbol end line when its scanning is done"""
        values = [self.iline + len(self.code) - 1, self.id_file, self.iline]
        return self.DBC.updateEndLine(values)

    def addCode(self, code) :
        """Add a instance of CodeLine to self.code array"""
        self.code.append(code)

class File(object) :

    """Common file and attributes used in any languages"""

    ### CONSTRUCTOR

    def __init__(self) :
        """Basic constructor: initialized attributes and File registered"""
        self.LINE_END = ''
        self.DBC = DBC()
        self.FNAME = ''  # file name
        self.FPATH = ''  # file path
        self.ICODE = ''   # initiale file code
        self.SCODE = []     # structure of a file (obtain after the scan)
        self.ID = 0         # file ID

    def process(self, fname, fpath) :
        """Basic constructor: initialized attributes and File registered"""
        fd = open(fpath + fname, 'r')
        code = fd.read()
        fd.close()

        self.LINE_END = self.__setLineEndings(code)
        self.FNAME = fname  # file name
        self.FPATH = fpath  # file path
        self.ICODE = code   # initiale file code
        self.SCODE = []     # structure of a file (obtain after the scan)
        self.ID = 0         # file ID

        self.__register()
        self.ID = self.__getID()

    ### PRIVATE METHODS

    def __setLineEndings(self, full_text):
        """ Set line endings (unix or windows)

            Must be one of `Unix` or `Windows`
        """
        res = re.findall('(\n|\c\r)', full_text)
        if not res : return
        return res[0]

    def __register(self) :
        """Registers Python file in database"""
        values = [self.FNAME, self.FPATH]
        res = self.DBC.addFile(values)
        if not res :
            LOG('Err on register')
        else :
            return True

    def __getID(self) :
        """Gets current file ID in database"""
        values = [self.FNAME, self.FPATH]
        return self.DBC.getFileID(values)

    def __preProcess(self) :
        """Abstract: method used for preprocessing the file"""
        return True

    def __scanCode(self, code) :
        """Abstract: method used for obtainning it's structuration"""
        return True

