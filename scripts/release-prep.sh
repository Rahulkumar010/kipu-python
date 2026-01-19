#!/bin/bash
# Release preparation script for Unix/Linux/macOS
# Usage: ./scripts/release-prep.sh

set -e

echo ""
echo "=== Syncing Changelog ==="
python scripts/sync_changelog.py

echo ""
echo "=== Building Documentation ==="
sphinx-build -M html docs docs/_build

echo ""
echo "========================================"
echo "  ✅ Release preparation complete!"
echo "========================================"
echo ""
echo "📝 Next steps:"
echo "   1. Review CHANGELOG.md"
echo "   2. git commit -am 'chore: prepare release'"
echo "   3. git tag vX.X.X"
echo "   4. git push --tags"
echo ""
