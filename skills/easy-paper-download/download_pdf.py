#!/usr/bin/env python3
"""
Easy-Paper PDF Downloader

This script downloads PDFs from easy-paper.com based on the workflow
analyzed from HAR files.

Usage:
    python download_pdf.py <viewer_url>
    python download_pdf.py https://server.easy-paper.com/paperdownload/pdf/?file=...
"""

import sys
import urllib.parse
import urllib.request
import ssl
import os


def construct_pdf_url(viewer_url: str) -> str:
    """
    Construct the direct PDF URL from the viewer URL.
    
    The viewer URL looks like:
    https://server.easy-paper.com/paperdownload/pdf/?file=%2Fpaperdownload%2Fdir_v3%2F...
    
    The PDF URL is:
    https://server.easy-paper.com/paperdownload/dir_v3/...
    """
    # Parse the viewer URL
    parsed = urllib.parse.urlparse(viewer_url)
    params = urllib.parse.parse_qs(parsed.query)
    
    if 'file' not in params:
        raise ValueError("URL does not contain 'file' parameter")
    
    # Get the file parameter and decode it
    file_param = params['file'][0]
    
    # Double-decode because the URL might be double-encoded
    decoded_path = urllib.parse.unquote(urllib.parse.unquote(file_param))
    
    # Construct the PDF URL
    pdf_url = f"https://server.easy-paper.com{decoded_path}"
    
    return pdf_url


def download_pdf(pdf_url: str, output_path: str = None, viewer_url: str = None) -> str:
    """
    Download the PDF from the given URL.
    
    Args:
        pdf_url: The direct PDF URL
        output_path: Where to save the file (optional)
        viewer_url: The original viewer URL for Referer header
        
    Returns:
        Path to the downloaded file
    """
    # Create SSL context that doesn't verify certificates
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Prepare headers based on HAR analysis
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/pdf,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Origin': 'https://easy-paper.com',
    }
    
    # Add Referer if we have the viewer URL
    if viewer_url:
        headers['Referer'] = viewer_url
    else:
        # Construct a referer from the PDF URL
        # The viewer URL is the PDF URL with /pdf/?file= prepended
        headers['Referer'] = f"https://server.easy-paper.com/paperdownload/pdf/?file={urllib.parse.quote(pdf_url.replace('https://server.easy-paper.com', ''), safe='')}"
    
    # Create request
    req = urllib.request.Request(pdf_url, headers=headers)
    
    print(f"Downloading from: {pdf_url[:80]}...")
    print(f"Referer: {headers['Referer'][:80]}...")
    
    try:
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            content_type = response.headers.get('Content-Type', '')
            content_length = response.headers.get('Content-Length')
            
            print(f"Content-Type: {content_type}")
            if content_length:
                print(f"Content-Length: {int(content_length):,} bytes")
            
            data = response.read()
            
            print(f"Downloaded {len(data):,} bytes")
            
            # Check if it's actually a PDF
            if data[:4] == b'%PDF':
                print("✓ Valid PDF file detected!")
            else:
                print(f"⚠ Warning: File doesn't start with PDF signature")
                print(f"  First 100 bytes: {data[:100]}")
            
            # Determine output filename
            if not output_path:
                # Try to get filename from Content-Disposition header
                content_disp = response.headers.get('Content-Disposition', '')
                if 'filename=' in content_disp:
                    # Extract filename
                    parts = content_disp.split('filename=')
                    if len(parts) > 1:
                        output_path = parts[-1].strip('"\'').replace("utf-8''", '')
                
                if not output_path:
                    output_path = "downloaded_paper.pdf"
            
            # Save the file
            with open(output_path, 'wb') as f:
                f.write(data)
            
            print(f"✓ Saved to: {output_path}")
            return output_path
            
    except urllib.error.HTTPError as e:
        print(f"✗ HTTP Error {e.code}: {e.reason}")
        print(f"  This usually means the session has expired.")
        print(f"  Solution: Get a fresh URL from the mobile app.")
        raise
    except Exception as e:
        print(f"✗ Error: {e}")
        raise


def main():
    if len(sys.argv) < 2:
        print("Usage: python download_pdf.py <viewer_url>")
        print("       python download_pdf.py https://server.easy-paper.com/paperdownload/pdf/?file=...")
        print()
        print("You can also pass the direct PDF URL (with /dir_v3/ in the path)")
        sys.exit(1)
    
    url = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check if this is a viewer URL or direct PDF URL
    if '/pdf/?file=' in url:
        # This is a viewer URL, construct the PDF URL
        print("=" * 70)
        print("Easy-Paper PDF Downloader")
        print("=" * 70)
        print(f"\nViewer URL detected: {url[:80]}...")
        
        try:
            pdf_url = construct_pdf_url(url)
            print(f"\nConstructed PDF URL: {pdf_url[:80]}...")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        # Assume it's already the PDF URL
        pdf_url = url
        print(f"\nUsing direct PDF URL: {pdf_url[:80]}...")
    
    print()
    
    try:
        downloaded_file = download_pdf(pdf_url, output, url if '/pdf/?file=' in url else None)
        print(f"\n✓ Success! File saved: {downloaded_file}")
    except Exception as e:
        print(f"\n✗ Failed to download: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
