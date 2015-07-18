#! /usr/bin/env python
#! -*- coding: utf8 -*-
# Source: http://rosettacode.org/wiki/99_Bottles_of_Beer/Python
 
def sing(b, end):
    print(b or 'No more','bottle'+('s' if b-1 else ''), end)
    print(b or 'No more','bottle'+('s' if b-1 else ''), end)
    print(b or 'No more','bottle'+('s' if b-1 else ''), end)
    print(b or 'No more','bottle'+('s' if b-1 else ''), end)
 
for i in range(99, 0, -1):
    sing(i, 'of beer on the wall,')
    sing(i, 'of beer,')
    print('Take one down, pass it around,')
    sing(i-1, 'of beer on the wall.\n')
	a = test

a = test
