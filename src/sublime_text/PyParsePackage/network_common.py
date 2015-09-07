#! /usr/bin/env python3
#! -*- coding: utf8 -*-
# Author: Cyril RICHARD

from threading import Thread
import socket as S
import sys
import os

### UTILITIES
#############################################################################################
#############################################################################################

#comes from: http://stackoverflow.com/questions/19196105/python-how-to-check-if-a-network-port-is-open-on-linux
def checkPort(host, port) :
  # Create a TCP socket
  s = S.socket()
  print ("Attempting to connect to", host, "on port", port)
  try:
    s.connect((host, port))
    print ("Connected to", host, "on port", port)
    return True
  except S.error :
    print ("Connection to", host ,"on port", port,"failed")
    return False

def _checkPort(host, port) :
  # host = S.gethostbyname(S.gethostname())
  print (host)
  sock = S.socket(S.AF_INET, S.SOCK_STREAM)
  result = sock.connect_ex((host, port))
  if result == 0:
    return False #open
  else:
    return True #not open

def serverLoop(sock, addr, callback, add_data=[]):
    while True :
        data = sock.recv(1024 * 5)
        if not data: break
        data = callback(data.decode('utf-8').replace('\n', ''), add_data)
        sock.sendall((data + '\n').encode('utf-8'))
        if "close" == data.rstrip(): break # type 'close' on client console to close connection from the server side

    sock.close()



### CLIENT CONNECTIONS
#############################################################################################
#############################################################################################

def initClient(host, port) :
  #on tente de récupérer les infos de connexion à l'adresse et port spécifié
  try :
    res = S.getaddrinfo(host, port, S.AF_UNSPEC, S.SOCK_STREAM, 0)
  except (S.gaierror, S.error) as e :
    exit('erreur sur ' + str(host) + ' port: ' + str(port) + ' log: ' + e.strerror)

  for add in res :
    family, socktype, proto, canonname, sockaddr = add

     #on tente la création du socket, le binding et l'établissement de la connexion
    try:
      s = S.socket(family, socktype, proto)
      s.connect(sockaddr)
    except S.error as e:
      raise

  if s is None:
    print('could not open socket')
    sys.exit(1)
  else :
    return s


### SERVER CONNECTION
#############################################################################################
#############################################################################################

# server connection using forks : memory address are distinct
def initFServer(port, loop=serverLoop, process=lambda x, d: x, add_data=[]) :
  s = None
  family = S.AF_UNSPEC
  socktype = S.SOCK_STREAM
  flags = S.AI_PASSIVE

  #on tente de récupérer les infos de connexion à l'adresse et port spécifié
  try :
    res = S.getaddrinfo('localhost', port, family, socktype, 0, flags)
  except S.gaierror as e :
    exit('erreur sur le port ' + str(port) + ' log: ' + e.strerror)

  for add in res :
    family, socktype, proto, canonname, sockaddr = add

     #on tente la création du socket, le binding et l'établissement de la connexion
    try:
      s = S.socket(family, socktype, proto)
      s.bind(sockaddr)
      s.listen(1)
    except S.error as e :
      sys.stderr.write(e.strerror)
      if s : s.close()
      s = None
      continue
    break

  while True :
    csock, addr = s.accept()
    if s is None:
      sys.exit('could not open socket')
    try :
      t = os.fork()
    except OSError as e :
      sys.stderr.write(e.strerror)
      continue

    if (t != 0) :
      csock.close()
    else :
      s.close()
      loop(csock, addr, process, add_data)
      exit(0)

#server connection using threads : memory address are equal
#inspired by: http://code.activestate.com/recipes/578247-basic-threaded-python-tcp-server/
def initTServer(port, loop=serverLoop, process=lambda x, d: x, add_data=[]) :
  try :
    serversock = S.socket(S.AF_INET, S.SOCK_STREAM)
    serversock.setsockopt(S.SOL_SOCKET, S.SO_REUSEADDR, 1)
    serversock.bind(("localhost", port))
    serversock.listen(5)
  except:
    raise

  while True:
    csock, addr = serversock.accept()
    thd = Thread(target=loop, args=(csock, addr, process, add_data))
    thd.setDaemon(True)
    thd.start()



