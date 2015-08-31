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


class PythonCodeLineTestCase(unittest.TestCase):

    def test_nonSymbol(self):
        res = []
        test = [
          CodeLine(1, '# je suis un commentaire', -1),
          CodeLine(1, 'if test == True:', -1),
          CodeLine(1, 'for x in test :', -1),
          CodeLine(1, '"""je suis un commentaire """', -1),
          CodeLine(1, '#!/usr/bin/env python3', -1),
          CodeLine(1, 'test = 5', 2)
        ]
        for line in test :
            res.append(line.type < 10)

        self.assertEqual(res, [True] * len(test))

    def test_variable(self):
        res = []
        test = [
          CodeLine(1, 'a = c', 0),
          CodeLine(1, '# a = c', 0),
          CodeLine(1, 'a = c', 2),
          CodeLine(1, '"a = c"', 0),
        ]
        for line in test :
            res.append(line.type == 11)

        self.assertEqual(res, [True, False, False, False])

    def test_function(self):
        res = []
        test = [
          CodeLine(1, 'def test () :', 0),
          CodeLine(1, '# def tesst () :', 0),
          CodeLine(1, 'def test () :', 2),
          CodeLine(1, '"def test () :"', 0),
        ]
        for line in test :
            res.append(line.type in [12, 13])

        self.assertEqual(res, [True, False, True, False])

    def test_import(self):
        res = []
        test = [
          CodeLine(1, 'import re', 0),
          CodeLine(1, 'import os as OS', 0),
          CodeLine(1, 'import re', 2),
          CodeLine(1, 'from .python_type import *', 0),
        ]
        for line in test :
            res.append(line.type in [10])

        self.assertEqual(res, [True, True, True, True])


    def test_class(self):
        res = []
        test = [
          CodeLine(1, 'class test : ', 0),
          CodeLine(1, 'class test (object) :', 0),
          CodeLine(1, 'class test (object, server) :', 0),
          CodeLine(1, 'class test :', 2),
          CodeLine(1, '"class test :"', 0),
        ]
        for line in test :
            res.append(line.type in [14])

        self.assertEqual(res, [True, True, True, True, False])

    def test_method(self):
        res = []
        test = [
          CodeLine(1, 'def test (self) :', 0),
          CodeLine(1, '# def tesst () :', 1),
          CodeLine(1, '    def __test (self) :', 1),
          CodeLine(1, '    def test (self) :', 1),
          CodeLine(1, '    def test (self, arg1) :', 1),
          CodeLine(1, '    def __init__ (self) :', 1),
          CodeLine(1, '    "def test () :"', 0),
        ]
        for line in test :
            res.append(line.type < 30 and line.type >= 20)

        self.assertEqual(res, [False, False, True, True, True, True, False])


    def test_classAttribute(self):
        res = []
        test = [
          CodeLine(1, 'self.attribut = c', 1),
          CodeLine(1, '# a = c', 1),
          CodeLine(1, '    self.attribut = c', 1),
          CodeLine(1, 'self.attribut = c', -1),
          CodeLine(1, '"self.attribut = c"', 0)
        ]
        for line in test :
            res.append(line.type == 30)

        self.assertEqual(res, [True, False, True, True, False])

if __name__ == '__main__':
    test = unittest.TestLoader().loadTestsFromTestCase(PythonCodeLineTestCase)
    unittest.TextTestRunner(verbosity=2).run(test)