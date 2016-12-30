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
import dateutil.relativedelta

def get_return(tickerlist):
    end = datetime.today() - timedelta(days=1)
    start = end - dateutil.relativedelta.relativedelta(months=12)
    p = wb.DataReader(tickerlist,'yahoo',start,end)
    price_df = p['Adj Close']
    price_df = price_df.interpolate()
    
    
    dtd_price_df = price_df.shift(1)
    mtd_price_df = price_df.shift(21)
    qtd_price_df = price_df.shift(63)
    ytd_price_df = price_df.shift(252)
    
    
    return_df_dtd = (price_df - dtd_price_df)/dtd_price_df
    return_df_mtd = (price_df - mtd_price_df)/mtd_price_df
    return_df_qtd = (price_df - qtd_price_df)/qtd_price_df
    return_df_ytd = (price_df - ytd_price_df)/ytd_price_df

    return_df_dtd = add_column_name(return_df_dtd)
    return_df_mtd = add_column_name(return_df_mtd)
    return_df_qtd = add_column_name(return_df_qtd)
    return_df_ytd = add_column_name(return_df_ytd)
    return return_df_dtd,return_df_mtd,return_df_qtd,return_df_ytd

    

def add_column_name(dataframe):
    l = []
    for i in dataframe.columns:
        l.append(ticker_dict[i])
    dataframe.columns = l
    return dataframe
       
