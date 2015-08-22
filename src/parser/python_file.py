#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This File implements the specific code for handling a Python File.
PreProcess of a file and scanning structure are defined here.
"""

import pdb
import re
from .conf import *
from .common import *
from .python_type import *
from .python_code_line import CodeLine
from .python_common import *

class PythonFile(File) :

    """Specific code for handling a Python file"""

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
        self.IDENT = self.__setIndent(txt) # indentation size
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
        # self.IDENT = self.__setIndent() # indentation size
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
                    tmp.updateEline()
                    clas().addCode(l)
                    continue
    ####
                if clas(): # si il y a une classe on ajoute la ligne de code au reste de la classe
                    clas().addCode(l)
                else : add(l) #sinon on l'ajoute a la structure générale
    ####
            #gestion des erreurs
            except :
                print ('error:', typ, lvl, l.show())
                raise
                return res

        # on met à jour les dernières lignes
        for x in res :
            if type(x) in CLIST :
                x.updateEline()
        return res


    def getSymbolTree(self, start='', end=''): #start and end not use yet
        """ Return symbol tree for GUI"""
        req_global = [ #label, table name, code for querying symbol
            ['Import', 'import', "10"],
            ['Variable', 'variable', "11"],
            ['Fonction', 'function', "12,13"],
            ['Classes', 'class', "14"],
        ]
        req_class = [ #label, table name, code for querying class symbol
            ['Attribut', 'class_attr', "30"],
            ['Constructeur', 'method', '22,25'],
            ['Methode Publique', 'method', '20,23'],
            ['Methode Privé', 'method', '21,24']
        ]
        res = [] # result array

        for lib, tab, l in req_global :
            tmp_arr = [] #temporary array used for creating branch
            tmp_ins = None #use to store symbole instance
            if tab not in ['class'] : # if querying not a class
                arr = self.DBC.getGlobalSymbols([l, self.ID, tab])
                if not arr : continue
                for x in arr :
                    tmp_ins = CDIC[int(x[2])]() # initialize current object
                    tmp_ins.load(x) # load current object with data
                    tmp_arr.append(tmp_ins.symbRepr()) # append symbol representation in arr
                res.append([lib] + tmp_arr) # append type of symbol and linked array
                continue
            elif tab in ['class'] : # if querying a class
                arr = self.DBC.getGlobalSymbols([l, self.ID, tab]) #array storing class
                if not arr : continue
                for x in arr : #for each class
                    class_arr = [] #will store symbol define in a given class
                    id_class = x[0] # get the class id
                    tmp_ins_class = CDIC[int(x[2])]() #instanciation of a class
                    tmp_ins_class.load(x) #load class attribute with an array of data
                    for lib2, tab2, l2 in req_class : #for each class symbol (method, attribute etc...)
                        tmp_arr2 = [] # another temporary arr
                        for z in self.DBC.getClassSymbols([l2, self.ID, tab2, id_class]) :
                            tmp_ins = CDIC[int(z[2])]()
                            tmp_ins.load(z)
                            tmp_arr2.append(tmp_ins.symbRepr())
                        if not tmp_arr2 : continue
                        class_arr.append([lib2] + tmp_arr2) #adding a category of symbol to class array
                    tmp_arr += [[tmp_ins_class.symbRepr()] + class_arr] #adding class array to tmp_arr
                res.append([lib] + tmp_arr) #adding all classes to result
            if not arr : continue
        return res
