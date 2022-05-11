import datetime as dt

import backtrader as bt
from config import BINANCE
from backtrader_binance import BinanceStore
from strategies.structure import MarketStructure as ts

if __name__ == '__main__':
    cerebro = bt.Cerebro(quicknotify=True)

    store = BinanceStore(
        api_key=BINANCE.get("key"),
        api_secret=BINANCE.get("secret"),
        coin_refer='BTC',
        coin_target='USDT',
        )
    # broker = store.getbroker()
    # cerebro.setbroker(broker)
    cerebro.broker.setcash(1000.0)

    # from_date = dt.datetime.utcnow() - dt.timedelta(minutes=5*1600)
    from_date = dt.datetime(2022, 3, 29, 0, 0)
    # to_date = dt.datetime(2021, 12, 24, 0, 0)
    data = store.getdata(
        timeframe_in_minutes=5,
        start_date=from_date,
        # todate=to_date,
        # end_date = to_date,
        )

    cerebro.addstrategy(ts)
    cerebro.adddata(data)
    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=20)
    cerebro.addsizer(bt.sizers.PercentSizer, percents = 91)
    initial_value = cerebro.broker.getvalue()
    # initial_value = store.get_asset_balance("BTC")
    print('Starting Portfolio Value: %.2f' % initial_value)
    cerebro.run()
    cerebro.plot()