# -*- coding: utf-8 -*-

import socket
import subprocess
import psutil
import labbench as lb
import os


class server(socket.socket):
  
  processes = {'notepad': 'notepad.exe', 'tma': 'TmaApplication.exe'}
  tmaPath = r'C:\Program Files (x86)\Aeroflex\TM500' \
            r'\LTE - LMF 8.11.0\Test Mobile Application'
  tmaFlags = ['/u', "Default User", '/c', 'y', '/p', 
              '5003', '/a', 'n', '/ea', 'y', '/pa'] #Trying to force double quotes on 'Default User'.  Tma requires it.
  
  def __init__(self, host, port):
    super().__init__(socket.AF_INET, socket.SOCK_STREAM)
    self.__host = host
    self.__port = port
    self.__pid = None
    self.bind((self.__host, self.__port))
    self.listen()
    
  @staticmethod
  def kill_by_name(*names):
    for pid in psutil.pids():
      try:
        proc = psutil.Process(pid)
        for target in names:
          if proc.name().lower() == target.lower():
            lb.logger.info('killing process {}'.format(proc.name()))
            proc.kill()
      except psutil.NoSuchProcess:
        continue
  
  @classmethod      
  def open_process(cls, process, path = None, flags = []):
    if process in cls.processes.values():
      if path is not None:
        cmd = [os.path.join(path, process)]
      else:
        cmd = [process]
      cmd.extend(flags)
      print(cmd)
      print('Trying to open %s' % process)
      return subprocess.Popen(cmd, stdin = subprocess.PIPE, 
                          stdout = subprocess.PIPE, shell = False)
    else:
      raise ValueError('Process not in server.processes')
          
  def process_data(self, data):
    ret = True
    msg = b''
    if data.decode() == 'q':
      ret = False
    elif data.decode() == 'openNp':
      self.__pid = self.open_process(server.processes['notepad'])
      msg = b'opened notepad'
    elif data.decode() ==  'openTMA':
      self.__pid = self.open_process(server.processes['tma'], 
                               server.tmaPath, 
                               server.tmaFlags)
      msg = b'opened tma'
    elif data.decode() == 'killNp':
      self.kill_by_name(server.processes['notepad'])
      msg = b'killed np'
    elif data.decode() ==  'killTMA':
      self.kill_by_name(server.processes['tma'])
      msg = b'killed tma'
    else:
      msg = b'echo: ' + data
    return ret, msg

if __name__ == '__main__':
  HOST = ''  # Standard loopback interface address (localhost or '' for connections from anyone)
  PORT = 57861  # Port to listen on (non-privileged ports are > 1023)
  with server(HOST, PORT) as s:
    while True:
      print('Waiting for client connection')
      conn, addr = s.accept()  #blocks here until client connects
      try:
        with conn:
          print('Connected by', addr)
          running = True
          while running:
            data = conn.recv(1024)  #blocks here until server recieves msg
            print('recieved: ', data.decode(), ' from client: %r'%addr[0])
            running, msg = s.process_data(data)  #process msgs from client
            conn.sendall(msg)  #echo back to client appropriate response
      except Exception as e:
          print(e)
          
          
          
