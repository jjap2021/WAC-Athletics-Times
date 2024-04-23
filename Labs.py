#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 15:04:21 2024

@author: mm
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
df = pd.read_csv('/home/mm/Downloads/CleanDataLab.csv')
df.replace({'Lab Days': {'TH': 'R', 'TTH': 'TR'}}, inplace=True)
print(df)
df[['Start', 'End']] = df['Lab Start-End'].str.split('-', n=1, expand=True)
#df['Lengths'] = pd.date_range(start=pd.to_datetime(df.Start), end=pd.to_datetime(df.End), freq='5min')
datelist=[]
print(df['Start'].dtypes)
#assert df.iloc[1,df.columns.get_loc('Start')] == None
for x in df.index: 
    starttime = df.iloc[x,df.columns.get_loc('Start')]
    endtime = df.iloc[x,df.columns.get_loc('End')]
    if type(starttime) != float:
        datelist.append(pd.date_range(start=starttime, end=endtime, freq='5min').strftime("%H:%M").tolist() )
    else:
        datelist.append("/")
df['Lengths'] =  datelist 
alltimes=[]
d = {'time': []}
timespan_df = pd.DataFrame(data=d)
for classtime in df.Lengths:
    for period in classtime:
        alltimes.append(period)
timespan_df['time']=alltimes
timesums = timespan_df['time'].value_counts().rename_axis('times').reset_index(name='counts')
timesums.drop((timesums[(timesums.times == '/')].index), inplace=True)

df['Lab Days'].fillna('X', inplace=True)
for weekday in ['M','T','W','R','F']:
    day_df = df[df['Lab Days'].str.contains(weekday)]
    day_df.reset_index(inplace=True)
#df['Lengths'] = pd.date_range(start=pd.to_datetime(df.Start), end=pd.to_datetime(df.End), freq='5min')
    datelist=[]
    print(day_df['Start'])
#assert df.iloc[1,df.columns.get_loc('Start')] == None
    for x in day_df.index: 
        starttime = day_df.iloc[x,day_df.columns.get_loc('Start')]
        endtime = day_df.iloc[x,day_df.columns.get_loc('End')]
        if type(starttime) != float:
            datelist.append(pd.date_range(start=starttime, end=endtime, freq='5min').strftime("%H:%M").tolist() )
        else:
            datelist.append("/")
    day_df['Lengths'] =  datelist 
    alltimes=[]
    d = {'time': []}
    timespan_df = pd.DataFrame(data=d)
    for classtime in day_df.Lengths:
        for period in classtime:
            alltimes.append(period)
    timespan_df['time']=alltimes
    timesums_day = timespan_df['time'].value_counts().rename_axis('times').reset_index(name=weekday)
    timesums_day.drop((timesums[(timesums.times == '/')].index), inplace=True)
    timesums = pd.concat([timesums, timesums_day[weekday]], axis=1)
    timesums.sort_values(['times'], inplace=True)
print(df.sort_values(['End'], inplace=True))
fig, axes = plt.subplots(5, figsize=(15, 15), sharex=True, sharey=True)
for _, day in enumerate(['M','T','W','R','F']):
    g = sns.barplot(timesums, x='times', y=day, ax=axes[_])
axes[3].xaxis.set_major_locator(ticker.IndexLocator(base=6, offset=0))
axes[3].xaxis.set_minor_locator(ticker.LinearLocator(165))
plt.xticks(rotation=45)
plt.show()
    
    
