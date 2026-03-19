import os
import argparse
import pandas as pd
from retrieval import update_symbol_data, INDICES

def main():
    parser = argparse.ArgumentParser(description="Macro Financial Data Retriever")
    parser.add_argument("--history-dir", type=str, default="data/history_data", help="Directory to store historical data files")
    parser.add_argument("--pv-dir", type=str, default="data/present_value", help="Directory to store the present_value file")
    args = parser.parse_args()
    
    if not os.path.exists(args.history_dir):
        os.makedirs(args.history_dir)
    if not os.path.exists(args.pv_dir):
        os.makedirs(args.pv_dir)
        
    latest_values = {}
    last_dates = {}
    
    print("Starting data retrieval for Macro indices...")
    print(f"History data will be stored in: {os.path.abspath(args.history_dir)}")
    print(f"Present value data will be stored in: {os.path.abspath(args.pv_dir)}\n")
    
    for ticker, name in INDICES.items():
        try:
            df = update_symbol_data(ticker, name, history_dir=args.history_dir)
            if not df.empty:
                # Find the latest valid 'Close' price
                if "Close" in df.columns:
                    valid_data = df["Close"].dropna()
                    if not valid_data.empty:
                        latest_close = valid_data.iloc[-1]
                        latest_date = valid_data.index[-1].date()
                    else:
                        latest_close = "N/A"
                        latest_date = "Unknown"
                else:
                    latest_close = df.iloc[-1][0]
                    latest_date = df.index[-1].date()
                    
                latest_values[name] = latest_close
                last_dates[name] = latest_date
        except Exception as e:
            print(f"[{name}] Error: {e}")
            
    # Save present values to a separate file
    if latest_values:
        pv_file = os.path.join(args.pv_dir, "present_values.csv")
        pv_data = []
        for name, value in latest_values.items():
            pv_data.append({
                "Index": name,
                "Present_Value": value,
                "Last_Updated": last_dates.get(name, "Unknown")
            })
            
        pv_df = pd.DataFrame(pv_data)
        pv_df.to_csv(pv_file, index=False)
        print(f"\nSuccessfully stored present values in {pv_file}")
    else:
        print("\nNo data retrieved.")

if __name__ == "__main__":
    main()
