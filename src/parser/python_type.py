#!/usr/bin/env python3
#!-*- coding: utf8 -*-
# Author: Cyril RICHARD

"""
This file contains each specialized Python symbol that can be initialized.
All this object are child with Symbol.
The 'analyze' method contains the third level of analyze: recuperation of
the missings Symbol attributes.
"""

from .common import Symbol
import re

### REGEX -- centralize regex used in this file
RDIC = {
  'se_docs' : re.compile('"""|\'\'\''), #identifie les commentaires multilines / doctring
  'se_cons' : re.compile(' *def *__init__'), #identifie un constucteur
  'se_priv_meth' : re.compile(' *def *__'), #identifie une methode privé
  'se_space': re.compile('^( +)'), #identifie la première série d'espace d'un mot
  'se_ncmt': re.compile('(#.*)'), #renvoie tout ce qui n'est pas un commentaire
  'se_str': re.compile("\"([^\"]*)\"|\'([^\']*)\'"), #identifie une chaine de caractère
  'se_meth': re.compile('def _{2}'), #vérifie si une méthode est privé
  'se_var': re.compile('==|<=|!=|>=|='), #regex utilisé pour trouver une variable
  'se_ol': re.compile(': *(\w)'), #cherche un caractère après ':', définit si un symbol est oneline

  'import_from': re.compile('from ([^ ]+) import *(\*|.+)'), #renvoie le module et ses éléments
  'import': re.compile('import ([^ ]+)'), #renvoie les modules
  'class': re.compile('class ([^\s\(:]*)[\( )]*([^):]*)'), #renvoie le nom d'une classe
  'class_attr': re.compile('self.([^ \(\)=]+) '), #renvoie le nom d'un attribut d'instance
  'fonction': re.compile('^def (.+(?=[(])).([^)]*)'), # #renvoie le nom d'une fonction et ses arguments
  'method': re.compile('def ([^\( ]+)[\( ]*([^\):]*)'), #identifie une méthode
  'variable': re.compile('([^[ =]+)'), #sélectionne le nom d'une variable
  'cl_comm': re.compile('\s,|,\s'), #selectionne les arguments quelque soit leur présentation
  'cl_idet': re.compile('[\t ]+'), #sélectionne l'indentation
  'syntaxe': re.compile('[\+\.;,\(\)\[\]{]') #nettoie une ligne de la syntaxe pour optimiser son parcours
}

class Import(Symbol) :
    """Python Import can be defined by :
        . a list of module
        . a list of element
        . an alias
    """
    def __init__(self) :
        """Initialize Import global & specific attributes"""
        super().__init__()
        self.module  = []   # liste de module
        self.element = []   # liste d'élément
        self.alias   = ''   # alias

    def register(self, id_file, code) :
        """Register an Import symbol in database"""
        super().register(id_file, code)
        self.analyze()
        self.update()

    def load(self, data) :
        """"Load instance attributes from an array of values"""
        super().load(data)
        self.module = data[7]
        self.element = data[8]
        self.alis = data[9]

    def analyze(self) :
        """Find attribute value in declaration line"""
        code = self.code[0].ccode
        code = re.sub(RDIC['cl_comm'], ',', code)
        if 'from' in code.split() : # ex: from re import findall
            imp = RDIC['import_from'].match(code)
            self.module = [imp.group(1)]
            ele = re.sub('\(|\)', '', imp.group(2))
            self.element = ele.split(',')
        else : # ex: import re
            imp = RDIC['import'].match(code)
            self.module = imp.group(1).split(',')
        if 'as' in code.split() : # ex: import re as R
            self.alias = re.findall('as (.+)', code)[0]

    def update(self) :
        """Register specific symbol attributes in database"""
        values = ['import', '', self.id_file, self.iline]
        values[1] = [['module', '|'.join(self.module)], \
         ['element', '|'.join(self.element)], ['alias', self.alias]]
        return self.DBC.updateSymbol(values)

    def symbRepr(self) :
        """return an array representative of current Symbol"""
        return [str(self.module) + ' [' + str(self.iline) + ']'] + self.element.split('|')

class Variable(Symbol) :
    """Python Variable can be defined by :
        . a name
    """
    def __init__(self) :
        """Initialize Variable global & specific attributes"""
        super().__init__()
        self.name = ''      # variable name

    def register(self, id_file, code) :
        """Register a Variable symbol in database"""
        super().register(id_file, code)
        self.analyze()
        self.update()

    def load(self, data) :
        """"Load instance attributes from an array of values"""
        super().load(data)
        self.name = data[7]

    def analyze(self) :
        """Find variable name"""
        code = self.code[0].ccode
        self.name = RDIC['variable'].match(code).group(1)

    def update(self) :
        """Register specific symbol attributes in database"""
        values = ['variable', '', self.id_file, self.iline]
        values[1] = [['name', self.name]]
        return self.DBC.updateSymbol(values)

    def symbRepr(self) :
        """return a string representative of current Symbol"""
        return str(self.name) + ' [' + str(self.iline) + ']'

