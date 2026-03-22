#!/usr/bin/env python3
"""
Customer Analysis Helper - Process research data with AI to generate analysis and email.

This helper script takes the raw research data and uses an LLM (via environment or direct API)
to generate the customer analysis and first-touch email.

Usage:
    # Generate analysis prompt only (for manual LLM use)
    python3 analyze_customer.py --data ./output/company_data.json --prompt-only
    
    # Full analysis (requires OPENAI_API_KEY or similar)
    python3 analyze_customer.py --data ./output/company_data.json --output ./analysis.json
"""

import argparse
import json
import os
import sys
from typing import Optional


def generate_analysis_prompt(data: dict) -> str:
    """Generate the analysis prompt for the LLM."""
    
    # Format search results
    search_results_text = ""
    for i, result in enumerate(data.get('search_results', [])[:5], 1):
        search_results_text += f"\n{i}. {result.get('title', 'N/A')}\n"
        search_results_text += f"   URL: {result.get('url', 'N/A')}\n"
        search_results_text += f"   {result.get('snippet', 'N/A')[:200]}\n"
    
    website_content = data.get('website_content', '')[:2000] if data.get('website_content') else 'No website content available'
    linkedin_info = data.get('linkedin_info', 'No LinkedIn information available')
    
    prompt = f"""You are an expert B2B sales researcher with 15+ years of experience in international sales. Analyze the following customer information and provide a comprehensive assessment for the sales team.

## Customer Information

**Company Name:** {data.get('company_name', 'Unknown')}

### Web Search Results
{search_results_text}

### Website Content
{website_content}

### LinkedIn Information
{linkedin_info}

---

## Analysis Requirements

Please analyze this customer and provide the following:

### 1. Company Summary (2-3 sentences)
What does this company do? What's their main business?

### 2. Customer Type Classification
Choose ONE:
- **End User** - Uses products directly in their operations
- **Distributor** - Resells products to other businesses
- **System Integrator** - Integrates products into larger solutions
- **OEM** - Incorporates products into their own products
- **Competitor** - Similar business, potential threat
- **Unknown** - Insufficient information

### 3. Priority Assessment
- **High** - Strong fit, high potential value, immediate opportunity
- **Medium** - Moderate fit, worth pursuing
- **Low** - Weak fit, limited potential

Provide reasoning for the priority level.

### 4. Industry Segment
Primary industry (e.g., Industrial Automation, Food & Beverage, Healthcare, Retail, etc.)

### 5. Potential Value
Estimated deal size range or strategic importance.

### 6. Business Fit Assessment
How well does this customer match our ideal customer profile? Consider:
- Industry alignment
- Company size
- Geographic location
- Technology adoption

### 7. Recommended Sales Approach
Specific strategy for engaging this customer.

### 8. Key Talking Points (3-5 points)
Specific conversation starters based on their business.

### 9. Red Flags (if any)
Any concerns, competitive threats, or warning signs.

### 10. Recommended Next Steps (3-5 actions)
Specific, actionable next steps for the sales team.

---

## Output Format

Respond with a valid JSON object exactly in this format:

```json
{{
  "company_summary": "string",
  "customer_type": "End User|Distributor|System Integrator|OEM|Competitor|Unknown",
  "priority_score": "High|Medium|Low",
  "priority_reasoning": "string",
  "industry_segment": "string",
  "potential_value": "string",
  "business_fit": "string",
  "sales_approach": "string",
  "talking_points": ["point 1", "point 2", "point 3"],
  "red_flags": ["flag 1"],
  "next_steps": ["step 1", "step 2", "step 3"]
}}
```

Important:
- Respond ONLY with the JSON object
- No markdown formatting around the JSON
- No additional commentary
- Ensure valid JSON syntax
"""
    
    return prompt


def generate_email_prompt(data: dict, analysis: dict) -> str:
    """Generate the email creation prompt."""
    
    talking_points = "\n".join([f"- {tp}" for tp in analysis.get('talking_points', [])])
    
    prompt = f"""You are an expert B2B sales copywriter specializing in personalized outreach emails. Write a compelling first-touch email based on the customer research.

## Customer Profile

**Company:** {data.get('company_name', '')}
**Industry:** {analysis.get('industry_segment', '')}
**Customer Type:** {analysis.get('customer_type', '')}
**Business Summary:** {analysis.get('company_summary', '')}

## Sales Context

**Recommended Approach:** {analysis.get('sales_approach', '')}

**Key Talking Points:**
{talking_points}

---

## Email Requirements

Write a professional, personalized first-touch email with these characteristics:

### Tone & Style
- Professional but conversational (not overly formal)
- Shows genuine research about their company
- Confident but not pushy
- 150-250 words total

### Structure
1. **Subject Line** - Compelling, specific, not spammy (avoid "Quick question")
2. **Opening** - Personalized hook referencing their business or recent news
3. **Value Proposition** - Clear statement of how you can help them
4. **Proof Point** - Brief credibility indicator (client, result, or expertise)
5. **Call to Action** - Specific, low-friction next step
6. **Sign-off** - Professional but warm

### Guidelines
- NO generic templates
- NO "I hope this email finds you well"
- NO feature dumps
- YES to specific references to their business
- YES to clear value proposition
- YES to single, clear CTA

---

## Output Format

Provide the email in this exact format:

```
Subject: [Subject line here]

[Email body here]

[Sign-off]
[Your name]
[Your title]
[Your company]
```
"""
    
    return prompt


