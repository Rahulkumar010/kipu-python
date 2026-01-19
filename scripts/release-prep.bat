@echo off
REM Release preparation script for Windows
REM Usage: release-prep.bat

echo.
echo === Syncing Changelog ===
python scripts/sync_changelog.py
if errorlevel 1 (
    echo ERROR: Failed to sync changelog
    exit /b 1
)

echo.
echo === Building Documentation ===
sphinx-build -M html docs docs/_build
if errorlevel 1 (
    echo ERROR: Failed to build docs
    exit /b 1
)

echo.
echo ========================================
echo   Release preparation complete!
echo ========================================
echo.
echo Next steps:
echo   1. Review CHANGELOG.md
echo   2. git commit -am "chore: prepare release"
echo   3. git tag vX.X.X
echo   4. git push --tags
echo.
