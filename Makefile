.PHONY: install test lint format clean build dev-install

install:
	uv pip install -e .

dev-install:
	uv pip install -e ".[dev]"

test:
	uv run pytest tests/ -v

test-cov:
	uv run pytest tests/ --cov=icms --cov-report=html --cov-report=term

lint:
	uv run ruff check src/ tests/
	uv run mypy src/

format:
	uv run ruff format src/ tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .coverage htmlcov/

build:
	uv build

# Quick check - runs fast subset of checks
quick:
	uv run ruff check src/
	uv run python examples/basic_usage.py