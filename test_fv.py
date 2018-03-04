# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 18:40:21 2018

@author: ASUS
"""

import os
import pandas as pd

#TODO: Active links without prearchive stuff

#TODO: Active data from active links WITHOUT POSTFIX!!!


#team = "Videoton FC"

#res = pd.read_csv("test/hun.csv")
#res_2 =  res.loc[(res.HomeTeam == team) | (res.AwayTeam == team), :]
#print(res_2)

def get_prefix(filename):
    if "-" in filename:
        return filename.split("-")[0]
    else:
        return filename.split(".")[0]
#    return filename[0:3]

def merge_files(file1,file2, prefix):
    try:
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)
        
        df_final = df1.append(df2)
        df_final = df_final.sort_values(['Date', 'Time'], ascending=[True, True])
#        filename = "test/" + prefix + ".csv"
        df_final = df_final.drop_duplicates(keep='first')
#        print(len(df1), len(df2), len(df_final))

        df_final.to_csv(file1, sep=',', encoding='utf-8', index=False, float_format='%.0f')
#        os.remove(file1)
        os.remove(file2)
    except:
        None
        
def merge_all(iternum):
    folder = "data"                           
    for i in range(iternum): 
        filelist = os.listdir(folder)
        for i in range(len(filelist)-1):
            file1 = str(filelist[i])
            file2 = str(filelist[i + 1])
            if get_prefix(file1) == get_prefix(file2):
                merge_files(folder + "/" + file1, folder + "/" + file2, get_prefix(file1))
    filelist = os.listdir(folder)
    for i in range(len(filelist)):
        file = filelist[i]
        try:
            if file.endswith(".csv") == True and "-" in file:
                os.rename(folder + "/" + file,folder + "/" + get_prefix(file) + ".csv")
        except:
            None
        
#merge_all(10)               
