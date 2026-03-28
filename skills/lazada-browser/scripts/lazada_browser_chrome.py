#!/usr/bin/env python3
"""
Lazada Seller Center Browser Automation - Chrome CDP Version
Uses real Chrome browser with persistent profile via CDP connection.
"""

import json
import sys
import os
import requests
import re
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright

# Chrome CDP Configuration
CHROME_CDP_URL = os.environ.get("CHROME_CDP_URL", "http://127.0.0.1:9222")
CHROME_PROFILE = os.environ.get("CHROME_PROFILE", "/home/enraie/.chrome-openclaw")

# Alert configuration
ALERT_EMAIL = os.environ.get("ALERT_EMAIL", "david@lextok.com")
BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "ono@lextok.com")
FROM_NAME = os.environ.get("FROM_NAME", "Enraie Bot")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "-1003848052058")


def check_chrome_connection():
    """Check if Chrome is running and accessible via CDP."""
    try:
        response = requests.get(f"{CHROME_CDP_URL}/json/version", timeout=5)
        if response.status_code == 200:
            version_info = response.json()
            print(f"[INFO] Connected to Chrome: {version_info.get('Browser', 'Unknown')}")
            return True
    except Exception as e:
        print(f"[ERROR] Cannot connect to Chrome at {CHROME_CDP_URL}: {e}", file=sys.stderr)
        print("[HINT] Make sure Chrome is running with --remote-debugging-port=9222", file=sys.stderr)
    return False


def send_alert_email(failure_reason, url_attempted, details=""):
    """Send email alert when Lazada access fails."""
    if not BREVO_API_KEY:
        print("[WARNING] BREVO_API_KEY not set. Cannot send alert email.", file=sys.stderr)
        return False
    
    subject = f"🚨 Lazada Access Failed - {failure_reason}"
    
    body = f"""
Hi David,

I failed to access the Lazada Seller Center due to: {failure_reason}

Details:
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- URL Attempted: {url_attempted}
- Error Details: {details}
- Bot: Enraie

The Chrome browser session may have expired or the account may have been logged out. 
Please check the Chrome profile at: {CHROME_PROFILE}

You can manually log in again via the browser.

Thanks,
Enraie Bot
    """
    
    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "sender": {"email": EMAIL_FROM, "name": FROM_NAME},
                "to": [{"email": ALERT_EMAIL}],
                "subject": subject,
                "textContent": body
            },
            timeout=30
        )
        
        if response.status_code in [200, 201, 202]:
            print(f"[ALERT] Email sent to {ALERT_EMAIL}")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}", file=sys.stderr)
    return False


def send_telegram_alert(failure_reason, url_attempted, details=""):
    """Send Telegram message alert when Lazada access fails."""
    if not TELEGRAM_BOT_TOKEN:
        print("[WARNING] TELEGRAM_BOT_TOKEN not set. Cannot send Telegram alert.", file=sys.stderr)
        return False
    
    message = f"""🚨 <b>Lazada Access Failed - Enraie</b>

<b>Reason:</b> {failure_reason}
<b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
<b>URL:</b> {url_attempted}

<b>Details:</b>
{details}

The Chrome browser session may need re-login.
Profile: <code>{CHROME_PROFILE}</code>

cc: @Dave_881010
    """
    
    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            },
            timeout=30
        )
        
        if response.status_code == 200 and response.json().get("ok"):
            print(f"[ALERT] Telegram message sent to group")
            return True
    except Exception as e:
        print(f"[ERROR] Exception sending Telegram message: {e}", file=sys.stderr)
    return False


def send_all_alerts(failure_reason, url_attempted, details=""):
    """Send both email and Telegram alerts."""
    email_sent = send_alert_email(failure_reason, url_attempted, details)
    telegram_sent = send_telegram_alert(failure_reason, url_attempted, details)
    return {"email_sent": email_sent, "telegram_sent": telegram_sent}


