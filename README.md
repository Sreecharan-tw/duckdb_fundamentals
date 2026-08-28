# DuckDB Fundamentals

A comprehensive repository with examples and tutorials for learning DuckDB, a fast in-process SQL database.

## What is DuckDB?

DuckDB is an embedded SQL OLAP database management system. It's optimized for analytical workloads and can process data faster than traditional databases for many operations.

## Getting Started

### Installation

```bash
pip install -r requirements.txt
```

This will install DuckDB and other required dependencies.

## Repository Structure

- **examples/** - Individual examples demonstrating different DuckDB features
- **data/** - Sample datasets used in examples
- **notebooks/** - Jupyter notebooks with detailed explanations

## Examples Overview

### Basic Operations
- `01_basic_operations.py` - Create, insert, query, and delete operations
- `02_data_types.py` - Working with different data types in DuckDB

### Data Loading & I/O
- `03_csv_operations.py` - Reading and writing CSV files
- `04_parquet_operations.py` - Working with Parquet files
- `05_pandas_integration.py` - Integration with Pandas DataFrames

### SQL Features
- `06_aggregations.py` - GROUP BY, aggregation functions
- `07_joins.py` - INNER, LEFT, RIGHT, FULL joins
- `08_window_functions.py` - ROW_NUMBER, RANK, LAG, LEAD, etc.
- `09_subqueries_ctes.py` - Subqueries and Common Table Expressions

### Advanced Features
- `10_json_operations.py` - Working with JSON data
- `11_time_series.py` - Time series analysis
- `12_statistics.py` - Statistical functions and computations

### Performance & Tips
- `13_performance_tips.py` - Query optimization techniques

## Running Examples

Each example file can be run independently:

```bash
python examples/01_basic_operations.py
python examples/02_data_types.py
# ... and so on
```

## Key DuckDB Features

- **Fast**: Optimized vectorized execution engine
- **In-Process**: No separate server process needed
- **SQL**: Full SQL support with Python integration
- **Multiple Formats**: Read/write CSV, Parquet, JSON, etc.
- **Pandas Integration**: Seamless conversion between DuckDB and Pandas
- **Analytical**: Optimized for OLAP workloads, not OLTP

## Documentation

For complete DuckDB documentation, visit: https://duckdb.org/docs/

## Prerequisites

- Python 3.8+
- Basic SQL knowledge
- Familiarity with Python

## License

MIT

## Contributing

Feel free to add more examples and improvements!
