class statarb(object):
  
  def__init__(self,df1, df2,ma,floor, ceiling,beta_lookback,start,end,exit_zscore=0):
  self.df1 = df1
  self.df2 = df2
  self.df = pd.DataFrame(index = df1.index)
  self.ma = ma
  self.floor = floor
  self.ceiling = ceiling
  self.Close = 'Close Long'
  self.Cover = 'Cover Short'
  self.exit_zscore = exit_zscore
  self.beta_lookback = beta_lookback
  self.start = start
  self.end = end

  def create_spread(self):

    self.df['X'] = self.df1['Close']
    self.df['Y'] = self.df2['Close']

    self.df['cov'] = pd.rolling_cov(self.df['X'],self.df['Y'],self.beta_lookback)
    self.df['var'] = pd.rolling_var(self.df['Y'],self.beta_lookback)
    self.df['beta'] = self.df['cov']/self.df['var']

    self.df['Hedge Ratio'] = self.df['beta']

    self.df['Spread'] = self.df['X'] - (self.df['Hedge Ratio']*self.df['Y'])
    self.df['Spread2'] = self.df['Y'] - (self.df['Hedge Ratio']*self.df['X'])

    return self.df

  def check_for_cointegration(self):
    coint = adfuller(self.df['Spread'].dropna())
    if coint[0] < coint[4]['1%']:
      print('Spread is cointegrated at 1 percent significance level')
    elif coint[0] < coint[4]['5%']:
      print('Spread is cointegrated at 5 percent significance level')
    elif coint[0] < coint[4][10%]:
      print('Spread is cointegrated at the 10 percent significance level')
    else:
      print('Spread is not cointegrated')

    return

  def generate_signals(self):
    self.df['Z-Score'] = (self.df['Spread'] - self.df['Spread'].rolling(window = self.ma).mean())/self.df['Spread'].rolling(window = self.ma).std()

    self.df['Priod Z-Score'] = self.df['Z-Score'].shift(1)

    self.df['Long Signal'] = (self.df['Z-Score'] <= self.floor)*1.0
    self.df['Short Signal'] = (self.df['Z-Score'] >= self.ceiling)*1.0
    self.df['Exit'] = (self.df['Z-Score'] <= self.exit_zscore)*1.0

    self.df['In Long'] = 0.0
    self.df['In Short'] = 0.0

    self.enter_long = 0
    self.enter_short = 0

    for 1,value in enumerate(self.df.iterrows()):
      if value[1]['Long Signal'] == 1.0:
        self.enter_long=1
      if value[1]['Short Signal'] == 1.0:
        self.enter_short = 1
      if value[1]['Exit'] == 1.0:
        self.enter_long=0
        self.enter_short=0
      
      self.df.iloc[i]['In Long']=self.enter_long
      self.df.iloc[i]['In Short']=self.enter_short
      
    return self.df

  def create_returns(self, allocation,pair_name):
    self.allocation = allocation
    self.pair = pair_name

    self.portfolio = pd.DataFrame(index = self.df.index)
    self.portfolio['Positions'] = self.df['Long Signal'] - self.df['Short Signal']
    self.portfolio['X'] = 1.0*self.df['X']*self.portfolio['Positions']
    self.portfolio['Y'] = self.df['Y']*self.portfolio['Positions']
    self.portfolio['Total'] = self.portfolio['X']+self.portfolio['Y']

    self.portfolio['Returns'] = self.portfolio['Total'].pct_change()
    self.portfolio['Returns'].fillna(0.0,inplace=True)
    self.portfolio['Returns'].replace([np.inf,-np.inf],0.0,inplace=True)
    self.portfolio['Returns'].replace(-1.0,0.0,inplace=True)

    self.mu=(self.portfolio['Returns'].mean())
    self.sigma=(self.portfolio['Returns'].std())
    self.Sharpe=(self.mu-0.005)/self.sigma
    self.portfolio['Win']=np.where(self.portfolio['Returns']>0,1,0)
    self.portfolio['Loss']=np.where(self.portfolio['Returns']<0,1,0)
    self.wins=self.portfolio['Win'].sum()
    self.losses=self.portfolio['Loss'].sum()
    self.total_trades = self.wins + self.losses
    
    self.win_loss_ratio=(self.wins/self.losses)

    self.prob_of_win=(self.wins/self.total_trades)
    self.prob_of_loss=(self.losses/self.total_trades)

    self.avg_win_return=(self.portfolio['Returns']>0).mean()
    self.avg_loss_return=(self.portfolio['Returns']<0).mean()
    self.payout_ratio=(self.avg_win_return/self.avg_loss_return)

    self.portfolio['Returns']=(self.portfolio['Returns']+1.0).cumprod()
    self.portfolio['Trade Returns'] = (self.portfolio['Total'].pct_change())
    self.portfolio['Portfolio Value'] = (self.allocation*self.portfolio['Returns'])
    self.portfolio['Portfolio Returns'] = self.portfolio['Portfolio Value'].pct-change()
    self.portfolio['Initial Value']=self.allocation

    with plt.style.context(['bmh','seaborn-paper']):
      plt.plot(self.portfolio['Portfolio Value'])
      plt.plot(self.portfolio['Initial Value'])
      plt.title('StatArb Pair%s Strategy Returns %s to %s'%(self.pair,self.start,self.end))
      plt.legend(loc=0)
      plt.tight_layout()
      plt.show()

    return

    strategy_kmeans = KMeans(n_clusters=100)

    strategy_kmeans.fit(features.fillna(0))

    