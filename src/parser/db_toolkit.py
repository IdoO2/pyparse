#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This File implements a database wrapper.
The aim of this wrapper is to normalize database operations.
"""

import sqlite3
from .conf import *

class DBC():

    ### CONSTRUCTOR

    def __init__(self):
        """Establish a database connection and execute an environment query"""
        self.DB_CONN = sqlite3.connect(DB_SYMBOL)
        self.DB_CURS = self.DB_CONN.cursor()
        self.DB_CURS.executescript('PRAGMA synchronous = OFF; PRAGMA foreign_keys = ON;')
        self.DB_CONN.commit()

    ### PRIVATE METHODS

    def __save(self, sql):
        """Normalize Insert and Update query executions"""
        try:
            self.DB_CURS.execute(sql)
            self.DB_CONN.commit()
        except :
            LOG('Issue while inserting data in db.')
            LOG(sql)
            return False
        return True

    def __select(self, sql):
        """Normalize Select query executions"""
        try:
            self.DB_CURS.execute(sql)
        except :
            LOG('Issue while inserting data in db.')
            LOG(sql)
            return False
        return self.DB_CURS.fetchall()

    def __getSymbols(self, values) :
        """Get all symbols corresponding to a of list types"""
        sql = 'SELECT id_symbol FROM symbol WHERE id_type IN (' + str(values[0])
        sql += ') AND id_file=\'' + str(values[1]) + '\''
        sql += ' ORDER BY ini_line ASC;'
        return self.__select(sql)

    def __getGlobalSymbol(self, values) :
        """Return a single non-Class symbol"""
        sql1 = 'SELECT * FROM symbol WHERE id_symbol=\'' + str(values[0]) + '\';'
        sql2 = 'SELECT * FROM ' + str(values[1]) + ' WHERE id_symbol=\'' + str(values[0]) + '\';'
        tmp = list(self.__select(sql1)[0]) + list(self.__select(sql2)[0])
        return tmp

    def __getClassSymbol(self, values) :
        """Return a single Class symbol"""
        sql1 = 'SELECT * FROM symbol WHERE id_symbol=\'' + str(values[0]) + '\';'
        sql2 = 'SELECT * FROM ' + str(values[1]) + ' WHERE id_symbol=\'' + str(values[0]) + '\' '
        sql2 += 'AND id_class=\'' + str(values[2]) + '\';'
        res1 = self.__select(sql1)
        res2 = self.__select(sql2)
        if not (res1 and res2) : return []
        return list(res1[0]) + list(res2[0])

    ### PUBLIC METHODS

    def addSymbol(self, values):
        """Add a symbol to database"""
        if self.getSymbolID([values[0], values[2]]) : return True
        sql = 'INSERT INTO symbol ("id_file", "id_type", "ini_line") VALUES '
        sql += "('" + '\', \''.join(values) + "');"
        return self.__save(sql)

    def addFile(self, values):
        """Add a file to database"""
        if self.getFileID(values) : return True
        sql = 'INSERT INTO file ("fname", "fpath") VALUES '
        sql += "('" + '\', \''.join(values) + "');"
        return self.__save(sql)

    def getFileID(self, values):
        """Get a file ID"""
        sql = 'SELECT id_file FROM file WHERE fname=\'' + str(values[0])
        sql += '\' AND fpath=\'' + str(values[1]) + '\';'
        res = self.__select(sql)
        if res : return res[0][0]
        return None

    def getSymbolID(self, values):
        """Get a Symbol ID"""
        sql = 'SELECT id_symbol FROM symbol WHERE id_file=\'' + str(values[0])
        sql += '\' AND ini_line=\'' + str(values[1]) + '\';'
        res = self.__select(sql)
        if res : return res[0][0]
        return None

    def updateEndLine(self, values) :
        """Update end_line field of a given symbol"""
        sql = "UPDATE symbol SET\n"
        sql += "\tend_line='" + str(values[0]) + "'\n"
        sql += "WHERE id_file='" + str(values[1])
        sql += "' AND ini_line='" + str(values[2]) + "';"
        return self.__save(sql)

    def updateSymbol(self, values) :
        """Update a symbol"""
        sql = "UPDATE " + values[0] + " SET\n\t"
        sql += (',\n\t'.join(['=\''.join(x) + "'" for x in values[1]]))
        sql += "\nWHERE id_symbol = "
        sql += "(SELECT id_symbol FROM symbol "
        sql += "WHERE id_file = '" + str(values[2]) + "' "
        sql += "AND ini_line = '" + str(values[3]) + "');"
        return self.__save(sql)

    def getGlobalSymbols(self, values) :
        """Return all non-Class symbols"""
        res = []
        name = []

        for x in self.__getSymbols(values) :
            x = (self.__getGlobalSymbol([str(x[0]), values[2]]))
            if x[7] not in name :
                res.append(x)
                name.append(x[7])
        return res

    def getClassSymbols(self, values) :
        """Return all Class symbols"""
        res = []
        name = []

        for x in self.__getSymbols(values) :
            x = (self.__getClassSymbol([str(x[0]), values[2], values[3]]))
            if x and x[8] not in name :
                name.append(x[8])
                res.append(x)
        return res

    def close(self):
        """Close database connection"""
        self.DB_CURS.close()

    def reset(self) :
        """Normalize Insert and Update query executions"""
        try:
            self.DB_CURS.execute('DELETE FROM file')
            self.DB_CONN.commit()
        except :
            LOG('Issue while deleting data in db.')
            LOG(sql)
            return False
        return True
