import pandas as pd
from pytrends.request import TrendReq

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

#Insert your keyword here
'''
keywords=["Trump","Tawian","64","89","天安門",]
'''
'''
plist = []
for keyword in keywords:
    print(keyword)
    keywords_list = [keyword]
    pytrend.build_payload(keywords_list, cat=0, timeframe='today 5-y',geo='TW',gprop='')
    interest_over_time_df = pytrend.interest_over_time()
    print(interest_over_time_df)
    plist.append(keyword)
'''
keyword = input("請輸入您的關鍵字:")
keyword = [keyword]
while keyword != "-1":
    #Setup payload, geo can be assign to the specific region
    pytrend.build_payload(keyword, cat=0, timeframe='today 5-y',geo='TW',gprop='')
    
    # Interest Over Time
    interest_over_time_df = pytrend.interest_over_time()
    print("這是台灣近五年搜尋熱度 :")
    print(interest_over_time_df.head())
    
    # Interest by Region
    interest_by_region_df = pytrend.interest_by_region()
    print("這是台灣地區針對此關鍵字的搜尋熱度地區分布 :")
    print(interest_by_region_df.head())
    
    # Related Queries, returns a dictionary of dataframes
    related_queries_dict = pytrend.related_queries()
    print("這是台灣地區相關此關鍵字的搜尋關鍵字 ::")
    print(related_queries_dict)
    
    keyword = input("請輸入您的關鍵字:")
    keyword = [keyword]

'''
# Get Google Hot Trends data
trending_searches_df = pytrend.trending_searches()
print(trending_searches_df.head())

# Get Google Hot Trends data
today_searches_df = pytrend.today_searches()
print(today_searches_df.head())

# Get Google Top Charts
top_charts_df = pytrend.top_charts(2018, hl='en-US', tz=300, geo='GLOBAL')
print(top_charts_df.head())

# Get Google Keyword Suggestions
suggestions_dict = pytrend.suggestions(keyword='Trump')
print(suggestions_dict)
'''