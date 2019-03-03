# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 18:40:21 2018

@author: ASUS
"""

import os
import pandas as pd

def get_row_stats(df):
    print("Total matches:", len(res))
    # Kiírja az utolsó sorozat hosszát (+1 a fogadáshoz kell)
    last_draw = len(res.FTR.to_string(index = False).replace("\n","").split("D")[-1]) + 1
    print("Last drawless row:", last_draw)
    # Kiírja a teljes df max hosszú D mentes sorozatának hosszát
    max_draw = len(max(res.FTR.to_string(index = False).replace("\n","").split("D"),key=len)) + 1
    print("Max drawless row:", max_draw)
    
    last_homeless = len(res.FTR.to_string(index = False).replace("\n","").split("H")[-1]) + 1
    print("Last homeless row:", last_homeless)
    max_homeless = len(max(res.FTR.to_string(index = False).replace("\n","").split("H"),key=len)) + 1
    print("Max homeless row:", max_homeless)
    
    last_awayless = len(res.FTR.to_string(index = False).replace("\n","").split("A")[-1]) + 1
    print("Last awayless row:", last_awayless)
    max_awayless = len(max(res.FTR.to_string(index = False).replace("\n","").split("A"),key=len)) + 1
    print("Max awayless row:", max_awayless)
    
    max_home = len(max(res.FTR.to_string(index = False).replace("\n","").replace("A","O").replace("D","O")\
                       .split("O"),key=len)) + 1
    print("Max home row:", max_home)
    
    max_away = len(max(res.FTR.to_string(index = False).replace("\n","").replace("H","O").replace("D","O")\
                       .split("O"),key=len)) + 1
    print("Max away row:", max_away)

"""
team = "Videoton FC"
res = pd.read_csv("data/hungary.csv")
res_2 =  res.loc[(res.HomeTeam == team) | (res.AwayTeam == team), :]
print(res_2.head())

# Generate a data frame here
for folder in os.listdir("data"):
    filename = "data/" + folder
#    print(folder)
    res = pd.read_csv(filename)
    # Kiírja az utolsó sorozat hosszát (+1 a fogadáshoz kell)
#    print(len(res.FTR.to_string(index = False).replace("\n","").split("D")[-1]) + 1)
    # Kiírja a teljes df max hosszú D mentes sorozatának hosszát
#    print(len(max(res.FTR.to_string(index = False).replace("\n","").split("D"),key=len)) + 1)
    teams = sorted(list(set(res.HomeTeam)))
    for team in teams:
        res_team =  res.loc[(res.HomeTeam == team) | (res.AwayTeam == team), :]
        print(team)
        print("Actual",len(res_team.FTR.to_string(index = False).replace("\n","").split("D")[-1]) + 1)
        print("Max",len(max(res_team.FTR.to_string(index = False).replace("\n","").split("D"),key=len)) + 1)
        print("Total", len(res_team))
        print()
""" 

country = "austria"
df = res = pd.read_csv("data/" + country + ".csv")       
get_row_stats(df)