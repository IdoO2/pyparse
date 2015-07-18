#! /usr/bin/env python3
#! -*- coding: utf8 -*-
# Author: Cyril RICHARD


"""
This file provides a CodeLine object used as a first level analyzer.
It works on the lowest level of logic in a Python file, an instruction.
This result is then used when the file is scanned for delimiting each context.
"""

import re
from python_common import *
from pprint import pprint


class CodeLine(object) :
    """Class that represent a line of code and calculate it's type"""
    indent = 4 # defaut indentation size

    def __init__(self, nline, code, context) :
        """Initializes CodeLine attributes"""
        self.context = context      # id of a supperior symbol
        self.type    = None         # type of CodeLine
        self.nline   = nline        # number of line
        self.level   = self.__getLevel(code)   # calculate level according identation
        self.ccode   = self.__preProcess(code) # clean the code
        # self.inst  = self.__getInstruction() # when i will process ';'... not now !
        self.type    = self.__getType(self.ccode) # type calculate by analyze
        self.icode   = code         # store initial code

    def __getType(self, string) :
        """Calculates CodeLine type with regex"""
        if self.type :
            return self.type
        if not string :
            return SYM_NONE
#### END NON-SYMBOL
        if len(re.findall(RDIC['se_docs'], string)) == 2 :
            return SYM_DOCS_ONE
        if len(re.findall(RDIC['se_docs'], string)) == 1 :
            return SYM_DOCS_MUL
#### END DOCSTRING
        if 'def' in string and self.level == 0 and \
         re.findall(RDIC['se_ol'], string) :
            return SYM_FCT_ONE
        if 'def' in string and self.level == 0 :
            return SYM_FCT_MUL
#### END FUNCTION
        if 'def' in string and self.level == 1 and \
         re.findall(RDIC['se_cons'], string) and \
         re.findall(RDIC['se_ol'], string) :
            return SYM_CON_MET_ONE
        if 'def' in string and self.level == 1 and \
         re.findall(RDIC['se_cons'], string) :
            return SYM_CON_MET_MUL
        if 'def' in string and self.level == 1 and \
         re.findall(RDIC['se_priv_meth'], string) and \
         re.findall(RDIC['se_ol'], string) :
            return SYM_PRI_MET_ONE
        if 'def' in string and self.level == 1 and \
         re.findall(RDIC['se_priv_meth'], string) :
            return SYM_PRI_MET_MUL
        if 'def' in string and self.level == 1 and \
         re.findall(RDIC['se_ol'], string) :
            return SYM_PUB_MET_ONE
        if 'def' in string and self.level == 1 :
            return SYM_PUB_MET_MUL
#### END METHOD
        if 'import' in string :
            return SYM_IMPT
        if 'class' in string and self.level == 0 :
            return SYM_CLASS
        if not 'self' in string and '=' in \
         re.findall(RDIC['se_var'], string) and not self.context :
            return SYM_GLO_VAR
        if not 'self' in string and \
         re.findall(RDIC['se_var'], string) and self.context :
            return SYM_PRI_VAR
        if 'self.' in string and not re.findall(' *self.[^ (]*\(', string) :
            return SYM_ATTR_CLASS
#### END OTHER
        return SYM_CODE # basic line of code

    def __preProcess (self, string) :
        """Cleans code line's content for an easiest analyze"""
        if not string : # if no content, it's empty.
            self.type = SYM_EMPT
            return string

        string = re.sub(RDIC['se_ncmt'], '', string)

        if not string :
            self.type = SYM_COMT
            return string

        string = re.sub(RDIC['cl_idet'], ' ', string)
        string = (string if string[0] != ' ' else string[1:]) # if start with space, it's removed
        string = re.sub(RDIC['se_str'], '', string)

        return string

    # Not done yet !
    # def __getInstruction(self) :
    #     """"""
    #     inst = []
    #     print (self.code)
    #     return inst

    def __getLevel(self, string) :
        """Calculates level according whitespace number before first caracter.
        This number is divided by the tab size."""
        if not string : return 0
        if not string[0] == ' ' : return 0
        res = (len(re.match(RDIC['se_space'], string).group(0)))

        return int(res / CodeLine.indent)

    def show(self) :
        """Shows CodeLine attributes"""
        pprint (vars(self))

    def getVariable(self) :
        """Exposes crucial variable. Used when the code is scanned."""
        return self.type, self.level

### OBJECT TESTING
if __name__ == '__main__' :
    arr  = [""] + ["print(test) #this is a test"]
    arr += ["a = C ; B = D"] + ["    a = C ; B = D"]
    arr += ["test2 = 1 + 2 + 5 + 78"]
    arr += ['    def  :  __init__()']
    arr += ['    def  :  __test()']
    arr += ['    def  :  test()']
    arr += ['import test met']
    arr += ['self.test = ']
    arr += ['#self.test = ']
    arr += ["\"self.test =\""]
    arr += ['\'self.test =\'']
    arr += ['def main () : return test']
    arr += ['    def __init__(self, master=None):']
    arr += ['for x in z : print x']
    # arr += ['\'self.\'test =\'']
    # arr += ['"self.\"test ="']
    for x in arr :
        test = CodeLine(12, x, 0)
        test.show()

