# -*- coding: utf-8 -*-
"""
Created on Sun May 21 12:04:43 2017

@author: ASUS
"""

import os
import pandas as pd
import datetime
import calendar
from lxml import html
from urllib.request import urlopen

def format_div(filename, country):
    filename = filename.replace("bundesliga","ger")
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

def get_result_letters(home,away):
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
    fulltime_letter = get_result_letters(fulltime[0], fulltime[1].strip())
    result_list = [fulltime[0], fulltime[1].strip(), int(fulltime[0]) + int(fulltime[1])]
    result_list.extend(fulltime_letter)
    if has_half_time and halftime.endswith(":") == False:
        halftime = halftime.split(":")
        halftime_letter = get_result_letters(halftime[0], halftime[1])
        result_list.extend((int(halftime[0]), int(halftime[1]), int(halftime[0]) + int(halftime[1])))
        result_list.extend(halftime_letter)
    elif (has_half_time == False and fulltime == ['0','0']):
        result_list.extend((0,0,0,"D","D","D"))
    else:
       result_list.extend(("","","","","",""))
       #result_list.extend((None,None,None,None,None,None))
    return result_list 


def store_data(result_df, dest):
    country = result_df.iat[0,0].split("-")[0]
    result_df['Date'] = pd.to_datetime(result_df['Date'], dayfirst = [True])
    filelist = os.listdir(dest)
    if country + ".csv" in filelist:
        old_df = pd.read_csv(dest + "/" + country + ".csv", low_memory=False)
        old_df['Date'] = pd.to_datetime(old_df['Date'], dayfirst = [True])
        res_df = result_df.append(old_df)
        res_df = res_df.sort_values(['Date', 'Time'], ascending=[True, True])
        res_df = res_df.drop_duplicates(subset=['Date','HomeTeam','AwayTeam'],keep='first')
        if len(res_df) != len(old_df):
            res_df.to_csv(dest + "/" + country + ".csv", sep=',', encoding='utf-8', index=False)
            # , float_format='%.0f'

    else:
        result_df = result_df.sort_values(['Date', 'Time'], ascending=[True, True])
        result_df.to_csv(dest + "/" + country + ".csv", sep=',', encoding='utf-8', index=False)

def get_results_old(url, where):
    index = 0    
    
    columns = ['Div','Round','Date','Time','timestamp','Weekday','HomeTeam','AwayTeam',
               'FTHG','FTAG','FTG','FTR', 'FTHR', 'FTAR',
               'HTHG','HTAG', 'HTG','HTR', 'HTHR', 'HTAR',
               'Report_url']
    result_df = pd.DataFrame(columns=columns)
    try:
        tree = html.parse(url)
        
        print(tree)
        table = tree.xpath('//table[contains(@class, "standard_tabelle")]')[0]
        country = tree.findall('//h1')[0].text_content().split("»")[0].strip()
        filename = url.replace("http://www.worldfootball.net/all_matches/","").replace("/","")
        div = format_div(filename, country)
        round_num = 0
        date = ""
        #filename = where + "/" + div + ".csv"
        tr = table.findall('tr')
        for i in tr:
            if len(i) == 1:
                round_num = i.text_content().strip().split(".")[0]
            else:
                report_url = ""
                td = i.findall('td')
                if td[0].text_content().strip() != "" and td[0].text_content().strip() != "00/00/0000":
                    date = td[0].text_content().strip()
                    date_day = date.split("/")
                    daytime = datetime.datetime(int(date_day[2]),int(date_day[1]), int(date_day[0]))
                    day = calendar.day_name[daytime.weekday()].lower()
                    
                time = td[1].text_content().strip()
                homeTeam = td[2].text_content().strip()
                awayTeam = td[4].text_content().strip()
                result = td[5].text_content().strip()
                if len(td[5].findall('a')) != 0:
                    report_url = "http://www.worldfootball.net" + td[5].findall('a')[0].xpath('@href')[0]
                    if len(td[5].findall('a')[0].findall('span')) > 0:
                        result = "-:-"
                if result != "-:-" and result != "dnp" and result.endswith(".") == False and result.endswith(":") == False:
                    date_loop = date.split("/")[2]+ date.split("/")[1]+date.split("/")[0]
                    if time == "":
                        timestamp = date_loop + "0000"
                    else:
                        timestamp = date_loop + time.replace(":","")
                    result = result.replace("(","|").replace(")","").replace(" pso","").replace(" aet","")
                    result = format_result(result)
                    
                    fthg, ftag, ftg, ftr, fthr, ftar, hthg, htag, htg, htr, hthr, htar = result
                    result_line_df = pd.DataFrame([[div, round_num, date, time, timestamp, day, homeTeam, awayTeam,\
                                                    fthg, ftag, ftg, ftr, fthr, ftar,\
                                                    hthg, htag, htg, htr, hthr, htar,\
                                                    report_url]], columns=columns, index = [index])
