import yfinance as yf
import pandas as pd

# Yahoo Finance is more limited than Alpaca but doesn't require any API key

def fetch_data(symbol, start, end):
    # Normalize symbol to uppercase
    symbol = symbol.upper()

    print(f'\nFetching data for {symbol} from {start} to {end}...')

    # Fetch historical data
    df = yf.download(symbol, start=start, end=end)

    # Structure the data
    df.reset_index(inplace=True)
    df.columns = ['timestamp', 'close', 'high', 'low', 'open', 'volume']
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize('UTC')
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

    print(f'\nFetched and processed {len(df)} rows of data.')

    # Save to CSV
    output_csv = f'src/data/training_data.yfinance.{symbol}.csv'
    df.to_csv(output_csv, index=False)

    print(f'\nData saved to: {output_csv}')


if __name__ == '__main__':
    symbol = input('Ticker symbol to fetch? (default: NVDA) ') or 'NVDA'
    start = input('Start date (YYYY-MM-DD)? (default: 2020-01-01) ') or '2020-01-01'
    end = input('End date (YYYY-MM-DD)? (default: 2024-12-31) ') or '2024-12-31'

    fetch_data(symbol, start, end)
