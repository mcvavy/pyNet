#!/usr/bin/env python3

'''This is the multithreaded UDP listener'''

import threading
import socket
import logging


__credits__ = [""]
__version__ = "1.0.1"
__maintainer__ = "Michael Oyibo"
__email__ = "wi13b051@technikum-wien.at"
__status__ = "Development"
__Group__ = "Database"
__GroupMembers__ = "['Michael', 'Andreas', 'Linda']"

class Listener():
    '''This class is responsible for sending and recieving messages'''

    def __init__(self, thisNode):
        logging.info('Initializing listener')
        self.thisNode = thisNode
        #Using a UDP socket for catching incoming packets from hosts
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #Binding the socket to a port
        self.sock.bind((self.thisNode.getIPAddress, 4242))

    def respond_to_client(self, ip):
        #Sending response
        logging.info("Responding with 'ok' to %s", ip)
        self.sock.sendto("ok".encode("utf-8"), ip)

    def client_listener(self):
        '''This listens for imcoming messages'''
        while True:
            #Receiving UDP messages with a buffer size of 1024 bytes
            msg, client = self.sock.recvfrom(1024)
            message = msg.decode("utf-8")
            if message == 'election':
                logging.info('Received data from client %s: %s', client, msg)
                print('Election request from {}\n\n'.format(client))
                send_thread = threading.Thread(target=self.respond_to_client, args=(client,))
                send_thread.start()

                #Kicks off election to higher hosts
                contestableHosts = list(filter(lambda x: int(x[0].split('.')[3]) > int(self.thisNode.getIPAddress.split('.')[3]), self.thisNode.getCurrentHosts))

                #Sending a request for election when more than one host apply for master
                if len(contestableHosts) >= 1:
                    for host in contestableHosts:
                        propagate_election_thread = threading.Thread(target=self.send_contest_request, args=("election", (host[0], 4242)))
                        propagate_election_thread.start()
                else:
                    #update master and broadcast
                    self.thisNode.update_master_node(self.thisNode.getIPAddress.split('.')[3])
                    for host in self.thisNode.getCurrentHosts:
                        self.sock.sendto("master".encode("utf-8"), client)

            if message == 'master':
                logging.info("Master Node with IP Address: % has been found\n", client)
                self.thisNode.update_master_node(client[0].split('.')[3])

    def broadcast_master(self, message, host):
        '''Broadcast the master to all nodes'''
        self.sock.sendto(message, host)


    def send_contest_request(self, message, address):
        '''Broadcast the master to all nodes'''
        self.sock.sendto(message.encode("utf-8"), address)
