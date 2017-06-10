#!/usr/bin/env python3

'''This is the multithreaded UDP listener'''

import threading
import socket
import logging

class Listener():
    '''This class is responsible for sending and recieving messages'''

    def __init__(self, thisNode):
        logging.info('Initializing Broker')
        self.thisNode = thisNode
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.thisNode.getIPAddress, 4242))
        # self.clients_list = []

    def talkToClient(self, ip):
        logging.info("Sending 'ok' to %s", ip)
        self.sock.sendto("ok".encode("utf-8"), ip)

    def listen_clients(self):
        '''This listens for imcoming messages'''
        while True:
            msg, client = self.sock.recvfrom(1024)
            message = msg.decode("utf-8")
            if message == 'election':
                logging.info('Received data from client %s: %s', client, msg)
                print('Received data from client %s: %s', client, msg)
                send_thread = threading.Thread(target=self.talkToClient, args=(client,))
                send_thread.start()

                #Kicks off election to higher hosts
                contestableHosts = list(filter(lambda x: int(x[0].split('.')[3]) > int(self.thisNode.getIPAddress.split('.')[3]), self.thisNode.getCurrentHosts))

                if len(contestableHosts) >= 1:
                    for host in contestableHosts:
                        propagate_election_thread = threading.Thread(target=self.send_contest_request, args=("election", (host[0], 4242)))
                        propagate_election_thread.start()
                # else:
                #     #update master and broadcast
                #     self.thisNode.update_master_node(self.thisNode.getIPAddress.split('.')[3])
                #     self.broadcast_master()

            else:
                logging.info("Master Node with IP Address: % has been found\n", client)
                print("I think the master node is {}".format(client))
                self.thisNode.update_master_node(client[0].split('.')[3])
                # self.thisNode.update_master_node(self.thisNode.getIPAddress.split('.')[3])
                self.broadcast_master()

    def broadcast_master(self):
        '''Broadcast the master to all nodes'''
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.sendto("master".encode("utf-8"), (self.thisNode.getBroadcastAddress, 4242))

    def send_contest_request(self, message, address):
        self.sock.sendto(message.encode("utf-8"), address)