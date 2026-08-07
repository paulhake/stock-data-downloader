#!/usr/bin/env python3
"""
Consolidate Historical Stock Data

This script reads all CSV files from the old_stock_charts folder and combines them
into a single master CSV file with 5-minute closing prices.

Features:
- Handles both old format (long) and new format (wide) CSV files
- Removes duplicate timestamps
- Handles missing dates and stocks that appear/disappear from feeds
- Creates a clean master CSV file for modeling
- Compatible with stock_data_downloader.ipynb output format
"""

import pandas as pd
import glob
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def read_old_format(filepath):
    """
    Read old format CSV: long format with columns [index, stock, Adj Close, date]
    or [datet, stock, date, close, volume, datetime]
    Convert to wide format with Datetime index and stock columns
    """
    print(f"  Reading old format: {os.path.basename(filepath)}")
    df = pd.read_csv(filepath)

    # Check if it has 'datet' column (early 2024 format)
    if 'datet' in df.columns:
        df['datetime_index'] = pd.to_datetime(df['datet'], utc=True)
        df = df.set_index('datetime_index')
        # Pivot to wide format using 'close' column
        wide_df = df.pivot_table(index=df.index, columns='stock', values='close')
    else:
        # Original old format with index
        df = pd.read_csv(filepath, index_col=0)
        # Parse index as datetime
        df.index = pd.to_datetime(df.index, utc=True)
        # Pivot to wide format
        wide_df = df.pivot_table(index=df.index, columns='stock', values='Adj Close')

    return wide_df


def read_new_format(filepath):
    """
    Read new format CSV: wide format with Datetime index and stock columns
    """
    print(f"  Reading new format: {os.path.basename(filepath)}")
    df = pd.read_csv(filepath, index_col=0)

    # Parse index as datetime
    df.index = pd.to_datetime(df.index, utc=True)

    return df


def detect_format(filepath):
    """
    Detect whether CSV is old format (long) or new format (wide)
    Handles multiple old format variations
    """
    # Read first few rows to check structure
    sample = pd.read_csv(filepath, nrows=5)

    # Old format variations:
    # - 'stock' and 'Adj Close' columns
    # - 'datet', 'stock', 'close' columns (early 2024 format)
    if 'stock' in sample.columns and ('Adj Close' in sample.columns or 'close' in sample.columns):
        return 'old'
    else:
        return 'new'


def consolidate_data(data_dir):
    """
    Read all CSV files from data_dir and consolidate into single DataFrame

    Args:
        data_dir: Path to directory containing CSV files

    Returns:
        DataFrame with consolidated data
    """
    print(f"\nScanning directory: {data_dir}")

    # Find all CSV files except the master file
    csv_pattern = os.path.join(data_dir, "*raw_prices*.csv")
    csv_files = glob.glob(csv_pattern)

    # Exclude any existing master files
    csv_files = [f for f in csv_files if 'data_all' not in f and 'master' not in f.lower()]

    print(f"Found {len(csv_files)} CSV files to process\n")

    if not csv_files:
        print("No CSV files found!")
        return None

    # Read all files
    all_dataframes = []

    for filepath in sorted(csv_files):
        try:
            # Detect format and read accordingly
            format_type = detect_format(filepath)

            if format_type == 'old':
                df = read_old_format(filepath)
            else:
                df = read_new_format(filepath)

            if df is not None and not df.empty:
                all_dataframes.append(df)
                print(f"    Shape: {df.shape}, Date range: {df.index.min()} to {df.index.max()}")

        except Exception as e:
            print(f"  ERROR reading {os.path.basename(filepath)}: {e}")

    if not all_dataframes:
        print("\nNo data was successfully loaded!")
        return None

    print(f"\n{'='*60}")
    print(f"Consolidating {len(all_dataframes)} DataFrames...")
    print(f"{'='*60}")

    # Concatenate all dataframes
    combined = pd.concat(all_dataframes, axis=0)

    print(f"Combined shape before deduplication: {combined.shape}")
    print(f"Date range: {combined.index.min()} to {combined.index.max()}")

    # Sort by datetime
    combined = combined.sort_index()

    # Remove duplicate timestamps (keep first occurrence)
    duplicates = combined.index.duplicated().sum()
    print(f"Found {duplicates} duplicate timestamps")

    combined = combined[~combined.index.duplicated(keep='first')]
    print(f"Shape after deduplication: {combined.shape}")

    # Get list of all unique stocks
    all_stocks = sorted(combined.columns.tolist())
    print(f"\nUnique stocks in dataset: {len(all_stocks)}")
    print(f"Stocks: {', '.join(all_stocks)}")

    # Calculate statistics
    total_points = combined.shape[0] * combined.shape[1]
    valid_points = combined.notna().sum().sum()
    missing_points = combined.isna().sum().sum()
    completeness = (valid_points / total_points) * 100

    print(f"\nData Statistics:")
    print(f"  Time periods: {combined.shape[0]:,}")
    print(f"  Stock tickers: {combined.shape[1]}")
    print(f"  Total data points: {total_points:,}")
    print(f"  Valid data points: {valid_points:,}")
    print(f"  Missing data points: {missing_points:,}")
    print(f"  Completeness: {completeness:.2f}%")

    return combined


