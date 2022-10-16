
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

api_url = 
#global variables
price_data = {}
normalized_data = {}
log_return = {}
cryptos = []

def process(event):
  resp = efficientFrontier([], 500)
  return resp


def get_crypto_data(coin, days):
  json_url = api_url.format(coin, days)
  # resp = await pyfetch(json_url, method="GET", headers=headers)
  # bjson = await resp.json()
  prices = bjson["prices"]
  df_price = pd.DataFrame(prices)  
  df_price = df_price.rename({0: 'date', 1: 'price'}, axis=1)  # new method
  df_price = df_price.set_index('date')
  return df_price

def plotPriceComparison(crypto, days):
  crypto_data = {}
  for coin in crypto:
    crypto_price_df = get_crypto_data(coin, days)
    crypto_data[coin] = crypto_price_df
  dfp = pd.concat(crypto_data, axis=1)
  dfp.columns = crypto
  
  global price_data
  price_data = dfp
  
  global normalized_data
  normalized_data = dfp/dfp.iloc[0]

  crypto_daily_ret = dfp.pct_change(1)  # Daily return
  log_ret = np.log(dfp/dfp.shift(1))  #Log return

  global log_return 
  log_return = log_ret
  sharpRatio()

def barchart(log_ret):
  fig, ax = plt.subplots(figsize=(10, 5))
  plt.hist(log_ret, bins=100)
  plt.tight_layout()
  plt.title('Return Frequency')
  plt.xlabel('Return %')
  plt.ylabel('Frequency')
  plt.legend(log_ret.columns)
  print("Basic Statistics:")
  log_ret.describe().transpose()
  print("Covariance:")
  print(log_ret.cov())
  global log_return
  log_return = log_ret

  
def efficientFrontier(crypto, days):
  global cryptos
  cryptos = crypto
  try:
    loop = asyncio.get_running_loop()
  except RuntimeError:
    loop = None
  if loop and loop.is_running():
    tsk = loop.create_task(plotPriceComparison(crypto, days))
    tsk.add_done_callback(
      lambda t: t.result()
    )
  else:
    print('Starting new event loop')
    asyncio.run(plotPriceComparison(crypto, days))
  

def sharpRatio():
  global log_return
  log_ret = log_return
  global normalized_data
  dfp = normalized_data
  global cryptos
  crypto = cryptos
  
  # <!-- log_ret.describe().transpose()
  # log_ret.mean() * 600
  # log_ret.cov() -->
  num_ports = 1500
  all_weights = np.zeros((num_ports,len(dfp.columns)))
  ret_arr = np.zeros(num_ports)
  vol_arr = np.zeros(num_ports)
  sharpe_arr = np.zeros(num_ports)

  for ind in range(num_ports):
    # Create Random Weights
    weights = np.array(np.random.random(len(dfp.columns)))
    # Rebalance Weights
    weights = weights / np.sum(weights)
    # Save Weights
    all_weights[ind,:] = weights
    # Expected Return
    ret_arr[ind] = np.sum((log_ret.mean() * weights) *365)
    # Expected Variance
    vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(log_ret.cov() * 365, weights)))
    # Sharpe Ratio
    sharpe_arr[ind] = ret_arr[ind]/vol_arr[ind]
  sharpe_arr.max()
  sharpe_arr.argmax()

  optimal_ratio = list(all_weights[sharpe_arr.argmax(),:])
  optimal_portfolio = {}
  i = 0
  for coin in crypto:
    optimal_portfolio[coin] = str(round(optimal_ratio[i] * 100)) + '%'
    i += 1

  max_sr_ret = ret_arr[sharpe_arr.argmax()]
  max_sr_vol = vol_arr[sharpe_arr.argmax()]
  maxiums = {}
  maxiums['Max_SharpeRatio_Return'] = max_sr_ret
  maxiums['Max_SharpeRatio_Volitility'] = max_sr_vol

  fig, ax = plt.subplots(figsize=(7, 4))
  plt.scatter(vol_arr,ret_arr,c=sharpe_arr,cmap='plasma')
  plt.colorbar(label='Sharpe Ratio')
  plt.xlabel('Volatility')
  plt.ylabel('Return')
  plt.title('Efficient Frontier: Sharpe Ratio')
  plt.scatter(max_sr_vol, max_sr_ret, c='red', s=50, edgecolors='black')

