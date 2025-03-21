# Makefile

# Variables
PYTHON = poetry run
SOURCE_DIR = wotmud_player  # Replace with your source directory
TEST_DIR = .  # Replace with your test directory

install:  ## Install project dependencies
	poetry install
	pre-commit install

lint:  ## Run linting and formatting
	$(PYTHON) pre-commit run --all-files

test:  ## Run tests
	$(PYTHON) pytest $(TEST_DIR)

check: lint test  ## Run all checks (linting, formatting, and tests)

clean:  ## Clean up temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

run:  ## Run the application (if applicable)
	$(PYTHON) python $(SOURCE_DIR)/main.py  # Replace with your entry point

build:  ## Build the project (if applicable)
	poetry build

publish:  ## Publish the project to PyPI (if applicable)
	poetry publish

help:  ## Show this help message
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: install lint test check clean run build publish help