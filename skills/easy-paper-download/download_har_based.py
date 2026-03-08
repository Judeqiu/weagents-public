#!/usr/bin/env python3
"""
Easy-Paper HAR-Based Auto Downloader

This script combines web_sfapi token acquisition with PDF download attempts.
Based on combined HAR analysis showing the connection between search and download.

Usage:
    python download_har_based.py --search "9702 physics 2024"
    python download_har_based.py --token-file tokens.json
"""

import argparse
import base64
import json
import os
import random
import ssl
import string
import sys
import time
import urllib.parse
import urllib.request
from typing import List, Optional, Dict

# SSL context
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE


class HARBassedDownloader:
    """Downloader using web_sfapi token acquisition + PDF construction."""
    
    BASE_URL = "https://server.easy-paper.com"
    WEB_URL = "https://easy-paper.com"
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir
        self.session = self._generate_session()
        self.tokens = []
        os.makedirs(output_dir, exist_ok=True)
    
    def _generate_session(self) -> str:
        """Generate session ID."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    def _get_headers(self, referer: Optional[str] = None) -> dict:
        """Generate headers matching HAR analysis."""
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': referer or self.WEB_URL + '/papersearch',
            'Origin': self.WEB_URL,
        }
    
    def acquire_tokens(self) -> List[Dict]:
        """
        Step 1: Acquire web_sfapi tokens (like in HAR 1).
        These tokens may be decryption keys for PDF URLs.
        """
        print(f"[{self.session}] Step 1: Acquiring web_sfapi tokens...")
        
        tokens = []
        
        # Trigger tokens by visiting search page (as in HAR 1)
        try:
            # Visit homepage
            req = urllib.request.Request(
                self.WEB_URL,
                headers=self._get_headers(),
                method='GET'
            )
            with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=10) as resp:
                resp.read()
            
            time.sleep(0.5)
            
            # Visit search page
            req = urllib.request.Request(
                self.WEB_URL + '/papersearch',
                headers=self._get_headers(),
                method='GET'
            )
            with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=10) as resp:
                resp.read()
            
            # The above should trigger web_sfapi calls in a real browser
            # For automation, we directly call web_sfapi with random tokens
            
            print(f"[{self.session}] Making web_sfapi calls...")
            
            # Generate random tokens similar to HAR pattern
            for i in range(3):
                random_token = ''.join(random.choices(
                    string.ascii_letters + string.digits + '%_-', k=48
                ))
                
                url = f"{self.BASE_URL}/web_sfapi/{urllib.parse.quote(random_token)}"
                
                try:
                    req = urllib.request.Request(url, headers=self._get_headers())
                    with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=5) as resp:
                        data = resp.read()
                        
                        # Try to decode as base64
                        try:
                            decoded = base64.b64decode(data)
                            tokens.append({
                                'url': url,
                                'encoded': data.decode('utf-8', errors='ignore'),
                                'decoded': decoded,
                                'size': len(decoded)
                            })
                            print(f"  Token {i+1}: {len(decoded)} bytes decoded")
                        except:
                            tokens.append({
                                'url': url,
                                'encoded': data.decode('utf-8', errors='ignore'),
                                'decoded': None,
                                'size': len(data)
                            })
                            print(f"  Token {i+1}: {len(data)} bytes (not base64)")
                            
                except Exception as e:
                    print(f"  Token {i+1}: Failed - {str(e)[:50]}")
                
                time.sleep(0.3)
        
        except Exception as e:
            print(f"  Warning: {e}")
        
        self.tokens = tokens
        return tokens
    
    def construct_pdf_urls_from_tokens(self, subject: str, year: str, 
                                        session: str, paper: str, 
                                        variant: str) -> List[str]:
        """
        Step 2: Construct PDF URLs using tokens.
        
        Based on HAR analysis, the PDF URL structure is:
        /paperdownload/dir_v3/{encrypted_data}%delimiter%{more_data}
        
        We try to use tokens to construct or decrypt these URLs.
        """
        print(f"[{self.session}] Step 2: Constructing PDF URLs from tokens...")
        
        urls = []
        
        # Standard encoding attempts
        short_year = year[2:]
        filename = f"{subject}_{session}{short_year}_{paper}_{variant}.pdf"
        
        # Strategy A: Use tokens as part of URL
        for i, token in enumerate(self.tokens):
            if token['decoded'] and len(token['decoded']) > 16:
                # Use first 32 bytes of decoded token as key
                key = token['decoded'][:32].hex() if isinstance(token['decoded'], bytes) else token['decoded'][:32]
                
                # Construct URL with token-based filename
                encoded_filename = f"{key}%25fo%40~%5BC.4L1.ZDcp{base64.b64encode(filename.encode()).decode().replace('=', '')}"
                url = f"{self.BASE_URL}/paperdownload/dir_v3/{encoded_filename}"
                urls.append(('token_based', url))
        
        # Strategy B: Direct hash combinations
        for token in self.tokens:
            if token['encoded']:
                # Use encoded token directly
                url = f"{self.BASE_URL}/paperdownload/dir_v3/{urllib.parse.quote(token['encoded'][:100])}"
                urls.append(('direct_token', url))
        
        # Strategy C: Filename + Token XOR/Combine
        for token in self.tokens:
            if token['decoded']:
                try:
                    # Create combined hash
                    combined = hashlib.sha256(
                        (filename + token['decoded'].hex()[:32]).encode()
                    ).hexdigest()[:48]
                    
                    url = f"{self.BASE_URL}/paperdownload/dir_v3/{combined}"
                    urls.append(('hash_combined', url))
                except:
                    pass
        
        print(f"  Generated {len(urls)} candidate URLs")
        return urls
    
    def try_download(self, url: str, output_path: str) -> bool:
        """Try to download PDF from URL."""
        try:
            headers = self._get_headers(self.WEB_URL + '/papersearch')
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=15) as resp:
                data = resp.read()
                
                if len(data) > 1000 and data[:4] == b'%PDF':
                    with open(output_path, 'wb') as f:
                        f.write(data)
                    return True
            
            return False
        except:
            return False
    
    def download(self, subject: str, year: str, session: str, 
                 paper: str, variant: str) -> Optional[str]:
        """
        Full workflow: Acquire tokens → Construct URLs → Download.
        """
        output_filename = f"{subject}_{session}{year[2:]}_{paper}_{variant}.pdf"
        output_path = os.path.join(self.output_dir, output_filename)
        
        print(f"\n{'='*70}")
        print(f"HAR-Based Auto Download")
        print(f"{'='*70}")
        print(f"Paper: {subject} {year} {session.upper()} {paper.upper()} {variant}")
        print(f"Session: {self.session}")
        print(f"{'='*70}\n")
        
        # Step 1: Acquire tokens
        tokens = self.acquire_tokens()
        if not tokens:
            print("✗ Failed to acquire tokens")
            return None
        
        print(f"\nAcquired {len(tokens)} tokens\n")
        
        # Step 2: Construct URLs
        urls = self.construct_pdf_urls_from_tokens(subject, year, session, paper, variant)
        
        # Step 3: Try each URL
        print(f"\nStep 3: Trying {len(urls)} URLs...")
        for i, (strategy, url) in enumerate(urls[:20]):  # Limit to first 20
            print(f"  [{i+1}/{min(len(urls), 20)}] {strategy}: {url[:60]}...")
            
            if self.try_download(url, output_path):
                print(f"\n✓ SUCCESS! Downloaded to: {output_path}")
                # Verify
                size = os.path.getsize(output_path)
                print(f"  File size: {size:,} bytes")
                return output_path
            
            time.sleep(0.2)
        
        print(f"\n✗ All {len(urls)} URLs failed")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="HAR-based auto downloader for EasyPaper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python download_har_based.py --subject 9702 --year 2024 --session s --paper qp --variant 12
  python download_har_based.py --subject 9709 --year 2023 --session w --paper ms --variant 13 -o ./papers/
        """
    )
    
    parser.add_argument("--subject", "-c", required=True, help="Subject code")
    parser.add_argument("--year", "-y", required=True, help="Year")
    parser.add_argument("--session", "-s", required=True, help="s/w/m")
    parser.add_argument("--paper", "-p", default="qp", help="qp/ms/er/gt")
    parser.add_argument("--variant", "-v", required=True, help="Variant number")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    
    args = parser.parse_args()
    
    downloader = HARBassedDownloader(output_dir=args.output)
    result = downloader.download(
        subject=args.subject,
        year=args.year,
        session=args.session,
        paper=args.paper,
        variant=args.variant
    )
    
    if result:
        print(f"\n✓ PDF saved: {result}")
        sys.exit(0)
    else:
        print("\n✗ Download failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
