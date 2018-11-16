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

jpm = quandl.get("EOD/JPM", start_date=start, end_date=end)
gs = quandl.get("EOD/GS", start_date=start, end_date=end)

plt.figure(figsize=(10,8))

plt.plot(jpm["Close"], label="JP Morgan")

plt.plot(gs["Close"], label="Goldman Sachs")

plt.title("JP Morgan and Goldman Sachs over 2016-2018")

plt.legend(loc=0)
plt.show()

newDF = pd.DataFrame()

newDF['JPM'] = jpm['Close']
newDF['GS'] = gs['Close']

newDF.head()

sns.heatmap(newDF.corr())

plt.figure(figsize=(15,10))
sns.jointplot(newDF['JPM'],newDF['GS'])
plt.legend(loc=0)
# plt.show()

newDF['Spread'] = newDF['JPM']-newDF['GS']

adf = adfuller(newDF['Spread'])

if adf[0] < adf[4]['1%']:
  print('Spread is cointegrated at 1 percent significance level')
elif adf[0] < adf[4]['5%']:
  print('Spread is cointegrated at 5 percent significance level')
elif adf[0] < adf[4]['10%']:
  print('Spread is cointegrated at 10 percent significance level')
else:
  print('Spread is not cointegrated')