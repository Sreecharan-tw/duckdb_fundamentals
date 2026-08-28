# DuckDB Fundamentals Repository

## Overview
This repository contains comprehensive examples and tutorials for learning DuckDB, an embedded SQL OLAP database. All examples are written in Python.

## Project Structure
- **examples/** - Individual Python scripts demonstrating DuckDB features
- **README.md** - Main documentation
- **requirements.txt** - Python dependencies

## Running Examples
Each example can be run independently:
```bash
python examples/01_basic_operations.py
python examples/02_data_types.py
# ... etc
```

## Example Topics Covered
1. Basic Operations (CREATE, INSERT, SELECT, DELETE)
2. Data Types (INTEGER, VARCHAR, DATE, DECIMAL, JSON, STRUCT, LIST)
3. CSV Operations (reading and writing CSV files)
4. Parquet Operations (working with Parquet format)
5. Pandas Integration (seamless DataFrame conversion)
6. Aggregations (GROUP BY, statistical functions)
7. Joins (INNER, LEFT, RIGHT, FULL, CROSS, self-joins)
8. Window Functions (ROW_NUMBER, RANK, LAG, LEAD, etc.)
9. Subqueries and CTEs (WITH clauses, recursive queries)
10. JSON Operations (JSON extraction, manipulation)
11. Time Series Analysis (date functions, moving averages)
12. Statistical Functions (percentiles, variance, correlation)
13. Performance Tips (optimization techniques)

## Key DuckDB Features
- Fast vectorized execution engine
- In-process database (no server needed)
- Multiple format support (CSV, Parquet, JSON)
- Seamless Pandas integration
- Full SQL support
- Optimized for OLAP workloads

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run example 01: `python examples/01_basic_operations.py`
3. Explore other examples in order

## Resources
- Official DuckDB docs: https://duckdb.org/docs/
- GitHub: https://github.com/duckdb/duckdb
