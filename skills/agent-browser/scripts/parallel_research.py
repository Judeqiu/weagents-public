#!/usr/bin/env python3
"""
并行分治调研脚本 - 移植 web-access 的并行分治能力

将多个独立调研目标分发给子任务并行执行，总耗时约等于单个子任务时长。

使用方式:
    # 从 JSON 文件加载目标
    python3 parallel_research.py --targets-file targets.json --output results.json
    
    # 直接指定目标
    python3 parallel_research.py --targets '[
        {"name": "产品A", "url": "https://a.com", "task": "提取价格"},
        {"name": "产品B", "url": "https://b.com", "task": "提取规格"}
    ]'
    
    # 限制并发数
    python3 parallel_research.py --targets-file targets.json --concurrency 3
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional
import concurrent.futures


@dataclass
class ResearchTarget:
    """调研目标"""
    name: str
    url: str
    task: str = ""  # 具体任务描述
    method: str = "auto"  # auto, browser, curl, jina
    priority: int = 0  # 优先级，数字越小越优先


@dataclass
class ResearchResult:
    """调研结果"""
    target: ResearchTarget
    success: bool
    content: str = ""
    method_used: str = ""
    error: str = ""
    duration: float = 0.0
    metadata: dict = field(default_factory=dict)


class ParallelResearcher:
    """并行调研器 - 实现 web-access 的并行分治策略"""
    
    def __init__(self, concurrency: int = 5, timeout: int = 120):
        self.concurrency = concurrency
        self.timeout = timeout
        self.script_dir = Path(__file__).parent
    
    async def research_single(self, target: ResearchTarget, session_id: str = None) -> ResearchResult:
        """
        单个调研任务
        
        使用 smart_fetch.py 执行实际获取
        """
        start_time = time.time()
        
        try:
            # 构建命令
            cmd = [
                sys.executable,
                str(self.script_dir / "smart_fetch.py"),
                "--url", target.url,
                "--json"
            ]
            
            if target.task:
                cmd.extend(["--task", target.task])
            
            if target.method == "browser":
                cmd.append("--force-browser")
            elif target.method == "jina":
                cmd.append("--use-jina")
            
            # 设置环境变量传递 session ID (用于隔离)
            env = os.environ.copy()
            if session_id:
                env['AGENT_BROWSER_SESSION'] = session_id
            
            # 执行
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(), 
                timeout=self.timeout
            )
            
            duration = time.time() - start_time
            
            if proc.returncode == 0:
                try:
                    result_data = json.loads(stdout.decode('utf-8'))
                    return ResearchResult(
                        target=target,
                        success=result_data.get('success', False),
                        content=result_data.get('content', ''),
                        method_used=result_data.get('method', 'unknown'),
                        error=result_data.get('error', ''),
                        duration=duration,
                        metadata=result_data.get('metadata', {})
                    )
                except json.JSONDecodeError:
                    return ResearchResult(
                        target=target,
                        success=False,
                        error="Invalid JSON response",
                        duration=duration
                    )
            else:
                error_msg = stderr.decode('utf-8') if stderr else "Unknown error"
                return ResearchResult(
                    target=target,
                    success=False,
                    error=error_msg,
                    duration=duration
                )
                
        except asyncio.TimeoutError:
            return ResearchResult(
                target=target,
                success=False,
                error=f"Timeout after {self.timeout}s",
                duration=time.time() - start_time
            )
        except Exception as e:
            return ResearchResult(
                target=target,
                success=False,
                error=str(e),
                duration=time.time() - start_time
            )
    
    async def research_all(self, targets: List[ResearchTarget]) -> List[ResearchResult]:
        """
        并行执行所有调研任务
        
        使用信号量控制并发数，每个任务使用独立的 session
        """
        semaphore = asyncio.Semaphore(self.concurrency)
        
        async def run_with_semaphore(target: ResearchTarget, index: int) -> ResearchResult:
            async with semaphore:
                # 生成唯一的 session ID
                session_id = f"research_{index}_{int(time.time())}"
                print(f"[Parallel] Starting: {target.name}", file=sys.stderr)
                
                result = await self.research_single(target, session_id)
                
                status = "✓" if result.success else "✗"
                print(f"[Parallel] {status} {target.name} ({result.duration:.1f}s)", file=sys.stderr)
                
                return result
        
        # 按优先级排序
        sorted_targets = sorted(enumerate(targets), key=lambda x: x[1].priority)
        
        # 创建所有任务
        tasks = [
            run_with_semaphore(target, idx)
            for idx, target in sorted_targets
        ]
        
        # 并行执行
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理异常
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(ResearchResult(
                    target=targets[i],
                    success=False,
                    error=f"Exception: {str(result)}"
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    def research_sync(self, targets: List[ResearchTarget]) -> List[ResearchResult]:
        """同步接口"""
        return asyncio.run(self.research_all(targets))


class ReportGenerator:
    """报告生成器"""
    
    @staticmethod
    def generate_markdown(results: List[ResearchResult]) -> str:
        """生成 Markdown 格式报告"""
        lines = [
            "# 并行调研报告",
            "",
            f"**总目标数**: {len(results)}",
            f"**成功**: {sum(1 for r in results if r.success)}",
            f"**失败**: {sum(1 for r in results if not r.success)}",
            f"**总耗时**: {max(r.duration for r in results):.1f}s (并行)",
            "",
            "---",
            ""
        ]
        
        for result in results:
            status = "✅ 成功" if result.success else "❌ 失败"
            lines.extend([
                f"## {result.target.name}",
                "",
                f"- **状态**: {status}",
                f"- **URL**: {result.target.url}",
                f"- **方法**: {result.method_used}",
                f"- **耗时**: {result.duration:.1f}s",
            ])
            
            if result.target.task:
                lines.append(f"- **任务**: {result.target.task}")
            
            if not result.success and result.error:
                lines.extend([
                    "",
                    f"**错误**: {result.error}"
                ])
            
            if result.success and result.content:
                # 截断过长的内容
                content = result.content
                if len(content) > 5000:
                    content = content[:5000] + "\n\n...(内容已截断)"
                lines.extend([
                    "",
                    "### 内容",
                    "",
                    "```",
                    content,
                    "```"
                ])
            
            lines.extend(["", "---", ""])
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_json(results: List[ResearchResult]) -> dict:
        """生成 JSON 格式报告"""
        return {
            "summary": {
                "total": len(results),
                "success": sum(1 for r in results if r.success),
                "failed": sum(1 for r in results if not r.success),
                "max_duration": max(r.duration for r in results) if results else 0
            },
            "results": [
                {
                    "name": r.target.name,
                    "url": r.target.url,
                    "success": r.success,
                    "method": r.method_used,
                    "duration": r.duration,
                    "content": r.content if r.success else None,
                    "error": r.error if not r.success else None
                }
                for r in results
            ]
        }


def parse_targets(targets_data) -> List[ResearchTarget]:
    """解析目标数据"""
    if isinstance(targets_data, str):
        targets_data = json.loads(targets_data)
    
    targets = []
    for item in targets_data:
        targets.append(ResearchTarget(
            name=item.get('name', 'Unnamed'),
            url=item['url'],
            task=item.get('task', ''),
            method=item.get('method', 'auto'),
            priority=item.get('priority', 0)
        ))
    
    return targets


def main():
    parser = argparse.ArgumentParser(
        description='并行分治调研 - 同时调研多个目标'
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--targets', help='JSON 格式的目标列表')
    input_group.add_argument('--targets-file', help='包含目标的 JSON 文件路径')
    
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', choices=['json', 'markdown'], default='json',
                       help='输出格式')
    parser.add_argument('--concurrency', '-c', type=int, default=5,
                       help='最大并发数 (默认: 5)')
    parser.add_argument('--timeout', '-t', type=int, default=120,
                       help='单个任务超时时间 (秒, 默认: 120)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细输出')
    
    args = parser.parse_args()
    
    # 加载目标
    if args.targets_file:
        with open(args.targets_file, 'r') as f:
            targets_data = json.load(f)
    else:
        targets_data = args.targets
    
    targets = parse_targets(targets_data)
    
    if not targets:
        print("Error: No targets found", file=sys.stderr)
        sys.exit(1)
    
    print(f"[ParallelResearch] Loaded {len(targets)} targets", file=sys.stderr)
    print(f"[ParallelResearch] Concurrency: {args.concurrency}", file=sys.stderr)
    
    # 执行调研
    researcher = ParallelResearcher(
        concurrency=args.concurrency,
        timeout=args.timeout
    )
    
    start_time = time.time()
    results = researcher.research_sync(targets)
    total_time = time.time() - start_time
    
    print(f"\n[ParallelResearch] All tasks completed in {total_time:.1f}s", file=sys.stderr)
    
    # 生成报告
    if args.format == 'markdown':
        output = ReportGenerator.generate_markdown(results)
    else:
        output = json.dumps(
            ReportGenerator.generate_json(results),
            ensure_ascii=False,
            indent=2
        )
    
    # 输出
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"[ParallelResearch] Report saved to: {args.output}", file=sys.stderr)
    else:
        print(output)
    
    # 返回码
    success_count = sum(1 for r in results if r.success)
    if success_count == 0:
        sys.exit(2)  # 全部失败
    elif success_count < len(results):
        sys.exit(1)  # 部分失败
    else:
        sys.exit(0)  # 全部成功


if __name__ == '__main__':
    main()
