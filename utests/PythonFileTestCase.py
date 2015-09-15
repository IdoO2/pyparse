#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

import sys
import os
sys.path.append(sys.path.append(\
  os.sep.join(os.getcwd().split(os.sep)[:os.getcwd().split(os.sep).index('pyparse')]+['pyparse' + os.sep]))) #fixing python path

import unittest
from pprint import *

from src.parser.conf import *
### module that need testing
from src.parser.db_toolkit import DBC
from src.parser.python_file import PythonFile
from src.parser.python_type import *


class PythonFileTestCase(unittest.TestCase):

    def test_global(self) :
        dbc = DBC()
        dbc.reset()

        res = []
        tests = os.listdir(TEST_DIRECTORY)
        for f in tests :
            test = PythonFile()
            test.process(f, TEST_DIRECTORY)
            tree = pformat(test.getSymbolTree())

            fd_org = open(UNIT_DIRECTORY + 'result/' + f[:-3] + '_res', 'r')
            org_tree = fd_org.read()
            fd_org.close()
            res.append(org_tree == tree)
        self.assertEqual(res, [True] * len(tests))

if __name__ == '__main__':
    test = unittest.TestLoader().loadTestsFromTestCase(PythonFileTestCase)
    unittest.TextTestRunner(verbosity=2).run(test)
