#!/usr/bin/env python3

"""This Class hold our funcational variables"""


__author__ = "Michael Oyibo"
__copyright__ = "Copyright 2017, Open Computing Enterprise Course"
__credits__ = ["Michael Oyibo"]
__version__ = "1.0.1"
__maintainer__ = "Michael Oyibo"
__email__ = "wi13b051@technikum-wien.at"
__status__ = "Development"
__Group__ = "Database"
__GroupMembers__ = "['Michael', 'Andreas', 'Linda']"


class Node(object):
    def __init__(self, myIP, myMAC, nodeList):
        self.myIP = myIP
        self.myMAC = myMAC
        self.nodeList = nodeList
        self.masterNode = []

    def add_node(self, newNode):
        #Add newly added node
        print("Adding host with   {}\n".format(newNode[0]))
        self.nodeList.append(newNode)


    def remove_node(self, xnode):
        #Remove node from node that is no longer active
        print("Removing host with {}\n".format(xnode[0]))
        self.nodeList.remove(xnode)

    def update_master_node(self, masterOctet):
        if self.myIP.split('.')[3] == str(masterOctet):
            self.masterNode = [self.myIP, self.myMAC.strip(), 'Raspberry Pi Foundation']
            print("My node is the master node {}\n".format(self.masterNode))
        else:
            masterNode = list(filter(lambda x: x[0][0].split('.')[3] == str(masterOctet), self.nodeList))
            self.masterNode = masterNode
            print("Master node has changed to {} with MAC address {}\n".format(masterNode[0], masterNode[1]))

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
        return self.nodeList

    @property
    def getMasterNode(self):
        return self.masterNode


# sudo nmap -sP 192.168.1.0/24 | awk '/^Nmap/{ip=$NF}/B8:27:EB/{print ip}'

