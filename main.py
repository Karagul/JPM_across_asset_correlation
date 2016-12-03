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
    Treasury_1Y = pd.DataFrame(fred.get_series('DGS1',observation_start='9/19/2011'))
    Treasury_5Y = pd.DataFrame(fred.get_series('DGS5',observation_start='9/19/2011'))
    Treasury_10Y = pd.DataFrame(fred.get_series('DGS10',observation_start='9/19/2011'))
    GDP = pd.DataFrame(fred.get_series('GDPC1',observation_start='9/19/2011'))
    CPI = pd.DataFrame(fred.get_series('CPIAUCSL',observation_start='9/19/2011'))
    Fed_Rate = pd.DataFrame(fred.get_series('DFF',observation_start='9/19/2011'))
    Uneply = pd.DataFrame(fred.get_series('UNRATE',observation_start='9/19/2011'))
    M2 = pd.DataFrame(fred.get_series('M2',observation_start='9/19/2011'))
    Non_farm = pd.DataFrame(fred.get_series('PAYEMS',observation_start='9/19/2011'))
    Fed_Debt = pd.DataFrame(fred.get_series('GFDEGDQ188S',observation_start='9/19/2011'))
    Dollar_Index = pd.DataFrame(fred.get_series('TWEXB',observation_start='9/19/2011'))    
    HOUST = pd.DataFrame(fred.get_series('HOUST',observation_start='9/19/2011'))
    WILLREITIND = pd.DataFrame(fred.get_series('WILLREITIND',observation_start='9/19/2011'))
    
    macro_m = pd.concat([GDP,CPI,Uneply,M2,Non_farm,Fed_Debt,Dollar_Index,HOUST],axis=1)
    macro_d = pd.concat([Libor_3M,Treasury_1Y,Treasury_5Y,Treasury_10Y,WILLREITIND],axis=1)
    macro_m.columns=['GDP','CPI','Uneply','M2','Non_farm','Fed_Debt','Dollar_index','HOUST']
    macro_d.columns = ['Libor_3M','Treasury_1Y','Treasury_5Y','Treasury_10Y','WILLREITIND']
    return Fed_Rate,macro_m,macro_d
    

if __name__ == '__main__':
    
    stocklist = ['FXF','FXB','FXE','FXA','SPY','EWJ','EWG','IWV','IYY','FEZ','ONEQ',\
                 'GLD','SLV','OIL','UNL','JJC','WEAT','CORN','TLT','IEF']   
    column_name = ['USD/JPY','GBP/USD','EUR/USD','AUD/USD','S&P','NIKKEI',\
                   'DAX','RUSSELL','DOW','EURO_50','NASDAQ','GOLD','SILVER',\
                   'OIL','GAS','COPPER','WEAT','CORN','20yr_Bond','7_10_yr_Bond']
    etf = get_etf(stocklist,column_name)
    Fed_Rate,macro_m,macro_d = get_libor()

    
    
    