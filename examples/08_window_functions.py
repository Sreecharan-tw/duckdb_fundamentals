"""
DuckDB Window Functions
Example 08 demonstrates window functions like ROW_NUMBER, RANK, LAG, LEAD.
"""

import duckdb

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Window Functions")
print("=" * 60)

# Create sample sales data
print("\n1. Creating sample sales data...")
conn.execute("""
    CREATE TABLE sales AS
    SELECT
        row_number() OVER () as sale_id,
        CASE
            WHEN row_number() OVER () % 2 = 1 THEN 'East'
            ELSE 'West'
        END as region,
        DATE '2024-01-01' + INTERVAL 1 day * FLOOR(RANDOM() * 30) as sale_date,
        100 + FLOOR(RANDOM() * 900) as amount
    FROM range(1, 21)
""")

result = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
print(f"✓ Created sales table with {result} records")

# ROW_NUMBER
print("\n2. ROW_NUMBER (assign sequential numbers)...")
result = conn.execute("""
    SELECT
        sale_id,
        amount,
        ROW_NUMBER() OVER (ORDER BY amount DESC) as rank_all,
        ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) as rank_by_region
    FROM sales
    ORDER BY amount DESC
    LIMIT 10
""").fetchall()

print("Top 10 sales by amount:")
print(f"{'ID':<5} {'Amount':>8} {'Overall Rank':>14} {'Region Rank':>12}")
print("-" * 42)
for sale_id, amount, rank_all, rank_by_region in result:
    print(f"{sale_id:<5} ${amount:>7} {rank_all:>14} {rank_by_region:>12}")

# RANK and DENSE_RANK
print("\n3. RANK vs DENSE_RANK...")
conn.execute("""
    CREATE TABLE scores AS
    SELECT 'Alice' as name, 95 as score
    UNION ALL
    SELECT 'Bob', 88
    UNION ALL
    SELECT 'Charlie', 95
    UNION ALL
    SELECT 'Diana', 88
    UNION ALL
    SELECT 'Eve', 92
""")

result = conn.execute("""
    SELECT
        name,
        score,
        RANK() OVER (ORDER BY score DESC) as rank,
        DENSE_RANK() OVER (ORDER BY score DESC) as dense_rank,
        ROW_NUMBER() OVER (ORDER BY score DESC) as row_num
    FROM scores
""").fetchall()

print("Score rankings:")
print(f"{'Name':<10} {'Score':>6} {'RANK':>6} {'DENSE_RANK':>11} {'ROW_NUM':>8}")
print("-" * 45)
for name, score, rank, dense_rank, row_num in result:
    print(f"{name:<10} {score:>6} {rank:>6} {dense_rank:>11} {row_num:>8}")

# LAG and LEAD
print("\n4. LAG and LEAD (previous and next values)...")

conn.execute("""
    CREATE TABLE daily_sales AS
    SELECT
        DATE '2024-01-01' + INTERVAL 1 day * (row_number() OVER () - 1) as sale_date,
        100 + FLOOR(RANDOM() * 500) as amount
    FROM range(1, 11)
""")

result = conn.execute("""
    SELECT
        sale_date,
        amount,
        LAG(amount) OVER (ORDER BY sale_date) as prev_day_amount,
        LEAD(amount) OVER (ORDER BY sale_date) as next_day_amount,
        amount - LAG(amount) OVER (ORDER BY sale_date) as day_change
    FROM daily_sales
    ORDER BY sale_date
""").fetchall()

print("Daily sales with previous and next day comparison:")
print(f"{'Date':<12} {'Amount':>8} {'Prev Day':>9} {'Next Day':>9} {'Change':>8}")
print("-" * 50)
for date, amount, prev_amt, next_amt, change in result:
    change_str = f"{change:+.0f}" if change else "---"
    print(f"{str(date):<12} ${amount:>7} ${prev_amt:>8} ${next_amt:>8} {change_str:>8}")

