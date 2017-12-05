## Name: Harsh Sikka UserID: hsikka3
import numpy as np
import datetime as dt
import pandas as pd
import util as ut
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot
import random
from indicators import calculate_prices, calculate_lower_band, calculate_upper_band, calculate_SMA, calculate_volatility
from ManualStrategy import testPolicy, benchmark, calculate_period_returns, print_stats
from marketsimcode import compute_portvals
import QLearner as ql
import StrategyLearner as sl

def generate_charts():

    

    learner_000 = sl.StrategyLearner()
    learner_000.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_000 = learner_000.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    print trades_000
    portfolio_000 = compute_portvals(trades_000,100000,0,0)
    first_portfolio_000 = portfolio_000.iloc[0]
    matplotlib.pyplot.plot(portfolio_000/first_portfolio_000, label='Impact 0.000', color='k')
    
    learner_001 = sl.StrategyLearner(impact=0.001)
    learner_001.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_001 = learner_001.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_001 = compute_portvals(trades_001,100000,0,0.001)
    first_portfolio_001 = portfolio_001.iloc[0]
    matplotlib.pyplot.plot(portfolio_001/first_portfolio_001, label='Impact 0.001', color='r')

    learner_005 = sl.StrategyLearner(impact=0.005)
    learner_005.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_005 = learner_005.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_005 = compute_portvals(trades_005,100000,0,0.005)
    first_portfolio_005 = portfolio_005.iloc[0]
    matplotlib.pyplot.plot(portfolio_005/first_portfolio_005, label='Impact 0.005', color='c')

    learner_01 = sl.StrategyLearner(impact=0.01)
    learner_01.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_01 = learner_01.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_01 = compute_portvals(trades_000,100000,0,0.01)
    first_portfolio_01 = portfolio_01.iloc[0]
    matplotlib.pyplot.plot(portfolio_01/first_portfolio_01, label='Impact 0.01', color='b')
    
    learner_05 = sl.StrategyLearner(impact=0.05)
    learner_05.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_05 = learner_05.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_05 = compute_portvals(trades_001,100000,0,0.05)
    first_portfolio_05 = portfolio_05.iloc[0]
    matplotlib.pyplot.plot(portfolio_05/first_portfolio_05, label='Impact 0.05', color='g')

    learner_1 = sl.StrategyLearner(impact=0.1)
    learner_1.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_1 = learner_01.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_1 = compute_portvals(trades_1,100000,0,0.1)
    first_portfolio_1 = portfolio_1.iloc[0]
    matplotlib.pyplot.plot(portfolio_1/first_portfolio_1, label='Impact 0.1', color='m')

    matplotlib.pyplot.xlim([dt.datetime(2008,1,1),dt.datetime(2009,12,31)])
    matplotlib.pyplot.xticks(rotation=10) 
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Normalized Portfolio Value')
    matplotlib.pyplot.title('Impact Effect on Portfolios - In Sample')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('experiment2.pdf')



def alt_generate():
    learner_000 = sl.StrategyLearner()
    learner_000.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_000 = learner_000.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_000 = compute_portvals(trades_000,100000,0,0)
    first_portfolio_000 = portfolio_000.iloc[0]
    matplotlib.pyplot.plot(portfolio_000/first_portfolio_000, label='Impact 0.000', color='k')
    trades_000_count = 0
    # print trades_000.index
    for x in trades_000.index:
        if trades_000.loc[x][0] != 0:
          trades_000_count+=1

    learner_001 = sl.StrategyLearner(impact=0.001)
    learner_001.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_001 = learner_001.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_001 = compute_portvals(trades_001,100000,0,0.001)
    first_portfolio_001 = portfolio_001.iloc[0]
    matplotlib.pyplot.plot(portfolio_001/first_portfolio_001, label='Impact 0.001', color='r')

    trades_001_count = 0
    for k in trades_001.index:
        if trades_001.loc[k][0] != 0:
          trades_001_count+=1
    
    learner_005 = sl.StrategyLearner(impact=0.005)
    learner_005.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_005 = learner_005.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_005 = compute_portvals(trades_005,100000,0,0.005)
    first_portfolio_005 = portfolio_005.iloc[0]
    matplotlib.pyplot.plot(portfolio_005/first_portfolio_005, label='Impact 0.005', color='c')

    trades_005_count = 0
    for y in trades_005.index:
        if trades_005.loc[y][0] != 0:
          trades_005_count+=1

    learner_025 = sl.StrategyLearner(impact=0.025)
    learner_025.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_025 = learner_025.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_025 = compute_portvals(trades_025,100000,0,0.025)
    first_portfolio_025 = portfolio_025.iloc[0]
    matplotlib.pyplot.plot(portfolio_025/first_portfolio_025, label='Impact 0.025', color='c')

    trades_025_count = 0
    for t in trades_025.index:
        if trades_025.loc[t][0] != 0:
          trades_025_count+=1

    learner_01 = sl.StrategyLearner(impact=0.01)
    learner_01.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_01 = learner_01.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_01 = compute_portvals(trades_01,100000,0,0.01)
    first_portfolio_01 = portfolio_01.iloc[0]
    matplotlib.pyplot.plot(portfolio_01/first_portfolio_01, label='Impact 0.01', color='m')

    trades_01_count = 0
    for z in trades_01.index:
        if trades_01.loc[z][0] != 0:
          trades_01_count+=1

    learner_05 = sl.StrategyLearner(impact=0.05)
    learner_05.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    trades_05 = learner_05.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    portfolio_05 = compute_portvals(trades_05,100000,0,0.05)
    first_portfolio_05 = portfolio_05.iloc[0]
    matplotlib.pyplot.plot(portfolio_05/first_portfolio_05, label='Impact 0.05', color='g')

    trades_05_count = 0
    for i in trades_05.index:
        if trades_05.loc[i][0] != 0:
          trades_05_count+=1

    matplotlib.pyplot.xlim([dt.datetime(2008,1,1),dt.datetime(2009,12,31)])
    matplotlib.pyplot.xticks(rotation=10) 
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Normalized Portfolio Value')
    matplotlib.pyplot.title('Impact Effect on Portfolios - In Sample')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('experiment2.pdf')

    print "impact 0.000 ->"
    print trades_000_count
    print_stats(portfolio_000)
    print "impact 0.001 ->" 
    print trades_001_count
    print_stats(portfolio_001)
    print "impact 0.005 ->"
    print trades_005_count
    print_stats(portfolio_005)
    print "impact 0.01 ->"
    print trades_01_count
    print_stats(portfolio_01)
    print "impact 0.025 ->"
    print trades_025_count
    print_stats(portfolio_025)
    print "impact 0.05 ->"
    print trades_05_count
    print_stats(portfolio_05)


if __name__ == "__main__":
    # generate_charts()
    alt_generate()