import os
import argparse
import json
import pandas as pd
from retrieval import update_symbol_data

def main():
    parser = argparse.ArgumentParser(description="Macro Financial Data Retriever")
    parser.add_argument("--tickers-file", type=str, required=True, help="Path to JSON file containing the tickers mapping dictionary")
    parser.add_argument("--history-dir", type=str, default="data/history_data", help="Directory to store historical data files")
    parser.add_argument("--pv-dir", type=str, default="data/present_value", help="Directory to store the present_value file")
    args = parser.parse_args()
    
    if not os.path.exists(args.tickers_file):
        print(f"Error: Tickers configuration file '{args.tickers_file}' not found.")
        return
        
    try:
        with open(args.tickers_file, 'r') as f:
            tickers_dict = json.load(f)
    except Exception as e:
        print(f"Error securely reading tickers config file: {e}")
        return
    
    if not os.path.exists(args.history_dir):
        os.makedirs(args.history_dir)
    if not os.path.exists(args.pv_dir):
        os.makedirs(args.pv_dir)
        
    latest_values = {}
    all_closes = {}
    
    print(f"Loaded {len(tickers_dict)} instruments from '{args.tickers_file}'")
    print(f"History data will be stored securely in: {os.path.abspath(args.history_dir)}")
    print(f"Present values will identically be locally saved to: {os.path.abspath(args.pv_dir)}\n")
    
    for ticker, name in tickers_dict.items():
        try:
            df = update_symbol_data(ticker, name, history_dir=args.history_dir)
            if not df.empty:
                if "Close" in df.columns:
                    all_closes[name] = df["Close"]
                
                if "Close" in df.columns:
                    valid_df = df.dropna(subset=["Close"])
                    if not valid_df.empty:
                        latest_row = valid_df.iloc[-1]
                        
                        def safe_round(val, decimals=4):
                            try:
                                return round(float(val), decimals)
                            except:
                                return val
                                
                        latest_values[name] = {
                            "Close": safe_round(latest_row.get("Close"), 2),
                            "MA_20": safe_round(latest_row.get("MA_20"), 2),
                            "MA_50": safe_round(latest_row.get("MA_50"), 2),
                            "MA_200": safe_round(latest_row.get("MA_200"), 2),
                            "RSI_14": safe_round(latest_row.get("RSI_14"), 2),
                            "ATR_14": safe_round(latest_row.get("ATR_14"), 2),
                            "Return_1M": safe_round(latest_row.get("Return_1M"), 4),
                            "Return_3M": safe_round(latest_row.get("Return_3M"), 4),
                            "Return_6M": safe_round(latest_row.get("Return_6M"), 4),
                            "Return_YTD": safe_round(latest_row.get("Return_YTD"), 4),
                            "Drawdown_52W": safe_round(latest_row.get("Drawdown_52W"), 4),
                            "Last_Updated": latest_row.name.date()
                        }
        except Exception as e:
            print(f"[{name}] Component Exception Error: {e}")
            
    if latest_values:
        pv_file = os.path.join(args.pv_dir, "present_values.csv")
        pv_data = []
        for name, metrics in latest_values.items():
            row = {"Index": name}
            row.update(metrics)
            pv_data.append(row)
            
        pv_df = pd.DataFrame(pv_data)
        pv_df.to_csv(pv_file, index=False)
        print(f"\nSuccessfully stored scalable LLM-friendly present values snapshot locally to {pv_file}")
    
    if all_closes:
        df_all_close = pd.DataFrame(all_closes)
        df_all_close.dropna(how='all', inplace=True)
        
        df_returns = df_all_close.pct_change()
        latest_30d_returns = df_returns.tail(30)
        corr_matrix = latest_30d_returns.corr().round(3) 
        
        corr_file = os.path.join(args.pv_dir, "cross_asset_correlation.csv")
        corr_matrix.index.name = "Ticker"
        corr_matrix.to_csv(corr_file)
        print(f"Successfully cleanly processed cross-asset 30D correlation array intelligently to {corr_file}")
    else:
        print("\nDeployment completed, zero values were able to uniquely save correctly.")

    if latest_values:
        from datetime import datetime
        metadata = {
            "snapshot_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "last_updated": str(max([v["Last_Updated"] for v in latest_values.values()]))
        }
        
        assets_data = {}
        for name, metrics in latest_values.items():
            close = metrics.get("Close")
            ma20 = metrics.get("MA_20")
            ma50 = metrics.get("MA_50")
            ma200 = metrics.get("MA_200")
            
            def safe_dist(c, ma):
                if c is not None and ma is not None and ma > 0:
                    return round((c - ma) / ma, 4)
                return None
                
            trend = None
            if close is not None and ma200 is not None:
                trend = "Bearish" if close < ma200 else "Bullish"
            
            # Asset snapshot with absolute values
            snapshot = {
                "Close": close,
                "MA_20": ma20,
                "MA_50": ma50,
                "MA_200": ma200,
                "RSI_14": metrics.get("RSI_14"),
                "ATR_14": metrics.get("ATR_14")
            }
            
            # Technical performance with relative/calculated indicators
            technical_performance = {
                "dist_to_MA20": safe_dist(close, ma20),
                "dist_to_MA50": safe_dist(close, ma50),
                "dist_to_MA200": safe_dist(close, ma200),
                "long_term_trend": trend,
                "Return_1M": metrics.get("Return_1M"),
                "Return_3M": metrics.get("Return_3M"),
                "Return_YTD": metrics.get("Return_YTD"),
                "Drawdown_52W": metrics.get("Drawdown_52W")
            }
            
            # Asset-specific correlations
            asset_correlations = {}
            if all_closes and 'corr_matrix' in locals() and name in corr_matrix.index:
                asset_correlations = corr_matrix.loc[name].where(pd.notnull(corr_matrix.loc[name]), None).to_dict()

            assets_data[name] = {
                "snapshot": snapshot,
                "technical_performance": technical_performance,
                "correlations": asset_correlations
            }
            
        market_context = {
            "metadata": metadata,
            "assets": assets_data
        }
        
        json_file_path = os.path.join(args.pv_dir, "market_context.json")
        with open(json_file_path, "w") as f:
            json.dump(market_context, f, indent=4)
            
        print(f"\nSuccessfully generated restructured asset-centric market context JSON to {json_file_path}")

if __name__ == "__main__":
    main()
