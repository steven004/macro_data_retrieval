# Macro Financial Data Retriever

A streamlined Python utility for intelligently fetching and appending historical data for 14 core macroeconomic indices, alongside calculating real-time present values.

## Features
- **Specific Instruments:** Fetches specifically chosen indices spanning equity, risk-free rates, energy, crypto, semiconductor, and shipping based on standard Yahoo Finance aggregations.
- **Robust Append Logic:** When running the retrieval script, it looks back 5 days to overwrite any previously recorded partial/incomplete data with the newest, fully complete trading day information. This corrects timezone inconsistencies native to financial market opening hours smoothly.
- **Weekend Safe:** Ignores non-trading days without injecting blank artifacts into the data, while gracefully allowing 24/7 assets like Bitcoin to track through weekends seamlessly.
- **Auto-Installation:** Bundled with a simple execution script `run.sh` that securely provisions its own virtual python environment and dependency tree on its first-time execution automatically.

## Installation & Deployment (Any Machine)

This repository comes pre-packaged with an automatic environment handler. Simply pull or clone the repository to your new machine, and run the wrapper script:

```bash
git clone git@github.com:steven004/macro_data_retrieval.git
cd macro_data_retrieval
chmod +x run.sh
./run.sh
```

## Usage
By default, the script will create two directories: `data/history_data` and `data/present_value`. If you wish to provide your own explicit paths for deployment on a server or secondary computer, use the following arguments:

```bash
./run.sh --history-dir "/path/to/your/history_directory" --pv-dir "/path/to/your/snapshot_directory"
```

## Outputs
- **History Data:** Appends 1-year of daily OHLC metrics to individual CSVs designated by name (`SP500_history.csv`).
- **Present Values:** Extracts the latest valid `Close` price and recorded update time identically to a centralized `present_values.csv` snapshot file. 
