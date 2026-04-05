#!/usr/bin/env python3
"""
Brave Search API Client - Enhanced Version
Fast, reliable web search with natural language control.

Features:
- Natural language query parsing
- Robust error handling with fallbacks
- Intelligent caching
- Multiple output formats
- Retry logic with exponential backoff
- Proxy support
- Result filtering and ranking
"""

import argparse
import hashlib
import json
import logging
import os
import random
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from urllib.parse import quote_plus, urlparse
import urllib3

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Disable SSL warnings for proxy environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class SearchConfig:
    """Configuration for search operations."""
    api_key: Optional[str] = None
    base_url: str = "https://api.search.brave.com/res/v1"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    safe_search: str = "moderate"
    country: Optional[str] = None
    language: Optional[str] = None
    proxy: Optional[str] = None
    user_agent_rotation: bool = True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary (excluding sensitive data)."""
        return {
            k: v for k, v in asdict(self).items() 
            if k != 'api_key' and v is not None
        }


class QueryParser:
    """Parse natural language queries into structured search parameters."""
    
    # Natural language patterns for search type detection
    PATTERNS = {
        'images': [
            r'(?:show\s+me\s+)?(?:pictures?|images?|photos?|pics?)\s+(?:of\s+)?(.+)',
            r'(.+)\s+(?:pictures?|images?|photos?|pics?)',
        ],
        'news': [
            r'(?:latest|recent|current|breaking)\s+(?:news\s+)?(?:about\s+)?(.+)',
            r'(?:news\s+)?(?:about\s+)?(.+)\s+(?:news|headlines)',
            r'what\s+(?:is|are)\s+(?:the\s+)?latest\s+(?:on|about)\s+(.+)',
        ],
        'videos': [
            r'(?:show\s+me\s+)?(?:videos?|clips?)\s+(?:of\s+)?(.+)',
            r'(.+)\s+(?:videos?|clips?)',
        ],
    }
    
    # Limit extraction patterns
    LIMIT_PATTERNS = [
        r'(?:top|best|first)\s+(\d+)',
        r'(\d+)\s+(?:results?|items?)',
        r'show\s+(?:me\s+)?(?:only\s+)?(\d+)',
    ]
    
    # Country/Language patterns
    LOCALE_PATTERNS = {
        'country': [
            r'(?:in|from)\s+((?:the\s+)?(?:US|USA|UK|GB|SG|JP|CN|DE|FR|AU|CA|IN))',
            r'(?:in|from)\s+(Singapore|Japan|China|Germany|France|Australia|Canada|India|America|England)',
        ],
        'language': [
            r'(?:in|using)\s+(English|Chinese|Mandarin|Japanese|Korean|German|French|Spanish|Italian)',
        ],
    }
    
    @classmethod
    def parse(cls, query: str) -> Dict[str, Any]:
        """
        Parse a natural language query into search parameters.
        
        Args:
            query: Natural language search query
            
        Returns:
            Dictionary with parsed search parameters
        """
        query_lower = query.lower()
        params = {
            'query': query,
            'search_type': 'web',
            'limit': 10,
            'country': None,
            'language': None,
        }
        
        # Detect search type
        for search_type, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, query, re.IGNORECASE)
                if match:
                    params['search_type'] = search_type
                    # Extract the actual query
                    groups = match.groups()
                    if groups:
                        params['query'] = groups[0].strip()
                    break
            if params['search_type'] != 'web':
                break
        
        # Extract limit
        for pattern in cls.LIMIT_PATTERNS:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                params['limit'] = int(match.group(1))
                break
        
        # Extract country
        for pattern in cls.LOCALE_PATTERNS['country']:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                country = match.group(1).strip().upper()
                # Normalize country names
                country_map = {
                    'SINGAPORE': 'SG',
                    'JAPAN': 'JP',
                    'CHINA': 'CN',
                    'GERMANY': 'DE',
                    'FRANCE': 'FR',
                    'AUSTRALIA': 'AU',
                    'CANADA': 'CA',
                    'INDIA': 'IN',
                    'AMERICA': 'US',
                    'USA': 'US',
                    'UNITED STATES': 'US',
                    'ENGLAND': 'GB',
                    'UK': 'GB',
                    'UNITED KINGDOM': 'GB',
                }
                params['country'] = country_map.get(country, country)
                break
        
        # Extract language
        for pattern in cls.LOCALE_PATTERNS['language']:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                lang = match.group(1).strip().lower()
                lang_map = {
                    'english': 'en',
                    'chinese': 'zh',
                    'mandarin': 'zh',
                    'japanese': 'ja',
                    'korean': 'ko',
                    'german': 'de',
                    'french': 'fr',
                    'spanish': 'es',
                    'italian': 'it',
                }
                params['language'] = lang_map.get(lang, lang)
                break
        
        # Clean up query - remove extracted modifiers
        clean_query = params['query']
        for patterns_list in [cls.PATTERNS.values(), cls.LIMIT_PATTERNS, 
                              cls.LOCALE_PATTERNS['country'], cls.LOCALE_PATTERNS['language']]:
            for pattern in patterns_list:
                clean_query = re.sub(pattern, '', clean_query, flags=re.IGNORECASE)
        
        # Remove common filler words
        clean_query = re.sub(r'\b(?:please|can you|could you|i want|i need|find|search for|look for)\b', 
                            '', clean_query, flags=re.IGNORECASE)
        
        params['query'] = clean_query.strip()
        
        return params


class ResultCache:
    """Simple file-based cache for search results."""
    
    def __init__(self, cache_dir: Optional[str] = None, ttl: int = 3600):
        self.ttl = ttl
        self.cache_dir = Path(cache_dir or os.path.expanduser("~/.cache/websearch"))
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, query: str, params: Dict) -> str:
        """Generate cache key from query and params."""
        key_data = f"{query}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path."""
        return self.cache_dir / f"{key}.json"
    
    def get(self, query: str, params: Dict) -> Optional[Dict]:
        """Get cached result if valid."""
        key = self._get_cache_key(query, params)
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cached = json.load(f)
            
            # Check if cache is still valid
            cached_time = datetime.fromisoformat(cached['timestamp'])
            if datetime.now() - cached_time < timedelta(seconds=self.ttl):
                logger.debug(f"Cache hit for query: {query[:50]}...")
                return cached['data']
            else:
                logger.debug(f"Cache expired for query: {query[:50]}...")
                cache_path.unlink()
                return None
        except (json.JSONDecodeError, KeyError, IOError) as e:
            logger.warning(f"Cache read error: {e}")
            return None
    
    def set(self, query: str, params: Dict, data: Dict):
        """Cache search result."""
        key = self._get_cache_key(query, params)
        cache_path = self._get_cache_path(key)
        
        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'params': params,
                'data': data
            }
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f)
            logger.debug(f"Cached result for query: {query[:50]}...")
        except IOError as e:
            logger.warning(f"Cache write error: {e}")
    
    def clear(self):
        """Clear all cached results."""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        logger.info("Cache cleared")


