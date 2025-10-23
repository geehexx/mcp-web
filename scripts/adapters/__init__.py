"""Adapter system for unified IDE configuration generation.

This module provides adapters to transform unified format configurations
into IDE-specific formats for both Cursor and Windsurf.
"""

from .cursor_adapter import CursorAdapter
from .unified_parser import UnifiedParser
from .validator import Validator
from .windsurf_adapter import WindsurfAdapter

__all__ = [
    "UnifiedParser",
    "CursorAdapter",
    "WindsurfAdapter",
    "Validator",
]
