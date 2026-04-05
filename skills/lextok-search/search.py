#!/usr/bin/env python3
"""
LexTok Search - Brave Search API Client
Internet search with optional full content fetching.
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("❌ Required packages not found. Install with: pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)


class LexTokSearchClient:
    """Client for LexTok Search using Brave Search API."""
    
    BASE_URL = "https://api.search.brave.com/res/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LexTok Search client.
        
        Args:
            api_key: Brave Search API key. If not provided, will try to load from config.
        """
        self.api_key = api_key or self._load_api_key()
        if not self.api_key:
            raise ValueError(
                "Brave API key not found. Please set it in config.json or "
                "set the BRAVE_API_KEY environment variable."
            )
        
        self.session = requests.Session()
        self.session.headers.update({
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json",
        })
    
    def _load_api_key(self) -> Optional[str]:
        """Load API key from config file or environment variable."""
        # First check environment variable
        api_key = os.environ.get("BRAVE_API_KEY")
        if api_key:
            return api_key
        
        # Then check config file
        config_paths = [
            "config.json",
            os.path.join(os.path.dirname(__file__), "config.json"),
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, "r") as f:
                        config = json.load(f)
                        api_key = config.get("brave_api_key") or config.get("api_key")
                        if api_key and api_key != "YOUR_BRAVE_API_KEY_HERE":
                            return api_key
                except (json.JSONDecodeError, IOError):
                    continue
        
        return None
    
    def search(
        self,
        query: str,
        limit: int = 5,
        include_content: bool = False,
        timeout: int = 10,
    ) -> Dict:
        """
        Perform a web search.
        
        Args:
            query: Search query string
            limit: Number of results (1-20)
            include_content: Whether to fetch full page content
            timeout: Timeout for content fetching in seconds
        
        Returns:
            Dictionary containing search results
        """
        if not query.strip():
            raise ValueError("Search query cannot be empty")
        
        limit = max(1, min(20, limit))  # Clamp between 1-20
        
        # Perform Brave search
        endpoint = f"{self.BASE_URL}/web/search"
        
        params = {
            "q": query,
            "count": limit,
            "offset": 0,
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            results = self._parse_results(data, query)
            
            # Fetch content if requested
            if include_content:
                for result in results["results"]:
                    result["content"] = self._fetch_content(result["url"], timeout)
            
            return results
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid API key. Please check your Brave API key.")
            elif e.response.status_code == 429:
                raise ValueError("Rate limit exceeded. Please wait before making more requests.")
            else:
                raise ValueError(f"API error: {e.response.status_code} - {e.response.text}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request failed: {str(e)}")
    
    def _parse_results(self, data: Dict, query: str) -> Dict:
        """Parse API response into clean format."""
        results = []
        
        web_results = data.get("web", {}).get("results", [])
        for item in web_results:
            results.append({
                "title": item.get("title", "No title"),
                "url": item.get("url", ""),
                "description": item.get("description", "No description"),
                "source": item.get("profile", {}).get("name", "Unknown"),
            })
        
        return {
            "query": query,
            "total_results": len(results),
            "results": results,
        }
    
    def _fetch_content(self, url: str, timeout: int = 10) -> Optional[str]:
        """
        Fetch and extract text content from a URL.
        
        Args:
            url: URL to fetch
            timeout: Request timeout in seconds
        
        Returns:
            Extracted text content or None if failed
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
            
            response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text(separator='\n', strip=True)
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit content length
            max_length = 10000
            if len(text) > max_length:
                text = text[:max_length] + "... [content truncated]"
            
            return text
            
        except requests.exceptions.Timeout:
            return "[Content fetch timed out]"
        except requests.exceptions.RequestException as e:
            return f"[Content fetch failed: {str(e)}]"
        except Exception as e:
            return f"[Content extraction failed: {str(e)}]"


def format_text_output(data: Dict, include_content: bool = False) -> str:
    """Format search results as readable text."""
    lines = []
    lines.append(f'🔍 Results for: "{data["query"]}"')
    lines.append(f'Found: {data["total_results"]} results')
    lines.append("")
    
    if not data["results"]:
        lines.append("No results found.")
        return "\n".join(lines)
    
    for i, result in enumerate(data["results"], 1):
        lines.append(f"{'='*60}")
        lines.append(f"{i}. {result['title']}")
        lines.append(f"   URL: {result['url']}")
        lines.append(f"   Source: {result['source']}")
        lines.append("")
        lines.append(f"   Description: {result['description']}")
        
        if include_content and "content" in result:
            lines.append("")
            lines.append("   Content Preview:")
            content = result['content']
            # Show first 800 chars of content
            preview = content[:800] if len(content) <= 800 else content[:800] + "..."
            for line in preview.split('\n')[:15]:
                if line.strip():
                    lines.append(f"   > {line}")
        
        lines.append("")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="LexTok Search - Internet search with Brave API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 search.py "python tutorials"
  python3 search.py "latest news" --limit 3
  python3 search.py "product review" --include-content --limit 2
  python3 search.py "research paper" --format json --include-content
        """
    )
    
    parser.add_argument(
        "query",
        help="Search query string"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=5,
        help="Number of results (1-20, default: 5)"
    )
    parser.add_argument(
        "--include-content",
        action="store_true",
        help="Fetch full page content (consumes more tokens)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format: text or json (default: text)"
    )
    parser.add_argument(
        "--config", "-c",
        default="config.json",
        help="Path to config file (default: config.json)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Page fetch timeout in seconds (default: 10)"
    )
    
    args = parser.parse_args()
    
    try:
        client = LexTokSearchClient()
        results = client.search(
            query=args.query,
            limit=args.limit,
            include_content=args.include_content,
            timeout=args.timeout,
        )
        
        if args.format == "json":
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(format_text_output(results, include_content=args.include_content))
            
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Search cancelled.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
