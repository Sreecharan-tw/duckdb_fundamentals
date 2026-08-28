"""
DuckDB Join Operations
Example 07 demonstrates different types of joins.
"""

import duckdb

conn = duckdb.connect(':memory:')

print("=" * 60)
print("DuckDB Join Operations")
print("=" * 60)

# Create sample tables
print("\n1. Creating sample tables...")

# Create customers table
conn.execute("""
    CREATE TABLE customers (
        customer_id INTEGER PRIMARY KEY,
        name VARCHAR,
        city VARCHAR,
        country VARCHAR
    )
""")

# Create orders table
conn.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date DATE,
        total_amount DECIMAL(10, 2)
    )
""")

# Insert customer data
conn.execute("""
    INSERT INTO customers VALUES
    (1, 'Alice Johnson', 'New York', 'USA'),
    (2, 'Bob Smith', 'London', 'UK'),
    (3, 'Charlie Davis', 'Tokyo', 'Japan'),
    (4, 'Diana Wilson', 'Toronto', 'Canada'),
    (5, 'Eve Martinez', 'Madrid', 'Spain')
""")

# Insert order data (note: customer 5 has no orders, customer 1 has multiple)
conn.execute("""
    INSERT INTO orders VALUES
    (101, 1, DATE '2024-01-15', 250.00),
    (102, 2, DATE '2024-01-16', 180.00),
    (103, 1, DATE '2024-01-17', 420.00),
    (104, 3, DATE '2024-01-18', 95.00),
    (105, 1, DATE '2024-01-19', 310.00),
    (106, 4, DATE '2024-01-20', 150.00),
    (107, 2, DATE '2024-01-21', 275.00)
""")

print("✓ Created customers and orders tables")

# INNER JOIN
print("\n2. INNER JOIN (customers with orders)...")
result = conn.execute("""
    SELECT
        c.customer_id,
        c.name,
        c.city,
        o.order_id,
        o.total_amount
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    ORDER BY c.customer_id, o.order_id
""").fetchall()

print("Customers with orders:")
print(f"{'ID':<4} {'Name':<15} {'City':<10} {'Order':<7} {'Amount':>8}")
print("-" * 50)
for cust_id, name, city, order_id, amount in result:
    print(f"{cust_id:<4} {name:<15} {city:<10} {order_id:<7} ${amount:>7.2f}")

# LEFT JOIN
print("\n3. LEFT JOIN (all customers, with orders if they have any)...")
result = conn.execute("""
    SELECT
        c.customer_id,
        c.name,
        COUNT(o.order_id) as num_orders,
        COALESCE(SUM(o.total_amount), 0) as total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
    ORDER BY total_spent DESC
""").fetchall()

print("Customer spending summary:")
print(f"{'ID':<4} {'Name':<15} {'Orders':>7} {'Total Spent':>12}")
print("-" * 42)
for cust_id, name, num_orders, total_spent in result:
    print(f"{cust_id:<4} {name:<15} {num_orders:>7} ${total_spent:>11.2f}")

# RIGHT JOIN
print("\n4. RIGHT JOIN (all orders, with customer details)...")
result = conn.execute("""
    SELECT
        o.order_id,
        c.name,
        c.city,
        o.order_date,
        o.total_amount
    FROM customers c
    RIGHT JOIN orders o ON c.customer_id = o.customer_id
    ORDER BY o.order_id
""").fetchall()

print("All orders with customer info:")
for order_id, name, city, order_date, amount in result:
    print(f"  Order {order_id}: {name} ({city}) - ${amount:.2f} on {order_date}")

# FULL OUTER JOIN
print("\n5. FULL OUTER JOIN (all records from both tables)...")
result = conn.execute("""
    SELECT
        COALESCE(c.customer_id, 0) as customer_id,
        c.name,
        COUNT(o.order_id) as num_orders,
        COALESCE(SUM(o.total_amount), 0) as total_amount
    FROM customers c
    FULL OUTER JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
    ORDER BY customer_id
""").fetchall()

print("Full outer join (all customers and orders):")
for cust_id, name, num_orders, total_amount in result:
    print(f"  Customer {cust_id}: {name}, Orders: {num_orders}, Total: ${total_amount:.2f}")

# CROSS JOIN
print("\n6. CROSS JOIN (all combinations)...")
conn.execute("""
    CREATE TABLE cities AS
    SELECT DISTINCT city FROM customers
    UNION
    SELECT DISTINCT city FROM customers WHERE city = 'Paris'
""")

result = conn.execute("""
    SELECT
        c.name,
        ci.city
    FROM customers c
    CROSS JOIN (SELECT DISTINCT city FROM customers LIMIT 3) ci
    LIMIT 5
""").fetchall()

print("Cross join sample (customers × cities):")
for name, city in result:
    print(f"  {name} in {city}")

# Multiple JOINs
print("\n7. Multiple joins (customers → orders)...")

# Create products table
conn.execute("""
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        name VARCHAR,
        price DECIMAL(10, 2)
    )
""")

conn.execute("""
    CREATE TABLE order_items (
        order_item_id INTEGER,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER
    )
""")

# Insert data
conn.execute("""
    INSERT INTO products VALUES
    (1, 'Laptop', 1200.00),
    (2, 'Mouse', 25.00),
    (3, 'Keyboard', 75.00),
    (4, 'Monitor', 350.00)
""")

conn.execute("""
    INSERT INTO order_items VALUES
    (1, 101, 1, 1),
    (2, 101, 2, 2),
    (3, 102, 3, 1),
    (4, 103, 1, 1),
    (5, 103, 4, 1),
    (6, 104, 2, 3)
""")

result = conn.execute("""
    SELECT
        c.name as customer_name,
        o.order_id,
        p.name as product_name,
        oi.quantity,
        p.price,
        oi.quantity * p.price as line_total
    FROM customers c
    INNER JOIN orders o ON c.customer_id = o.customer_id
    INNER JOIN order_items oi ON o.order_id = oi.order_id
    INNER JOIN products p ON oi.product_id = p.product_id
    ORDER BY o.order_id, p.name
""").fetchall()

print("Order details:")
print(f"{'Customer':<15} {'Order':<7} {'Product':<15} {'Qty':>4} {'Price':>8} {'Total':>10}")
print("-" * 65)
for cust_name, order_id, prod_name, qty, price, line_total in result:
    print(f"{cust_name:<15} {order_id:<7} {prod_name:<15} {qty:>4} ${price:>7.2f} ${line_total:>9.2f}")

# Self JOIN
print("\n8. Self JOIN (find similar customers)...")
conn.execute("""
    CREATE TABLE customer_pairs AS
    SELECT
        c1.customer_id as cust1_id,
        c1.name as cust1_name,
        c1.city as city,
        c2.customer_id as cust2_id,
        c2.name as cust2_name
    FROM customers c1
    JOIN customers c2 ON c1.city = c2.city AND c1.customer_id < c2.customer_id
""")

result = conn.execute("SELECT * FROM customer_pairs").fetchall()
if result:
    print("Customers in same city:")
    for c1_id, c1_name, city, c2_id, c2_name in result:
        print(f"  {c1_name} and {c2_name} (both in {city})")
else:
    print("  No customers share a city")

print("\n" + "=" * 60)
print("Join operations complete!")
print("=" * 60)
