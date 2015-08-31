#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

import sys
import os
sys.path.append(sys.path.append(\
  os.sep.join(os.getcwd().split(os.sep)[:os.getcwd().split(os.sep).index('pyparse')]+['pyparse' + os.sep]))) #fixing python path


import unittest
from src.parser.conf import *
from pprint import *

### module that need testing
from src.parser.db_toolkit import DBC
from src.parser.python_file import PythonFile


class DBToolKitTestCase(unittest.TestCase):

    def clean_database (self) :
        dbc = DBC()
        dbc.reset()
        test = PythonFile()
        test.process('complex.py', TEST_DIRECTORY)

    def test_addSymbol(self):
        self.clean_database()
        dbc = DBC()
        res = dbc.addSymbol(['1', '13', '150'])
        self.assertEqual(res, True)

    def test_addFile(self) :
        self.clean_database()
        dbc = DBC()
        dbc = DBC()
        res = dbc.addFile(['test_fname', 'test_path'])
        self.assertEqual(res, True)

    def test_getFileID(self) :
        self.clean_database()
        dbc = DBC()
        res = dbc.getFileID(['complex.py', TEST_DIRECTORY])
        self.assertEqual(res, True)

    def test_getSymbolID(self) :
        self.clean_database()
        dbc = DBC()
        res = dbc.getSymbolID([1, 35])
        self.assertEqual(res, 12)

    def test_updateEndLine(self) :
        self.clean_database()
        dbc = DBC()
        res = dbc.updateEndLine([105, 1, 105])
        self.assertEqual(res, True)

    def test_updateSymbol(self) :
        self.clean_database()
        dbc = DBC()
        res = dbc.updateSymbol(['method', [['name', 'showSymbol'],\
         ['args', 'self|type'], ['id_class', '34']], 1, 241])
        self.assertEqual(res, True)

    def test_getFileSymbols(self) :
        self.clean_database()
        dbc = DBC()
        res = dbc.getFileSymbols(1)
        self.assertEqual(len(res), 57)

    def test_reset(self):
        self.clean_database()
        dbc = DBC()
        res = dbc.reset()
        self.assertEqual(res, True)

if __name__ == '__main__':
    test = unittest.TestLoader().loadTestsFromTestCase(DBToolKitTestCase)
    unittest.TextTestRunner(verbosity=2).run(test)