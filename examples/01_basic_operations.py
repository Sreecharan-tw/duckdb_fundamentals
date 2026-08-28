"""
DuckDB Basics: CREATE, INSERT, SELECT, DELETE
Example 01 demonstrates fundamental database operations.
"""

import duckdb

# Create an in-memory database connection
conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Fundamentals: Basic Operations")
print("=" * 60)

# CREATE TABLE
print("\n1. Creating a table...")
conn.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        department VARCHAR,
        salary DECIMAL(10, 2),
        hire_date DATE
    )
""")
print("✓ Table 'employees' created")

# INSERT data
print("\n2. Inserting data...")
conn.execute("""
    INSERT INTO employees VALUES
    (1, 'Alice Johnson', 'Engineering', 95000.00, '2020-01-15'),
    (2, 'Bob Smith', 'Sales', 75000.00, '2019-06-20'),
    (3, 'Charlie Davis', 'Engineering', 92000.00, '2021-03-10'),
    (4, 'Diana Wilson', 'HR', 68000.00, '2018-11-05'),
    (5, 'Eve Martinez', 'Sales', 78000.00, '2021-08-22')
""")
print("✓ 5 rows inserted")

# SELECT all data
print("\n3. Selecting all data...")
result = conn.execute("SELECT * FROM employees").fetchall()
for row in result:
    print(row)

# SELECT with WHERE clause
print("\n4. Filtering data (Engineering department)...")
result = conn.execute(
    "SELECT name, salary FROM employees WHERE department = 'Engineering'"
).fetchall()
for row in result:
    print(f"  {row[0]}: ${row[1]}")

# UPDATE
print("\n5. Updating salary...")
conn.execute("UPDATE employees SET salary = 100000.00 WHERE name = 'Alice Johnson'")
print("✓ Alice's salary updated to $100,000")

# SELECT after update
result = conn.execute("SELECT name, salary FROM employees WHERE name = 'Alice Johnson'").fetchone()
print(f"  Verification: {result[0]} now earns ${result[1]}")

# DELETE
print("\n6. Deleting a record...")
conn.execute("DELETE FROM employees WHERE name = 'Eve Martinez'")
print("✓ Eve Martinez's record deleted")

# COUNT remaining records
count = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
print(f"  Remaining employees: {count}")

# ORDER BY and LIMIT
print("\n7. Top 3 highest-paid employees...")
result = conn.execute(
    "SELECT name, salary FROM employees ORDER BY salary DESC LIMIT 3"
).fetchall()
for name, salary in result:
    print(f"  {name}: ${salary}")

# ALTER TABLE
print("\n8. Adding a new column...")
conn.execute("ALTER TABLE employees ADD COLUMN bonus DECIMAL(10, 2) DEFAULT 0.00")
print("✓ Column 'bonus' added")

# DROP TABLE
print("\n9. Dropping the table...")
conn.execute("DROP TABLE employees")
print("✓ Table 'employees' dropped")

# Verify table no longer exists
try:
    conn.execute("SELECT * FROM employees")
except Exception as e:
    print(f"  Expected error: {type(e).__name__}")

print("\n" + "=" * 60)
print("Basic operations complete!")
print("=" * 60)
