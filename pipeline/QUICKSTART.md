# Quick Start Guide

## Testing the Package Locally

Before publishing to PyPI, test the package locally:

### 1. Install in Development Mode

```bash
cd D:\UVG\NLP\NLP-Tweets-Sentiment-Analysis-DL-Models\pipeline
pip install -e .
```

### 2. Run the Test Script

```bash
python test_package.py
```

### 3. Test Imports

```python
from pipeline.data_preparation import DataExtractor, TextPreprocessor
from pipeline.modeling import BaselineModel
from pipeline.evaluation import ModelEvaluator
```

## Building the Package

### Install Build Tools

```bash
pip install --upgrade build twine
```

### Build Distribution

```bash
# Clean previous builds
rmdir /s /q build dist *.egg-info

# Build the package
python -m build
```

This creates:
- `dist/nlp-sentiment-pipeline-0.1.0.tar.gz`
- `dist/nlp_sentiment_pipeline-0.1.0-py3-none-any.whl`

## Publishing to PyPI

### Test on TestPyPI First

```bash
python -m twine upload --repository testpypi dist/*
```

### Publish to PyPI

```bash
python -m twine upload dist/*
```

## After Publishing

Users can install with:
```bash
pip install nlp-sentiment-pipeline
```

## Notes

- Remember to update version numbers in:
  - `pyproject.toml`
  - `setup.py`
  - `pipeline/__init__.py`
- Update author name and email
- Update GitHub repository URLs

