import pandas as pd
import pickle
from pathlib import Path
from sklearn.linear_model import LogisticRegression

# Build a basic classification model
def train_model(training_source, training_symbol):
    # Normalize case
    training_source = training_source.lower()
    training_symbol = training_symbol.upper()

    # Load data
    input_csv = f'src/data/training_data.{training_source}.{training_symbol}.csv'
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        print(f'\nNo training data from {training_source} found for {training_symbol}')
        print('\nTo fetch training data, run "./scripts/fetch_data"')
        return

    print(f'\nLoaded training data from {training_source} for {training_symbol}')

    # Ensure we have the needed columns
    required_cols = {'timestamp', 'open', 'high', 'low', 'close', 'volume'}
    if not required_cols.issubset(df.columns):
        raise ValueError(f'\nTraining data CSV is missing some required columns: {required_cols}')

    # Convert timestamp to datetime if needed
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)

    # Basic feature engineering
    df['daily_return'] = df['close'].pct_change(fill_method=None)
    df['ma_5'] = df['close'].rolling(window=5).mean()

    # Drop the initial NAs
    df.dropna(inplace=True)

    # Create a binary label: if next day’s close is higher => label=1, else 0
    # We'll shift daily_return by -1 so today's row has tomorrow's label
    df['label'] = (df['daily_return'].shift(-1) > 0).astype(int)
    df.dropna(inplace=True)

    # Define features/labels
    X = df[['daily_return', 'ma_5']].values
    y = df['label'].values

    # Train a simple logistic regression
    model = LogisticRegression()
    model.fit(X, y)

    print(f'\nModel trained on {len(df)} samples with accuracy: {model.score(X, y):.2f}')

    # Save model
    output_model = f'src/data/trained_model.{training_source}.{training_symbol}.pkl'
    output_path = Path(output_model)
    with output_path.open('wb') as f:
        pickle.dump(model, f)

    print(f'\nTrained model saved to: {output_model}')

if __name__ == '__main__':
    training_source = input('Training data source? (default: alpaca) ') or 'alpaca'
    training_symbol = input('Training data ticker symbol? (default: NVDA) ') or 'NVDA'

    train_model(training_source, training_symbol)
