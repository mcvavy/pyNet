#!/usr/bin/env python3

"""This Class hold our funcational variables"""

import logging

__credits__ = [""]
__version__ = "2.0.1"
__maintainer__ = "Michael Oyibo, Andreas Wenzl"
__email__ = "wi13b051@technikum-wien.at"
__status__ = "Development"
__Group__ = "Database"
__GroupMembers__ = "['Michael', 'Andreas Wenzl', 'Linda']"


class Node(object):
    '''This class holds our business variables related to a host'''

    def __init__(self, myIP, myMAC, myBroadCastIP, nodeList):
        logging.info('Starting application........')
        self.myIP = myIP
        self.myMAC = myMAC
        self.broadCastIP = myBroadCastIP
        self.nodeList = nodeList
        self.masterNode = []

    def add_node(self, newNode):
        '''Add newly added node'''
        print("New host(s) detected....   {}\n".format(newNode[0]))
        print("**************************************************************\n")
        print("Adding host with {}\n".format(newNode[0]))
        self.nodeList.append(newNode)

    def update_ip_address(self, ipAddress):
        'Updating ip address in case it changes while the programm is running'
        self.myIP = ipAddress

    def remove_node(self, xnode):
        '''Remove node from node that is no longer active'''
        print("Dead/faulty host detected\n")
        print("**************************************************************\n")
        print("Removing host with {}\n".format(xnode[0]))
        self.nodeList.remove(xnode)

    def update_master_node(self, masterOctet):
        if self.myIP.split('.')[3] == str(masterOctet):
            self.masterNode = [self.myIP, self.myMAC.strip(), 'Raspberry Pi Foundation']
            print("My node is the master node {}\n".format(self.masterNode))
        else:
            masterNode = list(filter(lambda x: x[0].split('.')[3] == str(masterOctet), self.nodeList))[0]
            self.masterNode = list(masterNode)
            print("Master node has changed to {} with MAC address {}\n".format(self.masterNode[0], self.masterNode[1]))

    def fetch_master_node(self):
        lastOctetOfPis = list(map(lambda x: x[0].split('.')[3], self.nodeList))
        lastOctetOfPis.append(self.myIP.split('.')[3])

        #Node selection for master happens here
        self.update_master_node(max(list(map(int, lastOctetOfPis))))

    @property
    def getIPAddress(self):
        return self.myIP

    @property
    def getMACAddress(self):
        return self.myMAC

    @property
    def getCurrentHosts(self):
        '''returns list of all host on the list'''
        return self.nodeList

    @property
    def getMasterNode(self):
        '''returns the current master node'''
        return self.masterNode

    @property
    def getBroadcastAddress(self):
        '''returns the broadcast address'''
        return self.broadCastIP
