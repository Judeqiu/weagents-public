#!/usr/bin/env python3
"""
Easy-Paper Auto Downloader - Fully Automated

Attempts to download PDFs using multiple strategies based on HAR analysis.
Does not stop on failure - tries all possible approaches.

Usage:
    python download_auto.py --subject 9702 --year 2024 --session s --paper qp --variant 12
    python download_auto.py --subject 9709 --year 2023 --session w --paper ms --variant 13 --output ./papers/
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
from typing import Optional, Tuple


# SSL context for HTTPS requests
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE


class EasyPaperAutoDownloader:
    """Automated PDF downloader using multiple strategies."""
    
    BASE_URL = "https://server.easy-paper.com"
    VIEWER_URL = f"{BASE_URL}/paperdownload/pdf/"
    DOWNLOAD_URL = f"{BASE_URL}/paperdownload/dir_v3/"
    
    # User agents from HAR
    USER_AGENTS = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = output_dir
        self.session = self._generate_session()
        os.makedirs(output_dir, exist_ok=True)
    
    def _generate_session(self) -> str:
        """Generate a random session identifier."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    def _get_headers(self, referer: Optional[str] = None) -> dict:
        """Generate request headers based on HAR analysis."""
        headers = {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'application/pdf,application/octet-stream,*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        if referer:
            headers['Referer'] = referer
        else:
            headers['Referer'] = 'https://easy-paper.com/'
            headers['Origin'] = 'https://easy-paper.com'
        return headers
    
    def _encode_filename_v1(self, subject: str, year: str, session: str, paper: str, variant: str) -> str:
        """Strategy 1: Pipe-delimited path (from old skill attempt)."""
        # Get subject name
        subjects = {
            "9702": "Physics (9702)",
            "9709": "Mathematics (9709)",
            "9231": "Mathematics - Further (9231)",
            "9701": "Chemistry (9701)",
            "9700": "Biology (9700)",
            "9609": "Business (9609)",
            "9708": "Economics (9708)",
            "9706": "Accounting (9706)",
            "9696": "Geography (9696)",
            "9389": "History (9389)",
            "9489": "History (9489)",
            "9698": "Psychology (9698)",
            "9990": "Psychology (9990)",
            "9699": "Sociology (9699)",
            "9608": "Computer Science (9608)",
            "9618": "Computer Science (9618)",
            "9626": "Information Technology (9626)",
        }
        
        sessions_map = {"s": "Summer", "w": "Winter", "m": "March"}
        
        subject_name = subjects.get(subject, f"Subject ({subject})")
        session_name = sessions_map.get(session.lower(), session.capitalize())
        short_year = year[2:]
        
        filename = f"{subject}_{session}{short_year}_{paper}_{variant}.pdf"
        path = f"|CAIE|AS and A Level|{subject_name}|{year}|{session_name}|{filename}"
        
        # Try multiple encoding strategies
        encoded = base64.b64encode(path.encode()).decode()
        return encoded
    
    def _encode_filename_v2(self, subject: str, year: str, session: str, paper: str, variant: str) -> str:
        """Strategy 2: Direct filename encoding with HAR pattern."""
        short_year = year[2:]
        filename = f"{subject}_{session}{short_year}_{paper}_{variant}.pdf"
        
        # Create a hash-based token similar to HAR pattern
        data = f"{subject}:{year}:{session}:{paper}:{variant}:{self.session}"
        hash_token = hashlib.sha256(data.encode()).hexdigest()[:64]
        
        # HAR shows pattern: random_chars%fo@~[C.4L1.ZDcpmore_data
        # This appears to be: encrypted_data + delimiter + more_data
        
        # Generate similar pattern
        part1 = hash_token[:32]
        part2 = base64.b64encode(filename.encode()).decode().replace('=', '')[:40]
        part3 = hash_token[32:]
        
        # The delimiter from HAR: %fo@~[C.4L1.ZDcp
        delimiter = "%25fo%40~%5BC.4L1.ZDcp"
        
        return f"{part1}{delimiter}{part2}{delimiter}{part3}"
    
    def _encode_filename_v3(self, subject: str, year: str, session: str, paper: str, variant: str) -> list:
        """Strategy 3: Multiple hash variations."""
        short_year = year[2:]
        variants = []
        
        # Different combinations
        bases = [
            f"{subject}_{session}{short_year}_{paper}_{variant}.pdf",
            f"{subject}/{session}{short_year}/{paper}/{variant}",
            f"|CAIE|{subject}|{year}|{session}|{paper}|{variant}",
        ]
        
        for base in bases:
            # MD5
            md5_hash = hashlib.md5(base.encode()).hexdigest()
            variants.append(md5_hash)
            
            # SHA1
            sha1_hash = hashlib.sha1(base.encode()).hexdigest()
            variants.append(sha1_hash)
            
            # SHA256 truncated
            sha256_hash = hashlib.sha256(base.encode()).hexdigest()[:48]
            variants.append(sha256_hash)
            
            # Base64
            b64 = base64.b64encode(base.encode()).decode()
            variants.append(b64)
            
            # URL encoded
            url_enc = urllib.parse.quote(base)
            variants.append(url_enc)
        
        return variants
    
    def _try_web_sfapi(self, encoded_path: str) -> Optional[str]:
        """Try to get token from web_sfapi endpoint (from HAR analysis)."""
        try:
            # HAR shows: https://server.easy-paper.com/web_sfapi/{token}
            # The token appears to be base64-like
            
            token = base64.b64encode(f"{encoded_path}:{self.session}".encode()).decode()
            url = f"{self.BASE_URL}/web_sfapi/{urllib.parse.quote(token)}"
            
            headers = self._get_headers()
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=10) as resp:
                if resp.status == 200:
                    data = resp.read()
                    # Try to decode response - might contain PDF or decryption key
                    try:
                        decoded = base64.b64decode(data)
                        if decoded[:4] == b'%PDF':
                            return decoded
                    except:
                        pass
            
            return None
        except Exception:
            return None
    
    def _try_download(self, url: str, output_path: str) -> Tuple[bool, int]:
        """Attempt to download PDF from URL."""
        try:
            headers = self._get_headers()
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=30) as resp:
                if resp.status != 200:
                    return False, 0
                
                content_type = resp.headers.get('Content-Type', '')
                
                # Check if it's a PDF
                if 'application/pdf' not in content_type and 'octet-stream' not in content_type:
                    # Still try to read and check magic bytes
                    pass
                
                data = resp.read()
                
                # Verify PDF magic bytes
                if len(data) > 4 and data[:4] == b'%PDF':
                    with open(output_path, 'wb') as f:
                        f.write(data)
                    return True, len(data)
                
                return False, 0
                
        except urllib.error.HTTPError as e:
            return False, e.code
        except Exception:
            return False, 0
    
    def download(self, subject: str, year: str, session: str, paper: str, variant: str) -> Optional[str]:
        """
        Attempt to download PDF using all available strategies.
        Returns path to downloaded file or None.
        """
        output_filename = f"{subject}_{session}{year[2:]}_{paper}_{variant}.pdf"
        output_path = os.path.join(self.output_dir, output_filename)
        
        print(f"[{self.session}] Starting auto-download for:")
        print(f"  Subject: {subject}")
        print(f"  Year: {year}")
        print(f"  Session: {session}")
        print(f"  Paper: {paper}")
        print(f"  Variant: {variant}")
        print()
        
        strategies = []
        
        # Strategy 1: Try encoded filename variations
        print(f"[{self.session}] Strategy 1: Encoding variations...")
        
        enc_v1 = self._encode_filename_v1(subject, year, session, paper, variant)
        strategies.append(("base64_v1", enc_v1))
        
        enc_v2 = self._encode_filename_v2(subject, year, session, paper, variant)
        strategies.append(("hash_v2", enc_v2))
        
        enc_v3_list = self._encode_filename_v3(subject, year, session, paper, variant)
        for i, enc in enumerate(enc_v3_list):
            strategies.append((f"hash_v3_{i}", enc))
        
        # Try each strategy
        for strategy_name, encoded in strategies:
            # Construct URLs
            viewer_url = f"{self.VIEWER_URL}?file=%2Fpaperdownload%2Fdir_v3%2F{urllib.parse.quote(encoded)}"
            direct_url = f"{self.DOWNLOAD_URL}{urllib.parse.quote(encoded)}"
            
            # Try direct download first
            print(f"[{self.session}] Trying {strategy_name}: {direct_url[:60]}...")
            success, size = self._try_download(direct_url, output_path)
            
            if success:
                print(f"[{self.session}] ✓ SUCCESS! Downloaded {size} bytes")
                print(f"[{self.session}] Saved to: {output_path}")
                return output_path
            
            # Try with viewer URL as referer
            time.sleep(0.5)  # Be polite
        
        # Strategy 2: Try web_sfapi approach
        print(f"[{self.session}] Strategy 2: web_sfapi token approach...")
        for strategy_name, encoded in strategies[:3]:  # Try first 3
            result = self._try_web_sfapi(encoded)
            if result and isinstance(result, bytes):
                with open(output_path, 'wb') as f:
                    f.write(result)
                print(f"[{self.session}] ✓ SUCCESS via web_sfapi!")
                return output_path
            time.sleep(0.5)
        
        # Strategy 3: Brute force with random tokens (last resort)
        print(f"[{self.session}] Strategy 3: Testing random token patterns...")
        for i in range(5):
            random_token = ''.join(random.choices(string.ascii_letters + string.digits, k=48))
            url = f"{self.DOWNLOAD_URL}{random_token}"
            success, _ = self._try_download(url, output_path)
            if success:
                print(f"[{self.session}] ✓ SUCCESS with random token!")
                return output_path
            time.sleep(0.3)
        
        print(f"[{self.session}] ✗ All strategies failed")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Auto-download PDFs from easy-paper.com (tries all strategies)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python download_auto.py --subject 9702 --year 2024 --session s --paper qp --variant 12
  python download_auto.py --subject 9709 --year 2023 --session w --paper ms --variant 13
  python download_auto.py --subject 9701 --year 2024 --session m --paper qp --variant 12 -o ./downloads/
        """
    )
    
    parser.add_argument("--subject", "-c", required=True, help="Subject code (e.g., 9702, 9709)")
    parser.add_argument("--year", "-y", required=True, help="Year (e.g., 2024)")
    parser.add_argument("--session", "-s", required=True, help="Session: s (Summer), w (Winter), m (March)")
    parser.add_argument("--paper", "-p", default="qp", help="Paper type: qp, ms, er, gt (default: qp)")
    parser.add_argument("--variant", "-v", required=True, help="Variant: 11, 12, 13, 21, etc.")
    parser.add_argument("--output", "-o", default=".", help="Output directory (default: current)")
    parser.add_argument("--attempts", "-a", type=int, default=1, help="Number of retry attempts (default: 1)")
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Easy-Paper Auto Downloader")
    print("=" * 70)
    print()
    
    for attempt in range(args.attempts):
        if attempt > 0:
            print(f"\n{'='*70}")
            print(f"Retry attempt {attempt + 1}/{args.attempts}")
            print(f"{'='*70}\n")
        
        downloader = EasyPaperAutoDownloader(output_dir=args.output)
        result = downloader.download(
            subject=args.subject,
            year=args.year,
            session=args.session,
            paper=args.paper,
            variant=args.variant
        )
        
        if result:
            print()
            print("=" * 70)
            print(f"✓ SUCCESS! PDF downloaded to: {result}")
            print("=" * 70)
            sys.exit(0)
    
    print()
    print("=" * 70)
    print("✗ Download failed after all attempts")
    print("=" * 70)
    print()
    print("Possible reasons:")
    print("  - Site structure has changed")
    print("  - Encryption method updated")
    print("  - Rate limiting active")
    print("  - Paper not available")
    print()
    print("Try:")
    print("  - Using a VPN or different IP")
    print("  - Checking if paper exists on website")
    print("  - Manual download via mobile app")
    sys.exit(1)


if __name__ == "__main__":
    main()
