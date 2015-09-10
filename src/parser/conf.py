#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This file implements some constants providing facility for:
  . print on stderr log messages
  . call a debugger
  . access test directory, database, and database structure file
"""


import pdb
import sys
import os


### GETING PARENT DIRECTORY
PARENT_DIR = ''
for rep in os.getcwd().split(os.sep) :
    PARENT_DIR += rep + os.sep
    if rep == 'pyparse' : break

### SHORTCUT
LOG = lambda msg: sys.stderr.write(msg + "\n") # print log on stderr
DBG = pdb.set_trace                            # facility for calling the debugger

### CONSTANTES
DB_SYMBOL      = os.path.join(PARENT_DIR, 'src/parser/db/db-symbol')   # where database is store
DB_STRUCT      = os.path.join(PARENT_DIR, 'src/parser/db/struct.sql')  # where the data structure sql is stored
UNIT_DIRECTORY = os.path.join(PARENT_DIR, 'utests/')         # where unit test are stored
TEST_DIRECTORY = UNIT_DIRECTORY + 'file/'         # where some test file are store