#!/usr/bin/python3
# created by  Benedict Dupree (z5061171) and Fangni Ai (z5027221)
# last updated 1/2/17

import socket, sys, struct, os
import threading, array


MAX_LENGTH = 100

# SERVER_HOST = '127.0.0.1'
# PORT = 15000


class ChatClient():

    def __init__(self):

        ## Initialise socket
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # socket TCP connection
            print('Socket initialised')

        except socket.error:
            print('Error creating socket')
            sys.exit()

        ## Connect socket to server
        try:
            print(SERVER_HOST, PORT)
            self.sock.connect((SERVER_HOST, PORT))
            print('Connected to', SERVER_HOST, 'on port', PORT)
        except:
            print('Connection failed')
            sys.exit()

        print("\n\n<<<<<<<<< --------  Welcome to the LattePanda Client  --------- >>>>>>>>>\n\n")
        self.answer = input("Would you like to start up the Server? (Y/N): ")
        if self.answer == 'Y':
            self.start_freq = input("Enter a data receive frequency between 1 and 50: ")
            while (self.start_freq < 1) | (self.start_freq > 50) | is:
                self.start_freq = input("Error: Enter a data receive frequency between 1 and 50: ")
            print("Ready to receive messages from LattePanda w/ IP", SERVER_HOST,
                  "on Port", PORT, "at", self.start_freq, "Hz")
        else:
            pass

    def build_packet(self, stop, frequency):

        if stop:
            cmnd = b'0xff'
        else:
            cmnd = b'0x01'
        freq = bytes(frequency)
        packet = cmnd + freq
        print(packet)
        return packet


    # separately threaded receive function
    def receive():
        while True:
            data = self.sock.recv(1024)
            if not data: sys.exit(0)
            print(data)


    def change_freq(self):
        freq = input("Enter a data receive frequency between 1 and 50: ")
        while (freq < 1) | (freq > 50) | (freq.isdigit() == False):
            freq = input("Error: Enter a data receive frequency between 1 and 50: ")
        try:  # sending message packet
            self.sock.send(self.build_packet(stop, freq))
            # print("Sent message to", SERVER_HOST, ":", PORT)  # DEBUG
        except socket.error:
            print('Error sending message')
            sys.exit()

        return freq


    def run(self):
        while True:
            new_freq = change_freq()



if __name__ == '__main__':

    # Command line arguments specify mode, host, port.
    if len(sys.argv) != 3:
        print("Usage: <Server IP> <Server Port>")
    else:

        SERVER_HOST = sys.argv[1]
        print(SERVER_HOST)
        PORT = int(sys.argv[2])
        print(PORT)

    client = ChatClient()
    threading.Thread(target=client.receive()).start()
    threading.Thread(target=client).start()
