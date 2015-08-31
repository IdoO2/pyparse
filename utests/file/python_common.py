#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This file implements some constants providing facilities for:
	. access the symbol type that can be identified by the analyzer
	. instantiate the proper object according the symbol type
	. test if an object is a Python type
	. test if a type is parts of a meta-type
	. access to regex used during the process
"""

import re
from .python_type import *

### SYMBOL CONSTANT -- use for typing symbol

# [0-9] UNTRACK SYMBOL
SYM_NONE        = 0 # DEFAULT VALUE
SYM_EMPT        = 1 # EMPTY LINE
SYM_CODE        = 2 # BASIC CODE LINE
SYM_COMT        = 3 # COMMENT ONLY
SYM_PRI_VAR     = 4 # PRIVATE VARIABLE

# [10-19] SYMBOL DEFINE IN GLOBAL CONTEXT
SYM_IMPT        = 10 # IMPORT
SYM_GLO_VAR     = 11 # GLOBAL VARIABLE
SYM_FCT_ONE     = 12 # ONE_LINE FUNCTION
SYM_FCT_MUL     = 13 # MULTI_LINE FUNCTION
SYM_CLASS       = 14 # CLASS DECLARATION

# [20-29] CLASS METHOD SUPPORT
SYM_PUB_MET_ONE = 20 # ONE_LINE PUBLIC METHOD
SYM_PRI_MET_ONE = 21 # ONE_LINE PRIVATE METHOD
SYM_CON_MET_ONE = 22 # ONE_LINE CONSTRUCTOR METHOD
SYM_PUB_MET_MUL = 23 # MULTI_LINE PUBLIC METHOD
SYM_PRI_MET_MUL = 24 # MULTI_LINE PRIVATE METHOD
SYM_CON_MET_MUL = 25 # MULTI_LINE CONSTRUCTOR METHOD

# [30-39] CLASS ATTRIBUTE SUPPORT
SYM_ATTR_CLASS  = 30 # CLASS ATTRIBUTE USING 'self'

# [40-49] DOCSTRING SUPPORT
SYM_DOCS_ONE    = 40 # ONE_LINE DOCSTRING
SYM_DOCS_MUL    = 41 # MULTI_LINE DOCSTRING


### CLASS DIC -- facility for Symbol instantiation
  # use Symbol Constant as Hash key
CDIC = {
  SYM_IMPT: Import,
  SYM_GLO_VAR: Variable,
  SYM_FCT_ONE: Function,
  SYM_FCT_MUL: Function,
  SYM_CLASS: Class,
  SYM_ATTR_CLASS: ClassAttribute,
  SYM_PUB_MET_ONE: Method,
  SYM_PRI_MET_ONE: Method,
  SYM_CON_MET_ONE: Method,
  SYM_PUB_MET_MUL: Method,
  SYM_PRI_MET_MUL: Method,
  SYM_CON_MET_MUL: Method,
}

### CLASS LIST -- facility for class type testing
CLIST = [
  Import,
  Variable,
  Function,
  Class,
  ClassAttribute,
  Method,
]

### CONSTANT LIST -- facility for constant testing
  # symbol that don't count:
SYM_NEG = [SYM_EMPT, SYM_COMT, SYM_NONE]
  # multiline method:
SYM_MET_MUL = [SYM_CON_MET_MUL, SYM_PRI_MET_MUL, SYM_PUB_MET_MUL]
  # oneline method:
SYM_MET_ONE = [SYM_PUB_MET_ONE, SYM_PRI_MET_ONE, SYM_CON_MET_ONE]
  # online symbol:
SYM_ONE = [SYM_IMPT, SYM_FCT_ONE, SYM_GLO_VAR, SYM_DOCS_ONE] + SYM_MET_ONE
  # anyline method:
SYM_MET = SYM_MET_MUL + SYM_MET_ONE
  # multiline symbol:
SYM_MUL = [SYM_CLASS, SYM_FCT_MUL, SYM_DOCS_MUL] + SYM_MET_MUL


