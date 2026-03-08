#!/usr/bin/env python3
"""
question-finder/scripts/search_questions.py

CLI helper to search educational websites for exam questions and past papers.
Returns a ranked list of URLs with titles.

Usage:
    python3 search_questions.py --subject math --level alevel --topic algebra
    python3 search_questions.py --subject physics --level gcse --board aqa
    python3 search_questions.py --subject chemistry --board caie --year 2023

Dependencies:
    pip install requests beautifulsoup4
"""

import argparse
import sys
import urllib.parse
import json
from typing import Optional

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Missing dependencies. Run: pip install requests beautifulsoup4", file=sys.stderr)
    sys.exit(1)

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    )
}

# Map user-friendly subject names → PMT and URL slugs
SUBJECT_SLUG_MAP = {
    "math": "maths",
    "maths": "maths",
    "mathematics": "maths",
    "physics": "physics",
    "chemistry": "chemistry",
    "biology": "biology",
    "economics": "economics",
    "english": "english",
    "cs": "computer-science",
    "computer science": "computer-science",
    "computer-science": "computer-science",
    "psychology": "psychology",
    "history": "history",
    "geography": "geography",
    "further maths": "further-maths",
    "further-maths": "further-maths",
    "further mathematics": "further-maths",
}

LEVEL_SLUG_MAP = {
    "alevel": "a-level",
    "a-level": "a-level",
    "a level": "a-level",
    "gcse": "gcse",
    "igcse": "igcse",
    "ib": "ib",
    "sat": "sat",
    "ap": "ap",
}

CAIE_CODES = {
    "physics": "9702",
    "mathematics": "9709",
    "maths": "9709",
    "math": "9709",
    "chemistry": "9701",
    "biology": "9700",
    "computer-science": "9618",
    "economics": "9708",
    "psychology": "9990",
    "further-maths": "9231",
    "english": "9093",
}

SITE_ALIASES = {
    "pmt": "pmt",
    "physicsandmathstutor": "pmt",
    "savemyexams": "savemyexams",
    "sme": "savemyexams",
    "easyp": "easypaper",
    "easypaper": "easypaper",
    "mathsgenie": "mathsgenie",
    "khanacademy": "khanacademy",
    "khan": "khanacademy",
    "google": "google",
}


# ─────────────────────────────────────────────
# Searchers
# ─────────────────────────────────────────────

