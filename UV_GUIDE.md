# Quick Start Guide: Using UV with kipu-python

## What is UV?
UV is a **blazingly fast** Python package installer and resolver, written in Rust.
- 🚀 **10-100x faster** than pip
- 🔒 **Better dependency resolution** than pip
- 📦 **Drop-in replacement** for pip/pip-tools/virtualenv
- ⚡ **Instant** virtual environment creation

## Installation

### Install UV
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

## How UV Works with kipu-python

UV reads project metadata from **`pyproject.toml`** (PEP 621 standard).

- **`pyproject.toml`** - Main project config (name, version, dependencies)

The version is dynamically read from `kipu/__init__.py` via `pyproject.toml`.

## Usage

### Development Setup (UV way)
```bash
# Clone the repo
git clone https://github.com/Rahulkumar010/kipu-python.git
cd kipu-python

# Create virtual environment and install deps (FAST!)
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install project in editable mode with dev dependencies
uv pip install -e ".[dev]"
```

### Speed Comparison
```bash
# Traditional pip (30-60 seconds)
pip install -e ".[dev]"

# With UV (2-5 seconds! ⚡)
uv pip install -e ".[dev]"
```

### Common Commands

```bash
# Install dependencies
uv pip install -r requirements.txt

# Install with extras
uv pip install -e ".[dev,docs]"

# Sync dependencies (like pip-sync)
uv pip sync requirements.txt

# Compile requirements
uv pip compile pyproject.toml -o requirements.txt

# Update all packages
uv pip install --upgrade -e ".[dev]"
```

### UV + Pre-commit
```bash
# Install pre-commit hooks (still use regular pre-commit)
pre-commit install

# But install pre-commit itself with UV
uv pip install pre-commit
```

### Testing with UV
```bash
# Install test dependencies
uv pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=kipu --cov-report=term-missing
```

### Building Docs with UV
```bash
# Install docs dependencies
uv pip install -e ".[docs]"

# Build docs
cd docs && make html
```

## Why UV for kipu-python?

### Traditional Workflow:
```bash
$ time pip install -e ".[dev]"
# ... 45 seconds later ...
```

### With UV:
```bash
$ time uv pip install -e ".[dev]"
# ... 3 seconds later! ✨
```

### Benefits for Contributors:
- ⚡ **Faster CI/CD**: GitHub Actions complete 10x faster
- 🔄 **Quick iterations**: Install → test → debug cycles are instant
- 💾 **Better caching**: UV's cache is more efficient
- 🎯 **Reproducible builds**: Better dependency resolution

## Integration with Existing Tools

UV works seamlessly with:
- ✅ pip (drop-in replacement)
- ✅ pyproject.toml (reads project config)
- ✅ requirements.txt (compatible)
- ✅ virtualenv (creates venvs faster)
- ✅ GitHub Actions (just replace pip with uv pip)

## Makefile Integration

We've updated the Makefile to support UV:

```bash
# Use traditional pip
make test

# Or use UV directly for speed
uv pip install -e ".[dev]" && pytest
```

## CI/CD with UV

Update `.github/workflows/ci.yml`:

```yaml
- name: Install dependencies
  run: |
    pip install uv  # Install UV first
    uv pip install -e ".[dev]"  # Then use it!
```

This makes CI **5-10x faster**! ⚡

## Recommended Workflow

```bash
# 1. Daily development
uv pip install -e ".[dev]"  # Fast install
make test                    # Run tests

# 2. Before commit
make format                  # Auto-format
make lint                    # Check code

# 3. Releasing
make bump-patch              # Bump version
make release-prep            # Sync docs
git push --tags              # CI handles the rest
```

## Windows Troubleshooting

### `make release-prep` Sphinx Error

On Windows CMD, you may see this error:
```
Sphinx error:
Builder name release-prep not registered or available through entry point
```

**Cause**: Windows CMD doesn't handle nested Makefile calls correctly.

**Solution**: Run the commands separately:
```bash
# Step 1: Sync changelog
python scripts/sync_changelog.py

# Step 2: Build docs
sphinx-build -M html docs docs/_build
```

### m2r2 Not Found

If you get `ModuleNotFoundError: No module named 'm2r2'`:
```bash
uv pip install m2r2
```

### Encoding Errors

If you see `UnicodeDecodeError` on Windows, ensure your files are saved as UTF-8.

## Learn More

- UV Docs: https://github.com/astral-sh/uv
- UV Guide: https://astral.sh/blog/uv
- Benchmarks: https://github.com/astral-sh/uv#benchmarks
