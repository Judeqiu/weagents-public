#!/usr/bin/env python3
"""
Customer Research Agent - Automated customer background research using Chrome CDP.

This script automates the pre-sales workflow:
1. Search company information (Google, LinkedIn, website)
2. Analyze customer type and priority
3. Generate customer brief and first-touch email
4. Output structured data for CRM

Usage:
    python3 research_customer.py --company "TechVision Automation GmbH"
    python3 research_customer.py --email "inquiry@example.com" --content "email content..."
    python3 research_customer.py --company "ABC Corp" --output ./research_output
"""

import argparse
import asyncio
import json
import os
import re
import sys
from datetime import datetime
from typing import Optional
from urllib.parse import quote_plus

# Check for required packages
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Error: playwright not installed. Run: pip install playwright")
    sys.exit(1)

# Configuration
DEFAULT_CDP_URL = os.environ.get("CHROME_CDP_URL", "http://127.0.0.1:9222")

STEALTH_SCRIPTS = [
    # Hide webdriver property
    """() => {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    }""",
    # Fake browser plugins
    """() => {
        Object.defineProperty(navigator, 'plugins', {
            get: () => [
                {name: "Chrome PDF Plugin"},
                {name: "Chrome PDF Viewer"}
            ]
        });
    }""",
    # Fake Chrome runtime
    """() => {
        window.chrome = { runtime: {}, loadTimes: () => {} };
    }""",
]


