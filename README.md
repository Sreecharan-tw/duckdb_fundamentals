# DuckDB Fundamentals

A comprehensive repository with examples and tutorials for learning DuckDB, a fast in-process SQL database.

## What is DuckDB?

DuckDB is an embedded SQL OLAP database management system. It's optimized for analytical workloads and can process data faster than traditional databases for many operations.

## Getting Started

### Quick Setup with UV + Make

The easiest way to get started is using UV (fast Python package installer) with Make:

```bash
# Install UV (one-time)
pip install uv
# or
brew install uv  # macOS

# Install dependencies with UV
make install

# Run examples
make run-01       # Run basic operations example
make run-02       # Run data types example
# ... or
make run-all      # Run all 13 examples
```

### Manual Setup with UV

If you prefer to do it manually:

```bash
# Install UV (if not already installed)
pip install uv

# Install dependencies from pyproject.toml
uv sync

# Verify installation
uv run examples/01_basic_operations.py
```

### Verify Installation

After setup, verify everything works:

```bash
make version  # Show Python and DuckDB versions
make run-01   # Run first example (should complete successfully)
```

### Legacy Setup with pip

If you don't have UV installed:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run example
python examples/01_basic_operations.py
```

## Repository Structure

- **examples/** - Individual examples demonstrating different DuckDB features
- **Makefile** - Convenient commands for setup, running examples, and cleanup
- **requirements.txt** - Python dependencies

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

### Using Make (Recommended)

```bash
# Run a specific example
make run-01    # Basic operations
make run-02    # Data types
make run-03    # CSV operations
# ... etc (run-01 through run-13)

# Run all examples
make run-all

# List all available examples
make list

# View all available commands
make help
```

### Direct Python

Each example file can be run independently:

```bash
python examples/01_basic_operations.py
python examples/02_data_types.py
# ... and so on
```

## Makefile Commands

The project includes a Makefile for convenient commands using UV:

### Setup
- `make install` - Install dependencies with UV (creates .venv)
- `make install-dev` - Install with dev dependencies (includes jupyter, matplotlib, etc.)
- `make sync` - Sync dependencies from uv.lock file

### Run Examples
- `make run-01` through `make run-13` - Run specific examples
- `make run NUM=01` - Alternative way to run specific example
- `make run-all` - Run all 13 examples sequentially
- `make list` - Display all available examples

### Development
- `make lint` - Run ruff linter on examples
- `make format` - Format code with black
- `make clean` - Remove Python cache files
- `make clean-all` - Complete cleanup (.venv + cache + lock file)

### Other
- `make help` - Show all available commands
- `make version` - Display Python, UV, and DuckDB versions

## Why UV?

UV is a fast, Rust-based Python package installer that provides:

- **⚡ Fast** - 10-100x faster than pip
- **🔒 Reliable** - Deterministic dependency resolution
- **📦 Lock files** - uv.lock ensures reproducible environments
- **🎯 Simple** - Drop-in replacement for pip and venv
- **🐍 Python-native** - Installs and manages Python versions

For more info: https://github.com/astral-sh/uv

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
