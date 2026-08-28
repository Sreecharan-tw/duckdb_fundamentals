.PHONY: help venv install clean clean-all run-example help-examples list-examples

# Variables
PYTHON := python3
VENV_DIR := venv
VENV_BIN := $(VENV_DIR)/bin
REQUIREMENTS := requirements.txt

# Colors for output
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
RED := \033[0;31m
NC := \033[0m # No Color

# Default target
help:
	@echo "$(BLUE)DuckDB Fundamentals - Makefile Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Setup Commands:$(NC)"
	@echo "  $(YELLOW)make venv$(NC)           - Create virtual environment"
	@echo "  $(YELLOW)make install$(NC)        - Install dependencies"
	@echo "  $(YELLOW)make setup$(NC)          - Create venv and install dependencies (recommended)"
	@echo ""
	@echo "$(GREEN)Run Commands:$(NC)"
	@echo "  $(YELLOW)make run-01$(NC)         - Run basic operations example"
	@echo "  $(YELLOW)make run-02$(NC)         - Run data types example"
	@echo "  $(YELLOW)make run-03$(NC)         - Run CSV operations example"
	@echo "  $(YELLOW)make run-04$(NC)         - Run Parquet operations example"
	@echo "  $(YELLOW)make run-05$(NC)         - Run Pandas integration example"
	@echo "  $(YELLOW)make run-06$(NC)         - Run aggregations example"
	@echo "  $(YELLOW)make run-07$(NC)         - Run joins example"
	@echo "  $(YELLOW)make run-08$(NC)         - Run window functions example"
	@echo "  $(YELLOW)make run-09$(NC)         - Run subqueries & CTEs example"
	@echo "  $(YELLOW)make run-10$(NC)         - Run JSON operations example"
	@echo "  $(YELLOW)make run-11$(NC)         - Run time series example"
	@echo "  $(YELLOW)make run-12$(NC)         - Run statistics example"
	@echo "  $(YELLOW)make run-13$(NC)         - Run performance tips example"
	@echo "  $(YELLOW)make run-all$(NC)        - Run all examples"
	@echo "  $(YELLOW)make run-example NUM=<n>$(NC) - Run specific example (e.g., make run-example NUM=01)"
	@echo ""
	@echo "$(GREEN)Utility Commands:$(NC)"
	@echo "  $(YELLOW)make list$(NC)           - List all available examples"
	@echo "  $(YELLOW)make clean$(NC)          - Remove Python cache files"
	@echo "  $(YELLOW)make clean-venv$(NC)     - Remove virtual environment"
	@echo "  $(YELLOW)make clean-all$(NC)      - Remove venv and cache files"
	@echo "  $(YELLOW)make help$(NC)           - Show this help message"
	@echo ""

# Create virtual environment
venv:
	@echo "$(GREEN)Creating virtual environment...$(NC)"
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "$(GREEN)✓ Virtual environment created at $(VENV_DIR)$(NC)"
	@echo ""
	@echo "$(YELLOW)To activate the virtual environment, run:$(NC)"
	@echo "  $(BLUE)source $(VENV_DIR)/bin/activate$(NC)  (Linux/Mac)"
	@echo "  $(BLUE)$(VENV_DIR)\Scripts\activate$(NC)    (Windows)"

# Install dependencies
install: venv
	@echo "$(GREEN)Installing dependencies...$(NC)"
	$(VENV_BIN)/pip install --upgrade pip setuptools wheel
	$(VENV_BIN)/pip install -r $(REQUIREMENTS)
	@echo "$(GREEN)✓ Dependencies installed successfully$(NC)"

# Setup (create venv and install)
setup: venv install
	@echo ""
	@echo "$(GREEN)✓ Setup complete!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  1. Activate the virtual environment:"
	@echo "     $(BLUE)source $(VENV_DIR)/bin/activate$(NC)"
	@echo "  2. Run examples:"
	@echo "     $(BLUE)make run-01$(NC)  (or any example number)"
	@echo "  3. Run all examples:"
	@echo "     $(BLUE)make run-all$(NC)"

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

# Run individual examples
run-01: check-venv
	@$(VENV_BIN)/python examples/01_basic_operations.py

run-02: check-venv
	@$(VENV_BIN)/python examples/02_data_types.py

run-03: check-venv
	@$(VENV_BIN)/python examples/03_csv_operations.py

run-04: check-venv
	@$(VENV_BIN)/python examples/04_parquet_operations.py

run-05: check-venv
	@$(VENV_BIN)/python examples/05_pandas_integration.py

run-06: check-venv
	@$(VENV_BIN)/python examples/06_aggregations.py

run-07: check-venv
	@$(VENV_BIN)/python examples/07_joins.py

run-08: check-venv
	@$(VENV_BIN)/python examples/08_window_functions.py

run-09: check-venv
	@$(VENV_BIN)/python examples/09_subqueries_ctes.py

run-10: check-venv
	@$(VENV_BIN)/python examples/10_json_operations.py

run-11: check-venv
	@$(VENV_BIN)/python examples/11_time_series.py

run-12: check-venv
	@$(VENV_BIN)/python examples/12_statistics.py

run-13: check-venv
	@$(VENV_BIN)/python examples/13_performance_tips.py

# Run specific example by number
run-example: check-venv
	@if [ -z "$(NUM)" ]; then \
		echo "$(RED)Error: NUM parameter required$(NC)"; \
		echo "Usage: make run-example NUM=01"; \
		exit 1; \
	fi
	@if [ ! -f "examples/$(NUM)_*.py" ]; then \
		echo "$(RED)Error: Example $(NUM) not found$(NC)"; \
		exit 1; \
	fi
	@$(VENV_BIN)/python examples/$(NUM)_*.py

# Run all examples
run-all: check-venv
	@echo "$(BLUE)Running all DuckDB examples...$(NC)"
	@echo ""
	@for i in 01 02 03 04 05 06 07 08 09 10 11 12 13; do \
		echo "$(BLUE)Running example $$i...$(NC)"; \
		$(VENV_BIN)/python examples/$$i*.py; \
		echo ""; \
	done
	@echo "$(GREEN)✓ All examples completed$(NC)"

# Check if venv exists
check-venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(RED)Error: Virtual environment not found$(NC)"; \
		echo "$(YELLOW)Please run: make setup$(NC)"; \
		exit 1; \
	fi

# Clean Python cache files
clean:
	@echo "$(GREEN)Cleaning Python cache files...$(NC)"
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '.tox' -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '.coverage' -delete
	find . -type f -name 'htmlcov' -delete
	@echo "$(GREEN)✓ Cache files cleaned$(NC)"

# Remove virtual environment
clean-venv:
	@echo "$(YELLOW)Removing virtual environment...$(NC)"
	rm -rf $(VENV_DIR)
	@echo "$(GREEN)✓ Virtual environment removed$(NC)"

# Clean everything
clean-all: clean clean-venv
	@echo "$(GREEN)✓ All cleanup complete$(NC)"

# Create .python-version file (for pyenv users)
.python-version:
	@echo "3.8" > .python-version
	@echo "$(GREEN)✓ .python-version file created$(NC)"

# Install pre-commit hooks
install-hooks:
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "$(GREEN)Installing pre-commit hooks...$(NC)"; \
		$(VENV_BIN)/pip install pre-commit; \
		$(VENV_BIN)/pre-commit install; \
		echo "$(GREEN)✓ Pre-commit hooks installed$(NC)"; \
	else \
		echo "$(RED)Error: Virtual environment not found$(NC)"; \
		echo "$(YELLOW)Please run: make setup$(NC)"; \
	fi

# Display Python version
version:
	@echo "$(BLUE)Python and environment info:$(NC)"
	@$(PYTHON) --version
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "Virtual environment: $(GREEN)✓ Active$(NC)"; \
		echo "Location: $(VENV_DIR)"; \
	else \
		echo "Virtual environment: $(RED)✗ Not found$(NC)"; \
	fi

# Freeze requirements
freeze: check-venv
	@echo "$(GREEN)Freezing dependencies...$(NC)"
	$(VENV_BIN)/pip freeze > requirements-frozen.txt
	@echo "$(GREEN)✓ Frozen requirements saved to requirements-frozen.txt$(NC)"

.DEFAULT_GOAL := help
