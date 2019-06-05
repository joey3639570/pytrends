# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 02:09:23 2019

@author: Joey Zhuang
"""

import pandas as pd
from pytrends.request import TrendReq

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
    for i in range(0,5):
        keyword = input("請輸入您的關鍵字，最多五個，輸入-1結束輸入 : ")
        keyword = [keyword]
        if(keyword !=  ['-1']):
            keyword_list.append(keyword[0])
            print(keyword[0], "added. Your list : ", keyword_list)
        else:
            break
    return keyword_list

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
    mode = input("選擇你要搜尋的時間範圍:\n - 特定日期範圍輸入0\n - 幾個月內輸入1\n - 幾天內輸入2\n - 幾小時內輸入3\n - 全範圍請輸入4\n - 五年內請輸入5\n請輸入::")
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
    
    return interest_over_time_df, interest_by_region_df

def main():
    pytrend = setup_pytrend()
    kw_list = get_input()
    print("kw_list :: ", kw_list)
    geo = select_geo()
    print("Geo :: ", geo)
    timeframe = setup_timeframe()
    print("timeframe :: ", timeframe)
    iot, ibr = analyze(pytrend, kw_list, timeframe, geo)

if __name__ == '__main__':
    main()