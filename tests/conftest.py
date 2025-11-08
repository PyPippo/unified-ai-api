"""
pytest configuration for unified_ai_api tests.

This file configures the Python path to allow imports from the src directory.
"""

import sys
from pathlib import Path

# Add src directory to Python path so we can import unified_ai_api
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))
