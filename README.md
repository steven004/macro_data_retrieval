# Core Financial Data Retriever

A streamlined, highly flexible Python utility for intelligently fetching, extending, and snapshotting historical financial data for any arbitrary list of securities, commodities, or macro indices.

## Features
- **Flexible Ticker Configuration:** Completely decoupled from hard-coded symbols securely. Track 14 global macro metrics, or instantly switch to a custom tracking list of 50 tech stocks via simple external JSON config files.
- **Advanced Technical Indicators:** Organically calculates Trend (SMA 20/50/200), Momentum (RSI 14), Volatility (ATR 14), Rolling Returns (1M, 3M, 6M, YTD), Drawdowns cleanly formatting outputs intrinsically securely entirely offline locally.
- **Robust Append Logic:** Overwrites previous partial daily data securely implementing lookback caching effortlessly correcting timezone overlaps natively implicitly strictly.
- **Cross-Asset Math Matrix:** Extracts normalized 30-day trailing correlations between all provided tracking securities autonomously parsing instantly mapping outputs perfectly.

## Installation & Deployment

This repository comes pre-packaged with an automatic environment handler securely tracking setups gracefully completely safely.

```bash
git clone https://github.com/steven004/macro_data_retrieval.git
cd macro_data_retrieval
chmod +x run.sh
./run.sh
```

## Usage & Configuration

By default, the script executes using the included macro configuration file (`config/macro_tickers.json`). 

If you wish to track entirely different assets (for tactical trading, etc.), simply create a new JSON file mapping the Yahoo Finance ticker explicitly to your chosen output filename safely:
```json
{
  "AAPL": "Apple",
  "TSLA": "Tesla"
}
```

Then, execute the script pointing directly to your new tracking file dynamically bypassing defaults efficiently precisely natively:
```bash
./run.sh --tickers-file "config/my_tactical_tickers.json" --history-dir "data/tactical/history" --pv-dir "data/tactical/snapshots"
```
