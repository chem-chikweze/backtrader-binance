# #!/usr/bin/env python
# # -*- coding: utf-8; py-indent-offset:4 -*-
# ###############################################################################
# # Copyright (C) 2019 Daniel Rodriguez - MIT License
# #  - https://opensource.org/licenses/MIT
# #  - https://en.wikipedia.org/wiki/MIT_License
# ###############################################################################
# import argparse
# import logging
# import sys
# from utils import send_telegram_message, to_local_time
# import backtrader as bt
# from strategies.structure import MarketStructure as ts
# from backtrader_binance import BinanceStore
# from config import BINANCE
# import datetime as dt

# # This defines not only the commission info, but some other aspects
# # of a given data asset like the "getsize" information from below
# # params = dict(stocklike=True)  # No margin, no multiplier


# class CommInfoFractional(bt.CommissionInfo):
#     def getsize(self, price, cash):
#         '''Returns fractional size for cash operation @price'''
#         return self.p.leverage * (cash / price)


# class St(bt.Strategy):
#     params = dict(
#         p1=10, p2=30,  # periods for crossover
#         ma=bt.ind.SMA,  # moving average to use
#         target=0.5,  # percentage of value to use
#     )

#     def __init__(self):
#         ma1, ma2 = [self.p.ma(period=p) for p in (self.p.p1, self.p.p2)]
#         self.cross = bt.ind.CrossOver(ma1, ma2)

#     def next(self):
#         self.logdata()
#         if self.cross > 0:
#             self.loginfo('Enter Long')
#             self.order_target_percent(target=self.p.target)
#         elif self.cross < 0:
#             self.loginfo('Enter Short')
#             self.order_target_percent(target=-self.p.target)
#                 # Check if an order is pending ... if yes, we cannot send a 2nd one
#         if self.order:
#             print("order pending")
#             return            

#         # Check if we are in the market
#         if not self.position:
#             if self.buy_order: # some order was pending
#                 self.cancel(self.buy_order)

#             # do nothing if the trend is already in motion
#             if not (self.nullzig.l.zigzag[0] >= 0) :
#                 ""
#             else:   
#                 self.log('BUY CREATE, %.2f' % self.dataclose[0])
#                 # self.order = self.sell()
#                 self.order_target_percent(target=self.p.target)
#                 send_telegram_message("BUY {}  {}".format(self.dataclose[0], to_local_time()))

#         else:
#             # do nothing if the trend is already in motion
#             if not (self.nullzig.l.zigzag[0] >= 0) :
#                 ""
#             else:
#                 self.log('SELL CREATE, %.2f' % self.dataclose[0])
#                 # keep track of the created order to avoid a 2nd order
#                 # self.sell_order = self.buy()
#                 self.order_target_percent(target=self.p.target)
#                 send_telegram_message("SELL {}  {}".format(self.dataclose[0], to_local_time()))

#     def notify_trade(self, trade):
#         if trade.justopened:
#             self.loginfo('Trade Opened  - Size {} @Price {}',
#                          trade.size, trade.price)
#         elif trade.isclosed:
#             self.loginfo('Trade Closed  - Profit {}', trade.pnlcomm)

#         else:  # trade updated
#             self.loginfo('Trade Updated - Size {} @Price {}',
#                          trade.size, trade.price)

#     def notify_order(self, order):
#         if order.alive():
#             return

#         otypetxt = 'Buy ' if order.isbuy() else 'Sell'
#         if order.status == order.Completed:
#             self.loginfo(
#                 ('{} Order Completed - '
#                  'Size: {} @Price: {} '
#                  'Value: {:.2f} Comm: {:.2f}'),
#                 otypetxt, order.executed.size, order.executed.price,
#                 order.executed.value, order.executed.comm
#             )
#         else:
#             self.loginfo('{} Order rejected', otypetxt)

#     def loginfo(self, txt, *args):
#         out = [self.datetime.date().isoformat(), txt.format(*args)]
#         logging.info(','.join(out))

#     def logerror(self, txt, *args):
#         out = [self.datetime.date().isoformat(), txt.format(*args)]
#         logging.error(','.join(out))