def fetch_html(url: str) -> Optional[BeautifulSoup]:
    """Fetch a URL and return parsed BeautifulSoup, or None on failure."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"  [warn] Could not fetch {url}: {e}", file=sys.stderr)
        return None


def search_pmt(subject: str, level: str, topic: Optional[str], limit: int) -> list[dict]:
    """Search Physics & Maths Tutor via direct URL and Google site: search."""
    results = []
    slug_subject = SUBJECT_SLUG_MAP.get(subject.lower(), subject.lower())
    slug_level = LEVEL_SLUG_MAP.get(level.lower(), level.lower())

    # Try direct URL first
    if topic:
        topic_slug = topic.lower().replace(" ", "-")
        direct_url = f"https://www.physicsandmathstutor.com/{slug_subject}/{slug_level}/{topic_slug}/"
        results.append({
            "title": f"PMT — {subject.title()} {level.upper()} {topic.title()} Questions",
            "url": direct_url,
            "source": "physicsandmathstutor.com",
            "note": "Direct topic page (check if URL exists)"
        })

    # Google site: search as supplemental
    query = f'site:physicsandmathstutor.com {slug_level} {slug_subject}'
    if topic:
        query += f' {topic}'
    query += ' questions'
    google_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
    results.append({
        "title": f"Google: PMT search for {subject} {level}" + (f" {topic}" if topic else ""),
        "url": google_url,
        "source": "google → physicsandmathstutor.com",
        "note": "Google site: search — open in browser, then click results"
    })

    # Try fetching the PMT search page
    pmt_search_url = f"https://www.physicsandmathstutor.com/{slug_subject}/{slug_level}/"
    soup = fetch_html(pmt_search_url)
    if soup:
        links = soup.find_all("a", href=True)
        for link in links:
            href = link["href"]
            text = link.get_text(strip=True)
            if topic and topic.lower() not in text.lower() and topic.lower() not in href.lower():
                continue
            if text and len(text) > 5 and "physicsandmathstutor" in href or href.startswith("/"):
                full_url = href if href.startswith("http") else f"https://www.physicsandmathstutor.com{href}"
                results.append({
                    "title": text,
                    "url": full_url,
                    "source": "physicsandmathstutor.com",
                    "note": ""
                })
            if len(results) >= limit:
                break

    return results[:limit]


def search_savemyexams(subject: str, level: str, topic: Optional[str], limit: int) -> list[dict]:
    """Return Save My Exams search links (browser automation needed for full results)."""
    slug_subject = SUBJECT_SLUG_MAP.get(subject.lower(), subject.lower())
    slug_level = LEVEL_SLUG_MAP.get(level.lower(), level.lower())
    query = f"{slug_level} {slug_subject}" + (f" {topic}" if topic else "")
    encoded = urllib.parse.quote(query)

    return [
        {
            "title": f"Save My Exams — {subject.title()} {level.upper()}" + (f" {topic.title()}" if topic else ""),
            "url": f"https://www.savemyexams.com/search/?q={encoded}",
            "source": "savemyexams.com",
            "note": "JS-heavy site — use browser_subagent to interact with results"
        }
    ]


def search_mathsgenie(subject: str, level: str, topic: Optional[str], limit: int) -> list[dict]:
    """Search Maths Genie for topic worksheets."""
    if "math" not in subject.lower() and "maths" not in subject.lower():
        return []

    base = "https://www.mathsgenie.co.uk"
    # Actual Maths Genie URL paths (verified against live site)
    if "a-level" in level.lower() or level.lower() == "alevel":
        url = f"{base}/newalevel.php"
    else:
        url = f"{base}/gcse.php"

    results = [{
        "title": f"Maths Genie — {level.upper()} revision index",
        "url": url,
        "source": "mathsgenie.co.uk",
        "note": "Browse topic list and download PDFs"
    }]

    soup = fetch_html(url)
    if soup and topic:
        links = soup.find_all("a", href=True)
        for link in links:
            text = link.get_text(strip=True)
            href = link["href"]
            if topic.lower() in text.lower():
                full_url = href if href.startswith("http") else f"{base}/{href}"
                results.append({
                    "title": f"Maths Genie — {text}",
                    "url": full_url,
                    "source": "mathsgenie.co.uk",
                    "note": ""
                })
            if len(results) >= limit:
                break

    return results[:limit]


def search_easypaper(subject: str, year: Optional[str], limit: int) -> list[dict]:
    """Return Easy Paper search link for CAIE past papers."""
    slug = SUBJECT_SLUG_MAP.get(subject.lower(), subject.lower())
    code = CAIE_CODES.get(slug, "")
    query = f"{code} {year or ''}".strip()
    encoded = urllib.parse.quote(query)

    results = [{
        "title": f"Easy Paper — CAIE {subject.title()}" + (f" {year}" if year else ""),
        "url": f"https://easy-paper.com/papersearch?q={encoded}",
        "source": "easy-paper.com",
        "note": f"Subject code: {code}. Use easy-paper-download skill for automated PDF download."
    }]
    return results


def search_khanacademy(subject: str, topic: Optional[str], limit: int) -> list[dict]:
    """Return Khan Academy search link."""
    query = subject + (" " + topic if topic else "")
    encoded = urllib.parse.quote(query)
    return [{
        "title": f"Khan Academy — {subject.title()}" + (f": {topic.title()}" if topic else ""),
        "url": f"https://www.khanacademy.org/search?page_search_query={encoded}",
        "source": "khanacademy.org",
        "note": "Free practice questions with step-by-step solutions"
    }]


def search_google_fallback(subject: str, level: str, topic: Optional[str], board: Optional[str], limit: int) -> list[dict]:
    """Build a Google search URL as the last resort."""
    parts = [level, subject]
    if topic:
        parts.append(topic)
    if board and board != "any":
        parts.append(board)
    parts.append("questions past paper")
    query = " ".join(parts)
    return [{
        "title": f"Google Search — {query}",
        "url": f"https://www.google.com/search?q={urllib.parse.quote(query)}",
        "source": "google.com",
        "note": "Fallback: open in browser and pick the most relevant result"
    }]


# ─────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────

def route_and_search(args) -> list[dict]:
    subject = args.subject.lower()
    level = args.level.lower() if args.level else "alevel"
    board = args.board.lower() if args.board else "any"
    topic = args.topic
    year = args.year
    limit = args.limit
    forced_site = SITE_ALIASES.get(args.site.lower()) if args.site else None

    results = []

    if forced_site:
        if forced_site == "pmt":
            results += search_pmt(subject, level, topic, limit)
        elif forced_site == "savemyexams":
            results += search_savemyexams(subject, level, topic, limit)
        elif forced_site == "mathsgenie":
            results += search_mathsgenie(subject, level, topic, limit)
        elif forced_site == "easypaper":
            results += search_easypaper(subject, year, limit)
        elif forced_site == "khanacademy":
            results += search_khanacademy(subject, topic, limit)
        elif forced_site == "google":
            results += search_google_fallback(subject, level, topic, board, limit)
        return results

    # Auto-route
    if board in ("caie", "cambridge") or (subject in ("physics", "chemistry", "biology", "math", "maths") and year):
        results += search_easypaper(subject, year, limit)

    if level in ("alevel", "a-level", "a level", "gcse", "igcse"):
        results += search_pmt(subject, level, topic, limit)
        results += search_savemyexams(subject, level, topic, limit)

    if "math" in subject and level in ("alevel", "a-level", "gcse"):
        results += search_mathsgenie(subject, level, topic, limit)

    if level in ("sat", "ap", "k-12", "k12"):
        results += search_khanacademy(subject, topic, limit)

    if not results:
        results += search_khanacademy(subject, topic, limit)
        results += search_google_fallback(subject, level, topic, board, limit)

    # Deduplicate by URL
    seen = set()
    unique = []
    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    return unique[:limit]


# ─────────────────────────────────────────────
# Output
# ─────────────────────────────────────────────

def print_results(results: list[dict], fmt: str = "table"):
    if not results:
        print("No results found. Try broadening your search or using --site google.")
        return

    if fmt == "json":
        print(json.dumps(results, indent=2))
        return

    # Table format
    print(f"\n{'#':<4} {'Title':<55} {'Source':<30} {'URL'}")
    print("-" * 140)
    for i, r in enumerate(results, 1):
        title = r["title"][:53] + ".." if len(r["title"]) > 55 else r["title"]
        source = r["source"][:28] + ".." if len(r["source"]) > 30 else r["source"]
        print(f"{i:<4} {title:<55} {source:<30} {r['url']}")
        if r.get("note"):
            print(f"     ℹ  {r['note']}")
    print()


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Find exam questions and past papers from educational websites."
    )
    parser.add_argument("--subject", required=True,
                        help="Subject: math, physics, chemistry, biology, economics, english, cs")
    parser.add_argument("--level", default="alevel",
                        help="Level: alevel, gcse, igcse, ib, sat, ap (default: alevel)")
    parser.add_argument("--board", default="any",
                        help="Exam board: caie, aqa, ocr, edexcel, ib, collegeboard, any")
    parser.add_argument("--topic", default=None,
                        help="Topic (optional): e.g. 'algebra', 'organic chemistry', 'integration'")
    parser.add_argument("--year", default=None,
                        help="Year (optional): e.g. 2023")
    parser.add_argument("--site", default=None,
                        help="Force a specific site: pmt, savemyexams, easypaper, mathsgenie, khanacademy, google")
    parser.add_argument("--limit", type=int, default=8,
                        help="Max results to return (default: 8)")
    parser.add_argument("--format", dest="fmt", default="table", choices=["table", "json"],
                        help="Output format (default: table)")

    args = parser.parse_args()

    print(f"\n🔍 Searching for: {args.level.upper()} {args.subject.title()}"
          + (f" — {args.topic}" if args.topic else "")
          + (f" [{args.board.upper()}]" if args.board != "any" else "")
          + (f" ({args.year})" if args.year else ""))

    results = route_and_search(args)
    print_results(results, fmt=args.fmt)


if __name__ == "__main__":
    main()
