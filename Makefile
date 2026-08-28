.PHONY: help install dev clean clean-all run-example help-examples list-examples

# Variables
PYTHON := python3
UV := uv
VENV_DIR := .venv

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
RED := \033[0;31m
NC := \033[0m # No Color

# Default target
help:
	@echo "$(BLUE)DuckDB Fundamentals - Makefile Commands (UV)$(NC)"
	@echo ""
	@echo "$(GREEN)Setup Commands:$(NC)"
	@echo "  $(YELLOW)make install$(NC)      - Install dependencies with UV"
	@echo "  $(YELLOW)make install-dev$(NC)   - Install with dev dependencies"
	@echo "  $(YELLOW)make sync$(NC)          - Sync UV lock file"
	@echo ""
	@echo "$(GREEN)Run Commands:$(NC)"
	@echo "  $(YELLOW)make run-00$(NC)        - Create persistent database (for DBeaver/CLI)"
	@echo "  $(YELLOW)make run-01$(NC)        - Run basic operations example"
	@echo "  $(YELLOW)make run-02$(NC)        - Run data types example"
	@echo "  $(YELLOW)make run-03$(NC)        - Run CSV operations example"
	@echo "  $(YELLOW)make run-04$(NC)        - Run Parquet operations example"
	@echo "  $(YELLOW)make run-05$(NC)        - Run Pandas integration example"
	@echo "  $(YELLOW)make run-06$(NC)        - Run aggregations example"
	@echo "  $(YELLOW)make run-07$(NC)        - Run joins example"
	@echo "  $(YELLOW)make run-08$(NC)        - Run window functions example"
	@echo "  $(YELLOW)make run-09$(NC)        - Run subqueries & CTEs example"
	@echo "  $(YELLOW)make run-10$(NC)        - Run JSON operations example"
	@echo "  $(YELLOW)make run-11$(NC)        - Run time series example"
	@echo "  $(YELLOW)make run-12$(NC)        - Run statistics example"
	@echo "  $(YELLOW)make run-13$(NC)        - Run performance tips example"
	@echo "  $(YELLOW)make run-14$(NC)        - Run Pandas vs DuckDB comparison"
	@echo "  $(YELLOW)make run-all$(NC)       - Run all examples"
	@echo "  $(YELLOW)make run NUM=<n>$(NC)   - Run specific example (e.g., make run NUM=01)"
	@echo ""
	@echo "$(GREEN)Utility Commands:$(NC)"
	@echo "  $(YELLOW)make list$(NC)          - List all available examples"
	@echo "  $(YELLOW)make clean$(NC)         - Remove Python cache and lock files"
	@echo "  $(YELLOW)make clean-all$(NC)     - Remove .venv and cache files"
	@echo "  $(YELLOW)make version$(NC)       - Show Python and UV version"
	@echo "  $(YELLOW)make lint$(NC)          - Run linting with ruff"
	@echo "  $(YELLOW)make format$(NC)        - Format code with black"
	@echo "  $(YELLOW)make help$(NC)          - Show this help message"
	@echo ""

# Install dependencies
install: check-uv
	@echo "$(GREEN)Installing dependencies with UV...$(NC)"
	$(UV) sync
	@echo "$(GREEN)✓ Dependencies installed successfully$(NC)"

# Install with dev dependencies
install-dev: check-uv
	@echo "$(GREEN)Installing with dev dependencies...$(NC)"
	$(UV) sync --all-extras
	@echo "$(GREEN)✓ Dev dependencies installed$(NC)"

# Sync with lock file
sync: check-uv
	@echo "$(GREEN)Syncing with UV lock file...$(NC)"
	$(UV) sync
	@echo "$(GREEN)✓ Sync complete$(NC)"

# List all examples
list:
	@echo "$(BLUE)Available DuckDB Examples:$(NC)"
	@echo ""
	@echo "$(GREEN)01 - Basic Operations$(NC)"
	@echo "     CREATE, INSERT, SELECT, UPDATE, DELETE operations"
	@echo ""
	@echo "$(GREEN)02 - Data Types$(NC)"
	@echo "     Working with different data types (INTEGER, VARCHAR, DATE, etc.)"
	@echo ""
	@echo "$(GREEN)03 - CSV Operations$(NC)"
	@echo "     Reading and writing CSV files"
	@echo ""
	@echo "$(GREEN)04 - Parquet Operations$(NC)"
	@echo "     Working with Parquet format files"
	@echo ""
	@echo "$(GREEN)05 - Pandas Integration$(NC)"
	@echo "     Seamless DataFrame conversion and integration"
	@echo ""
	@echo "$(GREEN)06 - Aggregations$(NC)"
	@echo "     GROUP BY and aggregation functions"
	@echo ""
	@echo "$(GREEN)07 - Joins$(NC)"
	@echo "     INNER, LEFT, RIGHT, FULL, CROSS joins and self-joins"
	@echo ""
	@echo "$(GREEN)08 - Window Functions$(NC)"
	@echo "     ROW_NUMBER, RANK, LAG, LEAD, and moving averages"
	@echo ""
	@echo "$(GREEN)09 - Subqueries & CTEs$(NC)"
	@echo "     WITH clauses and recursive queries"
	@echo ""
	@echo "$(GREEN)10 - JSON Operations$(NC)"
	@echo "     Working with JSON data"
	@echo ""
	@echo "$(GREEN)11 - Time Series Analysis$(NC)"
	@echo "     Date functions and time-based operations"
	@echo ""
	@echo "$(GREEN)12 - Statistical Functions$(NC)"
	@echo "     Percentiles, variance, correlation, and distributions"
	@echo ""
	@echo "$(GREEN)13 - Performance Tips$(NC)"
	@echo "     Query optimization and best practices"
	@echo ""
	@echo "$(GREEN)14 - Pandas vs DuckDB Comparison$(NC)"
	@echo "     Speed and ease of use benchmark (100K rows Parquet)"

# Run individual examples
run-00: check-uv
	@$(UV) run examples/00_persistent_database.py

run-01: check-uv
	@$(UV) run examples/01_basic_operations.py

run-02: check-uv
	@$(UV) run examples/02_data_types.py

run-03: check-uv
	@$(UV) run examples/03_csv_operations.py

run-04: check-uv
	@$(UV) run examples/04_parquet_operations.py

run-05: check-uv
	@$(UV) run examples/05_pandas_integration.py

run-06: check-uv
	@$(UV) run examples/06_aggregations.py

run-07: check-uv
	@$(UV) run examples/07_joins.py

run-08: check-uv
	@$(UV) run examples/08_window_functions.py

run-09: check-uv
	@$(UV) run examples/09_subqueries_ctes.py

run-10: check-uv
	@$(UV) run examples/10_json_operations.py

run-11: check-uv
	@$(UV) run examples/11_time_series.py

run-12: check-uv
	@$(UV) run examples/12_statistics.py

run-13: check-uv
	@$(UV) run examples/13_performance_tips.py

run-14: check-uv
	@$(UV) run examples/14_pandas_vs_duckdb.py

# Run specific example by number
run: check-uv
	@if [ -z "$(NUM)" ]; then \
		echo "$(RED)Error: NUM parameter required$(NC)"; \
		echo "Usage: make run NUM=01"; \
		exit 1; \
	fi
	@if [ ! -f "examples/$(NUM)_*.py" ]; then \
		echo "$(RED)Error: Example $(NUM) not found$(NC)"; \
		exit 1; \
	fi
	@$(UV) run examples/$(NUM)_*.py

# Run all examples
run-all: check-uv
	@echo "$(BLUE)Running all DuckDB examples...$(NC)"
	@echo ""
	@echo "$(BLUE)Running example 00 (persistent database)...$(NC)"
	@$(UV) run examples/00_persistent_database.py
	@echo ""
	@for i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14; do \
		echo "$(BLUE)Running example $$i...$(NC)"; \
		$(UV) run examples/$$i*.py; \
		echo ""; \
	done
	@echo "$(GREEN)✓ All examples completed$(NC)"

# Check if UV is installed
check-uv:
	@if ! command -v $(UV) &> /dev/null; then \
		echo "$(RED)Error: UV not found$(NC)"; \
		echo "$(YELLOW)Install UV from: https://github.com/astral-sh/uv$(NC)"; \
		echo "$(YELLOW)or with: pip install uv$(NC)"; \
		exit 1; \
	fi

# Lint code with ruff
lint: check-uv
	@echo "$(GREEN)Running ruff linter...$(NC)"
	@$(UV) run ruff check examples/
	@echo "$(GREEN)✓ Linting complete$(NC)"

# Format code with black
format: check-uv
	@echo "$(GREEN)Formatting code with black...$(NC)"
	@$(UV) run black examples/
	@echo "$(GREEN)✓ Formatting complete$(NC)"

# Clean Python cache files
clean:
	@echo "$(GREEN)Cleaning Python cache files...$(NC)"
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.ruff_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '.coverage' -delete
	@echo "$(GREEN)✓ Cache files cleaned$(NC)"

# Clean everything
clean-all: clean
	@echo "$(YELLOW)Removing .venv and uv.lock...$(NC)"
	rm -rf .venv uv.lock
	@echo "$(GREEN)✓ All cleanup complete$(NC)"

# Display Python and UV version
version: check-uv
	@echo "$(BLUE)Python and UV info:$(NC)"
	@$(PYTHON) --version
	@$(UV) --version
	@echo ""
	@echo "$(GREEN)DuckDB version from dependencies:$(NC)"
	@$(UV) run python -c "import duckdb; print(f'DuckDB {duckdb.__version__}')"

.DEFAULT_GOAL := help
