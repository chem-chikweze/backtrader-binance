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
  "key": "MIiJgHM3eyTqPlbHCar6P5kZ23SsCHXKlnd8OmZpH72czt2hVVmUH0Czf1lEcwkX",
  "secret": "HC9h3GkiZ9DyiPvYFbwMPavVwVyvYbm8qpKcQlq42Wt73MAoCiRC8bpHoQtacL5K"

  # testnet
  # "key": "h51BzWIJPFEWsiwrtSEZrPbd9hg1RBLYA4Obt4648xvk6Ui9L13S75e8oPExxKcX", **/.git
  # "secret": "28612dc1YDdd4kDWljRSRZh3Zg63nI4AvfoViW2Xrdn5u777jKefzKBNSykZS8ce"

  # "key": "10ZSmwCkn5Ogx9YPzU0jpKWj7oArBu2AaEZ8CtTJTg3ns35039UH9YdbqUUcUo7g",
  # "secret": "T4P0TnS3hBzmYA25UW66hRGLBedzD0ftkqyrf7jhrcHHRG8D9sdm9MeEY3NOpZeB"
}

TELEGRAM = {
  "channel": "-1001683168351", 
  "bot": "2124069658:AAG9Q_NXP3PajsxDD58yn4tnRrK3rFWs8-U"
}

print("ENV = ", ENV)