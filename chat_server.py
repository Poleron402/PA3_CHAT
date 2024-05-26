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
client_names = {}  # dictionary to store client names


def handle_client(connection_socket, addr, client_id):
    client_name = client_names[connection_socket]  # get client name
    while True:  # loop to handle client messages
        try:
            message = connection_socket.recv(1024).decode()  # receive message from client
            if message == "bye":  # if client sends 'bye', close connection
                # Inform other client and close connection
                exit_message = f"{client_name} has left the chat."
                for client in clients.values():  # loop through clients
                    if client != connection_socket:  # if client is not the one leaving
                        client.send(exit_message.encode())  # send exit message
                connection_socket.close()  # close connection
                # remove client from clients dictionary - prevents server from sending to a client that has left
                clients.pop(client_id)
                break
            else:
                # Forward the message to the other client with the client's name
                message_to_send = f"{client_name}: {message}"
                for client in clients.values():  # loop through clients
                    if client != connection_socket:  # if client is not the one sending the message
                        client.send(message_to_send.encode())  # send message
        except Exception as e:
            log.error(f"Error handling client {client_name}: {e}")
            connection_socket.close()
            clients.pop(client_id)
            break


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', server_port))
    server_socket.listen(2)  # Allow two clients
    print("Server is ready to receive on port", server_port)

    client_counter = 0

    while True:
        if len(clients) < 2:
            conn, addr = server_socket.accept()
            client_counter += 1  # increment client counter
            client_id = f"Client {'Y' if client_counter == 1 else 'X'}"  # set client id
            clients[client_id] = conn  # add client to clients dictionary
            client_names[conn] = client_id  # add client name to client_names dictionary
            log.info(f"{client_id} connected from {addr}")  # log client connection
            #  start thread to handle client
            threading.Thread(target=handle_client, args=(conn, addr, client_id)).start()


if __name__ == "__main__":
    main()
