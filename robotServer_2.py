#!/usr/bin/python3
# TCP SERVER FOR MTRN4110
# created by  Benedict Dupree (z5061171)
# last updated 1/2/17

import sys, socket, threading, time
from array import array

MAX_CONNECTIONS = 5 ## only 1 client for now
SERVER_HOST = 'localhost'
SERVER_PORT = 9000


class RobotServer():

    send_freq = 0
    connected_client = False
    active_connections = []

    def __init__(self):

        # Create a TCP/IP socket
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Socket initialised')
        except socket.error:
            print('Error creating socket')
            sys.exit()

        # Bind the socket to the port
        server_address = (SERVER_HOST, SERVER_PORT)
        print('starting up on %s port %s' % server_address)
        try:
            self.sock.bind(server_address)
        except socket.error:
            print('Error binding socket')
            sys.exit()

        self.active_connections.append(self.sock)
        # Listen for incoming connections
        self.sock.listen(MAX_CONNECTIONS)
        print("\n\n<<<<<<<<< --------  This is the LattePanda Server  --------- >>>>>>>>>\n\n")


    def receive(self):

        if self.connected_client:
            # Receive the data in small chunks and retransmit it
            while True:
                data = self.client_connection.recv(16)
                print('received "%s"' % data)
                if data:
                    print('sending data back to the client')
                    # client_connection.sendall(data) # echo message back to client

                    # pull apart packet
                    stop_byte = data[0]
                    set_freq = data[1]
                    print('stop_byte is:', stop_byte, ", set_freq is:", set_freq)
                    # interpret data
                    if stop_byte == b'0xff':
                        self.send_freq = 0
                    elif stop_byte == b'0x01':
                        self.send_freq = int(set_freq)

                else:
                    print('no more data from', self.client_address)
                    break

    def pckg_data(self, d):

        pckt_array = array('H', [d+1, d+2, d+3, d+4, d+5, d+6, d+7, d+8, d+9, d+10])
        print(pckt_array)
        return pckt_array

    def send_data(self, d, client, cli_addr):

        for sckt in self.active_connections:
            if sckt == client:
                try:
                    client.sendall(self.pckg_data(d))
                except socket.error:
                    print("connection to client at", cli_addr, "lost")


    def run(self):

        # Wait for a connection
        print('waiting for a connection')
        while 1:
            # print('start loop')
            try:
                client_connection, client_address = self.sock.accept()
                print("im here")
            except socket.error:
                # print('could not connect to a client') # timeout needed??
                continue
            else:
                print('connection from', client_connection, "@", client_address)
                self.active_connections.append(client_connection)
                self.connected_client = True
                break



        # loop timing setup
        N = 1 / self.send_freq
        print('N is ', N)
        repsCompleted = 0
        beginningOfTime = time.clock()
        start = time.clock()
        goAgainAt = start + N

        d = 0
        while True:

            print("Loop #%d at time %f" % (repsCompleted, time.clock() - beginningOfTime))
            repsCompleted += 1

            self.send_data(d, client_connection, client_address)

            # Otherwise, wait for next interval
            timeToSleep = goAgainAt - time.clock()
            goAgainAt += N
            time.sleep(timeToSleep)
            d += 1


        # finally:
        #     # Clean up the connection
        #     self.client_connection.close()

if __name__ == '__main__':

    server = RobotServer()
    threading.Thread(target=server.receive).start()
    threading.Thread(target=server.run).start()

    server.sock.close()   # close socket
