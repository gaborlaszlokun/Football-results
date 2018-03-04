# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 17:44:06 2018

@author: ASUS
"""

import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime
import calendar


def format_div(filename, country):
    filename = filename.replace("bundesliga","ger")
#    new_filename = filename[:3]
    if filename[:3] != "eng":
        new_filename = country.lower()
    else:
        new_filename = "england"
    filename_arr = filename[3:].split("-")
    was_num = False
    for i in range(len(filename_arr)):
        if filename_arr[i].isdigit() and len(filename_arr[i]) == 4:
            new_filename += "-" + filename_arr[i]
            was_num = True
        elif was_num is True:
            new_filename += "-" + filename_arr[i]
    return new_filename

def get_result_letter(home,away):
    if home > away:
        return ("H","W","L")
    elif home < away:
        return ("A","L","W")
    else:
        return ("D","D","D")

def format_result(result):
    has_half_time = True
    if "|" in result:
        result = result.split("|")
        if "," not in result[1]:
            fulltime, halftime = result[:2]
        else:
            result = result[1].split(",")
            halftime, fulltime = result[:2]
    else:
        fulltime = result
        has_half_time = False
     
    fulltime = fulltime.strip()
    fulltime = fulltime.split(":")
    fulltime_letter = get_result_letter(fulltime[0], fulltime[1].strip())
    result_list = [fulltime[0], fulltime[1].strip(), int(fulltime[0]) + int(fulltime[1])]
    result_list.extend(fulltime_letter)
    if has_half_time and halftime.endswith(":") == False:
        halftime = halftime.split(":")
        halftime_letter = get_result_letter(halftime[0], halftime[1])
        result_list.extend((halftime[0], halftime[1], int(halftime[0]) + int(halftime[1])))
        result_list.extend(halftime_letter)
    elif (has_half_time == False and fulltime == ['0','0']):
        result_list.extend(('0','0','0',"D","D","D"))
#        result_list.extend(("D","D","D"))
    else:
       result_list.extend(("","","","","",""))
    return result_list 


def get_results(url, where, timeout_sec):
    index = 0    
    
    columns = ['Div','Round','Date','Time','Weekday','HomeTeam','AwayTeam',
               'FTHG','FTAG','FTG','FTR', 'FTHR', 'FTAW',
               'HTHG','HTAG', 'HTG','HTR', 'HTHR', 'HTAR',
               'Report_url']
    result_df = pd.DataFrame(columns=columns)
    try:
        usock = urlopen(url, timeout = timeout_sec)
        data = usock.read()
        usock.close()
    except:
        return 1
    
    soup = BeautifulSoup(data, 'html.parser')
    table= soup.findAll('table', { "class" : "standard_tabelle" })
    
    h1 = soup.findAll('h1')
    country = h1[0].getText().split("»")[0].strip()
    filename = url.replace("http://www.worldfootball.net/all_matches/","").replace("/","")
    div = format_div(filename, country)
    
    round_num = 0
    date = ""
    
    filename = where + "/" + div + ".csv"
    
    soup = BeautifulSoup(str(table[0]), 'html.parser')
    for i in range(1,len(table[0].contents),2):
        if len(table[0].contents[i]) == 3:
            round_num = table[0].contents[i].contents[1].string.split(".")[0]
        else:
            report_url = ""
            if table[0].contents[i].contents[1].string != None and table[0].contents[i].contents[1].string != "00/00/0000":
                date = table[0].contents[i].contents[1].string
                date_day = date.split("/")
                daytime = datetime.datetime(int(date_day[2]),int(date_day[1]), int(date_day[0]))
                day = calendar.day_name[daytime.weekday()].lower()
            time = table[0].contents[i].contents[3].getText()
            homeTeam = table[0].contents[i].contents[5].string
            awayTeam = table[0].contents[i].contents[9].string
            result = table[0].contents[i].contents[11].getText().strip()
            if result != "-:-" and result != "dnp" and result.endswith(".") == False and result.endswith(":") == False:
                result = result.replace("(","|").replace(")","").replace(" pso","").replace(" aet","")
                result = format_result(result)
                if len(table[0].contents[i].contents[11].contents) == 3\
                and table[0].contents[i].contents[11].contents[1].has_attr('href'):
                        report_url = "http://www.worldfootball.net" + table[0].contents[i].contents[11].contents[1]['href']
                fthg, ftag, ftg, ftr, fthr, ftar, hthg, htag, htg, htr, hthr, htar = result
                result_line_df = pd.DataFrame([[div, round_num, date, time, day, homeTeam, awayTeam,\
                                                fthg, ftag, str(ftg).split(".")[0], ftr, fthr, ftar,\
                                                hthg, htag, str(htg).split(".")[0], htr, hthr, htar,\
                                                report_url]], columns=columns, index = [index])
                index += 1
                result_df = result_df.append(result_line_df)
    if result_df.empty is False:
        result_df['Date'] = pd.to_datetime(result_df['Date'], dayfirst = [True])
        result_df = result_df.sort_values(['Date', 'Time'], ascending=[True, True])
        result_df.to_csv(filename, sep=',', encoding='utf-8', index=False)
            
        
#url = "http://www.worldfootball.net/all_matches/wal-premier-league-2017-2018/"
url = "http://www.worldfootball.net/all_matches/wal-premier-league-2003-2004/"
#url = "http://www.worldfootball.net/all_matches/usa-major-league-soccer-2017-playoffs/"
#url = "http://www.worldfootball.net/all_matches/usa-major-league-soccer-2016-playoffs/"
#url = "http://www.worldfootball.net/all_matches/usa-major-league-soccer-2015-playoffs/"
#url = "http://www.worldfootball.net/all_matches/ita-serie-a-2017-2018/"
#url = "http://www.worldfootball.net/all_matches/cze-1-fotbalova-liga-2017-2018/"
#url = "http://www.worldfootball.net/all_matches/por-superliga-2004-2005/"
url = "http://www.worldfootball.net/all_matches/crc-primera-division-2017-2018-clausura"
url = "http://www.worldfootball.net/all_matches/crc-primera-division-2009-2010-invierno/"
url = "http://www.worldfootball.net/all_matches/por-primeira-liga-2017-2018/"


get_results(url, "temp", 20)     
        
        
        
       
     
        
        
        
        
#    for j in range(1,len(table[0].contents[i].contents),2):
#        print(table[0].contents[i].contents[j]) # HINT: here how you can get the name of attr.
    

#print(soup.findAll(id="wac_fill_me"))
#print(soup.findAll(align="right"))

#soup = BeautifulSoup(data,"html.parser")   
#table= soup.findAll('table', { "class" : "standard_tabelle" }) 

#print( table[0].contents)

#soup = BeautifulSoup(str(table[0]),"html.parser")
#tr =  soup.findAll('tr')
#soup = BeautifulSoup(str(tr[1]),"html.parser")
#td = table= soup.findAll('td')
#print(td[0].string)

#base_url ="http://www.worldfootball.net"
#final_urls = ""
#
#usock = urlopen(base_url)
#data = usock.read()
#usock.close()     
#soup = BeautifulSoup(data,"html.parser")
#countries = soup.findAll('a', { "class" : "special" })
#for i in countries:
#    country_url = base_url + str(i['href'])
#    usock = urlopen(country_url)
#    data = usock.read()
#    usock.close()     
#    soup = BeautifulSoup(data,"html.parser")
#    schedule = soup.findAll('div', { "class" : "mehr_links" })
#    schedule_url = base_url + schedule[0].contents[0]['href']
#    usock = urlopen(schedule_url)
#    data = usock.read()
#    usock.close()     
#    soup = BeautifulSoup(data,"html.parser")
#    seasons = soup.findAll('option')
#    for j in seasons:
#        if "all_matches" in j['value']:
#            final_url = base_url + str(j['value']) + "\n"
#            print(final_url)
#            final_urls += final_url
#text = open("league_links.txt", "w")
#text.write(final_urls)
#text.close()