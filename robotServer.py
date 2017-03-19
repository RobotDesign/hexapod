#!/usr/bin/python3
# TCP SERVER FOR MTRN4110
# created by  Benedict Dupree (z5061171) and Fangni Ai (z5027221)
# last updated 1/2/17

import socket, threading, select
import sys

SERVER_HOST = '127.0.0.1'
PORT = 9000
MAX_CONNS = 50
# SERVER_HOST = socket.gethostname()
# print("hostname", hostname)
# SERVER_HOST = socket.gethostbyname(hostname) ## find LAN address of host
print("ip:", SERVER_HOST)
SERVER_ADDR = (SERVER_HOST, PORT)


class ChatServer(threading.Thread):

    CLIENT_CMND_LENGTH = 2
    TOTAL_MSG_LEN = 10

    def __init__(self):

        threading.Thread.__init__(self)
        self.connections = []  # list of active connections
        self.program_running = True    # running flag

        # Initialise socket
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket TCP connection
            print('Socket initialised')
        except socket.error:
            print('Error creating socket')
            sys.exit()

        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to local (device) IP and port
        try:
            self.sock.bind((SERVER_HOST, PORT))
        except socket.error:
            print('Error binding socket')
            sys.exit()

        self.sock.listen(MAX_CONNS)
        self.connections.append(self.sock)

        print('Socket bound to', SERVER_HOST, ":", PORT)
        print("\n\n<<<<<<<<< --------  This is the LattePanda Server  --------- >>>>>>>>>\n\n")


    def send_data(self, current_client, data):

        print("data to send is ", data, "of type", type(data))
        print("sending to", current_client, "...")
        try:
            current_client.send(data)
        except socket.error:
            # sckt.close()
            self.connections.remove(current_client)
            print("Error: socket removed")


    def receive_msg(self, sock):

        try:
            cmnd = sock.recv(self.CLIENT_CMND_LENGTH)
        except socket.error:
            print("couldn't receive command")

        print("received command is", cmnd)
        return cmnd

    ## Run - wait to receive messages from clients and print them
    def run(self):
        while self.program_running:
            print("start loop")
            try:
                readable_socks, writable_socks, errors = select.select(self.connections, [], [], 60)
            except socket.error:
                print("Error extracting read lists")
                continue
            else:
                print("readable socks:", readable_socks)
                for sckt in readable_socks:
                    # If socket instance eq server socket
                    if sckt == self.sock:
                        print("creating new client socket?")
                        try:      # accepting new client
                            client_sock, client_addr = self.sock.accept()
                        except socket.error:
                            break
                        else:
                            self.connections.append(client_sock)
                            self.connected_address = client_addr # clunky fix, doesnt work for more than one client
                            print("New client found at (%s, %s)" % client_addr)

                    # else is a client socket connection and we try and receive data from client
                    else:
                        print("receive?")

                        if sckt in self.connections:
                            continue

                        try:
                            msg_rcvd = self.receive_msg(sckt)  # Gets the client message...
                        except socket.error:
                            print("Client (%s, %s) has gone offline" % client_addr)
                            sckt.close()
                            self.connections.remove(sckt)
                            continue
                        if msg_rcvd:
                            print("im here")
                            # 'broadcast' back to everyone (in reality only one client)
                            self.send_data(sckt, msg_rcvd)




if __name__ == '__main__':

    server = ChatServer()
    server.run()
    server.sock.close()   # close socket

