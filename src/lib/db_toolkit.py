#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This File implements a database wrapper.
The aim of this wrapper is to normalize database operations.
"""

import sqlite3
from conf import *

def insert(dic, dbc, dbg=False) :
    """Insert takes dic['tab'] dic['col'] dic['val'] & db Cursor
    => return a Bool"""
    sql = "INSERT INTO " + dic['tab']
    sql += " (" + ', '.join(dic['col']) + ") "
    sql += "VALUES ('" + '\', \''.join(dic['val']) + "');"

    if dbg : print(sql)

    try:

        dbc.execute(sql)
    except :
        LOG('Issue while inserting data in db.')
        LOG(sql)
        dbc.close()
        return False
    dbc.close()
    return True

def select(dic, dbc, dbg=False) :
    """Select takes dic['tab'] dic['col'] dic['whr'] & db Cursor
    => return an array """
    sql = "SELECT " + ' '.join(dic['col'])
    sql += " FROM " + dic['tab']
    sql += " WHERE " + dic['whr']

    if dbg : print(sql)

    dbc.execute(sql)
    res = dbc.fetchall()

    dbc.close()
    return res

def update(dic, dbc, dbg=False) :
    """Update takes dic['tab'] dic['set'] dic['whr'] & db Cursor
    => return a Bool"""
    sql = "UPDATE " + dic['tab'] + "\nSET\n"
    sql += ',\n'.join(['\t' + '=\''.join(x) + '\'' for x in dic['set']])
    sql += "\nWHERE " + dic['whr']

    if dbg : print(sql)

    try:
        dbc.execute(sql)
    except :
        LOG('Issue while inserting data in db.')
        LOG(sql)
        dbc.close()
        return False

    dbc.close()
    return True

def delete(dic, dbc, dbg=False) :
    """Delete takes dic['tab'] dic['whr'] & db Cursor
    => return a Bool"""
    sql = "DELETE FROM " + dic['tab']
    sql += " WHERE " + dic['whr']

    if dbg : print(sql)

    try:
        dbc.execute(sql)
    except :
        LOG('Issue while deleting data in db.')
        LOG(sql)
        dbc.close()
        return False

    dbc.close()
    return True
