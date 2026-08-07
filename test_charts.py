#!/usr/bin/env python3
"""
Test script to verify chart generation works correctly
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for testing
from datetime import datetime
import numpy as np

# Load data
print("Loading data...")
df = pd.read_csv('data/master_stock_data.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df.index, utc=True)

print(f"Data shape: {df.shape}")
print(f"Date range: {df.index.min()} to {df.index.max()}")

# Get a sample stock and dates
stock = 'AAPL'
start_date = pd.to_datetime('2024-06-26', utc=True).normalize()

# Get 5 trading days
available_dates = df.index.normalize().unique()
future_dates = available_dates[available_dates >= start_date][:5]

print(f"\nTesting {stock} for dates:")
for date in future_dates:
    print(f"  {date.strftime('%Y-%m-%d')}")

# Create charts
fig, axes = plt.subplots(1, 5, figsize=(16, 4))
fig.tight_layout(pad=3.0)

for i, (ax, date) in enumerate(zip(axes, future_dates)):
    # Get day data
    day_data = df[df.index.normalize() == date][stock].dropna()

    print(f"\n{date.strftime('%Y-%m-%d')}: {len(day_data)} data points")
    if len(day_data) > 0:
        print(f"  Price range: ${day_data.min():.2f} - ${day_data.max():.2f}")
        # Calculate log return
        log_return = np.log(day_data.iloc[-1] / day_data.iloc[0])
        log_return_pct = log_return * 100
        print(f"  Log return: {log_return_pct:+.2f}%")

    # Plot
    if len(day_data) == 0:
        ax.text(0.5, 0.5, 'No Data', ha='center', va='center',
               fontsize=14, transform=ax.transAxes)
        title = f"{stock} - {date.strftime('%Y-%m-%d')}"
        return_color = 'black'
    else:
        time_indices = range(len(day_data))
        ax.plot(time_indices, day_data.values, linewidth=2, color='#1f77b4')

        # Calculate log return for title
        log_return = np.log(day_data.iloc[-1] / day_data.iloc[0])
        log_return_pct = log_return * 100
        return_color = 'green' if log_return >= 0 else 'red'
        title = f"{stock} - {date.strftime('%Y-%m-%d')}\nLog Return: {log_return_pct:+.2f}%"

    # Set title with log return
    ax.set_title(title, fontsize=11, fontweight='bold', pad=10,
                color=return_color)

    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

# Save test image
output_file = 'test_charts.png'
plt.savefig(output_file, dpi=150, bbox_inches='tight')
print(f"\n✓ Test charts saved to: {output_file}")
print("✓ Chart generation working correctly!")
