#!/usr/bin/env python3
"""
Easy-Paper Fully Automated Downloader

Automates the browser-based workflow:
1. Acquires tokens from web_sfapi (like browser JavaScript)
2. Constructs PDF URLs using token patterns
3. Downloads PDF automatically

Usage:
    python easypaper_auto.py --subject 9702 --year 2024 --session s --paper qp --variant 12
    python easypaper_auto.py -c 9709 -y 2023 -s w -p ms -v 13 -o ./downloads/
"""

import argparse
import base64
import hashlib
import json
import os
import random
import ssl
import string
import sys
import time
import urllib.parse
import urllib.request
from typing import Optional, List, Dict, Tuple

# SSL context
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE


class EasyPaperAutomated:
    """Fully automated downloader using web_sfapi workflow."""
    
    BASE_URL = "https://server.easy-paper.com"
    WEB_URL = "https://easy-paper.com"
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir
        self.session_id = self._generate_session()
        self.tokens: List[Dict] = []
        os.makedirs(output_dir, exist_ok=True)
        
    def _generate_session(self) -> str:
        """Generate unique session ID."""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    
    def _get_headers(self, referer: Optional[str] = None) -> dict:
        """Headers matching browser behavior from HAR."""
        return {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': referer or self.WEB_URL + '/',
            'Origin': self.WEB_URL,
            'Connection': 'keep-alive',
        }
    
    def acquire_session_tokens(self) -> bool:
        """
        Step 1: Acquire session tokens via web_sfapi.
        
        Mimics browser JavaScript behavior from HAR analysis.
        The web_sfapi returns encrypted tokens that serve as session keys.
        """
        print(f"[{self.session_id}] Step 1: Acquiring session tokens...")
        
        # First, establish session by visiting pages (as browser does)
        pages = [
            self.WEB_URL,
            self.WEB_URL + '/papersearch',
        ]
        
        for page in pages:
            try:
                req = urllib.request.Request(
                    page, 
                    headers=self._get_headers(),
                    method='GET'
                )
                with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=10) as resp:
                    resp.read()
                time.sleep(0.3)
            except Exception as e:
                pass  # Continue even if some pages fail
        
        # Now acquire tokens via web_sfapi (the key step from HAR)
        print(f"[{self.session_id}] Calling web_sfapi endpoints...")
        
        # Generate token requests similar to HAR pattern
        token_urls = self._generate_token_urls()
        
        for i, url in enumerate(token_urls[:5]):  # Try first 5
            try:
                req = urllib.request.Request(url, headers=self._get_headers())
                with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=8) as resp:
                    data = resp.read()
                    
                    # Try to decode response
                    try:
                        text = data.decode('utf-8')
                        # Check if it's base64
                        decoded = base64.b64decode(text)
                        self.tokens.append({
                            'url': url,
                            'encoded': text,
                            'decoded': decoded,
                            'size': len(decoded),
                            'index': i
                        })
                        print(f"  Token {i+1}: {len(decoded)} bytes (valid base64)")
                    except:
                        # Not base64, store raw
                        self.tokens.append({
                            'url': url,
                            'encoded': data.decode('utf-8', errors='ignore'),
                            'decoded': None,
                            'size': len(data),
                            'index': i
                        })
                        print(f"  Token {i+1}: {len(data)} bytes (raw)")
                        
            except Exception as e:
                print(f"  Token {i+1}: Failed ({str(e)[:40]})")
            
            time.sleep(0.2)
        
        print(f"[{self.session_id}] Acquired {len(self.tokens)} tokens")
        return len(self.tokens) > 0
    
    def _generate_token_urls(self) -> List[str]:
        """Generate web_sfapi URLs with random tokens (HAR pattern)."""
        urls = []
        
        # Pattern from HAR: random chars with % delimiter
        for _ in range(8):
            # Generate random token part
            part1 = ''.join(random.choices(string.ascii_letters + string.digits, k=48))
            part2 = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            part3 = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            
            # The delimiter pattern from HAR: %25fo%40~%5BC.4L1.ZDcp
            token = f"{part1}%25fo%40~%5BC.4L1.ZDcp{part2}%25fo%40~%5BC.4L1.ZDcp{part3}"
            
            url = f"{self.BASE_URL}/web_sfapi/{token}"
            urls.append(url)
        
        return urls
    
    def construct_pdf_candidates(self, subject: str, year: str, 
                                  session: str, paper: str, 
                                  variant: str) -> List[Tuple[str, str]]:
        """
        Step 2: Construct candidate PDF URLs using tokens.
        
        The PDF URL pattern from HAR:
        /paperdownload/dir_v3/{encrypted_parts_separated_by_delimiter}
        """
        print(f"[{self.session_id}] Step 2: Constructing PDF URLs...")
        
        candidates = []
        short_year = year[2:]
        filename = f"{subject}_{session}{short_year}_{paper}_{variant}.pdf"
        
        # Strategy 1: Use acquired tokens directly
        for token in self.tokens:
            if token.get('decoded') and len(token['decoded']) > 16:
                # Use token as encryption key
                key = base64.b64encode(token['decoded']).decode().replace('=', '')[:48]
                
                # Construct URL with token-based encoding
                encoded = f"{key}%25fo%40~%5BC.4L1.ZDcp"
                url = f"{self.BASE_URL}/paperdownload/dir_v3/{encoded}"
                candidates.append(('token_direct', url))
        
        # Strategy 2: Token + filename hash combination
        for token in self.tokens:
            if token.get('decoded'):
                try:
                    # Combine token with filename
                    combined = hashlib.sha256(
                        token['decoded'] + filename.encode()
                    ).hexdigest()[:64]
                    
                    # Add delimiter and more data
                    encoded = f"{combined}%25fo%40~%5BC.4L1.ZDcp"
                    url = f"{self.BASE_URL}/paperdownload/dir_v3/{encoded}"
                    candidates.append(('token_hash', url))
                except:
                    pass
        
        # Strategy 3: Encoded filename with token salt
        b64_filename = base64.b64encode(filename.encode()).decode().replace('=', '')
        for token in self.tokens:
            if token.get('encoded'):
                salt = token['encoded'][:32]
                encoded = f"{salt}%25fo%40~%5BC.4L1.ZDcp{b64_filename}"
                url = f"{self.BASE_URL}/paperdownload/dir_v3/{encoded}"
                candidates.append(('token_salt', url))
        
        # Strategy 4: Try viewer URL first (triggers session)
        for token in self.tokens:
            if token.get('encoded'):
                # Construct viewer URL that will fetch PDF
                viewer_file = f"/paperdownload/dir_v3/{token['encoded'][:64]}"
                viewer_url = f"{self.BASE_URL}/paperdownload/pdf/?file={urllib.parse.quote(viewer_file)}"
                candidates.append(('viewer', viewer_url))
        
        print(f"[{self.session_id}] Generated {len(candidates)} candidate URLs")
        return candidates
    
    def try_download(self, url: str, output_path: str) -> Tuple[bool, int]:
        """Attempt to download PDF from URL."""
        try:
            headers = self._get_headers(self.WEB_URL + '/papersearch')
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=20) as resp:
                data = resp.read()
                
                # Check for PDF magic bytes
                if len(data) > 10000 and data[:4] == b'%PDF':
                    with open(output_path, 'wb') as f:
                        f.write(data)
                    return True, len(data)
                
                return False, len(data)
                
        except Exception as e:
            return False, 0
    
    def download(self, subject: str, year: str, session: str, 
                 paper: str, variant: str) -> Optional[str]:
        """Full automated download workflow."""
        
        output_file = f"{subject}_{session}{year[2:]}_{paper}_{variant}.pdf"
        output_path = os.path.join(self.output_dir, output_file)
        
        print(f"\n{'='*70}")
        print(f"Easy-Paper Automated Download")
        print(f"{'='*70}")
        print(f"Paper: {subject} | Year: {year} | Session: {session}")
        print(f"Type: {paper} | Variant: {variant}")
        print(f"Session ID: {self.session_id}")
        print(f"{'='*70}\n")
        
        # Step 1: Acquire tokens
        if not self.acquire_session_tokens():
            print("✗ Failed to acquire session tokens")
            return None
        
        # Step 2: Construct candidate URLs
        candidates = self.construct_pdf_candidates(subject, year, session, paper, variant)
        
        if not candidates:
            print("✗ No candidate URLs generated")
            return None
        
        # Step 3: Try each candidate
        print(f"\nStep 3: Testing {len(candidates)} URLs...")
        
        for i, (strategy, url) in enumerate(candidates):
            print(f"  [{i+1}/{len(candidates)}] {strategy}: {url[:50]}...")
            
            success, size = self.try_download(url, output_path)
            
            if success:
                print(f"\n✓ SUCCESS!")
                print(f"  File: {output_path}")
                print(f"  Size: {size:,} bytes")
                return output_path
            
            time.sleep(0.3)
        
        print(f"\n✗ All {len(candidates)} candidates failed")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Fully automated Easy-Paper PDF downloader",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python easypaper_auto.py -c 9702 -y 2024 -s s -p qp -v 12
  python easypaper_auto.py --subject 9709 --year 2023 --session w --paper ms --variant 13
  python easypaper_auto.py -c 9701 -y 2024 -s m -p qp -v 11 -o ./papers/
        """
    )
    
    parser.add_argument("--subject", "-c", required=True, help="Subject code (e.g., 9702, 9709)")
    parser.add_argument("--year", "-y", required=True, help="Year (e.g., 2024)")
    parser.add_argument("--session", "-s", required=True, help="s (Summer), w (Winter), m (March)")
    parser.add_argument("--paper", "-p", default="qp", help="Paper type: qp, ms, er, gt")
    parser.add_argument("--variant", "-v", required=True, help="Variant: 11, 12, 13, 21, etc.")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    
    args = parser.parse_args()
    
    downloader = EasyPaperAutomated(output_dir=args.output)
    result = downloader.download(
        subject=args.subject,
        year=args.year,
        session=args.session,
        paper=args.paper,
        variant=args.variant
    )
    
    if result:
        print(f"\n{'='*70}")
        print(f"✓ Downloaded: {result}")
        print(f"{'='*70}")
        sys.exit(0)
    else:
        print(f"\n{'='*70}")
        print("✗ Download failed")
        print(f"{'='*70}")
        sys.exit(1)


if __name__ == "__main__":
    main()
