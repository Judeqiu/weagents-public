#!/usr/bin/env python3
"""
Generate Strategic and Financial Buyer Lists for M&A Transactions

Usage:
    python3 generate-buyer-list.py --company "Target Inc" --industry "software" --output buyers.csv
    python3 generate-buyer-list.py --company "Target Inc" --revenue 100 --ebitda 25 --output buyers.csv
"""

import argparse
import csv
import sys
from typing import List, Dict


def get_strategic_buyers(industry: str, revenue: float) -> List[Dict]:
    """Generate strategic buyer candidates based on industry and size."""
    
    # Industry-specific buyer databases (illustrative)
    buyer_database = {
        "software": [
            {"name": "Microsoft", "ticker": "MSFT", "market_cap": 3000, "fit": "High", "rationale": "Cloud platform expansion"},
            {"name": "Salesforce", "ticker": "CRM", "market_cap": 250, "fit": "High", "rationale": "SaaS consolidation"},
            {"name": "Oracle", "ticker": "ORCL", "market_cap": 400, "fit": "Medium", "rationale": "Enterprise software"},
            {"name": "SAP", "ticker": "SAP", "market_cap": 180, "fit": "Medium", "rationale": "ERP expansion"},
            {"name": "Adobe", "ticker": "ADBE", "market_cap": 200, "fit": "Medium", "rationale": "Creative/workflow tools"},
            {"name": "IBM", "ticker": "IBM", "market_cap": 150, "fit": "Low", "rationale": "Legacy modernization"},
            {"name": "ServiceNow", "ticker": "NOW", "market_cap": 160, "fit": "High", "rationale": "Workflow automation"},
            {"name": "Intuit", "ticker": "INTU", "market_cap": 180, "fit": "Low", "rationale": "SMB software"},
        ],
        "healthcare": [
            {"name": "Johnson & Johnson", "ticker": "JNJ", "market_cap": 450, "fit": "High", "rationale": "MedTech expansion"},
            {"name": "UnitedHealth", "ticker": "UNH", "market_cap": 500, "fit": "High", "rationale": "Healthcare services"},
            {"name": "Pfizer", "ticker": "PFE", "market_cap": 200, "fit": "Medium", "rationale": "Pharma diversification"},
            {"name": "Abbott", "ticker": "ABT", "market_cap": 200, "fit": "High", "rationale": "Diagnostics/devices"},
            {"name": "Medtronic", "ticker": "MDT", "market_cap": 120, "fit": "High", "rationale": "Medical devices"},
            {"name": "Thermo Fisher", "ticker": "TMO", "market_cap": 220, "fit": "Medium", "rationale": "Life sciences tools"},
            {"name": "CVS Health", "ticker": "CVS", "market_cap": 100, "fit": "Low", "rationale": "Pharmacy services"},
            {"name": "Elevance Health", "ticker": "ELV", "market_cap": 120, "fit": "Medium", "rationale": "Health insurance"},
        ],
        "industrial": [
            {"name": "Honeywell", "ticker": "HON", "market_cap": 150, "fit": "High", "rationale": "Industrial automation"},
            {"name": "Siemens", "ticker": "SIEGY", "market_cap": 140, "fit": "High", "rationale": "Diversified industrial"},
            {"name": "3M", "ticker": "MMM", "market_cap": 50, "fit": "Medium", "rationale": "Materials science"},
            {"name": "General Electric", "ticker": "GE", "market_cap": 180, "fit": "Medium", "rationale": "Energy/ aerospace"},
            {"name": "Emerson", "ticker": "EMR", "market_cap": 60, "fit": "High", "rationale": "Automation solutions"},
            {"name": "Danaher", "ticker": "DHR", "market_cap": 180, "fit": "Medium", "rationale": "Life sciences/industrial"},
            {"name": "Caterpillar", "ticker": "CAT", "market_cap": 180, "fit": "Low", "rationale": "Heavy equipment"},
            {"name": "Deere", "ticker": "DE", "market_cap": 120, "fit": "Low", "rationale": "Agricultural equipment"},
        ],
        "financial": [
            {"name": "JPMorgan Chase", "ticker": "JPM", "market_cap": 600, "fit": "Medium", "rationale": "Financial services"},
            {"name": "Berkshire Hathaway", "ticker": "BRK", "market_cap": 900, "fit": "High", "rationale": "Diversified holdings"},
            {"name": "Blackstone", "ticker": "BX", "market_cap": 150, "fit": "Medium", "rationale": "Alternative assets"},
            {"name": "KKR", "ticker": "KKR", "market_cap": 100, "fit": "Medium", "rationale": "Private equity"},
            {"name": "Fidelity", "ticker": "Private", "market_cap": 50, "fit": "High", "rationale": "Asset management"},
            {"name": "Charles Schwab", "ticker": "SCHW", "market_cap": 120, "fit": "Low", "rationale": "Brokerage services"},
        ],
        "consumer": [
            {"name": "Procter & Gamble", "ticker": "PG", "market_cap": 400, "fit": "Medium", "rationale": "Consumer goods"},
            {"name": "Coca-Cola", "ticker": "KO", "market_cap": 280, "fit": "Low", "rationale": "Beverages"},
            {"name": "PepsiCo", "ticker": "PEP", "market_cap": 230, "fit": "Low", "rationale": "Snacks/beverages"},
            {"name": "Walmart", "ticker": "WMT", "market_cap": 700, "fit": "Medium", "rationale": "Retail/omnichannel"},
            {"name": "Target", "ticker": "TGT", "market_cap": 70, "fit": "Medium", "rationale": "Retail"},
            {"name": "Amazon", "ticker": "AMZN", "market_cap": 2000, "fit": "High", "rationale": "E-commerce/cloud"},
            {"name": "Nike", "ticker": "NKE", "market_cap": 140, "fit": "Low", "rationale": "Apparel/footwear"},
        ],
    }
    
    # Default to software if industry not found
    buyers = buyer_database.get(industry.lower(), buyer_database["software"])
    
    # Sort by fit (High first) then by market cap
    fit_order = {"High": 0, "Medium": 1, "Low": 2}
    buyers.sort(key=lambda x: (fit_order.get(x["fit"], 3), -x["market_cap"]))
    
    return buyers


