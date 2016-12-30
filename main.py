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
from urllib.request import urlopen
import json
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime, timedelta


def get_return(tickerlist):
    start = datetime(2000,1,1)
    end = datetime(2016,12,19)
    p = wb.DataReader(tickerlist,'yahoo',start,end)
    price_df = p['Adj Close']
    price_df = price_df.interpolate()
    past_price_df = price_df.shift(1)
    return_df = (price_df - past_price_df)/past_price_df

    for i in return_df.columns:
        first_index = return_df.loc[:,i].first_valid_index()-timedelta(days=1)
        return_df.ix[first_index,i]=0
    return return_df
    
    
def get_price(tickerlist):
    start = datetime(2000,1,1)
    end = datetime(2016,12,19)
    p = wb.DataReader(tickerlist,'yahoo',start,end)
    price_df = p['Adj Close']
    price_df = price_df.interpolate()
    
    return price_df    


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
    OAS = pd.DataFrame(fred.get_series('BAMLH0A0HYM2',observation_start='1/1/2000'))
    
    
    GDP = pd.DataFrame(fred.get_series('GDPC1',observation_start='9/19/2011'))
    CPI = pd.DataFrame(fred.get_series('CPIAUCSL',observation_start='9/19/2011'))
    Fed_Rate = pd.DataFrame(fred.get_series('DFF',observation_start='9/19/2011'))
    Uneply = pd.DataFrame(fred.get_series('UNRATE',observation_start='9/19/2011'))
    M2 = pd.DataFrame(fred.get_series('M2',observation_start='9/19/2011'))
    Non_farm = pd.DataFrame(fred.get_series('PAYEMS',observation_start='9/19/2011'))
    Fed_Debt = pd.DataFrame(fred.get_series('GFDEGDQ188S',observation_start='9/19/2011'))
    Dollar_Index = pd.DataFrame(fred.get_series('TWEXB',observation_start='9/19/2011'))    
    HOUST = pd.DataFrame(fred.get_series('HOUST',observation_start='9/19/2011'))

    
    macro_m_price = pd.concat([GDP,CPI,Uneply,M2,Non_farm,Fed_Debt,Dollar_Index,HOUST],axis=1)
    macro_d_price = pd.concat([Libor_1M,Libor_3M,Treasury_1Y,Treasury_5Y,Treasury_10Y,Treasury_20Y,Treasury_30Y,WILLREITIND,OAS],axis=1)
    macro_m_price.columns=['GDP','CPI','Uneply','M2','Non_farm','Fed_Debt','Dollar_index','HOUST']
    macro_d_price.columns = ['Libor_1M','Libor_3M','Treasury_1Y','Treasury_5Y','Treasury_10Y','Treasury_20Y','Treasury_30Y','WILLREITIND','OAS']
    
    # Calculate return
    Fed_Rate = (Fed_Rate - Fed_Rate.shift(1))/Fed_Rate.shift(1)
    macro_m = (macro_m_price - macro_m_price.shift(1))/macro_m_price.shift(1)
    macro_d = (macro_d_price - macro_d_price.shift(1))/macro_d_price.shift(1)
    
    
    return Fed_Rate,macro_m_price,macro_m,macro_d_price,macro_d
    
def add_column_name(dataframe):
    l = []
    for i in dataframe.columns:
        l.append(ticker_dict[i])
    dataframe.columns = l
    return dataframe
    
    

