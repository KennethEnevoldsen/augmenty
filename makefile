install:
	@echo "--- 🚀 Installing project ---"
	uv sync --all-extras --all-groups

static-type-check:
	@echo "--- 🔍 Running static type check ---"
	uv run --group dev ty check src/ tests/

lint:
	@echo "--- 🧹 Running linters ---"
	uv run --group dev ruff format .
	uv run --group dev ruff check . --fix

lint-check:
	@echo "--- 🧹 Checking linting (no changes) ---"
	uv run --group dev ruff format . --check
	uv run --group dev ruff check .

test:
	@echo "--- 🧪 Running tests ---"
	uv run --group tests pytest tests/

pr:
	@echo "--- 🚀 Running PR checks ---"
	make lint
	make static-type-check
	make test
	@echo "Ready to make a PR"

build-docs:
	@echo "--- 📚 Building docs ---"
	uv run --group docs --extra all python docs/create_augmenters_table.py
	uv run --group docs --extra all sphinx-build -M html docs/ docs/_build

view-docs:
	@echo "--- 👀 Viewing docs ---"
	open docs/_build/html/index.html
