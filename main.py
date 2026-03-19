import os
import argparse
import pandas as pd
from retrieval import update_symbol_data, INDICES

def main():
    parser = argparse.ArgumentParser(description="Macro Financial Data Retriever")
    parser.add_argument("--dir", type=str, default="data", help="Directory to store the data files")
    args = parser.parse_args()
    
    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
        
    latest_values = {}
    last_dates = {}
    
    print("Starting data retrieval for Macro indices...")
    print(f"Data will be stored in: {os.path.abspath(args.dir)}\n")
    
    for ticker, name in INDICES.items():
        try:
            df = update_symbol_data(ticker, name, data_dir=args.dir)
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
        pv_file = os.path.join(args.dir, "present_values.csv")
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
