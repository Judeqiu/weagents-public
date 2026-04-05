#!/usr/bin/env python3
"""
智能调度获取脚本 - Legacy script for backwards compatibility

⚠️  DEPRECATION NOTICE  ⚠️
This script is maintained for backwards compatibility with existing automation.
For new Claude-based interactions, use the natural language skill instead.

See: skills/agent-browser/SKILL.md for the recommended natural language approach.

优先级顺序 (PRIORITY_ORDER):
1. mychrome (Chrome CDP)     - CDP-based Chrome as FIRST priority
2. agent-browser (bundled)   - SECOND priority
3. Browserless API           - THIRD priority
4. curl                      - FOURTH priority
5. Jina AI                   - FIFTH priority (optional)

使用方式 (Legacy):
    python3 smart_fetch.py --url https://example.com
    python3 smart_fetch.py --url https://example.com --task "提取价格"
    python3 smart_fetch.py --url https://example.com --use-jina

推荐方式 (Natural Language):
    Ask Claude: "Get the content from https://example.com"
    Claude will interpret SKILL.md and choose the best method automatically.
"""

import argparse
import asyncio
import json
import os
import re
import subprocess
import sys
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List


# ============================================================================
# SINGLE SOURCE OF TRUTH - FETCH METHOD PRIORITY ORDER
# ============================================================================
# This is the ONLY place where fetch method priority is defined.
# Modify this list to change the global priority order.
# 
# Current Priority: CDP Chrome > Bundled Chromium > Cloud > HTTP > Article
# ============================================================================
PRIORITY_ORDER: List[str] = [
    "mychrome",        # 1. Chrome CDP (persistent sessions, real Chrome)
    "agent-browser",   # 2. Bundled Chromium (fast, no external deps)
    "browserless",     # 3. Cloud browser (always works)
    "curl",            # 4. Simple HTTP (fastest for static)
    "jina",            # 5. Article preprocessing (saves tokens)
]


def get_method_priority(method: str) -> int:
    """Get priority rank of a method (lower = higher priority)"""
    try:
        return PRIORITY_ORDER.index(method)
    except ValueError:
        return 999  # Unknown methods get lowest priority


@dataclass
class FetchResult:
    """获取结果"""
    success: bool
    content: str
    method: str
    error: Optional[str] = None
    metadata: dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class SiteExperience:
    """站点经验管理 - 移植 web-access 的站点经验系统"""
    
    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            base_path = Path(__file__).parent.parent / "references" / "site-patterns"
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def get_domain(self, url: str) -> str:
        """从 URL 提取域名"""
        parsed = urllib.parse.urlparse(url)
        return parsed.netloc.lower().replace('www.', '')
    
    def load_experience(self, domain: str) -> Optional[dict]:
        """加载站点经验文件"""
        # 尝试多种域名变体
        variants = [
            domain,
            domain.replace('www.', ''),
            'www.' + domain if not domain.startswith('www.') else domain[4:]
        ]
        
        for variant in set(variants):
            exp_file = self.base_path / f"{variant}.md"
            if exp_file.exists():
                return self._parse_experience(exp_file.read_text())
        
        return None
    
    def _parse_experience(self, content: str) -> dict:
        """解析经验文件"""
        experience = {
            'features': [],
            'patterns': {},
            'traps': []
        }
        
        # 提取平台特征
        if '## 平台特征' in content:
            features_section = content.split('## 平台特征')[1].split('##')[0]
            for line in features_section.split('\n'):
                if line.strip().startswith('-'):
                    experience['features'].append(line.strip()[1:].strip())
        
        # 提取有效模式
        if '## 有效模式' in content:
            patterns_section = content.split('## 有效模式')[1].split('##')[0]
            for line in patterns_section.split('\n'):
                if line.strip().startswith('-'):
                    parts = line.strip()[1:].strip().split(': ', 1)
                    if len(parts) == 2:
                        experience['patterns'][parts[0]] = parts[1]
        
        # 提取已知陷阱
        if '## 已知陷阱' in content:
            traps_section = content.split('## 已知陷阱')[1].split('##')[0]
            for line in traps_section.split('\n'):
                if line.strip().startswith('-'):
                    experience['traps'].append(line.strip()[1:].strip())
        
        return experience
    
    def needs_browser(self, domain: str) -> bool:
        """判断站点是否需要浏览器"""
        exp = self.load_experience(domain)
        if exp:
            features = ' '.join(exp.get('features', [])).lower()
            return any(kw in features for kw in [
                '反爬', '动态', '单页', 'spa', '需要登录', 
                'javascript', 'ajax', 'react', 'vue'
            ])
        
        # 常见反爬平台列表
        anti_scraping_sites = [
            'xiaohongshu.com', 'xhslink.com',  # 小红书
            'weixin.qq.com', 'mp.weixin.qq.com',  # 微信
            'zhihu.com',  # 知乎
            'weibo.com',  # 微博
            'douyin.com',  # 抖音
            'bilibili.com',  # B站
            'taobao.com', 'tmall.com',  # 淘宝天猫
            'jd.com',  # 京东
            'linkedin.com',
            'instagram.com',
            'twitter.com', 'x.com',
        ]
        
        return any(site in domain for site in anti_scraping_sites)


