# MCP Server Implementation Guide

Practical implementation examples for financial data MCP servers.

---

## Server Implementation: Market Data MCP Server

### File: `mcp-servers/market-data-server.py`

```python
#!/usr/bin/env python3
"""
MCP Server for Market Data
Provides real-time stock prices, historical data, and company profiles.

Data Sources: Massive (formerly Massive/Polygon.io), Alpaca Markets
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import aiohttp
from mcp.server import Server
from mcp.types import Tool, TextContent

# Initialize MCP Server
app = Server("market-data-server")

# API Configuration
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

# Cache for reducing API calls
_cache = {}
_cache_ttl = 300  # 5 minutes

async def polygon_request(endpoint: str, params: Dict = None) -> Dict:
    """Make request to Massive (formerly Massive/Polygon.io) API."""
    base_url = "https://api.polygon.io/v2"
    url = f"{base_url}/{endpoint}"
    
    if params is None:
        params = {}
    params["apiKey"] = POLYGON_API_KEY
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise Exception(f"Massive/Polygon API error: {resp.status}")

async def alpaca_request(endpoint: str) -> Dict:
    """Make request to Alpaca API."""
    base_url = "https://data.alpaca.markets/v2"
    url = f"{base_url}/{endpoint}"
    
    headers = {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise Exception(f"Alpaca API error: {resp.status}")

# Define available tools
@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="get_stock_price",
            description="Get real-time stock price and quote data",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock ticker symbol (e.g., AAPL)"
                    },
                    "includeExtendedHours": {
                        "type": "boolean",
                        "description": "Include pre/post market data",
                        "default": False
                    }
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_historical_prices",
            description="Get historical stock prices (OHLCV)",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "timeframe": {
                        "type": "string",
                        "enum": ["1d", "1wk", "1mo"],
                        "default": "1d"
                    },
                    "days": {"type": "integer", "default": 252},
                    "startDate": {"type": "string"},
                    "endDate": {"type": "string"}
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_company_profile",
            description="Get company information and metadata",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "includePeers": {"type": "boolean", "default": True}
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="get_financial_ratios",
            description="Get financial ratios and metrics",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "period": {"type": "string", "enum": ["ttm", "annual"], "default": "ttm"}
                },
                "required": ["symbol"]
            }
        ),
        Tool(
            name="screen_stocks",
            description="Screen stocks by criteria",
            inputSchema={
                "type": "object",
                "properties": {
                    "marketCapMin": {"type": "number"},
                    "marketCapMax": {"type": "number"},
                    "sector": {"type": "string"},
                    "peMin": {"type": "number"},
                    "peMax": {"type": "number"},
                    "limit": {"type": "integer", "default": 50}
                }
            }
        )
    ]

# Implement tool handlers
@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    
    if name == "get_stock_price":
        symbol = arguments["symbol"].upper()
        
        # Check cache
        cache_key = f"price_{symbol}"
        if cache_key in _cache:
            cached_time, data = _cache[cache_key]
            if datetime.now() - cached_time < timedelta(seconds=_cache_ttl):
                return [TextContent(type="text", text=json.dumps(data, indent=2))]
        
        try:
            # Fetch from Massive/Polygon
            data = await polygon_request(f"aggs/ticker/{symbol}/prev")
            result = data.get("results", [{}])[0]
            
            # Get additional quote data
            quote = await polygon_request(f"last/trade/{symbol}")
            
            response = {
                "symbol": symbol,
                "price": result.get("c"),  # Close price
                "open": result.get("o"),
                "high": result.get("h"),
                "low": result.get("l"),
                "volume": result.get("v"),
                "vwap": result.get("vw"),
                "change": result.get("c", 0) - result.get("o", 0),
                "timestamp": datetime.fromtimestamp(result.get("t", 0) / 1000).isoformat()
            }
            
            # Cache result
            _cache[cache_key] = (datetime.now(), response)
            
            return [TextContent(type="text", text=json.dumps(response, indent=2))]
            
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    
    elif name == "get_historical_prices":
        symbol = arguments["symbol"].upper()
        timeframe = arguments.get("timeframe", "1d")
        days = arguments.get("days", 252)
        
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Map timeframe to multiplier and timespan
            multiplier_map = {"1d": (1, "day"), "1wk": (1, "week"), "1mo": (1, "month")}
            multiplier, timespan = multiplier_map.get(timeframe, (1, "day"))
            
            # Fetch from Massive/Polygon
            endpoint = f"aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{start_date.strftime('%Y-%m-%d')}/{end_date.strftime('%Y-%m-%d')}"
            data = await polygon_request(endpoint)
            
            results = data.get("results", [])
            formatted = [
                {
                    "date": datetime.fromtimestamp(r["t"] / 1000).strftime("%Y-%m-%d"),
                    "open": r["o"],
                    "high": r["h"],
                    "low": r["l"],
                    "close": r["c"],
                    "volume": r["v"],
                    "vwap": r.get("vw")
                }
                for r in results
            ]
            
            return [TextContent(type="text", text=json.dumps({
                "symbol": symbol,
                "timeframe": timeframe,
                "count": len(formatted),
                "data": formatted
            }, indent=2))]
            
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    
    elif name == "get_company_profile":
        symbol = arguments["symbol"].upper()
        include_peers = arguments.get("includePeers", True)
        
        try:
            # Fetch company details from Massive/Polygon
            data = await polygon_request(f"reference/tickers/{symbol}")
            ticker_info = data.get("results", {})
            
            response = {
                "symbol": symbol,
                "name": ticker_info.get("name"),
                "sector": ticker_info.get("sic_sector"),
                "industry": ticker_info.get("sic_industry"),
                "marketCap": ticker_info.get("market_cap"),
                "employees": ticker_info.get("total_employees"),
                "description": ticker_info.get("description"),
                "homepage": ticker_info.get("homepage_url"),
                "listDate": ticker_info.get("list_date"),
                "exchange": ticker_info.get("primary_exchange")
            }
            
            # Add peers if requested
            if include_peers:
                # This would come from a peer database
                # For now, return empty list
                response["peers"] = []
            
            return [TextContent(type="text", text=json.dumps(response, indent=2))]
            
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    
    elif name == "get_financial_ratios":
        symbol = arguments["symbol"].upper()
        
        try:
            # Fetch financials from Massive/Polygon
            data = await polygon_request(f"reference/financials/{symbol}", {"limit": 1})
            financials = data.get("results", [{}])[0].get("financials", {})
            
            # Extract key metrics
            income = financials.get("income_statement", {})
            balance = financials.get("balance_sheet", {})
            
            response = {
                "symbol": symbol,
                "period": "ttm",
                "valuation": {
                    "peRatio": None,  # Would need stock price
                    "priceToBook": None,
                    "evToRevenue": None,
                    "evToEbitda": None
                },
                "profitability": {
                    "grossMargin": income.get("gross_profit_ratio"),
                    "operatingMargin": income.get("operating_income_ratio"),
                    "netMargin": income.get("net_income_ratio")
                },
                "financialHealth": {
                    "currentRatio": None,
                    "debtToEquity": None,
                    "quickRatio": None
                },
                "raw": financials  # Include raw data for advanced use
            }
            
            return [TextContent(type="text", text=json.dumps(response, indent=2))]
            
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    
    elif name == "screen_stocks":
        # This would require a stock screener API
        # For now, return error
        return [TextContent(type="text", text=json.dumps({
            "error": "Stock screening not yet implemented. Use get_company_profile for individual stocks."
        }))]
    
    else:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

# Run the server
if __name__ == "__main__":
    import sys
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(main())
```

