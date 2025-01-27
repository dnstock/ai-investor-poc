import os
import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

def fetch_data(symbol, days, timeframe):
    ALPACA_API_KEY = os.getenv('ALPACA_API_KEY_ID')
    ALPACA_API_SECRET = os.getenv('ALPACA_API_SECRET_KEY')
    ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')

    if not ALPACA_API_KEY or not ALPACA_API_SECRET:
        raise ValueError('\nPlease set ALPACA_API_KEY_ID and ALPACA_API_SECRET_KEY env variables.')

    # Initialize Alpaca client
    api = tradeapi.REST(
        key_id=ALPACA_API_KEY,
        secret_key=ALPACA_API_SECRET,
        base_url=ALPACA_BASE_URL
    )

    # Set start and end dates in ISO 8601 format
    end_dt = datetime.now(timezone.utc)  # Use UTC
    end_str = end_dt.isoformat(timespec='seconds')

    start_dt = end_dt - timedelta(days=days)
    start_str = start_dt.isoformat(timespec='seconds')

    # Normalize symbol to uppercase
    symbol = symbol.upper()

    print(f'\nFetching data for {symbol} in {timeframe} intervals from {start_str} to {end_str}...')

    # Fetch the data
    try:
        bars = api.get_bars(
            symbol=symbol,
            timeframe=timeframe,
            start=start_str,    # | can also accept 'limit'
            end=end_str,        # | instead of start/end
            feed='iex',         # avoid SIP data, which is not free
        )
    except Exception as e:
        print(f'\nError fetching bars: {e}')
        return

    if not bars or len(bars) == 0:
        print('\nNo data returned from Alpaca.')
        return

    # Convert bars into a Pandas DataFrame
    data = []
    for bar in bars:
        data.append({
            'timestamp': bar.t,  # Python datetime
            'open': float(bar.o),
            'high': float(bar.h),
            'low': float(bar.l),
            'close': float(bar.c),
            'volume': float(bar.v)
        })
    df = pd.DataFrame(data)

    # Sort by timestamp ascending
    df.sort_values('timestamp', inplace=True)
    df.reset_index(drop=True, inplace=True)

    print(f'\nFetched and processed {len(df)} bars of data.')

    # Save DataFrame to CSV
    output_csv = f'src/data/training_data.alpaca.{symbol}.csv'
    df.to_csv(output_csv, index=False)
    print(f'\nData saved to: {output_csv}')

if __name__ == '__main__':
    symbol = input('Ticker symbol to fetch? (default: NVDA) ') or 'NVDA'
    days = int(input('How many days back from today to fetch? (default: 90) ') or 90)
    timeframe = input('Timeframe (e.g. 1Day, 1Min, 5Min)? (default: 1Hour) ') or '1Hour'

    fetch_data(symbol, days, timeframe)
