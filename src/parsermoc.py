#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

class Parser():

    """ MOC parser class

        - Construct with content and line ending name
        - Determine indentation
        - Receive full text when updated
    """

    __sublime_line_endings = {'Unix': '\n', 'Windows': '\c\r'}
    __line_end = '\n'
    __text_lines = []
    __indent = {'type': 'spaces', 'value': 1}

    def getSymbolTree(self):
        """ Return symbol tree """
        return [
                [('Master', {'type': 'class'}),
                    ('randval', {'type': 'method'}), [('__init__', {'type': 'method', 'signature': ['arg', '*args', '**kwargs']}),
                    ('change', {'type': 'function'})]]
        ]

    def updateWith(self, file_contents):
        """ Receive full text, raw, from UI

            Diffs current state of file with incoming state
            Triggers relevant actions on change
            Obviously the current state of this function is utterly broken
            (doesn’t handle line number changes)
        """
        if len(self.__text_lines) is 0:
            # No text? -> Initial population
            self.__setLineEndings(file_contents)
            self.__text_lines = file_contents.split(self.__line_end)
            self.__setIndent()

        new_state = file_contents.split(self.__line_end)
        for idx in range(len(new_state)):
            if new_state[idx] != self.__text_lines[idx]:
                print(new_state[idx])
                pass # ... on to model

    def __setLineEndings(self, full_text):
        """ Set line endings (unix or windows)

            Must be one of `Unix` or `Windows`
        """
        find_le = re.compile('(\n|\c\r)')
        le_found = find_le.match(full_text)
        if le_found is None:
            return
        if '\n' in le_found.group(0):
            self.__line_end = self.__sublime_line_endings['Unix']
        else:
            self.__line_end = self.__sublime_line_endings['Windows']

    def __setIndent(self):
        """ Determine indentation one character at a time
            Sets self.__indent, a dict with keys <str>type, <int>value
            Alternative to __setIndentRegex
        """
        for line in self.__text_lines:
            if line[0] is '\t':
                self.__indent['type'] = 'tabs'
                break
            if line[0] is ' ':
                i = 1
                while line[i] is ' ':
                    i += 1
                    self.__indent['value'] = i
            break

    def __setIndentRegex(self):
        """ Determine indentation using a regex
            Sets self.__indent, a dict with keys <str>type, <int>value
            Alternative to __setIndent
        """
        for line in self.__text_lines:
            ##indentRegex = '(?<=:' + le + ')^\s+'
            find_space = re.compile('^\s+')
            space_found = find_space.match(line)
            if space_found is None:
                continue
            else:
                if '\t' in space_found.group(0):
                    self.__indent['type'] = 'tabs'
                else:
                    self.__indent['value'] = len(space_found.group(0))
                break

