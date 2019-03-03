# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 14:58:29 2018

@author: ASUS
"""

import pandas as pd
from lxml import html
import datetime
from result_collector import get_results

#TODO: longest D sequence from a file OR description of D sequences (mean, median, max, etc)

#TODO: longest any sequence from a file

#TODO: behaviour of long D sequences (?)

#TODO:

#TODO:

#TODO:

#TODO:

#TODO:

#TODO:

only_active = True
this_year = int(datetime.datetime.now().year)
base_url ="http://www.worldfootball.net"
tree = html.parse(base_url)
countries = tree.xpath('//a[contains(@class, "special")]')
for i in countries:
    country_url = base_url + i.xpath('@href')[0]
    try:
        tree = html.parse(country_url)
        schedule = tree.xpath('//div[contains(@class, "mehr_links")]')
        link = base_url + schedule[0].findall('a')[0].xpath('@href')[0]
        if only_active is True and str(this_year) in link:
            print(link)
            get_results(link,"data")
    except:
        print("Failed to open", country_url)