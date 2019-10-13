# -*- coding: utf-8 -*-

import socket
import subprocess
import psutil
import os

PROCESSES = {'notepad': 'notepad.exe', 'tma': 'TmaApplication.exe'}
class server(socket.socket):
  
  def __init__(self, host, port):
    super().__init__(socket.AF_INET, socket.SOCK_STREAM)
    self.__host = host
    self.__port = port
    self.__pid = None
    self.bind((self.__host, self.__port))
    self.listen() 

  def run(self):
    try:
      print('Waiting for client connection')
      conn, addr = self.accept()  #blocks here until client connects
      with conn:
        connected = True
        print(f'Connected to {addr}')
        while connected:
          msg = conn.recv(1024)  #blocks here until server recieves msg
          print('recieved: ', msg.decode(), ' from client: %r'%addr[0])
          connected, response = self.process_data(msg)  #process msgs from client
          conn.sendall(response)  #echo back to client appropriate response
    except Exception as e:
      print(e) 
  
  @staticmethod
  def kill_by_name(*names):
    for pid in psutil.pids():
      try:
        proc = psutil.Process(pid)
        for target in names:
          if proc.name().lower() == server.PROCESSES[target].lower():
            proc.kill()
      except psutil.NoSuchProcess:
        continue
        
  def open_process(self, process, path = None, flags = []):
    if process in server.PROCESSES.keys():
      if path is not None:
        cmd = [os.path.join(path, server.PROCESSES[process])]
      else:
        cmd = [server.PROCESSES[process]]
      cmd.extend(flags)
      print(cmd)
      print('Trying to open %s' % process)
      return subprocess.Popen(cmd, stdin = subprocess.PIPE, 
                          stdout = subprocess.PIPE, shell = False)
    else:
      raise ValueError('Process not in server.PROCESSES')
          
  def process_data(self, data):
    ret = data.decode() != 'q'

    if data.decode() == 'openNp':
      self.__pid = self.open_process('notepad')
      msg = b'opened notepad'

    elif data.decode() == 'killNp':
      self.kill_by_name('notepad')
      msg = b'killed np'

    elif data.decode() ==  'killTMA':
      self.kill_by_name('tma')
      msg = b'killed tma'

    else:
      msg = data.upper()

    return ret, msg

if __name__ == '__main__':
    import sys
    HOST = '0.0.0.0' 
    PORT = 6000
    with server(HOST, PORT) as s:
      while True:
        s.run()
          
          
          
