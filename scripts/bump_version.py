#!/usr/bin/env python
"""
Bump version and update changelog
Usage:
    python scripts/bump_version.py patch  # 0.0.2 → 0.0.3
    python scripts/bump_version.py minor  # 0.0.2 → 0.1.0
    python scripts/bump_version.py major  # 0.0.2 → 1.0.0
"""
import re
import sys
from datetime import date
from pathlib import Path


def bump_version(part='patch'):
    """Bump version and update changelog"""
    # Read current version from __init__.py
    init_file = Path('kipu/__init__.py')
    content = init_file.read_text()
    
    current = re.search(r'__version__ = "(\d+)\.(\d+)\.(\d+)"', content)
    if not current:
        print("❌ Could not find version in kipu/__init__.py")
        return None
    
    major, minor, patch = map(int, current.groups())
    
    # Bump version
    if part == 'major':
        major += 1
        minor = 0
        patch = 0
    elif part == 'minor':
        minor += 1
        patch = 0
    elif part == 'patch':
        patch += 1
    else:
        print(f"❌ Invalid part: {part}. Use: major, minor, or patch")
        return None
    
    new_version = f"{major}.{minor}.{patch}"
    old_version = f"{current.group(1)}.{current.group(2)}.{current.group(3)}"
    
    # Update __init__.py
    new_content = re.sub(
        r'__version__ = ".*"',
        f'__version__ = "{new_version}"',
        content
    )
    init_file.write_text(new_content)
    
    # Add to CHANGELOG.md
    today = date.today().isoformat()
    changelog_entry = f"""## [{new_version}] - {today}

### Added
- 

### Changed
- 

### Fixed
- 

---

"""
    
    changelog_file = Path('CHANGELOG.md')
    changelog = changelog_file.read_text()
    
    # Insert after the header (before first version entry)
    header_end = changelog.find('## [')
    if header_end == -1:
        print("❌ Could not find version entries in CHANGELOG.md")
        return None
    
    new_changelog = changelog[:header_end] + changelog_entry + changelog[header_end:]
    changelog_file.write_text(new_changelog)
    
    print(f"✅ Bumped version: {old_version} → {new_version}")
    print(f"✅ Updated kipu/__init__.py")
    print(f"✅ Added changelog template for {new_version}")
    print(f"\n📝 Next steps:")
    print(f"   1. Edit CHANGELOG.md and fill in the changes")
    print(f"   2. Run: python scripts/sync_changelog.py")
    print(f"   3. Commit: git commit -am 'chore: bump version to {new_version}'")
    print(f"   4. Tag: git tag v{new_version}")
    print(f"   5. Push: git push --tags")
    
    return new_version


if __name__ == '__main__':
    part = sys.argv[1] if len(sys.argv) > 1 else 'patch'
    bump_version(part)
