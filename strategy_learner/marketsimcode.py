"""MC2-P1: Market simulator."""
## Name: Harsh Sikka UserID: hsikka3
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data


def author():
    return 'hsikka3'  

# Modified to only take in a dataframe of orders

def compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005):
    ## Data Frame of Orders
    ## old code taking orders from a file below
    # orders = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])

    orders = orders.sort_index()

    sym = orders.columns[0]
    order_df = orders.copy().drop([sym],axis=1)
    order_df = order_df.assign(Symbol = sym).assign(Order = 'BUY').assign(Shares = 0)
    
    for index, row in orders.iterrows():
        if row[0] > 0:
            order_df.loc[index,['Shares']] = row[0]
            order_df.loc[index,['Order']] = 'BUY'
        if row[0] < 0:
            order_df.loc[index,['Shares']] = -row[0]
            order_df.loc[index,['Order']] = 'SELL'

    # print order_df

    orders = order_df
            
    
    
    

    
    
    #grab symbols from orders for later use
    syms = orders.drop_duplicates('Symbol','first',False).values[:,0] # 0 is the symbols column
    # start and end dates
    
    start_date, end_date = orders.index[0], orders.index[-1]

    dates = pd.date_range(start_date, end_date)

    ## Data Frame of Prices
    prices = get_data(syms.tolist(), dates, True, 'Adj Close').assign(Cash = 1.0)
    prices = prices.fillna(method='ffill').fillna(method='bfill')

    
    # for index in orders.index:
    #     if (index in prices.index):
    #         start_date = index
    #         break

    # dates = pd.date_range(start_date, end_date)
    # prices = get_data(syms.tolist(), dates, True, 'Adj Close').assign(Cash = 1.0)
    # prices = prices.fillna(method='ffill').fillna(method='bfill')

    ## Data Frame of Trades

    trades = prices.copy()
    for column in trades:
        trades[column] = 0.0

    # loop through orders
    # for each order
        # if BUY
            ## store shares
            ## multiply shares by price on that date, multiply by -1, set to cash
        # if SELL
            ## store shares * -1
            ## multiply shares by price on that date, set to cash

     # set first cash to start val? i don't know if this is necessary

    for index, row in orders.iterrows():

        # check if order date is on a trading day

        if(index in prices.index): 
            impact_buy = 1.0 + impact
            impact_sell = 1.0 - impact

            if (row['Order'] == 'BUY'):
                trades.loc[index,row['Symbol']] += row['Shares']
                trades.loc[index,'Cash'] += row['Shares'] * ((prices.loc[index,row['Symbol']] * -1) * impact_buy)

            if (row['Order'] == 'SELL'):
                trades.loc[index,row['Symbol']] += row['Shares'] * -1
                trades.loc[index,'Cash'] += row['Shares'] * ((prices.loc[index,row['Symbol']]) * impact_sell)
            
            ## account for commission
            if (row['Shares'] != 0):
                trades.loc[index,'Cash'] -= commission
            

    ## Data Frame of Holdings
    temp_holdings = trades.copy()
    temp_holdings.loc[prices.index[0],'Cash'] = start_val + temp_holdings.loc[prices.index[0],'Cash']
    holdings = temp_holdings.cumsum(axis=0)

    ##Data Frame of Values
    values = prices * holdings
    
    # print values.sum(axis=1)
    return values.sum(axis=1)

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

# if __name__ == "__main__":
    
    