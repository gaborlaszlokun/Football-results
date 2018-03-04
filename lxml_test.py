# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 08:15:09 2018

@author: ASUS
"""

import pandas as pd
from lxml import html

url = "http://www.worldfootball.net/report/a-league-2017-2018-western-sydney-wanderers-perth-glory/"
url = "http://www.worldfootball.net/report/a-league-2017-2018-central-coast-mariners-melbourne-city-fc/"
url = "http://www.worldfootball.net/report/primera-division-2018-apertura-liverpool-fc-boston-river/"
url = "http://www.worldfootball.net/report/nb-i-2017-2018-ferencvarosi-tc-budapest-honved/"
url = "http://www.worldfootball.net/report/primera-division-2017-2018-ud-las-palmas-fc-barcelona/"
url = "http://www.worldfootball.net/report/nb-i-2017-2018-videoton-fc-budapesti-vasas/"

def halftime_res(table):
    home_goals = []
    away_goals = []
    tr = table.findall('tr')
    for i in tr:
        if len(i) > 1:
            minute = i.findall('td')[1].text_content().strip().split(".")[0].split(" ")[-1]
            if 'style' in i.findall('td')[1].attrib:
                if int(minute) < 46:
                    away_goals.append(minute)
            else:
                if int(minute) < 46:
                    home_goals.append(minute)
    print(len(home_goals), len(away_goals))
 
def goal_quartiles(table):
    None
    
def cards_sum(tree):
    yellow = len(tree.xpath('//img[contains(@title, "Yellow card")]'))
    yellow += len(tree.xpath('//img[contains(@title, "Second yellow card")]'))
    red = len(tree.xpath('//img[contains(@title, "Red card")]'))
    red += len(tree.xpath('//img[contains(@title, "Second yellow card")]'))
    print(yellow, red)

def get_attend(tree):
    if len(tree.xpath('//img[contains(@title, "Attendance")]')) > 0:
        attend = tree.xpath('//img[contains(@title, "Attendance")]/../..')[0].findall('td')[2].text_content().strip().replace(".","")
        print(attend)
        
tree = html.parse(url)
table = tree.xpath('//table[contains(@class, "standard_tabelle")]')[1]

#attend = tree.xpath('//img[contains(@title, "Attendance")]')[0].xpath('@src')[0]


halftime_res(table)
cards_sum(tree)
get_attend(tree)

#away_goal = tree.xpath('//td[contains(@style, "padding-left: 50px;")]')[0].text_content().strip()
#print(away_goal)
#h1 = tree.findall('//h1')[0].text_content()
#away_goal = tree.xpath('//td[contains(@style, "padding-left: 50px;")]')[0].text_content().strip()
#print(away_goal)


#table = tree.findall('//table')[1]
#table = tree.xpath('//table[contains(@class, "standard_tabelle")]')[0]

#
#round_num = 0
#tr = table.findall('tr')
#for i in tr:
#    if len(i) == 1:
#        round_num = i.text_content().strip()
#    else:
#        td = i.findall('td')
##        print(round_num)
##        print(td[0].text_content().strip())
##        print(td[1].text_content().strip())
##        print(td[2].text_content().strip())
##        print(td[4].text_content().strip())
##        print(td[5].text_content().strip())
#        if len(td[5].findall('a')) != 0:
#            link = td[5].findall('a')[0].xpath('@href')[0]
#            print(link)
#for i in tr:
#    if len(i) > 1:
#        td = i.findall('td')
#        print(td[0].text_content().strip())
#        print(td[1].text_content().strip())
#        print(td[2].text_content().strip())
#        print(td[4].text_content().strip())
#        print(td[5].text_content().strip())
#print(h1[0].text_content().strip())
#print(table.xpath('@class')[0])
 

       
"""        
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


def get_results(url, where):
    index = 0    
    
    columns = ['Div','Round','Date','Time','Weekday','HomeTeam','AwayTeam',
               'FTHG','FTAG','FTG','FTR', 'FTHR', 'FTAW',
               'HTHG','HTAG', 'HTG','HTR', 'HTHR', 'HTAR',
               'Report_url']
    result_df = pd.DataFrame(columns=columns)
    try:
        tree = html.parse(url)
        table = tree.xpath('//table[contains(@class, "standard_tabelle")]')[0]
        country = tree.findall('//h1')[0].text_content().split("»")[0].strip()
        filename = url.replace("http://www.worldfootball.net/all_matches/","").replace("/","")
        div = format_div(filename, country)
        round_num = 0
        date = ""
        filename = where + "/" + div + ".csv"
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
                    
                if result != "-:-" and result != "dnp" and result.endswith(".") == False and result.endswith(":") == False:
                    result = result.replace("(","|").replace(")","").replace(" pso","").replace(" aet","")
                    result = format_result(result)
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
    except:
        return 1
        
#url = "http://www.worldfootball.net/all_matches/wal-premier-league-2017-2018/"
#url = "http://www.worldfootball.net/all_matches/wal-premier-league-2003-2004/"
#url = "http://www.worldfootball.net/all_matches/usa-major-league-soccer-2017-playoffs/"
#url = "http://www.worldfootball.net/all_matches/usa-major-league-soccer-2016-playoffs/"
#url = "http://www.worldfootball.net/all_matches/usa-major-league-soccer-2015-playoffs/"
#url = "http://www.worldfootball.net/all_matches/ita-serie-a-2017-2018/"
#url = "http://www.worldfootball.net/all_matches/cze-1-fotbalova-liga-2017-2018/"
#url = "http://www.worldfootball.net/all_matches/por-superliga-2004-2005/"
#url = "http://www.worldfootball.net/all_matches/crc-primera-division-2017-2018-clausura"
#url = "http://www.worldfootball.net/all_matches/crc-primera-division-2009-2010-invierno/"
url = "http://www.worldfootball.net/all_matches/por-primeira-liga-2017-2018/"
#url = "http://www.worldfootball.net/all_matches/rou-liga-1-2017-2018-championship/"

get_results(url, "temp") 
"""