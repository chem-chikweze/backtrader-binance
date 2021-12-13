import requests
from datetime import datetime
from dateutil import tz
from config import TELEGRAM, ENV, NYC
from pytz import timezone


def print_trade_analysis(analyzer):
    # Get the results we are interested in
    if not analyzer.get("total"):
        return

    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total, 2)
    strike_rate = round((total_won / total_closed) * 2)

    # Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed, total_won, total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]

    # Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)

    # Print the rows
    print_list = [h1, r1, h2, r2]
    row_format = "{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('', *row))


def print_sqn(analyzer):
    sqn = round(analyzer.sqn, 2)
    print('SQN: {}'.format(sqn))


def send_telegram_message(message=""):
    if ENV != "production":
        return

    base_url = "https://api.telegram.org/bot%s" % TELEGRAM.get("bot")
    return requests.get("%s/sendMessage" % base_url, params={
        'chat_id': TELEGRAM.get("channel"),
        'text': message
    })

def to_local_time(utc=datetime.utcnow()):
    # # METHOD 1: Hardcode zones:
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')
    newyork_tz = timezone('America/New_York')

    newyork = newyork_tz.localize(utc)
    # METHOD 2: Auto-detect zones:
    # from_zone = tz.tzutc()
    # to_zone = tz.tzlocal()

    # utc = datetime.utcnow()
    # utc = datetime.strptime('2011-01-21 02:37:21', '%Y-%m-%d %H:%M:%S')

    # Tell the datetime object that it's in UTC time zone since 
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=NYC).strftime('%B %d %Y - %I:%M:%p')

    # Convert time zone
    # utc = utc.astimezone(to_zone).strftime('%B %d %Y - %I:%M:%p')
    return newyork