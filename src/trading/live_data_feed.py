import time
import backtrader as bt
from backtrader import date2num
import alpaca_trade_api as tradeapi

# Custom Backtrader feed that polls Alpaca for 1-min bars
class LiveData(bt.feeds.DataBase):
    def __init__(self, symbol, api_key, api_secret, base_url, poll_interval):
        super().__init__()
        self.symbol = symbol
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.poll_interval = poll_interval

        self._api = tradeapi.REST(
            key_id=self.api_key,
            secret_key=self.api_secret,
            base_url=self.base_url
        )

        self.last_bar_time = None

    def _load(self):
        try:
            bars = self._api.get_bars(
                symbol=self.symbol,
                timeframe='1Min',
                limit=2
            )
        except Exception as e:
            print(f'[AlpacaLiveData] Error fetching bars: {e}')
            time.sleep(self.poll_interval)
            return False

        if not bars or len(bars) == 0:
            time.sleep(self.poll_interval)
            return False

        latest_bar = bars[-1]
        bar_dt = latest_bar.t  # datetime of the latest bar

        if (self.last_bar_time is None) or (bar_dt > self.last_bar_time):
            self.last_bar_time = bar_dt
            self.lines.datetime[0] = date2num(bar_dt)
            self.lines.open[0] = float(latest_bar.o)
            self.lines.high[0] = float(latest_bar.h)
            self.lines.low[0] = float(latest_bar.l)
            self.lines.close[0] = float(latest_bar.c)
            self.lines.volume[0] = float(latest_bar.v)
            self.lines.openinterest[0] = 0.0

            return True
        else:
            time.sleep(self.poll_interval)
            return False
