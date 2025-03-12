# {{project_name}}

[![Python CI](https://github.com/{{github_username}}/{{project_name}}/actions/workflows/python-ci.yml/badge.svg)](https://github.com/{{github_username}}/{{project_name}}/actions/workflows/python-ci.yml)

A Python project with best practices for structure, linting, testing, and CI.

## Features

- 📦 Standardized project structure
- 🧹 Linting and formatting with `ruff`, `mypy`, and `black`
- 🧪 Testing with `pytest` and coverage reporting
- 🔄 Pre-commit hooks for code quality
- 🛠️ Task automation with `just` (improved alternative to `make`)
- 🚀 CI/CD with GitHub Actions

## Project Structure

```
{{project_name}}/
├── .github/
│   └── workflows/
│       └── python-ci.yml
├── src/
│   └── {{project_name}}/
│       ├── __init__.py
│       ├── __main__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── .pre-commit-config.yaml
├── justfile
├── pyproject.toml
└── README.md
```

## Getting Started

### Prerequisites

- Python {{python_version}} or higher
- [just](https://github.com/casey/just) command runner
- [pipx](https://github.com/pypa/pipx) (recommended for installing CLI tools)

Install the `just` command runner:

```bash
# On macOS
brew install just

# On Linux
pipx install just

# On Windows (with chocolatey)
choco install just
```

### Setup

Run the setup command:

```bash
just setup-dev
```

This will:
- Install the package in development mode
- Install all development dependencies
- Setup pre-commit hooks

## Development Tasks

The `justfile` provides various commands for common development tasks:

```bash
# Show all available commands
just

# Install the package and dependencies
just install

# Format code
just format

# Lint code
just lint

# Run tests with coverage
just test

# Run the application
just run

# Clean build artifacts
just clean

# Run pre-commit hooks on all files
just pre-commit-all
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 