---

## Server Implementation: SEC EDGAR MCP Server

### File: `mcp-servers/sec-edgar-server.py`

```python
#!/usr/bin/env python3
"""
MCP Server for SEC EDGAR Data
Provides access to company filings and financial statements.

Data Sources: SEC EDGAR API, sec-api.io (enhanced)
"""

import os
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Any
import aiohttp
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("sec-edgar-server")

SEC_API_KEY = os.getenv("SEC_API_KEY")  # From sec-api.io
SEC_USER_AGENT = os.getenv("SEC_USER_AGENT", "FinancialSkills MCP")

# SEC requires proper User-Agent
SEC_HEADERS = {"User-Agent": SEC_USER_AGENT}

async def sec_api_request(endpoint: str, params: Dict = None) -> Dict:
    """Make request to sec-api.io (enhanced SEC API)."""
    base_url = "https://api.sec-api.io"
    
    if params is None:
        params = {}
    params["token"] = SEC_API_KEY
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{base_url}/{endpoint}", params=params) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise Exception(f"SEC API error: {resp.status}")

async def edgar_request(cik: str, endpoint: str = None) -> Dict:
    """Make request to official SEC EDGAR API."""
    base_url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, headers=SEC_HEADERS) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise Exception(f"EDGAR API error: {resp.status}")

@app.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="get_company_filings",
            description="Get recent SEC filings for a company",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"},
                    "formTypes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "10-K, 10-Q, 8-K, DEF 14A"
                    },
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="get_financial_statements",
            description="Get standardized financial statements",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"},
                    "statement": {
                        "type": "string",
                        "enum": ["income", "balance", "cashflow"]
                    },
                    "period": {"type": "string", "enum": ["annual", "quarterly"], "default": "annual"},
                    "years": {"type": "integer", "default": 5}
                },
                "required": ["ticker", "statement"]
            }
        ),
        Tool(
            name="get_key_metrics",
            description="Get key financial metrics from filings",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticker": {"type": "string"},
                    "metrics": {"type": "array", "items": {"type": "string"}},
                    "period": {"type": "string", "enum": ["ttm", "annual", "quarterly"]}
                },
                "required": ["ticker"]
            }
        ),
        Tool(
            name="search_companies",
            description="Search SEC database for companies",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> List[TextContent]:
    
    if name == "get_company_filings":
        ticker = arguments["ticker"].upper()
        form_types = arguments.get("formTypes", [])
        limit = arguments.get("limit", 10)
        
        try:
            # Use sec-api.io for better structured data
            if SEC_API_KEY:
                query = f"ticker:{ticker}"
                if form_types:
                    query += f" AND ({' OR '.join(formTypes)})"
                
                data = await sec_api_request("filings", {
                    "q": query,
                    "size": limit
                })
                
                filings = data.get("filings", [])
                formatted = [
                    {
                        "form": f.get("formType"),
                        "filingDate": f.get("filedAt", "").split("T")[0],
                        "periodEnd": f.get("periodOfReport", "").split("T")[0],
                        "accessionNumber": f.get("accessionNo"),
                        "url": f"https://www.sec.gov/Archives/edgar/data/{f.get('cik')}/{f.get('accessionNo').replace('-', '')}/{f.get('primaryDocHref')}"
                    }
                    for f in filings
                ]
                
                return [TextContent(type="text", text=json.dumps({
                    "ticker": ticker,
                    "count": len(formatted),
                    "filings": formatted
                }, indent=2))]
            else:
                return [TextContent(type="text", text=json.dumps({
                    "error": "SEC API key not configured. Set SEC_API_KEY environment variable."
                }))]
                
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    
    elif name == "get_financial_statements":
        ticker = arguments["ticker"].upper()
        statement_type = arguments["statement"]
        period = arguments.get("period", "annual")
        years = arguments.get("years", 5)
        
        try:
            if SEC_API_KEY:
                # Map statement type to API parameter
                statement_map = {
                    "income": "income_statement",
                    "balance": "balance_sheet",
                    "cashflow": "cash_flow_statement"
                }
                
                data = await sec_api_request(f"financial-statements/{ticker}")
                
                # Extract relevant statement
                statements = data.get(statement_map.get(statement_type), [])
                
                # Limit to requested years
                statements = statements[:years]
                
                return [TextContent(type="text", text=json.dumps({
                    "ticker": ticker,
                    "statement": statement_type,
                    "period": period,
                    "count": len(statements),
                    "data": statements
                }, indent=2))]
            else:
                return [TextContent(type="text", text=json.dumps({
                    "error": "SEC API key not configured"
                }))]
                
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    
    elif name == "get_key_metrics":
        ticker = arguments["ticker"].upper()
        
        try:
            if SEC_API_KEY:
                # Get company metrics
                data = await sec_api_request(f"company-metrics/{ticker}")
                
                return [TextContent(type="text", text=json.dumps({
                    "ticker": ticker,
                    "metrics": data
                }, indent=2))]
            else:
                return [TextContent(type="text", text=json.dumps({
                    "error": "SEC API key not configured"
                }))]
                
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    
    elif name == "search_companies":
        query = arguments["query"]
        limit = arguments.get("limit", 10)
        
        try:
            # Use SEC API to search
            if SEC_API_KEY:
                data = await sec_api_request("companies/search", {
                    "q": query,
                    "size": limit
                })
                
                companies = data.get("companies", [])
                formatted = [
                    {
                        "ticker": c.get("ticker"),
                        "name": c.get("name"),
                        "cik": c.get("cik"),
                        "sector": c.get("sicSector"),
                        "industry": c.get("sicIndustry")
                    }
                    for c in companies
                ]
                
                return [TextContent(type="text", text=json.dumps({
                    "query": query,
                    "count": len(formatted),
                    "companies": formatted
                }, indent=2))]
            else:
                return [TextContent(type="text", text=json.dumps({
                    "error": "SEC API key not configured"
                }))]
                
        except Exception as e:
            return [TextContent(type="text", text=json.dumps({"error": str(e)}))]
    
    else:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    
    asyncio.run(main())
```

