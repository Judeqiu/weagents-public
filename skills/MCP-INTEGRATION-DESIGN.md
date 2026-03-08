# MCP Integration Design for Financial Skills

Connecting financial analysis tools to live market data via Model Context Protocol (MCP).

## Overview

This document specifies how to integrate the financial skills ecosystem with live financial data providers using MCP servers.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Financial Skills Ecosystem                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │   Valuation  │  │  Investment  │  │   Equity     │           │
│  │    Skills    │  │   Banking    │  │  Research    │           │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘           │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                     │
│                  ┌────────┴────────┐                           │
│                  │  MCP Client     │                           │
│                  │  (AI Agent)     │                           │
│                  └────────┬────────┘                           │
└───────────────────────────┼─────────────────────────────────────┘
                            │ MCP Protocol
┌───────────────────────────┼─────────────────────────────────────┐
│                     MCP Server Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Market Data  │  │   SEC EDGAR  │  │  Estimates   │          │
│  │    Server    │  │    Server    │  │   Server     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ M&A/Trans    │  │    News      │  │  Economic    │          │
│  │   Server     │  │    Server    │  │    Data      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────┐
│                     Data Providers                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ Bloomberg│ │FactSet/  │ │  SEC      │ │Alpaca/   │          │
│  │ Refinitiv│ │  CapIQ    │ │ EDGAR API │ │Massive/Polygon   │          │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## MCP Servers Overview

### 1. Market Data MCP Server
Real-time and historical market prices, volumes, corporate actions.

### 2. SEC EDGAR MCP Server
Company filings, financial statements, insider trading data.

### 3. Estimates MCP Server
Analyst estimates, earnings calendars, recommendation trends.

### 4. M&A Transactions MCP Server
Precedent transactions, deal terms, multiples database.

### 5. News & Sentiment MCP Server
Financial news, earnings call transcripts, sentiment analysis.

### 6. Economic Data MCP Server
Macroeconomic indicators, interest rates, industry data.

---

## Server 1: Market Data MCP Server

### Purpose
Provide real-time and historical stock prices, volumes, and corporate actions.

### Data Sources
- **Primary**: Massive (formerly Massive/Polygon.io), Alpaca Markets, Finnhub
- **Fallback**: Yahoo Finance, Alpha Vantage
- **Real-time**: WebSocket feeds for live prices

### Tools

#### `get_stock_price`
Get current stock price and basic quote data.

```json
{
  "name": "get_stock_price",
  "description": "Get real-time stock price and quote data",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbol": {
        "type": "string",
        "description": "Stock ticker symbol (e.g., AAPL)"
      },
      "includeExtendedHours": {
        "type": "boolean",
        "description": "Include pre/post market data",
        "default": false
      }
    },
    "required": ["symbol"]
  }
}
```

**Example Response:**
```json
{
  "symbol": "AAPL",
  "price": 185.64,
  "change": 2.34,
  "changePercent": 1.28,
  "volume": 52438921,
  "marketCap": 2850000000000,
  "peRatio": 28.5,
  "52WeekHigh": 199.62,
  "52WeekLow": 164.08,
  "timestamp": "2026-03-07T14:30:00Z"
}
```

#### `get_historical_prices`
Get historical OHLCV data for charting and analysis.

```json
{
  "name": "get_historical_prices",
  "description": "Get historical stock prices",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbol": { "type": "string" },
      "timeframe": {
        "type": "string",
        "enum": ["1min", "5min", "15min", "1h", "1d", "1wk", "1mo"],
        "default": "1d"
      },
      "startDate": { "type": "string", "format": "date" },
      "endDate": { "type": "string", "format": "date" },
      "limit": { "type": "integer", "default": 100 }
    },
    "required": ["symbol"]
  }
}
```

#### `get_company_profile`
Get company metadata, sector, employees, description.

```json
{
  "name": "get_company_profile",
  "description": "Get company information and metadata",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbol": { "type": "string" },
      "includePeers": { "type": "boolean", "default": true }
    },
    "required": ["symbol"]
  }
}
```

**Example Response:**
```json
{
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "sector": "Technology",
  "industry": "Consumer Electronics",
  "employees": 161000,
  "ceo": "Tim Cook",
  "description": "Apple designs, manufactures, and markets smartphones...",
  "website": "https://www.apple.com",
  "peers": ["MSFT", "GOOGL", "META", "AMZN"],
  "marketCap": 2850000000000,
  "enterpriseValue": 2900000000000
}
```

#### `get_financial_ratios`
Get key valuation and profitability ratios.

```json
{
  "name": "get_financial_ratios",
  "description": "Get financial ratios and metrics",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbol": { "type": "string" },
      "period": { "type": "string", "enum": ["ttm", "annual", "quarterly"], "default": "ttm" }
    },
    "required": ["symbol"]
  }
}
```

**Example Response:**
```json
{
  "symbol": "AAPL",
  "period": "ttm",
  "valuation": {
    "peRatio": 28.5,
    "forwardPE": 26.2,
    "pegRatio": 2.1,
    "priceToBook": 45.2,
    "priceToSales": 7.3,
    "evToEbitda": 21.4,
    "evToRevenue": 7.5
  },
  "profitability": {
    "grossMargin": 0.448,
    "operatingMargin": 0.302,
    "netMargin": 0.253,
    "roe": 1.60,
    "roa": 0.22,
    "roic": 0.45
  },
  "growth": {
    "revenueGrowth": 0.02,
    "earningsGrowth": 0.08,
    "bookValueGrowth": 0.05
  }
}
```

#### `screen_stocks`
Screen stocks based on criteria.

```json
{
  "name": "screen_stocks",
  "description": "Screen stocks by criteria",
  "inputSchema": {
    "type": "object",
    "properties": {
      "marketCapMin": { "type": "number" },
      "marketCapMax": { "type": "number" },
      "sector": { "type": "string" },
      "peMin": { "type": "number" },
      "peMax": { "type": "number" },
      "dividendYieldMin": { "type": "number" },
      "limit": { "type": "integer", "default": 50 }
    }
  }
}
```

### Configuration

```json
{
  "mcpServers": {
    "market-data": {
      "command": "python3",
      "args": ["mcp-servers/market-data-server.py"],
      "env": {
        "POLYGON_API_KEY": "your_polygon_key",
        "ALPACA_API_KEY": "your_alpaca_key",
        "ALPACA_SECRET_KEY": "your_alpaca_secret",
        "CACHE_DURATION": "300"
      }
    }
  }
}
```

---

## Server 2: SEC EDGAR MCP Server

### Purpose
Access company filings, financial statements, and insider trading data from SEC EDGAR.

### Data Source
- SEC EDGAR API (official)
- sec-api.io (enhanced API)

### Tools

#### `get_company_filings`
Get list of recent SEC filings for a company.

```json
{
  "name": "get_company_filings",
  "description": "Get SEC filings for a company",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticker": { "type": "string" },
      "formTypes": {
        "type": "array",
        "items": { "type": "string" },
        "description": "10-K, 10-Q, 8-K, DEF 14A, etc."
      },
      "limit": { "type": "integer", "default": 10 }
    },
    "required": ["ticker"]
  }
}
```

**Example Response:**
```json
{
  "ticker": "AAPL",
  "filings": [
    {
      "form": "10-Q",
      "filingDate": "2026-02-07",
      "periodEnd": "2025-12-31",
      "accessionNumber": "0000320193-26-000015",
      "url": "https://www.sec.gov/Archives/edgar/..."
    }
  ]
}
```

#### `get_financial_statements`
Get standardized financial statements.

```json
{
  "name": "get_financial_statements",
  "description": "Get income statement, balance sheet, or cash flow",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticker": { "type": "string" },
      "statement": {
        "type": "string",
        "enum": ["income", "balance", "cashflow"]
      },
      "period": { "type": "string", "enum": ["annual", "quarterly"], "default": "annual" },
      "years": { "type": "integer", "default": 5 }
    },
    "required": ["ticker", "statement"]
  }
}
```

**Example Response:**
```json
{
  "ticker": "AAPL",
  "statement": "income",
  "period": "annual",
  "data": [
    {
      "fiscalYear": 2025,
      "revenue": 391035000000,
      "costOfRevenue": 210352000000,
      "grossProfit": 180683000000,
      "operatingExpenses": 54887000000,
      "operatingIncome": 125796000000,
      "netIncome": 93736000000,
      "eps": 6.08,
      "sharesOutstanding": 15400000000
    }
  ]
}
```

#### `get_key_metrics`
Get standardized financial metrics (revenue, EBITDA, etc.).

```json
{
  "name": "get_key_metrics",
  "description": "Get key financial metrics from filings",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticker": { "type": "string" },
      "metrics": {
        "type": "array",
        "items": { "type": "string" },
        "description": "revenue, ebitda, netIncome, freeCashFlow, etc."
      },
      "period": { "type": "string", "enum": ["ttm", "annual", "quarterly"] }
    },
    "required": ["ticker"]
  }
}
```

#### `get_insider_trading`
Get insider trading activity.

```json
{
  "name": "get_insider_trading",
  "description": "Get Form 4 insider trading filings",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticker": { "type": "string" },
      "days": { "type": "integer", "default": 90 }
    },
    "required": ["ticker"]
  }
}
```

#### `search_companies`
Search for companies by name or CIK.

```json
{
  "name": "search_companies",
  "description": "Search SEC database for companies",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "limit": { "type": "integer", "default": 10 }
    },
    "required": ["query"]
  }
}
```

### Configuration

```json
{
  "mcpServers": {
    "sec-edgar": {
      "command": "python3",
      "args": ["mcp-servers/sec-edgar-server.py"],
      "env": {
        "SEC_API_KEY": "your_sec_api_key",
        "SEC_USER_AGENT": "YourName your@email.com"
      }
    }
  }
}
```

---

## Server 3: Estimates MCP Server

### Purpose
Access analyst estimates, earnings calendars, and recommendation trends.

### Data Sources
- Visible Alpha
- FactSet
- Bloomberg (if available)
- Earnings Whispers

### Tools

#### `get_earnings_estimates`
Get analyst EPS and revenue estimates.

```json
{
  "name": "get_earnings_estimates",
  "description": "Get analyst estimates for upcoming earnings",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticker": { "type": "string" },
      "period": { "type": "string", "description": "Q1-2026, FY2026, etc." }
    },
    "required": ["ticker"]
  }
}
```

**Example Response:**
```json
{
  "ticker": "AAPL",
  "quarter": "Q1-2026",
  "periodEnd": "2025-12-31",
  "eps": {
    "estimate": 2.15,
    "high": 2.35,
    "low": 1.95,
    "numEstimates": 28,
    "revisionTrend": "up",
    "lastRevision": "2026-02-28"
  },
  "revenue": {
    "estimate": 123500000000,
    "high": 128000000000,
    "low": 119000000000,
    "numEstimates": 25
  },
  "surpriseHistory": [
    {"quarter": "Q4-2025", "estimate": 1.60, "actual": 1.64, "surprise": 0.04}
  ]
}
```

#### `get_price_targets`
Get analyst price targets.

```json
{
  "name": "get_price_targets",
  "description": "Get analyst price targets and recommendations",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticker": { "type": "string" }
    },
    "required": ["ticker"]
  }
}
```

**Example Response:**
```json
{
  "ticker": "AAPL",
  "currentPrice": 185.64,
  "priceTarget": {
    "mean": 210.00,
    "median": 215.00,
    "high": 250.00,
    "low": 165.00,
    "numAnalysts": 35
  },
  "upside": 13.1,
  "recommendations": {
    "buy": 26,
    "hold": 8,
    "sell": 1,
    "consensus": "Buy"
  }
}
```

#### `get_earnings_calendar`
Get upcoming earnings announcements.

```json
{
  "name": "get_earnings_calendar",
  "description": "Get earnings calendar for date range",
  "inputSchema": {
    "type": "object",
    "properties": {
      "startDate": { "type": "string", "format": "date" },
      "endDate": { "type": "string", "format": "date" },
      "tickers": {
        "type": "array",
        "items": { "type": "string" },
        "description": "Specific tickers to check"
      },
      "minMarketCap": { "type": "number" }
    }
  }
}
```

#### `get_recommendation_trends`
Get recommendation changes over time.

```json
{
  "name": "get_recommendation_trends",
  "description": "Get analyst recommendation history",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticker": { "type": "string" },
      "months": { "type": "integer", "default": 6 }
    },
    "required": ["ticker"]
  }
}
```

### Configuration

```json
{
  "mcpServers": {
    "estimates": {
      "command": "python3",
      "args": ["mcp-servers/estimates-server.py"],
      "env": {
        "VISIBLE_ALPHA_API_KEY": "your_key",
        "EARNINGS_WHISPERS_KEY": "your_key"
      }
    }
  }
}
```

---

## Server 4: M&A Transactions MCP Server

### Purpose
Access precedent transactions, deal terms, and M&A multiples.

### Data Sources
- PitchBook
- Preqin
- SDC Platinum
- MergerMarket
- Public filings for announced deals

### Tools

#### `search_precedent_transactions`
Search for comparable M&A transactions.

```json
{
  "name": "search_precedent_transactions",
  "description": "Search M&A transaction database",
  "inputSchema": {
    "type": "object",
    "properties": {
      "industry": { "type": "string" },
      "sector": { "type": "string" },
      "dealSizeMin": { "type": "number" },
      "dealSizeMax": { "type": "number" },
      "years": { "type": "integer", "default": 5 },
      "acquirerType": { "type": "string", "enum": ["strategic", "financial", "all"] },
      "limit": { "type": "integer", "default": 20 }
    }
  }
}
```

**Example Response:**
```json
{
  "query": {
    "industry": "Software",
    "dealSizeMin": 1000000000,
    "dealSizeMax": 10000000000,
    "years": 3
  },
  "results": [
    {
      "date": "2025-06-15",
      "target": "Workday Competitor Inc",
      "acquirer": "Salesforce",
      "enterpriseValue": 5200000000,
      "revenue": 1200000000,
      "ebitda": 280000000,
      "evToRevenue": 4.3,
      "evToEbitda": 18.6,
      "premium": 32,
      "description": "Strategic acquisition to expand HR software"
    }
  ],
  "statistics": {
    "count": 45,
    "medianEvToRevenue": 5.2,
    "medianEvToEbitda": 19.5,
    "medianPremium": 28
  }
}
```

#### `get_deal_details`
Get detailed information about a specific transaction.

```json
{
  "name": "get_deal_details",
  "description": "Get detailed M&A transaction information",
  "inputSchema": {
    "type": "object",
    "properties": {
      "dealId": { "type": "string" }
    },
    "required": ["dealId"]
  }
}
```

#### `get_ma_multiples`
Get current M&A multiples by sector.

```json
{
  "name": "get_ma_multiples",
  "description": "Get median M&A multiples by sector",
  "inputSchema": {
    "type": "object",
    "properties": {
      "sector": { "type": "string" },
      "subSector": { "type": "string" },
      "dealSizeRange": { "type": "string" },
      "region": { "type": "string", "default": "North America" }
    },
    "required": ["sector"]
  }
}
```

**Example Response:**
```json
{
  "sector": "Software",
  "subSector": "SaaS",
  "data": {
    "evToRevenue": {
      "median": 6.5,
      "mean": 7.2,
      "range": { "low": 3.0, "high": 15.0 }
    },
    "evToEbitda": {
      "median": 22.0,
      "mean": 25.5,
      "range": { "low": 12.0, "high": 45.0 }
    }
  }
}
```

### Configuration

```json
{
  "mcpServers": {
    "ma-transactions": {
      "command": "python3",
      "args": ["mcp-servers/ma-transactions-server.py"],
      "env": {
        "PITCHBOOK_API_KEY": "your_key",
        "PREQUIN_API_KEY": "your_key"
      }
    }
  }
}
```

---

## Server 5: News & Sentiment MCP Server

### Purpose
Access financial news, earnings transcripts, and sentiment analysis.

### Data Sources
- Bloomberg (if available)
- Reuters
- SEC filing sentiment
- Earnings call transcripts
- Twitter/X financial sentiment

### Tools

#### `get_company_news`
Get recent news for a company.

```json
{
  "name": "get_company_news",
  "description": "Get recent news articles about a company",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticker": { "type": "string" },
      "days": { "type": "integer", "default": 7 },
      "includeSentiment": { "type": "boolean", "default": true }
    },
    "required": ["ticker"]
  }
}
```

**Example Response:**
```json
{
  "ticker": "AAPL",
  "articles": [
    {
      "title": "Apple announces new AI features for iPhone",
      "source": "TechCrunch",
      "date": "2026-03-05T10:30:00Z",
      "summary": "Apple unveiled new on-device AI capabilities...",
      "sentiment": "positive",
      "sentimentScore": 0.72,
      "url": "https://techcrunch.com/..."
    }
  ],
  "sentimentSummary": {
    "positive": 8,
    "neutral": 5,
    "negative": 2,
    "overall": "positive"
  }
}
```

#### `get_earnings_transcript`
Get earnings call transcript.

```json
{
  "name": "get_earnings_transcript",
  "description": "Get earnings call transcript",
  "inputSchema": {
    "type": "object",
    "properties": {
      "ticker": { "type": "string" },
      "quarter": { "type": "string", "description": "Q1-2026, FY2025, etc." },
      "section": {
        "type": "string",
        "enum": ["prepared", "qa", "full"],
        "default": "full"
      }
    },
    "required": ["ticker", "quarter"]
  }
}
```

#### `analyze_sentiment`
Analyze sentiment of text or document.

```json
{
  "name": "analyze_sentiment",
  "description": "Analyze sentiment of financial text",
  "inputSchema": {
    "type": "object",
    "properties": {
      "text": { "type": "string" },
      "context": { "type": "string", "enum": ["earnings", "news", "social"], "default": "news" }
    },
    "required": ["text"]
  }
}
```

#### `get_market_sentiment`
Get overall market sentiment indicators.

```json
{
  "name": "get_market_sentiment",
  "description": "Get market-wide sentiment indicators",
  "inputSchema": {
    "type": "object",
    "properties": {
      "index": { "type": "string", "enum": ["SPY", "QQQ", "VIX"], "default": "SPY" }
    }
  }
}
```

### Configuration

```json
{
  "mcpServers": {
    "news-sentiment": {
      "command": "python3",
      "args": ["mcp-servers/news-sentiment-server.py"],
      "env": {
        "NEWS_API_KEY": "your_key",
        "OPENAI_API_KEY": "for_sentiment_analysis"
      }
    }
  }
}
```

---

## Server 6: Economic Data MCP Server

### Purpose
Access macroeconomic indicators and industry data.

### Data Sources
- FRED (Federal Reserve Economic Data)
- World Bank
- IMF
- BLS (Bureau of Labor Statistics)

### Tools

#### `get_economic_indicator`
Get macroeconomic data.

```json
{
  "name": "get_economic_indicator",
  "description": "Get economic indicator time series",
  "inputSchema": {
    "type": "object",
    "properties": {
      "indicator": {
        "type": "string",
        "enum": ["GDP", "CPI", "UNEMPLOYMENT", "FED_RATE", "TREASURY_10Y", "INDUSTRIAL_PRODUCTION"]
      },
      "startDate": { "type": "string", "format": "date" },
      "endDate": { "type": "string", "format": "date" },
      "frequency": { "type": "string", "enum": ["daily", "monthly", "quarterly", "annual"], "default": "monthly" }
    },
    "required": ["indicator"]
  }
}
```

#### `get_industry_data`
Get industry-specific economic data.

```json
{
  "name": "get_industry_data",
  "description": "Get industry growth, margins, and trends",
  "inputSchema": {
    "type": "object",
    "properties": {
      "industry": { "type": "string" },
      "naicsCode": { "type": "string" },
      "metrics": {
        "type": "array",
        "items": { "type": "string" },
        "description": "revenue_growth, profit_margin, capex, etc."
      }
    },
    "required": ["industry"]
  }
}
```

### Configuration

```json
{
  "mcpServers": {
    "economic-data": {
      "command": "python3",
      "args": ["mcp-servers/economic-data-server.py"],
      "env": {
        "FRED_API_KEY": "your_fred_key"
      }
    }
  }
}
```

---

## Integration with Financial Skills

### Example: Automated Comps with Live Data

**Before MCP (Manual):**
```
User: "Value TechFlow Inc"
AI: "I need you to provide competitor data..."
User provides data manually
AI runs model
```

**With MCP (Automated):**
```
User: "Value TechFlow Inc"
AI: [Calls market-data server]
AI: [Gets company profile - finds peers automatically]
AI: [Gets financial ratios for all peers]
AI: [Calls sec-edgar server]
AI: [Gets financial statements]
AI: [Runs generate-comps.py with live data]
AI: "Based on live market data, TechFlow is worth $480-520M..."
```

### Skill Enhancement Examples

#### Enhanced Valuation Skill

```python
# Pseudo-code for enhanced generate-comps.py with MCP

async def generate_comps_with_live_data(target_ticker):
    # Get target company info
    target_profile = await mcp_client.call("get_company_profile", {
        "symbol": target_ticker,
        "includePeers": True
    })
    
    # Get peer companies automatically
    peers = target_profile["peers"][:5]  # Top 5 competitors
    
    # Get financial data for all peers
    peer_data = []
    for peer in peers:
        ratios = await mcp_client.call("get_financial_ratios", {
            "symbol": peer,
            "period": "ttm"
        })
        peer_data.append(ratios)
    
    # Generate Excel model with live data
    generate_comps_excel(target_ticker, peer_data)
```

#### Enhanced M&A Skill

```python
# Auto-populate buyer list with live data

async def generate_buyer_list_with_data(company_profile):
    # Search precedent transactions
    transactions = await mcp_client.call("search_precedent_transactions", {
        "industry": company_profile["industry"],
        "dealSizeMin": company_profile["revenue"] * 3,
        "dealSizeMax": company_profile["revenue"] * 10,
        "years": 3
    })
    
    # Identify active acquirers
    active_acquirers = extract_acquirers(transactions)
    
    # Get current market data for each
    for acquirer in active_acquirers:
        profile = await mcp_client.call("get_company_profile", {
            "symbol": acquirer["ticker"]
        })
        # Add to buyer list
```

#### Enhanced Equity Research Skill

```python
# Auto-generate earnings update

async def generate_earnings_update(ticker):
    # Get latest earnings
    estimates = await mcp_client.call("get_earnings_estimates", {
        "ticker": ticker
    })
    
    # Get actual results from SEC
    filings = await mcp_client.call("get_company_filings", {
        "ticker": ticker,
        "formTypes": ["8-K"],
        "limit": 1
    })
    
    # Compare actual vs estimate
    surprise = calculate_surprise(actual, estimates)
    
    # Get news sentiment
    news = await mcp_client.call("get_company_news", {
        "ticker": ticker,
        "days": 1
    })
    
    # Generate report
    return format_earnings_update(ticker, surprise, news)
```

---

## Configuration File

Complete `.mcp.json` configuration:

```json
{
  "mcpServers": {
    "market-data": {
      "command": "python3",
      "args": ["${workspaceFolder}/mcp-servers/market-data-server.py"],
      "env": {
        "POLYGON_API_KEY": "${env:POLYGON_API_KEY}",
        "ALPACA_API_KEY": "${env:ALPACA_API_KEY}",
        "ALPACA_SECRET_KEY": "${env:ALPACA_SECRET_KEY}"
      },
      "disabled": false,
      "autoApprove": ["get_stock_price", "get_historical_prices"]
    },
    "sec-edgar": {
      "command": "python3",
      "args": ["${workspaceFolder}/mcp-servers/sec-edgar-server.py"],
      "env": {
        "SEC_API_KEY": "${env:SEC_API_KEY}",
        "SEC_USER_AGENT": "YourName your@email.com"
      },
      "disabled": false,
      "autoApprove": ["get_financial_statements", "get_key_metrics"]
    },
    "estimates": {
      "command": "python3",
      "args": ["${workspaceFolder}/mcp-servers/estimates-server.py"],
      "env": {
        "VISIBLE_ALPHA_API_KEY": "${env:VISIBLE_ALPHA_API_KEY}"
      },
      "disabled": false
    },
    "ma-transactions": {
      "command": "python3",
      "args": ["${workspaceFolder}/mcp-servers/ma-transactions-server.py"],
      "env": {
        "PITCHBOOK_API_KEY": "${env:PITCHBOOK_API_KEY}"
      },
      "disabled": false
    },
    "news-sentiment": {
      "command": "python3",
      "args": ["${workspaceFolder}/mcp-servers/news-sentiment-server.py"],
      "env": {
        "NEWS_API_KEY": "${env:NEWS_API_KEY}",
        "OPENAI_API_KEY": "${env:OPENAI_API_KEY}"
      },
      "disabled": false
    },
    "economic-data": {
      "command": "python3",
      "args": ["${workspaceFolder}/mcp-servers/economic-data-server.py"],
      "env": {
        "FRED_API_KEY": "${env:FRED_API_KEY}"
      },
      "disabled": false
    }
  }
}
```

---

## API Provider Recommendations

### Free Tier Options

| Data Type | Provider | Free Tier | Notes |
|-----------|----------|-----------|-------|
| Market Data | Massive (formerly Massive/Polygon.io) | 5 API calls/min | Good for development |
| Market Data | Alpaca | Unlimited | Requires account |
| SEC Filings | SEC EDGAR | Unlimited | Official, slightly slower |
| SEC Enhanced | sec-api.io | 100 calls/month | Better structured data |
| Economic | FRED | Unlimited | Federal Reserve data |
| News | NewsAPI | 100 requests/day | Basic news coverage |

### Paid Tier Recommendations

| Data Type | Provider | Cost | Quality |
|-----------|----------|------|---------|
| Market Data | Bloomberg API | $$$$ | Institutional grade |
| Market Data | Refinitiv | $$$ | Professional |
| Estimates | Visible Alpha | $$ | Best-in-class |
| Estimates | FactSet | $$$ | Industry standard |
| M&A | PitchBook | $$$ | Comprehensive |
| M&A | Preqin | $$ | Private markets focus |
| News | Bloomberg | $$$$ | Real-time professional |

---

## Implementation Roadmap

### Phase 1: Core Market Data (2-3 weeks)
- [ ] Market Data MCP Server (Massive (formerly Massive/Polygon.io))
- [ ] Basic stock prices and ratios
- [ ] Integration with generate-comps.py

### Phase 2: Financial Statements (2 weeks)
- [ ] SEC EDGAR MCP Server
- [ ] Automated financial data fetching
- [ ] Integration with DCF model

### Phase 3: Estimates & Research (2 weeks)
- [ ] Estimates MCP Server
- [ ] Earnings calendar integration
- [ ] Enhanced equity research workflows

### Phase 4: M&A Data (2 weeks)
- [ ] M&A Transactions MCP Server
- [ ] Precedent transaction search
- [ ] Automated buyer identification

### Phase 5: Advanced Features (3 weeks)
- [ ] News & Sentiment MCP Server
- [ ] Economic Data MCP Server
- [ ] Cross-server analytics
- [ ] Automated report generation

---

## Security Considerations

### API Key Management
```bash
# Use environment variables, never hardcode keys
export POLYGON_API_KEY="your_key_here"
export SEC_API_KEY="your_key_here"
```

### Rate Limiting
- Implement caching to reduce API calls
- Respect provider rate limits
- Queue requests during high load

### Data Privacy
- Don't log sensitive financial data
- Encrypt API keys at rest
- Use HTTPS for all API calls

---

## Error Handling

### Common Errors and Responses

```python
{
  "error": {
    "type": "RATE_LIMIT_EXCEEDED",
    "message": "Massive/Polygon API rate limit reached. Retrying in 60 seconds.",
    "retryable": true,
    "retryAfter": 60
  }
}

{
  "error": {
    "type": "DATA_NOT_AVAILABLE",
    "message": "No financial data available for ticker XYZ",
    "retryable": false,
    "fallback": "Using manual input mode"
  }
}
```

---

## Conclusion

This MCP integration design enables the financial skills ecosystem to access live market data, transforming manual analysis workflows into automated, data-driven processes. The modular server architecture allows incremental implementation and easy swapping of data providers.

**Key Benefits:**
- ⚡ Real-time data access
- 🤖 Automated data population
- 📊 Enhanced accuracy
- 🔄 Always up-to-date analysis
- 🌍 Multiple data source fallbacks
