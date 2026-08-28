"""
DuckDB Performance Tips and Optimization Techniques
Example 13 demonstrates query optimization and performance best practices.
"""

import duckdb
import time

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Performance Tips and Optimization")
print("=" * 60)

# Create large dataset
print("\n1. Creating test dataset...")
conn.execute("""
    CREATE TABLE sales_large AS
    SELECT
        row_number() OVER () as sale_id,
        CASE
            WHEN row_number() OVER () % 5 = 1 THEN 'Electronics'
            WHEN row_number() OVER () % 5 = 2 THEN 'Clothing'
            WHEN row_number() OVER () % 5 = 3 THEN 'Home'
            WHEN row_number() OVER () % 5 = 4 THEN 'Sports'
            ELSE 'Books'
        END as category,
        DATE '2024-01-01' + INTERVAL 1 day * (row_number() OVER () % 365) as sale_date,
        10 + FLOOR(RANDOM() * 990) as amount,
        1 + FLOOR(RANDOM() * 100) as quantity
    FROM range(1, 100001)
""")
print("✓ Created sales_large with 100,000 rows")

# Tip 1: Use column selection instead of SELECT *
print("\n2. Tip 1: Select only needed columns...")
start = time.time()
result = conn.execute("""
    SELECT sale_id, amount
    FROM sales_large
    LIMIT 1000
""").fetchall()
elapsed_selective = time.time() - start

start = time.time()
result = conn.execute("""
    SELECT *
    FROM sales_large
    LIMIT 1000
""").fetchall()
elapsed_all = time.time() - start

print(f"  Column selection: {elapsed_selective*1000:.2f}ms")
print(f"  SELECT *: {elapsed_all*1000:.2f}ms")
print(f"  ✓ Selecting only needed columns is {(elapsed_all/elapsed_selective):.1f}x faster")

# Tip 2: Filter early with WHERE clause
print("\n3. Tip 2: Push filters down (WHERE before JOIN)...")
print("  ✓ DuckDB optimizer automatically pushes filters down the query plan")
print("  ✓ Always write WHERE conditions in the base tables when possible")

result = conn.execute("""
    SELECT category, COUNT(*) as count
    FROM sales_large
    WHERE amount > 500
    GROUP BY category
""").fetchall()
print(f"  Found {sum(c[1] for c in result)} sales > $500")

# Tip 3: Use appropriate data types
print("\n4. Tip 3: Use appropriate data types...")
print("  ✓ Use INTEGER instead of VARCHAR for numeric data")
print("  ✓ Use DATE instead of VARCHAR for dates")
print("  ✓ Use DECIMAL for monetary values")

result = conn.execute("""
    SELECT
        sale_date,
        CAST(amount AS INTEGER) as amount_int,
        CAST(amount AS DECIMAL) as amount_decimal
    FROM sales_large
    LIMIT 3
""").fetchall()
for sale_date, amt_int, amt_dec in result:
    print(f"  Date: {sale_date}, Int: {amt_int}, Decimal: {amt_dec}")

# Tip 4: Aggregation optimization
print("\n5. Tip 4: Aggregation techniques...")
print("  ✓ GROUP BY is fast in DuckDB's columnar engine")

start = time.time()
result = conn.execute("""
    SELECT
        category,
        COUNT(*) as num_sales,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount
    FROM sales_large
    GROUP BY category
""").fetchall()
elapsed = time.time() - start

print(f"  Aggregation of 100k rows: {elapsed*1000:.2f}ms")
for category, num_sales, total_amt, avg_amt in result:
    print(f"    {category}: {num_sales} sales, ${total_amt:.0f} total, ${avg_amt:.2f} avg")

# Tip 5: Use HAVING for group filtering
print("\n6. Tip 5: HAVING clause for group filtering...")
print("  ✓ Use HAVING to filter aggregated results")

result = conn.execute("""
    SELECT
        category,
        COUNT(*) as num_sales,
        SUM(amount) as total_amount
    FROM sales_large
    GROUP BY category
    HAVING SUM(amount) > 4000000
""").fetchall()

print(f"  Categories with sales > $4M: {len(result)}")
for category, num_sales, total_amt in result:
    print(f"    {category}: ${total_amt:,.0f}")

# Tip 6: Join optimization
print("\n7. Tip 6: Join optimization...")
print("  ✓ DuckDB optimizes join order automatically")
print("  ✓ Join smaller tables first when possible")

conn.execute("""
    CREATE TABLE categories AS
    SELECT DISTINCT category FROM sales_large
""")

