# Stock Data Consolidation Guide

This guide explains how to work with your historical stock data and maintain a master data file for modeling.

## Overview

Your stock data workflow now consists of:

1. **Historical Data**: All your old data from `/old_stock_charts/` folder (consolidated once)
2. **Master File**: A single clean CSV with all 5-minute closing prices ([master_stock_data.csv](data/master_stock_data.csv))
3. **New Data**: Automated downloads using [stock_data_downloader.ipynb](stock_data_downloader.ipynb)
4. **Append Process**: Easy merging of new data into the master file

## Master Data File

**Location**: `data/master_stock_data.csv`

**Format**:
- **Index**: Datetime (timezone-aware UTC)
- **Columns**: Stock tickers (AAPL, ABBV, ACN, etc.)
- **Values**: 5-minute closing prices
- **Date Range**: June 26, 2024 to February 17, 2026 (601 days)
- **Size**: 27,276 time periods × 45 stocks = 1.2M+ data points
- **Completeness**: 96.95%

**Statistics**:
```
Time Periods (Rows): 27,276
Stock Tickers (Columns): 45
Total Data Points: 1,227,420
Valid Data Points: 1,189,953
Missing Data Points: 37,467
Data Completeness: 96.95%
```

## Files Created

### Scripts
- **[consolidate_historical_data.py](consolidate_historical_data.py)** - One-time script to merge all historical data
- **[append_to_master.py](append_to_master.py)** - Helper to append new downloads to master file

### Notebooks
- **[stock_data_downloader.ipynb](stock_data_downloader.ipynb)** - Automated downloader with append functionality

### Data Files
- **[data/master_stock_data.csv](data/master_stock_data.csv)** - Your master data file for modeling
- **[data/master_file_creation_log.txt](data/master_file_creation_log.txt)** - Creation log with statistics

## Workflow

### Initial Setup (Already Done!)

The historical data consolidation has been completed:

```bash
python3 consolidate_historical_data.py
```

This created `data/master_stock_data.csv` by:
- Reading all CSV files from `/old_stock_charts/stockcharts_data/data_yfinance/`
- Handling both old format (long) and new format (wide) CSVs
- Removing 107 duplicate timestamps
- Merging 22 files into one clean master file

### Regular Usage: Download New Data

Use the Jupyter notebook to download new data:

1. Open [stock_data_downloader.ipynb](stock_data_downloader.ipynb)
2. Run the download cells (auto-detects last download date)
3. Optionally run the append cell to add to master file

**The notebook now**:
- Downloads 5-minute interval data from Yahoo Finance
- Saves in the same format as your master file
- Can automatically append to the master file
- Creates detailed logs of all operations

### Appending New Data to Master

**Option 1: Using the Notebook**
```python
# In stock_data_downloader.ipynb, after downloading:
from append_to_master import append_new_data

result = append_new_data(
    new_data_path="./stockcharts_data/data_yfinance/newf_raw_prices_2026-02-18_2026-03-01.csv",
    master_path="./data/master_stock_data.csv",
    backup=True  # Creates automatic backup
)
```

**Option 2: Command Line**
```bash
python3 append_to_master.py ./stockcharts_data/data_yfinance/newf_raw_prices_2026-02-18_2026-03-01.csv
```

The append script:
- ✅ Creates automatic backup before modifying master file
- ✅ Handles duplicate timestamps (keeps existing data)
- ✅ Detects new stocks or removed stocks
- ✅ Maintains chronological order
- ✅ Logs all operations to `data/append_log.txt`

## Data Format Compatibility

All files use the **same format** for easy merging:

```csv
,AAPL,ABBV,ACN,AES,AMGN,...
2024-06-26 13:30:00+00:00,212.10,171.44,301.70,10.52,...
2024-06-26 13:35:00+00:00,211.33,171.15,302.77,10.54,...
```

- **Wide format**: Each stock is a column
- **Datetime index**: UTC timezone-aware timestamps
- **5-minute intervals**: Market hours only
- **Close prices**: Single price per timestamp per stock

## Handling Missing Data

The master file includes gaps where:
- Stocks weren't being tracked yet (e.g., BAYRY has 42.3% coverage)
- Market was closed
- Data wasn't available from Yahoo Finance

**For modeling**: You can:
- Fill forward (`df.fillna(method='ffill')`)
- Interpolate (`df.interpolate()`)
- Drop stocks with low coverage
- Focus on date ranges where all stocks are present

## Example: Loading Data for Modeling

```python
import pandas as pd

# Load master file
df = pd.read_csv('data/master_stock_data.csv', index_col=0, parse_dates=True)

# Check data
print(f"Shape: {df.shape}")
print(f"Date range: {df.index.min()} to {df.index.max()}")
print(f"Stocks: {len(df.columns)}")

# Get stocks with >95% coverage
coverage = df.notna().sum() / len(df)
good_stocks = coverage[coverage > 0.95].index.tolist()
print(f"\nStocks with >95% coverage: {len(good_stocks)}")

# Filter to complete data range
df_filtered = df[good_stocks]

# Handle remaining missing values
df_clean = df_filtered.fillna(method='ffill').fillna(method='bfill')

print(f"\nClean data shape: {df_clean.shape}")
print(f"Missing values: {df_clean.isna().sum().sum()}")
```

## Stock List

Current stocks tracked (45 total):
```
AAPL, ABBV, ACN, AES, AMGN, AMZN, APPN, ASML, AVNT, AZN,
BAYRY, BIIB, BMY, COST, FTNT, GILD, GOOG, GSK, IBM, JNJ,
LLY, MRK, MSFT, NDAQ, NFLX, NICE, NVDA, NVS, PATH, PFE,
PSTG, PWR, REGN, SAM, SCHD, SGMO, SNOW, SNY, SWKS, TEVA,
TTD, VOO, VRTX, ZM, ZTS
```

**To add/remove stocks**: Edit the stock list in [stock_data_downloader.ipynb](stock_data_downloader.ipynb)

## Troubleshooting

**"Master file not found"**
- Run `python3 consolidate_historical_data.py` to create it

**"Duplicate timestamps"**
- This is normal - the append script removes them automatically
- Existing data takes precedence over new data

**"No new data downloaded"**
- Check that start date is before end date
- Verify market was open on those dates
- Check internet connection for Yahoo Finance

**"Package not found"**
- Run: `pip install -r requirements.txt`

## Logs

All operations are logged:

- **[data/master_file_creation_log.txt](data/master_file_creation_log.txt)** - Master file creation details
- **[data/append_log.txt](data/append_log.txt)** - All append operations
- **[logs/master_download_log.txt](/Users/paulhake/Documents/old_stock_charts/stockcharts_data/stock_data_logs/master_download_log.txt)** - Download history (old location)

## Next Steps

1. ✅ Master file created - Ready for modeling!
2. 📥 Use [stock_data_downloader.ipynb](stock_data_downloader.ipynb) to download new data
3. 🔄 Append new data to master file regularly
4. 📊 Load `data/master_stock_data.csv` in your modeling notebook
5. 🚀 Build your models!

## Questions?

- Check [README.md](README.md) for general project info
- See [stock_data_downloader.ipynb](stock_data_downloader.ipynb) for download options
- Review log files in `data/` for operation details
