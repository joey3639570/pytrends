# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 02:09:23 2019

@author: Joey Zhuang
"""

import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import numpy as np
import time
import random as rd
import module_grouping

geo_list = ['TW','US','']

# Login to Google. Only need to run this once, the rest of requests will use the same session.
# Return a pytrend object for you to call other function
def setup_pytrend():
    pytrend = TrendReq()
    return pytrend

# Get keywords from user, max input is 5, enter -1 to end input
# Return a keyword list.
def get_input():
    keyword_list = []
    num_keyword = 0
    for i in range(0,5):
        keyword = input("請輸入您的關鍵字，最多五個，輸入-1結束輸入 : ")
        keyword = [keyword]
        if(keyword !=  ['-1']):
            num_keyword += 1
            keyword_list.append(keyword[0])
            print(keyword[0], "added. Your list : ", keyword_list)
        else:
            break
    return keyword_list,num_keyword

# Get the asked geo from user, only choose from 'US, TW, World' now.
def select_geo():
    select = input("請選擇要搜尋的地區:\n - 台灣請輸入0\n - 美國請輸入1\n - 全世界請輸入2\n")
    select = int(select)
    geo = geo_list[select]
    return geo
'''
timeframe

Date to start from

Defaults to last 5yrs, 'today 5-y'.

Everything 'all'

Specific dates, 'YYYY-MM-DD YYYY-MM-DD' example '2016-12-14 2017-01-25'

Specific datetimes, 'YYYY-MM-DDTHH YYYY-MM-DDTHH' example '2017-02-06T10 2017-02-12T07'

Note Time component is based off UTC
Current Time Minus Time Pattern:

By Month: 'today #-m' where # is the number of months from that date to pull data for

For example: 'today 3-m' would get data from today to 3months ago
NOTE Google uses UTC date as 'today'
Seems to only work for 1, 2, 3 months only
Daily: 'now #-d' where # is the number of days from that date to pull data for

For example: 'now 7-d' would get data from the last week
Seems to only work for 1, 7 days only
Hourly: 'now #-H' where # is the number of hours from that date to pull data for

For example: 'now 1-H' would get data from the last hour
Seems to only work for 1, 4 hours only
'''
#Function for setting up timeframe , will return string.
def setup_timeframe():
    mode = input("- 註: 如果關鍵字較多，建議將搜尋時間範圍縮小一點。 -\n選擇你要搜尋的時間範圍:\n - 特定日期範圍輸入0\n - 幾個月內輸入1\n - 幾天內輸入2\n - 幾小時內輸入3\n - 全範圍請輸入4\n - 五年內請輸入5\n請輸入::")
    mode = int(mode)
    if mode == 0:
        output_string = input("輸入格式範例 2016-12-14 2017-01-25\n請輸入:")
    elif mode == 1:
        input_s = input("只能搜尋1,2,3個月內\n請輸入:")
        output_string = 'today ' + str(input_s) + '-m'
    elif mode == 2:
        input_s = input("只能搜尋1,7天內\n請輸入:")
        output_string = 'now ' + str(input_s) + '-d'
    elif mode == 3:
        input_s = input("只能搜尋1,4小時內\n請輸入:")
        output_string = 'now' + str(input_s) + '-h'
    elif mode == 4:
        output_string = 'all'
    else:
        output_string = "today 5-y"
    return output_string

'''
Basic function of pytrends, 
analyze the keyword by interest over time or region, 
and give you other suggestions of keywords.
Take input with pytrend_object, keyword_list, timeframe, geo.
return a pandas dataframe of interest over time and interest by region.
'''
def analyze(pytrend_object,keyword_list, timeframe, geo):
    #Build a payload
    pytrend_object.build_payload(keyword_list, cat=0, timeframe=timeframe, geo=geo, gprop='')
    
    # Interest Over Time
    interest_over_time_df = pytrend_object.interest_over_time()
    print("針對指定時間分析....")
    print(interest_over_time_df.head())
    
    # Interest by Region
    interest_by_region_df = pytrend_object.interest_by_region()
    print("針對指定地區分析....")
    print(interest_by_region_df.head())
    
    # Related Queries, returns a dictionary of dataframes
    related_queries_dict = pytrend_object.related_queries()
    print("相關關鍵字的搜尋關鍵字 ::")
    print(related_queries_dict)
    
    return interest_over_time_df, interest_by_region_df, related_queries_dict

# Take numpy array of the dataframe of iot and number of keyword.
# Output the picture of iot of keywords
def draw_iot(dataframe,num_keyword):
    nparray = dataframe.values
    head = dataframe.columns.values
    #Get the date
    idx = dataframe.index.tolist()
    #split is for putting the ticks in the x axis.
    split = np.array_split(idx,10)
    #ticks need location to put in.
    location = np.arange(len(nparray))
    loc_split = np.array_split(location,10)
    #Setting up the ticks should be put in.
    xticks_location = []
    xticks_list = []
    for i in range(0,10):
        xticks_location.append(loc_split[i][0])
        #print(xticks_location)
        xticks_list.append(split[i][0])
        #print(xticks_list)
    #Setting up the picture
    for i in range(0,num_keyword):
        draw = np.array([],np.int32)
        for j in range(0,len(nparray)):
            draw = np.hstack((draw,nparray[j][i]))
        plt.plot(draw, label=head[i])
    plt.title('Interest over Time')
    plt.legend()
    plt.xticks(xticks_location , xticks_list, rotation='vertical')
    plt.show()

#Trying to output histogram of ibr, not done yet.
'''
def draw_ibr(nparray,num_keyword,cities_list):
    print(nparray)
    for i in range(0,num_keyword):
        draw = np.array([],np.int32)
        for j in range(0,len(nparray)):
            draw = np.hstack((draw,nparray[j][i]))
            print(nparray[j][i])
        label_list = cities_list
        x = range(len(nparray))
        plt.xticks(label_list)
        plt.bar(left = x,height=draw)
        plt.show()
'''

# Take a dataframe as input, 
# Output the correlation coefficient of the data
def correlation(dataframe):
    dataframe = dataframe.drop(['isPartial'],axis=1)
    corr = dataframe.corr(method='pearson')
    return corr

# Get all related keyword into one list, need related queries dictionary to the input
def get_related_keyword(keyword_list, related_queries_dict):
    key_dict = {}
    for key in keyword_list:
        # There are rising keywords and top keywords in the related_queries_dict, I deicde to take both
        top = related_queries_dict[key]['top']
        #print(top)
        rising = related_queries_dict[key]['rising']
        #print(rising)
        # Only get the keyword out
        top_list = []
        if(top is None):
            top_list =[]
        else:
            top_list = top.loc[:,'query']
            top_list = top_list.tolist()
        rising_list = []
        if(rising is None):
            rising = []
        else:
            rising_list = rising.loc[:,'query']
            rising_list = rising_list.tolist() 
        #print(top_list)
        #print(rising_list)
        # Combining two list into one
        related_keyword = top_list + rising_list
        #print(related_keyword)
        # This part is for deleting replicated keyword
        related_keyword_list = list(set(related_keyword))
        #print(related_keyword_list)
        key_dict[key] = related_keyword_list  
    key_list = []
    for key in key_dict:
        key_list.append(key)
        for word in key_dict[key]:
            key_list.append(word)
    return key_list

def analyze_for_more_than_five(pytrend_object,keylist, timeframe, geo):
    df_dict = {}
    for key in keylist:
        keyword_list = [key]
        #Build a payload
        print("Analyzing keyword :: ", key)
        pytrend_object.build_payload(keyword_list, cat=0, timeframe=timeframe, geo=geo, gprop='')
        # Interest Over Time
        interest_over_time_df = pytrend_object.interest_over_time()
        print(interest_over_time_df[key].tolist())
        #print(key)
        df_dict[key] = interest_over_time_df[key].tolist()
    #print(df_dict)
    df = pd.DataFrame(df_dict)
    return df
        
    

def main():
    pytrend = setup_pytrend()
    kw_list,num_keyword = get_input()
    print("kw_list :: ", kw_list)
    geo = select_geo()
    print("Geo :: ", geo)
    timeframe = setup_timeframe()
    print("timeframe :: ", timeframe)
    iot, ibr, rqd = analyze(pytrend, kw_list, timeframe, geo)
    #print(iot.columns.values)
    #print(iot.index.tolist())
    #np_ibr = ibr.values
    print("----")
    print(kw_list)
    #key_list = get_related_keyword(kw_list,rqd)
    #draw_iot(iot,num_keyword)
    
    #print(ibr.index.tolist())
    #draw_ibr(np_ibr,num_keyword,ibr.index.tolist())
    """
    result = analyze_for_more_than_five(pytrend,key_list,timeframe,geo)
    corr = correlation(iot)
    print("Correlation ::\n",corr)
    corr_result = result.corr(method='pearson')
    print("Correlation Full ::\n",corr_result)
    """

if __name__ == '__main__':
    main()
