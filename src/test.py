#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

from parser.python_code_line import CodeLine
from parser.conf import TEST_DIRECTORY
from parser.python_file import PythonFile
from parser.db_toolkit import DBC

if __name__ == '__main__':
    for f in ['simple_oo.py', 'very_simple.py'] :
        db = DBC()
        print (f)
        fd = open(TEST_DIRECTORY + f, 'r')
        test = PythonFile(f, TEST_DIRECTORY)
        fd.close()
        for l in test.SCODE :
            if type(l) in [CodeLine] :
                continue
            # print (l.show())
            # l.show()
        # #     # print(l.stype)
        print()
        res = test.getSymbolTree()
        print (res)
        #for x in res : print(x)
        print()
