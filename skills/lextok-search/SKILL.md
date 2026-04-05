---
name: lextok-search
description: Use when needing to search the internet for current information including news, articles, product pages, documentation, blogs, reviews, research papers, or official websites. Use when you need to find up-to-date information that may not be in your training data.
version: 1.0.0
metadata:
  category: "web"
  requires:
    bins: ["python3"]
    python_packages: ["requests", "beautifulsoup4"]
---

# LexTok Search Skill

**Internet search using Brave Search API with optional full content fetching.**

This skill queries an internet search index to find current information on:
- News and articles
- Product pages and documentation
- Blogs and reviews
- Research papers
- Official websites

## When to Use

✅ **Use this skill for:**
- Finding current information not in training data
- Searching news and articles
- Finding product pages and documentation
- Research papers and academic sources
- Blogs and reviews
- Official websites

❌ **Don't use for:**
- Sites requiring authentication (use browser skills)
- Complex multi-step interactions

## Quick Start

### Basic Search

```bash
python3 skills/lextok-search/search.py "your search query"
```

### Search with Options

```bash
# Limit results
python3 skills/lextok-search/search.py "machine learning" --limit 3

# Include full page content (consumes more tokens)
python3 skills/lextok-search/search.py "python tutorial" --include-content

# Full example
python3 skills/lextok-search/search.py "AI developments" --limit 5 --include-content
```

## Setup

### Configure API Key

Edit `config.json` and add your Brave Search API key:

```json
{
  "brave_api_key": "YOUR_BRAVE_API_KEY_HERE"
}
```

Or set via environment variable:

```bash
export BRAVE_API_KEY="your-api-key"
```

### Get a Brave Search API Key

1. Go to https://api.search.brave.com/
2. Sign up for an account
3. Generate an API key
4. Add it to your `config.json`

## Parameters

| Parameter         | Type    | Default      | Description                                               |
| ----------------- | ------- | ------------ | --------------------------------------------------------- |
| `query`           | string  | **required** | Your search query                                         |
| `limit`           | number  | 5            | Number of results to return (typically 1-10)              |
| `include_content` | boolean | false        | Whether to fetch full page content (consumes more tokens) |

## Usage Examples

### Basic Search (default: 5 results)

```bash
python3 skills/lextok-search/search.py "latest AI developments"
```

Output:
```
🔍 Results for: "latest AI developments"

1. Latest AI Developments in 2024 - TechCrunch
   URL: https://techcrunch.com/2024/...
   Source: TechCrunch
   Artificial intelligence continues to evolve with new breakthroughs in...

2. AI News - MIT Technology Review
   URL: https://www.technologyreview.com/...
   Source: MIT Technology Review
   The latest advancements in machine learning and AI research...
```

### Search with Full Content

```bash
python3 skills/lextok-search/search.py "python best practices" --include-content --limit 3
```

Output includes `content` field with extracted page text for each result.

### JSON Output

```bash
python3 skills/lextok-search/search.py "news today" --format json
```

## Python API

```python
from search import LexTokSearchClient

# Initialize client
client = LexTokSearchClient(api_key="your-api-key")

# Basic search
results = client.search("your query", limit=5)

# Search with content
results = client.search("your query", limit=5, include_content=True)

# Print results
for result in results["results"]:
    print(f"{result['title']}: {result['url']}")
    if 'content' in result:
        print(f"Content: {result['content'][:500]}...")
```

## Command Reference

| Option                | Description | Default |
|-----------------------|-------------|---------|
| `--limit, -l`         | Number of results (1-20) | 5 |
| `--include-content`   | Fetch full page content | false |
| `--format, -f`        | Output format: text or json | text |
| `--config, -c`        | Path to config file | config.json |
| `--timeout`           | Page fetch timeout in seconds | 10 |

## API Limits

Brave Search API free tier includes:
- 2,000 queries per month
- 1 query per second rate limit

Paid tiers available for higher volume.

## Troubleshooting

### "API key not configured"

Add your API key to `config.json` or set the `BRAVE_API_KEY` environment variable.

### "Rate limit exceeded"

Wait a moment between requests. The free tier allows 1 request per second.

### Content fetching fails

Some sites block automated fetching. The skill will return search results without content in these cases.
