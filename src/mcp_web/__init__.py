"""MCP Web - MCP Server for Web Operations.

Provides intelligent URL summarization, content extraction, and web scraping capabilities.
"""

from importlib.metadata import version

__version__ = version("mcp-web")  # Single source of truth from pyproject.toml

from mcp_web.config import Config, load_config
from mcp_web.mcp_server import create_server

__all__ = ["Config", "load_config", "create_server", "__version__"]
