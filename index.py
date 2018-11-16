# finding pairs by brute force (without K-means clustering)

import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import seaborn as sns

import quandl
quandl.ApiConfig.api_key = 'S47WjtDP2RQtqNHzCbF-'

from statsmodels.tsa.stattools import adfuller

start='2016-01-01'
end='2018-01-01'

def begin():
  one_input = input('Enter Quandl code of the first stock: ')
  two_input = input('Enter Quandl code of the second stock: ')

  one = quandl.get(one_input, start_date=start, end_date=end)
  two = quandl.get(two_input, start_date=start, end_date=end)

  plt.figure(figsize=(10,8))

  plt.plot(one["Close"], label='First Stock')

  plt.plot(two["Close"], label='Second Stock')

  plt.title("Both stocks over 2016-2018")

  plt.legend(loc=0)
  plt.show()

  newDF = pd.DataFrame()

  newDF['one'] = one['Close']
  newDF['two'] = two['Close']

  newDF.head()

  sns.heatmap(newDF.corr())

  # plt.figure(figsize=(15,10))
  # sns.jointplot(newDF['one'],newDF['two'])
  # plt.legend(loc=0)
  # # plt.show()

  newDF['Spread'] = newDF['one']-newDF['two']

  adf = adfuller(newDF['Spread'])

  if adf[0] < adf[4]['1%']:
    print('Spread is cointegrated at 1 percent significance level')
  elif adf[0] < adf[4]['5%']:
    print('Spread is cointegrated at 5 percent significance level')
  elif adf[0] < adf[4]['10%']:
    print('Spread is cointegrated at 10 percent significance level')
  else:
    print('Spread is not cointegrated')
    
  play_again = input("Play again? y/n: ")
  if play_again == "y":
    game(states)
  else:
    print("Thanks! Come again!")
    
input("Welcome! Press Enter to begin.")

begin()
