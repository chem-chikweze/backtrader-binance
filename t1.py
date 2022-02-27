from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects 
import os.path  # To manage paths
import datetime as dt
from backtrader.dataseries import TimeFrame  # To find out the script name (in argv[0])
import yfinance as yf
from strategies.structure import MarketStructure as ts
import backtrader as bt
import backtrader.analyzers as btan
import backtrader.strategies as btstrats
import pprint
# from extensions.analyzers import BasicTradeStats
from backtrader_binance import BinanceStore
from config import BINANCE

def main():


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


    # # Create a cerebro entity
    # cerebro = bt.Cerebro()


    #     # Datas are in a subfolder of the samples. Need to find where the script is
    #     # because it could have been called from anywhere
    #     # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
    #     # datapath = os.path.join(modpath, '../../datas/data_file.csv')

    # data = bt.feeds.PandasData(dataname=yf.download('BNB-USD', '2021-10-29', dt.datetime.utcnow(), interval="1h"))
    # # Add the Data Feed to Cerebro
    # cerebro.adddata(data)


    # cerebro.broker.setcash(1000.0)
    # cerebro.addsizer(bt.sizers.PercentSizer, percents = 90)
    # cerebro.broker.setcommission(commission=0.002)
    

    #  # Analyzers
    # cerebro.addanalyzer(btan.SharpeRatio, _name='mysharpe')
    # # cerebro.addanalyzer(btan.TimeReturn, _name='annual', timeframe=bt.TimeFrame.Years )
    # cerebro.addanalyzer(btan.DrawDown, _name='drawdown')

    # cerebro.addanalyzer(BasicTradeStats, _name="BasicTradeStats", )
    # # cerebro.addanalyzer(BasicTradeStats, _name="BasicTradeStats", )
    # cerebro.addanalyzer(btan.SQN)


    # # Add a strategy
    # # strats = cerebro.optstrategy(
    # #     ts.TestStrategy,
    # #     maperiod=range(10, 31))
    # cerebro.addstrategy(ts)


    # # Starting backtrader bot
    # initial_value = cerebro.broker.getvalue()
    # print('Starting Portfolio Value: %.2f' % initial_value)
    # result = cerebro.run()



    # # Run over everything
    # thestrat = result[0]
    # for each in thestrat.analyzers:
    #     each.print()


    # print('Sharpe Ratio: ', thestrat.analyzers.mysharpe.get_analysis() )
    # # print('Annual Ratio: ', thestrat.analyzers.annual.get_analysis() )
    # # print('Drawdown Ratio: ', thestrat.analyzers.drawdown.get_analysis() )
    # cerebro.plot()


if __name__== "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("finished.")
        # time = dt.datetime.now().strftime("%d-%m-%y %H:%M")
        # send_telegram_message("Bot finished by user at %s" % time)
    except Exception as err:
        # send_telegram_message("Bot finished with error: %s" % err)
        print("Finished with error: ", err)
        raise
