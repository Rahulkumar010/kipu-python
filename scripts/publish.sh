#!/bin/bash

# Kipu API Python library Publishing Script
# This script helps publish the package to PyPI

set -e

echo "🏥 Kipu API Python library Publishing Script"
echo "=================================="

# Check if we're in the right directory
if [[ ! -f "setup.py" ]] || [[ ! -f "pyproject.toml" ]]; then
    echo "❌ Error: setup.py or pyproject.toml not found"
    echo "   Please run this script from the package root directory"
    exit 1
fi

# Check if we have required tools
command -v python >/dev/null 2>&1 || { echo "❌ Python is required but not installed"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git is required but not installed"; exit 1; }

# Get version from package
VERSION=$(python -c "from kipu import __version__; print(__version__)")
echo "📦 Package version: $VERSION"

# Check if this version already exists on PyPI
echo "🔍 Checking if version exists on PyPI..."
if pip index versions kipu-python | grep -q "$VERSION"; then
    echo "❌ Version $VERSION already exists on PyPI"
    echo "   Please bump the version number before publishing"
    exit 1
fi

# Check git status
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  Warning: You have uncommitted changes"
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborting..."
        exit 1
    fi
fi

# Check if we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
    echo "⚠️  Warning: You're not on the main branch (current: $CURRENT_BRANCH)"
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborting..."
        exit 1
    fi
fi

# Ask for confirmation
echo "🚀 Ready to publish kipu-python version $VERSION"
echo "   This will:"
echo "   1. Run tests and quality checks"
echo "   2. Build the package"
echo "   3. Upload to PyPI"
echo
read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborting..."
    exit 1
fi

# Install build dependencies
echo "📥 Installing build dependencies..."
pip install --upgrade build twine

# Run tests and quality checks
echo "🧪 Running tests and quality checks..."
if command -v make >/dev/null 2>&1; then
    make ci
else
    echo "   Running individual checks..."
    
    # Linting
    echo "   - Linting..."
    flake8 kipu tests || { echo "❌ Linting failed"; exit 1; }
    
    # Formatting
    echo "   - Format check..."
    black --check kipu tests || { echo "❌ Format check failed"; exit 1; }
    
    # Import sorting
    echo "   - Import order check..."
    isort --check-only kipu tests || { echo "❌ Import order check failed"; exit 1; }
    
    # Type checking
    echo "   - Type checking..."
    mypy kipu || { echo "❌ Type checking failed"; exit 1; }
    
    # Tests
    echo "   - Running tests..."
    pytest tests/ || { echo "❌ Tests failed"; exit 1; }
fi

echo "✅ All checks passed!"

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build package
echo "🔨 Building package..."
python -m build

# Check package
echo "🔍 Checking package..."
twine check dist/*

# Ask for final confirmation
echo "📤 Ready to upload to PyPI"
read -p "Upload now? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Build completed but not uploaded"
    echo "To upload later, run: twine upload dist/*"
    exit 0
fi

# Upload to PyPI
echo "🚀 Uploading to PyPI..."
twine upload dist/*

echo "🎉 Successfully published kipu-python version $VERSION to PyPI!"
echo "   Package URL: https://pypi.org/project/kipu-python/$VERSION/"
echo "   Install with: pip install kipu-python==$VERSION"

# Create git tag
if [[ -z $(git tag -l "v$VERSION") ]]; then
    echo "🏷️  Creating git tag..."
    git tag "v$VERSION"
    echo "   To push tag: git push origin v$VERSION"
fi

echo "✅ Publication complete!"
