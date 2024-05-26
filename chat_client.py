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
import threading
import sys

# Configure logging
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_name = '10.0.0.1'
server_port = 12000


# the function below is a thread that listens for messages from the server
def receive_messages(client_socket):
    while True:
        server_response = client_socket.recv(1024)  # receive server response
        if not server_response:  # if server has closed the connection
            break
        # Decode server response from UTF-8 bytestream
        server_response_decoded = server_response.decode()
        print(server_response_decoded)  # print server response
        # if server response is that the server has left the chat, break the loop
        if server_response_decoded.endswith('has left the chat.'):
            print('\n' + "Server has closed the connection.")
            break
    client_socket.close()  # close the socket
    sys.exit(0)


def main():
    # Create socket
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    try:
        # Establish TCP connection
        client_socket.connect((server_name, server_port))
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

    # Start the thread for receiving messages
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()

    print("Welcome to the chat! To send a message, type the message and click enter.")
    print("Input lowercase sentence: ")

    try:
        while True:
            user_input = input()  # get user input
            # Set data across socket to server
            client_socket.send(user_input.encode())
            if user_input.lower() == "bye":  # if user input is 'bye', break the loop
                print("\nDisconnecting from chat...\n")
                break

    except Exception as e:
        log.exception("Error sending message: {}".format(e))
    finally:
        # Close socket prior to exit
        client_socket.close()
        sys.exit(0)  # exit program


# This helps shield code from running when we import the module
if __name__ == "__main__":
    main()
