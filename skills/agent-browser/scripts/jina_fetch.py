#!/usr/bin/env python3
"""
Jina AI 预处理获取 - 节省 Token 的轻量级获取方式

使用 Jina AI 服务 (r.jina.ai) 将网页转换为 Markdown，
大幅节省 token 消耗，适合文章、博客、文档类页面。

限制:
- 20 RPM (每分钟请求限制)
- 不适合: 数据面板、商品页等非文章结构页面

使用方式:
    python3 jina_fetch.py https://example.com/article
    python3 jina_fetch.py https://example.com/article --output article.md
    python3 jina_fetch.py https://example.com/article --json
"""

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error
import urllib.parse


@dataclass
class JinaResult:
    """Jina 获取结果"""
    success: bool
    content: str
    title: str = ""
    url: str = ""
    error: Optional[str] = None
    metadata: dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class JinaFetcher:
    """Jina AI 获取器"""
    
    BASE_URL = "https://r.jina.ai"
    
    # 适合使用 Jina 的 URL 模式
    ARTICLE_PATTERNS = [
        '/blog/', '/article/', '/post/', '/news/',
        '/docs/', '/guide/', '/tutorial/', '/readme',
        '/wiki/', '/knowledge/',
    ]
    
    # 不适合使用 Jina 的 URL 模式
    UNSUITABLE_PATTERNS = [
        '/product/', '/item/', '/shop/', '/store/',
        '/cart/', '/checkout/',
        '/search?', '/filter?', '/sort?',
        '/dashboard/', '/admin/', '/panel/',
        '/api/', '/graphql',
    ]
    
    def __init__(self, delay: float = 3.0):
        """
        Args:
            delay: 请求间隔延迟 (秒)，遵守 20 RPM 限制
        """
        self.delay = delay
        self.last_request_time = 0
    
    def is_suitable(self, url: str) -> bool:
        """
        判断是否适合使用 Jina
        
        适合: 文章、博客、文档、新闻
        不适合: 商品页、搜索页、数据面板
        """
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.lower()
        
        # 检查不适合的模式
        for pattern in self.UNSUITABLE_PATTERNS:
            if pattern in path:
                return False
        
        # 检查适合的模式
        for pattern in self.ARTICLE_PATTERNS:
            if pattern in path:
                return True
        
        # 启发式判断：路径深度和内容特征
        path_parts = [p for p in path.split('/') if p]
        
        # 日期路径模式 (如 /2024/03/15/slug)
        if len(path_parts) >= 3:
            if all(p.isdigit() for p in path_parts[:3] if len(p) <= 4):
                return True
        
        # 长的 slug 通常是文章
        if path_parts and len(path_parts[-1]) > 20:
            return True
        
        # 默认保守策略：假设可能适合
        return True
    
    def _rate_limit(self):
        """速率限制 - 遵守 20 RPM"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def fetch(self, url: str, extract_title: bool = True) -> JinaResult:
        """
        使用 Jina AI 获取内容
        
        Args:
            url: 目标 URL
            extract_title: 是否提取标题
        
        Returns:
            JinaResult 对象
        """
        # 速率限制
        self._rate_limit()
        
        # 构建 Jina URL
        # 格式: https://r.jina.ai/http://example.com 或 https://r.jina.ai/example.com
        if url.startswith(('http://', 'https://')):
            jina_url = f"{self.BASE_URL}/{url}"
        else:
            jina_url = f"{self.BASE_URL}/https://{url}"
        
        try:
            req = urllib.request.Request(
                jina_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (compatible; SmartFetch/1.0)',
                    'Accept': 'text/plain, text/markdown, */*',
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                content = response.read().decode('utf-8', errors='ignore')
                
                # 检查 Jina 返回的错误
                if content.startswith('Error:'):
                    return JinaResult(
                        success=False,
                        content='',
                        url=url,
                        error=content
                    )
                
                # 提取标题 (第一行通常是标题)
                title = ""
                if extract_title and content:
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('---'):
                            title = line.lstrip('#').strip()
                            break
                
                return JinaResult(
                    success=True,
                    content=content,
                    title=title,
                    url=url,
                    metadata={
                        'jina_url': jina_url,
                        'content_length': len(content),
                        'content_type': response.headers.get('Content-Type', 'unknown')
                    }
                )
                
        except urllib.error.HTTPError as e:
            return JinaResult(
                success=False,
                content='',
                url=url,
                error=f"HTTP {e.code}: {e.reason}"
            )
        except urllib.error.URLError as e:
            return JinaResult(
                success=False,
                content='',
                url=url,
                error=f"URL Error: {e.reason}"
            )
        except Exception as e:
            return JinaResult(
                success=False,
                content='',
                url=url,
                error=f"Exception: {str(e)}"
            )
    
    def fetch_batch(self, urls: list, progress_callback=None) -> list:
        """
        批量获取 (顺序执行，遵守速率限制)
        
        Args:
            urls: URL 列表
            progress_callback: 进度回调函数 (current, total, result)
        
        Returns:
            JinaResult 列表
        """
        results = []
        for i, url in enumerate(urls):
            result = self.fetch(url)
            results.append(result)
            
            if progress_callback:
                progress_callback(i + 1, len(urls), result)
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description='使用 Jina AI 获取网页内容 (节省 Token)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    %(prog)s https://example.com/article
    %(prog)s https://example.com/article --output article.md
    %(prog)s https://example.com/article --json
    %(prog)s https://example.com/article --check
        """
    )
    
    parser.add_argument('url', nargs='?', help='目标 URL')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    parser.add_argument('--check', action='store_true', 
                       help='检查 URL 是否适合使用 Jina')
    parser.add_argument('--delay', type=float, default=3.0,
                       help='请求间隔 (秒, 默认: 3.0, 对应 20 RPM)')
    
    args = parser.parse_args()
    
    if not args.url and not args.check:
        parser.print_help()
        sys.exit(1)
    
    fetcher = JinaFetcher(delay=args.delay)
    
    # 检查模式
    if args.check and args.url:
        suitable = fetcher.is_suitable(args.url)
        print(f"URL: {args.url}")
        print(f"Suitable for Jina: {'Yes' if suitable else 'No'}")
        
        if suitable:
            print("\nThis URL appears to be an article/blog post.")
            print("Jina will likely return clean markdown content.")
        else:
            print("\nThis URL may not be suitable for Jina.")
            print("Consider using agent-browser for better results.")
        
        sys.exit(0 if suitable else 1)
    
    # 获取模式
    print(f"[JinaFetch] Fetching: {args.url}", file=sys.stderr)
    
    if not fetcher.is_suitable(args.url):
        print("[JinaFetch] Warning: This URL may not be suitable for Jina.", file=sys.stderr)
        print("[JinaFetch] Consider using --check first or use smart_fetch.py", file=sys.stderr)
    
    result = fetcher.fetch(args.url)
    
    if result.success:
        print(f"[JinaFetch] ✓ Success (saved {result.metadata.get('content_length', 0)} chars)", file=sys.stderr)
        
        if args.json:
            output = json.dumps({
                'success': True,
                'url': result.url,
                'title': result.title,
                'content': result.content,
                'metadata': result.metadata
            }, ensure_ascii=False, indent=2)
        else:
            output = result.content
        
        if args.output:
            Path(args.output).write_text(output, encoding='utf-8')
            print(f"[JinaFetch] Saved to: {args.output}", file=sys.stderr)
        else:
            print(output)
        
        sys.exit(0)
    
    else:
        print(f"[JinaFetch] ✗ Failed: {result.error}", file=sys.stderr)
        
        if args.json:
            print(json.dumps({
                'success': False,
                'url': args.url,
                'error': result.error
            }, ensure_ascii=False, indent=2))
        
        sys.exit(1)


if __name__ == '__main__':
    main()
