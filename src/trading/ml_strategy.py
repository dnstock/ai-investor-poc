import pickle
import numpy as np
import backtrader as bt
import backtrader.indicators as btind
from pathlib import Path

class MLStrategy(bt.Strategy):
    def __init__(self, model_path):
        # Load pre-trained model
        input_model = Path(model_path)
        with input_model.open("rb") as f:
            self.model = pickle.load(f)

        self.dataclose = self.datas[0].close
        # Indicators
        self.daily_return = btind.PercentChange(self.dataclose, period=1)  # 1-day return
        self.ma_5 = btind.SMA(self.dataclose, period=5)  # 5-period moving average

    def next(self):
        # Feature vectors
        feat_dr = self.daily_return[0]
        feat_ma = self.ma_5[0]

        # Skip if not enough data for indicators
        if np.isnan(feat_dr) or np.isnan(feat_ma):
            return

        X_live = np.array([[feat_dr, feat_ma]])
        pred = self.model.predict(X_live)[0]  # 1 => buy, 0 => do not hold

        if not self.position and pred == 1:
            self.buy()
        elif self.position and pred == 0:
            self.close()
