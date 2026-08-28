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

## Instructions for Claude

### Commit Strategy
⚠️ **DO NOT commit changes after each iteration or code change.**

Instead:
- Make multiple file edits/changes
- Batch related changes together
- **Only commit when explicitly asked** ("commit this", "save changes", etc.)
- When you do commit, combine related changes into one commit with a comprehensive message

**Rationale:**
- Keeps git history clean and organized
- Avoids cluttering the commit log with intermediate changes
- Allows for better grouping of related work
- Faster workflow with fewer git operations

### Code Changes
- Edit/create files as needed for features and fixes
- Test changes before committing
- Don't ask for permission to edit files
- Batch test + feature together when possible

### When to Commit
- User explicitly asks: "commit this", "save", "make a commit"
- At the end of a complete feature or fix
- When several related changes are ready
- When asked for a pull request

**Example Workflow:**
```
1. User: "Add feature X and Y"
2. Claude: Creates files, edits code (no commits)
3. Claude: Tests both features
4. Claude: Shows the work is complete
5. User: "Commit this" → Claude commits
```