---

## Integration Example: Enhanced Comps Generator

### File: `mcp-integrations/enhanced_comps.py`

```python
#!/usr/bin/env python3
"""
Enhanced Comparable Company Analysis with MCP Live Data

This script integrates the generate-comps.py tool with MCP servers
to automatically populate data from live sources.
"""

import asyncio
import json
import argparse
from typing import List, Dict
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def get_company_data(session: ClientSession, symbol: str) -> Dict:
    """Fetch company data from MCP servers."""
    
    # Get stock price
    price_result = await session.call_tool("get_stock_price", {"symbol": symbol})
    price_data = json.loads(price_result.content[0].text)
    
    # Get company profile
    profile_result = await session.call_tool("get_company_profile", {"symbol": symbol})
    profile_data = json.loads(profile_result.content[0].text)
    
    # Get financial ratios
    ratios_result = await session.call_tool("get_financial_ratios", {"symbol": symbol})
    ratios_data = json.loads(ratios_result.content[0].text)
    
    # Get SEC financials
    sec_result = await session.call_tool("get_key_metrics", {"ticker": symbol})
    sec_data = json.loads(sec_result.content[0].text)
    
    return {
        "symbol": symbol,
        "name": profile_data.get("name"),
        "price": price_data.get("price"),
        "marketCap": price_data.get("marketCap") or profile_data.get("marketCap"),
        "sector": profile_data.get("sector"),
        "industry": profile_data.get("industry"),
        "peRatio": ratios_data.get("valuation", {}).get("peRatio"),
        "evToEbitda": ratios_data.get("valuation", {}).get("evToEbitda"),
        "financials": sec_data.get("metrics", {})
    }

async def generate_live_comps(target: str, peers: List[str]):
    """Generate comps analysis with live data."""
    
    # Start MCP servers
    market_data_params = StdioServerParameters(
        command="python3",
        args=["mcp-servers/market-data-server.py"],
        env={"POLYGON_API_KEY": "your_key"}
    )
    
    sec_params = StdioServerParameters(
        command="python3",
        args=["mcp-servers/sec-edgar-server.py"],
        env={"SEC_API_KEY": "your_key"}
    )
    
    async with stdio_client(market_data_params) as (market_read, market_write):
        async with ClientSession(market_read, market_write) as market_session:
            await market_session.initialize()
            
            async with stdio_client(sec_params) as (sec_read, sec_write):
                async with ClientSession(sec_read, sec_write) as sec_session:
                    await sec_session.initialize()
                    
                    # Fetch data for all companies
                    print(f"Fetching live data for {target}...")
                    target_data = await get_company_data(market_session, target)
                    
                    peer_data = []
                    for peer in peers:
                        print(f"Fetching data for {peer}...")
                        try:
                            data = await get_company_data(market_session, peer)
                            peer_data.append(data)
                        except Exception as e:
                            print(f"Error fetching {peer}: {e}")
                    
                    # Calculate multiples
                    print("\n" + "="*60)
                    print(f"COMPARABLE COMPANY ANALYSIS: {target}")
                    print("="*60)
                    print(f"\nTarget: {target_data['name']} ({target})")
                    print(f"Market Cap: ${target_data.get('marketCap', 0)/1e9:.1f}B")
                    print(f"Sector: {target_data.get('sector')}")
                    
                    print("\nPeer Comparison:")
                    print("-" * 60)
                    print(f"{'Company':<15} {'Price':>10} {'P/E':>8} {'EV/EBITDA':>10}")
                    print("-" * 60)
                    
                    for peer in peer_data:
                        print(f"{peer['symbol']:<15} ${peer.get('price', 0):>9.2f} "
                              f"{peer.get('peRatio') or 'N/A':>8} "
                              f"{peer.get('evToEbitda') or 'N/A':>10}")
                    
                    # Generate Excel with populated data
                    print("\nGenerating Excel model...")
                    # Here you would call generate-comps.py with the live data
                    # For now, just print the data
                    
                    return {
                        "target": target_data,
                        "peers": peer_data
                    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--peers", required=True, help="Comma-separated list")
    args = parser.parse_args()
    
    peers = [p.strip() for p in args.peers.split(",")]
    
    result = asyncio.run(generate_live_comps(args.target, peers))
    print("\nLive data fetched successfully!")
```

