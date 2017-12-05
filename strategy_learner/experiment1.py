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


def testCode():

    
    manual_strategy = compute_portvals(testPolicy(),100000)
    benchmark_val = compute_portvals(benchmark(),100000)
    learner = sl.StrategyLearner()
    learner.addEvidence('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    q_trades = learner.testPolicy('JPM',dt.datetime(2008,1,1),dt.datetime(2009,12,31),100000)
    learner_strategy = compute_portvals(q_trades,100000)

    first_benchmark = benchmark_val.iloc[0]
    first_manual_strategy = manual_strategy.iloc[0]
    first_learner_strategy = learner_strategy.iloc[0]
    
    # print benchmark_val
    # print manual_strategy
    # print learner_strategy

    print '                        '
    print '                        '
    print '                        '


    print 'Benchmark - In Sample'
    print_stats(benchmark_val)
    print '_______________________________________'
    print 'Manual Strategy - In Sample'
    print_stats(manual_strategy)
    print '_______________________________________'
    print 'Learner Strategy - In Sample'
    print_stats(learner_strategy)
    print '_______________________________________'
    price_calc = calculate_prices()
    print 'Cumulative Return of JPM, Out of Sample -> ', price_calc.iloc[-1]/price_calc.iloc[0]

    matplotlib.pyplot.plot(benchmark_val/first_benchmark, label='Benchmark', color='b')
    matplotlib.pyplot.plot(manual_strategy/first_manual_strategy, label='Manual Rule Based Trader', color='k')
    matplotlib.pyplot.plot(learner_strategy/first_learner_strategy, label='Strategy Learner Trader', color='g')
    matplotlib.pyplot.xlim([dt.datetime(2008,1,1),dt.datetime(2009,12,31)])
    matplotlib.pyplot.xticks(rotation=10) 
    matplotlib.pyplot.xlabel('Date')
    matplotlib.pyplot.ylabel('Normalized Portfolio Value')
    matplotlib.pyplot.title('Portfolio Comparison - In Sample')
    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('experiment1.pdf')

    ## potential for out of sample chart

if __name__ == "__main__":
    testCode()
    