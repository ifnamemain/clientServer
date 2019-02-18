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
  def openTMA(self):
    self.write('openTMA')
    
  def killTMA(self):
    self.write('killTMA')
  
  def write(self, msg):
    self.sendall(str.encode(msg))
    self.read()
    
  def read(self):
    self.ready = select.select([self], [], [], self.timeOut)
    while not self.ready[0]:
      print('trying to read empty network buffer')
      time.sleep(1)
      self.ready = select.select([self], [], [], self.timeOut) 
    self.data = self.recv(self.bufSz)
    print('recieved: ', self.data.decode(), ' from server: %r'%self.host)
      
  def close(self):
    try:
      self.sendall(str.encode('q'))
      self.close()
    except:
      pass
  
if __name__ == '__main__':
  HOST = 'localhost'  # The server's hostname or IP address
  PORT = 8888        # The port used by the server
  c = client(HOST, PORT)









