"""
Test script to verify package structure and imports.
Run this before publishing to ensure everything is properly configured.
"""

def test_package_structure():
    """Test that all subpackages can be imported."""
    print("Testing package structure...\n")

    try:
        # Test main package import
        import pipeline
        print(f"✓ Main package imported successfully")
        print(f"  Version: {pipeline.__version__}")
        print(f"  Author: {pipeline.__author__}\n")

        # Test subpackage imports
        from pipeline import data_preparation
        print("✓ data_preparation subpackage imported")

        from pipeline import modeling
        print("✓ modeling subpackage imported")

        from pipeline import evaluation
        print("✓ evaluation subpackage imported\n")

        # Test individual module imports
        from pipeline.data_preparation import DataExtractor, TextPreprocessor, DataSplitter
        print("✓ data_preparation modules imported:")
        print("  - DataExtractor")
        print("  - TextPreprocessor")
        print("  - DataSplitter\n")

        from pipeline.modeling import BaselineModel, TfidfVectorizerWrapper
        print("✓ modeling modules imported:")
        print("  - BaselineModel")
        print("  - TfidfVectorizerWrapper\n")

        from pipeline.evaluation import ModelEvaluator
        print("✓ evaluation modules imported:")
        print("  - ModelEvaluator\n")

        print("=" * 60)
        print("All package imports successful! ✓")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_package_metadata():
    """Test package metadata."""
    print("\nTesting package metadata...\n")

    try:
        import pipeline

        metadata = {
            'Version': pipeline.__version__,
            'Author': pipeline.__author__,
            'Email': pipeline.__email__,
            'Subpackages': ', '.join(pipeline.__all__[:-1])
        }

        for key, value in metadata.items():
            print(f"{key}: {value}")

        print("\n✓ Metadata check complete")
        return True

    except Exception as e:
        print(f"✗ Metadata check failed: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("PIPELINE PACKAGE VERIFICATION")
    print("=" * 60 + "\n")

    success = True
    success = test_package_structure() and success
    success = test_package_metadata() and success

    print("\n" + "=" * 60)
    if success:
        print("ALL TESTS PASSED ✓")
        print("Package is ready for publishing!")
    else:
        print("SOME TESTS FAILED ✗")
        print("Please fix the issues before publishing.")
    print("=" * 60 + "\n")
