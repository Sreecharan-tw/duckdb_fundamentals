"""
DuckDB Parquet Operations
Example 04 demonstrates reading and writing Parquet files.
"""

import duckdb
import os

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Parquet Operations")
print("=" * 60)

# Create sample data table
print("\n1. Creating sample data...")
conn.execute("""
    CREATE TABLE products AS
    SELECT
        row_number() OVER () as id,
        CASE
            WHEN row_number() OVER () % 3 = 1 THEN 'Electronics'
            WHEN row_number() OVER () % 3 = 2 THEN 'Furniture'
            ELSE 'Books'
        END as category,
        'Product ' || row_number() OVER () as name,
        FLOOR(RANDOM() * 1000 + 100)::DECIMAL(10, 2) as price,
        FLOOR(RANDOM() * 100 + 1)::INTEGER as stock
    FROM (SELECT * FROM range(1, 11)) AS t(i)
""")

result = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
print(f"✓ Created products table with {result} rows")

# Display sample data
print("\n2. Sample data:")
result = conn.execute("SELECT * FROM products LIMIT 3").fetchall()
for row in result:
    print(f"  {row}")

# Write table to Parquet
print("\n3. Writing table to Parquet...")
parquet_file = '/tmp/products.parquet'
conn.execute(f"COPY products TO '{parquet_file}' (FORMAT PARQUET)")
print(f"✓ Data written to {parquet_file}")

# Check file size
file_size = os.path.getsize(parquet_file)
print(f"  File size: {file_size} bytes")

# Read Parquet file
print("\n4. Reading Parquet file...")
result = conn.execute(f"SELECT * FROM read_parquet('{parquet_file}')").fetchall()
print(f"✓ Read {len(result)} rows from Parquet file")

# Query Parquet file directly
print("\n5. Querying Parquet file...")
result = conn.execute(f"""
    SELECT
        category,
        COUNT(*) as num_products,
        AVG(price) as avg_price,
        SUM(stock) as total_stock
    FROM read_parquet('{parquet_file}')
    GROUP BY category
    ORDER BY avg_price DESC
""").fetchall()
print("Category Summary:")
for category, count, avg_p, total_s in result:
    print(f"  {category}: {count} products, avg price: ${avg_p:.2f}, stock: {total_s}")

# Write filtered data to Parquet
print("\n6. Writing filtered data to Parquet...")
expensive_parquet = '/tmp/expensive_products.parquet'
conn.execute(f"""
    COPY (
        SELECT * FROM read_parquet('{parquet_file}')
        WHERE price > 500
    ) TO '{expensive_parquet}' (FORMAT PARQUET)
""")
print(f"✓ Expensive products written to {expensive_parquet}")

result = conn.execute(f"SELECT COUNT(*) FROM read_parquet('{expensive_parquet}')").fetchone()[0]
print(f"  Expensive products: {result}")

# Read multiple Parquet files (glob pattern)
print("\n7. Reading with glob pattern...")
result = conn.execute(f"""
    SELECT COUNT(*) as total_rows
    FROM read_parquet('/tmp/*.parquet')
""").fetchone()[0]
print(f"✓ Total rows from all parquet files: {result}")

# Parquet with specific columns
print("\n8. Reading specific columns from Parquet...")
result = conn.execute(f"""
    SELECT id, name, price
    FROM read_parquet('{parquet_file}')
    WHERE price > 300
    ORDER BY price DESC
    LIMIT 5
""").fetchall()
print("Top 5 products by price (>$300):")
for row_id, name, price in result:
    print(f"  {name}: ${price:.2f}")

# Parquet metadata
print("\n9. Parquet file information...")
result = conn.execute(f"""
    SELECT * FROM parquet_scan('{parquet_file}')
    LIMIT 0
""")
print(f"✓ Parquet schema retrieved")

# Create partitioned output (simulated)
print("\n10. Writing with compression...")
compressed_parquet = '/tmp/products_compressed.parquet'
conn.execute(f"""
    COPY (SELECT * FROM products)
    TO '{compressed_parquet}'
    (FORMAT PARQUET, COMPRESSION 'SNAPPY')
""")
print(f"✓ Compressed Parquet created")

compressed_size = os.path.getsize(compressed_parquet)
original_size = os.path.getsize(parquet_file)
compression_ratio = (1 - compressed_size / original_size) * 100
print(f"  Compression ratio: {compression_ratio:.1f}%")

# Cleanup
print("\n11. Cleaning up...")
for f in [parquet_file, expensive_parquet, compressed_parquet]:
    if os.path.exists(f):
        os.remove(f)
print("✓ Temporary Parquet files removed")

print("\n" + "=" * 60)
print("Parquet operations complete!")
print("=" * 60)
