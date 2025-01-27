import os
import backtrader as bt
from trading.live_data_feed import LiveData
from trading.ml_strategy import MLStrategy
from dotenv import load_dotenv

load_dotenv()

def main(ml_source, ml_symbol, polling_interval):
    ALPACA_API_KEY = os.getenv('ALPACA_API_KEY_ID')
    ALPACA_API_SECRET = os.getenv('ALPACA_API_SECRET_KEY')
    ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')

    if not ALPACA_API_KEY or not ALPACA_API_SECRET:
        raise ValueError('\nPlease set ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY env variables.')

    # Normalize case
    ml_source = ml_source.lower()
    ml_symbol = ml_symbol.upper()

    # Check if the model exists
    ml_model = f'src/data/trained_model.{ml_source}.{ml_symbol}.pkl'
    if not os.path.exists(ml_model):
        print(f'\nNo trained model from {ml_source} found for {ml_symbol}')
        print('\nTo train a model, run "./scripts/train_model"')
        return

    cerebro = bt.Cerebro()

    # Starting capital
    cerebro.broker.setcash(100000.0)

    data_feed = LiveData(
        symbol=ml_symbol,
        api_key=ALPACA_API_KEY,
        api_secret=ALPACA_API_SECRET,
        base_url=ALPACA_BASE_URL,
        poll_interval=polling_interval  # in seconds
    )
    cerebro.adddata(data_feed)

    cerebro.addstrategy(MLStrategy, model_path=ml_model)

    # Analyzers
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')

    print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')
    results = cerebro.run()
    print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')

    # Extract analyzer results
    strat = results[0]
    sharpe_analyzer = strat.analyzers.sharpe.get_analysis()
    trades_analyzer = strat.analyzers.trades.get_analysis()

    print('Sharpe Ratio:', sharpe_analyzer.get('sharperatio'))
    print('Trade Summary:', trades_analyzer)

if __name__ == '__main__':
    ml_source = input('Data model source? (default: alpaca) ') or 'alpaca'
    ml_symbol = input('Data model ticker symbol? (default: NVDA) ') or 'NVDA'
    polling_interval = int(input('Polling interval in seconds? (default: 15) ') or 15)

    main(ml_source, ml_symbol, polling_interval)
