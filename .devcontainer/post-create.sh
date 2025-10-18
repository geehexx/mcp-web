#!/bin/bash
# Post-create script for mcp-web devcontainer
# This script runs after the container is created to set up the development environment

set -e  # Exit on error

echo "🚀 Setting up mcp-web development environment..."

# Install project dependencies with uv
echo "📦 Installing project dependencies..."
uv sync --all-extras

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
uv run playwright install chromium

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
uv run pre-commit install

# Create cache directories if they don't exist
echo "📁 Creating cache directories..."
mkdir -p ~/.cache/mcp-web
mkdir -p ~/.cache/pytest
mkdir -p ~/.cache/uv

# Display environment info
echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "📊 Environment information:"
echo "  - Python: $(uv run python --version)"
echo "  - uv: $(uv --version)"
echo "  - Task: $(task --version)"
echo ""
echo "🎯 Quick start commands:"
echo "  - task test:fast       # Run fast tests"
echo "  - task lint           # Run linting"
echo "  - task test:coverage  # Run tests with coverage"
echo "  - task --list         # List all available commands"
echo ""
echo "📚 See README.md and CONTRIBUTING.md for more information"
echo ""
