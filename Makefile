ifeq ($(OS),Windows_NT)
CLEAN_CMD = \
	for /d %%D in (build dist *.egg-info .pytest_cache htmlcov) do if exist %%D rmdir /s /q %%D && \
	if exist .coverage del /f /q .coverage && \
	for /r %%F in (*.pyc) do del /f /q "%%F" && \
	for /r %%D in (__pycache__) do rmdir /s /q "%%D"
else
CLEAN_CMD = \
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/ && \
	find . -type d -name __pycache__ -delete && \
	find . -type f -name "*.pyc" -delete
endif

.PHONY: help install install-dev test lint format security clean build upload docs version changelog bump-patch bump-minor bump-major release-prep

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install the package
	pip install .

install-dev:  ## Install development dependencies
	pip install -e ".[dev,docs]"

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ -v --cov=kipu --cov-report=html --cov-report=term

lint:  ## Run linting
	flake8 kipu tests
	isort --check-only kipu tests
	black --check kipu tests

format:  ## Format code
	isort kipu tests
	black kipu tests

# type-check:  ## Run type checking
# 	mypy kipu

security:  ## Run security checks
	safety check
	bandit -r kipu

clean:  ## Clean build artifacts
	@$(CLEAN_CMD)

build:  ## Build the package
	python -m build

check-build:  ## Check the built package
	twine check dist/*

upload-test:  ## Upload to Test PyPI
	twine upload --repository testpypi dist/*

upload:  ## Upload to PyPI
	twine upload dist/*

docs:  ## Build documentation
	sphinx-build -M html docs docs/_build

docs-serve:  ## Serve documentation locally
	cd docs && make livehtml

all: clean install-dev lint security test build check-build  ## Run all checks and build

ci: lint security test  ## Run CI checks

# ===== Automation Commands =====

version:  ## Show current version
	@python -c "from kipu import __version__; print(f'Current version: {__version__}')"

changelog:  ## Sync CHANGELOG.md to docs/changelog.rst
	python scripts/sync_changelog.py

bump-patch:  ## Bump patch version (0.0.2 → 0.0.3)
	python scripts/bump_version.py patch

bump-minor:  ## Bump minor version (0.0.2 → 0.1.0)
	python scripts/bump_version.py minor

bump-major:  ## Bump major version (0.0.2 → 1.0.0)
	python scripts/bump_version.py major

release-prep: changelog docs  ## Prepare for release
	@echo "✅ Release preparation complete!"
	@echo "📝 Next steps:"
	@echo "   1. Review CHANGELOG.md"
	@echo "   2. git commit -am 'chore: prepare release'"
	@echo "   3. git tag v$$(python -c 'from kipu import __version__; print(__version__)')"
	@echo "   4. git push --tags"

