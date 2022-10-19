import datetime
import json

import backtrader as bt
import matplotlib.pyplot as plt
import requests
import tradingview_ta
from tradingview_ta import TA_Handler
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
older_values = tv.get_hist(symbol='EREGL', exchange="BIST", interval=Interval.in_daily, n_bars=240)
y1 = older_values['close'].values
x1 = older_values['close'].index
begin_date = x1.array[0]
low_list = list()
high_list = list()
low_list_date = list()
high_list_date = list()
margin = 0.0001
one_minute = datetime.timedelta(minutes=1)

for i in range(len(x1.array)):
    x1.array[i] = begin_date + datetime.timedelta(minutes=i)

# min_val = y1.min()
# max_val = y1.max()
# min_val_index = np.where(y1 == min_val)[0][0]
# max_val_index = np.where(y1 == max_val)[0][0]
# min_val_time = x1[np.where(y1 == min_val)]
# max_val_time = x1[np.where(y1 == max_val)]
#

# plt.plot(min_val_time, min_val, "bo")
# plt.plot(max_val_time, max_val, "ro")
# temp_high = min_val
# temp_low = max_val

for i in range(len(y1) - 2):
    if y1[i] < y1[i + 1] and y1[i + 1] > y1[i + 2]:
        high_list.append(y1[i + 1])
        high_list_date.append(x1.array[i + 1])
    if y1[i] > y1[i + 1] and y1[i + 2] > y1[i + 1]:
        low_list.append(y1[i + 1])
        low_list_date.append(x1.array[i + 1])
    if y1[i] == y1[i + 1] and y1[i + 2] < y1[i + 1]:
        high_list.append(y1[i + 1])
        high_list_date.append(x1.array[i + 1])
    if y1[i] == y1[i + 1] and y1[i + 2] > y1[i + 1]:
        low_list.append(y1[i + 1])
        low_list_date.append(x1.array[i + 1])


plt.plot(x1, y1)
plt.plot(high_list_date, high_list, 'ro')
plt.plot(low_list_date, low_list, 'bo')
aa=high_list_date[0:2]
bb=high_list[0:2]
plt.plot(aa,bb)

plt.show()

cerebro = bt.Cerebro()  # create a "Cerebro" engine instance
cerebro.broker.setcash(10000.0)
# Create a data feed
data = bt.feeds.PandasData(dataname=older_values)

cerebro.adddata(data)  # Add the data feed
cerebro.broker.setcommission(commission=1.5, margin=1)
cerebro.addstrategy(ATR_SMA, period=8)  # Add the trading strategy
cerebro.run()  # run it all
cerebro.plot()  # and plot it with a single command

handler = TA_Handler(
    symbol="THYAO",
    exchange="BIST",
    screener="turkey",
    interval="1m"
)
tesla = TA_Handler(
    symbol="TSLA",
    screener="america",
    exchange="NASDAQ",
    interval=tradingview_ta.Interval.INTERVAL_1_DAY,
    # proxies={'http': 'http://example.com:8080'} # Uncomment to enable proxy (replace the URL).
)
print(tesla.get_analysis().summary)

analysis = handler.get_analysis()
print(analysis.indicators['close'])
print(analysis.indicators['open'])
print(analysis.indicators['high'])
print(analysis.indicators['low'])
print(analysis.indicators['volume'])
# Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}