start = time.time()
result = conn.execute("""
    SELECT
        c.category,
        COUNT(*) as count
    FROM categories c
    LEFT JOIN sales_large s ON c.category = s.category
    GROUP BY c.category
""").fetchall()
elapsed = time.time() - start

print(f"  Join performance: {elapsed*1000:.2f}ms")

# Tip 7: Limit for exploratory queries
print("\n8. Tip 7: Use LIMIT for exploration...")
print("  ✓ Always use LIMIT when exploring large datasets")

result = conn.execute("""
    SELECT * FROM sales_large LIMIT 10
""").fetchall()
print(f"  Retrieved 10 rows (not all 100,000)")

# Tip 8: Index equivalent operations
print("\n9. Tip 8: DuckDB handles sorting efficiently...")
start = time.time()
result = conn.execute("""
    SELECT * FROM sales_large
    ORDER BY amount DESC
    LIMIT 10
""").fetchall()
elapsed = time.time() - start

print(f"  Top 10 by amount: {elapsed*1000:.2f}ms (does not need index)")

# Tip 9: Caching with views
print("\n10. Tip 9: Use temporary tables/views for reuse...")
conn.execute("""
    CREATE TEMP TABLE category_summary AS
    SELECT
        category,
        COUNT(*) as num_sales,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount
    FROM sales_large
    GROUP BY category
""")

start = time.time()
result = conn.execute("""
    SELECT * FROM category_summary
    WHERE total_amount > 3000000
""").fetchall()
elapsed = time.time() - start

print(f"  Query on materialized view: {elapsed*1000:.2f}ms")

# Tip 10: Avoid subqueries where possible
print("\n11. Tip 10: Prefer JOIN over subqueries...")
print("  ✓ CTEs and JOINs are often more efficient than subqueries")

# Subquery approach
start = time.time()
result = conn.execute("""
    SELECT COUNT(*) FROM sales_large
    WHERE category IN (
        SELECT category FROM sales_large
        WHERE amount > 700
        GROUP BY category
        HAVING COUNT(*) > 100
    )
""").fetchone()
elapsed_subquery = time.time() - start

print(f"  Subquery approach: {elapsed_subquery*1000:.2f}ms")

# CTE approach
start = time.time()
result = conn.execute("""
    WITH high_value_cats AS (
        SELECT category
        FROM sales_large
        WHERE amount > 700
        GROUP BY category
        HAVING COUNT(*) > 100
    )
    SELECT COUNT(*) FROM sales_large s
    JOIN high_value_cats h ON s.category = h.category
""").fetchone()
elapsed_join = time.time() - start

print(f"  JOIN/CTE approach: {elapsed_join*1000:.2f}ms")

# Tip 11: Vectorized operations
print("\n12. Tip 11: DuckDB is vectorized...")
print("  ✓ DuckDB processes data in chunks (vectors)")
print("  ✓ Operations on multiple rows at once are faster")

result = conn.execute("""
    SELECT
        SUM(quantity) as total_qty,
        AVG(quantity) as avg_qty,
        MAX(quantity) as max_qty
    FROM sales_large
""").fetchone()

print(f"  Vectorized aggregations:")
print(f"    Total: {result[0]}, Average: {result[1]:.2f}, Max: {result[2]}")

# Tip 12: Use appropriate LIMIT
print("\n13. Tip 12: LIMIT pushdown...")
print("  ✓ DuckDB pushes LIMIT down the query plan")
print("  ✓ No need to select all rows when you only want top N")

start = time.time()
result = conn.execute("""
    SELECT * FROM sales_large
    ORDER BY amount DESC
    LIMIT 100
""").fetchall()
elapsed = time.time() - start

print(f"  Getting top 100: {elapsed*1000:.2f}ms")

print("\n" + "=" * 60)
print("Performance Tips Summary")
print("=" * 60)
print("""
1. Select only needed columns (avoid SELECT *)
2. Filter early with WHERE clauses
3. Use appropriate data types
4. DuckDB aggregations are fast (GROUP BY)
5. Use HAVING for post-aggregation filtering
6. Let DuckDB optimize joins automatically
7. Use LIMIT for exploratory queries
8. Sorting is efficient in DuckDB
9. Use temporary tables for multi-use results
10. Prefer CTEs and JOINs over subqueries
11. DuckDB is vectorized - batch operations are fast
12. LIMIT is pushed down efficiently
13. For small datasets, simplicity > optimization
""")
print("=" * 60)
