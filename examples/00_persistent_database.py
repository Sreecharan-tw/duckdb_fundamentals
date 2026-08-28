"""
DuckDB Persistent Database
Example 00 creates a persistent database file for external connections.

This database can be accessed from:
- DBeaver
- DuckDB CLI
- Python scripts
- Any other DuckDB client

Location: ./duckdb_example.duckdb
"""

import duckdb

# Create or connect to a persistent database file
# (instead of ':memory:' which is in-process only)
db_path = 'duckdb_example.duckdb'
conn = duckdb.connect(db_path)

print("=" * 60)
print("DuckDB Persistent Database Setup")
print("=" * 60)
print(f"\n✓ Database location: {db_path}")
print("\nYou can now connect to this database using:")
print(f"  DBeaver: Use JDBC connection to '{db_path}'")
print(f"  CLI:     duckdb {db_path}")
print(f"  Python:  duckdb.connect('{db_path}')")

# Create sample tables
print("\n1. Creating sample tables...")

conn.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        emp_id INTEGER PRIMARY KEY,
        name VARCHAR,
        department VARCHAR,
        salary DECIMAL(10, 2),
        hire_date DATE
    )
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        dept_id INTEGER PRIMARY KEY,
        dept_name VARCHAR,
        manager_id INTEGER
    )
""")

conn.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        sale_id INTEGER PRIMARY KEY,
        emp_id INTEGER,
        amount DECIMAL(12, 2),
        sale_date DATE
    )
""")

print("✓ Tables created")

# Insert sample data
print("\n2. Inserting sample data...")

conn.execute("""
    INSERT OR IGNORE INTO employees VALUES
    (1, 'Alice Johnson', 'Engineering', 95000.00, DATE '2020-01-15'),
    (2, 'Bob Smith', 'Sales', 75000.00, DATE '2019-06-20'),
    (3, 'Charlie Davis', 'Engineering', 92000.00, DATE '2021-03-10'),
    (4, 'Diana Wilson', 'HR', 68000.00, DATE '2018-11-05'),
    (5, 'Eve Martinez', 'Sales', 78000.00, DATE '2021-08-22')
""")

conn.execute("""
    INSERT OR IGNORE INTO departments VALUES
    (1, 'Engineering', 1),
    (2, 'Sales', 2),
    (3, 'HR', 4)
""")

conn.execute("""
    INSERT OR IGNORE INTO sales VALUES
    (101, 2, 25000.00, DATE '2024-01-15'),
    (102, 2, 18500.00, DATE '2024-01-16'),
    (103, 5, 22000.00, DATE '2024-01-17'),
    (104, 5, 19500.00, DATE '2024-01-18'),
    (105, 2, 21000.00, DATE '2024-01-19')
""")

print("✓ Sample data inserted")

# Display summary
print("\n3. Database Contents:")

result = conn.execute("SELECT COUNT(*) FROM employees").fetchone()
print(f"  Employees: {result[0]} records")

result = conn.execute("SELECT COUNT(*) FROM departments").fetchone()
print(f"  Departments: {result[0]} records")

result = conn.execute("SELECT COUNT(*) FROM sales").fetchone()
print(f"  Sales: {result[0]} records")

# Sample query
print("\n4. Sample Query - Employees by Department:")
result = conn.execute("""
    SELECT
        department,
        COUNT(*) as emp_count,
        AVG(salary) as avg_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
""").fetchall()

for dept, count, avg_sal in result:
    print(f"  {dept}: {count} employees, avg salary: ${avg_sal:,.2f}")

print("\n" + "=" * 60)
print("Database ready for external connections!")
print("=" * 60)
print(f"\nNext steps:")
print(f"  1. DBeaver: New Connection → DuckDB → File: {db_path}")
print(f"  2. CLI:     duckdb {db_path}")
print(f"  3. Python:  duckdb.connect('{db_path}')")
print("\n")
