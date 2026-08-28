"""
DuckDB Subqueries and Common Table Expressions (CTEs)
Example 09 demonstrates using subqueries and WITH clauses.
"""

import duckdb

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Subqueries and CTEs")
print("=" * 60)

# Create sample data
print("\n1. Creating sample employee and salary data...")
conn.execute("""
    CREATE TABLE employees AS
    SELECT
        row_number() OVER () as emp_id,
        'Employee ' || row_number() OVER () as name,
        CASE
            WHEN row_number() OVER () % 3 = 1 THEN 'Engineering'
            WHEN row_number() OVER () % 3 = 2 THEN 'Sales'
            ELSE 'HR'
        END as department,
        30000 + FLOOR(RANDOM() * 70000) as salary
    FROM range(1, 11)
""")
print("✓ Employees table created")

# Subquery in WHERE clause
print("\n2. Subquery in WHERE clause (employees earning above average)...")
result = conn.execute("""
    SELECT
        name,
        department,
        salary
    FROM employees
    WHERE salary > (SELECT AVG(salary) FROM employees)
    ORDER BY salary DESC
""").fetchall()

print("Employees earning above average:")
for name, dept, salary in result:
    print(f"  {name} ({dept}): ${salary}")

# Subquery in FROM clause
print("\n3. Subquery in FROM clause (department averages)...")
result = conn.execute("""
    SELECT
        dept_avg.department,
        dept_avg.avg_salary,
        COUNT(e.emp_id) as num_employees
    FROM (
        SELECT
            department,
            AVG(salary) as avg_salary
        FROM employees
        GROUP BY department
    ) as dept_avg
    JOIN employees e ON e.department = dept_avg.department
    GROUP BY dept_avg.department, dept_avg.avg_salary
    ORDER BY dept_avg.avg_salary DESC
""").fetchall()

print("Department salary analysis:")
for dept, avg_sal, num_emp in result:
    print(f"  {dept}: avg ${avg_sal:.2f}, {num_emp} employees")

# Correlated subquery
print("\n4. Correlated subquery (compare to department average)...")
result = conn.execute("""
    SELECT
        name,
        department,
        salary,
        (SELECT AVG(salary) FROM employees e2 WHERE e2.department = e.department) as dept_avg,
        salary - (SELECT AVG(salary) FROM employees e2 WHERE e2.department = e.department) as diff_from_avg
    FROM employees e
    ORDER BY department, salary DESC
    LIMIT 5
""").fetchall()

print("Salary comparison to department average:")
print(f"{'Name':<15} {'Dept':<15} {'Salary':>8} {'Dept Avg':>10} {'Difference':>11}")
print("-" * 60)
for name, dept, salary, dept_avg, diff in result:
    print(f"{name:<15} {dept:<15} ${salary:>7} ${dept_avg:>9.0f} {diff:>11.0f}")

# CTE (WITH clause) - Single CTE
print("\n5. Simple CTE (department statistics)...")
result = conn.execute("""
    WITH dept_stats AS (
        SELECT
            department,
            COUNT(*) as num_employees,
            AVG(salary) as avg_salary,
            MIN(salary) as min_salary,
            MAX(salary) as max_salary
        FROM employees
        GROUP BY department
    )
    SELECT
        department,
        num_employees,
        avg_salary,
        min_salary,
        max_salary,
        max_salary - min_salary as salary_range
    FROM dept_stats
    ORDER BY avg_salary DESC
""").fetchall()

print("Department statistics:")
print(f"{'Department':<15} {'Count':>6} {'Avg Salary':>12} {'Min':>8} {'Max':>8} {'Range':>8}")
print("-" * 60)
for dept, count, avg_sal, min_sal, max_sal, sal_range in result:
    print(f"{dept:<15} {count:>6} ${avg_sal:>11.0f} ${min_sal:>7} ${max_sal:>7} ${sal_range:>7}")

