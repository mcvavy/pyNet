#!/usr/bin/env python3

import os
import shlex
import subprocess
import time
import re


try:
    # nmap = subprocess.check_output("sudo nmap -sP 192.168.1.0/24 | awk '/^Nmap/{ip=$NF}/B8:27:EB/{print ip}'", shell=True)
    # nmap2 = subprocess.check_output("sudo nmap -sP 192.168.1.0/24 | awk '/^Nmap/'", shell=True)
    nmap3 = subprocess.check_output("sudo nmap -sP 192.168.1.0/24", shell=True).decode('utf-8')

    
    # p1 = subprocess.check_output("hostname -I", shell=True).decode('utf-8')
    # p1.wait()

    macAddress = subprocess.check_output("ifconfig | awk '/eth0/ { print toupper($5) }'", shell=True).decode('utf-8')
    # mac.wait()
    # stdo = p1.stdout.read().decode('utf-8')


    ipAddress = re.findall("([\d]+.[\d]+.[\d]+.[\d]+)",subprocess.check_output("hostname -I", shell=True).decode('utf-8'))

    print("This Node IP address is {} and MAC: {}".format(ipAddress[0], macAddress))
    # nmap = subprocess.check_output("sudo nmap -sP 192.168.1.0/24 | awk '/^Nmap/'", shell=True)

    pattern = "([\d]+.[\d]+.[\d]+.[\d]+)\nHost is up .*.\nMAC Address: ([0-9A-F:.]*) \((.*)\)\n"
    matches = re.findall(pattern,nmap3)

    listOfActivePIs = list(filter(lambda x: x[1].startswith('B8:27:EB'), matches))
    print("{} with the length of {}".format(listOfActivePIs, len(listOfActivePIs)))
except Exception  as e:
    print('nmam error')
    print("{}".format(str(e)))


# print("--------------------------------------------------")
# print("{}".format(nmap3))
