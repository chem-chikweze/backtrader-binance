import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds
import pandas as pd
import backtrader.filters as btfilters
from csv import writer
# from nullfilter import NullBarFilter
from utils import send_telegram_message, to_local_time

class ZigZag(bt.ind.PeriodN):
    '''
      ZigZag indicator.

    '''
    lines = (
        'trend',
        'last_high',
        'last_low',
        'zigzag', # contains 'nan' values for data points that are not pivots
        'value',
    )

    plotinfo = dict(
        subplot=False,
        plotlinelabels=True, plotlinevalues=True, plotvaluetags=True,
    )

    plotlines = dict(
        trend=dict(_plotskip=True),
        last_high=dict(color='green', ls='-', _plotskip=True),
        last_low=dict(color='black', ls='-', _plotskip=True),
        zigzag=dict(_name='zigzag', color='yellow', ls='-', _skipnan=True),
    )

    params = (
        ('period', 2),
        ('retrace',  2.238  ), #8.2387), 
        # in percent default  is 0.05 : 
        # 2.5 for bitcoin, 20 for AMC
        # 3 for SAN 100% 
        # 2.2 for BNBUSD trades more but 2.4,2.5 trades less but will they make e^x more long term?
        # LAGGGINGGGGGG this shit is lagging
        # but we can do this: when we identify a high, place an order at 0.92109500805 of the high.
        # or wait, could we keep on modifying our order. If we are in an uptrend that has exceeded 
        # some amount and we have set our profit, should we keep modifying our order to make up for this 
        # lagging mess.
        # keep modifying 
        # given this uptrend in amount, what was the learned retracement?
        # put our buy at retracement. If it works, kudos to the knowledge.
        # we have seen .92 retracement from highs at BNBUSD, we might trade with it. And then 
        # watch out for zigzag confirmation.
        # LAGGGgGgGGggggGGGGggg lagoster.
        ('minbars', 2), # number of bars to skip after the trend change
    )

    def __init__(self):
        super(ZigZag, self).__init__()
        assert self.p.retrace > 0, 'Retracement should be above zero.'
        assert self.p.minbars >= 0, 'Minimal bars should be >= zero.'

        self.ret = self.data.close * self.p.retrace / 100
        self.minbars = self.p.minbars
        self.count_bars = 0
        self.last_pivot_t = 0
        self.last_pivot_ago = 0
        # self.strategy = strategy
        # self.data = self.data.addfilter(NullBarFilter)

    def prenext(self):
        self.l.trend[0] = 0
        self.l.last_high[0] = self.data.high[0]
        self.l.last_low[0] = self.data.low[0]
        self.l.zigzag[0] = (self.data.high[0] + self.data.low[0]) / 2

    def next(self):
        curr_idx = len(self.data)
        self.ret = self.data.close[0] * self.p.retrace / 100
        self.last_pivot_ago = curr_idx - self.last_pivot_t
        self.l.trend[0] = self.l.trend[-1]
        self.l.last_high[0] = self.l.last_high[-1]
        self.l.last_low[0] = self.l.last_low[-1]
        self.l.zigzag[0] = float('NaN')

        t = False # keeps track of if we have a new data point to use to update our zigzag.csv

        # Search for trend
        if self.l.trend[-1] == 0:
            if self.l.last_low[0] < self.data.low[0] and self.l.last_high[0] < self.data.high[0]:
                self.l.trend[0] = 1
                self.l.last_high[0] = self.data.high[0]
                self.last_pivot_t = curr_idx

            elif self.l.last_low[0] > self.data.low[0] and self.l.last_high[0] > self.data.high[0]:
                self.l.trend[0] = -1
                self.l.last_low[0] = self.data.low[0]
                self.last_pivot_t = curr_idx

        # Up trend
        elif self.l.trend[-1] == 1:
            if self.data.high[0] > self.l.last_high[-1]:
                self.l.last_high[0] = self.data.high[0]
                self.count_bars = self.minbars
                self.last_pivot_t = curr_idx
            else:
                if self.count_bars <= 0 and self.l.last_high[0] - self.data.low[0] > self.ret and self.data.high[0] < self.l.last_high[0]:
                    self.l.trend[0] = -1
                    self.count_bars = self.minbars
                    self.l.last_low[0] = self.data.low[0]
                    self.l.zigzag[-self.last_pivot_ago] = self.l.last_high[0]
                    self.l.value[-self.last_pivot_ago] = 1 # resistance
                    self.last_pivot_t = curr_idx

                    list_data = [self.l.last_high[0],  1, self.data.close[0]]
                    with open('zigzags.csv', 'a', newline='') as f_object:  
                        writer_object = writer(f_object)
                        writer_object.writerow(list_data)  
                        f_object.close()

                    send_telegram_message('buy {} {} time: {}'.format(
                        self.l.last_high[0], 
                        1, 
                        self.data.close[0]
                        )
                    )


                elif self.count_bars < self.minbars and self.data.close[0] < self.l.last_low[0]:
                    self.l.trend[0] = -1
                    self.count_bars = self.minbars
                    self.l.last_low[0] = self.data.low[0]
                    self.l.zigzag[-self.last_pivot_ago] = self.l.last_high[0]
                    self.l.value[-self.last_pivot_ago] = 1 # resistance
                    self.last_pivot_t = curr_idx

                    # "if a new pivot point was made, write it to file"
                    # # list_data = pd.DataFrame( {"Pivot": self.l.last_high[0], "Value": 1}, index=[0])
                    # # df = pd.read_csv('zigzags.csv')
                    # # df  = pd.concat([list_data, df])
                    # # df.to_csv('zigzags.csv', mode='w')

                    list_data = [self.l.last_high[0],  1, self.data.close[0]]
                    with open('zigzags.csv', 'a', newline='') as f_object:  
                        writer_object = writer(f_object)
                        writer_object.writerow(list_data)  
                        f_object.close()

                    send_telegram_message('buy {} {} time: {}'.format(
                        self.l.last_high[0], 
                        1, 
                        self.data.close[0]
                        )
                    )

        # Down trend
        elif self.l.trend[-1] == -1:
            if self.data.low[0] < self.l.last_low[-1]:
                self.l.last_low[0] = self.data.low[0]
                self.count_bars = self.minbars
                self.last_pivot_t = curr_idx
            else:
                if self.count_bars <= 0 and self.data.high[0] - self.l.last_low[0] > self.ret and self.data.low[0] > self.l.last_low[0]:
                    self.l.trend[0] = 1
                    self.count_bars = self.minbars
                    self.l.last_high[0] = self.data.high[0]
                    self.l.zigzag[-self.last_pivot_ago] = self.l.last_low[0]
                    self.l.value[-self.last_pivot_ago] = -1 # new support
                    self.last_pivot_t = curr_idx

                    list_data = [self.l.last_low[0],  -1, self.data.close[0]]
                    with open('zigzags.csv', 'a', newline='') as f_object:  
                        writer_object = writer(f_object)
                        writer_object.writerow(list_data)  
                        f_object.close()
                    
                    send_telegram_message('sell {} {} time: {}'.format(
                        self.l.last_low[0], 
                        -1, 
                        self.data.close[0]
                        )
                    )


                elif self.count_bars < self.minbars and self.data.close[0] > self.l.last_high[-1]:
                    self.l.trend[0] = 1
                    self.count_bars = self.minbars
                    self.l.last_high[0] = self.data.high[0]
                    self.l.zigzag[-self.last_pivot_ago] = self.l.last_low[0]
                    self.l.value[-self.last_pivot_ago] = -1 # new support
                    self.last_pivot_t = curr_idx

                    list_data = [self.l.last_low[0],  -1, self.data.close[0]]
                    with open('zigzags.csv', 'a', newline='') as f_object:  
                        writer_object = writer(f_object)
                        writer_object.writerow(list_data)  
                        f_object.close()
                    
                    send_telegram_message('sell {} {} time: {}'.format(
                        self.l.last_low[0], 
                        -1, 
                        self.data.close[0]
                        )
                    )

                    

        # Decrease minbars counter
        self.count_bars -= 1

        def stop(self):
            myzigzag = self.l.zigzag
            myvalues = self.l.value
            myzigzag.csv = True
            myvalues.csv = True

    
class ZigzagFilter(object):
    def __init__(self, data):
        pass

    def __call__(self, data):
        if data >= -1:
            return False
        data.backwards()
        return True