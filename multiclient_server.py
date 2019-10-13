# -*- coding: utf-8 -*-

import socket
import os
import threading
import queue

class server(socket.socket):

  def __init__(self, host, port):
    super().__init__(socket.AF_INET, socket.SOCK_STREAM)
    self._host = host
    self._port = port
    self.connections = {}
    self.queue = queue.SimpleQueue()

  def handle_connection(self, conn, addr):
    with conn:
      connected = True
      print(f'Connected to {addr}')
      while connected:
        msg = conn.recv(1024)  #blocks here until server recieves msg
        print(f'received {msg.decode()} from {addr}')
        response = msg.decode().upper().encode()
        conn.sendall(response)  #echo back to client appropriate response
        if msg.decode().lower() == 'quit':
          break
    print(f'connection to {addr} closed')
    self.queue.put(conn)

  def cleanup_connections(self):
    while True:
      closed_conn = self.queue.get()
      self.connections[closed_conn].join()
      del self.connections[closed_conn]

  def accept_connections(self):
    try:
      conn, addr = s.accept()
      self.connections[conn] = threading.Thread(target=self.handle_connection, args=(conn, addr))
      self.connections[conn].start()
      print(f'Num clients: {len(self.connections)}')
    except Exception as e:
      print(f'error accepting new connection {e}')

  def __enter__(self):
    self.bind((self._host, self._port))
    self.listen()
    return self

  def __exit__(self, type, value, traceback):
    print(f'\nwaiting for threads to finish')
    for _,t in self.connections.items():
      t.join()
    print(f'releasing port {self._port}')
    self.close()

if __name__ == '__main__':
  HOST = '0.0.0.0'
  PORT = 6000
  threads = []

  try:
    with server(HOST, PORT) as s:
        while True:
          s.accept_connections()
  except KeyboardInterrupt:
    print('killing server')
  

          
          