def detect_auth_failure(page, url_attempted):
    """Detect if the page load resulted in an authentication failure."""
    title = page.title()
    current_url = page.url
    html_content = page.content()
    
    # Check for login page indicators
    login_indicators = [
        "login" in title.lower(),
        "sign in" in title.lower(),
        "password" in html_content.lower() and "login" in html_content.lower(),
        current_url.startswith("https://member.lazada.sg/user/login"),
        current_url.startswith("https://sellercenter.lazada.sg/user/login"),
    ]
    
    if any(login_indicators):
        return True, "Session Expired - Redirected to Login", f"URL: {current_url}, Title: {title}"
    
    # Check for offline page (old orders page)
    if "offline" in title.lower() or "offline" in current_url.lower():
        if "order" in url_attempted.lower() and "#!/" not in url_attempted:
            return True, "Orders Page Offline - Possible Session Issue", f"URL: {current_url}"
    
    # Check for error pages
    error_indicators = [
        "access denied" in title.lower(),
        "403" in title.lower(),
        "401" in title.lower(),
        "unauthorized" in title.lower(),
        "session expired" in html_content.lower(),
        "please log in" in html_content.lower(),
    ]
    
    if any(error_indicators):
        return True, "Access Denied or Session Expired", f"URL: {current_url}, Title: {title}"
    
    # Check for empty/different page than expected
    if len(html_content) < 5000 and "sellercenter.lazada.sg" in current_url:
        return True, "Page Content Too Small - Possible Redirect", f"Content length: {len(html_content)}"
    
    return False, None, None


def visit_lazada(url="https://sellercenter.lazada.sg/#!/", screenshot_path=None, wait_seconds=5, send_alert=True):
    """
    Visit Lazada Seller Center using Chrome CDP connection.
    Chrome profile already contains logged-in session.
    """
    # Check Chrome connection first
    if not check_chrome_connection():
        error_msg = f"Cannot connect to Chrome at {CHROME_CDP_URL}. Is Chrome running?"
        if send_alert:
            send_all_alerts("Chrome Connection Failed", url, error_msg)
        return {
            'status': 'error',
            'error': error_msg,
            'title': 'Error',
            'url': url,
            'html': ''
        }
    
    with sync_playwright() as p:
        # Connect to existing Chrome via CDP
        try:
            browser = p.chromium.connect_over_cdp(CHROME_CDP_URL)
            print(f"[INFO] Connected to Chrome via CDP")
        except Exception as e:
            error_msg = f"Failed to connect to Chrome CDP: {e}"
            if send_alert:
                send_all_alerts("Chrome CDP Connection Failed", url, error_msg)
            return {
                'status': 'error',
                'error': error_msg,
                'title': 'Error',
                'url': url,
                'html': ''
            }
        
        # Get existing context or create new one
        contexts = browser.contexts
        if contexts:
            context = contexts[0]
            print(f"[INFO] Using existing browser context")
        else:
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            print(f"[INFO] Created new browser context")
        
        # Try to use existing Lazada page, or create new one
        page = None
        pages = context.pages
        
        # Look for existing Lazada Seller Center page
        for existing_page in pages:
            if 'sellercenter.lazada.sg' in existing_page.url and '#!/' in existing_page.url:
                page = existing_page
                print(f"[INFO] Using existing Lazada page: {page.url}")
                break
        
        if page is None:
            # Create new page and navigate
            page = context.new_page()
            try:
                print(f"[INFO] Navigating to: {url}")
                page.goto(url, wait_until='domcontentloaded', timeout=60000)
                page.wait_for_timeout(wait_seconds * 1000)
            except Exception as e:
                error_msg = f"Page load timeout or error: {e}"
                if send_alert:
                    send_all_alerts("Page Load Failure", url, error_msg)
                return {
                    'status': 'error',
                    'error': error_msg,
                    'title': 'Error',
                    'url': url,
                    'html': ''
                }
        else:
            # Refresh existing page and wait
            try:
                page.reload(wait_until='domcontentloaded', timeout=60000)
                page.wait_for_timeout(wait_seconds * 1000)
            except Exception as e:
                print(f"[WARNING] Reload failed, using existing content: {e}")
        
        # Check for authentication failures
        is_failure, failure_reason, details = detect_auth_failure(page, url)
        
        if is_failure and send_alert:
            if screenshot_path:
                page.screenshot(path=screenshot_path, full_page=True)
            
            send_all_alerts(failure_reason, url, details)
            
            browser.close()
            return {
                'status': 'auth_failed',
                'error': failure_reason,
                'details': details,
                'title': page.title(),
                'url': page.url,
                'html': page.content()
            }
        
        # Successful load
        result = {
            'status': 'success',
            'title': page.title(),
            'url': page.url,
            'html': page.content()
        }
        
        if screenshot_path:
            page.screenshot(path=screenshot_path, full_page=True)
            result['screenshot'] = str(screenshot_path)
        
        # Don't close the page if it was an existing Lazada page
        # This keeps the session warm for next check
        if 'sellercenter.lazada.sg' not in page.url or '#!/' not in page.url:
            page.close()
        
        return result