class Function(Symbol) :
    """Python Function can be defined by :
        . a name
        . an argument list
    """
    def __init__(self) :
        """Initialize Function global & specific attributes"""
        super().__init__()
        self.name = ''      # function name
        self.args = []      # function argument list

    def register(self, id_file, code) :
        """Register a Function symbol in database"""
        super().register(id_file, code)
        self.analyze()
        self.update()

    def load(self, data) :
        """Load instance attributes from an array of values"""
        super().load(data)
        self.name = data[7]
        self.args = data[8]

    def analyze(self) :
        """Find Function name and arguments"""
        code = self.code[0].ccode
        head = RDIC['fonction'].match(code)
        self.name = head.group(1)
        self.args = head.group(2).replace(' ', '').split(',')

    def update(self) :
        """Register specific symbol attributes in database"""
        values = ['function', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['args', '|'.join(self.args)]]
        return self.DBC.updateSymbol(values)

    def symbRepr(self) :
        """return a string representative of current Symbol"""
        return str(self.name) + ' [' + str(self.iline) + ']'

class Class(Symbol) :
    """Python Class can be defined by :
        . a name
        . a list of parent class
    """
    def __init__(self) :
        """Initialize Class global & specific attributes"""
        super().__init__()
        self.name = ''
        self.lega = []

    def register(self, id_file, code) :
        """Register a Class symbol in database"""
        super().register(id_file, code)
        self.analyze()
        self.update()

    def load(self, data) :
        """Load instance attributes from an array of values"""
        super().load(data)
        self.name = data[7]
        self.lega = data[8]

    def analyze(self) :
        """Find Class name and legacy"""
        code = self.code[0].ccode
        head = RDIC['class'].match(code)
        self.name = head.group(1)
        self.lega = head.group(2).replace(' ', '').split(',')

    def update(self) :
        """Register specific symbol attributes in database"""
        values = ['class', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['legacy', '|'.join(self.lega)]]
        return self.DBC.updateSymbol(values)

    def symbRepr(self) :
        """return a string representative of current Symbol"""
        return str(self.name) + ' [' + str(self.iline) + ']'

    def show(self) :
        """Prints line-number and initial-code of each CodeLine stored in Symbol"""
        string = ''
        idclass = self.id if 'id' in vars(self) else None
        for x in self.code :
            string += x.show(idclass) + '\n'
        return string[:-1]

class ClassAttribute(Symbol) :
    """Python Class Attribute can be defined by :
        . a name
        . the class id linked to this attribute
    """
    def __init__(self) :
        """Initialize ClassAttribute global & specific attributes"""
        super().__init__()
        self.name = ''
        self.idclass = ''

    def register(self, id_file, code, idclass) :
        """Register a ClassAttribute symbol in database"""
        super().register(id_file, code)
        self.idclass = idclass
        self.analyze()
        self.update()

    def load(self, data) :
        """Load instance attributes from an array of values"""
        super().load(data)
        self.idclass = data[7]
        self.name = data[8]

    def analyze(self) :
        """Find ClassAttribute name"""
        code = self.code[0].ccode
        head = re.findall(RDIC['class_attr'], code)
        if head : self.name = head[0]

    def update(self) :
        """Register specific symbol attributes in database"""
        values = ['class_attr', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['id_class', str(self.idclass)]]
        return self.DBC.updateSymbol(values)

    def symbRepr(self) :
        """Return a string representative of current Symbol"""
        return str(self.name) + ' [' + str(self.iline) + ']'

    def show(self) :
        """Prints line-number and initial-code of each CodeLine stored in Symbol"""
        string = ''
        idclass = self.idclass if 'idclass' in vars(self) else None
        for x in self.code :
            string += x.show(idclass) + '\n'
        return string[:-1]

class Method(Symbol) :
    """Python Method can be defined by :
        . a name
        . a list of arguments
        . the class id linked to this attribute
    """
    def __init__(self) :
        """Initialize Method global & specific attributes"""
        super().__init__()
        self.name = ''
        self.args = []
        self.idclass = ''

    def register(self, id_file, code, idclass) :
        """Register a ClassAttribute symbol in database"""
        super().register(id_file, code)
        self.idclass = idclass
        self.analyze()
        self.update()

    def load(self, data) :
        """Load instance attributes from an array of values"""
        super().load(data)
        self.idclass = data[7]
        self.name = data[8]
        self.args = data[9]

    def analyze(self) :
        """Find Method name and arguments"""
        code = self.code[0].ccode
        head = RDIC['method'].match(code)
        self.name = head.group(1)
        self.args = head.group(2).replace(' ', '').split(',')

    def update(self) :
        """Register specific symbol attributes in database"""
        values = ['method', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['args', '|'.join(self.args)],\
         ['id_class', str(self.idclass)]]
        return self.DBC.updateSymbol(values)

    def show(self) :
    # def __str__(self) :
        """Prints line-number and initial-code of each CodeLine stored in Symbol"""
        string = ''
        idclass = self.idclass if 'idclass' in vars(self) else None
        for x in self.code :
            string += x.show(idclass) + '\n'
        return string[:-1]

    def symbRepr(self) :
        """Return a string representative of current Symbol"""
        return str(self.name) + ' [' + str(self.iline) + ']'


