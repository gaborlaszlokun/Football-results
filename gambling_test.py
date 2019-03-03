# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 13:59:57 2019

@author: ASUS
"""

import pandas as pd

country = "poland"

total_res = pd.read_csv("data/" + country + ".csv", encoding="utf-8", low_memory=False)


for season, res_season in total_res.groupby('Div'):
#    res_season['index'] = res_season.index.values
    if len(res_season) > 100:
        print()
        print(season)
        print(len(res_season))
        print("Total A:",(res_season.FTR.to_string(index = False).replace("\n","")).count("A"))
        print(res_season.FTR.value_counts(normalize=True))
        print(list(len(item) for item in (res_season.FTR.to_string(index = False).replace("\n","").replace("D","").split("A")) if len(item) > 2))
#    home_and_draw = int((1 - res_season.FTR.value_counts(normalize=True)['A'])*100)
#    print(res_season.FTR.to_string(index = False).replace("\n","").replace("D",""))
#    print(home_and_draw, "%")
#    print(len(max(res_season.FTR.to_string(index = False).replace("\n","").replace("D","").split("H"),key=len)) + 1)
#    print(len(max(res_season.FTR.to_string(index = False).replace("\n","").replace("H","D").split("D"),key=len)) + 1)
#    print("Win:", res_season.FTR.value_counts()['H'] * 100)
    



    #res_team =  res.loc[(res.HomeTeam == team) | (res.AwayTeam == team), :]
    # Split full database by years
    
        #print(res_season.FTG.rolling(5).sum())
        #res_season['sumgoals'] = res_season.FTG.rolling(5).sum().shift()
#        res_season['index'] = res_season.index.values
        #print(res_season[:10])
        
        
        



#res = total_res.loc[(total_res.Div == "england-2017-2018")]
#res['index'] = res.index.values

#evaluate_all(res, 5)