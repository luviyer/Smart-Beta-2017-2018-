# Smart-Beta-2017-2018

This project intends to examine Smart Beta strategies e.g. value, momentum, quality, and minimum volatility
and see how such strategies, operated by various funds like BlackRock, JP Morgan, etc. compare with baseline strategies
that we can create using metrics and practices that seem to be consensus in the industry.

Index methodologies will be investigated to find the common metrics used by similar strategy funds, and regression
analysis will be performed to compare those strategies with ours. We intend to regress asset weights as well as 
historical performance.

Some questions we'd like to answer include, Are these Smart Beta Strategies just marketing gimmicks i.e. do they actually
provide some source of uncorrelated abnormal return that cannot be attributed to a simple factor strategy (our factor portfolio)?
What elements of portfolio construction contribute most to the abnormal returns of these portfolios?...

Currently, we have created Python scripts that will determine the universe of stocks in a given month (used for backtesting
from Jan. 1973 to Dec. 2016), compute metrics such as return on equity (found in MSCI, S&P, etc. index methodologies), 
for a quality strategy, and compute the quality factor score for each stock in the monthly universe.

More to come soon!   