class BraveSearchClient:
    """
    Enhanced client for Brave Search API with reliability features.
    """
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    ]
    
    def __init__(self, config: Optional[SearchConfig] = None):
        """
        Initialize the Brave Search client.
        
        Args:
            config: SearchConfig instance. If not provided, will use defaults.
        """
        self.config = config or SearchConfig()
        
        # Load API key if not provided
        if not self.config.api_key:
            self.config.api_key = self._load_api_key()
        
        if not self.config.api_key:
            raise ValueError(
                "Brave API key not found. Please configure it using:\n"
                "1. Environment variable: export BRAVE_API_KEY='your-key'\n"
                "2. Config file: echo '{\"brave_api_key\": \"your-key\"}' > config.json\n"
                "3. Interactive setup: python3 setup.py"
            )
        
        # Initialize cache
        self.cache = ResultCache(ttl=self.config.cache_ttl) if self.config.cache_enabled else None
        
        # Setup session with retry strategy
        self.session = self._create_session()
        
        logger.info("BraveSearchClient initialized successfully")
    
    def _create_session(self) -> requests.Session:
        """Create configured requests session."""
        session = requests.Session()
        
        # Configure retries
        retry_strategy = Retry(
            total=self.config.max_retries,
            backoff_factor=self.config.retry_delay,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        # Set headers
        headers = {
            "X-Subscription-Token": self.config.api_key,
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate",
        }
        
        # Rotate user agents if enabled
        if self.config.user_agent_rotation:
            headers["User-Agent"] = random.choice(self.USER_AGENTS)
        
        session.headers.update(headers)
        
        # Configure proxy if provided
        if self.config.proxy:
            session.proxies = {
                "http": self.config.proxy,
                "https": self.config.proxy
            }
        
        return session
    
    def _load_api_key(self) -> Optional[str]:
        """
        Load API key from multiple sources with fallback.
        """
        # Priority 1: Environment variable
        env_key = os.environ.get("BRAVE_API_KEY")
        if env_key and not env_key.startswith("YOUR_"):
            logger.debug("Loaded API key from environment variable")
            return env_key
        
        # Priority 2: Various config file locations
        config_paths = [
            Path("config.json"),
            Path(__file__).parent / "config.json",
            Path.home() / ".config" / "websearch" / "config.json",
            Path.home() / ".openclaw" / "workspace" / "skills" / "websearch" / "config.json",
            Path.home() / ".openclaw" / "credentials" / "brave-search",
        ]
        
        for config_path in config_paths:
            if config_path.exists():
                try:
                    if config_path.suffix == '.json':
                        with open(config_path, "r") as f:
                            config = json.load(f)
                        
                        for key_name in ["brave_api_key", "api_key", "BRAVE_API_KEY"]:
                            key = config.get(key_name)
                            if key and not key.startswith("YOUR_"):
                                logger.debug(f"Loaded API key from {config_path}")
                                return key
                    else:
                        # Plain text file
                        with open(config_path, "r") as f:
                            key = f.read().strip()
                        if key and not key.startswith("YOUR_"):
                            logger.debug(f"Loaded API key from {config_path}")
                            return key
                except (json.JSONDecodeError, IOError) as e:
                    logger.debug(f"Failed to load config from {config_path}: {e}")
                    continue
        
        return None
    
    def search(
        self,
        query: str,
        limit: int = 10,
        offset: int = 0,
        search_type: str = "web",
        country: Optional[str] = None,
        language: Optional[str] = None,
        safe_search: Optional[str] = None,
        use_cache: bool = True,
    ) -> Dict:
        """
        Perform a web search with reliability features.
        
        Args:
            query: Search query string
            limit: Number of results (1-20 web/news, 1-50 images)
            offset: Result offset for pagination
            search_type: Type of search - "web", "news", or "images"
            country: Country code (e.g., "US", "SG")
            language: Language code (e.g., "en", "zh")
            safe_search: Safe search level - "off", "moderate", or "strict"
            use_cache: Whether to use caching
        
        Returns:
            Dictionary containing search results
        """
        if not query or not query.strip():
            raise ValueError("Search query cannot be empty")
        
        # Prepare parameters
        params = {
            'query': query.strip(),
            'limit': limit,
            'offset': offset,
            'search_type': search_type,
            'country': country or self.config.country,
            'language': language or self.config.language,
            'safe_search': safe_search or self.config.safe_search,
        }
        
        # Clamp limit
        max_limit = 50 if search_type == "images" else 20
        params['limit'] = max(1, min(max_limit, params['limit']))
        
        # Check cache
        if use_cache and self.cache:
            cached_result = self.cache.get(query, params)
            if cached_result:
                cached_result['cached'] = True
                return cached_result
        
        # Make API request
        try:
            if search_type == "images":
                result = self._search_images(query, params)
            else:
                result = self._search_web_or_news(query, params)
            
            # Cache result
            if use_cache and self.cache:
                self.cache.set(query, params, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    def _search_web_or_news(self, query: str, params: Dict) -> Dict:
        """Perform web or news search."""
        endpoint = f"{self.config.base_url}/{params['search_type']}/search"
        
        request_params = {
            "q": query,
            "count": params['limit'],
            "offset": params['offset'],
        }
        
        # Add optional parameters
        if params.get('country'):
            request_params["country"] = params['country']
        if params.get('language'):
            request_params["search_lang"] = params['language']
        if params.get('safe_search'):
            request_params["safesearch"] = params['safe_search']
        
        # Rotate user agent for each request
        if self.config.user_agent_rotation:
            self.session.headers["User-Agent"] = random.choice(self.USER_AGENTS)
        
        logger.debug(f"Making {params['search_type']} search request: {query[:50]}...")
        
        response = self.session.get(
            endpoint, 
            params=request_params, 
            timeout=self.config.timeout
        )
        response.raise_for_status()
        data = response.json()
        
        return self._parse_results(data, query, params)
    
    def _search_images(self, query: str, params: Dict) -> Dict:
        """Perform image search."""
        endpoint = f"{self.config.base_url}/images/search"
        
        request_params = {
            "q": query,
            "count": params['limit'],
            "offset": params['offset'],
        }
        
        if params.get('country'):
            request_params["country"] = params['country']
        
        if self.config.user_agent_rotation:
            self.session.headers["User-Agent"] = random.choice(self.USER_AGENTS)
        
        logger.debug(f"Making image search request: {query[:50]}...")
        
        response = self.session.get(
            endpoint, 
            params=request_params, 
            timeout=self.config.timeout
        )
        response.raise_for_status()
        data = response.json()
        
        return self._parse_image_results(data, query, params)
    
    def _parse_results(self, data: Dict, query: str, params: Dict) -> Dict:
        """Parse web/news API response."""
        results = []
        
        if params['search_type'] == "web":
            web_results = data.get("web", {}).get("results", [])
            for item in web_results:
                result = {
                    "title": item.get("title", "No title"),
                    "url": item.get("url", ""),
                    "description": item.get("description", "No description"),
                    "source": item.get("profile", {}).get("name", "Unknown"),
                    "age": item.get("age", ""),
                    "is_source_local": item.get("is_source_local", False),
                    "is_source_both": item.get("is_source_both", False),
                }
                # Add favicon if available
                if item.get("profile", {}).get("img"):
                    result["favicon"] = item["profile"]["img"]
                results.append(result)
        
        elif params['search_type'] == "news":
            news_results = data.get("results", [])
            for item in news_results:
                result = {
                    "title": item.get("title", "No title"),
                    "url": item.get("url", ""),
                    "description": item.get("description", "No description"),
                    "source": item.get("source", {}).get("name", "Unknown"),
                    "published": item.get("age", ""),
                    "meta_url": item.get("meta_url", {}).get("hostname", ""),
                }
                # Add thumbnail if available
                if item.get("thumbnail"):
                    result["thumbnail"] = item["thumbnail"].get("src", "")
                results.append(result)
        
        return {
            "query": query,
            "type": params['search_type'],
            "total_results": len(results),
            "params": {k: v for k, v in params.items() if v is not None},
            "results": results,
            "cached": False,
            "timestamp": datetime.now().isoformat(),
        }
    
    def _parse_image_results(self, data: Dict, query: str, params: Dict) -> Dict:
        """Parse image search results."""
        results = []
        image_results = data.get("results", [])
        
        for item in image_results:
            result = {
                "title": item.get("title", "No title"),
                "url": item.get("url", ""),
                "source": item.get("source", "Unknown"),
                "thumbnail": item.get("thumbnail", {}).get("src", ""),
                "width": item.get("width", 0),
                "height": item.get("height", 0),
            }
            results.append(result)
        
        return {
            "query": query,
            "type": "images",
            "total_results": len(results),
            "params": {k: v for k, v in params.items() if v is not None},
            "results": results,
            "cached": False,
            "timestamp": datetime.now().isoformat(),
        }
    
    def natural_search(self, query: str, **kwargs) -> Dict:
        """
        Search using natural language query parsing.
        
        Args:
            query: Natural language query
            **kwargs: Additional search parameters
            
        Returns:
            Search results
        """
        parsed = QueryParser.parse(query)
        parsed.update(kwargs)
        
        logger.info(f"Natural query: '{query}' -> Parsed: {parsed}")
        
        return self.search(
            query=parsed['query'],
            search_type=parsed['search_type'],
            limit=parsed['limit'],
            country=parsed.get('country'),
            language=parsed.get('language'),
        )
    
    def health_check(self) -> Dict:
        """Check API connectivity and key validity."""
        try:
            # Try a simple search
            result = self.search("test", limit=1, use_cache=False)
            return {
                "status": "healthy",
                "api_key_valid": True,
                "rate_limited": False,
                "message": "API is working correctly"
            }
        except ValueError as e:
            if "Invalid API key" in str(e):
                return {
                    "status": "error",
                    "api_key_valid": False,
                    "rate_limited": False,
                    "message": str(e)
                }
            raise
        except Exception as e:
            return {
                "status": "error",
                "api_key_valid": None,
                "rate_limited": "429" in str(e),
                "message": str(e)
            }


def format_text_output(data: Dict, verbose: bool = False, compact: bool = False) -> str:
    """Format search results as readable text."""
    lines = []
    
    # Header
    lines.append(f'🔍 Results for: "{data["query"]}"')
    lines.append(f'Type: {data["type"].capitalize()} | Found: {data["total_results"]} results')
    
    if data.get('cached'):
        lines.append("📦 Result loaded from cache")
    
    if verbose and data.get('params'):
        lines.append(f"Parameters: {json.dumps(data['params'])}")
    
    lines.append("")
    
    # Results
    if not data["results"]:
        lines.append("❌ No results found.")
        return "\n".join(lines)
    
    for i, result in enumerate(data["results"], 1):
        if compact:
            # Compact format
            lines.append(f"{i}. {result['title']}")
            lines.append(f"   {result['url']}")
        else:
            # Full format
            lines.append(f"{i}. {result['title']}")
            lines.append(f"   URL: {result['url']}")
            
            if result.get('source') and result['source'] != 'Unknown':
                lines.append(f"   Source: {result['source']}")
            
            if result.get('published') or result.get('age'):
                time_info = result.get('published') or result.get('age')
                lines.append(f"   Published: {time_info}")
            
            if result.get('thumbnail'):
                lines.append(f"   Thumbnail: {result['thumbnail']}")
                if result.get('width') and result.get('height'):
                    lines.append(f"   Dimensions: {result['width']}x{result['height']}")
            
            if result.get('description'):
                desc = result['description']
                if len(desc) > 200 and not verbose:
                    desc = desc[:200] + "..."
                lines.append(f"   {desc}")
        
        lines.append("")
    
    return "\n".join(lines)


def format_markdown_output(data: Dict) -> str:
    """Format results as Markdown."""
    lines = []
    
    lines.append(f"# Search Results: {data['query']}")
    lines.append(f"\n**Type:** {data['type'].capitalize()} | **Found:** {data['total_results']} results")
    lines.append("")
    
    for result in data["results"]:
        lines.append(f"## [{result['title']}]({result['url']})")
        
        if result.get('source'):
            lines.append(f"*Source: {result['source']}*")
        
        if result.get('published') or result.get('age'):
            time_info = result.get('published') or result.get('age')
            lines.append(f"*Published: {time_info}*")
        
        if result.get('thumbnail'):
            lines.append(f"\n![Thumbnail]({result['thumbnail']})")
        
        if result.get('description'):
            lines.append(f"\n{result['description']}")
        
        lines.append("---\n")
    
    return "\n".join(lines)


def format_csv_output(data: Dict) -> str:
    """Format results as CSV."""
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(["#", "Title", "URL", "Source", "Description"])
    
    # Data
    for i, result in enumerate(data["results"], 1):
        writer.writerow([
            i,
            result.get('title', ''),
            result.get('url', ''),
            result.get('source', ''),
            result.get('description', '')[:100] + '...' if result.get('description') else ''
        ])
    
    return output.getvalue()


def interactive_mode(client: BraveSearchClient):
    """Run interactive search mode."""
    print("🔍 Websearch Interactive Mode")
    print("=" * 50)
    print("Type your search query (or 'quit' to exit, 'help' for commands)")
    print()
    
    while True:
        try:
            query = input("Search> ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if query.lower() in ['help', '?']:
                print("\nCommands:")
                print("  quit, exit, q    - Exit interactive mode")
                print("  help, ?          - Show this help")
                print("  cache clear      - Clear search cache")
                print("  health           - Check API health")
                print()
                print("Search tips:")
                print("  'images of cats' - Search for images")
                print("  'latest news on AI' - Search news")
                print("  'top 5 python tutorials' - Limit results")
                print()
                continue
            
            if query.lower() == 'cache clear':
                if client.cache:
                    client.cache.clear()
                    print("✅ Cache cleared\n")
                else:
                    print("⚠️  Caching is disabled\n")
                continue
            
            if query.lower() == 'health':
                health = client.health_check()
                print(f"Status: {health['status']}")
                print(f"API Key Valid: {health['api_key_valid']}")
                print(f"Message: {health['message']}\n")
                continue
            
            # Perform natural language search
            result = client.natural_search(query)
            print(format_text_output(result))
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Search the web using Brave Search API - Enhanced Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search
  python3 search.py "python tutorials"
  
  # Natural language queries
  python3 search.py "show me images of cats"
  python3 search.py "latest news about AI"
  python3 search.py "top 5 restaurants in Singapore"
  
  # Search types
  python3 search.py "tech news" --type news
  python3 search.py "landscape photos" --type images
  
  # Output formats
  python3 search.py "python tips" --format json
  python3 search.py "recipes" --format markdown
  python3 search.py "companies" --format csv
  
  # Advanced options
  python3 search.py "local events" --country SG --language en
  python3 search.py "research paper" --no-cache --verbose
  python3 search.py "test" --health-check
  
  # Interactive mode
  python3 search.py --interactive
        """
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Search query string (optional in interactive mode)"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=10,
        help="Number of results (1-20 web/news, 1-50 images, default: 10)"
    )
    parser.add_argument(
        "--offset", "-o",
        type=int,
        default=0,
        help="Result offset for pagination (default: 0)"
    )
    parser.add_argument(
        "--type", "-t",
        choices=["web", "news", "images"],
        default=None,
        help="Search type: web, news, or images (auto-detected if not specified)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json", "markdown", "csv"],
        default="text",
        help="Output format (default: text)"
    )
    parser.add_argument(
        "--country", "-c",
        help="Country code (e.g., US, SG, GB)"
    )
    parser.add_argument(
        "--language", "-L",
        help="Language code (e.g., en, zh, ja)"
    )
    parser.add_argument(
        "--safe-search",
        choices=["off", "moderate", "strict"],
        default="moderate",
        help="Safe search level (default: moderate)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Compact output (less detail)"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Disable caching for this search"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear search cache and exit"
    )
    parser.add_argument(
        "--health-check",
        action="store_true",
        help="Check API health and exit"
    )
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Interactive search mode"
    )
    parser.add_argument(
        "--api-key",
        help="Brave API key (overrides config)"
    )
    parser.add_argument(
        "--proxy",
        help="Proxy URL (e.g., http://proxy:8080)"
    )
    
    args = parser.parse_args()
    
    try:
        # Create configuration
        config = SearchConfig(
            api_key=args.api_key,
            safe_search=args.safe_search,
            country=args.country,
            language=args.language,
            proxy=args.proxy,
            cache_enabled=not args.no_cache,
        )
        
        # Initialize client
        client = BraveSearchClient(config)
        
        # Handle special commands
        if args.clear_cache:
            if client.cache:
                client.cache.clear()
            else:
                print("Caching is disabled")
            return
        
        if args.health_check:
            health = client.health_check()
            print(json.dumps(health, indent=2))
            return
        
        if args.interactive:
            interactive_mode(client)
            return
        
        # Validate query
        if not args.query:
            parser.print_help()
            sys.exit(1)
        
        # Determine search type
        search_type = args.type
        
        if search_type:
            # Use explicit type
            result = client.search(
                query=args.query,
                limit=args.limit,
                offset=args.offset,
                search_type=search_type,
            )
        else:
            # Use natural language parsing
            result = client.natural_search(
                query=args.query,
                limit=args.limit,
                offset=args.offset,
            )
        
        # Output results
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        elif args.format == "markdown":
            print(format_markdown_output(result))
        elif args.format == "csv":
            print(format_csv_output(result))
        else:
            print(format_text_output(result, verbose=args.verbose, compact=args.compact))
            
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  Search cancelled.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        logger.exception("Unexpected error")
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
