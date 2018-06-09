# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:37:39 2017

@author: ASUS
"""

# C:\Users\ASUS\Anaconda3\python.exe football_results.py

#from lxml_test import get_results
from result_collector import get_results
from league_link_collector import get_new_results
from time import gmtime, strftime, sleep
import time

if __name__ == "__main__":
    while(True):
        get_new_results()

"""

startTime = time.time()

idx = 0

t = open("league_links.txt", "r") 
links = t.read()
t.close()
links = links.split("\n")

error_num = 0
for i in range(idx,len(links)):
    if get_results(links[i],"data") == 1:
        error_num += 1
        #TODO: strore it to somewhere
        print(links[i])

date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
if error_num == len(links):
    print(date, "Network error")
    sleep(60)
else:
    print(date, error_num, "errors occured")
print ('The script took {0} seconds !'.format(time.time() - startTime))
"""