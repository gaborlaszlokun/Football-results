# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:37:39 2017

@author: ASUS
"""

# C:\Users\ASUS\Anaconda3\python.exe football_results.py
import sys

from league_link_collector import collect

if __name__ == "__main__":
    if sys.argv[1] == "True" or sys.argv[1] == "False":
        if sys.argv[1] == "True":
            while(True):  
                collect(only_active=True)
        elif sys.argv[1] == "False":
            while(True):  
                collect(only_active=False)
    else:
        print("Invalid parameter error. Try to use boolean value!")
