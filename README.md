Arbitrage attempts to take advantage of discrepancies in the stock market.
One common way people do this is by find stocks that seem to be "cointegrated," meaning they tend to fluctuate together with a difference under ~5%. 
Then, when the two interrelated stocks start to diverge at some point in time, one would theoretically buy the lower one and short the higher one, because you would expect both to eventually return to the mean. So, if you bought the lower one, you would make money when it goes back up and vice versa.

The first part of my project allows the user to enter two stocks (using codes from Quandl) and see how cointegrated they are with 1) a graphical display, and 2) a mathematical calculation. This is the index.py file.

The second part would be to automatically go through and find cointegrated stocks as well as statistical arbitrage situations in those stocks. It is not yet working, but it is the index2.py file.
