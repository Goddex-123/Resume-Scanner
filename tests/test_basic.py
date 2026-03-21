import pytest
import sys
import os

def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        import resume_scanner
    except ImportError as e:
        pytest.fail(f"Failed to import module: {e}")

def test_directory_structure():
    """Test that critical directories exist."""
    required_dirs = [
        'resume_scanner',
        'data',
        'samples'
    ]
    for d in required_dirs:
        assert os.path.isdir(d), f"Directory {d} is missing"

def test_files_exist():
    """Test that critical files exist."""
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md'
    ]
    for f in required_files:
        assert os.path.isfile(f), f"File {f} is missing"
