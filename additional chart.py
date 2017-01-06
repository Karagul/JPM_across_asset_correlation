# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 15:16:07 2017

@author: ZFang
"""


from pandas_datareader.famafrench import get_available_datasets
import pandas_datareader.data as web
from datetime import datetime





get_available_datasets()

start = datetime(1961,7,1)

ff = web.DataReader("F-F_Research_Data_5_Factors_2x3_daily", "famafrench", start=start)
ff_df = (ff[0]/100)+1
cum_ff = ff_df.cumprod()-1



calendar_ff = ff_df.resample('A').prod()-1
calendar_ff.index = calendar_ff.index.year

calendar_ff[-10:].plot(kind='bar')



def calendar_return(dataframe):
    # Force all nan in dataframe to be np.nan
    dataframe = dataframe.fillna(np.nan)
    
    dataframe = dataframe+1
    dataframe.index = pd.DatetimeIndex(dataframe['Date'])
    Calendar_Return_df = (dataframe.resample('A').prod())-1
    Calendar_Return_df = Calendar_Return_df.transpose()
    Calendar_Return_df.columns = Calendar_Return_df.columns.year
    return Calendar_Return_df