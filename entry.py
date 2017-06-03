#!/usr/bin/env python3

import os
import time
from main import *
from multiprocessing import Process

def main():
  one = Process(target=FindPi('192.168.1.*/24').nmap_awk_results())  
  one.start()

  # two = Process(target=FindPi('172.17.1.*/24').nmap_awk_results())
  # two.start()

  # three = Process(target=FindPi('172.17.0.*/24').nmap_awk_results())
  # three.start()

  # four = Process(target=FindPi('172.16.1.*/24').nmap_awk_results())
  # four.start()

  # five = Process(target=FindPi('172.16.0.*/24').nmap_awk_results())
  # five.start()
 

  one.join()
  # two.join()
  # three.join()
  # four.join()
  # five.join()
  
if __name__== '__main__':
  main()