if __name__ == '__main__':
    equity_index_list = ['^GSPC','^N225','^SSEC','^FTSE','^HSI','^BVSP','^AORD','^GDAXI','^BSESN']
    currency_list = ['FXY','FXB','FXE','FXA','FXCH']
    
    ticker_dict = {'FXY':'JPY/USD','FXB':'GBP/USD','FXE':'EUR/USD','FXA':'AUD/USD','FXCH':'CHY/USD','BZF':'BRL/USD',
         '^GSPC':'S&P500','^N225':'Nikki_225','^SSEC':'SSE_Composite','^FTSE':'FTSE_100','^HSI':'HANG_SENG_INDEX',\
         '^BVSP':'IBOVESPA','^AORD':'ALL_ORDINARIES','^GDAXI':'DAX','^BSESN':'S&P_BSE_SENSEX',\
         'XLY':'Consumer Discretionary','XLP':'Consumer Staples','XLE':'Energy','XLF':'Financials',\
         'XLV':'Health Care','XLI':'Industrials','XLB':'Materials','XLRE':'Real Estate','XLK':'Technology','XLU':'Utilities'}
         

    ###### Equity Index Return ######
    equity_index_dtd,equity_index_mtd,equity_index_qtd,equity_index_ytd = get_return(equity_index_list)
    
    equity_data_dtd = equity_index_dtd.ix[-1].values
    equity_data_mtd = equity_index_mtd.ix[-1].values
    equity_data_qtd = equity_index_qtd.ix[-1].values
    equity_data_ytd = equity_index_ytd.ix[-1].values

    equity_str_dtd = ["%.2f" % x for x in 100*equity_data_dtd]
    equity_str_mtd = ["%.2f" % x for x in 100*equity_data_mtd]
    equity_str_qtd = ["%.2f" % x for x in 100*equity_data_qtd]
    equity_str_ytd = ["%.2f" % x for x in 100*equity_data_ytd]


    ###### Currency ######     
    current = 'latest'
    last_day = datetime.strftime(datetime.today()-dateutil.relativedelta.relativedelta(days=1),'%Y-%m-%d')
    last_month = datetime.strftime(datetime.today()-dateutil.relativedelta.relativedelta(months=1),'%Y-%m-%d')
    last_quarter = datetime.strftime(datetime.today()-dateutil.relativedelta.relativedelta(months=3),'%Y-%m-%d')
    last_year = datetime.strftime(datetime.today()-dateutil.relativedelta.relativedelta(months=12),'%Y-%m-%d')
    date_list = [current,last_day,last_month,last_quarter,last_year]
    
    currency_df = pd.DataFrame([])
    for i in range(len(date_list)):
        with urllib.request.urlopen('http://api.fixer.io/%s?base=USD' %date_list[i]) as f:
            currency_dict = ast.literal_eval(f.read().decode('utf-8'))
            currency_df = pd.concat([currency_df,pd.DataFrame.from_dict(currency_dict['rates'],'index')], axis=1)
    currency_df.columns = ['Current','Last_Day','Last_Month','Last_Quarter','Last_Year']
    currency_df['dtd'] = round((currency_df['Current']-currency_df['Last_Day'])/currency_df['Last_Day'],4)
    currency_df['mtd'] = round((currency_df['Current']-currency_df['Last_Month'])/currency_df['Last_Month'],4)
    currency_df['qtd'] = round((currency_df['Current']-currency_df['Last_Quarter'])/currency_df['Last_Quarter'],4)
    currency_df['ytd'] = round((currency_df['Current']-currency_df['Last_Year'])/currency_df['Last_Year'],4)

        
    ###### Concat the data ######      
    a=[]
    for i,j,k,l,m in zip(equity_index_dtd.columns,equity_str_dtd,equity_str_mtd,equity_str_qtd,equity_str_ytd):
        a.append(i+': '+j+'%'+'<br>'+'MTD/QTD/YTD'+'<br>'+k+'%/'+l+'%/'+m+'%')
    a[0] = a[0]+'<br>'+'USD/AUD: '+str(100*currency_df.loc['AUD','dtd'])+'%'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['AUD','mtd'])+'%/'+str(100*currency_df.loc['AUD','qtd'])+'%/'+str(100*currency_df.loc['AUD','ytd'])+'%'
    a[1] = a[1]+'<br>'+'USD/INR: '+str(100*currency_df.loc['INR','dtd'])+'%'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['INR','mtd'])+'%/'+str(100*currency_df.loc['INR','qtd'])+'%/'+str(100*currency_df.loc['INR','ytd'])+'%'
    a[2] = a[2]+'<br>'+'USD/BRL: '+str(100*currency_df.loc['BRL','dtd'])+'%'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['BRL','mtd'])+'%/'+str(100*currency_df.loc['BRL','qtd'])+'%/'+str(100*currency_df.loc['BRL','ytd'])+'%'
    a[3] = a[3]+'<br>'+'USD/GBP: '+str(100*currency_df.loc['GBP','dtd'])+'%'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['GBP','mtd'])+'%/'+str(100*currency_df.loc['GBP','qtd'])+'%/'+str(100*currency_df.loc['GBP','ytd'])+'%'
    a[4] = a[4]+'<br>'+'USD/EUR: '+str(100*currency_df.loc['EUR','dtd'])+'%'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['EUR','mtd'])+'%/'+str(100*currency_df.loc['EUR','qtd'])+'%/'+str(100*currency_df.loc['EUR','ytd'])+'%'
    a[6] = a[6]+'<br>'+'USD/HKD: '+str(100*currency_df.loc['HKD','dtd'])+'%'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['HKD','mtd'])+'%/'+str(100*currency_df.loc['HKD','qtd'])+'%/'+str(100*currency_df.loc['HKD','ytd'])+'%'
    a[7] = a[7]+'<br>'+'USD/JPY: '+str(100*currency_df.loc['JPY','dtd'])+'%'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['JPY','mtd'])+'%/'+str(100*currency_df.loc['JPY','qtd'])+'%/'+str(100*currency_df.loc['JPY','ytd'])+'%'
    a[8] = a[8]+'<br>'+'USD/CNY: '+str(100*currency_df.loc['CNY','dtd'])+'%'+'<br>'+'MTD/QTD/YTD'+'<br>'+str(100*currency_df.loc['CNY','mtd'])+'%/'+str(100*currency_df.loc['CNY','qtd'])+'%/'+str(100*currency_df.loc['CNY','ytd'])+'%'
    
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