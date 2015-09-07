#!/usr/bin/python3
# -*- coding: utf-8 -*-

from threading import Thread
import PyParsePackage.network_common as NC
import sublime, sublime_plugin

server = None


def changeFile(data) :
    file_path, file_name = data
    s = NC.initClient("127.0.0.1", 1255)
    qry = 'PROC' + file_path + ' ' + file_name
    s.sendall((qry + '\n').encode('utf-8'))

    rsp = s.recv(1024).decode()
    if 'OK' in rsp.split() :
        return True
    return False
    s.close()


def lauchServer() :
    global server
    server = AnalyzerServerST()
    server.run()

class AnalyzerServerST(object) :
    def __sync(self) :
        self.isSync = True
        return "SYNC OK"

    def __show(self, data) :
        view = sublime.active_window().active_view()
        target = view.text_point(int(data), 0)
        view.show(sublime.Region(target))
        return "SHOW OK"

    def __replace(self, data) :
        return

    def serverProcess(self, idata, add_data) :
    # on récupère la donnée et on dirige les requêtes vers les bonnes fonctions
        idata.replace('\n', '')
        op = idata[0:4]
        qry = idata[4:]

        if op == "SYNC" :
            return self.__sync()
        elif op == "SHOW" :
            return self.__show(qry)
        elif op == "REPL" :
            return self.__replace(qry.split())
        else :
            return "ERROR " + idata

    def run(self) :
        NC.initTServer(1254, process=self.serverProcess)


class EventDump(sublime_plugin.EventListener):
    def on_activated(self, view):
        wdic = (view.window().extract_variables())
        if "file_name" in wdic and '.py' in wdic["file_name"] :
            try :
                changeFile([wdic["file_name"], wdic["file_path"]])
            except :
                print ('error')
                pass
        wdic = (view.window().extract_variables())

    def on_post_save (self, view) :
        pass

if not NC.checkPort('127.0.0.1', 1254) :
    thd = Thread(target=lauchServer)
    thd.setDaemon(True)
    thd.start()

