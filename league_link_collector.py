# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:22:20 2017

@author: ASUS
"""

from result_collector import get_results
from lxml import html
import datetime
from time import gmtime, strftime, sleep
import time

def get_all_links():
    base_url ="http://www.worldfootball.net"
    final_urls = ""
    tree = html.parse(base_url)
    countries = tree.xpath('//a[contains(@class, "special")]')
    for i in countries:
        country_url = base_url + i.xpath('@href')[0]
        tree = html.parse(country_url)
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

def get_new_results():
    try:
        startTime = time.time()
        error_num = 0
        now = int(datetime.datetime.now().year)
        base_url ="http://www.worldfootball.net"
        tree = html.parse(base_url)
        countries = tree.xpath('//a[contains(@class, "special")]')
        for i in countries:
            country_url = base_url + i.xpath('@href')[0]
            tree = html.parse(country_url)
            schedule = tree.xpath('//div[contains(@class, "mehr_links")]')
            link = base_url + schedule[0].findall('a')[0].xpath('@href')[0]
            if str(now) in link:
                if get_results(link,"data") == 1:
                    error_num += 1
                    #print(link)
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print(date, error_num, "errors occured")
        print ("The collector script took", round(float(time.time() - startTime))," seconds!")
    except:
        date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print(date, "Network error!")
        sleep(300)
        

def get_archive_results():
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
    print(date, error_num, "errors occured")
    print ('The script took {0} seconds !'.format(time.time() - startTime))
    


#get_all_links()    
#get_new_results()
#get_archive_results()
