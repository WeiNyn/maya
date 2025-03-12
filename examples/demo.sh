#!/bin/bash
# This script demonstrates the usage of the Maya CLI tool

# Create directory for demo
mkdir -p demo
cd demo

echo "========================================"
echo "🔍 Maya - Python Project Initializer CLI"
echo "========================================"
echo

# Show help
echo "📋 Showing available commands:"
maya --help
echo

# Create a project with pip
echo "🚀 Creating a project with pip (default):"
maya init my_project --author "Demo User" --email "demo@example.com" --github "demouser"
echo

# Create a project with uv
echo "🚀 Creating a project with uv package manager:"
maya init uv_project --package-manager uv --python-version 3.10 --author "Demo User" --email "demo@example.com" --github "demouser"
echo

# Examine the uv project
echo "📄 Examining the uv project's justfile:"
cat uv_project/justfile
echo

echo "✅ Demo completed! Created projects:"
echo "  - my_project (with pip)"
echo "  - uv_project (with uv)"
echo
echo "Try them out with: cd my_project && just setup-dev" 