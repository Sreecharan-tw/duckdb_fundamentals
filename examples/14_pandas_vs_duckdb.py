"""
Pandas vs DuckDB: Speed & Ease Comparison
Example 14 compares querying Parquet files with Pandas vs DuckDB.

Key findings:
- DuckDB is faster for complex analytical queries
- Pandas requires loading entire dataset into memory
- DuckDB can query Parquet files without loading all data
- SQL is often simpler than Pandas operations
"""

import duckdb
import pandas as pd
import time
import os

print("=" * 70)
print("Pandas vs DuckDB: Parquet Query Performance Comparison")
print("=" * 70)

# Step 1: Create a larger sample Parquet file
print("\n1. Creating sample Parquet file (100,000 rows)...")

parquet_file = '/tmp/sales_benchmark.parquet'

# Generate sample data
data = {
    'sale_id': range(1, 100001),
    'product': ['Electronics', 'Clothing', 'Home', 'Sports', 'Books'] * 20000,
    'region': ['North', 'South', 'East', 'West'] * 25000,
    'amount': [i * 1.23 % 1000 + 50 for i in range(1, 100001)],
    'quantity': [i % 100 + 1 for i in range(1, 100001)],
    'discount': [i % 50 / 100 for i in range(1, 100001)],
}

df_sample = pd.DataFrame(data)
df_sample.to_parquet(parquet_file)

file_size_mb = os.path.getsize(parquet_file) / (1024 * 1024)
print(f"✓ Parquet file created: {file_size_mb:.2f} MB")
print(f"  Rows: {len(df_sample):,}")
print(f"  Columns: {len(df_sample.columns)}")

# ============================================================================
# QUERY 1: Simple Filtering
# ============================================================================
print("\n" + "=" * 70)
print("QUERY 1: Filter by amount > 500 and quantity > 50")
print("=" * 70)

# Pandas approach
print("\n📊 PANDAS Approach:")
print("-" * 70)
print("""
# Load entire file into memory
df = pd.read_parquet('sales_benchmark.parquet')

# Filter rows
result = df[(df['amount'] > 500) & (df['quantity'] > 50)]

# Count results
count = len(result)
""")

start = time.time()
df_pandas = pd.read_parquet(parquet_file)
result_pandas = df_pandas[(df_pandas['amount'] > 500) & (df_pandas['quantity'] > 50)]
pandas_time = time.time() - start

print(f"Results: {len(result_pandas):,} rows")
print(f"Time: {pandas_time*1000:.2f}ms (includes loading entire file)")
print(f"Memory: {df_pandas.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")

# DuckDB approach
print("\n🦆 DUCKDB Approach:")
print("-" * 70)
print("""
# Query directly without loading full file
result = duckdb.sql(f"
    SELECT * FROM parquet_scan('{parquet_file}')
    WHERE amount > 500 AND quantity > 50
").fetchall()
""")

start = time.time()
result_duckdb = duckdb.sql(f"""
    SELECT * FROM read_parquet('{parquet_file}')
    WHERE amount > 500 AND quantity > 50
""").fetchall()
duckdb_time = time.time() - start

print(f"Results: {len(result_duckdb):,} rows")
print(f"Time: {duckdb_time*1000:.2f}ms (only reads filtered data)")

speedup = pandas_time / duckdb_time
print(f"\n🚀 SPEEDUP: DuckDB is {speedup:.1f}x faster")
print("   (DuckDB doesn't load unused data)")

# ============================================================================
# QUERY 2: Aggregation with GROUP BY
# ============================================================================
print("\n" + "=" * 70)
print("QUERY 2: Sum amount by product and region")
print("=" * 70)

# Pandas approach
print("\n📊 PANDAS Approach:")
print("-" * 70)
print("""
result = df.groupby(['product', 'region'])['amount'].sum().reset_index()
result.columns = ['product', 'region', 'total_amount']
result = result.sort_values('total_amount', ascending=False)
""")