---

## Configuration: .mcp.json

```json
{
  "mcpServers": {
    "market-data": {
      "command": "python3",
      "args": ["mcp-servers/market-data-server.py"],
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
      "args": ["mcp-servers/sec-edgar-server.py"],
      "env": {
        "SEC_API_KEY": "${env:SEC_API_KEY}",
        "SEC_USER_AGENT": "FinancialSkills MCP"
      },
      "disabled": false,
      "autoApprove": ["get_financial_statements", "get_key_metrics"]
    }
  }
}
```

---

## Testing the Integration

```bash
# Start MCP server manually for testing
export POLYGON_API_KEY="your_key"
python3 mcp-servers/market-data-server.py

# In another terminal, test with MCP client
mcp-client call-tool market-data get_stock_price '{"symbol": "AAPL"}'
```

---

## Deployment Checklist

- [ ] Set up API keys (Massive/Polygon, SEC API, etc.)
- [ ] Install MCP dependencies: `pip3 install mcp`
- [ ] Test each MCP server individually
- [ ] Configure .mcp.json with correct paths
- [ ] Test integration with financial skills
- [ ] Set up caching to reduce API costs
- [ ] Configure rate limiting
- [ ] Add error handling and fallbacks
- [ ] Monitor API usage

---

## Cost Estimates

### Free Tier (Development)
- Massive/Polygon: 5 calls/minute
- SEC EDGAR: Unlimited but slower
- NewsAPI: 100 requests/day
- **Monthly Cost: $0**

### Production (High Volume)
- Massive/Polygon Starter: $49/month (unlimited)
- SEC API: $85/month (enhanced)
- Visible Alpha: Custom pricing
- **Estimated: $200-500/month**
