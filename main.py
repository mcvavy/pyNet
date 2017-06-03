#!/usr/bin/env python3

import os
import shlex
import subprocess
import time
import re
from Node import *


try:

    nmap3 = subprocess.check_output("sudo nmap -sP 192.168.1.0/24", shell=True).decode('utf-8')

    macAddress = subprocess.check_output("ifconfig | awk '/eth0/ { print toupper($5) }'", shell=True).decode('utf-8')

    ipAddress = re.findall("([\d]+.[\d]+.[\d]+.[\d]+)",subprocess.check_output("hostname -I", shell=True).decode('utf-8'))[0]
    print("This Node IP address is {} and MAC: {}".format(ipAddress, macAddress))

    matches = re.findall("([\d]+.[\d]+.[\d]+.[\d]+)\nHost is up .*.\nMAC Address: ([0-9A-F:.]*) \((.*)\)\n",nmap3)

    listOfActivePIs = list(filter(lambda x: x[1].startswith('B8:27:EB'), matches))
    # print("{} with the length of {}".format(listOfActivePIs, len(listOfActivePIs)))

    thisNode = Node(ipAddress, macAddress, listOfActivePIs)
    thisNode.fetch_master_node();


except Exception  as e:
    print('nmam error')
    print("{}".format(str(e)))
