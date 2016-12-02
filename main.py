# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:41:37 2016

@author: ZFang
"""

from datetime import datetime
import pandas_datareader.data as wb
from fredapi import Fred
import pandas as pd

def get_etf(stocklist,column_name):
    start = datetime(2011,9,19)
    end = datetime(2016,12,1)
    p = wb.DataReader(stocklist,'yahoo',start,end)
    return_df = p['Adj Close']
    return_df.columns = column_name  
    return return_df


def get_libor():
    fred = Fred(api_key='a0718ea00e6784c5f8b452741622a98c')
    Libor_3M = pd.DataFrame(fred.get_series('USD3MTD156N',observation_start='9/19/2011'))
    Libor_1Y = pd.DataFrame(fred.get_series('DSWP1',observation_start='9/19/2011'))
    Libor_5Y = pd.DataFrame(fred.get_series('DSWP5',observation_start='9/19/2011'))
    Libor_10Y = pd.DataFrame(fred.get_series('DSWP10',observation_start='9/19/2011'))
    data = pd.concat([Libor_3M,Libor_1Y,Libor_5Y,Libor_10Y],axis=1)
    data.columns=['Libor_3M','Libor_1Y','Libor_5Y','Libor_10Y']
    return data
    

if __name__ == '__main__':
    
    stocklist = ['FXF','FXB','FXE','FXA','SPY','EWJ','EWG','IWV','IYY','FEZ','ONEQ',\
                 'GLD','SLV','OIL','UNL','JJC','WEAT','CORN','TLT','IEF']   
    column_name = ['USD/JPY','GBP/USD','EUR/USD','AUD/USD','S&P','NIKKEI',\
                   'DAX','RUSSELL','DOW','EURO_50','NASDAQ','GOLD','SILVER',\
                   'OIL','GAS','COPPER','WEAT','CORN','20yr_Bond','7_10_yr_Bond']
    return_df = pd.concat([get_etf(stocklist,column_name),get_libor()],axis=1)
    corr_df = return_df.corr()
    
    
    