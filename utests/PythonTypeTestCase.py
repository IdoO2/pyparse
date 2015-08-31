#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

import sys
import os
sys.path.append(sys.path.append(\
  os.sep.join(os.getcwd().split(os.sep)[:os.getcwd().split(os.sep).index('pyparse')]+['pyparse' + os.sep]))) #fixing python path


import unittest

### module that need testing
from src.parser.python_code_line import CodeLine
from src.parser.python_type import *

class PythonTypeTestCase(unittest.TestCase):

    def test_variable(self):
        res = []
        tests = [
          CodeLine(1, 'a = c', 0),
          CodeLine(1, '      a = c', 0)
        ]
        for cline in tests :
            symb = Variable()
            symb.register(1, cline)
            res.append(symb.name == 'a')

        self.assertEqual(res, [True] * len(tests))

    def test_function(self):
        res = []
        tests = [
          CodeLine(1, 'def test () :', 0),
          CodeLine(1, 'def test (a,b,c) :', 2),
          CodeLine(1, 'def test (a, b, c) :', 0),
          CodeLine(1, 'def test (a ,b ,c ) :', 2),
        ]
        for cline in tests :
            symb = Function()
            symb.register(1, cline)
            res.append('test' in symb.name and symb.args == ['a', 'b', 'c'] \
             or symb.args == [''])

        self.assertEqual(res, [True] * len(tests))

    def test_import(self):
        res = []
        tests = [
          CodeLine(1, 'import re, os', 0),
          CodeLine(1, 'import re as OS', 0),
          CodeLine(1, 'import re', 2),
          CodeLine(1, 'from re import *', 0),
        ]
        for cline in tests :
            symb = Import()
            symb.register(1, cline)
            res.append(symb.module in [['re'], ['re','os']] \
             and symb.alias in ['OS', ''] \
             and symb.element in [[], ['*']])

        self.assertEqual(res, [True] * len(tests))

    def test_class(self):
        res = []
        tests = [
          CodeLine(1, 'class test : ', 0),
          CodeLine(1, 'class test (object) :', 0),
          CodeLine(1, 'class test(object) :', 0),
          CodeLine(1, 'class test (object, server) :', 0),
          CodeLine(1, 'class test :', 2),
        ]
        for cline in tests :
            symb = Class()
            symb.register(1, cline)
            res.append(symb.name == 'test'\
             and symb.lega in [[''], ['object', 'server'], ['object']])

        self.assertEqual(res, [True] * len(tests))

    def test_method(self):
        res = []
        tests = [
          CodeLine(1, '    def __test (self, arg) :', 1),
          CodeLine(1, '    def test (self) :', 1),
          CodeLine(1, '    def test (self,arg) :', 1),
          CodeLine(1, '    def __init__ (self) :', 1),
        ]
        for cline in tests :
            symb = Method()
            symb.register(1, cline, 1)
            res.append(symb.name in ['test', '__test', '__init__'] \
             and symb.args in [['self'], ['self', 'arg']])

        self.assertEqual(res, [True] * len(tests))

    def test_classAttribute(self):
        res = []
        tests = [
          CodeLine(1, 'self.attribut = c', 1),
          CodeLine(1, '    self.attribut = c', 1),
          CodeLine(1, 'self.attribut = c', 1),
        ]
        for cline in tests :
            symb = ClassAttribute()
            symb.register(1, cline, 1)
            res.append(symb.name == 'attribut' \
             and symb.idclass == 1)

        self.assertEqual(res, [True] * len(tests))

if __name__ == '__main__':
    test = unittest.TestLoader().loadTestsFromTestCase(PythonTypeTestCase)
    unittest.TextTestRunner(verbosity=2).run(test)