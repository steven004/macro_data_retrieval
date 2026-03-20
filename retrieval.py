import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from indicators import add_technical_indicators

def update_symbol_data(ticker_symbol: str, name: str, history_dir: str = ".") -> pd.DataFrame:
    """
    Updates the historical data for a given symbol, computes indicators, and returns the full dataframe.
    """
    file_path = os.path.join(history_dir, f"{name}_history.csv")
    today = datetime.now().date()
    
    # We fetch up to tomorrow to ensure we get all data across timezones
    end_date_str = (today + timedelta(days=1)).strftime('%Y-%m-%d') 
    
    ticker = yf.Ticker(ticker_symbol)
    
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path, index_col=0, parse_dates=True)
        if not df_existing.empty:
            df_existing.index = pd.to_datetime(df_existing.index).tz_localize(None)
            last_date = df_existing.index.max().date()
            
            # Fetch from last_date MINUS 5 days to overwrite any previously saved partial days
            start_date_fetch = last_date - timedelta(days=5)
            start_date_str = start_date_fetch.strftime('%Y-%m-%d')
            print(f"[{name}] Fetching data from {start_date_str} to update recent partials...")
            
            try:
                new_data = ticker.history(start=start_date_str, end=end_date_str)
                if not new_data.empty:
                    new_data.index = pd.to_datetime(new_data.index).tz_localize(None)
                    
                    df_combined = pd.concat([df_existing, new_data])
                    # Drop duplicate dates, keep the 'last' (newest fetched) which has complete data
                    df_combined = df_combined[~df_combined.index.duplicated(keep='last')]
                    df_combined.sort_index(inplace=True)
                    
                    # Compute technical indicators natively before saving
                    df_combined = add_technical_indicators(df_combined)
                    
                    df_combined.to_csv(file_path)
                    return df_combined
            except Exception as e:
                print(f"[{name}] Failed to fetch recent data: {e}. Using existing.")
                return df_existing
            
            return df_existing

    # If file doesn't exist
    start_date_1y = (today - timedelta(days=365)).strftime('%Y-%m-%d')
    print(f"[{name}] Creating new file: Fetching 1-year history from {start_date_1y}...")
    
    df_new = ticker.history(start=start_date_1y, end=end_date_str)
    if not df_new.empty:
        df_new.index = pd.to_datetime(df_new.index).tz_localize(None)
        
        # Compute technical indicators natively before saving
        df_new = add_technical_indicators(df_new)
        
        df_new.to_csv(file_path)
        return df_new
    
    print(f"[{name}] Warning: No data found.")
    return pd.DataFrame()
