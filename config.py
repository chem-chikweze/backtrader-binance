import os
import zoneinfo

PRODUCTION = "production"
DEVELOPMENT = "development"

COIN_TARGET = "USDT"
COIN_REFER = "BNB"

ENV = os.getenv("ENVIRONMENT", PRODUCTION)
DEBUG = True
NYC = zoneinfo.ZoneInfo("America/New_York")

BINANCE = {
  # old did not work

  # testnet
  # "key": "h51BzWIJPFEWsiwrtSEZrPbd9hg1RBLYA4Obt4648xvk6Ui9L13S75e8oPExxKcX", **/.git
  # "secret": "28612dc1YDdd4kDWljRSRZh3Zg63nI4AvfoViW2Xrdn5u777jKefzKBNSykZS8ce"
  "key": "V6yWvdItTkcXSKfhApGvTkx2HYNU9e1TeP6yJlY0jNme7zXUoPhu3yVOVz0QwhQL",
  "secret": "IFzyPqt4ctlYkQ6PDDj8KLt8H8wQdqshn9SRPNspodkVXUDw0RUSZwnAi6jU2BeH",

}

TELEGRAM = {
  "channel": "-1001683168351", 
  "bot": "2124069658:AAG9Q_NXP3PajsxDD58yn4tnRrK3rFWs8-U"
}

# TELEGRAM = {
#   "channel": "-1759912824", 
#   "bot": "5034003189:AAEVr7ycuuWhGj69B8lMZJ_uRJMWtWYUFXw"
# }



print("ENV = ", ENV)

# send_telegram_message('buy {} {} time: {}'.format(
#                         self.l.last_low[0], 
#                         -1, 
#                         to_local_time()
#                         )

# send_telegram_message('sell {} {} time: {}'.format(
#                         self.l.last_high[0], 
#                         1, 
#                         to_local_time()
#                         )
#                     )