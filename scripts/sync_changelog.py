#!/usr/bin/env python
"""
Sync CHANGELOG.md to docs/changelog.rst using m2r2
Converts markdown changelog to reStructuredText format for Sphinx

Requirements: uv pip install m2r2  (or pip install m2r2)
"""
from pathlib import Path
import subprocess
import sys


def convert_md_to_rst():
    """Convert CHANGELOG.md to docs/changelog.rst using m2r2"""
    changelog_md = Path('CHANGELOG.md')
    changelog_rst = Path('docs/changelog.rst')
    
    if not changelog_md.exists():
        print("❌ CHANGELOG.md not found")
        return False
    
    # Check if m2r2 is installed
    try:
        import m2r2
    except ImportError:
        print("❌ m2r2 not installed.")
        print("   Install with: uv pip install m2r2")
        print("   Or add to dev dependencies: pip install -e \".[dev]\"")
        return False
    
    # Convert using m2r2
    try:
        subprocess.check_call([
            sys.executable, "-m", "m2r2",
            str(changelog_md),
            "--overwrite"
        ])
        
        # m2r2 creates CHANGELOG.rst, move it to docs/
        generated_rst = Path('CHANGELOG.rst')
        if generated_rst.exists():
            # Read and update the content
            content = generated_rst.read_text(encoding='utf-8')
            
            # Add proper header if not present
            if not content.startswith('Changelog\n========='):
                header = "Changelog\n=========\n\n"
                content = header + content
            
            # Write to docs/
            changelog_rst.write_text(content, encoding='utf-8')
            
            # Clean up
            generated_rst.unlink()
            
            print(f"✅ Synced CHANGELOG.md → docs/changelog.rst")
            return True
        else:
            print("❌ m2r2 conversion failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running m2r2: {e}")
        return False


if __name__ == '__main__':
    convert_md_to_rst()