# FIRST_VALUE and LAST_VALUE
print("\n5. FIRST_VALUE and LAST_VALUE...")
result = conn.execute("""
    SELECT
        sale_date,
        amount,
        FIRST_VALUE(amount) OVER (ORDER BY sale_date) as first_in_period,
        LAST_VALUE(amount) OVER (
            ORDER BY sale_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) as last_in_period,
        FIRST_VALUE(amount) OVER (ORDER BY sale_date) as starting_amount
    FROM daily_sales
    ORDER BY sale_date
""").fetchall()

print("First and last values:")
print(f"{'Date':<12} {'Amount':>8} {'First':>8} {'Last':>8}")
print("-" * 40)
for date, amount, first_val, last_val, _ in result:
    print(f"{str(date):<12} ${amount:>7} ${first_val:>7} ${last_val:>7}")

# NTILE (percentiles)
print("\n6. NTILE (divide into buckets)...")
result = conn.execute("""
    SELECT
        name,
        score,
        NTILE(4) OVER (ORDER BY score) as quartile,
        NTILE(2) OVER (ORDER BY score) as half
    FROM scores
    ORDER BY score DESC
""").fetchall()

print("Score percentiles:")
print(f"{'Name':<10} {'Score':>6} {'Quartile':>9} {'Half':>5}")
print("-" * 35)
for name, score, quartile, half in result:
    print(f"{name:<10} {score:>6} {quartile:>9} {half:>5}")

# PERCENT_RANK and CUME_DIST
print("\n7. PERCENT_RANK and CUME_DIST...")
result = conn.execute("""
    SELECT
        name,
        score,
        PERCENT_RANK() OVER (ORDER BY score) as percent_rank,
        CUME_DIST() OVER (ORDER BY score) as cume_dist
    FROM scores
    ORDER BY score DESC
""").fetchall()

print("Rank distributions:")
print(f"{'Name':<10} {'Score':>6} {'Percent Rank':>14} {'Cumulative Dist':>16}")
print("-" * 50)
for name, score, pct_rank, cume_dist in result:
    print(f"{name:<10} {score:>6} {pct_rank:>14.2%} {cume_dist:>16.2%}")

# Windowing clauses
print("\n8. ROWS BETWEEN (moving average)...")
result = conn.execute("""
    SELECT
        sale_date,
        amount,
        AVG(amount) OVER (
            ORDER BY sale_date
            ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
        ) as moving_avg_3day,
        SUM(amount) OVER (
            ORDER BY sale_date
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ) as cumulative_3day
    FROM daily_sales
    ORDER BY sale_date
""").fetchall()

print("Moving averages and cumulative sums:")
print(f"{'Date':<12} {'Amount':>8} {'3-Day Avg':>10} {'3-Day Sum':>10}")
print("-" * 45)
for date, amount, mov_avg, cum_sum in result:
    print(f"{str(date):<12} ${amount:>7} ${mov_avg:>9.2f} ${cum_sum:>9.2f}")

# Partition with multiple columns
print("\n9. Multiple partitions...")
result = conn.execute("""
    SELECT
        region,
        sale_date,
        amount,
        ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) as region_rank,
        AVG(amount) OVER (PARTITION BY region) as region_avg
    FROM sales
    ORDER BY region, amount DESC
    LIMIT 10
""").fetchall()

print("Sales ranked within each region:")
print(f"{'Region':<8} {'Date':<12} {'Amount':>8} {'Rank':>5} {'Avg':>8}")
print("-" * 45)
for region, date, amount, rank, avg_amt in result:
    print(f"{region:<8} {str(date):<12} ${amount:>7} {rank:>5} ${avg_amt:>7.2f}")

# Running total
print("\n10. Running total...")
result = conn.execute("""
    SELECT
        sale_date,
        amount,
        SUM(amount) OVER (
            ORDER BY sale_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) as running_total
    FROM daily_sales
    ORDER BY sale_date
""").fetchall()

print("Running total of sales:")
print(f"{'Date':<12} {'Amount':>8} {'Running Total':>14}")
print("-" * 38)
for date, amount, running_total in result:
    print(f"{str(date):<12} ${amount:>7} ${running_total:>13.2f}")

print("\n" + "=" * 60)
print("Window functions complete!")
print("=" * 60)
