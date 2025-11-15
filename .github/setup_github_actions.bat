@echo off
echo ==========================================
echo GitHub Actions Setup Helper
echo ==========================================
echo.

echo This script will guide you through setting up GitHub Actions for automatic publishing.
echo.

echo Step 1: Get API Tokens
echo ----------------------
echo.
echo TestPyPI Token:
echo 1. Go to: https://test.pypi.org/manage/account/#api-tokens
echo 2. Click "Add API token"
echo 3. Name: github-actions-nlp-sentiment-pipeline
echo 4. Copy the token
echo.
echo PyPI Token:
echo 1. Go to: https://pypi.org/manage/account/#api-tokens
echo 2. Click "Add API token"
echo 3. Name: github-actions-nlp-sentiment-pipeline
echo 4. Copy the token
echo.
pause
echo.

echo Step 2: Add Secrets to GitHub
echo ------------------------------
echo.
echo 1. Go to: https://github.com/FranzCastillo/NLP-Tweets-Sentiment-Analysis-DL-Models/settings/secrets/actions
echo 2. Click "New repository secret"
echo 3. Add these two secrets:
echo.
echo    Secret Name: TEST_PYPI_API_TOKEN
echo    Value: (paste your TestPyPI token)
echo.
echo    Secret Name: PYPI_API_TOKEN
echo    Value: (paste your PyPI token)
echo.
pause
echo.

echo Step 3: Enable GitHub Actions
echo -----------------------------
echo.
echo 1. Go to: https://github.com/FranzCastillo/NLP-Tweets-Sentiment-Analysis-DL-Models/settings/actions
echo 2. Under "Actions permissions":
echo    - Select: Allow all actions and reusable workflows
echo 3. Under "Workflow permissions":
echo    - Select: Read and write permissions
echo    - Check: Allow GitHub Actions to create and approve pull requests
echo.
pause
echo.

echo Step 4: Commit and Push GitHub Actions
echo ---------------------------------------
echo.
echo Run these commands:
echo.
echo   git add .github
echo   git commit -m "Add GitHub Actions CI/CD workflows"
echo   git push origin mlops
echo.
pause
echo.

echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Push to mlops branch to test TestPyPI publishing
echo 2. Create a release on GitHub to publish to PyPI
echo.
echo For detailed instructions, see: .github\ACTIONS_SETUP.md
echo.
pause

