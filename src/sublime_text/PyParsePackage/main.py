#!/usr/bin/python3
# -*- coding: utf-8 -*-

from threading import Thread
import PyParsePackage.network_common as NC
import sublime, sublime_plugin
from os import path as ospath

server = None
OK_code = '200'
ER_code = '500'

class AnalyzerServerST(object) :
    def __show(self, data) :
        view = sublime.active_window().active_view()
        target = view.text_point(int(data), 0)
        view.show(sublime.Region(target))
        return OK_code

    def serverProcess(self, idata, unused):
        action, qry = idata[:4], idata[4:]

        if action != 'SHOW':
            return ER_code

        return self.__show(qry)

    def run(self) :
        NC.initTServer(1254, process=self.serverProcess)


class EventDump(sublime_plugin.EventListener):
    def on_activated(self, view):
        wdic = (view.window().extract_variables())
        if 'file_name' in wdic and '.py' == wdic['file_name'][-3:]:
            try:
                self.__changeFile(wdic['file_name'], wdic['file_path'])
            except Exception as em:
                print ('PyParse error: {}'.format(em))

    def __changeFile(self, file_name, file_path) :
        fullpath = ospath.join(file_path, file_name)
        query = 'PROC{}\n'.format(fullpath).encode('utf-8')

        try:
            s = NC.initClient('127.0.0.1', 1255)
            s.sendall(query)
            rsp = s.recv(1024).decode()
            s.close()
        except Exception as em:
            print('Unable to handle connection: {}'.format(em))


if not NC.checkPort('127.0.0.1', 1254):
    def lauchServer():
        global server
        server = AnalyzerServerST()
        server.run()

    thd = Thread(target=lauchServer)
    thd.setDaemon(True)
    thd.start()
