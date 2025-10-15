"""Site customization for pytest parallel execution.

This file is automatically loaded by Python and enables coverage.py
to work correctly with pytest-xdist parallel execution.

Reference: https://coverage.readthedocs.io/en/latest/subprocess.html
"""

try:
    import coverage

    coverage.process_startup()
except ImportError:
    pass
