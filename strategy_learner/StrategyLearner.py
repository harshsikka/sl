"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch
"""
## Name: Harsh Sikka UserID: hsikka3
import numpy as np
import datetime as dt
import pandas as pd
import util as ut
from indicators import calculate_prices, calculate_lower_band, calculate_upper_band, calculate_SMA, calculate_volatility
import QLearner as ql
from ManualStrategy import testPolicy, benchmark, calculate_period_returns
from marketsimcode import compute_portvals
import random

def checkBBVal(price, sma, std):
    diff = (price-sma)
    bbval = diff/(2*std)
    return bbval

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact

    def author(self):
        return 'hsikka3'  

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "IBM", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,1,1), \
        sv = 10000): 

        self.tradecount = 0
        # add your code to do learning here

        #pseudocode
        ## first day
          # calculate indicators, use querysetstate with the indicators
        ## rest of days
          # calculate reward
          # query q learner for action using indicators and reward
        
        steps = 100
        

        prices = calculate_prices([symbol],sd,ed)
        sma = calculate_SMA([symbol],sd,ed)
        
        orders_df = prices.copy().drop([symbol],axis=1).assign(Shares = 0)
        
        
        bbval = checkBBVal(prices,sma,calculate_volatility([symbol],sd,ed))
        bbval = bbval.fillna(0)
        disc_thresholds = []

        current_holdings = 0

        self.learner = ql.QLearner(num_states=steps, \
        num_actions = 3, \
        alpha = 0.2, \
        gamma = 0.9, \
        rar = 0.9, \
        radr = 0.99, \
        dyna = 0, \
        verbose = False)
        
        prices_ratio_1 = prices[:-1].values
        prices_ratio_2 = prices[1:]/prices_ratio_1
        dr = prices_ratio_2 - 1 # daily returns calculation

        ## discretize our indicator using prof's method
        bb_copy = bbval.copy()
        stepsize = bbval.shape[0]/steps
        bbval_sorted = bb_copy.sort_values(bb_copy.columns[0],ascending=True)

        bb_copy = bbval.copy()
        

        for x in range(0,steps - 1):
            y = x + 1
            # print bbval_sorted.iloc[y*stepsize][0]
            disc_thresholds.append(bbval_sorted.iloc[y*stepsize][0])

        count = 0
        # for i in bbval.itertuples():
            
            
        #     for j in disc_thresholds:
                    
        #         past_j = j - 1
        #         if i[1] < j[0] and i[1] >= past_j[0]:
        #             bb_copy.iloc[count] = j
        
        # print disc_thresholds
        discretized_bb = np.digitize(bb_copy.values,disc_thresholds)
        
        # print discretized_bb[0][0]
        epochs = 50
        current = 0
        
        while current < epochs:
            checkdate = 0
            holdings = 0
            for index, row in orders_df.iterrows():
                state = discretized_bb[checkdate][0]
                if checkdate == 0:
                    self.learner.querysetstate(state)
                    orders_df.loc[index] = -1000
                    holdings = -1000
                else:
                    reward_component = dr.loc[index][0] * holdings
                    reward = reward_component - self.impact*reward_component

                    action = self.learner.query(state,reward)
                    if action == 0 and holdings > -1000:
                        orders_df.loc[index] = -2000
                        holdings = -1000
                    elif action == 1:
                        orders_df.loc[index] = 0
                    elif action == 2 and holdings < 1000:
                        orders_df.loc[index] = 2000
                        holdings = 1000
                # print holdings    
                
                    # print action

                checkdate+=1
            current+=1

        # print orders_df
        return orders_df
                

                
        

        # example usage of the old backward compatible util function
        # syms=[symbol]
        # dates = pd.date_range(sd, ed)
        # prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        # prices = prices_all[syms]  # only portfolio symbols
        # prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        # if self.verbose: print prices
  
        # example use with new colname 
        # volume_all = ut.get_data(syms, dates, colname = "Volume")  # automatically adds SPY
        # volume = volume_all[syms]  # only portfolio symbols
        # volume_SPY = volume_all['SPY']  # only SPY, for comparison later
        # if self.verbose: print volume

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "IBM", \
        sd=dt.datetime(2009,1,1), \
        ed=dt.datetime(2010,1,1), \
        sv = 10000):

        steps = 100

        dates = pd.date_range(sd, ed)

        prices = calculate_prices([symbol],sd,ed)
        sma = calculate_SMA([symbol],sd,ed)
        orders_df = prices.copy().drop([symbol],axis=1).assign(Shares = 0)

        bbval = checkBBVal(prices,sma,calculate_volatility([symbol],sd,ed))
        bbval = bbval.fillna(0)
        disc_thresholds = []

        current_holdings = 0

        ## discretize our indicator using prof's method
        bb_copy = bbval.copy()
        stepsize = bbval.shape[0]/steps
        bbval_sorted = bb_copy.sort_values(bb_copy.columns[0],ascending=True)

        bb_copy = bbval.copy()
        

        for x in range(0,steps - 1):
            y = x + 1
            # print bbval_sorted.iloc[y*stepsize][0]
            disc_thresholds.append(bbval_sorted.iloc[y*stepsize][0])

        discretized_bb = np.digitize(bb_copy.values,disc_thresholds)

        checkdate = 0
        holdings = 0
        for index, row in orders_df.iterrows():
            state = discretized_bb[checkdate][0]
            action = self.learner.querysetstate(state)
            if checkdate == 0:
                    orders_df.loc[index] = -1000
                    holdings = -1000
                    
            else:
                if action == 0 and holdings > -1000:
                    self.tradecount+=1
                    orders_df.loc[index] = -2000
                    holdings = -1000
                elif action == 1:
                    orders_df.loc[index] = 0
                elif action == 2 and holdings < 1000:
                    self.tradecount+=1
                    orders_df.loc[index] = 2000
                    holdings = 1000
            # print holdings
            checkdate+=1
        orders_df.columns = [symbol]
        return orders_df
        

        # here we build a fake set of trades
        # your code should return the same sort of data
        # dates = pd.date_range(sd, ed)
        # prices_all = ut.get_data([symbol], dates)  # automatically adds SPY
        # trades = prices_all[[symbol,]]  # only portfolio symbols
        # trades_SPY = prices_all['SPY']  # only SPY, for comparison later
        # trades.values[:,:] = 0 # set them all to nothing
        # trades.values[0,:] = 1000 # add a BUY at the start
        # trades.values[40,:] = -1000 # add a SELL 
        # trades.values[41,:] = 1000 # add a BUY 
        # trades.values[60,:] = -2000 # go short from long
        # trades.values[61,:] = 2000 # go long from short
        # trades.values[-1,:] = -1000 #exit on the last day
        # if self.verbose: print type(trades) # it better be a DataFrame!
        # if self.verbose: print trades
        # if self.verbose: print prices_all
        # return trades


if __name__=="__main__":
     learner = StrategyLearner(impact=0.005)
     learner.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
     q_trades = learner.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
     manual_trades = testPolicy()
    
     print '_________ Benchmark _________'
     print compute_portvals(benchmark(),100000,9.95,0.005)
     print '_________ Man Strat _________'
     print compute_portvals(manual_trades,100000,9.95,0.005)
     print '_________ Q Learner _________'
     print compute_portvals(q_trades,100000,9.95,0.005)
     

     
     


    ## to do, properly discretize values of bb_val, create state and pass to learner

    
     


