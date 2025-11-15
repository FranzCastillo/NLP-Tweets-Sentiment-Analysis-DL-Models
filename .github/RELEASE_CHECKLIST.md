# Release Checklist

Use this checklist when preparing a new release of the package.

## Pre-Release

- [ ] All tests pass locally (`python test_package.py`)
- [ ] Code is merged to main/mlops branch
- [ ] All dependencies are up to date in `requirements.txt`
- [ ] Documentation is updated (README.md, docstrings)

## Version Update

- [ ] Update version in `pipeline/pyproject.toml`
- [ ] Update version in `pipeline/__init__.py`
- [ ] Update `CHANGES.md` or add release notes to README
- [ ] Update any version references in documentation

## Version Numbers

Current version: **0.1.0**

Next version should follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes (1.0.0)
- **MINOR**: New features, backward compatible (0.2.0)
- **PATCH**: Bug fixes, backward compatible (0.1.1)

## Testing

- [ ] Build package locally: `cd pipeline && python -m build`
- [ ] Check package: `twine check dist/*`
- [ ] Test installation: `pip install dist/*.whl`
- [ ] Run verification: `python test_package.py`
- [ ] Test imports work correctly

## Publishing (via GitHub Actions)

### Option A: GitHub Release (Recommended)
1. - [ ] Go to GitHub repository → Releases
2. - [ ] Click "Create a new release"
3. - [ ] Choose/create tag: `v0.x.x` (e.g., v0.1.0)
4. - [ ] Title: "Release 0.x.x" or descriptive name
5. - [ ] Description: Add release notes/changelog
6. - [ ] Click "Publish release"
7. - [ ] Monitor GitHub Actions workflow
8. - [ ] Verify on PyPI: https://pypi.org/project/nlp-sentiment-pipeline/

### Option B: Git Tag
1. - [ ] Commit all changes
2. - [ ] Create tag: `git tag v0.x.x`
3. - [ ] Push code: `git push origin mlops`
4. - [ ] Push tag: `git push origin v0.x.x`
5. - [ ] Monitor GitHub Actions workflow

## Post-Release

- [ ] Verify package on TestPyPI: https://test.pypi.org/project/nlp-sentiment-pipeline/
- [ ] Verify package on PyPI: https://pypi.org/project/nlp-sentiment-pipeline/
- [ ] Test installation from PyPI: `pip install nlp-sentiment-pipeline`
- [ ] Test that installed package works correctly
- [ ] Announce release (if applicable)

## Rollback (if needed)

If something goes wrong:
- [ ] PyPI doesn't allow deleting versions, but you can "yank" them
- [ ] Increment version and release a fix
- [ ] Update documentation with known issues

## Notes

- TestPyPI uploads happen automatically on push to main/mlops
- PyPI uploads only happen on GitHub releases or version tags
- You cannot overwrite a version once published
- Keep this checklist updated as the process evolves

