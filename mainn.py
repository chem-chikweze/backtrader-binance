#!/usr/bin/env python3
import time
import backtrader as bt
import datetime as dt
from ccxtbt import CCXTStore
from config import BINANCE
from strategies.structure import MarketStructure as ts
from utils import send_telegram_message, to_local_time
from indicators.zigzag import *


DEBUG = True


class CustomStrategy(bt.Strategy):
    buy_order = None

    def __init__(self):
        self.order = None
        self.last_operation = "BUY"
        self.status = "DISCONNECTED"
        self.nullzig = ZigZag(self.data)
        self.dataclose = self.datas[0].close

    def notify_data(self, data, status, *args, **kwargs):
        self.status = data._getstatusname(status)
        if status == data.LIVE:
            self.log("LIVE DATA - Ready to trade")
        else:
            print(dt.datetime.now().strftime("%d-%m-%y %H:%M"),
                  "notify_data: NOT LIVE - %s" % self.status)

    def next(self):
        if self.status != "LIVE":
            self.log("%s - $%.2f NOT LIVE" % (self.status, self.data0.close[0]))
            # print("not live")
            return

        if self.status == "LIVE":
            print(self.dataclose[0])
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return          

        # Check if we are in the market ince: 1639283400000
        if not self.position:
            if self.buy_order: # some order was pending
                self.cancel(self.buy_order)

            # do nothing if the trend is already in motion
            if not (self.nullzig.l.zigzag[0] >= 0) :
                ""
            else:   
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()
                send_telegram_message("sold {}  {}".format(self.dataclose[0], to_local_time()))

        else:
            # do nothing if the trend is already in motion
            if not (self.nullzig.l.zigzag[0] >= 0) :
                ""
            else:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # keep track of the created order to avoid a 2nd order
                self.sell_order = self.buy()
                send_telegram_message("bought {}  {}".format(self.dataclose[0], to_local_time()))


        print('*' * 5, 'NEXT:', bt.num2date(self.data0.datetime[0]), self.data0.close[0])

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                        (order.executed.price,
                         order.executed.value,
                         order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected %s' % order.status)
            self.last_operation = None

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        color = 'green'
        if trade.pnl < 0:
            color = 'red'

        self.log(('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm), color))

    def log(self, txt):
        if not DEBUG:
            return

        dt = self.data0.datetime.datetime()
        # print('[%s] %s' % (dt.strftime("%d-%m-%y %H:%M"), txt))
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


def main():
    cerebro = bt.Cerebro(quicknotify=True)
    broker_config = {
        'apiKey': BINANCE.get("key"),
        'secret': BINANCE.get("secret"),
        'nonce': lambda: str(int(time.time() * 1000)),
        'enableRateLimit': True,
    }
    store = CCXTStore(exchange='binance', currency='BTC',
                      config=broker_config, retries=5, debug=True)
    broker_mapping = {
        'order_types': {
            bt.Order.Market: 'market',
            bt.Order.Limit: 'limit',
            bt.Order.Stop: 'stop-loss',  # stop-loss for kraken, stop for bitmex
            bt.Order.StopLimit: 'stop limit'
        },
        'mappings': {
            'closed_order': {
                'key': 'status',
                'value': 'closed'
            },
            'canceled_order': {
                'key': 'result',
                'value': 1
            }
        }
    }
    broker = store.getbroker(broker_mapping=broker_mapping)
    cerebro.setbroker(broker) #ince:16392834 16392834

    hist_start_dat = dt.datetime(2021, 10, 29, 0, 0)
    #dt.datetime.utcnow() - dt.timedelta(minutes=10200)
    data = store.getdata(
        dataname='BNB/USDT',
        name="BNB/USDT",
        timeframe=bt.TimeFrame.Minutes,
        fromdate=hist_start_date,
        compression=30,
        ohlcv_limit=999
    )
    cerebro.adddata(data)
    cerebro.addstrategy(CustomStrategy)
    cerebro.addsizer(bt.sizers.PercentSizer, percents = 100)
    initial_value = cerebro.broker.getvalue()
    print('Starting Portfolio Value: %.2f' % initial_value)
    result = cerebro.run()
    cerebro.plot()

    final_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: %.2f' % final_value)


if __name__ == "__main__":
    try:
        main() #send_telegram_message ("Bot finished by user at %s" time)
    except KeyboardInterrupt:
        time = dt.datetime.now().strftime("%d-%m-%y %H:%M")
        send_telegram_message(("Bot finished by user at %s", time))
        
