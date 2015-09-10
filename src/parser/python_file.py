#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This File implements the specific code for handling a Python File.
PreProcess of a file and scanning structure are defined here.
"""
import re
from .conf import *
from .common import *
from .python_type import *
from .python_code_line import CodeLine
from .python_common import *

class PythonFile(File) :

    """Specific code for handling a Python file"""

    __tree = None

    ### CONSTRUCTOR

    def __init__(self) :
        """Adds missing attributes used in a Python file"""
        super().__init__()
        self.IDENT = 0      # indentation size
        self.CCODE = [] # clean code results of preprocess
        self.SCODE = [] # scan file content and returns code structure

    ### PRIVATE METHOD

    def __preProcess(self, txt) :
        """Preprocessing a file:
            . tabulations are changed in whitespaces
            . multiline are changed in one line"""
        txt = self.__comment(txt)
        self.IDENT = self.__setIndent(txt + '\n') # indentation size
        arr_txt = txt.replace('\t', ' ' * self.IDENT).split(self.LINE_END)
        i = 0

        while (i < len(arr_txt)) :
            offset, lines = self.__multiLine(arr_txt[i:], "", 0, 0)
            arr_txt[i] = lines[0]
            for x in range(1, offset+1) :
                arr_txt[i+x] = ''
            i += 1
        return arr_txt

    def __multiLine(self, data, res, count, itir) :
        open_parenth = count + data[0].count('(')
        clos_parenth = data[0].count(')')
        if data[0] == '' :
            return itir, [res] + itir * ['']
        elif data[0][-1] == '\\' :
            return self.__multiLine(data[1:], res + data[0][:-1], open_parenth - clos_parenth, itir + 1)
        elif open_parenth - clos_parenth == 0 :
            return itir, [res + data[0]] + itir * ['']
        else :
            return self.__multiLine(data[1:], res + data[0] + " ", open_parenth - clos_parenth, itir + 1)

    def __comment(self, txt) :
        res = re.findall('\'\'\'[^\']+\'\'\'|"""[^\"]+"""', txt)
        res += re.findall('#.+', txt)
        for x in res :
            offset = x.count('\n')
            txt = txt.replace(x, '\n' * offset)
        return txt

    def __setIndent(self, txt) :
        res = []

        arr = txt.split('\n')
        i = 0
        while (i < len(arr)) :
            if re.findall('def |if |for |class ', arr[i]) and \
             ' ' in arr[i+1] and ':' in arr[i] :
                res.append(len(re.findall('^ *', arr[i+1])[0]) - len(re.findall('^ *', arr[i])[0]))
            i += 1
        for x in res :
            if x != 0 : return x
        return 4

    ### PUBLIC METHOD

    def process(self, fname, fpath) :
        """Adds missing attributes used in a Python file"""
        super().process(fname, fpath)
        self.CCODE = self.__preProcess(self.ICODE) # clean code results of preprocess
        self.SCODE = self.scanCode(self.CCODE) # scan file content and returns code structure


    def scanCode(self, ccode) :
        """Scan a file code and return an array reprensting the file structure"""
        CodeLine.indent = self.IDENT # set ident for codeline

        res = []
        fifo = [None] # stores the context (ie the current symbol). first is global
        sym = lambda: fifo[-1] # current symbol
        clas = lambda: fifo[1] if len(fifo) > 1 and type(fifo[1]) is Class else None #return current class
        add = lambda l: sym().addCode(l) if type(sym()) in CLIST else res.append(l) #add a codeline in a symbol or directly
        cont = lambda: sym().id if type(sym()) in CLIST else 0 #return current context object
        styp = lambda: sym().stype if type(sym()) in CLIST else None #return symbol type of context symbol

        i = 0

        while i < len(ccode) :

            try :
                l = CodeLine(i+1, ccode[i], cont())
                i += 1


                typ, lvl = l.getVariable() # get type and level of codeline
    #### END INIT
                if styp() in [SYM_CLASS, SYM_FCT_MUL] + SYM_MET_MUL and lvl == 0 \
                 and typ not in SYM_NEG : # fin d'un symbol multiline avec une ligne au niveau 0
                    sym().updateEline() #on met à jour la dernière ligne
                    l.context = 0 #on reset le contexte de la ligne de code
                    fifo = [None] #on vide la liste contenant le context actuel
                if styp() in SYM_MET_MUL and lvl == 1 \
                 and typ not in SYM_NEG : # fin d'un symbol multiline avec une ligne au niveau 1 ne concerne que les méthodes
                    sym().updateEline() #on met à jour la dernière ligne
                    fifo.pop() # on enlève le contexte actuelle
                    l.context = cont() #on ajoute le nouveau contexte à la ligne de code
    ####
                if typ in [SYM_CLASS, SYM_FCT_MUL] :
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l)
                    fifo.append(tmp)
                    l.context = cont()
                    res.append(tmp)
                    continue
                if typ in SYM_MET_MUL :
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l, cont())
                    fifo.append(tmp)
                    l.context = cont()
                    clas().addCode(l)
                    continue
    ####
                if typ in SYM_ONE and typ not in SYM_MET_ONE :
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l)
                    res.append(tmp)
                    l.context = res[-1].id
                    tmp.updateEline()
                    continue
                if typ in SYM_ONE and typ in SYM_MET_ONE :
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l, cont())
                    l.context = tmp.id
                    clas().addCode(l)
                    tmp.updateEline()
                    continue
    ####
                if typ == SYM_GLO_VAR : #si c'est une variable global on l'ajoute à la structure du code
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l)
                    res.append(tmp)
                    continue
                if typ == SYM_ATTR_CLASS : # si c'est un attribut de classe on l'ajoute au code de la classe
                    tmp = CDIC[typ]()
                    tmp.register(self.ID, l, clas().id)
                    l.context = tmp.id
                    tmp.updateEline()
                    clas().addCode(l)
                    continue
    ####
                if clas(): # si il y a une classe on ajoute la ligne de code au reste de la classe
                    clas().addCode(l)
                else : add(l) #sinon on l'ajoute a la structure générale
    ####
            #gestion des erreurs
            except Exception:
                raise RuntimeError('Error while parsing file')

        # on met à jour les dernières lignes
        for x in res :
            if type(x) in CLIST :
                x.updateEline()
        return res

    def __buildTree(self, symbols):
        """ Create a tree structure from the flat db data

            TODO: handle more than two levels (recurse)
        """
        symb_map = {}
        tmp_tree = {}
        name = []
        i = 0
        # symbol entries are: 0-id, 1-first line number, 2-type, 3-visibility, 4-name, 5-args, 6-parent
        if not symbols : return {}

        while i < len(symbols) :
            s = symbols[i]
            symb_map.update({s[0]: i})
            if s[6] is None and str(s[4]) + str(s[6]) not in name :
                tmp_tree[i] = [s, {}]
                name.append(str(s[4]) + str(s[6]))
            elif s[6] in symb_map and str(s[4]) + str(s[6]) not in name :
                tmp_tree[symb_map[s[6]]][1][i] = [s, {}]
                name.append(str(s[4]) + str(s[6]))
            i += 1

        return tmp_tree

    def __translateTree(self, tmp_tree):
        """ Convert transitional tree structure to public standards

            TODO: handle more than two levels (recurse)
        """
        getName = lambda x : x[4]
        getType = lambda x : x[2]
        getVisi = lambda x : x[3]
        getSign = lambda x : x[5].split('|')
        getLine = lambda x : x[1]

        tree = []
        level = []

        for l in sorted(tmp_tree.keys()):
            symbol = tmp_tree[l][0]

            if not tmp_tree[l][1]:
                if getType(symbol) in ['function', 'import'] :
                    tree.append(
                        (getName(symbol), {'type': getType(symbol), 'signature': getSign(symbol), 'line': getLine(symbol)})
                    )
                else :
                    tree.append(
                        (getName(symbol), {'type': getType(symbol), 'line': getLine(symbol)})
                    )
            else:
                level = [(getName(symbol), {'type': symbol[2], 'line': symbol[1]})]
                for k in sorted(tmp_tree[l][1].keys()) :
                    sub_symbol = tmp_tree[l][1][k][0]

                    if getType(sub_symbol) in ['method', 'constructor'] :
                        level.append(
                            (getName(sub_symbol), {
                                'type': getType(sub_symbol),
                                'visibility': getVisi(sub_symbol),
                                'signature': getSign(sub_symbol),
                                'line': getLine(sub_symbol)
                            })
                        )
                    else :
                        level.append(
                            (getName(sub_symbol), {
                                'type': getType(sub_symbol),
                                'visibility': getVisi(sub_symbol),
                                'line': getLine(sub_symbol)
                            })
                        )

                tree.append(level)

        return tree


    def getSymbolTree(self):
        """ Return symbol tree for GUI"""

        if self.__tree:
            return self.__tree

        # Get all symbols for file
        symbols = self.DBC.getFileSymbols(self.ID)

        # Populate data structure with db symbols
        symbol_tree = self.__buildTree(symbols)
        self.__tree = self.__translateTree(symbol_tree)

        return self.__tree if self.__tree else []
