# DuckDB Connection Guide

## Overview

The `00_persistent_database.py` example creates a persistent DuckDB database file that can be accessed from external tools.

## Option 1: DBeaver Connection

### Prerequisites
- DBeaver installed (Community or Professional Edition)
- DuckDB JDBC driver

### Steps

1. **Create Database File**
   ```bash
   make run-00
   ```
   This creates `duckdb_example.duckdb` in the project root.

2. **Open DBeaver**

3. **Create New Connection**
   - Go to: `Database` → `New Database Connection`
   - Search for and select: **DuckDB**
   - Click **Next**

4. **Configure Connection Settings**
   - **Connection Name:** `DuckDB Examples`
   - **Database File:** Click browse and select `duckdb_example.duckdb`
   - **Path:** (should auto-populate)
   - Click **Test Connection** to verify

5. **Finish**
   - The connection appears in the Database Navigator
   - Expand it to see tables: `employees`, `departments`, `sales`

6. **Run Queries**
   - Right-click connection → `SQL Editor` → `Open SQL Script`
   - Try:
   ```sql
   SELECT * FROM employees;
   SELECT department, COUNT(*) as emp_count FROM employees GROUP BY department;
   SELECT * FROM sales WHERE amount > 20000;
   ```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| "DuckDB driver not found" | DBeaver will auto-download on first use |
| "Cannot open database file" | Ensure file path is correct, check file permissions |
| "Database is locked" | Close the database in other applications or CLI |

---

## Option 2: DuckDB CLI

### Simple Usage

```bash
# Open the database
duckdb duckdb_example.duckdb

# In the DuckDB CLI:
duckdb> SELECT * FROM employees;
duckdb> SELECT * FROM departments;
duckdb> SELECT * FROM sales;

# Exit
duckdb> .exit
```

### Common CLI Commands

```bash
# List all tables
duckdb duckdb_example.duckdb -c "SELECT * FROM information_schema.tables;"

# Run a query and export
duckdb duckdb_example.duckdb -c "SELECT * FROM employees;" > employees.csv

# Run a query file
duckdb duckdb_example.duckdb < query.sql

# Interactive mode with verbose output
duckdb duckdb_example.duckdb -echo
```

### Example Queries

```sql
-- Employees by department
SELECT department, COUNT(*) as count, AVG(salary) as avg_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;

-- Sales performance
SELECT e.name, COUNT(*) as sales_count, SUM(s.amount) as total_sales
FROM sales s
JOIN employees e ON s.emp_id = e.emp_id
GROUP BY e.name
ORDER BY total_sales DESC;

-- High earners
SELECT name, department, salary
FROM employees
WHERE salary > 75000
ORDER BY salary DESC;
```

---

## Option 3: Python Connection

Access the same database from Python:

```python
import duckdb

# Connect to persistent database
conn = duckdb.connect('duckdb_example.duckdb')

# Query data
result = conn.execute("SELECT * FROM employees").fetchall()
print(result)

# Close connection
conn.close()
```

---

## Option 4: Programmatic Updates

Modify the data from Python while keeping it in the persistent database:

```python
import duckdb

conn = duckdb.connect('duckdb_example.duckdb')

# Insert new data
conn.execute("""
    INSERT INTO employees VALUES
    (6, 'Frank Chen', 'Engineering', 88000.00, DATE '2024-01-01')
""")

# Query updated data
result = conn.execute("SELECT * FROM employees WHERE emp_id = 6").fetchone()
print(result)

conn.close()
```

---

## Database Schema

### employees
```
emp_id: INTEGER (Primary Key)
name: VARCHAR
department: VARCHAR
salary: DECIMAL(10, 2)
hire_date: DATE
```

### departments
```
dept_id: INTEGER (Primary Key)
dept_name: VARCHAR
manager_id: INTEGER
```

### sales
```
sale_id: INTEGER (Primary Key)
emp_id: INTEGER (FK to employees)
amount: DECIMAL(12, 2)
sale_date: DATE
```

---

## Creating Your Own Persistent Database

Modify `examples/00_persistent_database.py` to:
- Change `db_path` variable
- Add/modify table schemas
- Insert your own data

Example:
```python
db_path = 'my_data.duckdb'
conn = duckdb.connect(db_path)

conn.execute("""
    CREATE TABLE my_table (
        id INTEGER,
        name VARCHAR,
        value DOUBLE
    )
""")

conn.execute("""
    INSERT INTO my_table VALUES
    (1, 'Example', 123.45)
""")
```

---

## Performance Tips

1. **Indexes** - DuckDB automatically optimizes queries
2. **File Location** - Keep `.duckdb` file on fast storage (SSD)
3. **Concurrent Access** - DuckDB supports multiple read connections, one write
4. **Backup** - Simply copy the `.duckdb` file

---

## Useful Commands

```bash
# Show all tables and their schemas
duckdb duckdb_example.duckdb -c "SELECT * FROM information_schema.columns;"

# Export as CSV
duckdb duckdb_example.duckdb -c "COPY employees TO 'employees.csv' WITH (FORMAT csv, HEADER true);"

# Import from CSV
duckdb duckdb_example.duckdb -c "COPY imported_data FROM 'data.csv';"

# Get database statistics
duckdb duckdb_example.duckdb -c "SELECT * FROM pragma_database_size();"
```

---

## Next Steps

- Run `make run-00` to create/refresh the database
- Connect with DBeaver for visual exploration
- Use CLI for quick queries
- Modify Python scripts to add your data