#                    result_line_df = pd.DataFrame([[div, round_num, date, time, timestamp, day, homeTeam, awayTeam,\
#                                                    fthg, ftag, str(ftg).split(".")[0], ftr, fthr, ftar,\
#                                                    str(hthg).split(":")[0], htag, str(htg).split(".")[0], htr, hthr, htar,\
#                                                    report_url]], columns=columns, index = [index])
                    index += 1
                    result_df = result_df.append(result_line_df)
        if result_df.empty is False:
            store_data(result_df,div)
    except:
        return 1


def generate_result_df(url,tree):
    country = tree.findall('//h1')[0].text_content().split("»")[0].strip()
    filename = url.replace("http://www.worldfootball.net/all_matches/","").replace("/","")
    div = format_div(filename, country)
    
    index = 0    
    columns = ['Div','Round','Date','Time','timestamp','Weekday','HomeTeam','AwayTeam',
               'FTHG','FTAG','FTG','FTR', 'FTHR', 'FTAR',
               'HTHG','HTAG', 'HTG','HTR', 'HTHR', 'HTAR',
               'Report_url']
    result_df = pd.DataFrame(columns=columns)
    
    table = tree.xpath('//table[contains(@class, "standard_tabelle")]')[0]
    round_num = 0
    date = ""
    tr = table.findall('tr')
    for i in tr:
        if len(i) == 1:
            round_num = i.text_content().strip().split(".")[0]
        else:
            report_url = ""
            td = i.findall('td')
            if td[0].text_content().strip() != "" and td[0].text_content().strip() != "00/00/0000":
                date = td[0].text_content().strip()
                date_day = date.split("/")
                daytime = datetime.datetime(int(date_day[2]),int(date_day[1]), int(date_day[0]))
                day = calendar.day_name[daytime.weekday()].lower()
                
            time = td[1].text_content().strip()
            homeTeam = td[2].text_content().strip()
            awayTeam = td[4].text_content().strip()
            result = td[5].text_content().strip()
            if len(td[5].findall('a')) != 0:
                report_url = "http://www.worldfootball.net" + td[5].findall('a')[0].xpath('@href')[0]
                if len(td[5].findall('a')[0].findall('span')) > 0:
                    result = "-:-"
            if result != "-:-" and result != "dnp" and result.endswith(".") == False and result.endswith(":") == False:
                date_loop = date.split("/")[2]+ date.split("/")[1]+date.split("/")[0]
                if time == "":
                    timestamp = date_loop + "0000"
                else:
                    timestamp = date_loop + time.replace(":","")
                result = result.replace("(","|").replace(")","").replace(" pso","").replace(" aet","")
                result = format_result(result)
                
                fthg, ftag, ftg, ftr, fthr, ftar, hthg, htag, htg, htr, hthr, htar = result
                result_line_df = pd.DataFrame([[div, round_num, date, time, timestamp, day, homeTeam, awayTeam,\
                                                fthg, ftag, str(ftg).split(".")[0], ftr, fthr, ftar,\
                                                hthg, htag, str(htg).split(".")[0], htr, hthr, htar,\
                                                report_url]], columns=columns, index = [index])
                index += 1
                result_df = result_df.append(result_line_df)
    return result_df

def get_results(url, dest):
    try:
#        tree = html.parse(url)
#        print(url)
        tree = html.parse(urlopen(url))
        
        result_df = generate_result_df(url, tree)
        
        if result_df.empty is False:
            store_data(result_df,dest)
    except:
        print("jajj")
        return 1


#url = "http://www.worldfootball.net/all_matches/wal-premier-league-2017-2018/"
#url = "http://www.worldfootball.net/all_matches/wal-premier-league-2003-2004/"
#url = "http://www.worldfootball.net/all_matches/usa-major-league-soccer-2017-playoffs/"
#url = "http://www.worldfootball.net/all_matches/usa-major-league-soccer-2016-playoffs/"
#url = "http://www.worldfootball.net/all_matches/usa-major-league-soccer-2015-playoffs/"
url = "https://www.worldfootball.net/all_matches/ita-serie-a-2017-2018/"
#url = "http://www.worldfootball.net/all_matches/eng-premier-league-2017-2018/"
#url = "http://www.worldfootball.net/all_matches/wm-1990-in-italien/"
#url = "http://www.worldfootball.net/all_matches/crc-primera-division-2009-2010-invierno/"


#tree = html.parse("http://www.origo.hu")

#tree = html.parse(urlopen(url))
#print(tree)
#get_results(url,"temp2")