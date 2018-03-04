# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:11:57 2017

@author: ASUS
"""

import pandas as pd

#TODO: HT vs. FT goals

#TODO:Team names check

#TODO:

#TODO:

#TODO:

#TODO:

#TODO:





#assert 4 == 4

"""
offset = 5

filename = "tests/usa-2016.csv"
teams = []
block_letters = ""

results = pd.read_csv(filename)

for i in range(len(results)):
    team = results.iat[i,3]
    if team not in teams:
        teams.append(team)
        
teams = sorted(teams)

for team in teams:
    team_string = ""
    for i in range(len(results)):
        if results.iat[i,3] == team or results.iat[i,4] == team:
            team_string += results.iat[i,7]
    print team, team_string
    betweens = team_string.split("H")
    bet_lens = []
    for bet in betweens:
        bet_lens.append(len(bet))
    print max(bet_lens)

    for j in range(offset,len(team_string)):
        block = team_string[j-offset:j]
        print block, team_string[j]
        if "D" not in block:
            block_letters += team_string[j]
    print 
    
#print len(block_letters), block_letters.count("D")
    
"""