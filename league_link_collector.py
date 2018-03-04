# -*- coding: utf-8 -*-
"""
Created on Wed May 31 11:22:20 2017

@author: ASUS
"""

from result_collector import get_results
from test_fv import merge_all
from lxml import html
import datetime
from time import gmtime, strftime
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
#        print(link)
        if str(now) in link:
            if get_results(link,"data") == 1:
                error_num += 1
    merge_all(2)
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(date, error_num, "errors occured")
    print ("The script took", round(float(time.time() - startTime))," seconds!")
    


#get_all_links()    
#get_new_results()
