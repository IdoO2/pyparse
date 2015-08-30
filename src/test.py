#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

from pprint import *
from parser.db_toolkit import DBC
from os import listdir
from parser.python_code_line import CodeLine
from parser.conf import TEST_DIRECTORY
from parser.python_file import PythonFile

if __name__ == '__main__':
    database = DBC()
    database.reset() # reset database by deleting all symbol
    # for f in listdir(TEST_DIRECTORY) :
    for f in ['db_toolkit.py'] :
        print (f)
        test = PythonFile()
        test.process(f, TEST_DIRECTORY)
        # print ('\n'.join(test.CCODE))
        for l in test.SCODE :
            if type(l) in [CodeLine] :
                # print (l.show())
                continue

            # print (l.show())
        # #     # print(l.stype)
        print()
        res = test.getSymbolTree()
        pprint (res)
        print()

