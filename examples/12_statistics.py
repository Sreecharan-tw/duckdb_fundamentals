"""
DuckDB Statistical Functions
Example 12 demonstrates statistical calculations and data analysis.
"""

import duckdb

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Statistical Functions")
print("=" * 60)

# Create sample data
print("\n1. Creating sample dataset...")
conn.execute("""
    CREATE TABLE measurements AS
    SELECT
        row_number() OVER () as measurement_id,
        CASE
            WHEN row_number() OVER () % 2 = 1 THEN 'Group A'
            ELSE 'Group B'
        END as group_name,
        100 + FLOOR(RANDOM() * 100 + RANDOM() * 50) as value
    FROM range(1, 101)
""")
print("✓ Dataset created with 100 measurements")

# Basic statistics
print("\n2. Basic descriptive statistics...")
result = conn.execute("""
    SELECT
        COUNT(*) as count,
        SUM(value) as total,
        AVG(value) as mean,
        MIN(value) as min,
        MAX(value) as max,
        MAX(value) - MIN(value) as range
    FROM measurements
""").fetchone()

print(f"  Count: {result[0]}")
print(f"  Sum: {result[1]}")
print(f"  Mean: {result[2]:.2f}")
print(f"  Min: {result[3]}")
print(f"  Max: {result[4]}")
print(f"  Range: {result[5]}")

# Standard deviation and variance
print("\n3. Variance and standard deviation...")
result = conn.execute("""
    SELECT
        AVG(value) as mean,
        STDDEV_POP(value) as stddev_population,
        STDDEV_SAMP(value) as stddev_sample,
        VARIANCE_POP(value) as variance_population,
        VARIANCE_SAMP(value) as variance_sample
    FROM measurements
""").fetchone()

print(f"  Mean: {result[0]:.2f}")
print(f"  Population Std Dev: {result[1]:.2f}")
print(f"  Sample Std Dev: {result[2]:.2f}")
print(f"  Population Variance: {result[3]:.2f}")
print(f"  Sample Variance: {result[4]:.2f}")

# Percentiles
print("\n4. Percentiles...")
result = conn.execute("""
    SELECT
        QUANTILE_CONT(value, 0.25) as q1_25,
        QUANTILE_CONT(value, 0.50) as median_50,
        QUANTILE_CONT(value, 0.75) as q3_75,
        QUANTILE_CONT(value, 0.90) as p90,
        QUANTILE_CONT(value, 0.95) as p95,
        QUANTILE_CONT(value, 0.99) as p99
    FROM measurements
""").fetchone()

print("  Quartiles and Percentiles:")
print(f"    25th percentile (Q1): {result[0]:.2f}")
print(f"    50th percentile (Median): {result[1]:.2f}")
print(f"    75th percentile (Q3): {result[2]:.2f}")
print(f"    90th percentile: {result[3]:.2f}")
print(f"    95th percentile: {result[4]:.2f}")
print(f"    99th percentile: {result[5]:.2f}")

# Group statistics
print("\n5. Statistics by group...")
result = conn.execute("""
    SELECT
        group_name,
        COUNT(*) as count,
        AVG(value) as mean,
        STDDEV_SAMP(value) as stddev,
        MIN(value) as min,
        MAX(value) as max
    FROM measurements
    GROUP BY group_name
    ORDER BY group_name
""").fetchall()

print(f"{'Group':<10} {'Count':>6} {'Mean':>8} {'Std Dev':>8} {'Min':>6} {'Max':>6}")
print("-" * 48)
for group, count, mean, stddev, min_val, max_val in result:
    print(f"{group:<10} {count:>6} {mean:>8.2f} {stddev:>8.2f} {min_val:>6} {max_val:>6}")

# Correlation (requires multiple columns)
print("\n6. Creating correlated data...")
conn.execute("""
    CREATE TABLE bivariate AS
    SELECT
        row_number() OVER () as x_val,
        row_number() OVER () + FLOOR(RANDOM() * 50) as y_val
    FROM range(1, 51)
""")

result = conn.execute("""
    SELECT
        COUNT(*) as n,
        AVG(x_val) as mean_x,
        AVG(y_val) as mean_y,
        STDDEV_SAMP(x_val) as stddev_x,
        STDDEV_SAMP(y_val) as stddev_y
    FROM bivariate
""").fetchone()

print(f"  X: mean={result[1]:.2f}, stddev={result[3]:.2f}")
print(f"  Y: mean={result[2]:.2f}, stddev={result[4]:.2f}")

# Skewness (asymmetry)
print("\n7. Distribution analysis...")

