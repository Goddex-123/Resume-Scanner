import pytest
import os


def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        __import__("resume_scanner")
    except ImportError as e:
        pytest.fail(f"Failed to import module: {e}")


def test_directory_structure():
    """Test that critical directories exist."""
    required_dirs = ["resume_scanner", "data", "samples"]
    for d in required_dirs:
        assert os.path.isdir(d), f"Directory {d} is missing"


def test_files_exist():
    """Test that critical files exist."""
    required_files = ["app.py", "requirements.txt", "README.md"]
    for f in required_files:
        assert os.path.isfile(f), f"File {f} is missing"


def test_package_exports():
    """Test that all declared package exports in __all__ are accessible."""
    import resume_scanner
    for symbol in resume_scanner.__all__:
        assert hasattr(resume_scanner, symbol), f"Export {symbol} is missing from resume_scanner"
        assert getattr(resume_scanner, symbol) is not None

