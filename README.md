# Stock Data Downloader

Automated tool for downloading intraday stock price data from Yahoo Finance with intelligent date detection, comprehensive logging, and complete data consolidation system.

## Features

- **🤖 Auto-detection**: Automatically finds the last download date and continues from there
- **📊 5-minute intervals**: Downloads high-frequency intraday stock price data
- **📁 Organized storage**: Saves data with consistent naming convention
- **📝 Detailed logging**: Creates comprehensive logs for every download operation
- **🎯 Customizable**: Override dates and stock lists as needed
- **💾 Multiple stocks**: Download 45+ stocks simultaneously
- **🔄 Data consolidation**: Merge all historical data into a single master file
- **➕ Easy appending**: Add new downloads to master file with deduplication

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection

### Installation

1. Clone or download this repository

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Launch Jupyter Notebook:
```bash
jupyter notebook
```

4. Open `stock_data_downloader.ipynb` and run all cells

That's it! The notebook will:
- Detect your last download automatically
- Download new data up to today
- Save everything with proper naming
- Create detailed logs
- Optionally append to master data file

## Data Consolidation

### Create Master File

Consolidate all historical CSV files into a single master file:

```bash
python3 consolidate_historical_data.py
```

This creates `data/master_stock_data.csv` with all available data.

### Append New Data

After downloading new data, append it to the master file:

```bash
python3 append_to_master.py path/to/newf_raw_prices_*.csv
```

Or use the append cell in `stock_data_downloader.ipynb`.

### Documentation

- **[CONSOLIDATION_GUIDE.md](CONSOLIDATION_GUIDE.md)** - Complete workflow guide
- **[DATA_STATUS.md](DATA_STATUS.md)** - Current data coverage report

See these guides for detailed instructions on consolidation, appending, and working with the master file

## Usage

### Default Mode (Automatic)

Simply run all cells in the notebook. It will:
1. Find the most recent CSV file in `stockcharts_data/data_yfinance/`
2. Extract the end date from the filename
3. Download data from that date + 1 day until today
4. Save and log everything

### Custom Date Range

Edit the configuration cell in the notebook:

```python
# Override automatic detection
custom_start_date = "2026-01-21"
custom_end_date = "2026-02-10"
```

### Customize Stock List

Edit the stock list in the notebook:

```python
stocks = 'AAPL NVDA GOOG MSFT AMZN'.split()
```

**Default stocks included** (45 total):
- **Tech**: AAPL, NVDA, GOOG, MSFT, AMZN, IBM, NFLX, ASML, FTNT, NICE
- **Pharma/Bio**: PFE, JNJ, ABBV, MRK, AMGN, BMY, GILD, LLY, GSK, AZN, NVS, SNY, BIIB, REGN, VRTX, ZTS, SGMO, TEVA, BAYRY
- **Finance/Services**: NDAQ, ACN, APPN, PSTG, PATH, ZM, SNOW, AVNT
- **Energy/Utilities**: AES, PWR, SAM
- **Consumer**: COST
- **ETFs**: SCHD, VOO
- **Other**: TTD, SWKS

## File Structure

```
stock-data-downloader/
├── stock_data_downloader.ipynb  # Main notebook
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── SETUP_WINDOWS.md             # Windows setup guide
├── stockcharts_data/
│   └── data_yfinance/
│       └── newf_raw_prices_*.csv  # Downloaded data files
└── logs/
    ├── master_download_log.txt
    └── download_log_*.txt         # Detailed logs per download
```

## Data Format

### Output CSV Files

Files are saved with date-based naming (works on Windows, Mac, and Linux):
```
newf_raw_prices_2026-01-21_2026-02-03.csv
```

CSV structure:
- **Index**: Datetime (5-minute intervals)
- **Columns**: Stock tickers
- **Values**: Closing prices at each timestamp

Example:
```
Datetime                       AAPL        NVDA        GOOG
2026-01-21 14:30:00+00:00     244.91      145.32      189.45
2026-01-21 14:35:00+00:00     245.12      145.67      189.62
...
```

