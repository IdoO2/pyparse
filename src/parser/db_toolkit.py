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
    def __init__(self):
        '''
        - establish connection
        - assert params are correct
        - init query
        '''
        self.DB_CONN = sqlite3.connect(DB_SYMBOL)
        self.DB_CURS = self.DB_CONN.cursor()
        self.DB_CURS.execute('PRAGMA synchronous = OFF;')
        self.DB_CONN.commit()


    def addSymbol(self, values):
        '''
        - assert symbol info is ok
        - update query
        '''
        sql = 'INSERT INTO symbol ("id_file", "id_type", "ini_line") VALUES '
        sql += "('" + '\', \''.join(values) + "');"
        return self.__save(sql)


    def addFile(self, values):
        sql = 'INSERT INTO file ("fname", "fpath") VALUES '
        sql += "('" + '\', \''.join(values) + "');"
        return self.__save(sql)

    def getFileID(self, values):
        sql = 'SELECT id_file FROM file WHERE fname=\'' + str(values[0])
        sql += '\' AND fpath=\'' + str(values[1]) + '\';'
        res = self.__select(sql)
        if res : return res[0][0]
        return None

    def getSymbolID(self, values):
        sql = 'SELECT id_symbol FROM symbol WHERE id_file=\'' + str(values[0])
        sql += '\' AND ini_line=\'' + str(values[1]) + '\';'
        res = self.__select(sql)
        if res : return res[0][0]
        return None

    def updateEndLine(self, values) :
        sql = "UPDATE symbol SET\n"
        sql += "\tend_line='" + str(values[0]) + "'\n"
        sql += "WHERE id_file='" + str(values[1])
        sql += "' AND ini_line='" + str(values[2]) + "';"
        return self.__save(sql)

    def updateSymbol(self, values) :
        sql = "UPDATE " + values[0] + " SET\n\t"
        sql += (',\n\t'.join(['=\''.join(x) + "'" for x in values[1]]))
        sql += "\nWHERE id_symbol = "
        sql += "(SELECT id_symbol FROM symbol "
        sql += "WHERE id_file = '" + str(values[2]) + "' "
        sql += "AND ini_line = '" + str(values[3]) + "');"
        return self.__save(sql)

    def __save(self, sql):
        try:
            self.DB_CURS.execute(sql)
            self.DB_CONN.commit()
        except :
            LOG('Issue while inserting data in db.')
            LOG(sql)
            return False
        return True

    def __select(self, sql):
        try:
            self.DB_CURS.execute(sql)
        except :
            LOG('Issue while inserting data in db.')
            LOG(sql)
            return False
        return self.DB_CURS.fetchall()

    def close(self): self.DB_CURS.close()



if __name__ == '__main__':
    test = DBC()
    test.addFile(['edzed', './ezdzed'])
    test.DB_CONN.commit()