def get_financial_buyers(revenue: float, ebitda: float) -> List[Dict]:
    """Generate financial buyer candidates based on company size."""
    
    # Size-based categorization
    ev_estimate = ebitda * 10 if ebitda else revenue * 3
    
    financial_buyers = [
        # Large-cap PE (can do deals $1B+)
        {"name": "Blackstone", "type": "Large-cap PE", "aum": 1000, "fit": "High", "sweet_spot": "1000+", "rationale": "Platform/acquisition strategy"},
        {"name": "KKR", "type": "Large-cap PE", "aum": 600, "fit": "High", "sweet_spot": "1000+", "rationale": "Operational value creation"},
        {"name": "Carlyle", "type": "Large-cap PE", "aum": 400, "fit": "High", "sweet_spot": "500+", "rationale": "Sector specialization"},
        {"name": "TPG", "type": "Large-cap PE", "aum": 250, "fit": "High", "sweet_spot": "500+", "rationale": "Growth/ buyout hybrid"},
        {"name": "Warburg Pincus", "type": "Large-cap PE", "aum": 80, "fit": "Medium", "sweet_spot": "500+", "rationale": "Growth capital"},
        {"name": "Advent International", "type": "Large-cap PE", "aum": 100, "fit": "High", "sweet_spot": "300+", "rationale": "International reach"},
        
        # Mid-market PE ($100M-$1B EV)
        {"name": "Bain Capital", "type": "Mid-market PE", "aum": 160, "fit": "High", "sweet_spot": "200-800", "rationale": "Operational focus"},
        {"name": "Thoma Bravo", "type": "Mid-market PE", "aum": 130, "fit": "High", "sweet_spot": "200-1000", "rationale": "Software specialist"},
        {"name": "Vista Equity", "type": "Mid-market PE", "aum": 100, "fit": "High", "sweet_spot": "100-500", "rationale": "Enterprise software"},
        {"name": "Silver Lake", "type": "Mid-market PE", "aum": 100, "fit": "Medium", "sweet_spot": "500+", "rationale": "Technology focus"},
        {"name": "EQT", "type": "Mid-market PE", "aum": 250, "fit": "High", "sweet_spot": "100-500", "rationale": "European/ global reach"},
        {"name": "Veritas Capital", "type": "Mid-market PE", "aum": 50, "fit": "Medium", "sweet_spot": "100-500", "rationale": "Healthcare/ govtech"},
        
        # Lower mid-market ($25M-$100M EV)
        {"name": "Genstar", "type": "Lower mid-market PE", "aum": 40, "fit": "High", "sweet_spot": "50-200", "rationale": "Sector specialization"},
        {"name": "Summit Partners", "type": "Growth Equity", "aum": 30, "fit": "High", "sweet_spot": "50-200", "rationale": "Growth-stage focus"},
        {"name": "JMI Equity", "type": "Growth Equity", "aum": 6, "fit": "High", "sweet_spot": "25-150", "rationale": "Software growth"},
        {"name": "Insight Partners", "type": "Growth Equity", "aum": 90, "fit": "Medium", "sweet_spot": "50-500", "rationale": "ScaleUp expertise"},
        
        # Family Offices
        {"name": "Cascade Investment", "type": "Family Office", "aum": 100, "fit": "Medium", "sweet_spot": "100+", "rationale": "Long-term hold"},
        {"name": "Bezos Expeditions", "type": "Family Office", "aum": 50, "fit": "Low", "sweet_spot": "50+", "rationale": "Tech focus"},
    ]
    
    # Filter based on size fit
    if ev_estimate < 50:
        # Small company - focus on lower mid-market and growth equity
        fit_buyers = [b for b in financial_buyers if 
                      "Lower" in b["type"] or "Growth" in b["type"]]
    elif ev_estimate < 200:
        # Mid-market sweet spot
        fit_buyers = [b for b in financial_buyers if 
                      "Mid-market" in b["type"] or "Lower" in b["type"]]
    else:
        # Larger company - all PE relevant
        fit_buyers = financial_buyers
    
    # Sort by fit then AUM
    fit_order = {"High": 0, "Medium": 1, "Low": 2}
    fit_buyers.sort(key=lambda x: (fit_order.get(x["fit"], 3), -x["aum"]))
    
    return fit_buyers


