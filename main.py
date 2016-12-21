# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:41:37 2016

@author: ZFang
"""

from datetime import datetime
import pandas_datareader.data as wb
from fredapi import Fred
import pandas as pd
import numpy as np
from itertools import groupby

def get_value(tickerlist):
    start = datetime(2000,1,1)
    end = datetime(2016,12,19)
    p = wb.DataReader(tickerlist,'yahoo',start,end)
    return_df = p['Adj Close']
    return_df = return_df.interpolate()
    return return_df


def get_libor():
    fred = Fred(api_key='a0718ea00e6784c5f8b452741622a98c')
    Libor_1M = pd.DataFrame(fred.get_series('USD1MTD156N',observation_start='1/1/2000'))
    Libor_3M = pd.DataFrame(fred.get_series('USD3MTD156N',observation_start='1/1/2000'))
    Treasury_1Y = pd.DataFrame(fred.get_series('DGS1',observation_start='1/1/2000'))
    Treasury_5Y = pd.DataFrame(fred.get_series('DGS5',observation_start='1/1/2000'))
    Treasury_10Y = pd.DataFrame(fred.get_series('DGS10',observation_start='1/1/2000'))
    Treasury_20Y = pd.DataFrame(fred.get_series('DGS20',observation_start='1/1/2000'))
    Treasury_30Y = pd.DataFrame(fred.get_series('DGS30',observation_start='1/1/2000'))
    WILLREITIND = pd.DataFrame(fred.get_series('WILLREITIND',observation_start='1/1/2000'))
    
    
    GDP = pd.DataFrame(fred.get_series('GDPC1',observation_start='9/19/2011'))
    CPI = pd.DataFrame(fred.get_series('CPIAUCSL',observation_start='9/19/2011'))
    Fed_Rate = pd.DataFrame(fred.get_series('DFF',observation_start='9/19/2011'))
    Uneply = pd.DataFrame(fred.get_series('UNRATE',observation_start='9/19/2011'))
    M2 = pd.DataFrame(fred.get_series('M2',observation_start='9/19/2011'))
    Non_farm = pd.DataFrame(fred.get_series('PAYEMS',observation_start='9/19/2011'))
    Fed_Debt = pd.DataFrame(fred.get_series('GFDEGDQ188S',observation_start='9/19/2011'))
    Dollar_Index = pd.DataFrame(fred.get_series('TWEXB',observation_start='9/19/2011'))    
    HOUST = pd.DataFrame(fred.get_series('HOUST',observation_start='9/19/2011'))

    
    macro_m = pd.concat([GDP,CPI,Uneply,M2,Non_farm,Fed_Debt,Dollar_Index,HOUST],axis=1)
    macro_d = pd.concat([Libor_1M,Libor_3M,Treasury_1Y,Treasury_5Y,Treasury_10Y,Treasury_20Y,Treasury_30Y,WILLREITIND],axis=1)
    macro_m.columns=['GDP','CPI','Uneply','M2','Non_farm','Fed_Debt','Dollar_index','HOUST']
    macro_d.columns = ['Libor_1M','Libor_3M','Treasury_1Y','Treasury_5Y','Treasury_10Y','Treasury_20Y','Treasury_30Y','WILLREITIND']
    return Fed_Rate,macro_m,macro_d
    
def add_column_name(dataframe):
    l = []
    for i in dataframe.columns:
        l.append(ticker_dict[i])
    dataframe.columns = l
    return dataframe
    
    

if __name__ == '__main__':
    
    equity_etf_list = ['SPY','EWJ','EWG','IWV','IYY','FEZ','ONEQ','TLT','IEF']
    equity_index_list = ['^GSPC','^N225','^SSEC','^FTSE','^HSI','^BVSP','^AORD','^GDAXI','^STOXX50E','^BSESN']
    currency_list = ['FXY','FXB','FXE','FXA']
    commodity_etf_list = ['GLD','SLV','OIL','UNL','JJC','WEAT','CORN']
    
    ticker_dict = {'FXY':'USD/JPY','FXB':'GBP/USD','FXE':'EUR/USD','FXA':'AUD/USD',\
        'SPY':'S&P_ETF','EWJ':'NIKKEI_ETF','EWG':'DAX_ETF','IWV':'RUSSELL_ETF','IYY':'DOW_ETF',\
         'FEZ':'EURO_50_ETF','ONEQ':'NASDAQ_ETF','GLD':'GOLD','SLV':'SILVER','OIL':'OIL',\
         'UNL':'GAS','JJC':'COPPER','WEAT':'WEAT','CORN':'CORN','TLT':'20yr_Bond','IEF':'7_10_yr_Bond',\
         '^GSPC':'S&P500','^N225':'Nikki_225','^SSEC':'SSE_Composite','^FTSE':'FTSE_100','^HSI':'HANG_SENG_INDEX',\
         '^BVSP':'IBOVESPA','^AORD':'ALL_ORDINARIES','^GDAXI':'DAX','^STOXX50E':'ESTX50','^BSESN':'S&P_BSE_SENSEX'}
         
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

    

    ### Figure 1 S&P500 with top 10 major equity index 12 month rolling
    sp_equity_avg_corr = equity_index.rolling(window=260).corr(equity_index['S&P500']).ix[260:,['Nikki_225',\
    'DAX','SSE_Composite','FTSE_100','HANG_SENG_INDEX','IBOVESPA','ALL_ORDINARIES','ESTX50','S&P_BSE_SENSEX']].mean(axis=1)
    sp_equity_avg_corr.plot()
    
    ### Figure 2 Plot the all the yield change curve
    libor = macro_d.loc[:,['Libor_1M','Libor_3M','Treasury_1Y','Treasury_5Y','Treasury_10Y','Treasury_20Y','Treasury_30Y']]
    libor.plot()
    
    ### Figure 3 Developed Equity Market Cummulative return
    past_equity_index = equity_index.shift(1)
    cum_equity_index = (1+(equity_index-past_equity_index)/past_equity_index).cumprod()
    cum_equity_index.loc[:,['ALL_ORDINARIES','FTSE_100','DAX','S&P500','Nikki_225','ESTX50']].plot()
    
    ### Figure 4 Developing Equity Market Cummulative return
    cum_equity_index.loc[:,['IBOVESPA','S&P_BSE_SENSEX','HANG_SENG_INDEX','SSE_Composite']].plot()
    
    ### Figure 5 Correlation of Currencies with S&P 500
    currency_sp = pd.concat([currency,equity_index['S&P500']],axis=1)
    # deal with nan data
    currency_sp = currency_sp.interpolate()
    currency_sp_avg_corr = currency_sp.rolling(window=260).corr(currency_sp['S&P500']).ix[260:,[\
                        'AUD/USD','GBP/USD','EUR/USD','USD/JPY']].mean(axis=1)
    currency_sp_avg_corr.plot()
    
    ### Figure 6 Correlation of 10Y Treasury Yield and S&P 500
    trea_sp = pd.concat([macro_d['Treasury_10Y'],equity_index['S&P500']],axis=1)
    trea_sp = trea_sp.interpolate()
    trea_sp_corr = trea_sp.rolling(window=260).corr(trea_sp['S&P500']).ix[260:,['Treasury_10Y']]
    trea_sp_corr.plot()
    
    ### Figure 7 Correlation of S&P500 and other commodities
    comm_sp = pd.concat([commodity_etf,equity_index['S&P500']],axis=1)
    comm_sp = comm_sp.interpolate()
    comm_sp_corr = comm_sp.rolling(window=260).corr(comm_sp['S&P500']).ix[260:,['CORN','GOLD','COPPER','OIL','SILVER','GAS','WEAT']]
    comm_sp_corr.plot()