# Chart Labeler Guide

Interactive tool for viewing and labeling daily stock price patterns for machine learning classification.

## Purpose

This tool helps you manually review and categorize daily stock patterns to create labeled training data for an automated classifier.

## Features

- **Clean charts**: No axes or gridlines - just the price pattern
- **5-day view**: See 5 consecutive trading days side-by-side
- **Stock selection**: Choose any of 45 tracked stocks
- **Date navigation**: Jump to any date in your dataset
- **Simple UI**: Easy-to-use interface for quick review

## Usage

### Launch the Tool

```bash
python3 chart_labeler.py
```

This will open a GUI window with controls at the top and chart display below.

### View Charts

1. **Select Stock**: Choose from the dropdown (e.g., AAPL, NVDA, MSFT)
2. **Enter Date**: Type a start date in YYYY-MM-DD format (e.g., 2024-06-26)
3. **Click "Load Charts"**: Display 5 consecutive trading days

### Chart Information

Each chart shows:
- **Title**: Stock symbol and date (e.g., "AAPL - 2024-06-26")
- **Log Return**: Daily log return percentage (green = positive, red = negative)
- **Pattern**: 5-minute closing prices throughout the trading day
- **Clean design**: No axes, labels, or clutter - just the pattern

**Log Return Calculation**:
- Formula: `ln(last_price / first_price) * 100`
- Represents the percentage change from market open to close
- Color-coded: Green for gains, Red for losses

### Navigation Tips

**Finding dates with data**:
- Data ranges from **2024-03-14** to **2026-02-17**
- Gap exists: Feb 18 - July 31, 2026 (no data)
- Use dates where markets were open (weekdays, no holidays)

**Efficient review**:
1. Start with a date: `2024-06-26`
2. Review 5 days
3. Manually advance by 5 days: `2024-07-02`
4. Continue through dataset

## Typical Daily Patterns (Examples)

You'll want to categorize patterns like:

1. **Steady Uptrend** - Consistent rise throughout day
2. **Steady Downtrend** - Consistent decline throughout day
3. **Morning Rally** - Strong start, then plateau
4. **Morning Dump** - Drop at open, then recovery
5. **Volatile/Choppy** - Erratic movements up and down
6. **Flat/Sideways** - Little movement, range-bound
7. **V-Shape/Reversal** - Clear direction change mid-day

## Data Points

- **~78 data points** per day (5-minute intervals)
- **Market hours**: 9:30 AM - 4:00 PM ET
- **Missing data**: Some stocks have gaps (shown as "No Data")

## Test Charts

A test image is generated as `test_charts.png` showing sample AAPL charts. This helps verify the tool is working correctly.

## Next Steps (Future Features)

The current version focuses on chart viewing. Future enhancements will include:

- **Label selection**: Buttons to assign categories
- **Save labels**: Export to CSV/JSON
- **Keyboard shortcuts**: Quick navigation (arrow keys, number keys for labels)
- **Progress tracking**: See how many days you've labeled
- **Filter view**: Only show unlabeled days

## Troubleshooting

**"No data available"**
- Check the date is within range (2024-03-14 to 2026-02-17)
- Verify it's a trading day (not weekend/holiday)
- Some stocks have limited early coverage

**GUI doesn't open**
- Ensure tkinter is installed: `python3 -m tkinter`
- Check matplotlib is using TkAgg backend

**Timezone warnings**
- These are normal - data is stored in UTC

## Example Session

```bash
# Launch tool
python3 chart_labeler.py

# In the GUI:
# 1. Select "AAPL" from dropdown
# 2. Enter "2024-06-26" in date field
# 3. Click "Load Charts"
# 4. Review 5 days of AAPL patterns
# 5. (Future: Select label for each)
# 6. Enter next date: "2024-07-02"
# 7. Repeat
```

## Technical Details

### Data Loading

- Loads from `data/master_stock_data.csv`
- Automatically handles timezone-aware datetimes
- Filters to single-day data for each chart

### Chart Generation

- Uses matplotlib with TkAgg backend
- Figure size: 1600x400 pixels (5 charts @ 320 width each)
- Line width: 2px, color: blue (#1f77b4)
- Title font: 12pt bold

### Performance

- Initial load: ~2-5 seconds (loading 44,690 rows)
- Chart generation: <1 second for 5 days
- Memory usage: ~200-300 MB

## Files

- **[chart_labeler.py](chart_labeler.py)** - Main GUI application
- **[test_charts.py](test_charts.py)** - Test script (generates test_charts.png)
- **test_charts.png** - Sample output for verification

## Support

For issues:
1. Run `python3 test_charts.py` to verify chart generation
2. Check that `data/master_stock_data.csv` exists
3. Ensure all dependencies are installed: `pip install -r requirements.txt`
