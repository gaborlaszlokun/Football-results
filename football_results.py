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
from test_fv import merge_all
import time



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
        #HINT: print the bad links
        error_num += 1
        print(links[i])
#    if i % 10 == 0 and i != 0:
#        merge_all(10)
#    print(i)

date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
if error_num == len(links):
    print(date, "Network error")
    sleep(60)
else:
    print(date, error_num, "errors occured")
print ('The script took {0} minutes !'.format(time.time() - startTime))
merge_all(150)
"""