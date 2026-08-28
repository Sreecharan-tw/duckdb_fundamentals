"""
DuckDB Pandas Integration
Example 05 demonstrates seamless integration between DuckDB and Pandas.
"""

import duckdb
import pandas as pd
import numpy as np

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Pandas Integration")
print("=" * 60)

# Create Pandas DataFrame
print("\n1. Creating Pandas DataFrame...")
df = pd.DataFrame({
    'employee_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
    'department': ['Engineering', 'Sales', 'Engineering', 'HR', 'Sales'],
    'salary': [95000, 75000, 92000, 68000, 78000],
    'years_employed': [4, 5, 3, 6, 2]
})

print("Original DataFrame:")
print(df)

# Query Pandas DataFrame directly
print("\n2. Querying Pandas DataFrame directly...")
result = conn.execute("SELECT * FROM df WHERE salary > 80000").fetchdf()
print("Employees earning more than $80,000:")
print(result)

# Create DuckDB table from DataFrame
print("\n3. Creating DuckDB table from DataFrame...")
conn.execute("CREATE TABLE employees AS SELECT * FROM df")
print("✓ Table 'employees' created from DataFrame")

# Query the table
result = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
print(f"  Total employees: {result}")

# Aggregate operations
print("\n4. Aggregations by department...")
result = conn.execute("""
    SELECT
        department,
        COUNT(*) as num_employees,
        AVG(salary) as avg_salary,
        MIN(salary) as min_salary,
        MAX(salary) as max_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
""").fetchdf()
print(result)

# Convert result to Pandas
print("\n5. Converting query result to DataFrame...")
salary_df = conn.execute("""
    SELECT
        name,
        salary,
        salary * 0.1 as bonus_10_percent,
        salary * 0.15 as bonus_15_percent
    FROM employees
    ORDER BY salary DESC
""").fetchdf()
print("Salary with bonus calculations:")
print(salary_df)

# Modify DataFrame and insert back
print("\n6. Modifying DataFrame and inserting back...")
salary_df['bonus_given'] = salary_df['bonus_10_percent']
salary_df = salary_df[['name', 'salary', 'bonus_given']]

conn.execute("CREATE TABLE salary_bonuses AS SELECT * FROM salary_df")
result = conn.execute("SELECT * FROM salary_bonuses").fetchdf()
print("Bonus table:")
print(result)

# Join operations with DataFrame
print("\n7. Multi-step analysis with Pandas integration...")

# Step 1: Get employee stats from DuckDB
employee_stats = conn.execute("""
    SELECT
        name,
        department,
        salary,
        years_employed,
        salary / NULLIF(years_employed, 0) as salary_per_year
    FROM employees
""").fetchdf()

# Step 2: Add new columns in Pandas
employee_stats['salary_rank'] = employee_stats['salary'].rank(ascending=False)
employee_stats['is_senior'] = employee_stats['years_employed'] >= 4

# Step 3: Put back in DuckDB for final aggregation
conn.execute("CREATE TABLE enhanced_employees AS SELECT * FROM employee_stats")

result = conn.execute("""
    SELECT
        is_senior,
        COUNT(*) as num_employees,
        AVG(salary) as avg_salary
    FROM enhanced_employees
    GROUP BY is_senior
""").fetchdf()
print("Comparison of Senior vs Junior employees:")
print(result)

# Use Pandas operations on DuckDB results
print("\n8. Statistical analysis...")
stats_df = conn.execute("""
    SELECT
        salary,
        years_employed
    FROM employees
""").fetchdf()

print("Salary statistics:")
print(stats_df['salary'].describe())

print("\nCorrelation between salary and years employed:")
correlation = stats_df[['salary', 'years_employed']].corr()
print(correlation)

# Create new data and write back to DuckDB
print("\n9. Creating synthetic data with Pandas...")
new_employees = pd.DataFrame({
    'employee_id': [6, 7, 8],
    'name': ['Frank', 'Grace', 'Henry'],
    'department': ['Engineering', 'Marketing', 'HR'],
    'salary': [88000, 70000, 72000],
    'years_employed': [2, 1, 3]
})

conn.execute("INSERT INTO employees SELECT * FROM new_employees")
total = conn.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
print(f"✓ Added 3 employees, total: {total}")

# Batch operations
print("\n10. Batch operations...")
salaries = conn.execute("""
    SELECT name, salary FROM employees ORDER BY salary DESC
""").fetchdf()

# Apply Pandas operations
salaries['percentile_rank'] = salaries['salary'].rank(pct=True) * 100
salaries['salary_bracket'] = pd.cut(salaries['salary'], bins=3, labels=['Low', 'Medium', 'High'])

print("Salary brackets:")
print(salaries[['name', 'salary', 'salary_bracket', 'percentile_rank']])

print("\n" + "=" * 60)
print("Pandas integration complete!")
print("=" * 60)
