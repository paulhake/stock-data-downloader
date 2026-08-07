#!/usr/bin/env python3
"""
Append New Data to Master File

This script appends newly downloaded data to the master stock data CSV file.
It handles deduplication and maintains chronological order.

Usage:
    python append_to_master.py <new_data_file.csv>

Or use from within a script/notebook:
    from append_to_master import append_new_data
    append_new_data("path/to/new_file.csv")
"""

import pandas as pd
import os
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def append_new_data(new_data_path, master_path="./data/master_stock_data.csv", backup=True):
    """
    Append new data to the master file

    Args:
        new_data_path: Path to new CSV file to append
        master_path: Path to master CSV file
        backup: Whether to create a backup before appending

    Returns:
        dict: Summary of the append operation
    """
    print("="*60)
    print("APPEND NEW DATA TO MASTER FILE")
    print("="*60)

    # Check files exist
    if not os.path.exists(new_data_path):
        print(f"ERROR: New data file not found: {new_data_path}")
        return None

    if not os.path.exists(master_path):
        print(f"ERROR: Master file not found: {master_path}")
        print(f"Run consolidate_historical_data.py first to create the master file.")
        return None

    # Create backup if requested
    if backup:
        backup_path = master_path.replace(".csv", f"_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        print(f"\nCreating backup: {backup_path}")
        import shutil
        shutil.copy2(master_path, backup_path)

    # Load existing master data
    print(f"\nLoading master file: {master_path}")
    master_df = pd.read_csv(master_path, index_col=0)
    master_df.index = pd.to_datetime(master_df.index, utc=True)
    print(f"  Current shape: {master_df.shape}")
    print(f"  Date range: {master_df.index.min()} to {master_df.index.max()}")

    # Load new data
    print(f"\nLoading new data: {new_data_path}")
    new_df = pd.read_csv(new_data_path, index_col=0)
    new_df.index = pd.to_datetime(new_df.index, utc=True)
    print(f"  New data shape: {new_df.shape}")
    print(f"  Date range: {new_df.index.min()} to {new_df.index.max()}")

    # Check for new columns (stocks)
    master_cols = set(master_df.columns)
    new_cols = set(new_df.columns)

    added_stocks = new_cols - master_cols
    removed_stocks = master_cols - new_cols

    if added_stocks:
        print(f"\n  NEW STOCKS detected: {', '.join(sorted(added_stocks))}")
    if removed_stocks:
        print(f"  REMOVED STOCKS detected: {', '.join(sorted(removed_stocks))}")

    # Combine dataframes
    print("\nCombining data...")
    combined = pd.concat([master_df, new_df], axis=0)

    # Sort by datetime
    combined = combined.sort_index()

    # Count duplicates before removal
    duplicates = combined.index.duplicated().sum()
    print(f"  Found {duplicates} duplicate timestamps")

    # Remove duplicates (keep first - existing data takes precedence)
    combined = combined[~combined.index.duplicated(keep='first')]

    # Calculate changes
    rows_added = len(combined) - len(master_df)

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"Original master file: {len(master_df):,} rows x {len(master_df.columns)} stocks")
    print(f"New data file: {len(new_df):,} rows x {len(new_df.columns)} stocks")
    print(f"Duplicate timestamps removed: {duplicates:,}")
    print(f"Net rows added: {rows_added:,}")
    print(f"Updated master file: {len(combined):,} rows x {len(combined.columns)} stocks")
    print(f"New date range: {combined.index.min()} to {combined.index.max()}")

    # Save updated master file
    print(f"\nSaving updated master file...")
    combined.to_csv(master_path)

    file_size = os.path.getsize(master_path)
    file_size_mb = file_size / (1024 * 1024)
    print(f"Saved: {master_path}")
    print(f"File size: {file_size_mb:.2f} MB")

    # Create append log
    log_dir = os.path.dirname(master_path)
    log_path = os.path.join(log_dir, "append_log.txt")

    log_entry = f"""
{'='*60}
Append Operation - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}
New data file: {os.path.basename(new_data_path)}
New data date range: {new_df.index.min()} to {new_df.index.max()}
Rows in new data: {len(new_df):,}
Duplicate timestamps: {duplicates:,}
Net rows added: {rows_added:,}
Updated master rows: {len(combined):,}
Updated master date range: {combined.index.min()} to {combined.index.max()}
"""

    if added_stocks:
        log_entry += f"New stocks added: {', '.join(sorted(added_stocks))}\n"
    if removed_stocks:
        log_entry += f"Stocks no longer present: {', '.join(sorted(removed_stocks))}\n"

    with open(log_path, 'a') as f:
        f.write(log_entry)

    print(f"\nAppend log updated: {log_path}")

    print(f"\n{'='*60}")
    print("APPEND COMPLETE!")
    print(f"{'='*60}")

    return {
        'original_rows': len(master_df),
        'new_data_rows': len(new_df),
        'duplicates_removed': duplicates,
        'rows_added': rows_added,
        'final_rows': len(combined),
        'date_range': (combined.index.min(), combined.index.max()),
        'added_stocks': list(added_stocks),
        'removed_stocks': list(removed_stocks)
    }


def main():
    """Main function for command-line usage"""
    if len(sys.argv) < 2:
        print("Usage: python append_to_master.py <new_data_file.csv>")
        print("\nExample:")
        print("  python append_to_master.py ./stockcharts_data/data_yfinance/newf_raw_prices_2026-02-18_2026-03-01.csv")
        sys.exit(1)

    new_data_path = sys.argv[1]
    result = append_new_data(new_data_path)

    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
