"""Tests for the main module."""

import os
from pathlib import Path
from typing import Generator

import pytest
from typer.testing import CliRunner

from maya.main import app


@pytest.fixture
def runner() -> CliRunner:
    """Provide a CLI runner for testing."""
    return CliRunner()


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary directory for project testing."""
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(Path.cwd())


def test_init_command(runner: CliRunner, temp_project_dir: Path) -> None:
    """Test the init command creates a project structure."""
    project_name = "test_project"
    result = runner.invoke(app, ["init", project_name])
    assert result.exit_code == 0
    assert "Project created successfully" in result.stdout
    
    # Check that the directory was created
    project_dir = temp_project_dir / project_name
    assert project_dir.exists()
    
    # Check main directories
    assert (project_dir / "src").exists()
    assert (project_dir / "tests").exists()
    assert (project_dir / ".github").exists()
    
    # Check main files
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "justfile").exists()
    assert (project_dir / ".pre-commit-config.yaml").exists()


def test_init_with_uv(runner: CliRunner, temp_project_dir: Path) -> None:
    """Test the init command with uv package manager."""
    project_name = "uv_project"
    result = runner.invoke(app, ["init", project_name, "--package-manager", "uv"])
    assert result.exit_code == 0
    
    # Check that UV info is displayed
    assert "UV Package Manager" in result.stdout
    
    # Check justfile for uv commands
    justfile_path = temp_project_dir / project_name / "justfile"
    assert justfile_path.exists()
    
    with open(justfile_path, "r") as f:
        content = f.read()
        assert "uv pip install" in content


def test_version_command(runner: CliRunner) -> None:
    """Test the version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "Maya CLI" in result.stdout 