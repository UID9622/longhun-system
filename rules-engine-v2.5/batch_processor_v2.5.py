#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂规则引擎 · 批量处理 v2.5
优化特性: 并行化·进度条·失败重试·内存管理

DNA:#龍芯⚡️2026-06-07-BATCH-PROCESSOR-v2.5
责任: UID9622 · 不免责
"""

import json
import time
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
from typing import Dict, List, Callable, Any
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    from tqdm import tqdm
except ImportError:
    # Fallback if tqdm not installed
    def tqdm(iterable, **kwargs):
        return iterable


# ============================================================================
# [日志配置]
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/rules_engine_batch.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


# ============================================================================
# [失败重试装饰器]
# ============================================================================

def retry(max_retries: int = 3, backoff_factor: float = 2, jitter: bool = True):
    """
    失败自动重试装饰器

    Args:
        max_retries: 最大重试次数
        backoff_factor: 指数退避因子
        jitter: 是否添加随机抖动
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    if attempt < max_retries - 1:
                        # 计算等待时间
                        wait_time = backoff_factor ** attempt

                        # 添加随机抖动 (避免雷群效应)
                        if jitter:
                            import random
                            wait_time *= random.uniform(0.5, 1.5)

                        logger.warning(
                            f"尝试 {attempt + 1}/{max_retries} 失败: {e}. "
                            f"等待 {wait_time:.2f}s 后重试..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"所有 {max_retries} 次尝试均已失败: {e}")

            raise last_exception

        return wrapper

    return decorator


# ============================================================================
# [数据结构]
# ============================================================================

@dataclass
class Case:
    """案件数据"""
    id: str
    content: str
    metadata: Dict[str, Any]
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class ProcessResult:
    """处理结果"""
    case_id: str
    status: str  # 'success' | 'error' | 'skipped'
    result: Dict[str, Any]
    error: str = None
    processing_time_ms: float = 0
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


# ============================================================================
# [批量处理引擎]
# ============================================================================

class RulesEngineBatchProcessorV25:
    """规则引擎批量处理器 v2.5"""

    def __init__(
        self,
        max_workers: int = 4,
        chunk_size: int = 100,
        enable_progress: bool = True
    ):
        """
        初始化处理器

        Args:
            max_workers: 最大线程数
            chunk_size: 每批处理的案件数
            enable_progress: 是否显示进度条
        """
        self.max_workers = max_workers
        self.chunk_size = chunk_size
        self.enable_progress = enable_progress
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        self.results: List[ProcessResult] = []
        self.errors: List[Dict] = []

        logger.info(f"初始化批量处理器: workers={max_workers}, chunk_size={chunk_size}")

    @retry(max_retries=3, backoff_factor=2)
    def _process_case(self, case: Case) -> ProcessResult:
        """
        处理单个案件 (带重试机制)

        Args:
            case: 案件对象

        Returns:
            处理结果
        """
        start_time = time.time()

        try:
            # 模拟规则引擎计算
            # 实际应该调用真实的规则评估函数
            result = self._evaluate_case_with_rules(case)

            processing_time = (time.time() - start_time) * 1000  # 转换为毫秒

            return ProcessResult(
                case_id=case.id,
                status='success',
                result=result,
                processing_time_ms=processing_time
            )

        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            logger.error(f"案件 {case.id} 处理失败: {e}")

            return ProcessResult(
                case_id=case.id,
                status='error',
                result={},
                error=str(e),
                processing_time_ms=processing_time
            )

    def _evaluate_case_with_rules(self, case: Case) -> Dict[str, Any]:
        """
        评估案件 (实现规则逻辑)

        Args:
            case: 案件对象

        Returns:
            评估结果字典
        """
        # 简化版规则引擎
        # 实际应包含复杂的业务逻辑

        return {
            "case_id": case.id,
            "verdict": "通过" if len(case.content) > 10 else "驳回",
            "confidence": 0.95,
            "rules_applied": ["rule_001", "rule_002"],
            "metadata": case.metadata
        }

    def process_batch(
        self,
        cases: List[Case],
        output_file: Path = None
    ) -> Dict[str, Any]:
        """
        批量处理案件

        Args:
            cases: 案件列表
            output_file: 输出文件路径 (可选)

        Returns:
            处理统计信息
        """
        logger.info(f"开始处理 {len(cases)} 个案件")

        self.results = []
        self.errors = []

        # 提交所有任务
        futures = {
            self.executor.submit(self._process_case, case): i
            for i, case in enumerate(cases)
        }

        # 进度条包装
        iterator = as_completed(futures)
        if self.enable_progress:
            iterator = tqdm(iterator, total=len(cases), desc="处理进度")

        # 收集结果
        for future in iterator:
            idx = futures[future]
            try:
                result = future.result()
                self.results.append(result)

                if result.status == 'error':
                    self.errors.append({
                        'index': idx,
                        'case_id': result.case_id,
                        'error': result.error
                    })

            except Exception as e:
                logger.error(f"任务执行异常 (index={idx}): {e}")
                self.errors.append({
                    'index': idx,
                    'error': str(e)
                })

        # 生成报告
        report = self._generate_report(output_file)
        logger.info(f"批量处理完成: {report['summary']}")

        return report

    def process_batch_from_file(
        self,
        input_file: Path,
        output_file: Path = None
    ) -> Dict[str, Any]:
        """
        从文件读取案件并批量处理

        Args:
            input_file: 输入 JSON 文件
            output_file: 输出文件路径

        Returns:
            处理统计信息
        """
        logger.info(f"从文件读取案件: {input_file}")

        # 读取输入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 转换为 Case 对象
        cases = [
            Case(
                id=item.get('id'),
                content=item.get('content'),
                metadata=item.get('metadata', {})
            )
            for item in data
        ]

        logger.info(f"读取 {len(cases)} 个案件")

        # 处理案件
        return self.process_batch(cases, output_file)

    def _generate_report(self, output_file: Path = None) -> Dict[str, Any]:
        """
        生成处理报告

        Args:
            output_file: 输出文件路径 (可选)

        Returns:
            报告字典
        """
        total = len(self.results)
        success = sum(1 for r in self.results if r.status == 'success')
        errors = sum(1 for r in self.results if r.status == 'error')

        avg_time = sum(r.processing_time_ms for r in self.results) / total if total > 0 else 0

        report = {
            'summary': f"总计: {total}, 成功: {success}, 失败: {errors}",
            'statistics': {
                'total': total,
                'success': success,
                'errors': errors,
                'success_rate': f"{(success / total * 100):.1f}%" if total > 0 else "N/A",
                'avg_processing_time_ms': f"{avg_time:.2f}"
            },
            'results': [asdict(r) for r in self.results],
            'error_details': self.errors,
            'timestamp': datetime.now().isoformat()
        }

        # 如果指定输出文件，保存报告
        if output_file:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"报告已保存: {output_file}")

        return report

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.executor.shutdown(wait=True)


# ============================================================================
# [命令行界面]
# ============================================================================

def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("使用方式:")
        print("  python batch_processor_v2.5.py <input_file> [output_file]")
        print()
        print("示例:")
        print("  python batch_processor_v2.5.py cases.json results.json")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file.parent / f"{input_file.stem}_results.json"

    # 执行批量处理
    with RulesEngineBatchProcessorV25(max_workers=4) as processor:
        report = processor.process_batch_from_file(input_file, output_file)

    # 打印摘要
    print("\n" + "=" * 60)
    print("📊 处理完成!")
    print("=" * 60)
    print(f"总计:    {report['statistics']['total']}")
    print(f"成功:    {report['statistics']['success']}")
    print(f"失败:    {report['statistics']['errors']}")
    print(f"成功率:  {report['statistics']['success_rate']}")
    print(f"平均时间: {report['statistics']['avg_processing_time_ms']} ms")
    print(f"结果已保存: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