# Multiple CTEs
print("\n6. Multiple CTEs (chained calculations)...")
result = conn.execute("""
    WITH salary_ranges AS (
        SELECT
            MIN(salary) as min_salary,
            MAX(salary) as max_salary,
            AVG(salary) as avg_salary
        FROM employees
    ),
    categorized_employees AS (
        SELECT
            name,
            department,
            salary,
            CASE
                WHEN salary < sr.min_salary + (sr.max_salary - sr.min_salary) * 0.33 THEN 'Low'
                WHEN salary < sr.min_salary + (sr.max_salary - sr.min_salary) * 0.67 THEN 'Medium'
                ELSE 'High'
            END as salary_category
        FROM employees, salary_ranges sr
    )
    SELECT
        salary_category,
        COUNT(*) as num_employees,
        AVG(salary) as avg_salary
    FROM categorized_employees
    GROUP BY salary_category
    ORDER BY num_employees DESC
""").fetchall()

print("Salary categories:")
for category, count, avg_sal in result:
    print(f"  {category}: {count} employees, avg: ${avg_sal:.2f}")

# Recursive CTE
print("\n7. Recursive CTE (generate sequence)...")
result = conn.execute("""
    WITH RECURSIVE numbers AS (
        SELECT 1 as n
        UNION ALL
        SELECT n + 1 FROM numbers WHERE n < 5
    )
    SELECT n FROM numbers
""").fetchall()

print("Recursive sequence (1-5):")
for row in result:
    print(f"  {row[0]}")

# CTE with multiple operations
print("\n8. Complex CTE pipeline...")
result = conn.execute("""
    WITH ranked_employees AS (
        SELECT
            name,
            department,
            salary,
            RANK() OVER (PARTITION BY department ORDER BY salary DESC) as dept_rank
        FROM employees
    ),
    top_earners AS (
        SELECT
            department,
            name,
            salary,
            dept_rank
        FROM ranked_employees
        WHERE dept_rank <= 2
    )
    SELECT
        department,
        COUNT(*) as num_top_earners,
        STRING_AGG(name, ', ') as top_earner_names,
        AVG(salary) as avg_top_earner_salary
    FROM top_earners
    GROUP BY department
""").fetchall()

print("Top 2 earners by department:")
for dept, count, names, avg_sal in result:
    print(f"  {dept}:")
    print(f"    Names: {names}")
    print(f"    Avg salary: ${avg_sal:.2f}")

# Subquery in SELECT clause
print("\n9. Subquery in SELECT clause...")
result = conn.execute("""
    SELECT
        name,
        salary,
        (SELECT COUNT(*) FROM employees WHERE salary > e.salary) as higher_paid_count,
        (SELECT COUNT(*) FROM employees WHERE salary <= e.salary) as same_or_lower_paid_count
    FROM employees e
    ORDER BY salary DESC
    LIMIT 5
""").fetchall()

print("Employee salary rankings:")
print(f"{'Name':<15} {'Salary':>8} {'Higher Paid':>12} {'Same or Lower':>13}")
print("-" * 50)
for name, salary, higher_count, same_lower_count in result:
    print(f"{name:<15} ${salary:>7} {higher_count:>12} {same_lower_count:>13}")

# EXISTS operator with subquery
print("\n10. EXISTS operator (departments with high earners)...")
result = conn.execute("""
    SELECT DISTINCT
        department
    FROM employees e
    WHERE EXISTS (
        SELECT 1
        FROM employees e2
        WHERE e2.department = e.department
        AND e2.salary > 60000
    )
    ORDER BY department
""").fetchall()

print("Departments with at least one employee earning >$60,000:")
for row in result:
    print(f"  {row[0]}")

# IN with subquery
print("\n11. IN operator with subquery...")
result = conn.execute("""
    SELECT
        name,
        salary
    FROM employees
    WHERE department IN (
        SELECT department
        FROM employees
        GROUP BY department
        HAVING AVG(salary) > 50000
    )
    ORDER BY salary DESC
""").fetchall()

print("Employees in high-salary departments:")
for name, salary in result:
    print(f"  {name}: ${salary}")

print("\n" + "=" * 60)
print("Subqueries and CTEs complete!")
print("=" * 60)
