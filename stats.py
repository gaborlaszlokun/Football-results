# -*- coding: utf-8 -*-
"""
Created on Sun Aug 06 12:10:58 2017

@author: ASUS
"""

import pandas as pd
import numpy as np
import os
import math


def make_letter_list(result):
    result_letters = ""
    for i in range(0,len(result)):
        result_letters += result.iat[i,7]
    letter_arr = result_letters.split("D")
    return letter_arr

def get_period_lens(letter_arr):
    period_lens = []
    for period in letter_arr:
       period_lens.append(len(period))
    return period_lens

def get_last_period(filename):
    result = pd.read_csv(filename)
    letter_arr = make_letter_list(result)
    return len(letter_arr[-1])

def get_max_period(filename):
   result = pd.read_csv(filename)
   letter_arr = make_letter_list(result)
   period_lens = get_period_lens(letter_arr)
   return max(period_lens)

def get_median(filename):
    result = pd.read_csv(filename)
    letter_arr = make_letter_list(result)
    period_lens = get_period_lens(letter_arr)
    return math.ceil(np.median(period_lens))


def get_active_stats():
    
    index = 0
    columns = ['Country','MaxPeriod','LastPeriod','Median']
    stats_df = pd.DataFrame(columns=columns)
    
    #TODO: add csv generator and graph(s)
    for folder in os.listdir("data"):
        for file in os.listdir("active/" + str(folder)):
            filename = "active/" + str(folder) + "/" + str(file)
            
            stat_line_df = pd.DataFrame([[folder, get_max_period(filename), get_last_period(filename), get_median(filename)]], columns=columns, index = [index])
            index += 1
            stats_df = stats_df.append(stat_line_df)
            
            if get_last_period(filename) > 5:
                print('\x1b[6;30;42m', folder, get_max_period(filename), get_last_period(filename), get_median(filename),'\x1b[0m') 
#            else:
#                print('\x1b[6;30;41m' ,folder, get_max_period(filename), get_last_period(filename), get_median(filename),'\x1b[0m') 
    print (stats_df.MaxPeriod.value_counts().sort_index())

#<3 This Much! <3
def get_archive_stats(country):
    for folder in os.listdir("archive"):
        for file in os.listdir("archive/" + str(folder)):
            filename = "archive/" + str(folder) + "/" + str(file)
            if ".csv" in filename and country in filename:
                print (filename, get_max_period(filename))
#                print(sorted(get_period_lens(make_letter_list(pd.read_csv(filename)))))
                print()
  

def get_all_archive_stats():
    for file in os.listdir("test/" ):
        filename = "test/" + str(file)
        print(filename, get_max_period(filename))
#                print(sorted(get_period_lens(make_letter_list(pd.read_csv(filename)))))
        print()   

get_all_archive_stats()           
#get_archive_stats("POL")
#get_active_stats()        