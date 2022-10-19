import backtrader as bt
from urllib3.connectionpool import xrange


# Create a subclass of Strategy to define the indicators and logic
#
# class SmaCross(bt.Strategy):
#     # list of parameters which are configurable for the strategy
#     params = dict(
#         pfast=10,  # period for the fast moving average
#         pslow=30  # period for the slow moving average
#     )
#
#     def __init__(self):
#
#         sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
#         sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
#         self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
#
#     def next(self):
#         if not self.position:  # not in the market
#             size_ = (self.broker.get_cash() * 0.95) / self.data
#             if self.crossover > 0:  # if fast crosses slow to the upside
#                 self.buy(size=size_, exectype=bt.Order.StopTrail, trailpercent=0.01)  # enter long
#         else:
#             if self.crossover < 0:  # in the market & cross to the downside
#                 self.close()  # close long position


# Create a subclass of Strategy to define the indicators and logic

class Murticator(bt.Indicator):
    lines = ('Murticator', 'Up', 'Down')
    params = (('period', 12),)

    def __init__(self):
        self.diff = None
        self.test_min = None
        self.test_max = None
        self.signal1 = None
        self.Up = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.Down = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.atr = bt.ind.ATR(period=7)

    # params = (('value', 5),)
    def next(self):
        test = self.data.get(size=self.p.period)
        atrtest = self.atr[-1]
        if len(test) > self.p.period - 1:
            self.test_max = max(test)
            self.test_min = min(test)
            self.diff = self.test_max - self.test_min

            if self.diff < atrtest:
                self.signal1 = 1
            else:
                self.signal1 = 0

            if test[-1] >= self.test_max and self.signal1 == 1:
                self.lines.Murticator[0] = 1
            elif test[-1] <= self.test_min and self.signal1 == 1:
                self.lines.Murticator[0] = -1
            else:
                self.lines.Murticator[0] = 0

            if test[-1] >= self.test_max:
                self.lines.Up[0] = 1
                self.Up.append(1)
            else:
                self.lines.Up[0] = 0
                self.Up.append(0)
            if test[-1] <= self.test_min:
                self.lines.Down[0] = 1
                self.Down.append(1)
            else:
                self.lines.Down[0] = 0
                self.Down.append(0)


class ATR_SMA(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = (('period', 5),)

    def __init__(self):
        self.index = 0
        sma1 = bt.ind.SMA(period=9)  # fast moving average
        sma2 = bt.ind.SMA(period=1)
        self.crossover = bt.ind.CrossOver(sma2, sma1)
        murticator = Murticator(period=self.p.period)
        self.is_squeezing = murticator
        print()

    def next(self):
        if not self.position:
            if self.is_squeezing == 1:
                # if self.crossover > 0 :
                size_ = (self.broker.get_cash() * 0.90) / self.data
                self.buy(size=size_, exectype=bt.Order.StopTrail, trailpercent=0.01)  # enter long
                # self.buy()
        else:
            if self.is_squeezing == -1 and self.crossover < 0:
                self.close()
        # if self.is_squeezing[-2] == 1 and self.is_squeezing[-1] == 0:
        #     self.buy()
        # elif self.is_squeezing[-2] == 1 and self.is_squeezing[-1] == 0:
        #     self.sell()

        # if self.is_squeezing[-2] == 1 and self.is_squeezing[-1] == 0 and self.is_squeezing.Up[self.index] == 1:
        #     print("issqueeze:", self.is_squeezing[-2], self.is_squeezing.Up[self.index])
        #     self.buy()
        #
        # if self.is_squeezing[-2] == 1 and self.is_squeezing[-1] == 0 and self.is_squeezing.Down[self.index] == 1:
        #     print(self.is_squeezing[-2], self.is_squeezing[-1], self.is_squeezing.Down[self.index])
        #     self.sell()
        self.index += 1
        # if not self.position:
        #     if self.is_squeezing:
        #         self.buy()
        # else:
        #     if not self.is_squeezing:
        #         self.close()
        # if not self.position:  # not in the market
        #     if self.crossover > 0:  # if fast crosses slow to the upside
        #         size_ = (self.broker.get_cash() * 0.95) / self.data
        #         self.buy(size=size_, exectype=bt.Order.StopTrail, trailpercent=0.001)  # enter long
        # else:
        #     if self.crossover < 0:  # in the market & cross to the downside
        #         self.close()  # close long position
