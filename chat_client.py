#!env python
"""Chat client for CST311 Programming Assignment 3"""
__author__ = "[OtterAI]"
__credits__ = [
  "Anthony Suvorov",
  "Aryeh Freud",
  "Eric Rodriguez",
  "Polina Mejia"
]
# Import statements
import socket as s
import threading
# Configure logging
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_name = '10.0.0.1'
server_port = 12000


def send_msg(client_socket):
  print('Welcome to the chat')
  while True:
    user_input = input()
      # Set data across socket to server
      #  Note: encode() converts the string to UTF-8 for transmission
    if user_input.lower()=='bye':
      user_input+"\n***The client has left the chat***"
      client_socket.send(user_input.encode())
      break
    # Read response from server
    client_socket.send(user_input.encode())
  
  

def receive_msg(client_socket):
  # try:
    while True:
      server_response = client_socket.recv(1024)
      if not server_response:
        break
      # Decode server response from UTF-8 bytestream
      server_response_decoded = server_response.decode()
      # Print output from server
      print(server_response_decoded)


    
def main():
  # Create socket
  client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
  # un = input("Enter username: ")
  # client_socket.connect((server_name,server_port))
  # client_socket.send(un.encode())
  try:
    x = threading.Thread(target=send_msg, args=(client_socket,))
    y = threading.Thread(target=receive_msg, args=(client_socket,))
    x.start()
    y.start()
    x.join()
    y.join()
  finally:
    if client_socket:
      client_socket.close()

# This helps shield code from running when we import the module
if __name__ == "__main__":
  main()