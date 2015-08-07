#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

from parser.conf import TEST_DIRECTORY
from parser.python_parser import PythonParser


if __name__ == '__main__':
    for f in ['simple_oo.py', 'very_simple.py'] :
        print (f)
        fd = open(TEST_DIRECTORY + f, 'r')
        test = PythonParser(f, TEST_DIRECTORY, fd.read(), 4)
        fd.close()
        for l in test.SCODE :
            # if type(l) in [Class] :
                # l.show()
            print (l)
            # l.show()
        # #     # print(l.stype)
        print()
