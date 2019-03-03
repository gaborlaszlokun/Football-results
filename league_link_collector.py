# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:22:20 2017

@author: ASUS
"""

from result_collector import get_results
from lxml import html
import datetime
from time import localtime, strftime, sleep
import time
import os
from urllib.request import urlopen

def get_all_links():
    base_url ="http://www.worldfootball.net"
    final_urls = ""
    tree = html.parse(urlopen(base_url))
    countries = tree.xpath('//a[contains(@class, "special")]')
    for i in countries:
        country_url = base_url + i.xpath('@href')[0]
        tree = html.parse(country_url)
        tree = html.parse(urlopen(country_url))
        schedule = tree.xpath('//div[contains(@class, "mehr_links")]')
        schedule_url = base_url + schedule[0].findall('a')[0].xpath('@href')[0]
        tree = html.parse(schedule_url)
        seasons = tree.findall('//option')
        for j in seasons:
            if 'value' in j.attrib:
                if "all_matches" in j.xpath('@value')[0]:
                    final_url = base_url + j.xpath('@value')[0] + "\n"
                    final_urls += final_url
    text = open("league_links.txt", "w")
    text.write(final_urls)
    text.close()

#HINT: possibly useless
def replace_zeros():
    for folder in os.listdir("temp"):
        filename = "temp/" + folder
        f = open(filename, 'r', encoding="utf8")
        cont = f.read()
        f.close()
        if ".0" in cont:
            print(filename)
            cont = cont.replace(".0","")
            f = open(filename, 'w', encoding="utf8")
            f.write(cont)
            f.close()

# Collects active or archive data from worldfootball.com
def collect(only_active):
    try:
        startTime = time.time()
        error_num = 0
        this_year = int(datetime.datetime.now().year)
        base_url ="http://www.worldfootball.net"
        tree = html.parse(urlopen(base_url))
        countries = tree.xpath('//a[contains(@class, "special")]')
        for i in countries:
            country_url = base_url + i.xpath('@href')[0]
            try:
                tree = html.parse(urlopen(country_url))
                schedule = tree.xpath('//div[contains(@class, "mehr_links")]')
                link = base_url + schedule[0].findall('a')[0].xpath('@href')[0]
                if only_active is True and str(this_year) in link:
                    if get_results(link,"data") == 1:
                        error_num += 1
            
                elif only_active is False:
                    schedule_url = base_url + schedule[0].findall('a')[0].xpath('@href')[0]
                    tree = html.parse(urlopen(schedule_url))
                    seasons = tree.findall('//option')
                    for j in seasons:
                        if 'value' in j.attrib:
                            if "all_matches" in j.xpath('@value')[0]:
                                link = base_url + j.xpath('@value')[0]
                                if get_results(link,"temp") == 1:
                                    error_num += 1

            except:
                print("Failed to open", country_url)
        
        #replace_zeros()
        
        date = strftime("%Y-%m-%d %H:%M:%S", localtime())
        print(date, error_num, "errors occured")
        print ("The collector script took", round(float(time.time() - startTime))," seconds!")
    except:
        date = strftime("%Y-%m-%d %H:%M:%S", localtime())
        print(date, "Network error!")
        sleep(60)   
        
#collect(only_active=False)

#replace_zeros()

#get_all_links()    
#get_new_results()
#get_archive_results()