### Log Files

**Individual logs** (`download_log_YYYYMMDD_HHMMSS.txt`):
- Download timestamp
- Date range covered
- File size and location
- Row/column counts
- Data completeness percentage
- Per-stock statistics

**Master log** (`master_download_log.txt`):
- One-line summary of each download
- Quick reference for all historical downloads

## How It Works

### 1. Date Detection
The notebook scans `stockcharts_data/data_yfinance/` for files matching:
```
newf_raw_prices_*.csv
```

It parses the filenames to extract end dates and finds the most recent one.

### 2. Data Download
Uses the `yfinance` library to fetch:
- **Interval**: 5-minute bars
- **Data**: Close prices for all stocks
- **Range**: Last download date + 1 to today (or custom dates)

### 3. Save & Log
- Saves CSV with consistent naming convention
- Creates detailed log with statistics
- Appends summary to master log
- Ensures data directories exist

## Platform-Specific Instructions

### Windows
See [SETUP_WINDOWS.md](SETUP_WINDOWS.md) for detailed Windows setup instructions.

### macOS/Linux
```bash
# Install packages
pip install -r requirements.txt

# Launch Jupyter
jupyter notebook
```

## Troubleshooting

### No data downloaded
- Check internet connection
- Verify markets were open (no weekends/holidays)
- Try a wider date range

### SSL/Certificate errors
- Update certifi: `pip install --upgrade certifi`
- Check firewall/antivirus settings

### Import errors
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`
- Check Python version: `python --version` (needs 3.8+)

### File permission errors
- Run as administrator (Windows) or use `sudo` (macOS/Linux)
- Check folder write permissions

## Advanced Usage

### Virtual Environment (Recommended)

Keep packages isolated:

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Running Without Jupyter

Convert notebook to Python script:
```bash
jupyter nbconvert --to script stock_data_downloader.ipynb
python stock_data_downloader.py
```

### Automated Daily Downloads

**macOS/Linux (cron):**
```bash
# Edit crontab
crontab -e

# Add line (runs daily at 4:30 PM after market close)
30 16 * * 1-5 cd /path/to/stock-data-downloader && /path/to/python stock_data_downloader.py
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: Daily, 4:30 PM, weekdays
4. Action: Start Program
   - Program: `C:\path\to\python.exe`
   - Arguments: `stock_data_downloader.py`
   - Start in: `C:\path\to\stock-data-downloader`

## API Rate Limits

Yahoo Finance has informal rate limits:
- Avoid downloading same data repeatedly
- Space out downloads (built-in with auto-detection)
- The notebook is designed to only fetch new data

## Data Considerations

- **Market hours**: Data only available during trading hours (9:30 AM - 4:00 PM ET)
- **Weekends/Holidays**: No data on non-trading days
- **Extended hours**: After-hours trading included (up to ~8:55 PM ET)
- **Data quality**: Yahoo Finance data is free but may have occasional gaps

## Contributing

Feel free to:
- Add more stocks to the default list
- Enhance logging features
- Improve error handling
- Add data validation

## License

This is an open-source tool for educational and personal use.

**Disclaimer**: This tool is for informational purposes only. Not financial advice. Use at your own risk.

## Dependencies

Main packages:
- `yfinance` - Yahoo Finance API wrapper
- `pandas` - Data manipulation
- `numpy` - Numerical computing
- `jupyter` - Interactive notebook interface

See [requirements.txt](requirements.txt) for complete list.

## Changelog

### Version 1.0 (2026-02-04)
- Initial release
- Auto-detection of last download date
- Comprehensive logging system
- Support for 45+ stocks
- Windows/macOS/Linux compatibility

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files in `logs/` folder
3. Verify requirements are installed correctly
4. Check Yahoo Finance API status

## Acknowledgments

- Built with [yfinance](https://github.com/ranaroussi/yfinance)
- Data provided by Yahoo Finance
