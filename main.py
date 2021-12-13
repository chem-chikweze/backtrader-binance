#!/usr/bin/env python3

import backtrader as bt
import backtrader.analyzers as btan
from ccxtbt import CCXTStore
import yfinance as yf
from indicators.analyzers import BasicTradeStats
import time
import datetime as dt
from backtrader_binance import BinanceStore
from config import BINANCE, ENV, PRODUCTION, COIN_TARGET, COIN_REFER, DEBUG
# from btplotting import BacktraderPlottingLive

# from dataset.dataset import CustomDataset
from sizer.percent import FullMoney
from strategies.structure import MarketStructure as ts
from utils import send_telegram_message, to_local_time


def main():
    cerebro = bt.Cerebro(quicknotify=True)

    if ENV == PRODUCTION:  # Live trading with Binance
        # broker_config = {
        #     'apiKey': BINANCE.get("key"),
        #     'secret': BINANCE.get("secret"),
        #     'nonce': lambda: str(int(time.time() * 1000)),
        #     'enableRateLimit': True,
        # }

        # store = CCXTStore(exchange='binance', currency=COIN_REFER, config=broker_config, retries=5, debug=DEBUG)

        # broker_mapping = {
        #     'order_types': {
        #         bt.Order.Market: 'market',
        #         bt.Order.Limit: 'limit',
        #         bt.Order.Stop: 'stop-loss',
        #         bt.Order.StopLimit: 'stop limit'
        #     },
        #     'mappings': {
        #         'closed_order': {
        #             'key': 'status',
        #             'value': 'closed'
        #         },
        #         'canceled_order': {
        #             'key': 'status',
        #             'value': 'canceled'
        #         }
        #     }
        # }

        # broker = store.getbroker(broker_mapping=broker_mapping)
        # cerebro.setbroker(broker)
        # cerebro.addsizer(bt.sizers.PercentSizer, percents = 90)

        # hist_start_date = dt.datetime.utcnow() - dt.timedelta(minutes=1)
        # data = store.getdata(
        #     dataname='%s/%s' % (COIN_TARGET, COIN_REFER),
        #     name='%s%s' % (COIN_TARGET, COIN_REFER),
        #     timeframe=bt.TimeFrame.Minutes,
        #     fromdate=hist_start_date,
        #     todate=dt.datetime.utcnow(),
        #     compression=1,
        #     ohlcv_limit=99999
        # )
        # # Add the feed
        # cerebro.adddata(data)


        # binance store
        store = BinanceStore(
        api_key=BINANCE.get("key"),
        api_secret=BINANCE.get("secret"),
        coin_refer=COIN_REFER,
        coin_target=COIN_TARGET,
        testnet=True
        )
        broker = store.getbroker()
        cerebro.setbroker(broker)

        from_date = dt.datetime.utcnow() - dt.timedelta(minutes=(60*89)+5 )
        data = store.getdata(
            timeframe_in_minutes=1,
            start_date=from_date)

        cerebro.adddata(data)

    else:  # Backtesting with CSV file
        data = bt.feeds.PandasData(dataname=yf.download('BNB-USD', '2020-12-01', '2021-11-27', interval="1h"))
        # cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=30)
        cerebro.adddata(data)
        cerebro.broker.setcommission(commission=0.001, name=COIN_TARGET)  # Simulating exchange fee
        cerebro.broker.setcash(100000.0)
        cerebro.addsizer(bt.sizers.PercentSizer, percents = 90)
        
    # Analyzers to evaluate trades and strategies
    # cerebro.addanalyzer(btan.DrawDown, _name='drawdown')
    cerebro.addanalyzer(BasicTradeStats, _name="BasicTradeStats", )
    # for live plotting
    # cerebro.addanalyzer(BacktraderPlottingLive)

    # Include Strategy
    cerebro.addstrategy(ts)

    # Starting backtrader bot
    initial_value = cerebro.broker.getvalue()
    print('Starting Portfolio Value: %.2f' % initial_value)
    result = cerebro.run()

    # Print analyzers - results
    final_value = cerebro.broker.getvalue()
    print('Final Portfolio Value: %.2f' % final_value)
    print('Profit %.3f%%' % ((final_value - initial_value) / initial_value * 100))
    
    thestrat = result[0]
    for each in thestrat.analyzers:
        each.print()

    if DEBUG:
        cerebro.plot()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("finished.")
        # time = dt.datetime.now().strftime("%d-%m-%y %H:%M")
        send_telegram_message("Bot finished by user at %s" % to_local_time())
    except Exception as err:
        send_telegram_message("Bot finished with error: %s" % err)
        print("Finished with error: ", err)
        raise
