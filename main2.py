import json

import backtrader as bt
import requests
from tvDatafeed import TvDatafeed, Interval

from st_smacross import ATR_SMA

x = requests.get('https://scanner.tradingview.com/turkey/scan')

y = json.loads(x.content)
symbol_names = list()
exchange_names = set()
for i in range(y['totalCount']):
    exchange_names.add(y['data'][i]['s'].split(":")[0])
    symbol_names.append(y['data'][i]['s'].split(":")[1])

tv = TvDatafeed()


index = 0
for symbol in symbol_names:
    cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
    cerebro.broker.setcash(10000.0)
    # Create a data feed
    # if index!=3:
    #     index+=1
    # else:
    #     break
    print("symbol_name:",symbol)
    older_values = tv.get_hist(symbol="TATGD", exchange="BIST", interval=Interval.in_daily, n_bars=240)
    data = bt.feeds.PandasData(dataname=older_values)
    cerebro.broker.setcommission(commission=1.5, margin=1)
    cerebro.adddata(data)  # Add the data feed
    cerebro.addstrategy(ATR_SMA, period=7)  # Add the trading strategy
    cerebro.run()  # run it all
    cerebro.plot()  # and plot it with a single command