start = time.time()
result_pandas = (
    df_pandas.groupby(['product', 'region'])['amount']
    .sum()
    .reset_index()
)
result_pandas.columns = ['product', 'region', 'total_amount']
result_pandas = result_pandas.sort_values('total_amount', ascending=False)
pandas_time = time.time() - start

print(f"Results:\n{result_pandas.head().to_string()}")
print(f"Time: {pandas_time*1000:.2f}ms")

# DuckDB approach
print("\n🦆 DUCKDB Approach:")
print("-" * 70)
print("""
result = duckdb.sql(f"
    SELECT product, region, SUM(amount) as total_amount
    FROM read_parquet('{parquet_file}')
    GROUP BY product, region
    ORDER BY total_amount DESC
").fetchdf()
""")

start = time.time()
result_duckdb = duckdb.sql(f"""
    SELECT product, region, SUM(amount) as total_amount
    FROM read_parquet('{parquet_file}')
    GROUP BY product, region
    ORDER BY total_amount DESC
""").fetchdf()
duckdb_time = time.time() - start

print(f"Results:\n{result_duckdb.head().to_string()}")
print(f"Time: {duckdb_time*1000:.2f}ms")

speedup = pandas_time / duckdb_time
print(f"\n🚀 SPEEDUP: DuckDB is {speedup:.1f}x faster")
print("   (SQL aggregation is optimized)")

# ============================================================================
# QUERY 3: Complex Multi-Step Analysis
# ============================================================================
print("\n" + "=" * 70)
print("QUERY 3: Top products by region with avg discount")
print("=" * 70)

# Pandas approach
print("\n📊 PANDAS Approach (multiple steps):")
print("-" * 70)
print("""
# Step 1: Filter high-value sales
filtered = df[df['amount'] > 300]

# Step 2: Group and aggregate
agg = filtered.groupby(['region', 'product']).agg({
    'amount': 'sum',
    'quantity': 'count',
    'discount': 'mean'
}).reset_index()

# Step 3: Calculate total
agg['total_with_discount'] = agg['amount'] * (1 - agg['discount'])

# Step 4: Sort and top-n
result = (agg.sort_values('total_with_discount', ascending=False)
          .groupby('region')
          .head(2)
          .reset_index(drop=True))
""")

start = time.time()
filtered = df_pandas[df_pandas['amount'] > 300]
agg = filtered.groupby(['region', 'product']).agg({
    'amount': 'sum',
    'quantity': 'count',
    'discount': 'mean'
}).reset_index()
agg.columns = ['region', 'product', 'total_amount', 'sale_count', 'avg_discount']
agg['total_with_discount'] = agg['total_amount'] * (1 - agg['avg_discount'])
result_pandas = (agg.sort_values('total_with_discount', ascending=False)
                 .groupby('region')
                 .head(2)
                 .reset_index(drop=True))
pandas_time = time.time() - start

print(f"Results:\n{result_pandas.to_string()}")
print(f"Time: {pandas_time*1000:.2f}ms")

# DuckDB approach
print("\n🦆 DUCKDB Approach (single query):")
print("-" * 70)
print("""
result = duckdb.sql(f"
    WITH ranked AS (
        SELECT
            region, product,
            SUM(amount) as total_amount,
            COUNT(*) as sale_count,
            AVG(discount) as avg_discount,
            SUM(amount) * (1 - AVG(discount)) as total_with_discount,
            ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(amount) * (1 - AVG(discount)) DESC) as rank
        FROM read_parquet('{parquet_file}')
        WHERE amount > 300
        GROUP BY region, product
    )
    SELECT * FROM ranked WHERE rank <= 2
    ORDER BY region, rank
").fetchdf()
""")

