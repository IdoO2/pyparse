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


class Import(Symbol) :
    def __init__(self, id_file, code, dbcon) :
        super().__init__(id_file, code, dbcon)
        self.module = None
        self.element = None
        self.alias = None

    def analyze(self) : return

    def update(self) : return

class Variable(Symbol) :
    def __init__(self, id_file, code, dbcon) :
        super().__init__(id_file, code, dbcon)
        self.name = None

    def analyze(self) : return

    def update(self) : return

class Function(Symbol) :
    def __init__(self, id_file, code, dbcon) :
        super().__init__(id_file, code, dbcon)
        self.name = None
        self.args = []

    def analyze(self) : return

    def update(self) : return

class Class(Symbol) :
    def __init__(self, id_file, code, dbcon) :
        super().__init__(id_file, code, dbcon)
        self.name = None
        self.lega = []
        self.attr = []
        self.meth = []

    def analyze(self) : return

    def update(self) : return

class ClassAttribute(Symbol) :
    def __init__(self, id_file, code, dbcon, idclass) :
        super().__init__(id_file, code, dbcon)
        self.name = None
        self.idclass = idclass

    def analyze(self) : return

    def update(self) : return

class Method(Symbol) :
    def __init__(self, id_file, code, dbcon, idclass) :
        super().__init__(id_file, code, dbcon)
        self.name = None
        self.args = None
        self.type = None
        self.idclass = idclass

    def analyze(self) : return

    def update(self) : return

class DocString(Symbol) :
    def __init__(self, id_file, code, dbcon) :
        super().__init__(id_file, code, dbcon)

    def analyze(self) : return

    def update(self) : return

