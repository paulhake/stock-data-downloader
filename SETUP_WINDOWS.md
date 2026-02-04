# Windows Setup Instructions for Stock Data Downloader

This guide will help you set up and run the `stock_data_downloader.ipynb` notebook on Windows.

## Prerequisites

- Windows 10 or 11
- Internet connection
- Administrator access (for Python installation)

## Step 1: Install Python

1. **Download Python 3.8 or newer** from [python.org](https://www.python.org/downloads/)
   - Click the yellow "Download Python" button
   - Choose Python 3.10 or 3.11 (recommended)

2. **Run the installer**
   - ⚠️ **IMPORTANT**: Check the box "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify installation**
   - Open Command Prompt (search for `cmd` in Start menu)
   - Type: `python --version`
   - You should see something like `Python 3.11.x`

## Step 2: Install Required Packages

Open Command Prompt and navigate to the project folder:

```cmd
cd C:\path\to\old_stock_charts
```

Install all required packages using pip:

```cmd
pip install -r requirements_downloader.txt
```

This will install:
- pandas (data manipulation)
- numpy (numerical computing)
- yfinance (stock data download)
- jupyter (notebook interface)
- All necessary dependencies

**Installation may take 5-10 minutes depending on your internet speed.**

## Step 3: Launch Jupyter Notebook

In the same Command Prompt window:

```cmd
jupyter notebook
```

This will:
- Start the Jupyter server
- Automatically open your web browser to `http://localhost:8888`

If the browser doesn't open automatically, copy the URL from the Command Prompt (it will look like `http://localhost:8888/?token=...`)

## Step 4: Run the Notebook

1. In the Jupyter browser interface, click on `stock_data_downloader.ipynb`

2. **Run cells in order** by clicking each cell and pressing `Shift+Enter`, or:
   - Click "Cell" → "Run All" to run everything

3. The notebook will:
   - Auto-detect your last download date
   - Download new stock data
   - Save CSV files to `stockcharts_data/data_yfinance/`
   - Create logs in `logs/` folder

## Step 5: Customize (Optional)

To override automatic date detection, edit the main download cell:

```python
# Change these lines:
custom_start_date = "2026-01-21"  # Your desired start date
custom_end_date = "2026-02-10"    # Your desired end date
```

Then run the cell again with `Shift+Enter`.

## Troubleshooting

### "Python is not recognized..."
- Python wasn't added to PATH during installation
- **Solution**: Reinstall Python and check "Add Python to PATH"

### "pip is not recognized..."
- Usually fixed by reinstalling Python with PATH option
- **Alternative**: Use `python -m pip install -r requirements_downloader.txt`

### SSL Certificate Errors
- Windows firewall or antivirus blocking connections
- **Solution**: Temporarily disable antivirus during download, or add Python to allowed apps

### Jupyter won't start
- Port 8888 may be in use
- **Solution**: Try `jupyter notebook --port 8889`

### yfinance download errors
- Yahoo Finance API may be temporarily unavailable
- **Solution**: Wait a few minutes and try again
- Check internet connection

### Missing data warnings
- Normal if markets were closed (weekends/holidays)
- The notebook automatically skips non-trading days

## File Structure After Setup

```
old_stock_charts/
├── stock_data_downloader.ipynb  ← Main notebook
├── requirements_downloader.txt  ← Package list
├── SETUP_WINDOWS.md            ← This file
├── stockcharts_data/
│   └── data_yfinance/
│       ├── newf_data_all.csv
│       └── newf_raw_prices_*.csv  ← Downloaded data files
└── logs/
    ├── master_download_log.txt
    └── download_log_*.txt         ← Detailed logs
```

## Daily Usage

After initial setup, to download new data:

1. Open Command Prompt
2. Navigate to project folder: `cd C:\path\to\old_stock_charts`
3. Start Jupyter: `jupyter notebook`
4. Open the notebook and run all cells
5. Check the logs folder for download confirmation

## Virtual Environment (Optional but Recommended)

To keep packages isolated:

```cmd
# Create virtual environment
python -m venv stock_env

# Activate it
stock_env\Scripts\activate

# Install packages
pip install -r requirements_downloader.txt

# Run Jupyter
jupyter notebook
```

To deactivate the virtual environment when done:
```cmd
deactivate
```

## Need Help?

- Check the logs in the `logs/` folder for detailed error messages
- Ensure all folders have write permissions
- Try running Command Prompt as Administrator
- Verify your internet connection is stable

## Stock Ticker Customization

To modify which stocks are downloaded, edit the stock list in the notebook:

```python
stocks = 'AAPL NVDA GOOG MSFT AMZN'.split()  # Your custom list
```

Current list includes 45 stocks including tech, pharma, and index funds.
