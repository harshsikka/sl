## Name: Harsh Sikka UserID: hsikka3
import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot

from util import get_data, plot_data
from indicators import calculate_prices, calculate_lower_band, calculate_upper_band, calculate_SMA, calculate_volatility
from marketsimcode import compute_portvals

def checkBBVal(price, sma, std):
    diff = (price-sma)
    bbval = diff/(2*std)
    return bbval

def author():
    return 'hsikka3'  



def testPolicy(symbol = 'JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31), sv = 100000):
    prices = calculate_prices([symbol],sd,ed)
    orders_df = prices.copy().drop([symbol],axis=1).assign(Shares = 0)

    sma = calculate_SMA([symbol],sd, ed)
    std = calculate_volatility([symbol],sd,ed)

    current_holdings = 0
    for i in range(0,len(prices.values[:,0])):

      if(i==0):
        
        orders_df.loc[orders_df.index[i],'Shares'] = -1000
        current_holdings = -1000
        
        #do nothing in this iteration
      elif(i >= 21):
        #get current price, current sma, and current std for equation
        curr_price = prices.loc[prices.index[i],'JPM']
        curr_sma = sma.loc[sma.index[i], 'JPM']
        curr_std = std.loc[std.index[i], 'JPM']

        bb_val = checkBBVal(curr_price,curr_sma,curr_std)
        
        if(bb_val < -1):
          if(current_holdings < 1000  and curr_std < 2):
            
            orders_df.loc[orders_df.index[i],'Shares'] = 2000
            current_holdings += 2000
            
            # matplotlib.pyplot.axvline(x=orders_df.index[i], color='g', linestyle='--')
          
        elif(bb_val > 1):
          if(current_holdings > -1000  and curr_std < 2):
            
            orders_df.loc[orders_df.index[i],'Shares'] = -2000
            current_holdings -= 2000
            
            # matplotlib.pyplot.axvline(x=orders_df.index[i], color='r', linestyle='--')
          
      else:
        
        orders_df.loc[orders_df.index[i],'Shares'] = 0
    #   print current_holdings
    #   print orders_df.index[i]
    # print orders_df
    orders_df.columns = [symbol]
    
    return orders_df

    

  

def benchmark(symbol = 'JPM', sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,12,31)):
    prices = calculate_prices([symbol],sd,ed)
    
    benchmark_df = prices.copy().drop([symbol],axis=1)
    benchmark_df = benchmark_df.assign(Shares = 0)
    benchmark_df.iloc[0,0] = 1000

    # orders = pd.read_csv('./benchmark.csv', index_col='Date', parse_dates=True)
    # print orders

    benchmark_df.columns = [symbol]
    return benchmark_df

def calculate_period_returns(df, period):
    if period == 252:
        period_returns = (df/df.shift(1)) - 1
        period_returns.ix[0] = 0
        period_returns = period_returns[1:] 
    #fill in other periods here
    
    return period_returns

def print_stats(df):
    print '--------- Portfolio Information -----------'
    cum_return = df.iloc[-1]/df.iloc[0] - 1
    daily_returns = calculate_period_returns(df,252)
    mean_dr = daily_returns.mean()
    std_dr = daily_returns.std()
    print 'Cumulative Return -> ', cum_return
    print 'Mean of Daily Returns ->', mean_dr
    print 'Standard Deviation of Daily Returns ->', std_dr
    print 'Final Portfolio Value ->', df[-1]

def testCode():

    # old manual strat code
    ## the in sample plots
    benchmark_val = compute_portvals(benchmark(),100000)
    # print benchmark_val
    # first_benchmark = benchmark_val.iloc[0]

    manual_strategy = compute_portvals(testPolicy(),100000)
    # print manual_strategy
    first_manual_strategy = manual_strategy.iloc[0]
    print '                        '
    print '                        '
    print '                        '

   

    print 'Benchmark - In Sample'
    print_stats(benchmark_val)
    print '_______________________________________'
    print 'Manual Strategy - In Sample'
    print_stats(manual_strategy)
    print '_______________________________________'
    price_calc = calculate_prices()
    print 'Cumulative Return of JPM, Out of Sample -> ', price_calc.iloc[-1]/price_calc.iloc[0]
    

    matplotlib.pyplot.plot(benchmark_val/first_benchmark, label='Benchmark', color='b')
    matplotlib.pyplot.plot(manual_strategy/first_manual_strategy, label='Manual Rule Based Trader', color='k')
    matplotlib.pyplot.xlim([dt.datetime(2008,1,1),dt.datetime(2009,12,31)])
    matplotlib.pyplot.xticks(rotation=10)
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Normalized Portfolio Value')
    matplotlib.pyplot.title('Portfolio Comparison - In Sample')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('manual_strategy_in_sample.pdf')
   
    matplotlib.pyplot.clf()


    # the out of sample plots, simply exit out of the in sample and out will be presented
    out_benchmark = compute_portvals(benchmark('JPM', dt.datetime(2010,1,1), dt.datetime(2011,12,31)),100000)
    # print out_benchmark
    out_first_benchmark = out_benchmark.iloc[0]

    out_manual_strategy = compute_portvals(testPolicy('JPM', dt.datetime(2010,1,1), dt.datetime(2011,12,31)),100000)
    # print out_manual_strategy
    out_first_manual_strategy = out_manual_strategy.iloc[0]

    print '                        '
    print '                        '
    print '                        '

    print 'Benchmark - Out of Sample'
    print_stats(out_benchmark)
    print '_______________________________________'
    print 'Manual Strategy - Out of Sample'
    print_stats(out_manual_strategy)
    print '_______________________________________'
    price_calc = calculate_prices(['JPM'],'2010-01-01','2011-12-31')
    print 'Cumulative Return of JPM, Out of Sample -> ', price_calc.iloc[-1]/price_calc.iloc[0] - 1

    matplotlib.pyplot.plot(out_benchmark/out_first_benchmark, label='Benchmark', color='b')
    matplotlib.pyplot.plot(out_manual_strategy/out_first_manual_strategy, label='Manual Rule Based Trader', color='k')
    matplotlib.pyplot.xlim([dt.datetime(2010,1,1), dt.datetime(2011,12,31)])
    matplotlib.pyplot.xticks(rotation=10)
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Normalized Portfolio Value')
    matplotlib.pyplot.title('Portfolio Comparison - Out of Sample')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('manual_strategy_out_sample.pdf')
    


if __name__ == "__main__":
    testCode()
    
    