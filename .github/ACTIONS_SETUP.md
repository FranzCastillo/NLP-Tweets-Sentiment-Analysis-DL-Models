# GitHub Actions CI/CD Setup Guide

This repository uses GitHub Actions to automatically test, build, and publish the `nlp-sentiment-pipeline` package.

## Workflows Overview

### 1. `ci-cd.yml` - Main CI/CD Pipeline
**Triggers:**
- Push to `main` or `mlops` branches → Publishes to TestPyPI
- Pull requests → Runs tests only
- GitHub Release created → Publishes to PyPI

**Jobs:**
- **Test**: Runs on Python 3.8, 3.9, 3.10, 3.11
- **Build**: Creates distribution packages
- **Publish to TestPyPI**: Auto-publishes on push to main/mlops
- **Publish to PyPI**: Auto-publishes on GitHub release

### 2. `publish-on-tag.yml` - Tag-based Publishing
**Triggers:**
- Push tags matching `v*.*.*` (e.g., v0.1.0, v1.2.3)

**Actions:**
- Runs tests
- Builds package
- Publishes to TestPyPI
- Publishes to PyPI
- Creates GitHub Release with artifacts

### 3. `test-pr.yml` - Pull Request Testing
**Triggers:**
- Pull requests to `main` or `mlops`

**Actions:**
- Runs tests on multiple Python versions
- Tests package build
- Tests installation from built wheel

## Setup Instructions

### Step 1: Create API Tokens

#### For TestPyPI:
1. Go to https://test.pypi.org/manage/account/#api-tokens
2. Click "Add API token"
3. Name: `github-actions-nlp-sentiment-pipeline`
4. Scope: Entire account (or specific to your project after first upload)
5. Copy the token (starts with `pypi-`)

#### For PyPI:
1. Go to https://pypi.org/manage/account/#api-tokens
2. Click "Add API token"
3. Name: `github-actions-nlp-sentiment-pipeline`
4. Scope: Entire account (or specific to your project after first upload)
5. Copy the token

### Step 2: Add Secrets to GitHub Repository

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

   **Secret 1:**
   - Name: `TEST_PYPI_API_TOKEN`
   - Value: (paste your TestPyPI token)

   **Secret 2:**
   - Name: `PYPI_API_TOKEN`
   - Value: (paste your PyPI token)

### Step 3: Enable GitHub Actions

1. Go to **Settings** → **Actions** → **General**
2. Under "Actions permissions", select:
   - ✅ Allow all actions and reusable workflows
3. Under "Workflow permissions", select:
   - ✅ Read and write permissions
   - ✅ Allow GitHub Actions to create and approve pull requests

## Usage

### Automatic Publishing to TestPyPI

Simply push to `main` or `mlops` branch:
```bash
git add .
git commit -m "Update package"
git push origin mlops
```

The package will automatically be published to TestPyPI.

### Publishing to PyPI (Production)

#### Option 1: Create a GitHub Release
1. Go to your repository on GitHub
2. Click **Releases** → **Create a new release**
3. Click **Choose a tag** → Create new tag (e.g., `v0.1.0`)
4. Fill in release title and description
5. Click **Publish release**

The workflow will automatically publish to PyPI.

#### Option 2: Push a Git Tag
```bash
# Update version in pyproject.toml, setup.py, and pipeline/__init__.py first
git add .
git commit -m "Release v0.1.0"
git tag v0.1.0
git push origin mlops
git push origin v0.1.0
```

This triggers both TestPyPI and PyPI publishing, plus creates a GitHub Release.

### Testing Before Publishing

Create a pull request:
```bash
git checkout -b feature/my-changes
git add .
git commit -m "My changes"
git push origin feature/my-changes
```

Then create a PR on GitHub. The tests will run automatically.

## Workflow Details

### What Gets Published

- **TestPyPI**: 
  - Every push to main/mlops branches
  - Every version tag
  - URL: https://test.pypi.org/project/nlp-sentiment-pipeline/

- **PyPI**: 
  - GitHub releases only
  - Version tags (v*.*.*)
  - URL: https://pypi.org/project/nlp-sentiment-pipeline/

### Version Management

Before releasing a new version:

1. Update version in `pipeline/pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. Update version in `pipeline/__init__.py`:
   ```python
   __version__ = "0.2.0"
   ```

3. Update `CHANGES.md` or `README.md` with changelog

4. Commit and create release/tag

## Monitoring

- **View workflow runs**: Go to **Actions** tab in your GitHub repository
- **Check build status**: Each commit will show a ✅ or ❌ indicator
- **View logs**: Click on any workflow run to see detailed logs

## Troubleshooting

### "Package already exists" error
- You cannot overwrite a version on PyPI
- Increment the version number in all files
- Create a new release/tag

### Authentication failed
- Check that secrets are correctly set in GitHub
- Verify tokens are valid and not expired
- Ensure token has correct permissions

### Tests failing
- Check the workflow logs in GitHub Actions
- Run tests locally: `python test_package.py`
- Fix issues and push again

### Build artifacts
- Workflow saves built packages for 7 days
- Download from the Actions run page under "Artifacts"

## Manual Publishing (Fallback)

If you need to publish manually:

```bash
cd pipeline
python -m build
python -m twine upload --repository testpypi dist/*
python -m twine upload dist/*
```

## Best Practices

1. **Always test on TestPyPI first** before publishing to PyPI
2. **Use semantic versioning**: MAJOR.MINOR.PATCH
3. **Create tags for releases**: `git tag v0.1.0`
4. **Write release notes** when creating GitHub releases
5. **Test in a clean environment** after publishing:
   ```bash
   pip install nlp-sentiment-pipeline==0.1.0
   ```

## Security Notes

- Never commit API tokens to the repository
- Use GitHub Secrets for all credentials
- Rotate tokens periodically
- Use scoped tokens when possible (project-specific)
- Review workflow runs regularly for suspicious activity

