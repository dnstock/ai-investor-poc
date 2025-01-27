# AI Investor POC
Automated AI-Driven Investments -- Proof of Concept

## Description
This is intended as a complete proof-of-concept (POC) project showcasing an AI-driven day-trading strategy using Backtrader, scikit-learn, and a custom data feed using the Alpaca API. This POC can run continuously, simulate trades, and show performance metrics.

## Project Structure

```plaintext
ai-investor-poc/
├── .env.example                        # Environment variables
├── pyproject.toml
├── scripts/                            # Shell scripts to facilitate operations
│   ├── run
│   ├── get_data
│   └── train_model
└── src/
    ├── data/                           # Storage for historical data and ML models
    ├── ml/
    │   ├── fetch_data_alpaca.py        # Script to get historical data from Alpaca
    │   ├── fetch_data_yfinance.py      # Script to get historical data from Yahoo Finance
    │   └── train_model.py              # Script to train the ML model
    ├── trading/
    │   ├── live_data_feed.py           # Custom Backtrader data feed for Alpaca
    │   └── ml_strategy.py              # ML-based Backtrader strategy
    └── main.py                         # Main script to run the trading algorithm

```

## 1. Project Setup

### Prerequisites
```bash
# Clone the repository
git clone git@github.com:dnstock/ai-investor-poc.git

# Navigate to the project directory
cd ai-investor-poc

# Install dependencies
poetry install
```

### Configure Environment Variables
Create a `.env` file in the root directory
```bash
cp .env.example .env
```

Add your API keys to the `.env` file
```plaintext
ALPACA_API_KEY=your_alpaca_api_key
ALPACA_SECRET_KEY=your_alpaca_secret_key
```

## 2. Data Preparation

### Load Training Data

We must generate some historical data to train the ML model.

Run one of these commands in your terminal to download datasets from either Alpaca or Yahoo Finance:
```bash
./scripts/get_data           # fetches data from Alpaca (default)
# or
./scripts/get_data yfinance  # fetches data from Yahoo Finance
```
You will be prompted to provide a stock ticker symbol and a date range, and for Alpaca, a timeframe interval.


This will fetch, process and store historical data for a single ticker (e.g., NVDA) over a specified time period.

The script will automatically create a CSV file and save it in `src/data/` with the following format:
```
training_data.{data_source}.{ticker}.csv
```

### Train the Model

We must now train the ML model using the historical data.

Run the following command in your terminal:
```bash
./scripts/train_model
```
You will be prompted to provide a data source and a stock ticker symbol.

This will train an ML model using Logistic Regression with minimal features. It will be used as our trading strategy, and may be run once or periodically. We can expand this in future iterations with technical indicators (RSI, MACD) and fundamental data.


The script will automatically create a PKL file and save it in `src/data/` with the following format:
```
trained_model.{data_source}.{ticker}.pkl
```

## 3. Runtime Data Feeds

### Custom Live Data
```
live_data_feed.py
```
This code polls the Alpaca API to simulate real-time data. For a POC, we fetch the latest data on a user-defined interval, parse it, and feed new bars into Backtrader. This is a simplified version of a real data feed.

### Polling Frequency

If `_load()` returns False often (no new bar), the “live” loop essentially waits. You can adjust sleep durations during startup or extend it to fetch multiple bars at once. For a real production setup, we'd want to use websockets or a streaming API, but for a POC, polling is fine.

## 4. Strategy

### Using the ML Model

```
ml_strategy.py
```

This code loads the saved Logistic Regression model, generates the strategy features, and places the trades. We could expand this in future iterations by enhancing the feature engineering (RSI, MACD, sentiment, etc.).

In a more robust system, we could also incorporate position sizing, risk constraints, trailing stops, etc.

## 5. Usage

### Start the POC

Run the following command in your terminal:
```bash
./scripts/run
```

You will be prompted to provide a data source, a stock ticker symbol and a polling interval.

### Results Console
Watch the console for new bars, trades, PnL changes, and final performance metrics when you eventually stop the program.

#### NOTE:
>The script effectively runs in a loop, calling `_load()` for new data. If no new bar is available, it returns False and Backtrader tries again. Eventually, you can CTRL+C to stop, and you’ll see final metrics.

## 6. Future Improvements

### Expanding the POC to an MVP

Multiple Tickers
- Create multiple `Alpaca` instances for each symbol (and add them via `cerebro`).
- Strategies can handle multiple data feeds.
- App can run multiple strategies in parallel.

More Sophisticated ML
- Add features (RSI, Bollinger Bands, sentiment, fundamentals).
- Use advanced models (random forests, gradient boosting, deep learning).
- Implement robust train/test splits to avoid overfitting.

Persisting Performance
- Log trades, daily PnL to CSV, or integrate with a small database.
- Visualize with a simple Streamlit or Dash app.

Broker Integration
- Eventually, integrate a broker API and place real orders.

### For Investors

For now, this is purely simulation in Backtrader. Its purpose is to present to investors as a baseline POC, showcasing how such a system can ingest live market data, apply ML signals, place simulated trades, and log performance.

Further iterations and polish to follow investments -- Let's make some f*cking money!
