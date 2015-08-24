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

### SHORTCUT
LOG = lambda msg: sys.stderr.write(msg + "\n") # print log on stderr
DBG = pdb.set_trace                            # facility for calling the debugger

### CONSTANTES
TEST_DIRECTORY = '../test/'         # where some test file are store
DB_SYMBOL = 'parser/db/db-symbol'   # where database is store
DB_STRUCT = 'parser/db/struct.sql'  # where the data structure sql is stored
