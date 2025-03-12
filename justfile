# List all available commands
default:
    @just --list

# Install the package and development dependencies
install:
    pip install -e ".[dev]"
    pre-commit install

# Format code
format:
    black src tests
    ruff check --fix src tests

# Lint code
lint:
    ruff check src tests
    mypy src tests

# Run tests with coverage
test:
    pytest --cov=maya --cov-report=term-missing

# Clean artifacts
clean:
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info
    rm -rf .pytest_cache/
    rm -rf .coverage
    rm -rf htmlcov/
    rm -rf .mypy_cache/
    rm -rf .ruff_cache/
    find . -type d -name __pycache__ -exec rm -rf {} +

# Build package
build: clean
    python -m build

# Run pre-commit hooks on all files
pre-commit-all:
    pre-commit run --all-files

# Setup a new development environment
setup-dev: install
    @echo "Development environment set up successfully!"

# Run the main application
run:
    python -m maya 