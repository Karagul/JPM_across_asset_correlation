# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 09:44:31 2016

@author: ZFang


1- change currency order
2- refine YTD MTD QTD return
3- change the format value(return)


"""
from datetime import datetime
import pandas_datareader.data as wb
from fredapi import Fred
import pandas as pd
import numpy as np
from itertools import groupby
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime, timedelta
import plotly.plotly as py
from plotly.graph_objs import *
import dateutil.relativedelta
import urllib.request
import ast
import math
import string


    
'''
    last_year = datetime.today().replace(month=1,day=1)-dateutil.relativedelta.relativedelta(days=1)
    price.columns[price.isnull().values[0]]
    price = wb.DataReader(equity_index_list,'yahoo',last_year,last_year)['Adj Close']

    price = wb.DataReader(equity_index_list,'yahoo',last_year-dateutil.relativedelta.relativedelta(days=2),last_year-dateutil.relativedelta.relativedelta(days=2))['Adj Close']
'''




    
def get_price(tickerlist):
    # get all datetime
    # end = datetime.today()-dateutil.relativedelta.relativedelta(days=1)
    last_day = datetime.today()-dateutil.relativedelta.relativedelta(days=1)
    last_last_day = datetime.today()-dateutil.relativedelta.relativedelta(days=2)
    last_month = datetime.today().replace(day=1)-dateutil.relativedelta.relativedelta(days=1)
    q = math.ceil(datetime.today().month/3)-1
    last_quarter = datetime.today().replace(month=q*3+1,day=1)-dateutil.relativedelta.relativedelta(days=1)
    last_year = datetime.today().replace(month=1,day=1)-dateutil.relativedelta.relativedelta(days=1)
    # start = last_year - dateutil.relativedelta.relativedelta(days=1)
    date_list = [last_day,last_last_day,last_month,last_quarter,last_year]
    # pull the data
    
    
    # collect a new dataframe for return calculation
    price_cal_df= pd.DataFrame([])
    for d in date_list:
        price_cal_df = pd.concat([price_cal_df,check_empty(tickerlist,d)])
        
    # price_cal_df = price_cal_df.interpolate()
    # Change column name
    price_cal_df = add_column_name(price_cal_df)
    return price_cal_df  
    
def add_column_name(dataframe):
    l = []
    for i in dataframe.columns:
        l.append(ticker_dict[i])
    dataframe.columns = l
    return dataframe    
    
def get_return(df):
    return_df = pd.DataFrame(np.zeros([5,9]),index=['T','DTD','MTD','QTD','YTD'],columns=df.columns)
    return_df.iloc[0,:] = round(100*(df.iloc[0,:]-df.iloc[0,:])/df.iloc[0,:],2)
    return_df.iloc[1,:] = round(100*(df.iloc[0,:]-df.iloc[1,:])/df.iloc[1,:],2)
    return_df.iloc[2,:] = round(100*(df.iloc[0,:]-df.iloc[2,:])/df.iloc[2,:],2)
    return_df.iloc[3,:] = round(100*(df.iloc[0,:]-df.iloc[3,:])/df.iloc[3,:],2)
    return_df.iloc[4,:] = round(100*(df.iloc[0,:]-df.iloc[4,:])/df.iloc[4,:],2)
    return return_df
    
    
def check_empty(tickerlist,date):
    i = 1
    price = wb.DataReader(tickerlist,'yahoo',date,date)['Adj Close']
    while price.isnull().values.any():
        target = price.columns[price.isnull().values[0]]
        for i in target:
            j=1
            while price[i].isnull().values[0]:
                price[i] = wb.DataReader(i,'yahoo',date-dateutil.relativedelta.relativedelta(days=j),date-dateutil.relativedelta.relativedelta(days=j))['Adj Close'].values[0]
                j=j+1

    return price
    
    
    
def get_currency_price():
    # get all datetime
    last_day = datetime.strftime(datetime.today()-dateutil.relativedelta.relativedelta(days=1),'%Y-%m-%d')
    last_last_day = datetime.strftime(datetime.today()-dateutil.relativedelta.relativedelta(days=2),'%Y-%m-%d')
    last_month = datetime.strftime(datetime.today().replace(day=1)-dateutil.relativedelta.relativedelta(days=1),'%Y-%m-%d')
    q = math.ceil(datetime.today().month/3)-1
    last_quarter = datetime.strftime(datetime.today().replace(month=q*3+1,day=1)-dateutil.relativedelta.relativedelta(days=1),'%Y-%m-%d')
    last_year = datetime.strftime(datetime.today().replace(month=1,day=1)-dateutil.relativedelta.relativedelta(days=1),'%Y-%m-%d')
    date_list = [last_day,last_last_day,last_month,last_quarter,last_year]

    # Pull the data and do return calculation
    currency_df = pd.DataFrame([])
    for i in range(len(date_list)):
        with urllib.request.urlopen('http://api.fixer.io/%s?base=USD' %date_list[i]) as f:
            currency_dict = ast.literal_eval(f.read().decode('utf-8'))
            currency_df = pd.concat([currency_df,pd.DataFrame.from_dict(currency_dict['rates'],'index')], axis=1)
    currency_df.columns = ['Last_Day','Last_Last_Day','Last_Month','Last_Quarter','Last_Year']
    currency_df['dtd'] = round((currency_df['Last_Day']-currency_df['Last_Last_Day'])/currency_df['Last_Last_Day'],4)
    currency_df['mtd'] = round((currency_df['Last_Day']-currency_df['Last_Month'])/currency_df['Last_Month'],4)
    currency_df['qtd'] = round((currency_df['Last_Day']-currency_df['Last_Quarter'])/currency_df['Last_Quarter'],4)
    currency_df['ytd'] = round((currency_df['Last_Day']-currency_df['Last_Year'])/currency_df['Last_Year'],4)
    
    return currency_df
    
    
    
currency_df = get_currency_price() 


       
if __name__ == '__main__':
    equity_index_list = ['^GSPC','^N225','^SSEC','^FTSE','^HSI','^BVSP','^AORD','^GDAXI','^BSESN']
    currency_list = ['FXY','FXB','FXE','FXA','FXCH']
    
    ticker_dict = {'FXY':'JPY/USD','FXB':'GBP/USD','FXE':'EUR/USD','FXA':'AUD/USD','FXCH':'CHY/USD','BZF':'BRL/USD',
         '^GSPC':'S&P500','^N225':'Nikki_225','^SSEC':'SSE_Composite','^FTSE':'FTSE_100','^HSI':'HANG_SENG_INDEX',\
         '^BVSP':'IBOVESPA','^AORD':'ALL_ORDINARIES','^GDAXI':'DAX','^BSESN':'S&P_BSE_SENSEX',\
         'XLY':'Consumer Discretionary','XLP':'Consumer Staples','XLE':'Energy','XLF':'Financials',\
         'XLV':'Health Care','XLI':'Industrials','XLB':'Materials','XLRE':'Real Estate','XLK':'Technology','XLU':'Utilities'}
         

    ###### Equity Index Return ######
    print('It starts')
    zzz = get_price(equity_index_list)
    print('It ends')
    zzz_df = get_return(zzz)
    zzz_str =  zzz_df.applymap(str)

    ###### Currency ######     
    currency_df = get_currency_price() 
        
    ###### Concat the data ######      
    a=[]
    for i,p,j,k,l,m in zip(zzz.columns,zzz.iloc[0,:],zzz_str.ix['DTD'],zzz_str.ix['MTD'],zzz_str.ix['QTD'],zzz_str.ix['YTD']):
        a.append(i+': '+str(round(p,2))+'('+j+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+k+'%/'+l+'%/'+m+'%')
    a[0] = a[0]+'<br>'+'AUD/USD: '+str(round(1/currency_df.loc['AUD','Last_Day'],2))+'('+str(-100*currency_df.loc['AUD','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(-100*currency_df.loc['AUD','mtd'])+'%/'+str(-100*currency_df.loc['AUD','qtd'])+'%/'+str(-100*currency_df.loc['AUD','ytd'])+'%'
    a[1] = a[1]+'<br>'+'USD/INR: '+str(round(currency_df.loc['INR','Last_Day'],2))+'('+str(100*currency_df.loc['INR','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['INR','mtd'])+'%/'+str(100*currency_df.loc['INR','qtd'])+'%/'+str(100*currency_df.loc['INR','ytd'])+'%'
    a[2] = a[2]+'<br>'+'USD/BRL: '+str(round(currency_df.loc['BRL','Last_Day'],2))+'('+str(100*currency_df.loc['BRL','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['BRL','mtd'])+'%/'+str(100*currency_df.loc['BRL','qtd'])+'%/'+str(100*currency_df.loc['BRL','ytd'])+'%'
    a[3] = a[3]+'<br>'+'GBP/USD: '+str(round(1/currency_df.loc['GBP','Last_Day'],2))+'('+str(-100*currency_df.loc['GBP','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(-100*currency_df.loc['GBP','mtd'])+'%/'+str(-100*currency_df.loc['GBP','qtd'])+'%/'+str(-100*currency_df.loc['GBP','ytd'])+'%'
    a[4] = a[4]+'<br>'+'EUR/USD: '+str(round(1/currency_df.loc['EUR','Last_Day'],2))+'('+str(-100*currency_df.loc['EUR','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(-100*currency_df.loc['EUR','mtd'])+'%/'+str(-100*currency_df.loc['EUR','qtd'])+'%/'+str(-100*currency_df.loc['EUR','ytd'])+'%'
    a[6] = a[6]+'<br>'+'USD/HKD: '+str(round(currency_df.loc['HKD','Last_Day'],2))+'('+str(100*currency_df.loc['HKD','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['HKD','mtd'])+'%/'+str(100*currency_df.loc['HKD','qtd'])+'%/'+str(100*currency_df.loc['HKD','ytd'])+'%'
    a[7] = a[7]+'<br>'+'USD/JPY: '+str(round(currency_df.loc['JPY','Last_Day'],2))+'('+str(100*currency_df.loc['JPY','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['JPY','mtd'])+'%/'+str(100*currency_df.loc['JPY','qtd'])+'%/'+str(100*currency_df.loc['JPY','ytd'])+'%'
    a[8] = a[8]+'<br>'+'USD/CNY: '+str(round(currency_df.loc['CNY','Last_Day'],2))+'('+str(100*currency_df.loc['CNY','dtd'])+'%)'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['CNY','mtd'])+'%/'+str(100*currency_df.loc['CNY','qtd'])+'%/'+str(100*currency_df.loc['CNY','ytd'])+'%'
    

    py.sign_in('fzn0728', '1enskD2UuiVkZbqcMZ5K')
    '''
    Equity_Return = {
      "hoverinfo": "text+name", 
      "lat": [-33.8688, 19.0760, -23.5505, 51.5074, 52.5200, 40.7128, 22.3964, 35.6895, 39.9042, 47.3769],
      "lon": [151.2093, 72.8777, -46.6333, -0.1278, 13.4050, -74.0059, 114.1095, 139.6917, 116.4074, 8.5417],
      "marker":{
          "color":"rgb(255, 70, 70)",
          "size":["15","15","15","15","15","15","15","15","15","15"],
          "opacity":[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]
                },
      "text":['ALL_ORDINARIES:<br>0.35%','S&P_BSE_SENSEX:<br>-0.05%','IBOVESPA:<br>1.20%','FTSE_100:<br>-0.12%','DAX:<br>-0.38%',\
      'S&P500:<br>0.77%','HANG_SENG_INDEX:<br>2.05%<br>USD/HKD:<br>7.7548','Nikki_225:<br>1.65%','SSE_Composite:<br>0.22%','ESTX50:<br>0.03%'],
      "name":'Equity Index',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    '''
    label_color = "rgb(0, 215, 0)"

    Australia = {
      "hoverinfo": "text+name", 
      "lat": [-33.8688],
      "lon": [151.2093],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[0],
      "name":'Australia',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    India = {
      "hoverinfo": "text+name", 
      "lat": [19.0760],
      "lon": [72.8777],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[1],
      "name":'India',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    Brazil = {
      "hoverinfo": "text+name", 
      "lat": [-23.5505],
      "lon": [-46.6333],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[2],
      "name":'Brazil',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    UK = {
      "hoverinfo": "text+name", 
      "lat": [51.5074],
      "lon": [-0.1278],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[3],
      "name":'UK',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    Germany = {
      "hoverinfo": "text+name", 
      "lat": [52.5200],
      "lon": [13.4050],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[4],
      "name":'Germany',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    US = {
      "hoverinfo": "text+name", 
      "lat": [40.7128],
      "lon": [-74.0059],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[5],
      "name":'US',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    Hong_Kong = {
      "hoverinfo": "text+name", 
      "lat": [22.3964],
      "lon": [114.1095],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[6],
      "name":'Hong Kong',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }


    Japan = {
      "hoverinfo": "text+name", 
      "lat": [35.6895],
      "lon": [139.6917],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[7],
      "name":'Japan',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }
    Shanghai = {
      "hoverinfo": "text+name", 
      "lat": [39.9042],
      "lon": [116.4074],
      "marker":{
          "color":label_color,
          "size":"15",
          "opacity":0.5
                },
      "text":a[8],
      "name":'Hong Kong',
      "mode": "markers", 
      "type": "scattergeo", 
      "uid": "2f55b6"
    }

    
    '''
    trace1 = {
      "text": ['Australia','India','Brazil','United Kingdom','Germany','United States of America','China','Japan'],
      "locations": ["AUS","IND","BRA","GBR","DEU","USA","CHN","JPN",], 
      "type": "scattergeo", 
      "uid": "b73666", 
      "name":""
    }
    '''
    
    Country_index = {
      "z": ['7','8','6','5','4','1','2','3'],
      "text": ['Australia','India','Brazil','United Kingdom','Germany','United States of America','China','Japan'],
      "colorscale": [[0.0, "rgb(255,0,0)"], [0.2, "rgb(255,255,0)"], [0.4, "rgb(128,255,0)"],\
                      [0.6, "rgb(0,255,64)"],[0.8, "rgb(0,255,255)"], [1.0, "rgb(0,128,192)"]], 
      "locations": ["AUS","IND","BRA","GBR","DEU","USA","CHN","JPN"], 
      "type": "choropleth", 
      "uid": "b73666", 
      "showscale": False,
      "name":"Country Index",
      "zmax":"9",
      "zmin":"1"
    }
    
    
    
    data = Data([Australia, India, Brazil, UK, Germany, US, Hong_Kong, Japan, Shanghai, Country_index])
    layout = {
      "autosize": True, 
      "geo": {
        "countrywidth": 0.5, 
        "lakecolor": "rgb(129, 145, 254)", 
        "landcolor": "rgb(40, 23, 255)", 
        "lataxis": {
          "gridcolor": "rgb(102, 102, 102)", 
          "gridwidth": 0.5, 
          "showgrid": True
        }, 
        "lonaxis": {
          "gridcolor": "rgb(102, 102, 102)", 
          "gridwidth": 0.5, 
          "showgrid": True
        }, 
        "oceancolor": "rgb(214, 207, 209)", 
        "projection": {
          "rotation": {
            "lat": 40, 
            "lon": -100, 
            "roll": 0
          }, 
          "type": "orthographic"
        }, 
        "showcountries": True, 
        "showlakes": True, 
        "showland": True, 
        "showocean": True
      }, 
      "height": 400, 
      "margin": {
        "r": 100, 
        "t": 100, 
        "b": 100, 
        "l": 100
      }, 
      "showlegend": True, 
      "title": "Global Index Performance", 
      "width": 500
    }
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig)