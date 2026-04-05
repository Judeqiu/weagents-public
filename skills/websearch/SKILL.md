---
name: websearch
description: Professional-grade web search using Brave Search API with natural language control, intelligent caching, and multiple output formats. Extremely reliable with retry logic, fallback mechanisms, and flexible configuration options.
version: 2.0.0
metadata:
  category: "web"
  requires:
    bins: ["python3"]
    python_packages: ["requests>=2.28.0"]
  features:
    - natural_language_control
    - intelligent_caching
    - retry_logic
    - multiple_formats
    - proxy_support
    - user_agent_rotation
---

# Websearch Skill v2.0

**Professional-grade web search with natural language control.**

This skill provides an extremely reliable and flexible web search solution using the Brave Search API. It features natural language query parsing, intelligent caching, robust error handling with retry logic, and multiple output formats.

## 🌟 Key Features

| Feature | Description |
|---------|-------------|
| 🗣️ **Natural Language** | Search using plain English - "show me images of cats" |
| 🧠 **Smart Parsing** | Automatically detects search type, limits, country, language |
| 💾 **Intelligent Cache** | Results cached for 1 hour to reduce API calls |
| 🔄 **Retry Logic** | Automatic retry with exponential backoff on failures |
| 🌍 **International** | Country and language filtering support |
| 📤 **Multiple Formats** | Text, JSON, Markdown, CSV output |
| 🔒 **Reliable** | Proxy support, user agent rotation, robust error handling |
| 💬 **Interactive Mode** | Chat-like interface for continuous searching |

---

## 🚀 Quick Start

### Basic Search

```bash
python3 search.py "python tutorials"
```

### Natural Language Queries

```bash
# The skill automatically understands what you want
python3 search.py "show me images of cute cats"
python3 search.py "latest news about artificial intelligence"
python3 search.py "top 5 restaurants in Singapore"
python3 search.py "python best practices in English"
```

### Interactive Mode

```bash
python3 search.py --interactive
```

Then type natural queries:
```
Search> images of mountains
Search> latest tech news from Japan
Search> top 10 python libraries
Search> quit
```

---

## 📖 Natural Language Control

The skill understands natural language and automatically extracts:

### Search Type Detection

| Query Pattern | Detected Type |
|--------------|---------------|
| "images of cats" | `images` |
| "pictures of dogs" | `images` |
| "latest news on AI" | `news` |
| "breaking news about stocks" | `news` |
| "videos of tutorials" | `web` (with video context) |
| "how to learn python" | `web` |

### Result Limits

| Query Pattern | Extracted Limit |
|--------------|-----------------|
| "top 5 results" | 5 |
| "show me 20 items" | 20 |
| "best 10 restaurants" | 10 |
| "first 3 results" | 3 |

### Location & Language

| Query Pattern | Extracted Parameters |
|--------------|---------------------|
| "restaurants in Singapore" | `country: SG` |
| "news from Japan" | `country: JP` |
| "tutorials in Chinese" | `language: zh` |
| "content in English" | `language: en` |

### Combined Examples

```bash
# Complex natural language query
python3 search.py "show me top 15 images of beautiful landscapes from Japan"
# -> search_type: images, limit: 15, country: JP

python3 search.py "latest breaking news about technology in English"
# -> search_type: news, language: en

python3 search.py "best 5 python tutorials from the US"
# -> limit: 5, country: US
```

---

## 🔧 Setup & Configuration

### 1. Get API Key

1. Visit https://api.search.brave.com/app/keys
2. Sign up for free account
3. Generate API key
4. Free tier: 2,000 queries/month, 1 query/second

### 2. Configure API Key

Choose ONE of these methods (in priority order):

#### Method A: Environment Variable (Recommended)
```bash
export BRAVE_API_KEY="your-api-key-here"
```

Add to `~/.bashrc` or `~/.zshrc` for persistence.

#### Method B: Config File
```bash
echo '{"brave_api_key": "your-api-key-here"}' > config.json
```

#### Method C: Interactive Setup
```bash
python3 setup.py
```

#### Method D: Global Config
```bash
mkdir -p ~/.config/websearch
echo '{"brave_api_key": "your-api-key-here"}' > ~/.config/websearch/config.json
```

#### Method E: OpenClaw Credentials
```bash
echo "your-api-key-here" > ~/.openclaw/credentials/brave-search
chmod 600 ~/.openclaw/credentials/brave-search
```

### 3. Verify Setup

```bash
python3 search.py --health-check
```

Expected output:
```json
{
  "status": "healthy",
  "api_key_valid": true,
  "rate_limited": false,
  "message": "API is working correctly"
}
```

---

## 💻 Command Reference

### Basic Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--limit` | `-l` | Number of results (1-20 web/news, 1-50 images) | 10 |
| `--offset` | `-o` | Pagination offset | 0 |
| `--type` | `-t` | Force search type: `web`, `news`, `images` | auto-detect |
| `--format` | `-f` | Output format: `text`, `json`, `markdown`, `csv` | text |

### Advanced Options

| Option | Description | Example |
|--------|-------------|---------|
| `--country` | Country code | `--country SG` |
| `--language` | Language code | `--language zh` |
| `--safe-search` | `off`, `moderate`, `strict` | `--safe-search strict` |
| `--verbose` | Detailed output | `--verbose` |
| `--compact` | Minimal output | `--compact` |
| `--no-cache` | Bypass cache | `--no-cache` |
| `--proxy` | Proxy URL | `--proxy http://proxy:8080` |

### Special Commands

| Command | Description |
|---------|-------------|
| `--interactive` | Interactive search mode |
| `--health-check` | Verify API connectivity |
| `--clear-cache` | Clear search cache |

---

## 📤 Output Formats

### Text Format (Default)

```bash
python3 search.py "python tutorial"
```

```
🔍 Results for: "python tutorial"
Type: Web | Found: 10 results

1. Python Tutorial - W3Schools
   URL: https://www.w3schools.com/python/
   Source: W3Schools
   Age: 2 years ago
   Well organized and easy to understand Web building tutorials...

2. Learn Python - Python.org
   URL: https://www.python.org/about/gettingstarted/
   Source: Python.org
   Age: 3 years ago
   Learn to code with our beginner-friendly tutorials...
```

### JSON Format

```bash
python3 search.py "python tutorial" --format json
```

```json
{
  "query": "python tutorial",
  "type": "web",
  "total_results": 10,
  "params": {
    "limit": 10,
    "search_type": "web"
  },
  "results": [
    {
      "title": "Python Tutorial - W3Schools",
      "url": "https://www.w3schools.com/python/",
      "description": "Well organized and easy to understand...",
      "source": "W3Schools",
      "age": "2 years ago"
    }
  ],
  "cached": false,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Markdown Format

```bash
python3 search.py "python tutorial" --format markdown
```

```markdown
# Search Results: python tutorial

**Type:** Web | **Found:** 10 results

## [Python Tutorial - W3Schools](https://www.w3schools.com/python/)

*Source: W3Schools*

Well organized and easy to understand Web building tutorials...

---
```

### CSV Format

```bash
python3 search.py "python tutorial" --format csv
```

```csv
#,Title,URL,Source,Description
1,Python Tutorial - W3Schools,https://www.w3schools.com/python/,W3Schools,Well organized...
2,Learn Python - Python.org,https://www.python.org/about/gettingstarted/,Python.org,Learn to code...
```

---

## 🐍 Python API

### Basic Usage

```python
from websearch import BraveSearchClient

# Initialize (auto-loads API key from config)
client = BraveSearchClient()

# Simple search
results = client.search("python tutorials", limit=5)

# Natural language search
results = client.natural_search("show me images of cats")

# Print results
for result in results["results"]:
    print(f"{result['title']}: {result['url']}")
```

### Advanced Usage

```python
from websearch import BraveSearchClient, SearchConfig

# Custom configuration
config = SearchConfig(
    api_key="your-api-key",
    timeout=60,
    max_retries=5,
    cache_enabled=True,
    cache_ttl=7200,  # 2 hours
    proxy="http://proxy:8080",
    user_agent_rotation=True,
)

client = BraveSearchClient(config)

# Image search
images = client.search(
    "landscape photos",
    search_type="images",
    limit=20
)

# International search
results = client.search(
    "local restaurants",
    country="SG",
    language="en",
    limit=10
)

# Disable cache for fresh results
results = client.search(
    "breaking news",
    search_type="news",
    use_cache=False
)

# Health check
health = client.health_check()
print(f"API Status: {health['status']}")
```

---

## 🛠️ Interactive Mode Commands

When in interactive mode (`--interactive`):

| Command | Description |
|---------|-------------|
| `quit`, `exit`, `q` | Exit interactive mode |
| `help`, `?` | Show help |
| `cache clear` | Clear search cache |
| `health` | Check API health |

### Interactive Example

```bash
$ python3 search.py --interactive

🔍 Websearch Interactive Mode
==================================================
Type your search query (or 'quit' to exit, 'help' for commands)

Search> images of cute cats
🔍 Results for: "cute cats"
Type: Images | Found: 10 results
...

Search> latest news about AI from the US
🔍 Results for: "AI"
Type: News | Found: 10 results | Country: US
...

Search> cache clear
✅ Cache cleared

Search> health
Status: healthy
API Key Valid: True
Message: API is working correctly

Search> quit
Goodbye!
```

---

## 🔧 Troubleshooting

### "API key not configured"

**Problem:** No API key found in any configuration source.

**Solution:**
```bash
# Set environment variable
export BRAVE_API_KEY="your-key-here"

# Or run interactive setup
python3 setup.py
```

### "Invalid API key"

**Problem:** API key is invalid or expired.

**Solution:**
1. Verify key at https://api.search.brave.com/app/keys
2. Check for typos or extra spaces
3. Generate a new key if expired

### "Rate limit exceeded"

**Problem:** Too many requests (free tier: 1 req/sec).

**Solution:**
- The client has automatic retry - just wait
- Use cache to reduce repeated searches: don't use `--no-cache`
- Consider upgrading to paid tier

### "No results found"

**Problem:** Empty results.

**Solution:**
- Try different search terms
- Check internet connectivity
- Verify Brave API service status

### Cache Issues

**Clear cache:**
```bash
python3 search.py --clear-cache
```

**Disable cache for specific search:**
```bash
python3 search.py "query" --no-cache
```

---

## 🌍 Supported Locales

### Countries

| Code | Country |
|------|---------|
| US | United States |
| SG | Singapore |
| GB | United Kingdom |
| AU | Australia |
| CA | Canada |
| JP | Japan |
| CN | China |
| DE | Germany |
| FR | France |
| IN | India |

### Languages

| Code | Language |
|------|----------|
| en | English |
| zh | Chinese |
| ja | Japanese |
| ko | Korean |
| de | German |
| fr | French |
| es | Spanish |
| it | Italian |

---

## 📊 API Limits

| Tier | Queries/Month | Rate Limit |
|------|---------------|------------|
| Free | 2,000 | 1 req/sec |
| Pro | 10,000 | 10 req/sec |
| Business | 50,000+ | Custom |

Upgrade at: https://api.search.brave.com/

---

## 🔒 Security Features

- API key loaded from secure locations only
- Config file permissions set to 600
- No API key in logs or error messages
- User agent rotation to prevent blocking
- Proxy support for corporate environments

---

## 📝 Changelog

### v2.0.0
- ✨ Natural language query parsing
- ✨ Intelligent caching system
- ✨ Interactive search mode
- ✨ Multiple output formats (text, JSON, Markdown, CSV)
- ✨ Retry logic with exponential backoff
- ✨ Health check functionality
- ✨ Proxy support
- ✨ User agent rotation
- ✨ Enhanced error messages
- ✨ Setup helper script

### v1.1.0
- Added image search support
- Added retry logic
- Added country/language filtering

### v1.0.0
- Initial release with web and news search

---

## 💡 Tips & Best Practices

1. **Use Natural Language:** Let the skill automatically detect search type
2. **Enable Caching:** Reduces API calls and improves speed
3. **Use Interactive Mode:** For exploration and research
4. **JSON Format:** For programmatic processing
5. **Markdown Format:** For documentation and reports
6. **Health Check:** Verify setup before batch operations

---

*For issues and feature requests, please refer to the skill documentation or contact the OpenClaw agent.*
