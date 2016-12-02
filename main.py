# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 09:41:37 2016

@author: ZFang
"""

from datetime import datetime
import pandas_datareader.data as wb


stocklist = ['FXF','FXB','FXE','FXA','SPY','EWJ','EWG','IWV','IYY','FEZ','ONEQ','GLD','SLV','OIL','UNL','JJC','WEAT','CORN','TLT','IEF']

start = datetime(2011,9,19)
end = datetime(2016,12,1)
p = wb.DataReader(stocklist,'yahoo',start,end)
return_df = p['Adj Close']
return_df.columns = ['USD/JPY','GBP/USD','EUR/USD','AUD/USD','S&P','NIKKEI','DAX','RUSSELL','DOW','EURO_50','NASDAQ','GOLD','SILVER','OIL','GAS','COPPER','WEAT','CORN','20yr_Bond','7_10_yr_Bond']
corr_df = return_df.corr()

