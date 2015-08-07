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
from pprint import pprint


class Symbol(object) :

    """Common operations and attributes shared by every symbols in every languages"""

    ### CONSTRUCTOR

    def __init__(self, id_file, code) :
        """Basic constructor: initialized attributes and Symbol registered"""
        self.DBC = DBC()
        self.id = None          # ID of the symbol
        self.id_file = id_file  # ID of the file
        self.stype = code.type  # type of symbol like analyzed in first line
        self.iline = code.nline # first line
        self.eline = code.nline # last line
        self.uline = []         # use line
        self.code = [code]      # array of CodeLine instance: store the contains of the symbol
        self.__register()       # register in db the symbol

    ### PRIVATE METHODS

    def __register(self) :
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
        """Prints line-number and initial-code of each CodeLine stored in Symbol"""
        for x in self.code :
            x.show()

    def showSym(self) :
        """Prints attributes of the current Symbol (use mostly in debugg)"""
        pprint (vars(self))

    def updateEline(self) :
        """Updates Symbol end line when its scanning is done"""
        values = [self.iline + len(self.code) - 1, self.id_file, self.iline]
        return self.DBC.updateEndLine(values)

    def addCode(self, code) :
        """Add a instance of CodeLine to self.code array"""
        self.code.append(code)

class Parser (object) :

    """Common file and attributes used in any languages"""

    ### CONSTRUCTOR

    def __init__(self, fname, fpath, code) :
        """Basic constructor: initialized attributes and File registered"""
        self.DBC = DBC()
        self.FNAME = fname  # file name
        self.FPATH = fpath  # file path
        self.ICODE = code   # initiale file code
        self.SCODE = []     # structure of a file (obtain after the scan)
        self.ID = 0         # file ID

        self.__register()
        self.ID = self.__getID()

    ### PRIVATE METHODS

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

