"""
DuckDB Aggregations and GROUP BY
Example 06 demonstrates aggregation functions and grouping.
"""

import duckdb

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Aggregations and GROUP BY")
print("=" * 60)

# Create sample data
print("\n1. Creating sample sales data...")
conn.execute("""
    CREATE TABLE sales AS
    SELECT
        row_number() OVER () as sale_id,
        CASE
            WHEN row_number() OVER () % 3 = 1 THEN 'North'
            WHEN row_number() OVER () % 3 = 2 THEN 'South'
            ELSE 'West'
        END as region,
        CASE
            WHEN row_number() OVER () % 4 = 1 THEN 'Electronics'
            WHEN row_number() OVER () % 4 = 2 THEN 'Clothing'
            WHEN row_number() OVER () % 4 = 3 THEN 'Home'
            ELSE 'Sports'
        END as category,
        DATE '2024-01-01' + INTERVAL 1 day * FLOOR(RANDOM() * 30) as sale_date,
        10 + FLOOR(RANDOM() * 990) as amount
    FROM range(100)
""")
print("✓ Sales table created with 100 records")

# Basic aggregations
print("\n2. Basic aggregation functions...")
result = conn.execute("""
    SELECT
        COUNT(*) as total_sales,
        SUM(amount) as total_revenue,
        AVG(amount) as avg_amount,
        MIN(amount) as min_amount,
        MAX(amount) as max_amount
    FROM sales
""").fetchone()

print(f"  Total Sales: {result[0]}")
print(f"  Total Revenue: ${result[1]}")
print(f"  Average Amount: ${result[2]:.2f}")
print(f"  Min Amount: ${result[3]}")
print(f"  Max Amount: ${result[4]}")

# GROUP BY with aggregations
print("\n3. Sales by region...")
result = conn.execute("""
    SELECT
        region,
        COUNT(*) as num_sales,
        SUM(amount) as total_revenue,
        AVG(amount) as avg_sale,
        MAX(amount) as largest_sale
    FROM sales
    GROUP BY region
    ORDER BY total_revenue DESC
""").fetchall()

print("Region Summary:")
for region, num_sales, total_rev, avg_sale, largest in result:
    print(f"  {region:10} | Sales: {num_sales:3} | Revenue: ${total_rev:7.0f} | Avg: ${avg_sale:7.2f} | Max: ${largest:5}")

# Multiple GROUP BY columns
print("\n4. Sales by region and category...")
result = conn.execute("""
    SELECT
        region,
        category,
        COUNT(*) as num_sales,
        SUM(amount) as revenue,
        AVG(amount) as avg_amount
    FROM sales
    GROUP BY region, category
    ORDER BY region, revenue DESC
""").fetchall()

print("Region-Category Summary:")
print(f"{'Region':<10} {'Category':<12} {'Sales':>5} {'Revenue':>8} {'Avg Sale':>8}")
print("-" * 50)
for region, category, num_sales, revenue, avg_amt in result:
    print(f"{region:<10} {category:<12} {num_sales:>5} ${revenue:>7.0f} ${avg_amt:>7.2f}")

# COUNT with DISTINCT
print("\n5. Distinct counts...")
result = conn.execute("""
    SELECT
        COUNT(DISTINCT region) as num_regions,
        COUNT(DISTINCT category) as num_categories,
        COUNT(DISTINCT sale_date) as num_sale_dates
    FROM sales
""").fetchone()

print(f"  Unique regions: {result[0]}")
print(f"  Unique categories: {result[1]}")
print(f"  Unique sale dates: {result[2]}")

# HAVING clause (filter groups)
print("\n6. Regions with total revenue > $5000...")
result = conn.execute("""
    SELECT
        region,
        COUNT(*) as num_sales,
        SUM(amount) as total_revenue
    FROM sales
    GROUP BY region
    HAVING SUM(amount) > 5000
    ORDER BY total_revenue DESC
""").fetchall()

print("High-revenue regions:")
for region, num_sales, total_rev in result:
    print(f"  {region}: {num_sales} sales, ${total_rev:.0f}")

# Statistical aggregations
print("\n7. Statistical functions...")
result = conn.execute("""
    SELECT
        region,
        COUNT(*) as num_sales,
        STDDEV_POP(amount) as std_dev,
        VARIANCE_POP(amount) as variance
    FROM sales
    GROUP BY region
""").fetchall()

print("Statistical Summary:")
for region, num_sales, std_dev, variance in result:
    print(f"  {region}: {num_sales} sales, Std Dev: {std_dev:.2f}, Variance: {variance:.2f}")

# MIN and MAX with GROUP BY
print("\n8. First and last sale amounts by region...")
result = conn.execute("""
    SELECT
        region,
        MIN(amount) as smallest_purchase,
        MAX(amount) as largest_purchase,
        MAX(amount) - MIN(amount) as price_range
    FROM sales
    GROUP BY region
    ORDER BY price_range DESC
""").fetchall()

print("Purchase Price Range:")
for region, min_amt, max_amt, price_range in result:
    print(f"  {region}: ${min_amt} - ${max_amt} (range: ${price_range})")

# String aggregation (GROUP_CONCAT)
print("\n9. Categories sold in each region...")
result = conn.execute("""
    SELECT
        region,
        GROUP_CONCAT(DISTINCT category, ', ') as categories,
        COUNT(DISTINCT category) as num_categories
    FROM sales
    GROUP BY region
""").fetchall()

print("Categories by Region:")
for region, categories, num_cats in result:
    print(f"  {region}: {categories}")

# Date-based aggregations
print("\n10. Sales by date...")
result = conn.execute("""
    SELECT
        DATE_TRUNC('week', sale_date)::DATE as week_start,
        COUNT(*) as num_sales,
        SUM(amount) as weekly_revenue,
        AVG(amount) as avg_sale
    FROM sales
    GROUP BY DATE_TRUNC('week', sale_date)
    ORDER BY week_start
    LIMIT 5
""").fetchall()

print("Weekly Sales Summary:")
print(f"{'Week Start':<15} {'Sales':>6} {'Revenue':>10} {'Avg Sale':>10}")
print("-" * 45)
for week_start, num_sales, revenue, avg_sale in result:
    print(f"{str(week_start):<15} {num_sales:>6} ${revenue:>9.0f} ${avg_sale:>9.2f}")

print("\n" + "=" * 60)
print("Aggregations complete!")
print("=" * 60)