def call_llm(prompt: str, api_key: Optional[str] = None) -> str:
    """Call LLM API (placeholder - implement based on available API)."""
    
    # Try OpenAI
    if os.environ.get('OPENAI_API_KEY') or api_key:
        try:
            import openai
            client = openai.OpenAI(api_key=api_key or os.environ.get('OPENAI_API_KEY'))
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert B2B sales researcher."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    # Try Kimi/Moonshot (common in China)
    if os.environ.get('MOONSHOT_API_KEY'):
        try:
            import openai
            client = openai.OpenAI(
                api_key=os.environ.get('MOONSHOT_API_KEY'),
                base_url="https://api.moonshot.cn/v1"
            )
            
            response = client.chat.completions.create(
                model="kimi-latest",
                messages=[
                    {"role": "system", "content": "You are an expert B2B sales researcher."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Moonshot API error: {e}")
            return None
    
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Customer Analysis Helper - Generate AI prompts for customer research"
    )
    parser.add_argument("--data", "-d", required=True,
                       help="Path to research data JSON file")
    parser.add_argument("--output", "-o",
                       help="Output file for analysis results")
    parser.add_argument("--prompt-only", action="store_true",
                       help="Only output the analysis prompt (don't call LLM)")
    parser.add_argument("--email-only", action="store_true",
                       help="Generate email prompt (requires analysis file)")
    parser.add_argument("--analysis", "-a",
                       help="Path to analysis JSON file (for email generation)")
    
    args = parser.parse_args()
    
    # Load research data
    try:
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading data file: {e}")
        sys.exit(1)
    
    # Generate analysis prompt
    if not args.email_only:
        analysis_prompt = generate_analysis_prompt(data)
        
        if args.prompt_only:
            print("=== ANALYSIS PROMPT ===")
            print(analysis_prompt)
            print("\n=== END PROMPT ===")
            print("\nCopy the above prompt and send to your LLM.")
            print("Save the JSON response and use --analysis to generate email.")
            return
        
        # Call LLM for analysis
        print("Generating analysis...")
        analysis_response = call_llm(analysis_prompt)
        
        if analysis_response:
            # Try to parse JSON
            try:
                # Clean up response (remove markdown code blocks if present)
                cleaned = analysis_response
                if "```json" in cleaned:
                    cleaned = cleaned.split("```json")[1].split("```")[0]
                elif "```" in cleaned:
                    cleaned = cleaned.split("```")[1].split("```")[0]
                
                analysis = json.loads(cleaned.strip())
                
                # Save analysis
                output_file = args.output or args.data.replace('_data.json', '_analysis.json')
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(analysis, f, indent=2, ensure_ascii=False)
                
                print(f"✓ Analysis saved to: {output_file}")
                print(f"\nSummary:")
                print(f"  Customer Type: {analysis.get('customer_type', 'N/A')}")
                print(f"  Priority: {analysis.get('priority_score', 'N/A')}")
                print(f"  Industry: {analysis.get('industry_segment', 'N/A')}")
                
            except json.JSONDecodeError as e:
                print(f"Error parsing LLM response as JSON: {e}")
                print("Raw response:")
                print(analysis_response)
        else:
            print("✗ No LLM response received.")
            print("Set OPENAI_API_KEY or MOONSHOT_API_KEY environment variable.")
    
    # Generate email
    if args.email_only or args.analysis:
        analysis_file = args.analysis or args.output
        
        if not analysis_file or not os.path.exists(analysis_file):
            print(f"Error: Analysis file not found: {analysis_file}")
            print("Generate analysis first or provide --analysis path")
            sys.exit(1)
        
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis = json.load(f)
        
        email_prompt = generate_email_prompt(data, analysis)
        
        if args.prompt_only:
            print("=== EMAIL PROMPT ===")
            print(email_prompt)
            print("\n=== END PROMPT ===")
            return
        
        print("\nGenerating email draft...")
        email_response = call_llm(email_prompt)
        
        if email_response:
            output_file = args.output or args.data.replace('_data.json', '_email.txt')
            if output_file.endswith('.json'):
                output_file = output_file.replace('.json', '.txt')
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(email_response)
            
            print(f"✓ Email draft saved to: {output_file}")
            print("\nPreview:")
            print("-" * 50)
            print(email_response[:500] + "..." if len(email_response) > 500 else email_response)
        else:
            print("✗ No LLM response received for email generation.")


if __name__ == "__main__":
    main()
