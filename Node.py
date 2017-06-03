#!/usr/bin/env python3

import datetime

__author__ = "Michael Oyibo"
__copyright__ = "Copyright 2017, Open Computing Enterprise Course"
__credits__ = ["Michael Oyibo"]
__version__ = "1.0.1"
__maintainer__ = "Michael Oyibo"
__email__ = "wi13b051@technikum-wien.at"
__status__ = "Development"


class Node(object):
    def __init__(self, myIP, myMAC, nodeList):
        self.myIP = myIP
        self.myMAC = myMAC
        self.nodeList = nodeList
        self.masterNode = ''

    def add_node(self):
        #Add newly added node
        pass


    def remove_node(self):
        #Remove node from node that is no longer active
        pass

    def update_master_node(self, masterOctet):
        if self.myIP.split('.')[3] == str(masterOctet):
            self.masterNode = [self.myIP, self.myMAC.strip(), 'Raspberry Pi Foundation']
            # print("I am the master!! {}".format(self.masterNode))
        else:
            masterNode = list(filter(lambda x: x[0][0].split('.')[3] == str(masterOctet), self.nodeList))
            self.masterNode = masterNode
            # print("Master node is {}".format(masterNode))

    def fetch_master_node(self):
        lastOctetOfPis = list(map(lambda x: x[0].split('.')[3], self.nodeList))
        lastOctetOfPis.append(self.myIP.split('.')[3])

        # print("Last octet of all node are {}".format(lastOctetOfPis))
        #Node selection for master happens here

        self.update_master_node(max(list(map(int, lastOctetOfPis))))

        # print("Highest IP is  {}".format(max(list(map(int, lastOctetOfPis)))))

    def getIPAddress(self):
        return self.myIP

    def getMACAddress(self):
        return self.myMAC

