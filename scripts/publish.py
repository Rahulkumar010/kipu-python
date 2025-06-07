#!/usr/bin/env python3

# Kipu API Python library Publishing Script
# This script helps publish the package to PyPI

import os
import shutil
import subprocess
import sys


def run(cmd, check=True, capture_output=False, text=True):
    return subprocess.run(
        cmd, shell=True, check=check, capture_output=capture_output, text=text
    )


def confirm(prompt):
    resp = input(prompt + " (y/N): ").strip().lower()
    return resp == "y"


def main():
    print("🏥 Kipu API Python library Publishing Script")
    print("==================================")

    # Check for setup.py and pyproject.toml
    if not (os.path.isfile("setup.py") and os.path.isfile("pyproject.toml")):
        print("❌ Error: setup.py or pyproject.toml not found")
        print("   Please run this script from the package root directory")
        sys.exit(1)

    # Check for python and git
    if shutil.which("python") is None:
        print("❌ Python is required but not installed")
        sys.exit(1)
    if shutil.which("git") is None:
        print("❌ Git is required but not installed")
        sys.exit(1)

    # Get version from package
    try:
        version = run(
            'python -c "from kipu import __version__; print(__version__)"',
            capture_output=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        print("❌ Failed to get version from package")
        sys.exit(1)

    print(f"📦 Package version: {version}")

    # Check if version exists on PyPI
    print("🔍 Checking if version exists on PyPI...")
    try:
        versions_output = run(
            "pip index versions kipu-python", capture_output=True
        ).stdout
    except subprocess.CalledProcessError:
        versions_output = ""
    if version in versions_output:
        print(f"❌ Version {version} already exists on PyPI")
        print("   Please bump the version number before publishing")
        sys.exit(1)

    # Check git status
    status = run("git status --porcelain", capture_output=True).stdout.strip()
    if status:
        print("⚠️  Warning: You have uncommitted changes")
        if not confirm("Do you want to continue?"):
            print("Aborting...")
            sys.exit(1)

    # Check current git branch
    current_branch = run(
        "git branch --show-current", capture_output=True
    ).stdout.strip()
    if current_branch != "main":
        print(f"⚠️  Warning: You're not on the main branch (current: {current_branch})")
        if not confirm("Do you want to continue?"):
            print("Aborting...")
            sys.exit(1)

    # Final confirmation before publishing
    print(f"🚀 Ready to publish kipu-python version {version}")
    print("   This will:")
    print("   1. Run tests and quality checks")
    print("   2. Build the package")
    print("   3. Upload to PyPI\n")

    if not confirm("Continue?"):
        print("Aborting...")
        sys.exit(1)

    # Install build dependencies
    print("📥 Installing build dependencies...")
    run("pip install --upgrade build twine")

    # Run tests and quality checks
    print("🧪 Running tests and quality checks...")

    if shutil.which("make"):
        run("make ci")
    else:
        print("   Running individual checks...")

        try:
            print("   - Linting...")
            subprocess.run("flake8 kipu tests", shell=True, check=True)

            print("   - Format check...")
            subprocess.run("black --check kipu tests", shell=True, check=True)

            print("   - Import order check...")
            subprocess.run("isort --check-only kipu tests", shell=True, check=True)

            print("   - Type checking...")
            subprocess.run("mypy kipu", shell=True, check=True)

            print("   - Running tests...")
            subprocess.run("pytest tests/", shell=True, check=True)

        except subprocess.CalledProcessError as e:
            cmd_name = e.cmd if isinstance(e.cmd, str) else " ".join(e.cmd)
            error_map = {
                "flake8": "❌ Linting failed",
                "black": "❌ Format check failed",
                "isort": "❌ Import order check failed",
                "mypy": "❌ Type checking failed",
                "pytest": "❌ Tests failed",
            }
            # Find which error message to show based on command invoked
            error_message = next(
                (msg for tool, msg in error_map.items() if tool in cmd_name),
                "❌ Step failed",
            )
            print(error_message)
            sys.exit(1)

    print("✅ All checks passed!")

    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    for path in ("build", "dist"):
        if os.path.isdir(path):
            shutil.rmtree(path)
    for item in os.listdir("."):
        if item.endswith(".egg-info") and os.path.isdir(item):
            shutil.rmtree(item)

    # Build package
    print("🔨 Building package...")
    run("python -m build")

    # Check package
    print("🔍 Checking package...")
    run("twine check dist/*")

    # Final confirmation before upload
    print("📤 Ready to upload to PyPI")
    if not confirm("Upload now?"):
        print("Build completed but not uploaded")
        print("To upload later, run: twine upload dist/*")
        sys.exit(0)

    # Upload to PyPI
    print("🚀 Uploading to PyPI...")
    run("twine upload dist/*")

    print(f"🎉 Successfully published kipu-python version {version} to PyPI!")
    print(f"   Package URL: https://pypi.org/project/kipu-python/{version}/")
    print(f"   Install with: pip install kipu-python=={version}")

    # Create git tag if not exists
    existing_tags = run("git tag -l", capture_output=True).stdout.splitlines()
    tag_name = f"v{version}"
    if tag_name not in existing_tags:
        print("🏷️  Creating git tag...")
        run(f"git tag {tag_name}")
        print(f"   To push tag: git push origin {tag_name}")

    print("✅ Publication complete!")


if __name__ == "__main__":
    main()