def check_orders(send_alert=True):
    """Check for new orders on the dashboard."""
    result = visit_lazada("https://sellercenter.lazada.sg/#!/", send_alert=send_alert)
    
    if result['status'] != 'success':
        return {
            'status': result['status'],
            'error': result.get('error', 'Unknown error'),
            'orders': 'N/A',
            'pending_pack': 'N/A',
            'pending_shipping': 'N/A',
            'pending_return_refund': 'N/A',
            'raw_html_length': 0,
            'user_action_required': 'Please check Chrome - session may have expired or page is on login screen'
        }
    
    # Parse order counts from the HTML
    html = result['html']
    
    order_info = {
        'status': 'success',
        'orders': '0',
        'pending_pack': '0',
        'pending_shipping': '0',
        'pending_return_refund': '0',
        'raw_html_length': len(html)
    }
    
    # Check if we're on login page (session expired)
    if 'login' in result.get('title', '').lower() or 'login' in result.get('url', '').lower():
        order_info['status'] = 'login_required'
        order_info['user_action_required'] = 'Please check Chrome - you are on the login page. Need to log in.'
        return order_info
    
    # Check if page content is too small (possible redirect)
    if len(html) < 5000:
        order_info['status'] = 'page_error'
        order_info['user_action_required'] = 'Please check Chrome - page content is too small, may be redirected'
        return order_info
    
    patterns = [
        (r'Orders\s*</div>\s*<div[^>]*>(\d+)', 'orders'),
        (r'Pending Pack\s*</div>\s*<div[^>]*>(\d+)', 'pending_pack'),
        (r'Pending Shipping\s*</div>\s*<div[^>]*>(\d+)', 'pending_shipping'),
    ]
    
    for pattern, key in patterns:
        match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
        if match:
            order_info[key] = match.group(1)
    
    return order_info


def navigate_to_orders(send_alert=True):
    """Navigate to the Orders page."""
    return visit_lazada("https://sellercenter.lazada.sg/#!/", send_alert=send_alert)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Lazada Seller Center Browser - Chrome CDP Version')
    parser.add_argument('--url', default='https://sellercenter.lazada.sg/#!/', help='URL to visit')
    parser.add_argument('--screenshot', help='Path to save screenshot')
    parser.add_argument('--check-orders', action='store_true', help='Check order counts')
    parser.add_argument('--wait', type=int, default=5, help='Seconds to wait for page load')
    parser.add_argument('--no-alert', action='store_true', help='Disable email alerts on failure')
    parser.add_argument('--cdp-url', default='http://127.0.0.1:9222', help='Chrome CDP URL')
    
    args = parser.parse_args()
    
    # Set CDP URL from argument
    CHROME_CDP_URL = args.cdp_url
    
    send_alert = not args.no_alert
    
    if args.check_orders:
        info = check_orders(send_alert=send_alert)
        print(json.dumps(info, indent=2))
    else:
        result = visit_lazada(args.url, args.screenshot, args.wait, send_alert=send_alert)
        
        if result['status'] == 'auth_failed':
            print(f"[AUTH FAILED] {result['error']}")
            print(f"[DETAILS] {result.get('details', '')}")
            print(f"[ALERT] Notifications sent")
            sys.exit(1)
        elif result['status'] == 'error':
            print(f"[ERROR] {result['error']}")
            sys.exit(1)
        else:
            print(f"Title: {result['title']}")
            print(f"URL: {result['url']}")
            if result.get('screenshot'):
                print(f"Screenshot: {result['screenshot']}")
            print(f"\nHTML length: {len(result['html'])} chars")
