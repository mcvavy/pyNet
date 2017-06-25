#!/usr/bin/env python3

"""This is a Raspberry network scanner application"""

import subprocess
import time
import re
from Node import Node
from listener import *
import threading
import logging

__credits__ = [""]
__version__ = "2.0.0"
__maintainer__ = "Michael Oyibo"
__email__ = "wi13b051@technikum-wien.at"
__status__ = "Development"
__Group__ = "Database"
__GroupMembers__ = "['Michael', 'Andreas Wenzl', 'Linda']"



def initialize():
    """This function initializes the application"""

    #Gather information about the current device and display it
    thisNode = Node(fetch_IP_address(), fetch_MAC_address(), fetch_broadcast_address(), scanHosts())
    print("My IP is {} and MAC is {}\n".format(thisNode.getIPAddress, thisNode.getMACAddress))

    #Register this device as a listener for incoming messages
    listener = Listener(thisNode)

    #Election of a master node
    begin_election_process(thisNode, listener)

    #Initialises threads for scanning devices and messaging
    scanner_thread = threading.Thread(target=network_scanner, args=(thisNode,listener))
    listener_thread = threading.Thread(target=network_listener, args=(listener,))

    #start scanning and listener threads
    scanner_thread.start()
    listener_thread.start()

def network_listener(listener):
    '''Thread to forever listen and send messages'''
    listener.client_listener()

def network_scanner(thisNode, listener):
    '''Thread to forever loop scanning the network'''
    while True:
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

        '''Check if master is alive/dead then raise election requests'''
        if not thisNode.getMasterNode:
            begin_election_process(thisNode, listener)
        else:
            if command_executor(thisNode.getMasterNode[0]) == '':
            #We kickoff election contest
                begin_election_process(thisNode, listener)

        if command_executor(thisNode.getIPAddress) == '':
            thisNode.update_ip_address(fetch_IP_address())
            begin_election_process(thisNode, listener)

        time.sleep(5)

        if thisNode.getMasterNode:
            print("Current Master is Node with IP: {} ,  MAC: {}, Vendor: {}\n\n".format(thisNode.getMasterNode[0],thisNode.getMasterNode[1],thisNode.getMasterNode[2]))
        print("Current live hosts are {}\n\n".format(thisNode.getCurrentHosts))

def begin_election_process(thisNode, listener):
    '''The Bully Election Algorithm begins'''
    #We kickoff election contest
    contest_election_thread = threading.Thread(target=contest_election, args=(thisNode,listener))
    contest_election_thread.start()

def contest_election(thisNode, listener):
    #A list of contestable nodes in the network i.e Nodes with higher last IP octet on the network
    contestableHosts = list(filter(lambda x: int(x[0].split('.')[3]) > int(thisNode.getIPAddress.split('.')[3]), thisNode.getCurrentHosts))

    process_election(contestableHosts, listener, thisNode)

def process_election(contestableHosts, listener, thisNode):
    #Sending a request for election if at least one node with higher last octet is available
    if len(contestableHosts) >= 1:
        for host in contestableHosts:
            propagate_election_thread = threading.Thread(target=listener.send_contest_request, args=("election", (host[0], 4242)))
            propagate_election_thread.start()
    else:
        #update master and broadcast information no other node with higher last IP octet or is the only available node
        thisNode.update_master_node(thisNode.getIPAddress.split('.')[3])

        broadcast_master_to_all = threading.Thread(target=listener.broadcast_master, args=("master".encode("utf-8"),))
        broadcast_master_to_all.start()


def scanHosts(): #We will scan for hosts every 5 seconds
    """This function scans for hosts on the network"""
    nmap3 = subprocess.check_output("sudo nmap -sP 192.168.1.0/24", shell=True).decode('utf-8')
    matches = re.findall("([\d]+.[\d]+.[\d]+.[\d]+)\nHost is up .*.\nMAC Address: ([0-9A-F:.]*) \((.*)\)\n",nmap3)
    listOfLiveHost = list(filter(lambda x: x[1].startswith('B8:27:EB'), matches))
    return listOfLiveHost

def fetch_MAC_address():
    """This function returns MAC address"""
    return subprocess.check_output("ifconfig | awk '/eth0/ { print toupper($5) }'", shell=True).decode('utf-8')

def fetch_IP_address():
    """This function returns IP address"""
    return re.findall("([\d]+.[\d]+.[\d]+.[\d]+)",subprocess.check_output("hostname -I", shell=True).decode('utf-8'))[0]

def command_executor(ipAddress):
    """This function pings a node to check if dead or alive"""
    return subprocess.check_output("nmap "+ ipAddress + " | awk '/Host is up/{ print $1, $2, $3 }'", shell=True).decode('utf-8')

def fetch_broadcast_address():
    """This function fetches the broadcast address of the current host"""
    return subprocess.check_output("ifconfig | awk '/Bcast:/ {split($3,arr,\":\"); print arr[2]}'", shell=True).decode('utf-8')


if __name__== '__main__':
    if subprocess.check_output("nmap | awk '/nmap -v -A/{print $4}'", shell=True).decode('utf-8') == '':
        print("Updating packages and installing nmap..........\n\n")
        subprocess.call("(sudo apt-get update -y)", shell=True)
        subprocess.call("(sudo apt-get install nmap -y)", shell=True)

    initialize()
