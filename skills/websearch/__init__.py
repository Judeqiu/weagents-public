"""
Websearch Skill - Professional Brave Search API Client

A robust, flexible web search solution with natural language control,
intelligent caching, and multiple output formats.

Features:
- Natural language query parsing
- Intelligent result caching
- Robust retry logic
- Multiple output formats
- Proxy support
- User agent rotation

Example:
    >>> from websearch import BraveSearchClient, SearchConfig
    >>> client = BraveSearchClient()
    >>> results = client.natural_search("show me images of cats")
    >>> print(f"Found {results['total_results']} results")

Version: 2.0.0
"""

from .search import (
    BraveSearchClient,
    SearchConfig,
    QueryParser,
    ResultCache,
    format_text_output,
    format_markdown_output,
    format_csv_output,
)

__version__ = "2.0.0"
__author__ = "OpenClaw"
__all__ = [
    "BraveSearchClient",
    "SearchConfig", 
    "QueryParser",
    "ResultCache",
    "format_text_output",
    "format_markdown_output",
    "format_csv_output",
]
