#!/usr/bin/env python3
"""
站点经验管理系统 - 移植 web-access 的站点经验积累功能

功能:
- 按域名存储和复用操作经验
- 记录平台特征、有效模式、已知陷阱
- CLI 工具用于查询和管理经验

使用方式:
    python3 site_experience.py query xiaohongshu.com
    python3 site_experience.py add xiaohongshu.com --feature "需要登录"
    python3 site_experience.py list
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import urllib.parse


class SiteExperienceManager:
    """站点经验管理器"""
    
    TEMPLATE = """---
domain: {domain}
aliases: [{aliases}]
updated: {date}
---

## 平台特征
{features}

## 有效模式
{patterns}

## 已知陷阱
{traps}
"""

    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            # 查找正确的路径
            script_dir = Path(__file__).parent
            skill_dir = script_dir.parent
            base_path = skill_dir / "references" / "site-patterns"
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def _normalize_domain(self, domain: str) -> str:
        """标准化域名"""
        domain = domain.lower().strip()
        # 移除协议
        if '://' in domain:
            domain = urllib.parse.urlparse(domain).netloc
        # 移除路径
        domain = domain.split('/')[0]
        # 移除 www.
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    
    def _get_file_path(self, domain: str) -> Path:
        """获取经验文件路径"""
        normalized = self._normalize_domain(domain)
        return self.base_path / f"{normalized}.md"
    
    def load(self, domain: str) -> Optional[dict]:
        """加载站点经验"""
        file_path = self._get_file_path(domain)
        
        if not file_path.exists():
            # 尝试查找相似域名
            all_files = list(self.base_path.glob("*.md"))
            normalized = self._normalize_domain(domain)
            
            for f in all_files:
                name = f.stem
                if normalized in name or name in normalized:
                    file_path = f
                    break
            else:
                return None
        
        content = file_path.read_text(encoding='utf-8')
        return self._parse(content)
    
    def _parse(self, content: str) -> dict:
        """解析经验文件内容"""
        result = {
            'domain': '',
            'aliases': [],
            'updated': '',
            'features': [],
            'patterns': {},
            'traps': []
        }
        
        # 解析 frontmatter
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            fm_content = frontmatter_match.group(1)
            
            # domain
            domain_match = re.search(r'^domain:\s*(.+)$', fm_content, re.M)
            if domain_match:
                result['domain'] = domain_match.group(1).strip()
            
            # aliases
            aliases_match = re.search(r'^aliases:\s*\[(.*?)\]', fm_content, re.M)
            if aliases_match:
                aliases_str = aliases_match.group(1)
                result['aliases'] = [a.strip().strip('"\'') for a in aliases_str.split(',') if a.strip()]
            
            # updated
            updated_match = re.search(r'^updated:\s*(.+)$', fm_content, re.M)
            if updated_match:
                result['updated'] = updated_match.group(1).strip()
        
        # 解析平台特征
        features_section = re.search(r'## 平台特征\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if features_section:
            for line in features_section.group(1).strip().split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    result['features'].append(line[1:].strip())
        
        # 解析有效模式
        patterns_section = re.search(r'## 有效模式\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if patterns_section:
            for line in patterns_section.group(1).strip().split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    # 格式: "名称: 值"
                    if ': ' in line[1:]:
                        parts = line[1:].strip().split(': ', 1)
                        result['patterns'][parts[0]] = parts[1]
                    else:
                        result['patterns'][line[1:].strip()] = ''
        
        # 解析已知陷阱
        traps_section = re.search(r'## 已知陷阱\s*\n(.*?)(?=##|$)', content, re.DOTALL)
        if traps_section:
            for line in traps_section.group(1).strip().split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    result['traps'].append(line[1:].strip())
        
        return result
    
    def save(self, domain: str, data: dict) -> bool:
        """保存站点经验"""
        try:
            file_path = self._get_file_path(domain)
            
            # 保留原有数据
            existing = self.load(domain) or {}
            
            # 合并数据
            merged = {
                'domain': data.get('domain', existing.get('domain', self._normalize_domain(domain))),
                'aliases': data.get('aliases', existing.get('aliases', [])),
                'updated': datetime.now().strftime('%Y-%m-%d'),
                'features': data.get('features', existing.get('features', [])),
                'patterns': {**existing.get('patterns', {}), **data.get('patterns', {})},
                'traps': list(set(data.get('traps', []) + existing.get('traps', [])))
            }
            
            # 生成内容
            content = self.TEMPLATE.format(
                domain=merged['domain'],
                aliases=', '.join(f'"{a}"' for a in merged['aliases']),
                date=merged['updated'],
                features='\n'.join(f'- {f}' for f in merged['features']) if merged['features'] else '- (待补充)',
                patterns='\n'.join(f'- {k}: {v}' for k, v in merged['patterns'].items()) if merged['patterns'] else '- (待补充)',
                traps='\n'.join(f'- {t}' for t in merged['traps']) if merged['traps'] else '- (待补充)'
            )
            
            file_path.write_text(content, encoding='utf-8')
            return True
            
        except Exception as e:
            print(f"Error saving experience: {e}", file=sys.stderr)
            return False
    
    def add_feature(self, domain: str, feature: str) -> bool:
        """添加平台特征"""
        existing = self.load(domain) or {}
        features = existing.get('features', [])
        if feature not in features:
            features.append(feature)
        return self.save(domain, {'features': features})
    
    def add_pattern(self, domain: str, name: str, value: str) -> bool:
        """添加有效模式"""
        existing = self.load(domain) or {}
        patterns = existing.get('patterns', {})
        patterns[name] = value
        return self.save(domain, {'patterns': patterns})
    
    def add_trap(self, domain: str, trap: str) -> bool:
        """添加已知陷阱"""
        existing = self.load(domain) or {}
        traps = existing.get('traps', [])
        if trap not in traps:
            traps.append(trap)
        return self.save(domain, {'traps': traps})
    
    def list_all(self) -> list:
        """列出所有站点经验"""
        files = sorted(self.base_path.glob("*.md"))
        results = []
        for f in files:
            data = self._parse(f.read_text(encoding='utf-8'))
            results.append({
                'domain': data.get('domain', f.stem),
                'updated': data.get('updated', 'unknown'),
                'features_count': len(data.get('features', [])),
                'patterns_count': len(data.get('patterns', {})),
                'traps_count': len(data.get('traps', []))
            })
        return results
    
    def needs_browser(self, domain: str) -> bool:
        """判断站点是否需要浏览器"""
        exp = self.load(domain)
        if not exp:
            return False
        
        features_text = ' '.join(exp.get('features', [])).lower()
        anti_patterns = ['反爬', '动态', '单页', 'spa', '需要登录', 
                        'javascript', 'ajax', 'react', 'vue', 'angular']
        
        return any(p in features_text for p in anti_patterns)
    
    def get_patterns(self, domain: str) -> dict:
        """获取站点的有效模式"""
        exp = self.load(domain)
        return exp.get('patterns', {}) if exp else {}


def print_experience(data: dict):
    """打印经验内容"""
    if not data:
        print("No experience found for this domain.")
        return
    
    print(f"\n📍 Domain: {data.get('domain', 'N/A')}")
    print(f"📝 Aliases: {', '.join(data.get('aliases', []))}")
    print(f"📅 Updated: {data.get('updated', 'N/A')}")
    
    print("\n🔧 Platform Features:")
    for f in data.get('features', []):
        print(f"  • {f}")
    
    print("\n✅ Valid Patterns:")
    for k, v in data.get('patterns', {}).items():
        print(f"  • {k}: {v}")
    
    print("\n⚠️ Known Traps:")
    for t in data.get('traps', []):
        print(f"  • {t}")


def main():
    parser = argparse.ArgumentParser(
        description='站点经验管理系统'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # query 命令
    query_parser = subparsers.add_parser('query', help='查询站点经验')
    query_parser.add_argument('domain', help='域名或URL')
    
    # list 命令
    subparsers.add_parser('list', help='列出所有站点经验')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加/更新站点经验')
    add_parser.add_argument('domain', help='域名')
    add_parser.add_argument('--feature', action='append', help='添加平台特征')
    add_parser.add_argument('--pattern', action='append', nargs=2, metavar=('NAME', 'VALUE'), 
                           help='添加有效模式')
    add_parser.add_argument('--trap', action='append', help='添加已知陷阱')
    add_parser.add_argument('--alias', action='append', help='添加别名')
    
    # check 命令
    check_parser = subparsers.add_parser('check', help='检查站点是否需要浏览器')
    check_parser.add_argument('domain', help='域名或URL')
    
    # init 命令 - 创建模板
    init_parser = subparsers.add_parser('init', help='创建站点经验模板')
    init_parser.add_argument('domain', help='域名')
    init_parser.add_argument('--alias', action='append', help='别名')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = SiteExperienceManager()
    
    if args.command == 'query':
        data = manager.load(args.domain)
        print_experience(data)
    
    elif args.command == 'list':
        all_exp = manager.list_all()
        if not all_exp:
            print("No site experiences found.")
        else:
            print(f"{'Domain':<30} {'Updated':<12} {'Features':<10} {'Patterns':<10} {'Traps':<10}")
            print("-" * 80)
            for exp in all_exp:
                print(f"{exp['domain']:<30} {exp['updated']:<12} "
                      f"{exp['features_count']:<10} {exp['patterns_count']:<10} {exp['traps_count']:<10}")
    
    elif args.command == 'add':
        data = {'domain': manager._normalize_domain(args.domain)}
        
        if args.alias:
            data['aliases'] = args.alias
        if args.feature:
            data['features'] = args.feature
        if args.pattern:
            data['patterns'] = {name: value for name, value in args.pattern}
        if args.trap:
            data['traps'] = args.trap
        
        if manager.save(args.domain, data):
            print(f"✓ Experience saved for {args.domain}")
        else:
            print(f"✗ Failed to save experience")
            sys.exit(1)
    
    elif args.command == 'check':
        needs_browser = manager.needs_browser(args.domain)
        print(f"Domain: {args.domain}")
        print(f"Needs browser: {'Yes' if needs_browser else 'No / Unknown'}")
        
        if needs_browser:
            patterns = manager.get_patterns(args.domain)
            if patterns:
                print("\nKnown patterns:")
                for k, v in patterns.items():
                    print(f"  • {k}: {v}")
    
    elif args.command == 'init':
        domain = manager._normalize_domain(args.domain)
        aliases = args.alias or []
        
        # 常见平台自动添加别名
        alias_map = {
            'xiaohongshu.com': ['小红书', '小红书笔记'],
            'zhihu.com': ['知乎'],
            'weibo.com': ['微博'],
            'bilibili.com': ['B站', '哔哩哔哩'],
        }
        
        for d, als in alias_map.items():
            if d in domain or domain in d:
                aliases.extend(als)
        
        data = {
            'domain': domain,
            'aliases': list(set(aliases)),
            'features': ['(待观察和补充)'],
            'patterns': {},
            'traps': []
        }
        
        if manager.save(args.domain, data):
            print(f"✓ Template created for {domain}")
            file_path = manager._get_file_path(domain)
            print(f"  Edit: {file_path}")
        else:
            print(f"✗ Failed to create template")
            sys.exit(1)


if __name__ == '__main__':
    main()
