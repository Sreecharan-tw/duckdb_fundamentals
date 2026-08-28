"""
DuckDB Time Series Analysis
Example 11 demonstrates time series operations and date/time functions.
"""

import duckdb
from datetime import datetime, timedelta

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Time Series Analysis")
print("=" * 60)

# Create time series data
print("\n1. Creating time series data...")
conn.execute("""
    CREATE TABLE stock_prices AS
    SELECT
        DATE '2024-01-01' + INTERVAL 1 day * (row_number() OVER () - 1) as trading_date,
        'AAPL' as ticker,
        150.00 + FLOOR(RANDOM() * 20) + (row_number() OVER () % 10) / 10.0 as close_price,
        (150.00 + FLOOR(RANDOM() * 20) + (row_number() OVER () % 10) / 10.0) * 1.02 as high_price,
        (150.00 + FLOOR(RANDOM() * 20) + (row_number() OVER () % 10) / 10.0) * 0.98 as low_price,
        1000000 + FLOOR(RANDOM() * 500000) as volume
    FROM range(1, 31)
""")
print("✓ Stock price time series created")

# Display sample data
result = conn.execute("""
    SELECT trading_date, close_price, high_price, low_price, volume
    FROM stock_prices
    LIMIT 5
""").fetchall()

print("Sample stock prices:")
print(f"{'Date':<12} {'Close':>8} {'High':>8} {'Low':>8} {'Volume':>10}")
print("-" * 50)
for date, close, high, low, volume in result:
    print(f"{str(date):<12} ${close:>7.2f} ${high:>7.2f} ${low:>7.2f} {volume:>10}")

# Date functions
print("\n2. Date functions...")
result = conn.execute("""
    SELECT
        trading_date,
        DAYNAME(trading_date) as day_name,
        EXTRACT(WEEK FROM trading_date) as week_num,
        EXTRACT(MONTH FROM trading_date) as month,
        EXTRACT(QUARTER FROM trading_date) as quarter,
        EXTRACT(YEAR FROM trading_date) as year,
        EXTRACT(DAY FROM trading_date) as day
    FROM stock_prices
    LIMIT 3
""").fetchall()

print("Date components:")
for date, day_name, week, month, quarter, year, day in result:
    print(f"  {date}: {day_name}, Week {week}, Month {month}, Q{quarter}, Day {day}")

# Date grouping
print("\n3. Aggregating by date intervals...")
result = conn.execute("""
    SELECT
        DATE_TRUNC('week', trading_date)::DATE as week_start,
        COUNT(*) as num_trading_days,
        AVG(close_price) as weekly_avg_price,
        MIN(low_price) as weekly_low,
        MAX(high_price) as weekly_high
    FROM stock_prices
    GROUP BY DATE_TRUNC('week', trading_date)
    ORDER BY week_start
""").fetchall()

print("Weekly aggregations:")
print(f"{'Week Start':<12} {'Days':>5} {'Avg Price':>11} {'Low':>8} {'High':>8}")
print("-" * 50)
for week_start, num_days, avg_price, low, high in result:
    print(f"{str(week_start):<12} {num_days:>5} ${avg_price:>10.2f} ${low:>7.2f} ${high:>7.2f}")

# Date arithmetic
print("\n4. Date arithmetic...")
result = conn.execute("""
    SELECT
        trading_date,
        close_price,
        trading_date + INTERVAL 7 day as one_week_later,
        trading_date - INTERVAL 30 day as thirty_days_ago,
        CURRENT_DATE - trading_date as days_from_today
    FROM stock_prices
    ORDER BY trading_date DESC
    LIMIT 3
""").fetchall()

print("Date arithmetic:")
for date, price, one_week_later, thirty_ago, days_from_today in result:
    print(f"  {date}: ${price:.2f}")
    print(f"    One week later: {one_week_later}")
    print(f"    Thirty days ago: {thirty_ago}")
    print(f"    Days from today: {days_from_today}")

