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

  'import_from': re.compile('from ([^ ]+) import *(\*|.+)'),
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
    def __init__(self) :
        super().__init__()
        self.module = ''
        self.element = ''
        self.alias = ''

    def register(self, id_file, code) :
        super().register(id_file, code)
        self.analyze()
        self.update()

    def load(self, data) :
        super().load(data)
        self.module = data[7]
        self.element = data[8]
        self.alis = data[9]

    def analyze(self) :
        code = self.code[0].ccode
        code = re.sub(RDIC['cl_comm'], ',', code)
        if 'from' in code.split() :
            imp = RDIC['import_from'].match(code)
            self.module = (imp.group(1))
            ele = re.sub('\(|\)', '', imp.group(2))
            self.element = ele.split(',')
        else :
            imp = RDIC['import'].match(code)
            self.module = imp.group(1)
        if 'as' in code.split() :
            self.alias = re.findall('as (.+)', code)[0]

    def update(self) :
        values = ['import', '', self.id_file, self.iline]
        values[1] = [['module', self.module], \
         ['element', '|'.join(self.element)], ['alias', self.alias]]
        return self.DBC.updateSymbol(values)

    def symbRepr(self) :
        """Prints attributes of the current Symbol (use mostly in debugg)"""
        return [str(self.module) + ' [' + str(self.iline) + ']'] + self.element.split('|')

class Variable(Symbol) :
    def __init__(self) :
        super().__init__()
        self.name = ''

    def register(self, id_file, code) :
        super().register(id_file, code)
        self.analyze()
        self.update()

    def load(self, data) :
        super().load(data)
        self.name = data[7]

    def analyze(self) :
        code = self.code[0].ccode
        self.name = RDIC['variable'].match(code).group(1)

    def update(self) :
        values = ['variable', '', self.id_file, self.iline]
        values[1] = [['name', self.name]]
        return self.DBC.updateSymbol(values)

    def symbRepr(self) :
        """Prints attributes of the current Symbol (use mostly in debugg)"""
        return str(self.name) + ' [' + str(self.iline) + ']'

class Function(Symbol) :
    def __init__(self) :
        super().__init__()
        self.name = ''
        self.args = []

    def register(self, id_file, code) :
        super().register(id_file, code)
        self.analyze()
        self.update()

    def load(self, data) :
        super().load(data)
        self.name = data[7]
        self.args = data[8]

    def analyze(self) :
        code = self.code[0].ccode
        head = RDIC['fonction'].match(code)
        self.name = head.group(1)
        self.args = head.group(2).replace(' ', '').split(',')

    def update(self) :
        values = ['function', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['args', '|'.join(self.args)]]
        return self.DBC.updateSymbol(values)

    def symbRepr(self) :
        """Prints attributes of the current Symbol (use mostly in debugg)"""
        return str(self.name) + ' [' + str(self.iline) + ']'

class Class(Symbol) :
    def __init__(self) :
        super().__init__()
        self.name = ''
        self.lega = []

    def register(self, id_file, code) :
        super().register(id_file, code)
        self.analyze()
        self.update()

    def load(self, data) :
        super().load(data)
        self.name = data[7]
        self.lega = data[8]

    def analyze(self) :
        code = self.code[0].ccode
        head = RDIC['class'].match(code)
        self.name = head.group(1)
        self.lega = head.group(2).replace(' ', '').split(',')

    def update(self) :
        values = ['class', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['legacy', '|'.join(self.lega)]]
        return self.DBC.updateSymbol(values)

    def symbRepr(self) :
        """Prints attributes of the current Symbol (use mostly in debugg)"""
        return str(self.name) + ' [' + str(self.iline) + ']'


    def show(self) :
    # def __str__(self) :
        """Prints line-number and initial-code of each CodeLine stored in Symbol"""
        string = ''
        idclass = self.id if 'id' in vars(self) else None
        for x in self.code :
            string += x.show(idclass) + '\n'
        return string[:-1]

class ClassAttribute(Symbol) :
    def __init__(self) :
        super().__init__()
        self.name = ''
        self.idclass = ''

    def register(self, id_file, code, idclass) :
        super().register(id_file, code)
        self.idclass = idclass
        self.analyze()
        self.update()

    def load(self, data) :
        super().load(data)
        self.idclass = data[7]
        self.name = data[8]

    def analyze(self) :
        code = self.code[0].ccode
        head = RDIC['class_attr'].match(code)
        self.name = head.group(1)

    def update(self) :
        values = ['class_attr', '', self.id_file, self.iline]
        values[1] = [['name', self.name], ['id_class', str(self.idclass)]]
        return self.DBC.updateSymbol(values)

    def symbRepr(self) :
        """Prints attributes of the current Symbol (use mostly in debugg)"""
        return str(self.name) + ' [' + str(self.iline) + ']'

    def show(self) :
    # def __str__(self) :
        """Prints line-number and initial-code of each CodeLine stored in Symbol"""
        string = ''
        idclass = self.idclass if 'idclass' in vars(self) else None
        for x in self.code :
            string += x.show(idclass) + '\n'
        return string[:-1]

class Method(Symbol) :
    def __init__(self) :
        super().__init__()
        self.name = ''
        self.args = []
        self.idclass = ''

    def register(self, id_file, code, idclass) :
        super().register(id_file, code)
        self.idclass = idclass
        self.analyze()
        self.update()

    def load(self, data) :
        super().load(data)
        self.idclass = data[7]
        self.name = data[8]
        self.args = data[9]

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

    def show(self) :
    # def __str__(self) :
        """Prints line-number and initial-code of each CodeLine stored in Symbol"""
        string = ''
        idclass = self.idclass if 'idclass' in vars(self) else None
        for x in self.code :
            string += x.show(idclass) + '\n'
        return string[:-1]

    def symbRepr(self) :
        """Prints attributes of the current Symbol (use mostly in debugg)"""
        return str(self.name) + ' [' + str(self.iline) + ']'