def save_master_file(df, output_dir, output_filename="master_stock_data.csv"):
    """
    Save consolidated data to master CSV file

    Args:
        df: DataFrame to save
        output_dir: Directory to save file
        output_filename: Name of output file
    """
    if df is None or df.empty:
        print("No data to save!")
        return

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, output_filename)

    print(f"\n{'='*60}")
    print(f"Saving master file...")
    print(f"{'='*60}")

    df.to_csv(output_path)

    file_size = os.path.getsize(output_path)
    file_size_mb = file_size / (1024 * 1024)

    print(f"Saved to: {output_path}")
    print(f"File size: {file_size_mb:.2f} MB")

    # Create a summary log
    log_content = f"""Master Stock Data File - Creation Log
{'='*60}
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

FILE INFORMATION:
  Filename: {output_filename}
  Path: {output_path}
  Size: {file_size_mb:.2f} MB ({file_size:,} bytes)

DATA STATISTICS:
  Time Periods (Rows): {len(df):,}
  Stock Tickers (Columns): {len(df.columns)}
  Date Range: {df.index.min()} to {df.index.max()}
  Duration: {(df.index.max() - df.index.min()).days} days

  Total Data Points: {df.shape[0] * df.shape[1]:,}
  Valid Data Points: {df.notna().sum().sum():,}
  Missing Data Points: {df.isna().sum().sum():,}
  Completeness: {(df.notna().sum().sum() / (df.shape[0] * df.shape[1]) * 100):.2f}%

STOCK TICKERS ({len(df.columns)}):
  {', '.join(sorted(df.columns.tolist()))}

PER-STOCK STATISTICS:
"""

    for col in sorted(df.columns):
        col_valid = df[col].notna().sum()
        col_completeness = (col_valid / len(df)) * 100
        log_content += f"  {col}: {col_valid:,}/{len(df):,} points ({col_completeness:.1f}%)\n"

    log_content += "\n" + "="*60 + "\n"

    log_path = os.path.join(output_dir, "master_file_creation_log.txt")
    with open(log_path, 'w') as f:
        f.write(log_content)

    print(f"Log saved to: {log_path}")

    return output_path


def main():
    """Main execution function"""
    print("="*60)
    print("STOCK DATA CONSOLIDATION SCRIPT")
    print("="*60)

    # Configuration - search multiple directories
    data_dirs = [
        "/Users/paulhake/Documents/old_stock_charts/stockcharts_data/data_yfinance/",
        "/Users/paulhake/Documents/old_stock_charts/stockcharts_data/"
    ]
    output_dir = "/Users/paulhake/Documents/stock-data-downloader/data/"
    output_filename = "master_stock_data.csv"

    # Consolidate data from all directories
    all_dataframes = []
    for data_dir in data_dirs:
        print(f"\n{'='*60}")
        print(f"Processing directory: {data_dir}")
        print(f"{'='*60}")
        df = consolidate_data(data_dir)
        if df is not None:
            all_dataframes.append(df)

    # Combine all dataframes from different directories
    if not all_dataframes:
        print("\nNo data found in any directory!")
        return

    print(f"\n{'='*60}")
    print(f"COMBINING DATA FROM ALL DIRECTORIES")
    print(f"{'='*60}")

    master_df = pd.concat(all_dataframes, axis=0)
    master_df = master_df.sort_index()

    # Remove duplicates
    duplicates = master_df.index.duplicated().sum()
    print(f"Found {duplicates} duplicate timestamps across all directories")
    master_df = master_df[~master_df.index.duplicated(keep='first')]

    print(f"Final combined shape: {master_df.shape}")
    print(f"Final date range: {master_df.index.min()} to {master_df.index.max()}")

    if master_df is not None:
        # Save master file
        output_path = save_master_file(master_df, output_dir, output_filename)

        print(f"\n{'='*60}")
        print("CONSOLIDATION COMPLETE!")
        print(f"{'='*60}")
        print(f"Master file: {output_path}")
        print("\nYou can now use stock_data_downloader.ipynb to append new data")
        print("to this master file moving forward.")

        print(f"\nNOTE: Data from March-July 2026 mentioned in logs is not")
        print(f"available in the file system. The master file contains all")
        print(f"available CSV files found.")
    else:
        print("\nConsolidation failed!")


if __name__ == "__main__":
    main()
