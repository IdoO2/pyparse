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

### REGEX -- use across the analyzer for code parsing
RDIC = {
  'se_docs' : re.compile('"""|\'\'\''),
  'se_cons' : re.compile(' *def *__init__'),
  'se_priv_meth' : re.compile(' *def *__'),
  'se_space': re.compile('^( +)'),
  'se_ncmt': re.compile('(#.*)'), #renvoie tout ce qui n'est pas un commentaire
  'se_str': re.compile("\"([^\"]*)\"|\'([^\']*)\'"),
  'se_meth': re.compile('def _{2}'), #vérifie si une méthode est privé
  'se_var': re.compile('==|<=|!=|>=|='), #regex utilisé pour trouver une variable
  'se_ol': re.compile(': *(\w)'),

  'import_from': re.compile('from ([^ ]+) import (\*|.+)'),
  'import': re.compile('import ([^ ]+)'),
  'class': re.compile('class ([^(\s:]+).([^)]*)'),
  'class_attr': re.compile('self.([^=]+)'),
  'fonction': re.compile('^def (.+(?=[(])).([^)]*)'),
  'method': re.compile('def ([^(]+).([^)]*)'),
  'variable': re.compile('([^[ =]+)'),
  'cl_comm': re.compile('\s,|,\s'), #selectionne les arguments quelque soit leur présentation
  'cl_idet': re.compile('[\t ]+'), #sélectionne l'indentation
  'syntaxe': re.compile('[\+\.;,\(\)\[\]{]') #nettoie une ligne de la syntaxe pour optimiser son parcours
}

class Import(Symbol) :
    def __init__(self, id_file, code) :
        super().__init__(id_file, code)
        self.module = ''
        self.element = ''
        self.alias = ''
        self.analyze()
        self.update()

    def analyze(self) :
        code = self.code[0].ccode
        code = re.sub(RDIC['cl_comm'], ',', code)
        if 'from' in code.split() :
            imp = RDIC['import_from'].match(code)
            self.module = (imp.group(1))
            self.element = imp.group(2).split(',')
        else :
            imp = RDIC['import_from'].match(code)
            self.module = imp.group(1)
        if 'as' in code.split() :
            self.alias = re.findall('as (.+)', code)[0]

    def update(self) :
        values = ['import', '', self.id_file, self.iline]
        values[1] = [['module', self.module], \
         ['element', '|'.join(self.element)], ['alias', self.alias]]
        return self.DBC.updateSymbol(values)

class Variable(Symbol) :
    def __init__(self, id_file, code) :
        super().__init__(id_file, code)
        self.name = ''
        self.analyze()
        self.update()

    def analyze(self) :
        code = self.code[0].ccode
        self.name = RDIC['variable'].match(code).group(1)

    def update(self) :
        values = ['variable', '', self.id_file, self.iline]
        values[1] = [['name', self.name]]
        return self.DBC.updateSymbol(values)

class Function(Symbol) :
    def __init__(self, id_file, code) :
        super().__init__(id_file, code)
        self.name = ''
        self.args = []
        self.analyze()
        self.update()

    def analyze(self) :
        code = self.code[0].ccode
        head = RDIC['fonction'].match(code)
        self.name = head.group(1)
        self.args = head.group(2).replace(' ', '').split(',')

    def update(self) :
        values = ['function', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['args', '|'.join(self.args)]]
        return self.DBC.updateSymbol(values)

class Class(Symbol) :
    def __init__(self, id_file, code) :
        super().__init__(id_file, code)
        self.name = ''
        self.lega = []
        self.analyze()
        self.update()

    def analyze(self) :
        code = self.code[0].ccode
        head = RDIC['class'].match(code)
        self.name = head.group(1)
        self.lega = head.group(2).replace(' ', '').split(',')

    def update(self) :
        values = ['class', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['legacy', '|'.join(self.lega)]]
        return self.DBC.updateSymbol(values)

class ClassAttribute(Symbol) :
    def __init__(self, id_file, code, idclass) :
        super().__init__(id_file, code)
        self.name = ''
        self.idclass = idclass
        self.analyze()
        self.update()

    def analyze(self) :
        code = self.code[0].ccode
        head = RDIC['class_attr'].match(code)
        self.name = head.group(1)

    def update(self) :
        values = ['class_attr', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['id_class', str(self.idclass)]]
        return self.DBC.updateSymbol(values)

class Method(Symbol) :
    def __init__(self, id_file, code, idclass) :
        super().__init__(id_file, code)
        self.name = ''
        self.args = []
        self.idclass = idclass
        self.analyze()
        self.update()

    def analyze(self) :
        code = self.code[0].ccode
        head = RDIC['method'].match(code)
        self.name = head.group(1)
        self.args = head.group(2).replace(' ', '').split(',')

    def update(self) :
        values = ['method', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['args', '|'.join(self.args)],\
         ['id_class', str(self.idclass)]]
        return self.DBC.updateSymbol(values)

class DocString(Symbol) :
    def __init__(self, id_file, code) :
        super().__init__(id_file, code)

    def analyze(self) : return

    def update(self) : return