start = time.time()
result_duckdb = duckdb.sql(f"""
    WITH ranked AS (
        SELECT
            region, product,
            SUM(amount) as total_amount,
            COUNT(*) as sale_count,
            AVG(discount) as avg_discount,
            SUM(amount) * (1 - AVG(discount)) as total_with_discount,
            ROW_NUMBER() OVER (PARTITION BY region ORDER BY SUM(amount) * (1 - AVG(discount)) DESC) as rank
        FROM read_parquet('{parquet_file}')
        WHERE amount > 300
        GROUP BY region, product
    )
    SELECT * FROM ranked WHERE rank <= 2
    ORDER BY region, rank
""").fetchdf()
duckdb_time = time.time() - start

print(f"Results:\n{result_duckdb.to_string()}")
print(f"Time: {duckdb_time*1000:.2f}ms")

speedup = pandas_time / duckdb_time
print(f"\n🚀 SPEEDUP: DuckDB is {speedup:.1f}x faster")
print("   (Complex logic in single query)")

# ============================================================================
# SUMMARY & COMPARISON
# ============================================================================
print("\n" + "=" * 70)
print("SUMMARY: When to Use Each")
print("=" * 70)

print("""
┌─────────────────┬──────────────────────────────────────────────────────┐
│ USE PANDAS WHEN │ - Need to work with data in Python (ML, viz)         │
│                 │ - Small datasets (< 1-2 GB)                          │
│                 │ - Complex Python operations                          │
│                 │ - Working with multiple file formats together        │
├─────────────────┼──────────────────────────────────────────────────────┤
│ USE DUCKDB WHEN │ - Querying Parquet/CSV without loading all data     │
│                 │ - Fast SQL analytics queries                         │
│                 │ - Large files (1-100+ GB)                            │
│                 │ - Simple queries (filtering, grouping, joins)        │
│                 │ - No Python dependency needed                        │
│                 │ - Memory efficiency matters                          │
└─────────────────┴──────────────────────────────────────────────────────┘
""")

print("\n📊 EASE OF USE COMPARISON:")
print("-" * 70)

comparisons = [
    ("Simple filter", "pandas: df[df['x'] > 5]", "duckdb: SELECT * WHERE x > 5"),
    ("Groupby sum", "pandas: df.groupby('x')['y'].sum()", "duckdb: SELECT x, SUM(y) GROUP BY x"),
    ("Join tables", "pandas: pd.merge(df1, df2)", "duckdb: SELECT * FROM t1 JOIN t2"),
    ("Window function", "pandas: df.groupby('x').rank()", "duckdb: ROW_NUMBER() OVER (PARTITION BY x)"),
    ("Complex pipeline", "pandas: 5+ chained operations", "duckdb: Single SQL query with CTEs"),
]

print(f"{'Operation':<20} {'Pandas':<35} {'DuckDB':<35}")
print("-" * 90)
for op, pandas_code, duckdb_code in comparisons:
    print(f"{op:<20} {pandas_code:<35} {duckdb_code:<35}")

print("\n🎯 KEY INSIGHTS:")
print("-" * 70)
print("""
1. ✅ DuckDB is FASTER for analytical queries
   - Doesn't load unused data
   - Optimized query execution
   - Works on files directly

2. ✅ DuckDB is SIMPLER for complex analysis
   - SQL is more readable than chained Pandas
   - Fewer intermediate operations
   - Native window functions, CTEs

3. ✅ DuckDB is MEMORY EFFICIENT
   - Handles files larger than RAM
   - Parquet compression benefits
   - No need to load entire dataset

4. ✅ Pandas is better for:
   - Visualization preparation
   - Machine learning pipelines
   - Mixed data types and sources
   - Python-native operations

5. 🎉 BEST PRACTICE:
   - Use DuckDB to query/filter data
   - Use Pandas for ML/visualization
   - Export DuckDB results to Pandas when needed
""")

# Clean up
os.remove(parquet_file)

print("\n" + "=" * 70)
print("Comparison complete!")
print("=" * 70)
