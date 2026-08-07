#!/usr/bin/env python3
"""
Stock Chart Labeler

Interactive UI for viewing and labeling daily stock price patterns.
Creates clean charts showing 5-minute closing prices for manual classification.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Use TkAgg backend for better GUI support
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import numpy as np

class ChartLabeler:
    def __init__(self, data_path='data/master_stock_data.csv'):
        """Initialize the chart labeler"""
        print("Loading data...")
        self.df = pd.read_csv(data_path, index_col=0, parse_dates=True)
        self.df.index = pd.to_datetime(self.df.index, utc=True)

        print(f"Data loaded: {self.df.shape}")
        print(f"Date range: {self.df.index.min()} to {self.df.index.max()}")

        # Get list of stocks
        self.stocks = sorted(self.df.columns.tolist())

        # Get list of unique dates
        self.dates = sorted(self.df.index.normalize().unique())

        print(f"Available stocks: {len(self.stocks)}")
        print(f"Available dates: {len(self.dates)}")

        # Current state
        self.current_stock = self.stocks[0] if self.stocks else None
        self.current_date = None

        # Setup GUI
        self.setup_gui()

    def setup_gui(self):
        """Setup the Tkinter GUI"""
        self.root = tk.Tk()
        self.root.title("Stock Chart Labeler")
        self.root.geometry("1600x900")

        # Control panel at top
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(side=tk.TOP, fill=tk.X)

        # Stock selection
        ttk.Label(control_frame, text="Stock:").pack(side=tk.LEFT, padx=5)
        self.stock_var = tk.StringVar(value=self.current_stock)
        stock_combo = ttk.Combobox(control_frame, textvariable=self.stock_var,
                                   values=self.stocks, width=15)
        stock_combo.pack(side=tk.LEFT, padx=5)

        # Date entry
        ttk.Label(control_frame, text="Start Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.date_var = tk.StringVar()
        date_entry = ttk.Entry(control_frame, textvariable=self.date_var, width=15)
        date_entry.pack(side=tk.LEFT, padx=5)

        # Load button
        load_btn = ttk.Button(control_frame, text="Load Charts", command=self.load_charts)
        load_btn.pack(side=tk.LEFT, padx=5)

        # Info label
        self.info_var = tk.StringVar(value="Select stock and date, then click Load Charts")
        info_label = ttk.Label(control_frame, textvariable=self.info_var, foreground="blue")
        info_label.pack(side=tk.LEFT, padx=20)

        # Canvas for charts
        self.chart_frame = ttk.Frame(self.root)
        self.chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Store figure and canvas
        self.figure = None
        self.canvas = None

    def get_trading_days(self, start_date, num_days=5):
        """Get the next N trading days starting from start_date"""
        start_date = pd.to_datetime(start_date, utc=True).normalize()

        # Get all dates that have data
        available_dates = self.df.index.normalize().unique()

        # Filter to dates >= start_date
        future_dates = available_dates[available_dates >= start_date]

        if len(future_dates) < num_days:
            return future_dates[:len(future_dates)]

        return future_dates[:num_days]

    def get_day_data(self, stock, date):
        """Get data for a specific stock and date"""
        date = pd.to_datetime(date, utc=True).normalize()

        # Get all data for this date
        day_data = self.df[self.df.index.normalize() == date][stock]

        return day_data.dropna()

    def create_chart(self, ax, stock, date, data):
        """Create a single chart without axes"""
        if len(data) == 0:
            ax.text(0.5, 0.5, 'No Data', ha='center', va='center',
                   fontsize=14, transform=ax.transAxes)
            ax.set_title(f"{stock} - {date.strftime('%Y-%m-%d')}",
                        fontsize=12, fontweight='bold', pad=10)
            ax.axis('off')
            return

        # Calculate daily log return
        first_price = data.iloc[0]
        last_price = data.iloc[-1]
        log_return = np.log(last_price / first_price)
        log_return_pct = log_return * 100  # Convert to percentage

        # Determine color based on return (green for positive, red for negative)
        return_color = 'green' if log_return >= 0 else 'red'

        # Plot the line
        time_indices = range(len(data))
        ax.plot(time_indices, data.values, linewidth=2, color='#1f77b4')

        # Set title with stock name, date, and log return
        title = f"{stock} - {date.strftime('%Y-%m-%d')}\nLog Return: {log_return_pct:+.2f}%"
        ax.set_title(title, fontsize=11, fontweight='bold', pad=10,
                    color=return_color if log_return != 0 else 'black')

        # Remove axes, ticks, and labels
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Add subtle grid for reference (optional)
        # ax.grid(True, alpha=0.1, linestyle='--')

    def load_charts(self):
        """Load and display 5 charts"""
        stock = self.stock_var.get()
        date_str = self.date_var.get()

        # Validate inputs
        if not stock:
            messagebox.showerror("Error", "Please select a stock")
            return

        if not date_str:
            messagebox.showerror("Error", "Please enter a start date")
            return

        try:
            start_date = pd.to_datetime(date_str, utc=True)
        except:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return

        # Get trading days
        trading_days = self.get_trading_days(start_date, num_days=5)

        if len(trading_days) == 0:
            messagebox.showerror("Error", f"No data available for {stock} from {date_str}")
            return

        self.info_var.set(f"Loading {len(trading_days)} days for {stock}...")
        self.root.update()

        # Clear previous figure
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if self.figure:
            plt.close(self.figure)

        # Create new figure with 5 subplots side by side
        self.figure, axes = plt.subplots(1, 5, figsize=(16, 4))
        self.figure.tight_layout(pad=3.0)

        # Handle case where we have fewer than 5 days
        if not isinstance(axes, np.ndarray):
            axes = [axes]

        # Create charts for each day
        for i, (ax, date) in enumerate(zip(axes, trading_days)):
            day_data = self.get_day_data(stock, date)
            self.create_chart(ax, stock, date, day_data)

        # Hide unused subplots
        for i in range(len(trading_days), 5):
            axes[i].axis('off')

        # Embed figure in tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.info_var.set(f"Showing {len(trading_days)} days for {stock} starting {trading_days[0].strftime('%Y-%m-%d')}")

    def run(self):
        """Run the GUI"""
        print("Starting GUI...")
        self.root.mainloop()


def main():
    """Main function"""
    print("="*60)
    print("STOCK CHART LABELER")
    print("="*60)

    # Check if data file exists
    import os
    if not os.path.exists('data/master_stock_data.csv'):
        print("ERROR: Master data file not found!")
        print("Run consolidate_historical_data.py first to create the master file.")
        return

    # Create and run labeler
    labeler = ChartLabeler()
    labeler.run()


if __name__ == "__main__":
    main()
