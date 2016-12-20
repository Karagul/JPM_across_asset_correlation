# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:41:37 2016

@author: ZFang
"""

from datetime import datetime
import pandas_datareader.data as wb
from fredapi import Fred
import pandas as pd

def get_value(tickerlist):
    start = datetime(2011,9,19)
    end = datetime(2016,12,1)
    p = wb.DataReader(tickerlist,'yahoo',start,end)
    return_df = p['Adj Close']
    return return_df


def get_libor():
    fred = Fred(api_key='a0718ea00e6784c5f8b452741622a98c')
    Libor_1M = pd.DataFrame(fred.get_series('USD1MTD156N',observation_start='9/19/2011'))
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
    macro_d = pd.concat([Libor_1M,Libor_3M,Treasury_1Y,Treasury_5Y,Treasury_10Y,WILLREITIND],axis=1)
    macro_m.columns=['GDP','CPI','Uneply','M2','Non_farm','Fed_Debt','Dollar_index','HOUST']
    macro_d.columns = ['Libor_1M','Libor_3M','Treasury_1Y','Treasury_5Y','Treasury_10Y','WILLREITIND']
    return Fed_Rate,macro_m,macro_d
    
def add_column_name(dataframe):
    l = []
    for i in dataframe.columns:
        l.append(ticker_dict[i])
    dataframe.columns = l
    return dataframe

if __name__ == '__main__':
    
    equity_etf_list = ['SPY','EWJ','EWG','IWV','IYY','FEZ','ONEQ','TLT','IEF']
    equity_index_list = ['^GSPC','^N225','^SSEC','^FTSE','^HSI','^BVSP','^AORD','^GDAXI','^STOXX50E']
    currency_list = ['FXY','FXB','FXE','FXA']
    commodity_etf_list = ['GLD','SLV','OIL','UNL','JJC','WEAT','CORN']
    
    ticker_dict = {'FXY':'USD/JPY','FXB':'GBP/USD','FXE':'EUR/USD','FXA':'AUD/USD',\
        'SPY':'S&P_ETF','EWJ':'NIKKEI_ETF','EWG':'DAX_ETF','IWV':'RUSSELL_ETF','IYY':'DOW_ETF',\
         'FEZ':'EURO_50_ETF','ONEQ':'NASDAQ_ETF','GLD':'GOLD','SLV':'SILVER','OIL':'OIL',\
         'UNL':'GAS','JJC':'COPPER','WEAT':'WEAT','CORN':'CORN','TLT':'20yr_Bond','IEF':'7_10_yr_Bond',\
         '^GSPC':'S&P500','^N225':'Nikki_225','^SSEC':'SSE Composite','^FTSE':'FTSE_100','^HSI':'HANG_SENG_INDEX',\
         '^BVSP':'IBOVESPA','^AORD':'ALL_ORDINARIES','^GDAXI':'DAX','^STOXX50E':'ESTX50'}
    ###### Equity ETF ######
    equity_etf = get_value(equity_etf_list)
    equity_etf = add_column_name(equity_etf)
    ###### Equity Index ######
    equity_index = get_value(equity_index_list)
    equity_index = add_column_name(equity_index)
    ###### Currency ######
    currency = get_value(currency_list)
    currency = add_column_name(currency)
    ###### Currency ######
    commodity_etf = get_value(commodity_etf_list)
    commodity_etf = add_column_name(commodity_etf)
    
    
    Fed_Rate,macro_m,macro_d = get_libor()

    
    
    