class CustomerResearchAgent:
    """Agent for researching customer background information."""
    
    def __init__(self, cdp_url: str = DEFAULT_CDP_URL):
        self.cdp_url = cdp_url
        self.browser = None
        self.context = None
        self.research_data = {
            "company_name": "",
            "search_results": [],
            "website_content": "",
            "linkedin_info": "",
            "analysis": {},
            "generated_email": "",
            "timestamp": datetime.now().isoformat(),
        }
    
    async def connect(self):
        """Connect to Chrome via CDP."""
        playwright = await async_playwright().start()
        
        try:
            self.browser = await playwright.chromium.connect_over_cdp(self.cdp_url)
            
            # Use existing context or create new one
            contexts = self.browser.contexts
            if contexts:
                self.context = contexts[0]
            else:
                self.context = await self.browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                )
            
            print(f"✓ Connected to Chrome at {self.cdp_url}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to connect to Chrome: {e}")
            print("\nTroubleshooting:")
            print("1. Ensure Chrome is running with: --remote-debugging-port=9222")
            print("2. Check connection: curl http://127.0.0.1:9222/json/version")
            return False
    
    async def search_google(self, query: str, num_results: int = 5) -> list:
        """Search Google for company information."""
        page = await self.context.new_page()
        
        try:
            # Apply stealth scripts
            for script in STEALTH_SCRIPTS:
                await page.add_init_script(script)
            
            # Navigate to Google
            search_url = f"https://www.google.com/search?q={quote_plus(query)}"
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            
            # Extract search results
            results = await page.evaluate("""() => {
                const items = [];
                const elements = document.querySelectorAll('div[data-header-feature="0"] a h3, div[data-hveid] a h3, div.g a h3');
                elements.forEach((el, index) => {
                    if (index < 10) {
                        const link = el.closest('a');
                        const snippet = el.parentElement?.parentElement?.querySelector('div[data-sncf="1"], div.VwiC3b')?.innerText || '';
                        items.push({
                            title: el.innerText,
                            url: link ? link.href : '',
                            snippet: snippet.substring(0, 300)
                        });
                    }
                });
                return items;
            }""")
            
            await page.close()
            return results[:num_results]
            
        except Exception as e:
            print(f"Warning: Google search failed: {e}")
            await page.close()
            return []
    
    async def scrape_website(self, url: str) -> str:
        """Scrape company website for key information."""
        if not url or not url.startswith("http"):
            return ""
        
        page = await self.context.new_page()
        
        try:
            # Apply stealth scripts
            for script in STEALTH_SCRIPTS:
                await page.add_init_script(script)
            
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)
            
            # Extract key content
            content = await page.evaluate("""() => {
                // Try to get about page content
                const aboutLink = Array.from(document.querySelectorAll('a')).find(a => 
                    a.innerText.toLowerCase().includes('about') || 
                    a.href.toLowerCase().includes('about')
                );
                
                let aboutContent = '';
                if (aboutLink) {
                    // Note: We won't navigate to avoid complexity
                    aboutContent = 'About page available at: ' + aboutLink.href;
                }
                
                // Extract main page content
                const title = document.title || '';
                const metaDescription = document.querySelector('meta[name="description"]')?.content || '';
                
                // Get visible text from main content areas
                const mainContent = document.querySelector('main, #main, .main, [role="main"]');
                const bodyContent = mainContent ? mainContent.innerText : document.body.innerText;
                
                // Extract key sections
                const headings = Array.from(document.querySelectorAll('h1, h2, h3'))
                    .map(h => h.innerText)
                    .filter(t => t.length > 0 && t.length < 200)
                    .slice(0, 10);
                
                return {
                    title: title,
                    metaDescription: metaDescription,
                    headings: headings,
                    contentPreview: bodyContent?.substring(0, 2000) || '',
                    aboutInfo: aboutContent
                };
            }""")
            
            await page.close()
            
            # Format content
            formatted = f"""Title: {content.get('title', '')}
Meta Description: {content.get('metaDescription', '')}

Key Headings:
{chr(10).join(['- ' + h for h in content.get('headings', [])])}

Content Preview:
{content.get('contentPreview', '')}

{content.get('aboutInfo', '')}"""
            
            return formatted
            
        except Exception as e:
            print(f"Warning: Failed to scrape {url}: {e}")
            await page.close()
            return ""
    
    async def search_linkedin(self, company_name: str) -> str:
        """Search LinkedIn for company information."""
        page = await self.context.new_page()
        
        try:
            # Apply stealth scripts
            for script in STEALTH_SCRIPTS:
                await page.add_init_script(script)
            
            # Search for company on LinkedIn
            search_query = f"{company_name} site:linkedin.com/company"
            search_url = f"https://www.google.com/search?q={quote_plus(search_query)}"
            
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)
            
            # Extract LinkedIn URL from search results
            linkedin_url = await page.evaluate("""() => {
                const links = document.querySelectorAll('a');
                for (const link of links) {
                    if (link.href.includes('linkedin.com/company')) {
                        return link.href;
                    }
                }
                return '';
            }""")
            
            linkedin_info = ""
            
            if linkedin_url:
                # Try to visit LinkedIn page
                try:
                    await page.goto(linkedin_url, wait_until="networkidle", timeout=30000)
                    await asyncio.sleep(3)
                    
                    linkedin_data = await page.evaluate("""() => {
                        const companyName = document.querySelector('h1')?.innerText || '';
                        const description = document.querySelector('[data-test-id="about-us"]')?.innerText || 
                                          document.querySelector('.organization-about-description')?.innerText || '';
                        const industry = Array.from(document.querySelectorAll('dd')).find(el => 
                            el.previousElementSibling?.innerText?.includes('Industry')
                        )?.innerText || '';
                        const companySize = Array.from(document.querySelectorAll('dd')).find(el => 
                            el.previousElementSibling?.innerText?.includes('Company size')
                        )?.innerText || '';
                        const headquarters = Array.from(document.querySelectorAll('dd')).find(el => 
                            el.previousElementSibling?.innerText?.includes('Headquarters')
                        )?.innerText || '';
                        
                        return {
                            name: companyName,
                            description: description.substring(0, 1000),
                            industry: industry,
                            size: companySize,
                            headquarters: headquarters,
                            url: window.location.href
                        };
                    }""")
                    
                    linkedin_info = f"""LinkedIn Profile:
- Company: {linkedin_data.get('name', '')}
- Industry: {linkedin_data.get('industry', '')}
- Company Size: {linkedin_data.get('size', '')}
- Headquarters: {linkedin_data.get('headquarters', '')}
- Description: {linkedin_data.get('description', '')}
- URL: {linkedin_data.get('url', '')}"""
                    
                except Exception as e:
                    linkedin_info = f"LinkedIn URL found but could not access: {linkedin_url}"
            else:
                linkedin_info = "No LinkedIn company page found in search results."
            
            await page.close()
            return linkedin_info
            
        except Exception as e:
            print(f"Warning: LinkedIn search failed: {e}")
            await page.close()
            return ""
    
    def extract_company_from_email(self, email_content: str) -> tuple:
        """Extract company name and contact info from email."""
        company_name = ""
        contact_name = ""
        
        # Try to extract from email signature or content
        lines = email_content.split('\n')
        
        # Look for common patterns
        for line in lines:
            # Company name patterns
            if any(keyword in line.lower() for keyword in ['company:', 'from:', 'organization:', 'inc.', 'ltd', 'gmbh', 'corp']):
                if len(line) > 3:
                    company_name = line.split(':')[-1].strip() if ':' in line else line.strip()
                    company_name = company_name[:100]  # Limit length
            
            # Contact name patterns
            if any(keyword in line.lower() for keyword in ['name:', 'regards,', 'sincerely,', 'best,']):
                potential_name = line.split(',')[-1].strip() if ',' in line else line.split(':')[-1].strip()
                if len(potential_name) > 2 and len(potential_name) < 50:
                    contact_name = potential_name
        
        return company_name, contact_name
    
    def generate_analysis_prompt(self, data: dict) -> str:
        """Generate prompt for AI analysis."""
        prompt = f"""You are an expert B2B sales researcher. Analyze the following customer information and provide a comprehensive assessment.

## Customer Information

Company Name: {data.get('company_name', 'Unknown')}

### Search Results
{json.dumps(data.get('search_results', []), indent=2, ensure_ascii=False)}

### Website Content
{data.get('website_content', 'No website content available')[:3000]}

### LinkedIn Information
{data.get('linkedin_info', 'No LinkedIn information available')}

## Required Analysis

Please provide the following in JSON format:

{{
  "company_summary": "Brief 2-3 sentence description of what the company does",
  "customer_type": "End User | Distributor | System Integrator | OEM | Competitor | Unknown",
  "priority_score": "High | Medium | Low",
  "priority_reasoning": "Why this priority level",
  "industry_segment": "Primary industry (e.g., Industrial Automation, Retail, Healthcare)",
  "potential_value": "Estimated deal size or strategic importance",
  "key_contacts": ["List of identified key personnel"],
  "business_fit": "How well they match our ideal customer profile",
  "sales_approach": "Recommended sales strategy",
  "talking_points": ["3-5 key points for initial conversation"],
  "red_flags": ["Any concerns or warnings"],
  "next_steps": ["Specific recommended actions"]
}}

Respond ONLY with the JSON object, no additional text."""
        
        return prompt
    
    def generate_email_prompt(self, data: dict, analysis: dict) -> str:
        """Generate prompt for first-touch email."""
        prompt = f"""You are an expert B2B sales copywriter. Write a personalized first-touch email based on the customer research.

## Customer Information

Company: {data.get('company_name', '')}
Industry: {analysis.get('industry_segment', '')}
Customer Type: {analysis.get('customer_type', '')}
Company Summary: {analysis.get('company_summary', '')}

### Key Talking Points
{chr(10).join(['- ' + tp for tp in analysis.get('talking_points', [])])}

### Recommended Approach
{analysis.get('sales_approach', '')}

## Email Requirements

Write a professional, personalized first-touch email that:
1. Shows you've done your research about their company
2. Demonstrates understanding of their industry/business
3. Presents a clear value proposition
4. Has a specific, low-friction call to action
5. Is 150-250 words
6. Uses a professional but conversational tone

Structure:
- Subject line (compelling and relevant)
- Opening (personalized hook based on their business)
- Value proposition (how we can help)
- Proof point (brief credibility statement)
- Call to action (specific next step)
- Professional sign-off

Respond with the complete email (subject line included)."""
        
        return prompt
    
    async def research(self, company_name: str, email_content: Optional[str] = None) -> dict:
        """Execute full research workflow."""
        
        # If email provided, extract company info
        if email_content and not company_name:
            extracted_company, contact_name = self.extract_company_from_email(email_content)
            company_name = extracted_company or "Unknown Company"
            print(f"Extracted company from email: {company_name}")
        
        self.research_data["company_name"] = company_name
        print(f"\n🔍 Researching: {company_name}\n")
        
        # Step 1: Google Search
        print("Step 1/4: Searching for company information...")
        search_query = company_name
        search_results = await self.search_google(search_query, num_results=8)
        self.research_data["search_results"] = search_results
        print(f"  ✓ Found {len(search_results)} search results")
        
        # Find company website from search results
        company_website = ""
        for result in search_results:
            url = result.get('url', '')
            if url and url.startswith('http') and 'google' not in url and 'linkedin' not in url:
                company_website = url
                break
        
        # Step 2: Scrape Website
        print("Step 2/4: Analyzing company website...")
        if company_website:
            website_content = await self.scrape_website(company_website)
            self.research_data["website_content"] = website_content
            print(f"  ✓ Scraped website: {company_website[:60]}...")
        else:
            print("  ⚠ No company website found")
        
        # Step 3: LinkedIn Research
        print("Step 3/4: Searching LinkedIn...")
        linkedin_info = await self.search_linkedin(company_name)
        self.research_data["linkedin_info"] = linkedin_info
        if linkedin_info:
            print("  ✓ LinkedIn information gathered")
        else:
            print("  ⚠ No LinkedIn data found")
        
        # Step 4: Analysis (will be done by LLM via OpenClaw)
        print("Step 4/4: Preparing analysis data...")
        print("  ✓ Research data ready for AI analysis")
        
        return self.research_data
    
    def save_results(self, output_dir: str, analysis: Optional[dict] = None, email: Optional[str] = None):
        """Save research results to files."""
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename base
        safe_name = re.sub(r'[^\w\s-]', '', self.research_data['company_name']).strip().replace(' ', '_')[:50]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = f"{safe_name}_{timestamp}"
        
        # Save raw data as JSON
        json_path = os.path.join(output_dir, f"{base_name}_data.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.research_data, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Saved raw data: {json_path}")
        
        # Save analysis if provided
        if analysis:
            analysis_path = os.path.join(output_dir, f"{base_name}_analysis.json")
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"  ✓ Saved analysis: {analysis_path}")
        
        # Save email if provided
        if email:
            email_path = os.path.join(output_dir, f"{base_name}_email.txt")
            with open(email_path, 'w', encoding='utf-8') as f:
                f.write(email)
            print(f"  ✓ Saved email: {email_path}")
        
        # Generate markdown report
        report_path = os.path.join(output_dir, f"{base_name}_report.md")
        self._generate_markdown_report(report_path, analysis, email)
        print(f"  ✓ Saved report: {report_path}")
        
        return {
            'json': json_path,
            'analysis': analysis_path if analysis else None,
            'email': email_path if email else None,
            'report': report_path
        }
    
    def _generate_markdown_report(self, path: str, analysis: Optional[dict], email: Optional[str]):
        """Generate a comprehensive markdown report."""
        report = f"""# Customer Research Report

**Company:** {self.research_data['company_name']}  
**Research Date:** {self.research_data['timestamp']}

---

## Executive Summary

"""
        
        if analysis:
            report += f"""### Company Overview
{analysis.get('company_summary', 'N/A')}

### Customer Classification
- **Type:** {analysis.get('customer_type', 'Unknown')}
- **Priority:** {analysis.get('priority_score', 'Unknown')}
- **Industry:** {analysis.get('industry_segment', 'Unknown')}
- **Potential Value:** {analysis.get('potential_value', 'Unknown')}

### Business Fit
{analysis.get('business_fit', 'N/A')}

### Recommended Sales Approach
{analysis.get('sales_approach', 'N/A')}

### Key Talking Points
{chr(10).join(['- ' + tp for tp in analysis.get('talking_points', [])])}

### Red Flags
{chr(10).join(['- ' + rf for rf in analysis.get('red_flags', [])]) or '- None identified'}

### Recommended Next Steps
{chr(10).join(['1. ' + ns for ns in analysis.get('next_steps', [])])}

"""
        
        if email:
            report += f"""---

## First-Touch Email Draft

```
{email}
```

"""
        
        report += f"""---

## Source Data

### Search Results
"""
        
        for i, result in enumerate(self.research_data.get('search_results', []), 1):
            report += f"""
**{i}. {result.get('title', 'N/A')}**  
URL: {result.get('url', 'N/A')}  
{result.get('snippet', '')}
"""
        
        if self.research_data.get('linkedin_info'):
            report += f"""

### LinkedIn Information
{self.research_data['linkedin_info']}
"""
        
        if self.research_data.get('website_content'):
            report += f"""

### Website Content
<details>
<summary>Click to expand website content</summary>

```
{self.research_data['website_content'][:5000]}
```

</details>
"""
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(report)
    
    async def close(self):
        """Close browser connection."""
        if self.browser:
            await self.browser.close()


