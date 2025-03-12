"""CLI tool for initializing Python projects with best practices."""

import os
import re
import shutil
import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer(
    help="Initialize Python projects with best practices for linting, testing, and CI."
)
console = Console()

# Use str instead of Literal for package manager
# PackageManager = Literal["pip", "uv"]


def create_directory_structure(project_path: Path) -> None:
    """Create the directory structure for a new project.
    
    Args:
        project_path: The path to the new project
    """
    dirs = [
        project_path / "src" / project_path.name,
        project_path / "tests",
        project_path / "docs",
        project_path / ".github" / "workflows",
    ]

    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        (dir_path / "__init__.py").touch(exist_ok=True)

    # Remove __init__.py from root directories where it's not needed
    if (project_path / "__init__.py").exists():
        os.remove(project_path / "__init__.py")
    if (project_path / "tests" / "__init__.py").exists():
        os.remove(project_path / "tests" / "__init__.py")


def replace_project_name(file_path: Path, old_name: str, new_name: str) -> None:
    """Replace the project name in a file.
    
    Args:
        file_path: Path to the file
        old_name: Original project name
        new_name: New project name
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Replace the project name, being careful with case (maya, MAYA, Maya)
    pattern = re.compile(re.escape(old_name), re.IGNORECASE)
    content = pattern.sub(lambda m: new_name if m.group(0).islower() else new_name.title(), content)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def copy_template_files(
    project_path: Path, 
    package_manager: str, 
    python_version: str,
    author_name: str,
    author_email: str,
    github_username: str
) -> None:
    """Copy and customize template files to the new project.
    
    Args:
        project_path: Path to the new project
        package_manager: Package manager to use
        python_version: Python version for the project
        author_name: Author's name
        author_email: Author's email
        github_username: GitHub username
    """
    template_path = Path(__file__).parent / "templates"
    
    # Copy template files
    for template_file in template_path.glob("**/*"):
        # Skip justfile templates, we'll handle those separately
        if template_file.name in ["justfile-uv", "justfile"] or not template_file.is_file():
            continue
        
        rel_path = template_file.relative_to(template_path)
        dest_path = project_path / rel_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read the template file
        with open(template_file, "r", encoding="utf-8") as file:
            content = file.read()
        
        # Replace placeholders with actual values
        replacements = {
            "{{project_name}}": project_path.name,
            "{{author_name}}": author_name,
            "{{author_email}}": author_email,
            "{{github_username}}": github_username,
            "{{python_version}}": python_version,
        }
        
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        # Write the customized file
        with open(dest_path, "w", encoding="utf-8") as file:
            file.write(content)

    # Handle justfile based on package manager
    if package_manager == "uv":
        just_template = template_path / "justfile-uv"
    else:
        just_template = template_path / "justfile"
    
    with open(just_template, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Replace placeholders
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    with open(project_path / "justfile", "w", encoding="utf-8") as file:
        file.write(content)

    # Create main module files
    with open(project_path / "src" / project_path.name / "__init__.py", "w", encoding="utf-8") as f:
        f.write(f'"""\n{project_path.name.title()} - Your project description here.\n"""\n\n__version__ = "0.1.0"\n')

    with open(project_path / "src" / project_path.name / "__main__.py", "w", encoding="utf-8") as f:
        f.write(f'"""Main entry point for the package when run as a module."""\n\nfrom {project_path.name}.main import main\n\nif __name__ == "__main__":\n    main()\n')  # noqa: E501

    with open(project_path / "src" / project_path.name / "main.py", "w", encoding="utf-8") as f:
        f.write(f'"""Main module for the {project_path.name.title()} application."""\n\nfrom typing import List, Optional\n\n\ndef main() -> None:\n    """Main entry point for the application."""\n    print("Hello from {project_path.name}!")\n\n\nif __name__ == "__main__":\n    main()\n')  # noqa: E501

    # Create a test file
    with open(project_path / "tests" / "test_main.py", "w", encoding="utf-8") as f:
        f.write(f'"""Tests for the main module."""\n\nimport pytest\n\nfrom {project_path.name}.main import main\n\n\ndef test_main() -> None:\n    """Test the main function."""\n    # This is a placeholder test\n    assert True\n')  # noqa: E501


@app.command()
def init(
    project_name: str = typer.Argument(..., help="Name of the project to create"),
    package_manager: str = typer.Option(
        "pip", "--package-manager", "-p", help="Package manager to use (pip or uv)"
    ),
    python_version: str = typer.Option(
        "3.8", "--python-version", "-py", help="Minimum Python version required"
    ),
    author_name: str = typer.Option(
        "", "--author", "-a", help="Author name"
    ),
    author_email: str = typer.Option(
        "", "--email", "-e", help="Author email"
    ),
    github_username: str = typer.Option(
        "", "--github", "-g", help="GitHub username"
    ),
) -> None:
    """Initialize a new Python project with best practices.
    
    Creates a new project directory with a standardized structure,
    linting, testing, and CI configuration.
    """
    # Validate package manager input
    if package_manager not in ["pip", "uv"]:
        console.print(f"[bold red]Error:[/] Package manager must be either 'pip' or 'uv', got '{package_manager}'.")
        sys.exit(1)

    # Validate project name (should be a valid Python package name)
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", project_name):
        console.print(f"[bold red]Error:[/] Project name '{project_name}' is not a valid Python package name.")
        sys.exit(1)
    
    # Set defaults for optional parameters
    if not author_name:
        author_name = "Your Name"
    if not author_email:
        author_email = "your.email@example.com"
    if not github_username:
        github_username = "username"
    
    project_path = Path(project_name)
    
    # Check if directory already exists
    if project_path.exists():
        overwrite = typer.confirm(
            f"Directory '{project_name}' already exists. Overwrite?",
            default=False,
        )
        if not overwrite:
            console.print("[yellow]Aborted.[/]")
            sys.exit(0)
        shutil.rmtree(project_path)
    
    console.print(f"[green]Creating project: [bold]{project_name}[/][/]")
    
    # Create directory structure
    create_directory_structure(project_path)
    
    # Copy and customize template files
    copy_template_files(
        project_path, 
        package_manager, 
        python_version,
        author_name,
        author_email,
        github_username
    )
    
    # Display summary
    console.print(
        Panel(
            Text.from_markup(
                f"[bold green]Project created successfully![/]\n\n"
                f"To get started with your new project:\n\n"
                f"[bold]cd {project_name}[/]\n"
                f"[bold]just setup-dev[/]"
            ),
            title="Success",
            expand=False,
        )
    )
    
    # Show additional information about uv if selected
    if package_manager == "uv":
        console.print(
            Panel(
                Text.from_markup(
                    "[bold blue]UV Package Manager[/]\n\n"
                    "Your project is configured to use the [bold]uv[/bold] package manager.\n"
                    "Make sure uv is installed with:\n\n"
                    "[bold]pip install uv[/bold]\n\n"
                    "The justfile includes special commands for uv:"
                    "\n• [bold]just add-dep package-name[/bold] - Add a new dependency with uv"
                ),
                title="UV Configuration",
                expand=False,
            )
        )


@app.command()
def version() -> None:
    """Show the version of the Maya CLI tool."""
    try:
        from maya import __version__
        console.print(f"Maya CLI v{__version__}")
    except ImportError:
        console.print("Maya CLI v0.1.0")


def main() -> None:
    """Entry point for the application."""
    app()


if __name__ == "__main__":
    main() 