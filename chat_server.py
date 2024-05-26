#!env python

"""Chat server for CST311 Programming Assignment 3"""
__author__ = "OtterAI"
__credits__ = [
    "Anthony Suvorov",
    "Aryeh Freud",
    "Eric Rodriguez",
    "Polina Mejia"
]

import socket
import threading
# Configure logging
import logging

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

server_port = 12000
clients = {}  # dictionary to store client sockets


def handle_client(connection_socket, addr):
    while True:  # loop to handle client messages
        try:
            message = connection_socket.recv(1024).decode()  # receive message from client
            if not message:
                break
            if message == "bye":  # if client sends 'bye', close connection
                # Inform other client and close connection
                exit_message = f"{clients[connection_socket]} has left the chat."
                for client in clients.keys():  # loop through clients
                    if client != connection_socket:  # if client is not the one leaving
                        client.send(exit_message.encode())  # send exit message
                connection_socket.close()  # close connection
                # remove client from clients dictionary - prevents server from sending to a client that has left
                clients.pop(connection_socket)
                break
            else:
                # Forward the message to the other client with the client's name
                message_to_send = f"{clients[connection_socket]}: {message}"
                for client in clients.keys():  # loop through clients
                    if client != connection_socket:  # if client is not the one sending the message
                        client.send(message_to_send.encode())  # send message
        except Exception as e:
            log.error(f"Error handling client {clients[connection_socket]}: {e}")
            connection_socket.close()
            clients.pop(connection_socket)
            break
    connection_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(2)  # Allow two clients
    print("Server is ready to receive on port", server_port)
    client_counter = 0
    while True:
        # if len(clients) < 2:
        connection_socket, address = server_socket.accept()
        client_counter+=1
        client_id  = f"Client {'Y' if client_counter == 1 else 'X'}" 
        clients[connection_socket] = client_id
        log.info(f"Connected to {client_id} at {address}") # set client id
        #  start thread to handle client
        threading.Thread(target=handle_client, args=(connection_socket, address)).start()
        
    # server_socket.close()
if __name__ == "__main__":
    main()
