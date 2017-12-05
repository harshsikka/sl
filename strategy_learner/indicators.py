import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot

from util import get_data, plot_data

def author():
    return 'hsikka3'  

def calculate_prices(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')

  price = df.iloc[0:,1:]
  price = price.fillna(method='ffill').fillna(method='bfill')
  return price

def calculate_SMA(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')

  price = df.iloc[0:,1:]
  price = price.fillna(method='ffill').fillna(method='bfill')
  # JPMdf = JPMdf/JPMdf.iloc[0]
  rollingDF = pd.rolling_mean(price,window=20)
  return rollingDF

# def calculate_EMA(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
#   dates = pd.date_range(sd,ed)
#   df = get_data(symbols,dates,True,'Adj Close')

#   price = df.iloc[0:,1:]
#   price = price.fillna(method='ffill').fillna(method='bfill')
#   # JPMdf = JPMdf/JPMdf.ioc[0]
#   rollingDF = pd.rolling_mean(price,window=20)
#   return rollingDF

def calculate_upper_band(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')

  price = df.iloc[0:,1:]
  price = price.fillna(method='ffill').fillna(method='bfill')

  double_std = 2 * pd.rolling_std(price,window=20)

  upper_band = calculate_SMA(symbols,sd,ed) + double_std 

  return upper_band

def calculate_lower_band(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')

  price = df.iloc[0:,1:]
  price = price.fillna(method='ffill').fillna(method='bfill')

  double_std = 2 * pd.rolling_std(price,window=20)

  lower_band = calculate_SMA(symbols,sd,ed) - double_std

  return lower_band

def calculate_volatility(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
  dates = pd.date_range(sd,ed)
  df = get_data(symbols,dates,True,'Adj Close')
  price = df.iloc[0:,1:]

  volatility_df = pd.rolling_std(price,window=20)

  return volatility_df

# def calculate_momentum(symbols=['JPM'], sd='2008-01-01' , ed='2009-12-31'):
#   dates = pd.date_range(sd,ed)
#   df = get_data(symbols,dates,True,'Adj Close')
#   price = df.iloc[0:,1:]

def checkBBVal(price, sma, std):
    diff = (price-sma)
    bbval = diff/(2*std)
    return bbval




if __name__ == "__main__":
    ## first indicator is price, sma, and price/sma
    price = calculate_prices()
    price = price/price.iloc[0]

    sma = calculate_SMA()
    sma = sma/sma.iloc[20]
    

    price_sma = price/sma
    matplotlib.pyplot.plot(price, label = 'JPM')
    matplotlib.pyplot.plot(sma, label = 'SMA')
    matplotlib.pyplot.plot(price_sma, label = 'Price/SMA')
    matplotlib.pyplot.xlim([dt.datetime(2008,1,1), dt.datetime(2009,12,31)])
    matplotlib.pyplot.xticks(rotation=10)
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Value')
    matplotlib.pyplot.title('Normalized Price, SMA and Price/SMA')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('price_sma.pdf')

    matplotlib.pyplot.clf()

    ## second indicator is bbs
    upper_bb = calculate_upper_band()
    lower_bb = calculate_lower_band()
    price = calculate_prices()
    sma = calculate_SMA()

    matplotlib.pyplot.plot(price, label = 'JPM')
    matplotlib.pyplot.plot(sma, label = 'SMA')
    matplotlib.pyplot.plot(upper_bb, label = 'Upper Band')
    matplotlib.pyplot.plot(lower_bb, label = 'Lower Band')
    matplotlib.pyplot.xlim([dt.datetime(2008,1,1), dt.datetime(2009,12,31)])
    matplotlib.pyplot.xticks(rotation=10)
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Price')
    matplotlib.pyplot.title('Bollinger Bands')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('bollinger_bands.pdf')
    matplotlib.pyplot.clf()

    # to assist bbs, i'll plot bollinger value

    bb_val = checkBBVal(price,sma,calculate_volatility())
    matplotlib.pyplot.plot(bb_val, label = 'Bollinger Band Value')
    matplotlib.pyplot.xlim([dt.datetime(2008,1,1), dt.datetime(2009,12,31)])
    matplotlib.pyplot.xticks(rotation=10)
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Value')
    matplotlib.pyplot.title('Bollinger Band Value')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.grid(color='0.25', linestyle='--', linewidth=1)
    matplotlib.pyplot.savefig('bollinger_value.pdf')
    matplotlib.pyplot.clf()

    ## now, the third indicator, one that is considered unique, used will be Volatility
    volatility = calculate_volatility()
    price = calculate_prices()
    price = price/price.iloc[0]
    matplotlib.pyplot.plot(price, label = 'JPM')
    matplotlib.pyplot.plot(volatility, label = 'Volatility')
    matplotlib.pyplot.xlim([dt.datetime(2008,1,1), dt.datetime(2009,12,31)])
    matplotlib.pyplot.xticks(rotation=10)
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Value')
    matplotlib.pyplot.title('Volatility vs Normalized Price')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('volatility.pdf')
    matplotlib.pyplot.clf()