async def main():
    parser = argparse.ArgumentParser(
        description="Customer Research Agent - Automated customer background research"
    )
    parser.add_argument("--company", "-c", help="Company name to research")
    parser.add_argument("--email", "-e", help="Email content file path (extracts company info)")
    parser.add_argument("--output", "-o", default="./research_output", 
                       help="Output directory for results (default: ./research_output)")
    parser.add_argument("--cdp-url", default=DEFAULT_CDP_URL,
                       help=f"Chrome CDP URL (default: {DEFAULT_CDP_URL})")
    parser.add_argument("--analysis-file", "-a", 
                       help="Path to JSON file with AI analysis results")
    parser.add_argument("--email-draft", 
                       help="Path to file with generated email draft")
    
    args = parser.parse_args()
    
    if not args.company and not args.email:
        parser.print_help()
        print("\nError: Must provide either --company or --email")
        sys.exit(1)
    
    # Read email content if provided
    email_content = None
    if args.email:
        with open(args.email, 'r', encoding='utf-8') as f:
            email_content = f.read()
    
    # Initialize agent
    agent = CustomerResearchAgent(cdp_url=args.cdp_url)
    
    try:
        # Connect to Chrome
        if not await agent.connect():
            sys.exit(1)
        
        # Execute research
        research_data = await agent.research(args.company, email_content)
        
        # Load analysis if provided
        analysis = None
        if args.analysis_file:
            with open(args.analysis_file, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
        
        # Load email draft if provided
        email_draft = None
        if args.email_draft:
            with open(args.email_draft, 'r', encoding='utf-8') as f:
                email_draft = f.read()
        
        # Save results
        print(f"\n💾 Saving results to {args.output}...")
        files = agent.save_results(args.output, analysis, email_draft)
        
        print(f"\n✅ Research complete!")
        print(f"\nOutput files:")
        for key, path in files.items():
            if path:
                print(f"  - {key}: {path}")
        
        # Print summary for OpenClaw to parse
        print(f"\n---OPENCLAW_OUTPUT---")
        print(json.dumps({
            "company": research_data["company_name"],
            "search_results_count": len(research_data["search_results"]),
            "has_website": bool(research_data["website_content"]),
            "has_linkedin": bool(research_data["linkedin_info"]),
            "output_files": files,
            "analysis_prompt": agent.generate_analysis_prompt(research_data)
        }, indent=2, ensure_ascii=False))
        
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())