# Time series with lag
print("\n5. Price changes (LAG for previous price)...")
result = conn.execute("""
    SELECT
        trading_date,
        close_price,
        LAG(close_price) OVER (ORDER BY trading_date) as prev_close,
        close_price - LAG(close_price) OVER (ORDER BY trading_date) as price_change,
        ROUND(
            (close_price - LAG(close_price) OVER (ORDER BY trading_date)) /
            LAG(close_price) OVER (ORDER BY trading_date) * 100, 2
        ) as percent_change
    FROM stock_prices
    ORDER BY trading_date
    LIMIT 10
""").fetchall()

print("Daily price changes:")
print(f"{'Date':<12} {'Close':>8} {'Previous':>9} {'Change':>8} {'% Change':>9}")
print("-" * 50)
for date, close, prev_close, change, pct_change in result:
    change_str = f"{change:+.2f}" if change is not None else "---"
    pct_str = f"{pct_change:+.2f}%" if pct_change is not None else "---"
    print(f"{str(date):<12} ${close:>7.2f} ${prev_close:>8.2f} {change_str:>8} {pct_str:>9}")

# Moving averages
print("\n6. Moving averages...")
result = conn.execute("""
    SELECT
        trading_date,
        close_price,
        AVG(close_price) OVER (
            ORDER BY trading_date
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ) as ma_5day,
        AVG(close_price) OVER (
            ORDER BY trading_date
            ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
        ) as ma_10day
    FROM stock_prices
    ORDER BY trading_date
""").fetchall()

print("Moving averages:")
print(f"{'Date':<12} {'Price':>8} {'MA 5-Day':>10} {'MA 10-Day':>10}")
print("-" * 45)
for date, price, ma5, ma10 in result:
    ma5_str = f"${ma5:.2f}" if ma5 is not None else "---"
    ma10_str = f"${ma10:.2f}" if ma10 is not None else "---"
    print(f"{str(date):<12} ${price:>7.2f} {ma5_str:>10} {ma10_str:>10}")

# Date filtering
print("\n7. Date range filtering...")
result = conn.execute("""
    SELECT
        trading_date,
        close_price,
        volume
    FROM stock_prices
    WHERE trading_date BETWEEN DATE '2024-01-08' AND DATE '2024-01-14'
    ORDER BY trading_date
""").fetchall()

print("Trading data for week of Jan 8-14:")
for date, price, volume in result:
    print(f"  {date}: ${price:.2f}, volume: {volume}")

# Timestamp functions
print("\n8. Timestamp operations...")
conn.execute("""
    CREATE TABLE events AS
    SELECT
        row_number() OVER () as event_id,
        TIMESTAMP '2024-08-28 09:00:00' + INTERVAL 1 hour * row_number() OVER () as event_time,
        'Event ' || row_number() OVER () as event_name
    FROM range(1, 6)
""")

result = conn.execute("""
    SELECT
        event_time,
        event_name,
        EXTRACT(HOUR FROM event_time) as hour,
        EXTRACT(MINUTE FROM event_time) as minute
    FROM events
""").fetchall()

print("Event times:")
for event_time, name, hour, minute in result:
    print(f"  {event_time}: {name} (Hour: {hour}, Minute: {minute})")

# Time between dates
print("\n9. Time differences...")
result = conn.execute("""
    SELECT
        event_id,
        event_time,
        LAG(event_time) OVER (ORDER BY event_time) as prev_event_time,
        EXTRACT(EPOCH FROM (event_time - LAG(event_time) OVER (ORDER BY event_time))) / 3600 as hours_since_prev
    FROM events
""").fetchall()

print("Time intervals between events:")
for event_id, event_time, prev_time, hours_diff in result:
    hours_str = f"{hours_diff:.1f}" if hours_diff is not None else "---"
    print(f"  Event {event_id} ({event_time}): {hours_str} hours since previous")

# Current timestamp
print("\n10. Current date/time functions...")
result = conn.execute("""
    SELECT
        CURRENT_DATE as today,
        CURRENT_TIMESTAMP as now,
        DATE_TRUNC('month', CURRENT_DATE) as month_start,
        DATE_TRUNC('year', CURRENT_DATE) as year_start
""").fetchone()

print("Current date/time:")
print(f"  Today: {result[0]}")
print(f"  Now: {result[1]}")
print(f"  Month start: {result[2]}")
print(f"  Year start: {result[3]}")

print("\n" + "=" * 60)
print("Time series analysis complete!")
print("=" * 60)
