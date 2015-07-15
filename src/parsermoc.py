#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

class Parser():

    __sublime_line_endings = {'Unix': '\n', 'Windows': '\c\r'}
    __line_end = '\n'
    __text_lines = []
    __indent = {'type': 'spaces', 'value': 4}

    def __init__(self, file_contents, line_endings):
        '''
        Take possession of the text:
        - set line endings
        - set indent value
        - parse to list of lines
        '''
        self.__line_end = self.__sublime_line_endings[line_endings]
        self.__text_lines = file_contents.split(self.__line_end)
        self.__setIndent()

    def __str__(self):
        return '--------------------\n'.join([
                str(len(self.__text_lines))
            ] + self.__text_lines
        )

    def updateWith(self, file_contents):
        '''
        Diffs current state of file with incoming state
        Triggers relevant actions on change
        Obviously the current state of this function is utterly broken
        (doesn’t handle line number changes)
        '''
        new_state = file_contents.split(self.__line_end)
        for idx in range(len(new_state)):
            if new_state[idx] != self.__text_lines[idx]:
                print(new_state[idx])
                pass # ... on to model

    def __setIndent(self):
        '''
        Set indentation value for class per file
        Sets self.__indent, a dict with keys <str>type, <int>value
        '''
        for line in self.__text_lines:
            ##indentRegex = '(?<=:' + le + ')^\s+'
            find_space = re.compile('^\s+')
            space_found = find_space.match(line)
            if space_found is None:
                continue
            else:
                if '\t' in space_found.group(0):
                    self.__indent['type'] = 'tabs'
                    self.__indent['value'] = 1
                else:
                    self.__indent['value'] = len(space_found.group(0))
                break

