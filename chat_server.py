#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "OtterAI"
__credits__ = [
  "Anthony Suvorov",
  "Aryeh Freud",
  "Eric Rodriguez",
  "Polina Mejia"
]


import socket as s
import time
import threading
# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000

client_ports = {}
def connection_handler(connection_socket, address):
      while True:
        query = connection_socket.recv(1024)
        query_decoded = query.decode()
        if not query:
          break
        response = f"{str(client_ports.get(connection_socket))}: {query_decoded}"
        # Sent response over the network, encoding to UTF-8
        if query_decoded.lower() == 'bye':
          response += '\n***Client has disconnected***'
          del client_ports[connection_socket]
          if len(client_ports) != 0:
            for i in client_ports.keys():
              if i != connection_socket:
                i.send(response.encode())
          break
        for i in client_ports.keys():
          if i != connection_socket:
            i.send(response.encode())
      connection_socket.close()
  

def main():
  # Create a TCP socket
  # Notice the use of SOCK_STREAM for TCP packets
  server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
  
  # Assign port number to socket, and bind to chosen port
  server_socket.bind(('',server_port))
  
  # Configure how many requests can be queued on the server at once
  server_socket.listen(2)
  
  # Alert user we are now online
  log.info("The server is ready to receive on port " + str(server_port))
  
  # Surround with a try-finally to ensure we clean up the socket after we're done
  try:
    # Enter forever loop to listen for requests
    while True:
      # When a client connects, create a new socket and record their address
      connection_socket, address = server_socket.accept()
      # client_ports.append(connection_socket)
      un = connection_socket.recv(1024)
      client_ports[connection_socket] = un.decode()
      log.info(f"Connected to {un.decode()} at {address}")
      # Pass the new socket and address off to a connection handler function
      x1 = threading.Thread(target=connection_handler, args = (connection_socket, address))
      x1.start()
  finally:
    server_socket.close()

if __name__ == "__main__":
  main()