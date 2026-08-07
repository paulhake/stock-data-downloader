# Stock Data Status Report

**Generated**: August 7, 2026 (Updated with complete consolidation)

## Master Data File Status

**File**: [data/master_stock_data.csv](data/master_stock_data.csv)

### Coverage Summary

- **Date Range**: March 14, 2024 → February 17, 2026
- **Duration**: 705 days (23.5 months)
- **Time Periods**: 44,690 rows (5-minute intervals)
- **Stocks Tracked**: 45 unique tickers
- **Total Data Points**: ~2,011,050
- **File Size**: 26.63 MB

### Data Completeness

The master file now includes **ALL available CSV files** from:
1. `/old_stock_charts/stockcharts_data/data_yfinance/` (June 2024 - Feb 2026)
2. `/old_stock_charts/stockcharts_data/` (March 2024 - June 2024)

This represents a **64% increase** in data compared to the initial consolidation:
- **Previous**: 27,276 time periods (Jun 2024 - Feb 2026)
- **Current**: 44,690 time periods (Mar 2024 - Feb 2026)
- **Added**: 17,414 time periods from early 2024

## Missing Data Gap

### March - July 2026 Data

The download logs in `stock_data_logs/` reference CSV files from March-July 2026:

| Log Date | Referenced File | Status |
|----------|----------------|---------|
| 2026-03-03 | newf_raw_prices_2026-02-02_2026-03-02.csv | ❌ Not Found |
| 2026-03-09 | newf_raw_prices_2026-02-02_2026-03-09.csv | ❌ Not Found |
| 2026-03-15 | newf_raw_prices_2026-02-02_2026-03-13.csv | ❌ Not Found |
| 2026-03-23 | newf_raw_prices_2026-02-02_2026-03-20.csv | ❌ Not Found |
| 2026-03-30 | newf_raw_prices_2026-02-02_2026-03-27.csv | ❌ Not Found |
| 2026-04-12 | newf_raw_prices_2026-03-02_2026-04-10.csv | ❌ Not Found |
| 2026-04-20 | newf_raw_prices_2026-03-02_2026-04-20.csv | ❌ Not Found |
| 2026-04-29 | newf_raw_prices_2026-03-02_2026-04-28.csv | ❌ Not Found |
| 2026-06-08 | newf_raw_prices_2026-04-13_2026-06-05.csv | ❌ Not Found |
| 2026-07-05 | newf_raw_prices_2026-05-15_2026-07-02.csv | ❌ Not Found |
| 2026-08-02 | newf_raw_prices_2026-06-05_2026-07-31.csv | ❌ Not Found |

**Impact**: Gap from **February 18, 2026 → July 31, 2026** (~5.5 months)

These files were downloaded according to the logs but are not currently in the file system. If you locate these files, you can use `append_to_master.py` to add them to the master file.

## Stock Coverage

### All 45 Stocks

```
AAPL, ABBV, ACN, AES, AMGN, AMZN, APPN, ASML, AVNT, AZN,
BAYRY, BIIB, BMY, COST, FTNT, GILD, GOOG, GSK, IBM, JNJ,
LLY, MRK, MSFT, NDAQ, NFLX, NICE, NVDA, NVS, PATH, PFE,
PSTG, PWR, REGN, SAM, SCHD, SGMO, SNOW, SNY, SWKS, TEVA,
TTD, VOO, VRTX, ZM, ZTS
```

### Coverage Notes

- **3 stocks** (AES, SCHD, VOO) were added later in the tracking period
- **BAYRY** has limited coverage in early periods
- Most stocks have >95% data completeness within their active periods

## Data Format

### File Structure

```csv
,AAPL,ABBV,ACN,AES,AMGN,AMZN,...
2024-03-14 09:30:00+00:00,172.32,160.5,380.92,...
2024-03-14 09:35:00+00:00,172.45,160.8,381.10,...
```

- **Index**: DateTime (UTC timezone-aware)
- **Columns**: Stock tickers
- **Values**: 5-minute closing prices
- **Frequency**: 5-minute intervals during US market hours

### Market Hours

- **Regular Hours**: 9:30 AM - 4:00 PM ET
- **UTC Times**: Varies by DST (13:30-20:00 or 14:30-21:00)
- **~78 intervals** per trading day

## Timeline

### Available Data

```
2024-03-14 ████████████████████████████████████████ 2024-06-25
2024-06-26 ████████████████████████████████████████ 2026-02-17
```

### Missing Data

```
2026-02-18 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 2026-07-31
```

## Recommendations

### 1. Recover Missing 2026 Data (If Available)

If the March-July 2026 CSV files exist elsewhere:

```bash
# Append each file to master
python3 append_to_master.py path/to/newf_raw_prices_2026-03-*.csv
```

### 2. Download Fresh Data (If Recovery Not Possible)

Use [stock_data_downloader.ipynb](stock_data_downloader.ipynb) to re-download March-July 2026:

```python
# In the notebook, set:
custom_start_date = "2026-02-18"
custom_end_date = "2026-07-31"
```

**Note**: Yahoo Finance may have limitations on historical 5-minute data availability.

### 3. Continue Forward from Current Date

Use the automated downloader going forward to prevent future gaps:

```bash
# Downloads latest data and appends to master automatically
jupyter notebook stock_data_downloader.ipynb
```

## Using the Data

### Load Master File

```python
import pandas as pd

# Load data
df = pd.read_csv('data/master_stock_data.csv',
                 index_col=0,
                 parse_dates=True)

print(f"Shape: {df.shape}")
print(f"Date range: {df.index.min()} to {df.index.max()}")
print(f"Duration: {(df.index.max() - df.index.min()).days} days")
```

### Handle Missing Values

```python
# Check completeness per stock
coverage = (df.notna().sum() / len(df) * 100).sort_values(ascending=False)
print(coverage)

# Filter to high-coverage stocks
good_stocks = coverage[coverage > 90].index.tolist()
df_filtered = df[good_stocks]

# Forward fill missing values
df_clean = df_filtered.fillna(method='ffill')
```

### Split Train/Test

```python
# Use 80% for training, 20% for testing
split_date = df.index[int(len(df) * 0.8)]

train = df[df.index < split_date]
test = df[df.index >= split_date]

print(f"Train: {train.shape} ({train.index.min()} to {train.index.max()})")
print(f"Test: {test.shape} ({test.index.min()} to {test.index.max()})")
```

## Files & Logs

### Data Files
- **[data/master_stock_data.csv](data/master_stock_data.csv)** - Main data file
- **data/master_stock_data_backup_*.csv** - Backups (created before updates)

### Logs
- **[data/master_file_creation_log.txt](data/master_file_creation_log.txt)** - Creation details
- **[data/append_log.txt](data/append_log.txt)** - Append history

### Scripts
- **[consolidate_historical_data.py](consolidate_historical_data.py)** - Consolidation script
- **[append_to_master.py](append_to_master.py)** - Append helper
- **[stock_data_downloader.ipynb](stock_data_downloader.ipynb)** - Automated downloader

## Support

For issues or questions:
1. Check [CONSOLIDATION_GUIDE.md](CONSOLIDATION_GUIDE.md) for detailed workflow
2. Review log files in `data/` directory
3. See [README.md](README.md) for general project info
