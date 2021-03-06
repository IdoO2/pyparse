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
import os
import re

class Symbol(object) :

    """Common operations and attributes shared by every symbols in every languages"""

    ### CONSTRUCTOR

    def __init__(self) :
        """Basic constructor: initialized attributes and Symbol registered"""
        self.DBC     = DBC()        # database connection
        self.id      = None         # symbol ID
        self.id_file = None         # file ID
        self.stype   = None         # type of symbol
        self.iline   = None         # first line
        self.eline   = None         # last line
        self.uline   = []           # array of lines using this symbol
        self.code    = []           # array of CodeLine instance: store the contains of the symbol

    ### PRIVATE METHODS

    def __save(self) :
        """Register a Symbol in databse using the Connection instance"""
        values = [str(self.id_file), str(self.stype), str(self.iline)]
        res = self.DBC.addSymbol(values)
        if not res : LOG('Err on register')
        else :
            self.id = self.__getID() # sets id when it's correctly registered
            return True

    def __getID(self) :
        """Gets current file ID in database"""
        values = [self.id_file, self.iline]
        return self.DBC.getSymbolID(values)

    ### PUBLIC METHODS

    def load(self, data) :
        """Load attribute from a data attribute"""
        self.id      = data[0]      # symbol ID
        self.id_file = data[1]      # file ID
        self.stype   = data[2]      # type of symbol
        self.iline   = data[3]      # first line
        self.eline   = data[4]      # last line

    def register(self, id_file, code) :
        """Register a symbol in database"""
        self.id      = None         # symbol ID
        self.id_file = id_file      # file ID
        self.stype   = code.type    # type of symbol
        self.iline   = code.nline   # first line
        self.eline   = code.nline   # last line
        self.uline   = []           # array of lines using this symbol
        self.code    = [code]       # array of CodeLine instance: store the contains of the symbol
        return self.__save()               # database registration


    def show(self) :
        """Return a concatenate string of line representations"""
        string = ''
        for x in self.code :
            string += x.show() + '\n'
        return string[:-1]

    def updateEline(self) :
        """Updates symbol end line when scanning is done"""
        values = [self.iline + len(self.code) - 1, self.id_file, self.iline]
        return self.DBC.updateEndLine(values)

    def symbRepr(self) :
        """return an array representative of current Symbol"""
        return [str(self.id_file) + ' ' + str(self.iline) + ' [' + str(self.stype) + ']']

    def addCode(self, code) :
        """Add a instance of CodeLine to self.code array"""
        self.code.append(code)

class File(object) :

    """Common file and attributes used in any languages"""

    ### CONSTRUCTOR

    def __init__(self) :
        """Basic constructor: initialized attributes"""
        self.DBC      = DBC()   # database connection
        self.LINE_END = ''      # line ending style : Unix or Linux
        self.FNAME    = ''      # file name
        self.FPATH    = ''      # file path
        self.ICODE    = ''      # initiale file code
        self.SCODE    = []      # file structure
        self.ID       = 0       # file ID

    ### PRIVATE METHODS

    def __setLineEndings(self, full_text):
        """ Set line endings (unix or windows) """
        le = re.search('(\n|\c\r)', full_text)
        if not le:
            LOG('Unable to determine line endings type')
            self.LINE_END = '\n'
        else : self.LINE_END = le.group()

    def __register(self) :
        """Register file in database"""
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

    ### PUBLIC METHODS

    def process(self, fname, fpath):
        """Process a file"""
        fullpath = fpath + fname
        if not os.path.isfile(fullpath) or not os.access(fullpath, os.R_OK):
            raise RuntimeError('File {} is not readable'.format(fullpath))
        fd = open(fullpath, 'r')
        code = fd.read() # get file content
        fd.close()

        self.__setLineEndings(code)
        self.FNAME = fname # file name
        self.FPATH = fpath # file path
        self.ICODE = code # initiale file content

        self.__register() # register file in database
        self.ID = self.__getID() # get file ID
