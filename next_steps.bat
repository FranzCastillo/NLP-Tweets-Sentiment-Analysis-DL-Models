@echo off
echo ==========================================
echo Version Bump Complete: 0.1.2
echo ==========================================
echo.

echo Files updated:
echo - pipeline/__init__.py
echo - pipeline/pyproject.toml
echo - pipeline/README.md
echo.

echo ==========================================
echo Publishing to PyPI (Production)
echo ==========================================
echo.

echo RECOMMENDED: Create a GitHub Release
echo -------------------------------------
echo 1. Commit and push your changes:
echo    git add .
echo    git commit -m "Release version 0.1.2"
echo    git push origin mlops
echo.
echo 2. Go to GitHub:
echo    https://github.com/FranzCastillo/NLP-Tweets-Sentiment-Analysis-DL-Models/releases/new
echo.
echo 3. Create new release:
echo    - Tag: v0.1.2
echo    - Title: Release 0.1.2
echo    - Description: Second test release for PyPI publishing
echo    - Click "Publish release"
echo.
echo This will trigger the workflow to publish to PyPI!
echo.

echo ==========================================
echo ALTERNATIVE: Use Git Tag
echo ==========================================
echo.
echo   git add .
echo   git commit -m "Release version 0.1.2"
echo   git tag v0.1.2
echo   git push origin mlops
echo   git push origin v0.1.2
echo.
echo This will publish to BOTH TestPyPI and PyPI.
echo.

echo ==========================================
echo After Publishing
echo ==========================================
echo.
echo Install from PyPI:
echo   pip install nlp-sentiment-pipeline
echo.
echo Or from TestPyPI:
echo   pip install --index-url https://test.pypi.org/simple/ nlp-sentiment-pipeline
echo.

pause