# Create skewed data
conn.execute("""
    CREATE TABLE skewed_data AS
    SELECT
        CASE
            WHEN RANDOM() < 0.7 THEN 50 + FLOOR(RANDOM() * 30)
            ELSE 100 + FLOOR(RANDOM() * 50)
        END as value
    FROM range(1, 201)
""")

result = conn.execute("""
    SELECT
        COUNT(*) as count,
        AVG(value) as mean,
        STDDEV_SAMP(value) as stddev,
        MIN(value) as min,
        MAX(value) as max
    FROM skewed_data
""").fetchone()

print("Skewed distribution:")
print(f"  Count: {result[0]}")
print(f"  Mean: {result[1]:.2f}")
print(f"  Std Dev: {result[2]:.2f}")
print(f"  Min: {result[3]}, Max: {result[4]}")

# Covariance (manual calculation)
print("\n8. Covariance calculation...")
result = conn.execute("""
    SELECT
        AVG(x_val * y_val) - AVG(x_val) * AVG(y_val) as covariance
    FROM bivariate
""").fetchone()

print(f"  Covariance (X, Y): {result[0]:.2f}")

# Rank and percentile rank
print("\n9. Ranking and percentile ranks...")
result = conn.execute("""
    SELECT
        measurement_id,
        value,
        RANK() OVER (ORDER BY value) as rank,
        PERCENT_RANK() OVER (ORDER BY value) as percent_rank,
        CUME_DIST() OVER (ORDER BY value) as cumulative_dist,
        ROUND(PERCENT_RANK() OVER (ORDER BY value) * 100, 1) as percentile
    FROM measurements
    WHERE measurement_id IN (1, 10, 50, 90, 100)
    ORDER BY value
""").fetchall()

print("Rank and percentile data:")
print(f"{'ID':<5} {'Value':>7} {'Rank':>6} {'Percentile':>11}")
print("-" * 35)
for mid, value, rank, pct_rank, cume_dist, percentile in result:
    print(f"{mid:<5} {value:>7} {rank:>6} {percentile:>10.1f}%")

# Histogram/binning
print("\n10. Data distribution (histogram)...")
result = conn.execute("""
    SELECT
        CASE
            WHEN value < 120 THEN '100-119'
            WHEN value < 140 THEN '120-139'
            WHEN value < 160 THEN '140-159'
            WHEN value < 180 THEN '160-179'
            ELSE '180+'
        END as bin,
        COUNT(*) as frequency,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM measurements), 1) as percent
    FROM measurements
    GROUP BY bin
    ORDER BY bin
""").fetchall()

print("Value distribution:")
print(f"{'Bin':<12} {'Frequency':>10} {'Percentage':>11}")
print("-" * 35)
for bin_label, freq, percent in result:
    bar_length = int(percent / 5)
    bar = '█' * bar_length
    print(f"{bin_label:<12} {freq:>10} {percent:>10.1f}% {bar}")

# Summary statistics by decile
print("\n11. Decile analysis...")
result = conn.execute("""
    SELECT
        NTILE(10) OVER (ORDER BY value) as decile,
        COUNT(*) as count,
        MIN(value) as min,
        MAX(value) as max,
        AVG(value) as avg
    FROM measurements
    GROUP BY NTILE(10) OVER (ORDER BY value)
    ORDER BY decile
""").fetchall()

print("By decile:")
print(f"{'Decile':>7} {'Count':>6} {'Min':>6} {'Max':>6} {'Avg':>7}")
print("-" * 35)
for decile, count, min_val, max_val, avg_val in result:
    print(f"{decile:>7} {count:>6} {min_val:>6} {max_val:>6} {avg_val:>7.2f}")

# Aggregate functions summary
print("\n12. Summary of aggregate functions...")
result = conn.execute("""
    SELECT
        COUNT(*) as total_count,
        COUNT(DISTINCT group_name) as unique_groups,
        SUM(value) as total_sum,
        AVG(value) as average,
        MIN(value) as minimum,
        MAX(value) as maximum,
        STDDEV_SAMP(value) as sample_stddev,
        VARIANCE_SAMP(value) as sample_variance
    FROM measurements
""").fetchone()

stats_dict = {
    'Count': result[0],
    'Unique Groups': result[1],
    'Sum': result[2],
    'Average': f"{result[3]:.2f}",
    'Min': result[4],
    'Max': result[5],
    'Sample Std Dev': f"{result[6]:.2f}",
    'Sample Variance': f"{result[7]:.2f}"
}

print("All measurements statistics:")
for key, value in stats_dict.items():
    print(f"  {key}: {value}")

print("\n" + "=" * 60)
print("Statistical functions complete!")
print("=" * 60)
