# memtop — developer tasks
# Everything runs through `uv run --with`, mirroring the single-file script's
# self-contained philosophy: no project scaffolding, no venv to manage.

# Runtime deps the script imports (kept in sync with memtop's PEP 723 block).
DEPS := --with psutil --with rich --with typer

.DEFAULT_GOAL := help

.PHONY: help test lint format check install clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

test: ## Run the test suite (pytest)
	uv run $(DEPS) --with pytest pytest -v

lint: ## Lint with ruff (and verify formatting)
	uv run --with ruff ruff check .
	uv run --with ruff ruff format --check .

format: ## Auto-format with ruff
	uv run --with ruff ruff format .
	uv run --with ruff ruff check --fix .

check: lint test ## Run lint + tests (what CI runs)

install: ## Symlink memtop onto your PATH (~/.local/bin)
	mkdir -p $(HOME)/.local/bin
	ln -sf $(CURDIR)/memtop $(HOME)/.local/bin/memtop
	@echo "Linked $(CURDIR)/memtop -> $(HOME)/.local/bin/memtop"

clean: ## Remove caches
	rm -rf .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
