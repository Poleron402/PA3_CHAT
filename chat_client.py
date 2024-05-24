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

lock = threading.Lock()
def main():
  # Create socket
  client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
  
  try:
    # Establish TCP connection
    client_socket.connect((server_name,server_port))
  except Exception as e:
    log.exception(e)
    log.error("***Advice:***")
    if isinstance(e, s.gaierror):
      log.error("\tCheck that server_name and server_port are set correctly.")
    elif isinstance(e, ConnectionRefusedError):
      log.error("\tCheck that server is running and the address is correct")
    else:
      log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
    exit(8)
    
  # Get input from user
  # initializer = False
  user_input = ''

  print('Welcome to the chat')
  while user_input.lower() != 'bye':
    user_input = input("Enter a message: ")
  # Wrap in a try-finally to ensure the socket is properly closed regardless of errors
    try:
      # Set data across socket to server
      #  Note: encode() converts the string to UTF-8 for transmission
      client_socket.send(user_input.encode())
    # Read response from server
      server_response = client_socket.recv(1024)
      # Decode server response from UTF-8 bytestream
      server_response_decoded = server_response.decode()
      # lock.acquire()
      # Print output from server
      print('From Server:')
      print(server_response_decoded)
      # lock.release()
    finally:
    #   # Close socket prior to exit
      client_socket.close()
  # client_socket.close()
# This helps shield code from running when we import the module
if __name__ == "__main__":
  main()