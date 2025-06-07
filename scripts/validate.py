#!/usr/bin/env python3
"""
Validation script for the Kipu API Python package
Ensures all components are properly configured before publishing
"""

import ast
import os
import sys
from pathlib import Path
from typing import List, Tuple


def check_file_exists(path: str) -> bool:
    """Check if a file exists"""
    return Path(path).exists()


def check_required_files() -> List[str]:
    """Check that all required files exist"""
    required_files = [
        "setup.py",
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "MANIFEST.in",
        "requirements.txt",
        "CHANGELOG.md",
        "kipu/__init__.py",
        "kipu/client.py",
        "kipu/auth.py",
        "kipu/flattener.py",
        "kipu/base_client.py",
        "kipu/exceptions.py",
        "kipu/cli.py",
        "tests/__init__.py",
    ]

    missing = []
    for file_path in required_files:
        if not check_file_exists(file_path):
            missing.append(file_path)

    return missing


def get_version_from_init() -> str:
    """Extract version from __init__.py"""
    try:
        with open("kipu/__init__.py", "r") as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__version__":
                        if isinstance(node.value, ast.Constant):
                            return node.value.value
                        elif isinstance(node.value, ast.Str):  # Python < 3.8
                            return node.value.s
    except Exception as e:
        print(f"Error reading version: {e}")

    return None


def check_version_consistency() -> List[str]:
    """Check that version is consistent across files"""
    errors = []
    version = get_version_from_init()

    if not version:
        errors.append("Could not extract version from __init__.py")
        return errors

    # Check setup.py
    try:
        with open("setup.py", "r") as f:
            setup_content = f.read()
            if f'version="{version}"' not in setup_content:
                errors.append(f"setup.py version doesn't match __init__.py ({version})")
    except Exception:
        errors.append("Could not read setup.py")

    return errors


def check_imports() -> List[str]:
    """Check that all imports work correctly"""
    errors = []

    try:
        # Add the package to path
        sys.path.insert(0, os.path.abspath("."))

        # Try importing main components
        # Check that version is accessible
        from kipu import JsonFlattener, KipuClient, __version__
        from kipu.auth import KipuAuth
        from kipu.cli import main as cli_main
        from kipu.exceptions import KipuAPIError

        if not __version__:
            errors.append("__version__ is not set")

    except ImportError as e:
        errors.append(f"Import error: {e}")
    except Exception as e:
        errors.append(f"Unexpected error during import: {e}")

    return errors


def check_cli_entry_point() -> List[str]:
    """Check that CLI entry point is properly configured"""
    errors = []

    try:
        # Check setup.py has entry point
        with open("setup.py", "r") as f:
            setup_content = f.read()
            if "kipu-cli=kipu.cli:main" not in setup_content:
                errors.append("CLI entry point not found in setup.py")

        # Check pyproject.toml has entry point
        with open("pyproject.toml", "r") as f:
            pyproject_content = f.read()
            if "kipu-cli" not in pyproject_content:
                errors.append("CLI entry point not found in pyproject.toml")

    except Exception as e:
        errors.append(f"Error checking entry points: {e}")

    return errors


def check_package_metadata() -> List[str]:
    """Check package metadata consistency"""
    errors = []

    required_metadata = [
        ("name", "kipu-python"),
        ("description", "comprehensive Python library"),
        ("author", "Rahul"),
        ("license", "MIT"),
    ]

    try:
        with open("setup.py", "r") as f:
            setup_content = f.read()

        for key, expected in required_metadata:
            if expected.lower() not in setup_content.lower():
                errors.append(f"Missing or incorrect {key} in setup.py")

    except Exception as e:
        errors.append(f"Error reading setup.py metadata: {e}")

    return errors


def main():
    """Run all validation checks"""
    print("🧪 Kipu API Python Package Validation")
    print("=" * 50)

    all_errors = []

    # Check required files
    print("📁 Checking required files...")
    missing_files = check_required_files()
    if missing_files:
        all_errors.extend([f"Missing file: {f}" for f in missing_files])
    else:
        print("✅ All required files present")

    # Check version consistency
    print("\n🔢 Checking version consistency...")
    version_errors = check_version_consistency()
    if version_errors:
        all_errors.extend(version_errors)
    else:
        version = get_version_from_init()
        print(f"✅ Version consistent: {version}")

    # Check imports
    print("\n📦 Checking imports...")
    import_errors = check_imports()
    if import_errors:
        all_errors.extend(import_errors)
    else:
        print("✅ All imports working")

    # Check CLI entry point
    print("\n⌨️  Checking CLI entry point...")
    cli_errors = check_cli_entry_point()
    if cli_errors:
        all_errors.extend(cli_errors)
    else:
        print("✅ CLI entry point configured")

    # Check package metadata
    print("\n📋 Checking package metadata...")
    metadata_errors = check_package_metadata()
    if metadata_errors:
        all_errors.extend(metadata_errors)
    else:
        print("✅ Package metadata looks good")

    # Summary
    print("\n" + "=" * 50)
    if all_errors:
        print("❌ VALIDATION FAILED")
        print("\nErrors found:")
        for error in all_errors:
            print(f"  • {error}")
        sys.exit(1)
    else:
        print("🎉 ALL VALIDATIONS PASSED!")
        print("\nPackage is ready for publication to PyPI!")
        print("\nNext steps:")
        print("  1. Run tests: make test")
        print("  2. Build package: make build")
        print("  3. Publish: make upload")


if __name__ == "__main__":
    main()
