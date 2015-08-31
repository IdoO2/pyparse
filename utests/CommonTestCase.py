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
from src.parser.python_code_line import CodeLine
from src.parser.python_file import PythonFile
from src.parser.common import Symbol


class CommonTestCase(unittest.TestCase):
#### START SYMBOL
    def start(self) :
        dbc = DBC()
        dbc.reset()
        test = PythonFile()
        test.process('complex.py', TEST_DIRECTORY)

    def test_Symbol_load(self):
        self.start()
        symb = Symbol()
        symb.load([1, 1, 13, 5, 20])
        res = symb.symbRepr()
        self.assertEqual(res, ['1 5 [13]'])

    def test_Symbol_register(self) :
        self.start()
        symb = Symbol()
        symb.load([1, 1, 13, 5, 20])
        code_line = CodeLine(1, '', -1)
        res = symb.register('1', code_line)
        self.assertEqual(res, True)

    def test_Symbol_updateEline(self) :
        self.start()
        symb = Symbol()
        symb.load([1, 1, 13, 5, 20])
        code_line = CodeLine(1, '', -1)
        symb.register('1', code_line)
        symb.eline = CodeLine(1, '', -1)
        res = symb.updateEline()
        self.assertEqual(res, True)

    def test_Symbol_addCode(self) :
        self.start()
        symb = Symbol()
        symb.load([1, 1, 13, 5, 20])
        code_line = CodeLine(1, '', -1)
        symb.register('1', code_line)
        symb.addCode(CodeLine(2, '', -1))
        self.assertEqual(len(symb.code), 2)
#### END SYMBOL

#### START FILE
    def test_process(self) :
        dbc = DBC()
        dbc.reset()
        test = PythonFile()
        test.process('complex.py', TEST_DIRECTORY)
        res = [test.FNAME, test.FPATH, len(test.ICODE), len(test.SCODE), test.ID]
        arr = ['complex.py', '/home/tuxcy/src/pyparse/utests/file/', 10303, 79, 1]
        self.assertEqual(res, arr)
#### END FILE

if __name__ == '__main__':
    test = unittest.TestLoader().loadTestsFromTestCase(CommonTestCase)
    unittest.TextTestRunner(verbosity=2).run(test)