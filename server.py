# -*- coding: utf-8 -*-

import socket
import subprocess

def runCmd(cmd):
  p = subprocess.Popen(cmd, stdin = subprocess.PIPE, 
                          stdout = subprocess.PIPE, shell = False)
  #(out, err) = p.communicate()
  #print('out: ', str(out), str(err))
  return p

HOST = ''  # Standard loopback interface address (localhost or '' for connections from anyone)
PORT = 57861  # Port to listen on (non-privileged ports are > 1023)

pNP = None
pTMA = None
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        print('Waiting for client connection')
        conn, addr = s.accept()
        try:
            with conn:
              print('Connected by', addr)
              while True:
                data = conn.recv(1024)
                print('recieved: ', data.decode(), ' from client: %r'%addr[0])
                if data.decode() == 'q':
                  break
                elif data.decode() == 'openNp':
                  print('trying to open notepad')
                  pNP = runCmd('notepad')
                  conn.sendall(b'Opened process: %d' %pNP.pid)
                elif data.decode() == 'killNp':
                  if not pNP is None:
                    pNP.kill()
                    conn.sendall(b'killed process: %d' %pNP.pid)
                elif data.decode() ==  'openTMA':
                  print('trying to open TMA')
                  cmd = [r'C:\Program Files (x86)\Aeroflex\TM500\LTE - LMF 8.13.0\Test Mobile Application\TmaApplication.exe']
                  cmd.extend(['/u', "Default User", '/c', 'y', '/p', '5003', '/a', 'n', '/ea', 'y', '/pa'])#DO NOT MUCK WITH "Default User" string.  MUST HAVE DOUBLE QUOTES ONLY or TMA CRASHES!!!
                  pTMA = runCmd(cmd)
                  conn.sendall(b'Opened process: %d' %pTMA.pid)
                elif data.decode() ==  'killTMA':
                  #pId = runCmd('taskkill /F /PID %d'%pIdTMA)
                  #pId.kill()
                  if not pTMA is None:
                    try:
                        pTMA.kill()
                        conn.sendall(b'killed process: %d' %pTMA.pid)
                    except:
                        conn.sendall(b'problem killing process: %d' %pTMA.pid)
                  else:
                      conn.sendall(b'nothing to kill')
                else:
                  conn.sendall(b'echo: ' + data)
        except:
            pass
          
          
          
