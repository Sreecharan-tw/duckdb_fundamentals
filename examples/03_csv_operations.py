"""
DuckDB CSV Operations
Example 03 demonstrates reading and writing CSV files.
"""

import duckdb
import os

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB CSV Operations")
print("=" * 60)

# Create sample data and save to CSV
print("\n1. Creating sample CSV file...")
csv_file = '/tmp/sales_data.csv'

# Create sample CSV content
csv_content = """product,quantity,price,date
Laptop,5,1200.00,2024-01-10
Mouse,150,25.00,2024-01-11
Keyboard,80,75.00,2024-01-12
Monitor,30,350.00,2024-01-13
Laptop,3,1200.00,2024-01-14
Mouse,200,25.00,2024-01-15"""

with open(csv_file, 'w') as f:
    f.write(csv_content)

print(f"✓ Sample CSV created at {csv_file}")

# Read CSV file
print("\n2. Reading CSV file...")
result = conn.execute(f"SELECT * FROM read_csv_auto('{csv_file}')").fetchall()
print("Data from CSV:")
for row in result:
    print(f"  {row}")

# Read CSV with specific options
print("\n3. Reading CSV with column renaming...")
result = conn.execute(f"""
    SELECT * FROM read_csv(
        '{csv_file}',
        AUTO_DETECT=true,
        HEADER=true
    )
""").fetchall()
print(f"✓ Read {len(result)} rows")

# Query CSV data directly
print("\n4. Querying CSV data...")
result = conn.execute(f"""
    SELECT
        product,
        SUM(quantity) as total_quantity,
        AVG(price) as avg_price,
        MAX(price) as max_price
    FROM read_csv_auto('{csv_file}')
    GROUP BY product
    ORDER BY total_quantity DESC
""").fetchall()
print("Product Summary:")
for product, qty, avg_p, max_p in result:
    print(f"  {product}: {qty} units, avg price: ${avg_p:.2f}, max price: ${max_p:.2f}")

# Create a table from CSV
print("\n5. Creating table from CSV...")
conn.execute(f"""
    CREATE TABLE sales AS
    SELECT * FROM read_csv_auto('{csv_file}')
""")
print("✓ Table 'sales' created from CSV")

# Verify table
count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
print(f"  Total rows: {count}")

# Write table to CSV
print("\n6. Writing table to CSV...")
output_csv = '/tmp/sales_summary.csv'
conn.execute(f"""
    COPY (
        SELECT
            product,
            SUM(quantity) as total_qty,
            COUNT(*) as num_transactions,
            AVG(price) as avg_price
        FROM sales
        GROUP BY product
    ) TO '{output_csv}' (HEADER true, DELIMITER ',')
""")
print(f"✓ Summary exported to {output_csv}")

# Read and display the exported file
print("\n7. Verifying exported CSV:")
with open(output_csv, 'r') as f:
    for line in f:
        print(f"  {line.strip()}")

# Advanced CSV options
print("\n8. Reading CSV with custom delimiter...")
# Create tab-separated file
tsv_file = '/tmp/data.tsv'
tsv_content = """name\tage\tsalary
Alice\t30\t95000
Bob\t28\t75000
Charlie\t35\t110000"""

with open(tsv_file, 'w') as f:
    f.write(tsv_content)

result = conn.execute(f"""
    SELECT * FROM read_csv(
        '{tsv_file}',
        DELIMITER='\t',
        HEADER=true,
        AUTO_DETECT=true
    )
""").fetchall()
print("Tab-separated data:")
for row in result:
    print(f"  {row}")

# Skip rows
print("\n9. Reading CSV with skipped rows...")
result = conn.execute(f"""
    SELECT * FROM read_csv(
        '{csv_file}',
        SKIP=1,
        HEADER=false
    )
""").fetchall()
print(f"✓ Read CSV skipping first row: {len(result)} rows")

# Reading specific columns
print("\n10. Reading specific columns from CSV...")
result = conn.execute(f"""
    SELECT product, quantity
    FROM read_csv_auto('{csv_file}')
    WHERE quantity > 50
""").fetchall()
print("Products with quantity > 50:")
for product, qty in result:
    print(f"  {product}: {qty}")

# Cleanup
os.remove(csv_file)
os.remove(output_csv)
os.remove(tsv_file)
print("\n✓ Temporary files cleaned up")

print("\n" + "=" * 60)
print("CSV operations complete!")
print("=" * 60)
