#!/usr/bin/python3
# -*- coding: utf-8 -*-

from threading import Thread
import Test.network_common as NC
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

    def __init__(self) :
        self.isSync = False

    def __sync(self) :
        self.isSync = True
        print ("synced...")
        return "SYNC OK"

    def __show(self, data) :
        print ("show")
        return "SHOW " + data + " OK"

    def __replace(self, data) :
        print ("replace", data[0], data[1])
        return

    def serverProcess(self, idata, add_data) :
    # on récupère la donnée et on dirige les requêtes vers les bonnes fonctions
        idata.replace('\n', '')
        op = idata[0:4]
        qry = idata[4:]

        if op == "SYNC" :
            return self.__sync()
        elif op == "SHOW" :
            return self.__show(qry.split())
        elif op == "REPL" :
            return self.__replace(qry.split())
        else :
            return "ERROR " + idata

    def run(self) :
        NC.initFServer(1254, process=self.serverProcess)


class EventDump(sublime_plugin.EventListener):
    def on_activated(self, view):
        wdic = (view.window().extract_variables())
        if "file_name" in wdic and '.py' in wdic["file_name"] :
            changeFile([wdic["file_name"], wdic["file_path"]])
        print (view.file_name(), "is now the active view")

    def on_post_save (self, view) :
        print (view.file_name(), "saved")

if not NC.checkPort("127.0.0.1", 1254) :
    print ("starting analyser server")
    thd = Thread(target=lauchServer)
    thd.setDaemon(True)
    thd.start()

