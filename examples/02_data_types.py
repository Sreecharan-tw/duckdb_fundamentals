"""
DuckDB Data Types
Example 02 demonstrates working with different data types.
"""

import duckdb
from datetime import datetime, date, timedelta

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Data Types")
print("=" * 60)

# Create table with various data types
print("\n1. Creating table with multiple data types...")
conn.execute("""
    CREATE TABLE data_types_demo (
        id INTEGER,
        name VARCHAR,
        age SMALLINT,
        salary DECIMAL(12, 2),
        hire_date DATE,
        last_login TIMESTAMP,
        is_active BOOLEAN,
        tags LIST(VARCHAR),
        metadata STRUCT(department VARCHAR, level VARCHAR)
    )
""")
print("✓ Table created with various data types")

# Insert data
print("\n2. Inserting data with different types...")
conn.execute("""
    INSERT INTO data_types_demo VALUES
    (
        1,
        'Alice',
        30,
        95000.50,
        DATE '2020-01-15',
        TIMESTAMP '2024-08-28 14:30:00',
        true,
        ['python', 'sql', 'analytics'],
        {'department': 'Engineering', 'level': 'Senior'}
    ),
    (
        2,
        'Bob',
        28,
        75000.00,
        DATE '2019-06-20',
        TIMESTAMP '2024-08-27 09:15:00',
        true,
        ['sales', 'negotiation'],
        {'department': 'Sales', 'level': 'Mid-level'}
    )
""")
print("✓ Data inserted")

# Numeric types
print("\n3. Numeric Types:")
result = conn.execute(
    "SELECT id, age, salary FROM data_types_demo WHERE id = 1"
).fetchone()
print(f"  ID (INTEGER): {result[0]} (type: {type(result[0]).__name__})")
print(f"  Age (SMALLINT): {result[1]} (type: {type(result[1]).__name__})")
print(f"  Salary (DECIMAL): {result[2]} (type: {type(result[2]).__name__})")

# String types
print("\n4. String Types:")
result = conn.execute("SELECT name FROM data_types_demo WHERE id = 1").fetchone()
print(f"  Name (VARCHAR): '{result[0]}' (length: {len(result[0])})")

# Boolean type
print("\n5. Boolean Type:")
result = conn.execute(
    "SELECT name, is_active FROM data_types_demo WHERE id = 1"
).fetchone()
print(f"  {result[0]} is_active: {result[1]}")

active_count = conn.execute("SELECT COUNT(*) FROM data_types_demo WHERE is_active = true").fetchone()[0]
print(f"  Active employees: {active_count}")

# Date and Timestamp types
print("\n6. Date and Timestamp Types:")
result = conn.execute(
    "SELECT hire_date, last_login FROM data_types_demo WHERE id = 1"
).fetchone()
print(f"  Hire Date (DATE): {result[0]}")
print(f"  Last Login (TIMESTAMP): {result[1]}")

# Date arithmetic
print("\n7. Date Arithmetic:")
result = conn.execute("""
    SELECT
        name,
        hire_date,
        CURRENT_DATE - hire_date as days_employed,
        DATE_TRUNC('month', hire_date) as hire_month
    FROM data_types_demo
""").fetchall()
for row in result:
    print(f"  {row[0]}: {row[2]} days employed, hired in {row[3]}")

# List type
print("\n8. List Type:")
result = conn.execute(
    "SELECT name, tags FROM data_types_demo WHERE id = 1"
).fetchone()
print(f"  {result[0]}'s tags: {result[1]}")

# List functions
print("\n9. List Functions:")
result = conn.execute("""
    SELECT
        name,
        list_length(tags) as num_tags,
        list_contains(tags, 'python') as knows_python
    FROM data_types_demo
""").fetchall()
for row in result:
    print(f"  {row[0]}: {row[1]} tags, knows Python: {row[2]}")

# Struct type
print("\n10. Struct Type (accessing nested fields):")
result = conn.execute("""
    SELECT
        name,
        metadata.department,
        metadata.level
    FROM data_types_demo
""").fetchall()
for row in result:
    print(f"  {row[0]}: {row[1]}, {row[2]}")

# Type casting
print("\n11. Type Casting:")
result = conn.execute("""
    SELECT
        id,
        CAST(id AS VARCHAR) as id_as_text,
        CAST('123' AS INTEGER) as text_to_int,
        CAST(salary AS INTEGER) as salary_rounded
    FROM data_types_demo
    LIMIT 1
""").fetchone()
print(f"  ID (original): {result[0]}")
print(f"  ID (as text): '{result[1]}'")
print(f"  Text to int: {result[2]}")
print(f"  Salary (rounded): {result[3]}")

# NULL handling
print("\n12. NULL Handling:")
conn.execute("INSERT INTO data_types_demo (id, name) VALUES (3, 'Charlie')")
result = conn.execute("""
    SELECT
        id,
        name,
        age,
        COALESCE(age, 0) as age_with_default
    FROM data_types_demo
    WHERE id = 3
""").fetchone()
print(f"  ID: {result[0]}, Name: {result[1]}, Age (NULL): {result[2]}, Age (coalesced): {result[3]}")

print("\n" + "=" * 60)
print("Data types exploration complete!")
print("=" * 60)
