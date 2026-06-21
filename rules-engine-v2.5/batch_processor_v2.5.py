#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
龍魂規則引擎 · 批量處理 v2.5
優化特性: 並行化·進度條·失敗重試·內存管理

DNA:#龍芯⚡️2026-06-07-BATCH-PROCESSOR-v2.5
責任: UID9622 · 不免責
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
# [日誌配置]
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
# [失敗重試裝飾器]
# ============================================================================

def retry(max_retries: int = 3, backoff_factor: float = 2, jitter: bool = True):
    """
    失敗自動重試裝飾器

    Args:
        max_retries: 最大重試次數
        backoff_factor: 指數退避因子
        jitter: 是否添加隨機抖動
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
                        # 計算等待時間
                        wait_time = backoff_factor ** attempt

                        # 添加隨機抖動 (避免雷群效應)
                        if jitter:
                            import random
                            wait_time *= random.uniform(0.5, 1.5)

                        logger.warning(
                            f"嘗試 {attempt + 1}/{max_retries} 失敗: {e}. "
                            f"等待 {wait_time:.2f}s 後重試..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"所有 {max_retries} 次嘗試均已失敗: {e}")

            raise last_exception

        return wrapper

    return decorator


# ============================================================================
# [數據結構]
# ============================================================================

@dataclass
class Case:
    """案件數據"""
    id: str
    content: str
    metadata: Dict[str, Any]
    timestamp: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


@dataclass
class ProcessResult:
    """處理結果"""
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
# [批量處理引擎]
# ============================================================================

class RulesEngineBatchProcessorV25:
    """規則引擎批量處理器 v2.5"""

    def __init__(
        self,
        max_workers: int = 4,
        chunk_size: int = 100,
        enable_progress: bool = True
    ):
        """
        初始化處理器

        Args:
            max_workers: 最大線程數
            chunk_size: 每批處理的案件數
            enable_progress: 是否顯示進度條
        """
        self.max_workers = max_workers
        self.chunk_size = chunk_size
        self.enable_progress = enable_progress
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        self.results: List[ProcessResult] = []
        self.errors: List[Dict] = []

        logger.info(f"初始化批量處理器: workers={max_workers}, chunk_size={chunk_size}")

    @retry(max_retries=3, backoff_factor=2)
    def _process_case(self, case: Case) -> ProcessResult:
        """
        處理單個案件 (帶重試機制)

        Args:
            case: 案件對象

        Returns:
            處理結果
        """
        start_time = time.time()

        try:
            # 模擬規則引擎計算
            # 實際應該調用真實的規則評估函數
            result = self._evaluate_case_with_rules(case)

            processing_time = (time.time() - start_time) * 1000  # 轉換為毫秒

            return ProcessResult(
                case_id=case.id,
                status='success',
                result=result,
                processing_time_ms=processing_time
            )

        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            logger.error(f"案件 {case.id} 處理失敗: {e}")

            return ProcessResult(
                case_id=case.id,
                status='error',
                result={},
                error=str(e),
                processing_time_ms=processing_time
            )

    def _evaluate_case_with_rules(self, case: Case) -> Dict:
        """
        評估案件 (實現規則邏輯)

        Args:
            case: 案件對象

        Returns:
            評估結果字典
        """
        # 簡化版規則引擎
        # 實際應包含複雜的業務邏輯

        return {
            "case_id": case.id,
            "verdict": "通過" if len(case.content) > 10 else "駁回",
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
        批量處理案件

        Args:
            cases: 案件列表
            output_file: 輸出文件路徑 (可選)

        Returns:
            處理統計信息
        """
        logger.info(f"開始處理 {len(cases)} 個案件")

        self.results = []
        self.errors = []

        # 提交所有任務
        futures = {
            self.executor.submit(self._process_case, case): i
            for i, case in enumerate(cases)
        }

        # 進度條包裝
        iterator = as_completed(futures)
        if self.enable_progress:
            iterator = tqdm(iterator, total=len(cases), desc="處理進度")

        # 收集結果
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
                logger.error(f"任務執行異常 (index={idx}): {e}")
                self.errors.append({
                    'index': idx,
                    'error': str(e)
                })

        # 生成報告
        report = self._generate_report(output_file)
        logger.info(f"批量處理完成: {report['summary']}")

        return report

    def process_batch_from_file(
        self,
        input_file: Path,
        output_file: Path = None
    ) -> Dict[str, Any]:
        """
        從文件讀取案件並批量處理

        Args:
            input_file: 輸入 JSON 文件
            output_file: 輸出文件路徑

        Returns:
            處理統計信息
        """
        logger.info(f"從文件讀取案件: {input_file}")

        # 讀取輸入文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 轉換為 Case 對象
        cases = [
            Case(
                id=item.get('id'),
                content=item.get('content'),
                metadata=item.get('metadata', {})
            )
            for item in data
        ]

        logger.info(f"讀取 {len(cases)} 個案件")

        # 處理案件
        return self.process_batch(cases, output_file)

    def _generate_report(self, output_file: Path = None) -> Dict[str, Any]:
        """
        生成處理報告

        Args:
            output_file: 輸出文件路徑 (可選)

        Returns:
            報告字典
        """
        total = len(self.results)
        success = sum(1 for r in self.results if r.status == 'success')
        errors = sum(1 for r in self.results if r.status == 'error')

        avg_time = sum(r.processing_time_ms for r in self.results) / total if total > 0 else 0

        report = {
            'summary': f"總計: {total}, 成功: {success}, 失敗: {errors}",
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

        # 如果指定輸出文件，保存報告
        if output_file:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info(f"報告已保存: {output_file}")

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

    # 執行批量處理
    with RulesEngineBatchProcessorV25(max_workers=4) as processor:
        report = processor.process_batch_from_file(input_file, output_file)

    # 打印摘要
    print("\n" + "=" * 60)
    print("📊 處理完成!")
    print("=" * 60)
    print(f"總計:    {report['statistics']['total']}")
    print(f"成功:    {report['statistics']['success']}")
    print(f"失敗:    {report['statistics']['errors']}")
    print(f"成功率:  {report['statistics']['success_rate']}")
    print(f"平均時間: {report['statistics']['avg_processing_time_ms']} ms")
    print(f"結果已保存: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
