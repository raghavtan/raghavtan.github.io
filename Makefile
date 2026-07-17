ifneq ($(shell command -v tput 2> /dev/null),)
    YELLOW := $(shell tput setaf 3)
    GREEN := $(shell tput setaf 2)
    RED := $(shell tput setaf 1)
    BLUE := $(shell tput setaf 4)
    RESET := $(shell tput sgr0)
else
    YELLOW :=
    GREEN :=
    RED :=
    BLUE :=
    RESET :=
endif

# Output directory for generated artifacts (also the Pages deploy artifact).
OUTPUT_DIR := public

.PHONY: help setup install lint fmt fmt-check test ci generate build serve clean

help:  ## Show this help message
	@echo "$(YELLOW)Available commands:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-14s$(RESET) %s\n", $$1, $$2}'

setup: install  ## One-shot dev setup: sync deps + install pre-commit hooks
	@echo "$(BLUE)Installing pre-commit git hooks...$(RESET)"
	@uv run pre-commit install
	@echo "$(GREEN)Setup complete.$(RESET)"

install:  ## Sync the virtual environment from pyproject.toml/uv.lock
	@echo "$(BLUE)Syncing dependencies with uv...$(RESET)"
	@uv sync
	@echo "$(GREEN)Dependencies synced.$(RESET)"

lint:  ## Lint with ruff
	@echo "$(BLUE)Linting with ruff...$(RESET)"
	@uv run ruff check .
	@echo "$(GREEN)Lint clean.$(RESET)"

fmt:  ## Format code with ruff
	@echo "$(BLUE)Formatting with ruff...$(RESET)"
	@uv run ruff format .
	@echo "$(GREEN)Format complete.$(RESET)"

fmt-check:  ## Check formatting without writing changes
	@uv run ruff format --check .

test:  ## Run the test suite
	@echo "$(BLUE)Running tests...$(RESET)"
	@uv run pytest
	@echo "$(GREEN)Tests passed.$(RESET)"

ci: lint fmt-check test  ## Run everything CI runs (lint + format check + tests)
	@echo "$(GREEN)CI checks passed.$(RESET)"

generate:  ## Generate resume artifacts into $(OUTPUT_DIR)/
	@echo "$(BLUE)Generating resume into $(OUTPUT_DIR)/...$(RESET)"
	@uv run python main.py
	@echo "$(GREEN)Generation complete.$(RESET)"

build: ci generate  ## Full build: run CI checks then generate the site
	@echo "$(GREEN)Build complete -> $(OUTPUT_DIR)/$(RESET)"

serve: generate  ## Generate then serve the site locally on :8000
	@echo "$(YELLOW)Serving $(OUTPUT_DIR)/ at http://localhost:8000$(RESET)"
	@uv run python -m http.server 8000 --directory $(OUTPUT_DIR)

clean:  ## Remove generated artifacts and caches
	@echo "$(RED)Cleaning up...$(RESET)"
	@rm -rf $(OUTPUT_DIR) __pycache__ */__pycache__ .pytest_cache .ruff_cache
	@echo "$(GREEN)Cleanup done.$(RESET)"
