# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 10:31:37 2018

@author: antlab
"""
import socket
import select
import time
       
class client(socket.socket):
  def __init__(self, hostIp, port):
    super().__init__(socket.AF_INET, socket.SOCK_STREAM)
    self.host = hostIp
    self.port = port
    self.bufSz = 1024
    self.data = None
    self.timeOut = 1
    self.ready = None
    self.connect((self.host, self.port))
    
  def openNp(self):
    self.write('openNp')
    
  def killNp(self):
    self.write('killNp')
    self.connect((self.host, self.port))
  
  def msg_resp(self, msg):
    self.sendall(str.encode(msg))
    self.ready = select.select([self], [], [], self.timeOut)
    while not self.ready[0]:
      print('trying to read empty network buffer')
      time.sleep(1)
      self.ready = select.select([self], [], [], self.timeOut) 
    self.data = self.recv(self.bufSz)
    resp = f'received {self.data.decode()} from {self.host}'
    return resp
      
  def close(self):
    try:
      self.sendall(str.encode('q'))
    except Exception as e:
      print(f'Error on close: {e}')
  
if __name__ == '__main__':
    import sys
    HOST = str(sys.argv[1])  # The server's hostname or IP address
    PORT = int(sys.argv[2])  # The port used by the server
    c = client(HOST, PORT)









