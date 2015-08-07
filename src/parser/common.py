#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This file implements 2 general class usable for every languages:
    . Symbol: base class of every symbol (based on the db table 'symbol')
    . File: base class of every file (based on the db table 'file')
"""

from .db_toolkit import *
from .conf import *
from pprint import pprint


class Symbol(object) :

    """Common operations and attributes shared by every symbols in every languages"""

    ### CONSTRUCTOR

    def __init__(self, id_file, code, dbcon) :
        """Basic constructor: initialized attributes and Symbol registered"""
        self.dbcon = dbcon      # Connection instance (for database)
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
        dic = { # preparing data to send in insert
          'tab': "symbol",
          'col': ["id_file", "id_type", "ini_line"],
          'val': [str(self.id_file), str(self.stype), str(self.iline)]
        }
        res = insert(dic, self.dbcon.cursor(), dbg=False)
        if not res : LOG('Err on register')
        else :
            self.id = self.__getID() # sets id when it's correctly registered

    def __getID(self) :
        """Get the ID of a Symbol from the databse"""
        dic = {
          'tab': "symbol",
          'col': ["id_symbol"], #finds with the file id and the init line
          'whr': "id_file='" + str(self.id_file) + \
           "' AND ini_line='"+ str(self.iline) + '\';'
        }
        res = select(dic, self.dbcon.cursor(), dbg=False)
        if not res : LOG('Err on getID')
        else :
            return res[0][0] # return first line and first column of result

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
        dic = {
          'tab': "symbol",
          'set': [["end_line", str(self.iline + len(self.code))]],
          #finds with the file id and the init line
          'whr': "id_file='" + str(self.id_file) + \
            "' AND ini_line='"+ str(self.iline) + '\';'
        }
        res = update(dic, self.dbcon.cursor(), dbg=True)
        if not res : LOG('Err on updateEline')
        else :
            return res

    def addCode(self, code) :
        """Add a instance of CodeLine to self.code array"""
        self.code.append(code)

class Parser (object) :

    """Common file and attributes used in any languages"""

    ### CONSTRUCTOR

    def __init__(self, fname, fpath, code, dbcon) :
        """Basic constructor: initialized attributes and File registered"""
        self.DBCON = dbcon  # Connection instance (for database)
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
        dic = {
          'tab': "file",
          'col': ["fname", "fpath"],
          'val': [self.FNAME, self.FPATH]
        }
        res = insert(dic, self.DBCON.cursor(), dbg=False)
        if not res :
            LOG('Err on register')
        else :
            return True

    def __getID(self) :
        """Gets current file ID in database"""
        dic = {
          'tab': "file",
          'col': ["id_file"],
          # finds using name and path attributes
          'whr': "fname='" + self.FNAME + \
            "' AND fpath='"+ self.FPATH + '\';'
        }
        res = select(dic, self.DBCON.cursor(), dbg=False)
        if not res :
            LOG('Err on getID')
            return False
        else :
            return res[0][0]

    def __preProcess(self) :
        """Abstract: method used for preprocessing the file"""
        return True

    def __scanCode(self, code) :
        """Abstract: method used for obtainning it's structuration"""
        return True