def categorize_buyers(strategic: List[Dict], financial: List[Dict], target_name: str) -> Dict:
    """Categorize and prioritize buyers."""
    
    categories = {
        "Tier 1 - High Priority": [],
        "Tier 2 - Medium Priority": [],
        "Tier 3 - Lower Priority": [],
    }
    
    # Strategic categorization
    for buyer in strategic:
        if buyer["fit"] == "High":
            categories["Tier 1 - High Priority"].append({
                **buyer, 
                "category": "Strategic",
                "priority": "High"
            })
        elif buyer["fit"] == "Medium":
            categories["Tier 2 - Medium Priority"].append({
                **buyer, 
                "category": "Strategic",
                "priority": "Medium"
            })
        else:
            categories["Tier 3 - Lower Priority"].append({
                **buyer, 
                "category": "Strategic",
                "priority": "Low"
            })
    
    # Financial categorization
    for buyer in financial:
        if buyer["fit"] == "High":
            categories["Tier 1 - High Priority"].append({
                **buyer, 
                "category": "Financial",
                "priority": "High"
            })
        elif buyer["fit"] == "Medium":
            categories["Tier 2 - Medium Priority"].append({
                **buyer, 
                "category": "Financial",
                "priority": "Medium"
            })
        else:
            categories["Tier 3 - Lower Priority"].append({
                **buyer, 
                "category": "Financial",
                "priority": "Low"
            })
    
    return categories


