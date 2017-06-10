#!/usr/bin/env python3

'''This is the multithreaded UDP listener'''

import threading
import socket
import logging

class Listener():
    '''This class is responsible for sending and recieving messages'''

    def __init__(self, thisNode):
        logging.info('Initializing listener')
        self.thisNode = thisNode
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.thisNode.getIPAddress, 4242))

    def respond_to_client(self, ip):
        logging.info("Responding with 'ok' to %s", ip)
        self.sock.sendto("ok".encode("utf-8"), ip)

    def listen_clients(self):
        '''This listens for imcoming messages'''
        while True:
            msg, client = self.sock.recvfrom(1024)
            message = msg.decode("utf-8")
            if message == 'election':
                logging.info('Received data from client %s: %s', client, msg)
                print('Received data from client %s: %s', client, msg)
                send_thread = threading.Thread(target=self.respond_to_client, args=(client,))
                send_thread.start()

                #Kicks off election to higher hosts
                contestableHosts = list(filter(lambda x: int(x[0].split('.')[3]) > int(self.thisNode.getIPAddress.split('.')[3]), self.thisNode.getCurrentHosts))

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