#!/usr/bin/env python3
"""
Extract PDFs from browser HAR files.

Usage:
    python extract_from_har.py capture.har --output paper.pdf
    python extract_from_har.py capture.har  # Auto-detect output name

The HAR file should be captured while viewing a PDF on easy-paper.com:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Check "Preserve log"
4. Open the paper PDF
5. Right-click in Network tab → "Save all as HAR with content"
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path


def extract_pdfs_from_har(har_path: str, output_dir: str = ".") -> list:
    """
    Extract all PDFs from a HAR file.
    
    Args:
        har_path: Path to HAR file
        output_dir: Directory to save PDFs
        
    Returns:
        List of paths to extracted PDFs
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Loading HAR file: {har_path}")
    
    with open(har_path, 'r', encoding='utf-8') as f:
        har = json.load(f)
    
    entries = har.get('log', {}).get('entries', [])
    print(f"Found {len(entries)} entries")
    
    extracted = []
    
    for i, entry in enumerate(entries):
        response = entry.get('response', {})
        content = response.get('content', {})
        
        mime_type = content.get('mimeType', '')
        
        # Check if this is a PDF
        if 'pdf' in mime_type.lower() or 'application/octet-stream' in mime_type:
            url = entry.get('request', {}).get('url', '')
            size = content.get('size', 0)
            
            print(f"\n[{i}] Potential PDF:")
            print(f"    URL: {url[:80]}...")
            print(f"    Size: {size:,} bytes")
            print(f"    MIME: {mime_type}")
            
            # Get the content
            text = content.get('text', '')
            encoding = content.get('encoding', '')
            
            if not text:
                print("    No content text")
                continue
                
            try:
                # Decode based on encoding
                if encoding == 'base64':
                    pdf_data = base64.b64decode(text)
                else:
                    pdf_data = text.encode('latin-1')
                    
                # Verify it's a PDF
                if not pdf_data.startswith(b'%PDF'):
                    # Check if it might be encrypted
                    if len(pdf_data) < 1000:
                        print(f"    Too small or encrypted ({len(pdf_data)} bytes)")
                        continue
                    print(f"    Warning: Doesn't start with %PDF signature")
                    
                # Generate output name
                output_name = f"extracted_{i:03d}.pdf"
                
                # Try to get better name from URL
                if 'paperdownload' in url or 'pdf' in url.lower():
                    # Extract paper info from URL if possible
                    url_parts = url.split('/')
                    if url_parts:
                        last_part = url_parts[-1].split('?')[0]
                        if last_part and len(last_part) > 5:
                            output_name = f"{last_part[:50]}.pdf"
                            
                output_path = output_dir / output_name
                
                # Save PDF
                with open(output_path, 'wb') as f:
                    f.write(pdf_data)
                    
                print(f"    ✓ Saved: {output_path} ({len(pdf_data):,} bytes)")
                extracted.append(str(output_path))
                
            except Exception as e:
                print(f"    ✗ Error: {e}")
                
    return extracted


def main():
    parser = argparse.ArgumentParser(
        description="Extract PDFs from browser HAR files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
How to capture HAR:
  1. Open browser DevTools (F12)
  2. Go to Network tab
  3. Check "Preserve log"
  4. Navigate to the paper on easy-paper.com
  5. Wait for PDF to fully load
  6. Right-click in Network tab → "Save all as HAR with content"
  7. Run: python extract_from_har.py my_capture.har
        """
    )
    
    parser.add_argument("har_file", help="Path to HAR file")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--list", "-l", action="store_true", help="List only, don't extract")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.har_file):
        print(f"Error: HAR file not found: {args.har_file}")
        sys.exit(1)
        
    if args.list:
        # Just list PDFs in HAR
        with open(args.har_file, 'r') as f:
            har = json.load(f)
        
        entries = har.get('log', {}).get('entries', [])
        print(f"\nPDFs found in {args.har_file}:")
        print("="*70)
        
        for i, entry in enumerate(entries):
            response = entry.get('response', {})
            content = response.get('content', {})
            mime_type = content.get('mimeType', '')
            
            if 'pdf' in mime_type.lower():
                url = entry.get('request', {}).get('url', '')
                size = content.get('size', 0)
                print(f"\n[{i}] {size:,} bytes")
                print(f"    {url[:70]}...")
    else:
        # Extract PDFs
        extracted = extract_pdfs_from_har(args.har_file, args.output)
        
        print(f"\n{'='*70}")
        if extracted:
            print(f"✓ Extracted {len(extracted)} PDF(s):")
            for path in extracted:
                print(f"  - {path}")
        else:
            print("✗ No PDFs found in HAR file")
            print("\nTroubleshooting:")
            print("1. Make sure you captured HAR while PDF was open")
            print("2. Check 'Preserve log' was enabled")
            print("3. Try selecting 'Save all as HAR with content'")
        print(f"{'='*70}")


if __name__ == "__main__":
    main()
