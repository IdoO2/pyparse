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
        if self.getSymbolID([values[0], values[2]]) : return True
        sql = 'INSERT INTO symbol ("id_file", "id_type", "ini_line") VALUES '
        sql += "('" + '\', \''.join(values) + "');"
        return self.__save(sql)


    def addFile(self, values):
        if self.getFileID(values) : return True
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

    def __getSymbols(self, values) :
        sql = 'SELECT id_symbol FROM symbol WHERE id_type IN (' + str(values[0])
        sql += ') AND id_file=\'' + str(values[1]) + '\''
        sql += ' ORDER BY ini_line ASC;'
        return self.__select(sql)

    def __getGlobalSymbol(self, values) :
        sql1 = 'SELECT * FROM symbol WHERE id_symbol=\'' + str(values[0]) + '\';'
        sql2 = 'SELECT * FROM ' + str(values[1]) + ' WHERE id_symbol=\'' + str(values[0]) + '\';'
        tmp = list(self.__select(sql1)[0]) + list(self.__select(sql2)[0])
        return tmp

    def __getClassSymbol(self, values) :
        sql1 = 'SELECT * FROM symbol WHERE id_symbol=\'' + str(values[0]) + '\';'
        sql2 = 'SELECT * FROM ' + str(values[1]) + ' WHERE id_symbol=\'' + str(values[0]) + '\' '
        sql2 += 'AND id_class=\'' + str(values[2]) + '\';'
        res1 = self.__select(sql1)
        res2 = self.__select(sql2)
        if not (res1 and res2) : return []
        return list(res1[0]) + list(res2[0])


    def getGlobalSymbols(self, values) :
        res = []

        for x in self.__getSymbols(values) :
            x = (self.__getGlobalSymbol([str(x[0]), values[2]]))
            res.append(x)
        return res

    def getClassSymbols(self, values) :
        res = []

        for x in self.__getSymbols(values) :
            x = (self.__getClassSymbol([str(x[0]), values[2], values[3]]))
            res.append(x)
        return res




    # def getClassTypeSymbols(self, values) :
    #     res = []

    #     arr_attr = ['class_attr']
    #     arr_cons = ['constructor']
    #     arr_publ = ['method public']
    #     arr_priv = ['method private']

    #     class_attr = self.__getSymbols(['30', values[1]])
    #     class_cons = self.__getSymbols(['22,25', values[1]])
    #     class_publ = self.__getSymbols(['20,23', values[1]])
    #     class_priv = self.__getSymbols(['21,24', values[1]])
    #     # print (class_attr, class_cons, class_publ, class_priv)
    #     for x in self.__getSymbols(values) :
    #         id_class = x[0]
    #         cla_arr = self.__getSymbol([id_class, 'class'])
    #         for attr in class_attr :
    #             #attr = self.__getClassSymbol([attr[0], 'class_attr', id_class])
    #             arr_attr.append(self.__getClassSymbol([attr[0], 'class_attr', id_class]))
    #         for cons in class_cons :
    #             # print(self.__getClassSymbol([attr[0], 'method', id_class]))
    #             arr_cons.append(self.__getClassSymbol([cons[0], 'method', id_class]))
    #         for publ in class_publ :
    #             arr_publ.append(self.__getClassSymbol([publ[0], 'method', id_class]))
    #             # print(self.__getClassSymbol([attr[0], 'method', id_class]))
    #         for priv in class_priv :
    #             arr_priv.append(self.__getClassSymbol([priv[0], 'method', id_class]))
    #             # print(self.__getClassSymbol([attr[0], 'method', id_class]))
    #         # print(self.__getClassSymbol([,'class_attr',id_class]))
    #         cla_arr += [arr_attr] + [arr_cons] + [arr_publ] + [arr_priv]
    #         res.append(cla_arr)
    #     return res


    def close(self): self.DB_CURS.close()


if __name__ == '__main__':
    test = DBC()
    test.addFile(['edzed', './ezdzed'])
    test.DB_CONN.commit()

