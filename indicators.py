import pandas as pd
import numpy as np

def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Appends trend, momentum, volatility, rolling return, and drawdown indicators 
    to a pandas DataFrame containing High, Low, Close price data.
    """
    # Create a copy to prevent mutating slices
    df = df.copy()
    
    if not all(col in df.columns for col in ['High', 'Low', 'Close']):
        return df
        
    # --- Trend Indicators ---
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    df['MA_200'] = df['Close'].rolling(window=200).mean()
    
    # --- Momentum (RSI) ---
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()
    rs = avg_gain / avg_loss
    df['RSI_14'] = 100 - (100 / (1 + rs))
    # Handle perfect gains
    df.loc[avg_loss == 0, 'RSI_14'] = 100
    
    # --- Volatility (ATR) ---
    high_low = df['High'] - df['Low']
    high_pc = (df['High'] - df['Close'].shift(1)).abs()
    low_pc = (df['Low'] - df['Close'].shift(1)).abs()
    tr = pd.concat([high_low, high_pc, low_pc], axis=1).max(axis=1)
    df['ATR_14'] = tr.ewm(alpha=1/14, adjust=False).mean()
    
    # --- Rolling Returns ---
    # Approximating trading days: 1M=21, 3M=63, 6M=126
    df['Return_1M'] = df['Close'].pct_change(periods=21)
    df['Return_3M'] = df['Close'].pct_change(periods=63)
    df['Return_6M'] = df['Close'].pct_change(periods=126)
    
    # YTD Return
    df['Year'] = df.index.year
    first_close_of_year = df.groupby('Year')['Close'].transform('first')
    df['Return_YTD'] = (df['Close'] / first_close_of_year) - 1
    df.drop(columns=['Year'], inplace=True)
    
    # --- Drawdown (From 52-Week High) ---
    # 52 weeks is visually ~252 trading days
    rolling_max_1y = df['High'].rolling(window=252, min_periods=1).max()
    df['Drawdown_52W'] = (df['Close'] / rolling_max_1y) - 1
    
    return df