#     def logdebug(self, txt, *args):
#         out = [self.datetime.date().isoformat(), txt.format(*args)]
#         logging.debug(','.join(out))

#     def logdata(self):
#         txt = []
#         txt += ['{:.2f}'.format(self.data.open[0])]
#         txt += ['{:.2f}'.format(self.data.high[0])]
#         txt += ['{:.2f}'.format(self.data.low[0])]
#         txt += ['{:.2f}'.format(self.data.close[0])]
#         txt += ['{:.2f}'.format(self.data.volume[0])]
#         self.loginfo(','.join(txt))


# def run(args=None):
#     cerebro = bt.Cerebro(quicknotify=True)

#     store = BinanceStore(
#         api_key=BINANCE.get("key"),
#         api_secret=BINANCE.get("secret"),
#         coin_refer='BNB',
#         coin_target='USDT',
#         )
#     broker = store.getbroker()
#     cerebro.setbroker(broker)

#     # from_date = dt.datetime.utcnow() - dt.timedelta(minutes=5*1600)
#     from_date = dt.datetime(2021, 10, 29, 0, 0)
#     # from_date = dt.datetime(2021, 12, 12, 0, 0)
#     data = store.getdata(
#         timeframe_in_minutes=1,
#         start_date=from_date
#         )

#     cerebro.addstrategy(ts)
#     cerebro.adddata(data)
#     # cerebro.addsizer(bt.sizers.PercentSizer, percents = 91)
#     cerebro.broker.addcommissioninfo(CommInfoFractional())

#     cerebro.run()
#     # args = parse_args(args)

#     # cerebro = bt.Cerebro()

#     # data = bt.feeds.BacktraderCSVData(dataname=args.data)
#     # cerebro.adddata(data)  # create and add data feed

#     # cerebro.addstrategy(St)  # add the strategy

#     # cerebro.broker.set_cash(args.cash)  # set broker cash

#     # if args.fractional:  # use the fractional scheme if requested
#     # cerebro.broker.addcommissioninfo(CommInfoFractional())

#     # cerebro.run()  # execute

#     # if args.plot:  # Plot if requested to
#     #     cerebro.plot(**eval('dict(' + args.plot + ')'))


# def logconfig(pargs):
#     if pargs.quiet:
#         verbose_level = logging.ERROR
#     else:
#         verbose_level = logging.INFO - pargs.verbose * 10  # -> DEBUG

#     logger = logging.getLogger()
#     for h in logger.handlers:  # Remove all loggers from root
#         logger.removeHandler(h)

#     stream = sys.stdout if not pargs.stderr else sys.stderr  # choose stream

#     logging.basicConfig(
#         stream=stream,
#         format="%(message)s",  # format="%(levelname)s: %(message)s",
#         level=verbose_level,
#     )


# def parse_args(pargs=None):
#     parser = argparse.ArgumentParser(
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter,
#         description='Fractional Sizes with CommInfo',
#     )

#     pgroup = parser.add_argument_group('Data Options')
#     parser.add_argument('--data', default='../../datas/2005-2006-day-001.txt',
#                         help='Data to read in')

#     pgroup = parser.add_argument_group(title='Broker Arguments')
#     pgroup.add_argument('--cash', default=100000.0, type=float,
#                         help='Starting cash to use')

#     pgroup.add_argument('--fractional', action='store_true',
#                         help='Use fractional commission info')

#     pgroup = parser.add_argument_group(title='Plotting Arguments')
#     pgroup.add_argument('--plot', default='', nargs='?', const='{}',
#                         metavar='kwargs', help='kwargs: "k1=v1,k2=v2,..."')

#     pgroup = parser.add_argument_group('Verbosity Options')
#     pgroup.add_argument('--stderr', action='store_true',
#                         help='Log to stderr, else to stdout')
#     pgroup = pgroup.add_mutually_exclusive_group()
#     pgroup.add_argument('--quiet', '-q', action='store_true',
#                         help='Silent (errors will be reported)')
#     pgroup.add_argument('--verbose', '-v', action='store_true',
#                         help='Increase verbosity level')

#     # Parse and process some args
#     pargs = parser.parse_args(pargs)
#     logconfig(pargs)  # config logging
#     return pargs


# if __name__ == '__main__':
#     run()