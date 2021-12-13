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
        coin_refer='BNB',
        coin_target='USDT',
        )
    broker = store.getbroker()
    cerebro.setbroker(broker)

    # from_date = dt.datetime.utcnow() - dt.timedelta(minutes=5*1600)
    from_date = dt.datetime(2021, 10, 29, 0, 0)
    # from_date = dt.datetime(2021, 12, 12, 0, 0)
    data = store.getdata(
        timeframe_in_minutes=1,
        start_date=from_date
        )

    cerebro.addstrategy(ts)
    cerebro.adddata(data)
    cerebro.addsizer(bt.sizers.PercentSizer, percents = 91)
    cerebro.run()