class SmartFetcher:
    """智能调度器 - Single source of truth for fetch priority"""
    
    def __init__(self):
        self.site_exp = SiteExperience()
    
    def is_article_url(self, url: str) -> bool:
        """判断是否为文章/博客类 URL (适合 Jina)"""
        article_patterns = [
            r'/blog/', r'/article/', r'/post/', r'/news/',
            r'/docs/', r'/guide/', r'/tutorial/',
            r'/(?:\d{4}/\d{2}/\d{2}|[0-9a-f]{8,})/',  # 日期路径或哈希ID
        ]
        return any(re.search(p, url, re.I) for p in article_patterns)
    
    def is_static_page(self, url: str) -> bool:
        """判断是否为简单静态页面"""
        static_extensions = ['.html', '.htm', '.txt', '.md', '.json', '.xml']
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.lower()
        
        # 有静态扩展名
        if any(path.endswith(ext) for ext in static_extensions):
            return True
        
        # 简单路径 (无复杂查询参数)
        if not parsed.query or len(parsed.query) < 50:
            return True
        
        return False
    
    def _check_mychrome_available(self) -> bool:
        """检查 mychrome (Chrome CDP) 是否可用"""
        chrome_url = os.environ.get('CHROME_CDP_URL', 'http://localhost:9222')
        skill_path = Path.home() / ".openclaw" / "workspace" / "skills" / "mychrome"
        
        # Check skill exists
        if not skill_path.exists():
            return False
        
        # Check Chrome CDP is accessible
        try:
            import urllib.request
            req = urllib.request.Request(f"{chrome_url}/json/version", method='GET')
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200
        except:
            return False
    
    def _check_agent_browser_available(self) -> bool:
        """检查 agent-browser 是否已安装"""
        return subprocess.run(
            ['which', 'agent-browser'], 
            capture_output=True
        ).returncode == 0
    
    async def fetch_with_mychrome(self, url: str, task: str = "") -> FetchResult:
        """使用 mychrome (Chrome CDP) 获取 - FIRST PRIORITY"""
        try:
            chrome_url = os.environ.get('CHROME_CDP_URL', 'http://localhost:9222')
            skill_path = Path.home() / ".openclaw" / "workspace" / "skills" / "mychrome"
            
            # Use chrome_cdp_helper.py for CDP-based fetching
            helper_script = skill_path / "scripts" / "chrome_cdp_helper.py"
            
            if not helper_script.exists():
                return FetchResult(
                    success=False,
                    content='',
                    method='mychrome',
                    error='mychrome helper script not found'
                )
            
            proc = await asyncio.create_subprocess_exec(
                'python3', str(helper_script),
                '--cdp-url', chrome_url,
                '--url', url,
                '--extract-content',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
            
            if proc.returncode == 0 and stdout:
                content = stdout.decode('utf-8', errors='ignore')
                # Try to parse as JSON (chrome_cdp_helper returns JSON)
                try:
                    data = json.loads(content)
                    if data.get('success'):
                        return FetchResult(
                            success=True,
                            content=data.get('content', content),
                            method='mychrome',
                            metadata={'cdp_url': chrome_url, 'title': data.get('title')}
                        )
                except json.JSONDecodeError:
                    # Not JSON, use raw content
                    pass
                
                if len(content) > 100:
                    return FetchResult(
                        success=True,
                        content=content,
                        method='mychrome',
                        metadata={'cdp_url': chrome_url}
                    )
            
            error_msg = stderr.decode() if stderr else 'mychrome failed'
            return FetchResult(
                success=False,
                content='',
                method='mychrome',
                error=error_msg
            )
            
        except asyncio.TimeoutError:
            return FetchResult(
                success=False,
                content='',
                method='mychrome',
                error='Timeout'
            )
        except Exception as e:
            return FetchResult(
                success=False,
                content='',
                method='mychrome',
                error=str(e)
            )
    
    async def fetch_with_agent_browser(self, url: str, task: str = "") -> FetchResult:
        """使用 agent-browser (bundled Chromium) 获取 - SECOND PRIORITY"""
        try:
            proc = await asyncio.create_subprocess_exec(
                'agent-browser', 'open', url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for open to complete
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=30)
            
            if proc.returncode != 0:
                return FetchResult(
                    success=False,
                    content='',
                    method='agent-browser',
                    error=stderr.decode() if stderr else 'agent-browser open failed'
                )
            
            # Get content
            proc2 = await asyncio.create_subprocess_exec(
                'agent-browser', 'content',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout2, stderr2 = await asyncio.wait_for(proc2.communicate(), timeout=30)
            
            # Close browser
            await asyncio.create_subprocess_exec('agent-browser', 'close')
            
            if proc2.returncode == 0 and stdout2:
                content = stdout2.decode('utf-8', errors='ignore')
                return FetchResult(
                    success=True,
                    content=content,
                    method='agent-browser',
                    metadata={'task': task}
                )
            
            return FetchResult(
                success=False,
                content='',
                method='agent-browser',
                error=stderr2.decode() if stderr2 else 'agent-browser content failed'
            )
            
        except asyncio.TimeoutError:
            return FetchResult(
                success=False,
                content='',
                method='agent-browser',
                error='Timeout'
            )
        except Exception as e:
            return FetchResult(
                success=False,
                content='',
                method='agent-browser',
                error=str(e)
            )
    
    async def fetch_with_browserless(self, url: str, task: str = "") -> FetchResult:
        """使用 Browserless API 获取 - THIRD PRIORITY"""
        try:
            skill_path = Path(__file__).parent.parent
            helper = skill_path / "scripts" / "browserless_helper.sh"
            
            if not helper.exists():
                return FetchResult(
                    success=False,
                    content='',
                    method='browserless',
                    error='Browserless helper not found'
                )
            
            proc = await asyncio.create_subprocess_exec(
                'bash', str(helper), 'content', '--url', url, '--output', '/dev/stdout',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
            
            if proc.returncode == 0 and stdout:
                content = stdout.decode('utf-8', errors='ignore')
                return FetchResult(
                    success=True,
                    content=content,
                    method='browserless',
                    metadata={'task': task}
                )
            
            return FetchResult(
                success=False,
                content='',
                method='browserless',
                error=stderr.decode() if stderr else 'Browserless failed'
            )
            
        except asyncio.TimeoutError:
            return FetchResult(
                success=False,
                content='',
                method='browserless',
                error='Timeout'
            )
        except Exception as e:
            return FetchResult(
                success=False,
                content='',
                method='browserless',
                error=str(e)
            )
    
    async def fetch_with_curl(self, url: str) -> FetchResult:
        """使用 curl 获取 - FOURTH PRIORITY"""
        try:
            proc = await asyncio.create_subprocess_exec(
                'curl', '-sL', '-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                '--max-time', '30',
                '--retry', '2',
                url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=35)
            
            if proc.returncode == 0 and stdout:
                content = stdout.decode('utf-8', errors='ignore')
                
                # 检查是否为有效 HTML
                if '<html' in content.lower() or '<!doctype' in content.lower():
                    return FetchResult(
                        success=True,
                        content=content,
                        method='curl',
                        metadata={'size': len(content)}
                    )
            
            return FetchResult(
                success=False,
                content='',
                method='curl',
                error=stderr.decode() if stderr else 'curl failed'
            )
            
        except asyncio.TimeoutError:
            return FetchResult(
                success=False,
                content='',
                method='curl',
                error='Timeout'
            )
        except Exception as e:
            return FetchResult(
                success=False,
                content='',
                method='curl',
                error=str(e)
            )
    
    async def fetch_with_jina(self, url: str) -> FetchResult:
        """使用 Jina AI 获取 (节省 token) - FIFTH PRIORITY"""
        try:
            jina_url = f"https://r.jina.ai/{url}"
            
            proc = await asyncio.create_subprocess_exec(
                'curl', '-sL', '-A', 'Mozilla/5.0', 
                '--max-time', '30',
                jina_url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=35)
            
            if proc.returncode == 0 and stdout:
                content = stdout.decode('utf-8', errors='ignore')
                # Jina 返回空或错误信息
                if content and len(content) > 100 and 'Error:' not in content[:100]:
                    return FetchResult(
                        success=True,
                        content=content,
                        method='jina',
                        metadata={'jina_url': jina_url}
                    )
            
            return FetchResult(
                success=False,
                content='',
                method='jina',
                error=stderr.decode() if stderr else 'Jina returned empty or error'
            )
            
        except asyncio.TimeoutError:
            return FetchResult(
                success=False,
                content='',
                method='jina',
                error='Timeout'
            )
        except Exception as e:
            return FetchResult(
                success=False,
                content='',
                method='jina',
                error=str(e)
            )
    
    async def smart_fetch(
        self, 
        url: str, 
        task: str = "",
        prefer_jina: bool = False,
        force_browser: bool = False,
        force_method: Optional[str] = None
    ) -> FetchResult:
        """
        智能获取 - 根据 PRIORITY_ORDER 顺序尝试所有方法
        
        这是唯一的优先级决策点。要修改全局优先级，请修改文件顶部的 PRIORITY_ORDER 常量。
        
        Args:
            url: 目标 URL
            task: 任务描述
            prefer_jina: 是否优先尝试 Jina (会调整优先级，将 jina 提前到 curl 之前)
            force_browser: 强制使用浏览器 (mychrome -> agent-browser -> browserless)
            force_method: 强制使用特定方法
        """
        domain = self.site_exp.get_domain(url)
        
        print(f"[SmartFetch] Target: {url}", file=sys.stderr)
        print(f"[SmartFetch] Domain: {domain}", file=sys.stderr)
        
        # 如果强制指定方法，只尝试该方法
        if force_method:
            print(f"[SmartFetch] Force method: {force_method}", file=sys.stderr)
            method_map = {
                'mychrome': self.fetch_with_mychrome,
                'agent-browser': self.fetch_with_agent_browser,
                'browserless': self.fetch_with_browserless,
                'curl': self.fetch_with_curl,
                'jina': self.fetch_with_jina,
            }
            if force_method in method_map:
                return await method_map[force_method](url, task)
            else:
                return FetchResult(
                    success=False,
                    content='',
                    method='unknown',
                    error=f'Unknown method: {force_method}'
                )
        
        # 确定本次请求的优先级顺序
        current_priority = PRIORITY_ORDER.copy()
        
        # 策略调整：如果 prefer_jina 且是文章，将 jina 提前
        if prefer_jina and self.is_article_url(url):
            print(f"[SmartFetch] Article detected, prioritizing Jina", file=sys.stderr)
            current_priority.remove('jina')
            # 插入到 curl 之前
            curl_idx = current_priority.index('curl')
            current_priority.insert(curl_idx, 'jina')
        
        # 策略调整：如果站点已知需要浏览器，将浏览器方法提前
        if self.site_exp.needs_browser(domain):
            print(f"[SmartFetch] Site {domain} requires browser (from experience)", file=sys.stderr)
            # 将浏览器方法移到最前面（保持它们之间的相对顺序）
            browser_methods = ['mychrome', 'agent-browser', 'browserless']
            other_methods = [m for m in current_priority if m not in browser_methods]
            current_priority = browser_methods + other_methods
        
        # 策略调整：如果 force_browser，只尝试浏览器类方法
        if force_browser:
            print(f"[SmartFetch] Force browser mode", file=sys.stderr)
            current_priority = ['mychrome', 'agent-browser', 'browserless']
        
        print(f"[SmartFetch] Priority order: {current_priority}", file=sys.stderr)
        
        # 按优先级顺序尝试所有方法
        for method in current_priority:
            print(f"[SmartFetch] Trying {method}...", file=sys.stderr)
            
            if method == 'mychrome':
                result = await self.fetch_with_mychrome(url, task)
            elif method == 'agent-browser':
                result = await self.fetch_with_agent_browser(url, task)
            elif method == 'browserless':
                result = await self.fetch_with_browserless(url, task)
            elif method == 'curl':
                result = await self.fetch_with_curl(url)
            elif method == 'jina':
                result = await self.fetch_with_jina(url)
            else:
                continue
            
            if result.success:
                print(f"[SmartFetch] ✓ Success with {method}", file=sys.stderr)
                return result
            else:
                print(f"[SmartFetch] ✗ {method} failed: {result.error[:100] if result.error else 'unknown'}", file=sys.stderr)
        
        # 全部失败
        return FetchResult(
            success=False,
            content='',
            method='all',
            error=f'All fetch methods failed. Tried: {current_priority}'
        )


def main():
    parser = argparse.ArgumentParser(
        description='智能获取网页内容 - Single source of truth for fetch priority'
    )
    parser.add_argument('--url', help='目标 URL')
    parser.add_argument('--task', default='', help='任务描述 (用于浏览器模式)')
    parser.add_argument('--use-jina', action='store_true', help='优先使用 Jina (文章模式)')
    parser.add_argument('--force-browser', action='store_true', help='强制使用浏览器方法')
    parser.add_argument('--force-method', choices=['mychrome', 'agent-browser', 'browserless', 'curl', 'jina'],
                       help='强制使用特定方法')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--show-priority', action='store_true', help='显示当前优先级顺序并退出')
    
    args = parser.parse_args()
    
    # 显示优先级
    if args.show_priority:
        print("Current fetch method priority order (highest to lowest):")
        for i, method in enumerate(PRIORITY_ORDER, 1):
            marker = ""
            if method == "mychrome":
                marker = "  <-- CDP-based Chrome (FIRST)"
            elif method == "agent-browser":
                marker = "  <-- Bundled Chromium (SECOND)"
            print(f"  {i}. {method}{marker}")
        print("\nTo change priority, modify PRIORITY_ORDER in this script.")
        sys.exit(0)
    
    # Validate URL is required for normal operation
    if not args.url:
        parser.error('--url is required (unless using --show-priority)')
    
    fetcher = SmartFetcher()
    result = asyncio.run(fetcher.smart_fetch(
        url=args.url,
        task=args.task,
        prefer_jina=args.use_jina,
        force_browser=args.force_browser,
        force_method=args.force_method
    ))
    
    # 输出结果
    if args.json:
        output = json.dumps({
            'success': result.success,
            'method': result.method,
            'content': result.content,
            'error': result.error,
            'metadata': result.metadata
        }, ensure_ascii=False, indent=2)
    else:
        if result.success:
            output = result.content
        else:
            output = f"Error ({result.method}): {result.error}"
    
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(output)
    
    sys.exit(0 if result.success else 1)


if __name__ == '__main__':
    main()