def generate_report(target: str, industry: str, revenue: float, ebitda: float, 
                    categories: Dict, output_file: str):
    """Generate buyer list report and CSV."""
    
    # Print report
    print(f"\n{'='*60}")
    print(f"BUYER LIST FOR: {target}")
    print(f"Industry: {industry.title()} | Revenue: ${revenue}M | EBITDA: ${ebitda}M")
    print(f"{'='*60}\n")
    
    total_buyers = 0
    for tier, buyers in categories.items():
        if buyers:
            print(f"\n{tier} ({len(buyers)} buyers)")
            print("-" * 60)
            
            for buyer in buyers:
                print(f"\n{buyer['name']} ({buyer.get('ticker', 'Private')})")
                print(f"  Type: {buyer['category']}")
                if 'market_cap' in buyer:
                    print(f"  Market Cap: ${buyer['market_cap']}B")
                if 'aum' in buyer:
                    print(f"  AUM: ${buyer['aum']}B")
                print(f"  Fit: {buyer['fit']}")
                print(f"  Rationale: {buyer['rationale']}")
                total_buyers += 1
    
    print(f"\n{'='*60}")
    print(f"Total Buyers Identified: {total_buyers}")
    print(f"{'='*60}\n")
    
    # Write CSV
    with open(output_file, 'w', newline='') as f:
        fieldnames = ['tier', 'name', 'ticker', 'type', 'market_cap_aum', 'fit', 'rationale', 'priority']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for tier, buyers in categories.items():
            for buyer in buyers:
                row = {
                    'tier': tier,
                    'name': buyer['name'],
                    'ticker': buyer.get('ticker', 'Private'),
                    'type': buyer['category'],
                    'market_cap_aum': buyer.get('market_cap', buyer.get('aum', 'N/A')),
                    'fit': buyer['fit'],
                    'rationale': buyer['rationale'],
                    'priority': buyer['priority']
                }
                writer.writerow(row)
    
    print(f"✓ Buyer list saved to: {output_file}")
    print(f"\nRecommended next steps:")
    print("1. Review and prioritize Tier 1 buyers")
    print("2. Research recent M&A activity for each buyer")
    print("3. Prepare tailored teasers for top 10-15 buyers")
    print("4. Execute NDAs with interested parties")


def main():
    parser = argparse.ArgumentParser(
        description='Generate Strategic and Financial Buyer Lists',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --company "TechFlow Inc" --industry software --revenue 50 --ebitda 12 --output buyers.csv
    %(prog)s --company "HealthCo" --industry healthcare --revenue 100 --ebitda 20 --output buyers.csv
    %(prog)s --company "Industrial Solutions" --industry industrial --revenue 200 --ebitda 40 --output buyers.csv

Supported Industries: software, healthcare, industrial, financial, consumer
        """
    )
    
    parser.add_argument('--company', '-c', required=True,
                        help='Target company name')
    parser.add_argument('--industry', '-i', required=True,
                        help='Industry sector (software, healthcare, industrial, financial, consumer)')
    parser.add_argument('--revenue', '-r', type=float, default=50,
                        help='Revenue in millions (default: 50)')
    parser.add_argument('--ebitda', '-e', type=float, default=10,
                        help='EBITDA in millions (default: 10)')
    parser.add_argument('--output', '-o', default='buyer_list.csv',
                        help='Output CSV file (default: buyer_list.csv)')
    
    args = parser.parse_args()
    
    print(f"Generating buyer list for {args.company}...")
    print(f"Industry: {args.industry}")
    print(f"Revenue: ${args.revenue}M")
    print(f"EBITDA: ${args.ebitda}M\n")
    
    # Get buyers
    strategic = get_strategic_buyers(args.industry, args.revenue)
    financial = get_financial_buyers(args.revenue, args.ebitda)
    
    # Categorize
    categories = categorize_buyers(strategic, financial, args.company)
    
    # Generate report
    generate_report(args.company, args.industry, args.revenue, args.ebitda, 
                   categories, args.output)


if __name__ == '__main__':
    main()
