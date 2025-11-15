# Publishing to PyPI

This guide walks you through publishing the `nlp-sentiment-pipeline` package to PyPI.

## Prerequisites

1. **Create PyPI Account**
   - Go to [https://pypi.org/](https://pypi.org/) and create an account
   - Go to [https://test.pypi.org/](https://test.pypi.org/) for testing (recommended first)

2. **Install Required Tools**
   ```bash
   pip install --upgrade pip setuptools wheel twine build
   ```

3. **Configure PyPI Credentials**
   Create a `~/.pypirc` file:
   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-YourAPITokenHere

   [testpypi]
   username = __token__
   password = pypi-YourTestAPITokenHere
   ```

## Pre-Publishing Checklist

- [ ] Update version number in `pyproject.toml`, `setup.py`, and `__init__.py`
- [ ] Update `README.md` with accurate information
- [ ] Update `LICENSE` with correct year and author
- [ ] Ensure all tests pass
- [ ] Update `CHANGELOG.md` or add version info to README
- [ ] Replace placeholder values (author name, email, GitHub URLs)

## Building the Package

### Method 1: Using `build` (Recommended)

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build the package
python -m build
```

### Method 2: Using `setup.py`

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build source distribution and wheel
python setup.py sdist bdist_wheel
```

This creates:
- `dist/nlp-sentiment-pipeline-0.1.0.tar.gz` (source distribution)
- `dist/nlp_sentiment_pipeline-0.1.0-py3-none-any.whl` (wheel)

## Testing the Build Locally

```bash
# Install in editable mode
pip install -e .

# Or install from the built wheel
pip install dist/nlp_sentiment_pipeline-0.1.0-py3-none-any.whl
```

Test the installation:
```python
import pipeline
from pipeline.data_preparation import DataExtractor
from pipeline.modeling import BaselineModel
from pipeline.evaluation import ModelEvaluator

print(pipeline.__version__)
```

## Publishing to Test PyPI (Recommended First)

```bash
# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps nlp-sentiment-pipeline
```

## Publishing to PyPI

```bash
# Upload to PyPI
python -m twine upload dist/*
```

Or upload specific files:
```bash
python -m twine upload dist/nlp-sentiment-pipeline-0.1.0*
```

## Verify Publication

Visit your package page:
- PyPI: `https://pypi.org/project/nlp-sentiment-pipeline/`
- Test PyPI: `https://test.pypi.org/project/nlp-sentiment-pipeline/`

## Installing the Published Package

```bash
pip install nlp-sentiment-pipeline
```

## Updating the Package

1. Make your changes
2. Update version numbers (follow [Semantic Versioning](https://semver.org/))
3. Update changelog
4. Rebuild: `python -m build`
5. Upload: `python -m twine upload dist/*`

## Common Issues

### "File already exists"
- You can't overwrite an existing version on PyPI
- Increment the version number and rebuild

### Import errors
- Check package structure with `python -m tarfile -l dist/*.tar.gz`
- Verify `__init__.py` files exist in all subpackages

### Missing dependencies
- Ensure all dependencies are listed in `requirements.txt` and `pyproject.toml`

## Best Practices

1. **Always test on Test PyPI first**
2. **Use semantic versioning**: MAJOR.MINOR.PATCH
3. **Tag releases in Git**: `git tag v0.1.0 && git push --tags`
4. **Keep a changelog**: Document changes between versions
5. **Use GitHub Actions**: Automate building and publishing

## GitHub Actions Example

Create `.github/workflows/publish.yml`:
```yaml
name: Publish to PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

## Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)