if __name__ == '__main__':
    
    equity_etf_list = ['SPY','EWJ','EWG','IWV','IYY','FEZ','ONEQ','TLT','IEF']
    equity_index_list = ['^GSPC','^N225','^SSEC','^FTSE','^HSI','^BVSP','^AORD','^GDAXI','^STOXX50E','^BSESN','^VIX']
    currency_list = ['FXY','FXB','FXE','FXA','FXF']
    commodity_etf_list = ['GLD','SLV','OIL','UNL','JJC','WEAT','CORN']
    equity_sector_list = ['XLY','XLP','XLE','XLF','XLV','XLI','XLB','XLRE','XLK','XLU']
    
    ticker_dict = {'FXY':'JPY/USD','FXB':'GBP/USD','FXE':'EUR/USD','FXA':'AUD/USD','FXF':'CHF/USD',\
        'SPY':'S&P_ETF','EWJ':'NIKKEI_ETF','EWG':'DAX_ETF','IWV':'RUSSELL_ETF','IYY':'DOW_ETF',\
         'FEZ':'EURO_50_ETF','ONEQ':'NASDAQ_ETF','GLD':'GOLD','SLV':'SILVER','OIL':'OIL',\
         'UNL':'GAS','JJC':'COPPER','WEAT':'WEAT','CORN':'CORN','TLT':'20yr_Bond','IEF':'7_10_yr_Bond',\
         '^GSPC':'S&P500','^N225':'Nikki_225','^SSEC':'SSE_Composite','^FTSE':'FTSE_100','^HSI':'HANG_SENG_INDEX',\
         '^BVSP':'IBOVESPA','^AORD':'ALL_ORDINARIES','^GDAXI':'DAX','^STOXX50E':'ESTX50','^BSESN':'S&P_BSE_SENSEX',\
         '^VIX':'VIX','XLY':'Consumer Discretionary','XLP':'Consumer Staples','XLE':'Energy','XLF':'Financials',\
         'XLV':'Health Care','XLI':'Industrials','XLB':'Materials','XLRE':'Real Estate','XLK':'Technology','XLU':'Utilities'}
         
    ###### Equity ETF ######
    equity_etf = get_return(equity_etf_list)
    equity_etf = add_column_name(equity_etf)
    ###### Equity Index ######
    equity_index = get_return(equity_index_list)
    equity_index_price = get_price(equity_index_list)
    equity_index = add_column_name(equity_index)
    equity_index_price = add_column_name(equity_index_price)
    ###### Currency ######
    currency = get_return(currency_list)    
    currency = add_column_name(currency)
    ###### Currency ######
    commodity_etf = get_return(commodity_etf_list)
    commodity_etf = add_column_name(commodity_etf)
    ###### Equity(SP500) Sector ######
    equity_sector = get_return(equity_sector_list)
    equity_sector = add_column_name(equity_sector)
    
    Fed_Rate,macro_m_price,macro_m,macro_d_price,macro_d = get_libor()

    
    
    # Plotly
    color1 = 'b'
    color2 = 'b'
        
    
    
    ### Figure 1 Developed Equity Market Cummulative return
    cum_equity_index = (1+equity_index).cumprod()-1
    cum_DM_equity_index = cum_equity_index.loc[:,['ALL_ORDINARIES','FTSE_100','DAX','S&P500','Nikki_225','ESTX50']]
    
    trace1 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['ALL_ORDINARIES'],
        name='ALL_ORDINARIES'
    )
    trace2 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['FTSE_100'],
        name='FTSE_100'
    )
    trace3 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['DAX'],
        name='DAX'
    )
    trace4 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['S&P500'],
        name='S&P500'
    )
    trace5 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['Nikki_225'],
        name='Nikki_225'
    )
    trace6 = go.Scatter(
        x=cum_DM_equity_index.index,
        y=100*cum_DM_equity_index['ESTX50'],
        name='ESTX50'
    )

    data = [trace1,trace2,trace3,trace4,trace5,trace6]
    layout = go.Layout(
        title='Cumulative Return of Developed Market Equity Indices',
        yaxis=dict(
            title='Cumulative Return',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
            
    fig_1 = go.Figure(data=data, layout=layout)
    plot_url_1 = py.plot(fig_1, filename='Figure 1 Cumulative Return of Developed Market Equity Indices', sharing='public')
    
    
    

    
    ### Figure 2 Developing Equity Market Cummulative return
    cum_EM_equity_index = cum_equity_index.loc[:,['IBOVESPA','S&P_BSE_SENSEX','HANG_SENG_INDEX','SSE_Composite']]
    
    trace1 = go.Scatter(
        x=cum_EM_equity_index.index,
        y=100*cum_EM_equity_index['IBOVESPA'],
        name='IBOVESPA'
    )
    trace2 = go.Scatter(
        x=cum_EM_equity_index.index,
        y=100*cum_EM_equity_index['S&P_BSE_SENSEX'],
        name='P_BSE_SENSEX'
    )
    trace3 = go.Scatter(
        x=cum_EM_equity_index.index,
        y=100*cum_EM_equity_index['HANG_SENG_INDEX'],
        name='HANG_SENG_INDEX'
    )
    trace4 = go.Scatter(
        x=cum_EM_equity_index.index,
        y=100*cum_EM_equity_index['SSE_Composite'],
        name='S&SSE_Composite'
    )

    data = [trace1,trace2,trace3,trace4,trace5,trace6]
    layout = go.Layout(
        title='Cumulative Return of Emerging Market Equity Indices',
        yaxis=dict(
            title='Cumulative Return',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
            
    fig_2 = go.Figure(data=data, layout=layout)
    plot_url_2 = py.plot(fig_2, filename='Figure 2 Cumulative Return of Emerging Market Equity Indices', sharing='public')    
    
    
    ### Figure 3 S&P500 with top 10 major equity index 12 month rolling
    top_10_list = ['ALL_ORDINARIES','S&P_BSE_SENSEX','IBOVESPA','FTSE_100','DAX','S&P500','HANG_SENG_INDEX','Nikki_225','SSE_Composite','ESTX50']
    equity_corr = equity_index[top_10_list].rolling(window=260).corr()
    mask = np.ones(equity_corr.iloc[0].shape,dtype='bool')
    mask[np.triu_indices(len(equity_corr.iloc[0]))] = False
    equity_avg_corr_l = []
    for i in range(len(equity_corr)):
        equity_avg_corr_l.append(equity_corr.iloc[i][(equity_corr.iloc[i]>-2)&mask].sum().sum()/45)
    equity_avg_corr = pd.DataFrame(equity_avg_corr_l, index=equity_index.index, columns=['Average_Correlation'])
    equity_avg_corr = equity_avg_corr['2000-12-29 00:00:00':]

    trace1 = go.Scatter(
        x=equity_avg_corr.index,
        y=equity_avg_corr['Average_Correlation'],
        name='Avg Correlation'
    ) 
    
    data = [trace1]
    layout = go.Layout(
        title='Average Correlation Between 10 Major Equity Indices',
        showlegend=True,
        yaxis=dict(
            title='Equity Index Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
    fig_3 = go.Figure(data=data, layout=layout)
    plot_url_3 = py.plot(fig_3, filename='Figure 3 Average Correlation Between 10 Major Equity Indices', sharing='public')
    
    
    
    ### Figure 4 Correlation Between DM and EM Countries Equity Index
    DM_avg_equity_index = equity_index.loc[:,['ALL_ORDINARIES','FTSE_100','DAX','S&P500','Nikki_225','ESTX50']].mean(axis=1)
    EM_avg_equity_index = equity_index.loc[:,['IBOVESPA','S&P_BSE_SENSEX','HANG_SENG_INDEX','SSE_Composite']].mean(axis=1)
    
    DM_EM_index = pd.concat([DM_avg_equity_index,EM_avg_equity_index],axis=1)
    DM_EM_index.columns = ['DM Market','EM Market']
    
    DM_EM_corr = DM_EM_index.rolling(window=260).corr(DM_EM_index['DM Market']).ix['2001-01-02 00:00:00':,['EM Market']]
    
    trace1 = go.Scatter(
        x=DM_EM_corr.index,
        y=DM_EM_corr['EM Market'],
        name='DM and EM Correlation'
        )

    data = [trace1]
    layout = go.Layout(
        title='Correlation Between DM and EM Countries Equity Index',
        showlegend=True,
        yaxis=dict(
            title='DM EM Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
            
    fig_4 = go.Figure(data=data, layout=layout)
    plot_url_4 = py.plot(fig_4, filename='Figure 4 Correlation Between DM and EM Countries Equity Index', sharing='public')
    
    
    
    ### Figure 5 Plot the all the yield change curve
    libor = macro_d_price.loc[:,['Libor_1M','Libor_3M','Treasury_1Y','Treasury_5Y','Treasury_10Y','Treasury_20Y','Treasury_30Y']]
    
    trace1 = go.Scatter(
        x=libor.index,
        y=libor['Libor_1M'],
        name='Libor_1M'
    )
    trace2 = go.Scatter(
        x=libor.index,
        y=libor['Libor_3M'],
        name='Libor_3M'
    )
    trace3 = go.Scatter(
        x=libor.index,
        y=libor['Treasury_1Y'],
        name='Treasury_1Y'
    )
    trace4 = go.Scatter(
        x=libor.index,
        y=libor['Treasury_5Y'],
        name='Treasury_5Y'
    )
    trace5 = go.Scatter(
        x=libor.index,
        y=libor['Treasury_10Y'],
        name='Treasury_10Y'
    )
    trace6 = go.Scatter(
        x=libor.index,
        y=libor['Treasury_20Y'],
        name='Treasury_20Y'
    )
    trace7 = go.Scatter(
        x=libor.index,
        y=libor['Treasury_30Y'],
        name='Treasury_30Y'
    )

    data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7]
    layout = go.Layout(
        title='Libor/Treasury Rate',
        yaxis=dict(
            title='Yield',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
    annotations = []   
    # Source
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                                  xanchor='center', yanchor='top',
                                  text='Some Short Description',
                                  font=dict(family='Arial',
                                            size=12,
                                            color='rgb(150,150,150)'),
                                  showarrow=False))  
                
    layout['annotations'] = annotations   
            
            
    fig_5 = go.Figure(data=data, layout=layout)
    plot_url_5 = py.plot(fig_5, filename='Figure 5 Libor and Treasury Rate', sharing='public')
    #libor.plot()
    
    ### Figure 6 Cumulative Return of Major Currencies
    
    cum_currency = (1+currency).cumprod()-1
    
    trace1 = go.Scatter(
        x=cum_currency.index,
        y=100*cum_currency['AUD/USD'],
        name='AUD/USD'
    )
    trace2 = go.Scatter(
        x=cum_currency.index,
        y=100*cum_currency['GBP/USD'],
        name='GBP/USD'
    )
    trace3 = go.Scatter(
        x=cum_currency.index,
        y=100*cum_currency['EUR/USD'],
        name='EUR/USD'
    )
    trace4 = go.Scatter(
        x=cum_currency.index,
        y=100*cum_currency['CHF/USD'],
        name='CHF/USD'
    )
    trace5 = go.Scatter(
        x=cum_currency.index,
        y=100*cum_currency['JPY/USD'],
        name='JPY/USD'
    )

    data = [trace1,trace2,trace3,trace4,trace5]
    layout = go.Layout(
        title='Cumulative Return of Major Currencies',
        yaxis=dict(
            title='Cummulative Return',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
            
    fig_6 = go.Figure(data=data, layout=layout)
    plot_url_6 = py.plot(fig_6, filename='Figure 6 Cumulative Return of Major Currencies', sharing='public')    
    
    
    


    ### Figure 7 Correlation of Currencies with S&P 500
    currency_sp = pd.concat([currency,equity_index['S&P500']],axis=1)
    # deal with nan data
    currency_sp = currency_sp.interpolate()
    currency_sp_avg_corr = currency_sp.rolling(window=260).corr(currency_sp['S&P500']).ix[260:,[\
                        'AUD/USD','GBP/USD','EUR/USD','JPY/USD','CHF/USD']].mean(axis=1)
    currency_sp_avg_corr = currency_sp_avg_corr['2007-01-02 00:00:00':]
    currency_sp_avg_corr.name = 'Average_Correlation'
    
    
    trace1 = go.Scatter(
        x=currency_sp_avg_corr.index,
        y=currency_sp_avg_corr.values,
        name='Average Correlation'
    ) 
    
    data = [trace1]
    layout = go.Layout(
        title='Average Correlation of Major Currencies with S&P 500',
        showlegend=True,
        yaxis=dict(
            title='Average Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
    fig_7 = go.Figure(data=data, layout=layout)
    plot_url_7 = py.plot(fig_7, filename='Figure 7 Average Correlation of Major Currency ETF with S&P 500', sharing='public')
    
    
    ### Figure 8 Correlation of 10Y Treasury Yield and S&P 500
    trea_sp = pd.concat([macro_d_price['Treasury_10Y'],equity_index['S&P500']],axis=1)
    trea_sp = trea_sp.interpolate()
    trea_sp_corr = trea_sp.rolling(window=260).corr(trea_sp['S&P500']).ix[260:,['Treasury_10Y']]
    trea_sp_corr_yield = pd.concat([trea_sp_corr,macro_d_price.ix[260:,'Treasury_10Y']],axis=1)
    trea_sp_corr_yield.columns = ['Correlation','10Y_yield']
    # trea_sp_corr_yield.plot()
    
    
    
    trace1 = go.Scatter(
        x=trea_sp_corr_yield.index,
        y=trea_sp_corr_yield['Correlation'],
        name='Correlation of Treasury&Equity'
    ) 
    
    trace2 = go.Scatter(
        x=trea_sp_corr_yield.index,
        y=trea_sp_corr_yield['10Y_yield'],
        name='Treasury Yield',
        yaxis='y2'
    ) 
    
    data = [trace1, trace2]
    layout = go.Layout(
        title='Correlation 10 Year Treasury & S&P500',
        yaxis=dict(
            title='Correlation'
        ),
        yaxis2=dict(
            title='Treasury_10Y',
            titlefont=dict(
                color=color2
            ),
            tickfont=dict(
                color=color2
            ),
            overlaying='y',
            side='right'
        )
    )
    
    fig8 = go.Figure(data=data, layout=layout)
    plot_url_8 = py.plot(fig8, filename='Figure 8 Correlation 10 Year Treasury & S&P500',sharing='public')
    
    

    ### Figure 9 Cumulative Return of Commodities
    cum_commodity_etf = (1+commodity_etf).cumprod()-1
    # cum_commodity_etf.loc[:,['CORN','GOLD','COPPER','OIL','SILVER','GAS','WEAT']].plot()
    
    trace1 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['CORN'],
        name='CORN'
    )
    trace2 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['GOLD'],
        name='GOLD'
    )
    trace3 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['COPPER'],
        name='COPPER'
    )
    trace4 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['OIL'],
        name='OIL'
    )
    trace5 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['SILVER'],
        name='SILVER'
    )
    trace6 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['GAS'],
        name='GAS'
    )
    trace7 = go.Scatter(
        x=cum_commodity_etf.index,
        y=100*cum_commodity_etf['WEAT'],
        name='WEAT'
    )

    data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7]
    layout = go.Layout(
        title='Cumulative Return of Major Commodities',
        yaxis=dict(
            title='Cumulative Return',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
            
    fig_9 = go.Figure(data=data, layout=layout)
    plot_url_9 = py.plot(fig_9, filename='Figure 9 Cumulative Return of Major Commodities', sharing='public')    
    
    
    
    
    ### Figure 10 Correlation of S&P500 and other commodities
    comm_sp = pd.concat([commodity_etf,equity_index['S&P500']],axis=1)
    comm_sp = comm_sp.interpolate()
    comm_sp_corr = comm_sp.rolling(window=260).corr(comm_sp['S&P500']).ix[260:,['CORN','GOLD','COPPER','OIL','SILVER','GAS','WEAT']]
    comm_sp_corr = comm_sp_corr['2005-11-16 00:00:00':]
    # comm_sp_corr.plot()
    
    trace1 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['CORN'],
        name='CORN'
    )
    trace2 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['GOLD'],
        name='GOLD'
    )
    trace3 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['COPPER'],
        name='COPPER'
    )
    trace4 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['OIL'],
        name='OIL'
    )
    trace5 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['SILVER'],
        name='SILVER'
    )
    trace6 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['GAS'],
        name='GAS'
    )
    trace7 = go.Scatter(
        x=comm_sp_corr.index,
        y=comm_sp_corr['WEAT'],
        name='WEAT'
    )

    data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7]
    layout = go.Layout(
        title='Correlation of Commodities with S&P500',
        yaxis=dict(
            title='Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
            
    fig_10 = go.Figure(data=data, layout=layout)
    plot_url_10 = py.plot(fig_10, filename='Figure 10 Correlation of Commodities with S&P500', sharing='public')
    
    
    ### Figure 11 Average Correlation with all Commodities
    comm_corr = commodity_etf.rolling(window=260).corr()
    mask = np.ones(comm_corr.iloc[0].shape,dtype='bool')
    mask[np.triu_indices(len(comm_corr.iloc[0]))] = False
    comm_avg_corr_l = []
    for i in range(len(comm_corr)):
        comm_avg_corr_l.append(comm_corr.iloc[i][(comm_corr.iloc[i]>-2)&mask].sum().sum()/21)
    comm_avg_corr = pd.DataFrame(comm_avg_corr_l, index=commodity_etf.index, columns=['Average_Correlation'])
    comm_avg_corr = comm_avg_corr['2007-05-10 00:00:00':]

    trace1 = go.Scatter(
        x=currency_sp_avg_corr.index,
        y=currency_sp_avg_corr.values,
        name='Average Correlation'
    ) 
    
    data = [trace1]
    layout = go.Layout(
        title='Average Correlation of Major Commodities',
        showlegend=True,
        yaxis=dict(
            title='Average Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
    fig_11 = go.Figure(data=data, layout=layout)
    plot_url_11 = py.plot(fig_11, filename='Figure 11 Average Correlation of Major Commodities', sharing='public')
    
    
    ### Figure 12 Option Adjusted Spread (OAS) and VIX
    oas_vix = pd.concat([equity_index_price['VIX'],macro_d['OAS']],axis=1)
    oas_vix = oas_vix.interpolate()
    
    
    trace1 = go.Scatter(
        x=oas_vix.index,
        y=oas_vix['VIX'],
        name='VIX'
    )
    trace2 = go.Scatter(
        x=oas_vix.index,
        y=oas_vix['OAS'],
        name='OAS',
        yaxis='y2'
    )

    data = [trace1,trace2]
    layout = go.Layout(
        title='Option Adjusted Spread (OAS) and VIX',
        yaxis=dict(
            title='VIX Value',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        ),
        yaxis2=dict(
            title='OAS',
            titlefont=dict(
                color=color1
            ),
            tickfont=dict(
                color=color1
            ),
            overlaying='y',
            side='right'
        )
    )
            
            
    fig_12 = go.Figure(data=data, layout=layout)
    plot_url_12 = py.plot(fig_12, filename='Figure 12 Option Adjusted Spread (OAS) and VIX', sharing='public')
        
 
    ### Figure 13 Correlation of OAS and S&P500
    oas_sp = pd.concat([-equity_index['S&P500'],equity_index['VIX'],macro_d['OAS']],axis=1)
    oas_sp = oas_sp.interpolate()
    oas_sp_corr = oas_sp.rolling(window=260).corr(oas_sp['OAS']).ix[260:,['S&P500','VIX']]
    # oas_sp_corr.plot()
    
    trace1 = go.Scatter(
        x=oas_sp_corr.index,
        y=oas_sp_corr['S&P500'],
        name='OAS to S&P500 (Inverse)'
    )
    trace2 = go.Scatter(
        x=oas_sp_corr.index,
        y=oas_sp_corr['VIX'],
        name='OAS to VIX'
    )

    data = [trace1,trace2]
    layout = go.Layout(
        title='Correlation of High Yield OAS to S&P500 and VIX',
        yaxis=dict(
            title='Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
            
    fig_13 = go.Figure(data=data, layout=layout)
    plot_url_13 = py.plot(fig_13, filename='Figure 13 Correlation of High Yield OAS to S&P500 and VIX', sharing='public')
    
    
    ### Figure 14 Cummulative Return of S&P 500 Sector Index
    cum_equity_sector = (1+equity_sector).cumprod()-1
    
    
    trace1 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Materials'],
        name='Materials'
    )
    trace2 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Energy'],
        name='Energy'
    )
    trace3 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Financials'],
        name='Financials'
    )
    trace4 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Industrials'],
        name='Industrials'
    )
    trace5 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Technology'],
        name='Technology'
    )
    trace6 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Consumer Staples'],
        name='Consumer Staples'
    )
    trace7 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Real Estate'],
        name='Real Estate'
    )
    trace8 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Utilities'],
        name='Utilities'
    )
    trace9 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Health Care'],
        name='Health Care'
    )
    trace10 = go.Scatter(
        x=cum_equity_sector.index,
        y=100*cum_equity_sector['Consumer Discretionary'],
        name='Consumer Discretionary'
    )  
    
    
    data = [trace1,trace2,trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10]
    layout = go.Layout(
        title='Cummulative Return of Major S&P500 Component Indices',
        yaxis=dict(
            title='Cummulative Return',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1),
            ticksuffix='%'
        )

    )
            
    fig_14 = go.Figure(data=data, layout=layout)
    plot_url_14 = py.plot(fig_14, filename='Figure 14 Cummulative Return of Major S&P500 Component Indices', sharing='public')    
    
    
    ### Figure 15 Correlation between S&P 500 Sectors
    equity_sector_corr = equity_sector.rolling(window=260).corr()
    mask_sector = np.ones(equity_sector_corr.iloc[0].shape,dtype='bool')
    mask_sector[np.triu_indices(len(equity_sector_corr.iloc[0]))] = False
    equity_sector_corr_l = []
    for i in range(len(equity_sector_corr)):
        equity_sector_corr_l.append(equity_sector_corr.iloc[i][(equity_sector_corr.iloc[i]>-2)&mask_sector].sum().sum()/45)
    equity_sector_avg_corr = pd.DataFrame(equity_sector_corr_l, index=equity_sector.index, columns=['Average_Correlation'])
    equity_sector_avg_corr = equity_sector_avg_corr['2001-01-11 00:00:00':]

    # comm_sp_corr.plot()

    trace1 = go.Scatter(
        x=equity_sector_avg_corr.index,
        y=equity_sector_avg_corr['Average_Correlation'],
        name='Average Correlation'
        )

    data = [trace1]
    layout = go.Layout(
        title='Average Correlation of Different Component in S&P500',
        showlegend=True,
        yaxis=dict(
            title='Average Correlation',
            titlefont=dict(
                color=color1),
            tickfont=dict(
                color=color1)
        )

    )
            
    fig_15 = go.Figure(data=data, layout=layout)
    plot_url_15 = py.plot(fig_15, filename='Figure 15 Average Correlation of Different Component in S&P500', sharing='public')
    

    
    ###########################################
    


        