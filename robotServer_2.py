#!/usr/bin/python3
# TCP SERVER FOR MTRN4110
# created by  Benedict Dupree (z5061171)
# last updated 1/2/17

import sys, socket, threading, time, select
from array import array
import numpy

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

        self.program_running = True
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the port
        server_address = (SERVER_HOST, SERVER_PORT)
        print('starting up on %s port %s' % server_address)
        try:
            self.sock.bind(server_address)
        except socket.error:
            print('Error binding socket')
            sys.exit()

        self.active_connections.append(self.sock)
        print(self.active_connections)

        # Listen for incoming connections
        self.sock.listen(MAX_CONNECTIONS)
        print("\n\n<<<<<<<<< --------  This is the LattePanda Server  --------- >>>>>>>>>\n\n")


    def receive(self, client, client_address):

        if self.connected_client:
            # Receive the data in small chunks and retransmit it
            while self.program_running:
                try:
                    data = client.recv(16)
                    print('received "%s"' % data)
                except KeyboardInterrupt:
                    client.close()
                    self.program_running = False
                if data:
                    # print('sending data back to the client')
                    # client_connection.sendall(data) # echo message back to client

                    # pull apart packet
                    stop_byte = data[0]
                    set_freq = data[1]
                    print('stop_byte is:', stop_byte, ", set_freq is:", set_freq)
                    # interpret data
                    if stop_byte == 255:
                        self.send_freq = 0
                    elif stop_byte == 1:
                        self.send_freq = int(set_freq)
                        print(self.send_freq)

                    ## start sending data in timed loop based on specified frequency
                    threading.Thread(target=self.timed_send_loop, args=(client, client_address)).start()


                else:
                    print('no more data from', client_address)
                    client.close()
                    self.program_running = False


    def pckg_data(self, d):

        pckt_array = numpy.array([d+1, d+2, d+3, d+4, d+5, d+6, d+7, d+8, d+9, d+10], numpy.uint16)

        # pckt_array = numpy.uint16()
        print(pckt_array)
        return pckt_array

    def send_data(self, d, client, cli_addr):

        for sckt in self.active_connections:
            if sckt == client:
                print(cli_addr)
                try:
                    client.sendto(self.pckg_data(d), cli_addr)
                    print("sending?")
                except socket.error:
                    self.active_connections.remove(client)
                    print("Error: connection to client at", cli_addr, "lost")


    def timed_send_loop(self, client, client_address):
        # loop timing setup
        print("FREQUENCY = ", self.send_freq)
        if self.send_freq > 0:
            self.data_transmitting = True
            N = 1 / self.send_freq
            print('N is ', N)
            loops = 0
            beginningOfTime = time.perf_counter()
            print(beginningOfTime)
            start = time.perf_counter()
            print(time.process_time(), time.perf_counter())
            nextLoopAt = start + N
            d = 0
            while self.data_transmitting:
                print('nextLoopAt', nextLoopAt)
                print("Loop #%d at time %f" % (loops, time.perf_counter() - beginningOfTime))

                try:
                    self.send_data(d, client, client_address)
                except KeyboardInterrupt:
                    client.close()
                    self.program_running = False
                print('time.clock after data send:', time.perf_counter())

                # If we missed our interval, iterate immediately and increment the target time
                if time.perf_counter() > nextLoopAt:
                    print("Oops, missed an iteration")
                    nextLoopAt += N
                    continue

                # Otherwise, wait for next interval
                timeToSleep = nextLoopAt - time.perf_counter()
                nextLoopAt += N
                time.sleep(timeToSleep)
                loops += 1
                d += 1
        else:
            print("stopping data transmission...")
            self.data_transmitting = False


    def run(self):

        # Wait for a connection
        print('waiting for a connection')
        while self.program_running:
            # print('start loop')
            print(self.active_connections)
            try:
                readable_socks, writable_socks, errors = select.select(self.active_connections, [], [], 60)
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
                            client_connection, client_address = self.sock.accept()
                        except socket.error:
                            break
                        else:
                            self.active_connections.append(client_connection)
                            self.connected_client = True
                            print("New client found at (%s, %s)" % client_address)

                        try:
                            threading.Thread(target=self.receive, args=(client_connection, client_address)).start()
                        except:
                            print("error creating receive thread")

                            # try:
                            #     client_connection, client_address = self.sock.accept()
                            #     print("im here")
                            # except socket.error:
                            #     # print('could not connect to a client') # timeout needed??
                            #     continue
                            # else:
                            #     print('connection from', client_connection, "@", client_address)
                            #     self.active_connections.append(client_connection)
                            #     self.connected_client = True
                            #     break

        #close server socket
        self.sock.close()

if __name__ == '__main__':

    server = RobotServer()
    server_thread = threading.Thread(target=server.run)
    server_thread.start()

