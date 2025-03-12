# Maya

A Python project initializer CLI that sets up project scaffolding with best practices for structure, linting, testing, and CI.

## Features

- 📦 Creates standardized project structure
- 🧹 Sets up linting and formatting with `ruff`, `mypy`, and `black`
- 🧪 Configures testing with `pytest` and coverage reporting
- 🔄 Installs pre-commit hooks for code quality
- 🛠️ Creates task automation with `just` (improved alternative to `make`)
- 🚀 Sets up CI/CD with GitHub Actions
- 🔌 Supports both `pip` and `uv` package managers

## Installation

```bash
# Clone the repository
git clone https://github.com/WeiNyn/maya.git
cd maya

# Install the package
pip install -e .
```

## Usage

### Initialize a new project

```bash
# Basic usage
maya init my_project

# With uv package manager
maya init my_project --package-manager uv

# With custom Python version
maya init my_project --python-version 3.10

# With author information
maya init my_project --author "Your Name" --email "your.email@example.com" --github yourusername
```

### Options

```
--package-manager, -p TEXT     Package manager to use (pip or uv) [default: pip]
--python-version, -py TEXT     Minimum Python version required [default: 3.8]
--author, -a TEXT              Author name
--email, -e TEXT               Author email
--github, -g TEXT              GitHub username
--help                         Show help message and exit
```

## Generated Project Structure

When you run `maya init my_project`, it creates a new project with the following structure:

```
my_project/
├── .github/
│   └── workflows/
│       └── python-ci.yml
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── __main__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── .pre-commit-config.yaml
├── .gitignore
├── justfile
├── pyproject.toml
└── README.md
```

## UV Package Manager Support

Maya supports the [uv](https://github.com/astral-sh/uv) package manager, a fast Python package installer and resolver written in Rust. To use uv with your projects:

```bash
# Install uv
pip install uv

# Create a new project with uv support
maya init my_project --package-manager uv
```

When using the uv option, Maya:
- Configures the justfile with uv-specific commands
- Adds additional utilities like `just add-dep [package]` to manage dependencies with uv

## Development

To contribute to Maya:

```bash
# Clone the repository
git clone https://github.com/username/maya.git
cd maya

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 