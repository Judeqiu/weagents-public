#!/usr/bin/env python3
"""
Websearch Skill - Usage Examples
Demonstrates various features and use cases.
"""

from websearch import BraveSearchClient, SearchConfig


def example_basic_search():
    """Basic search example."""
    print("Example 1: Basic Search")
    print("-" * 60)
    
    client = BraveSearchClient()
    results = client.search("python tutorials", limit=5)
    
    print(f"Query: {results['query']}")
    print(f"Found: {results['total_results']} results")
    print()
    
    for i, result in enumerate(results['results'][:3], 1):
        print(f"{i}. {result['title']}")
        print(f"   {result['url']}")
    print()


def example_natural_language():
    """Natural language search example."""
    print("Example 2: Natural Language Search")
    print("-" * 60)
    
    client = BraveSearchClient()
    
    queries = [
        "show me images of cute cats",
        "latest news about artificial intelligence",
        "top 5 python tutorials",
        "restaurants in Singapore",
    ]
    
    for query in queries:
        results = client.natural_search(query)
        print(f"Query: '{query}'")
        print(f"  -> Type: {results['type']}, Found: {results['total_results']}")
        if results.get('params'):
            print(f"  -> Params: {results['params']}")
        print()


def example_image_search():
    """Image search example."""
    print("Example 3: Image Search")
    print("-" * 60)
    
    client = BraveSearchClient()
    results = client.search(
        "landscape photography",
        search_type="images",
        limit=5
    )
    
    print(f"Query: {results['query']}")
    print(f"Found: {results['total_results']} images")
    print()
    
    for result in results['results'][:3]:
        print(f"- {result['title']}")
        print(f"  URL: {result['url']}")
        print(f"  Size: {result.get('width', 'N/A')}x{result.get('height', 'N/A')}")
        print()


def example_international():
    """International search example."""
    print("Example 4: International Search")
    print("-" * 60)
    
    client = BraveSearchClient()
    
    # Search in specific country and language
    results = client.search(
        "local news",
        search_type="news",
        country="SG",
        language="en",
        limit=5
    )
    
    print(f"Query: {results['query']}")
    print(f"Country: SG, Language: en")
    print(f"Found: {results['total_results']} results")
    print()


def example_custom_config():
    """Custom configuration example."""
    print("Example 5: Custom Configuration")
    print("-" * 60)
    
    config = SearchConfig(
        timeout=60,
        max_retries=5,
        cache_enabled=True,
        cache_ttl=7200,  # 2 hours
    )
    
    client = BraveSearchClient(config)
    results = client.search("reliable web search", limit=3)
    
    print(f"Custom timeout: {config.timeout}s")
    print(f"Custom retries: {config.max_retries}")
    print(f"Cache TTL: {config.cache_ttl}s")
    print(f"Results: {results['total_results']}")
    print()


def example_format_output():
    """Format output example."""
    print("Example 6: Different Output Formats")
    print("-" * 60)
    
    client = BraveSearchClient()
    results = client.search("python best practices", limit=3)
    
    from websearch import (
        format_text_output,
        format_markdown_output,
        format_csv_output
    )
    
    print("Text format preview:")
    text = format_text_output(results, compact=True)
    print(text[:300] + "...")
    print()
    
    print("Markdown format preview:")
    md = format_markdown_output(results)
    print(md[:300] + "...")
    print()
    
    print("CSV format preview:")
    csv = format_csv_output(results)
    print(csv[:200] + "...")
    print()


def example_health_check():
    """Health check example."""
    print("Example 7: Health Check")
    print("-" * 60)
    
    client = BraveSearchClient()
    health = client.health_check()
    
    print(f"Status: {health['status']}")
    print(f"API Key Valid: {health['api_key_valid']}")
    print(f"Message: {health['message']}")
    print()


def example_cache_management():
    """Cache management example."""
    print("Example 8: Cache Management")
    print("-" * 60)
    
    client = BraveSearchClient()
    
    # First search - will cache
    print("First search (caches result)...")
    results1 = client.search("cache test query", limit=1)
    print(f"Cached: {results1.get('cached', False)}")
    
    # Second search - should hit cache
    print("Second search (should hit cache)...")
    results2 = client.search("cache test query", limit=1)
    print(f"Cached: {results2.get('cached', False)}")
    
    # Search with cache disabled
    print("Search with cache disabled...")
    results3 = client.search("cache test query", limit=1, use_cache=False)
    print(f"Cached: {results3.get('cached', False)}")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 60)
    print("Websearch Skill - Usage Examples")
    print("=" * 60 + "\n")
    
    examples = [
        ("Basic Search", example_basic_search),
        ("Natural Language", example_natural_language),
        ("Image Search", example_image_search),
        ("International", example_international),
        ("Custom Config", example_custom_config),
        ("Format Output", example_format_output),
        ("Health Check", example_health_check),
        ("Cache Management", example_cache_management),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"❌ Example '{name}' failed: {e}")
        print()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
