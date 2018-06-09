# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 18:40:21 2018

@author: ASUS
"""

import os
import pandas as pd

res = pd.read_csv("data/spain.csv")
# Kiírja az utolsó sorozat hosszát (+1 a fogadáshoz kell)
print(len(res.FTR.to_string(index = False).replace("\n","").split("D")[-1]) + 1)
# Kiírja a teljes df max hosszú D mentes sorozatának hosszát
print(len(max(res.FTR.to_string(index = False).replace("\n","").split("D"),key=len)) + 1)

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