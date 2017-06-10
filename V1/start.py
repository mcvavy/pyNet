#!/usr/bin/env python3

"""This is a Raspberry network scanner application"""

import os
import shlex
import subprocess
import time
import re
from Node import *


__author__ = "Michael Oyibo"
__copyright__ = "Copyright 2017, Open Computing Enterprise Course"
__credits__ = ["Michael Oyibo"]
__version__ = "1.0.1"
__maintainer__ = "Michael Oyibo"
__email__ = "wi13b051@technikum-wien.at"
__status__ = "Development"
__Group__ = "Database"
__GroupMembers__ = "['Michael', 'Andreas', 'Linda']"



def initialize():
    """This function initializes the application"""
    thisNode = Node(fetch_IP_address(), fetch_MAC_address(), scanHosts())
    print("This Node IP is {} and MAC is {}\n".format(thisNode.getIPAddress, thisNode.getMACAddress))

    # thisNode.fetch_master_node();

    while(True):
        #Let's run two iterations
        # for i in range(2):
        # print("Running nmap Iteration: {}\n\n".format(str(i+1)))
        try:

            print("Scanning for new hosts............\n")
            newHostScans = scanHosts()
        except subprocess.CalledProcessError as e:
            print('nmam error')
            time.sleep(60*5)
            continue



        """ Looping through the newly scanned hosts"""
        #Check if each host in the new list is in our current list
        for host in newHostScans:
            if host not in thisNode.getCurrentHosts:
                thisNode.add_node(host)

        """Ping all addresses on our list to check if they are alive or dead"""
        for host in thisNode.getCurrentHosts:
            if command_executor(host[0]) == '':
                thisNode.remove_node(host)

        """Check for new master who's in town"""
        thisNode.fetch_master_node()

        #Wait 5 seconds before next scan
        time.sleep(5)

        print("Current Master is Node with IP: {} ,  MAC: {}, Vendor: {}\n\n".format(thisNode.getMasterNode[0],thisNode.getMasterNode[1],thisNode.getMasterNode[2]))
        print("Current live hosts are {}\n\n".format(thisNode.getCurrentHosts))

def scanHosts(): #We will scan for hosts every 5 seconds
    """This function scans for hosts on the network"""
    nmap3 = subprocess.check_output("sudo nmap -sP 192.168.1.0/24", shell=True).decode('utf-8')
    matches = re.findall("([\d]+.[\d]+.[\d]+.[\d]+)\nHost is up .*.\nMAC Address: ([0-9A-F:.]*) \((.*)\)\n",nmap3)
    listOfLiveHost = list(filter(lambda x: x[1].startswith('B8:27:EB'), matches))
    return listOfLiveHost

def fetch_MAC_address():
    return subprocess.check_output("ifconfig | awk '/eth0/ { print toupper($5) }'", shell=True).decode('utf-8')

def fetch_IP_address():
    return re.findall("([\d]+.[\d]+.[\d]+.[\d]+)",subprocess.check_output("hostname -I", shell=True).decode('utf-8'))[0]

def command_executor(ipAddress):
    return subprocess.check_output("nmap "+ ipAddress + " | awk '/Host is up/{ print $1, $2, $3 }'", shell=True).decode('utf-8')


    
if __name__== '__main__':
    initialize()