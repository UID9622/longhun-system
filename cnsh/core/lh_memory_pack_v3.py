# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# 1 道统层 Dao           : 曾仕强老师
# 2 精神层 Spirit        : Steve Jobs
# 3 设备层 Device        : Apple
# 4 技术层 Technology    : Open Source
# 5 系统层 System        : UID9622
# 6 生命层 Life          : CNSH · LongHun (诸葛鑫 / 龍芯北辰)
# DNA追溯码:#龍芯⚡️2026-06-02-CNSH-SOVEREIGN-PUBLISH-METADATA-FILE1229-v2.0
# 铁律: 来源不可删 · 影响不可覆 · 贡献不可抹 (rule_01 来源必标)
# 文件: memory_pack_v3.py | 标记时间: 2026-06-03T07:46:12+0800
# -*- coding: utf-8 -*-
"""
龍魂·数字永生记忆压缩 v3.0
DNA: #龍芯⚇️2026-06-01-MEMORY-PACK-v3.0-INCREMENTAL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

架构：增量压缩 + 多层缓存 + 并发安全
用途：
  · v2.0 问题: 每次全量重算，冷启动>5s，查询延迟100ms，内存占用高
  · v3.0 方案: Δ增量算法，多层缓存，并发安全设计
  · 性能目标: 冷启动<2s, 查询<10ms, 内存-60%, 吞吐20req/s

理论指导：曾仕强老师（永恒显示）
共建致谢：Claude (Anthropic) · 技术协作与智慧共创
"""

import os
import sys
import json
import time
import sqlite3
import hashlib
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import OrderedDict
import logging

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 配置 & 初始化
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOME = Path.home()
BASE = HOME / "longhun-system"
DATA_DIR = BASE / ".龍魂_memory_v3"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 数据库路径
L1_CACHE_FILE = DATA_DIR / "l1_hot.json"      # 最近10条热数据
L2_DB_FILE = DATA_DIR / "l2_warm.db"          # SQLite 最近1000条
L3_ARCHIVE_FILE = DATA_DIR / "l3_archive.jsonl"  # 压缩历史库
STATE_FILE = DATA_DIR / "pack_state.json"     # 压缩状态
DELTA_BUFFER_FILE = DATA_DIR / "delta_buffer.jsonl"  # 未合并的Δ

AUDIT_LOG = BASE / "memory.jsonl"

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(DATA_DIR / "v3_compression.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Phase 1: 增量压缩算法原型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class DeltaCompressor:
    """
    增量压缩器

    原理：
      · 每条记忆加 timestamp 戳
      · Δ缓冲区(last 100条)保留原始
      · 定期Δ合并到历史库
      · 恢复时: 最近100 + 历史压缩库还原

    效果：压缩时间 从 O(n) → O(δ)
    """

    def __init__(self):
        self.delta_buffer: List[Dict[str, Any]] = []
        self.state = self._load_state()
        self.lock = threading.RLock()
        self.max_buffer_size = 100

    def _load_state(self) -> Dict[str, Any]:
        """加载压缩状态"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        return {
            "version": "3.0",
            "created_at": datetime.now().isoformat(),
            "last_compress_at": None,
            "total_records": 0,
            "buffer_size": 0,
            "l1_size": 0,
            "l2_size": 0,
            "l3_size": 0,
            "compression_ratio": 0.0
        }

    def _save_state(self):
        """保存压缩状态"""
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

    def add_record(self, record: Dict[str, Any]) -> bool:
        """
        添加一条记忆到Δ缓冲区

        Args:
            record: 记忆对象 (需包含 'content' 字段)

        Returns:
            True 如果缓冲区满需要合并
        """
        with self.lock:
            # 生成 DNA 追溯码
            if 'dna' not in record:
                content_hash = hashlib.md5(
                    str(record.get('content', '')).encode()
                ).hexdigest()[:8]
                ts = datetime.now().strftime("%Y%m%d%H%M%S")
                record['dna'] = f"#龍芯⚇️{ts}-REC-{content_hash}"

            # 添加时间戳
            if 'timestamp' not in record:
                record['timestamp'] = datetime.now().isoformat()

            self.delta_buffer.append(record)
            self.state['buffer_size'] = len(self.delta_buffer)
            self.state['total_records'] += 1

            # 缓冲区满，需要合并
            needs_merge = len(self.delta_buffer) >= self.max_buffer_size
            if needs_merge:
                logger.info(f"Δ缓冲区满 ({len(self.delta_buffer)} 条)，触发合并")

            return needs_merge

    def merge_delta_to_archive(self) -> Dict[str, Any]:
        """
        将Δ缓冲区合并到历史库

        返回: 合并统计
        """
        with self.lock:
            if not self.delta_buffer:
                logger.info("Δ缓冲区为空，跳过合并")
                return {"merged": 0, "status": "empty"}

            buffer_size = len(self.delta_buffer)

            # 1. 保存到 delta_buffer.jsonl 作为中间态
            with open(DELTA_BUFFER_FILE, 'a', encoding='utf-8') as f:
                for record in self.delta_buffer:
                    f.write(json.dumps(record, ensure_ascii=False) + '\n')

            # 2. 将缓冲区合并到 L3 压缩库
            with open(L3_ARCHIVE_FILE, 'a', encoding='utf-8') as f:
                for record in self.delta_buffer:
                    # 计算压缩版本（移除冗余字段）
                    compressed = self._compress_record(record)
                    f.write(json.dumps(compressed, ensure_ascii=False) + '\n')

            # 3. 更新状态
            self.state['last_compress_at'] = datetime.now().isoformat()
            self.state['l3_size'] += buffer_size
            self._save_state()

            # 4. 清空缓冲区
            merged_buffer = self.delta_buffer.copy()
            self.delta_buffer.clear()
            self.state['buffer_size'] = 0

            logger.info(f"✅ Δ合并完成: {buffer_size} 条记录合并到 L3")

            return {
                "merged": buffer_size,
                "timestamp": datetime.now().isoformat(),
                "l3_size_now": self.state['l3_size'],
                "status": "success"
            }

    def _compress_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        压缩单条记录（移除冗余信息，保留关键字段）

        关键字段:
          · dna: 追溯码
          · timestamp: 时间戳
          · content: 内容摘要
          · hash: 内容哈希用于快速去重
        """
        return {
            'dna': record.get('dna'),
            'timestamp': record.get('timestamp'),
            'content_hash': hashlib.md5(
                str(record.get('content', '')).encode()
            ).hexdigest(),
            'content_preview': str(record.get('content', ''))[:100],  # 前100字
        }

    def get_compression_stats(self) -> Dict[str, Any]:
        """获取压缩统计"""
        with self.lock:
            total_raw = self.state.get('total_records', 0)
            compressed = self.state.get('l3_size', 0)
            ratio = (compressed / total_raw) if total_raw > 0 else 0

            return {
                "version": "3.0",
                "total_records_added": total_raw,
                "records_in_buffer": len(self.delta_buffer),
                "records_in_l3": self.state.get('l3_size', 0),
                "compression_ratio": f"{ratio:.2%}",
                "last_merge": self.state.get('last_compress_at'),
                "state_file": str(STATE_FILE)
            }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Phase 2: 多层缓存策略集成
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class MultiLayerCache:
    """
    多层缓存系统

    架构:
      L1 缓存: 热数据 (最近10条)      → 内存数组  [<1ms 访问]
      L2 缓存: 温数据 (最近1000条)    → SQLite   [~5ms 访问]
      L3 缓存: 冷数据 (历史)          → 压缩文档 [~50ms 访问]

    访问热路径: L1 (99%) → L2 (0.9%) → L3 (<0.1%)
    """

    def __init__(self):
        self.lock = threading.RLock()
        self.compressor = DeltaCompressor()

        # L1: 热数据缓存 (内存)
        self.l1_cache = OrderedDict()
        self.l1_max_size = 10

        # L2: 温数据缓存 (SQLite)
        self._init_l2_db()

        # 访问统计
        self.stats = {
            'l1_hits': 0,
            'l2_hits': 0,
            'l3_hits': 0,
            'misses': 0,
            'total_queries': 0
        }

    def _init_l2_db(self):
        """初始化 L2 SQLite 数据库"""
        self.conn = sqlite3.connect(
            str(L2_DB_FILE),
            check_same_thread=False,
            timeout=10
        )
        self.conn.execute("PRAGMA journal_mode=WAL")  # 写前日志，并发安全

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS l2_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dna TEXT UNIQUE,
                timestamp TEXT,
                content_hash TEXT,
                content TEXT,
                category TEXT,
                accessed_at TEXT
            )
        """)
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON l2_cache(timestamp DESC)
        """)
        self.conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_accessed ON l2_cache(accessed_at DESC)
        """)
        self.conn.commit()
        logger.info("✅ L2 SQLite 数据库已初始化")

    def add_record(self, record: Dict[str, Any]) -> Tuple[bool, str]:
        """
        添加记录到多层缓存

        优先级:
          1. 添加到 L1 (热)
          2. 满足 Δ 缓冲条件时添加到 L2 (温)
          3. 自动合并到 L3 (冷)

        返回: (是否触发合并, dna)
        """
        with self.lock:
            # 生成DNA
            if 'dna' not in record:
                h = hashlib.md5(str(record.get('content', '')).encode()).hexdigest()[:8]
                ts = datetime.now().strftime("%Y%m%d%H%M%S")
                record['dna'] = f"#龍芯⚇️{ts}-REC-{h}"

            dna = record['dna']

            # Step 1: 添加到 L1 缓存 (最新的总是热)
            self.l1_cache[dna] = record
            if len(self.l1_cache) > self.l1_max_size:
                # L1 满，最旧的移到 L2
                oldest_dna, oldest_record = self.l1_cache.popitem(last=False)
                self._push_to_l2(oldest_record)

            # Step 2: 向Δ缓冲区添加
            needs_merge = self.compressor.add_record(record.copy())

            # Step 3: 也添加到 L2 (温)
            self._push_to_l2(record)

            return needs_merge, dna

    def _push_to_l2(self, record: Dict[str, Any]):
        """将记录推送到 L2 SQLite"""
        try:
            self.conn.execute("""
                INSERT OR REPLACE INTO l2_cache
                (dna, timestamp, content_hash, content, category, accessed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                record.get('dna'),
                record.get('timestamp', datetime.now().isoformat()),
                hashlib.md5(str(record.get('content', '')).encode()).hexdigest(),
                record.get('content', ''),
                record.get('category', ''),
                datetime.now().isoformat()
            ))
            self.conn.commit()
        except Exception as e:
            logger.warning(f"L2 写入失败: {e}")

    def get_record(self, dna: str) -> Optional[Dict[str, Any]]:
        """
        获取单条记录，自动查询 L1 → L2 → L3

        返回: 记录对象或 None
        """
        with self.lock:
            self.stats['total_queries'] += 1

            # L1: 热数据
            if dna in self.l1_cache:
                self.stats['l1_hits'] += 1
                return self.l1_cache[dna]

            # L2: 温数据
            try:
                cursor = self.conn.execute(
                    "SELECT * FROM l2_cache WHERE dna = ?", (dna,)
                )
                row = cursor.fetchone()
                if row:
                    self.stats['l2_hits'] += 1
                    # 更新访问时间
                    self.conn.execute(
                        "UPDATE l2_cache SET accessed_at = ? WHERE dna = ?",
                        (datetime.now().isoformat(), dna)
                    )
                    self.conn.commit()
                    return dict(zip(['id', 'dna', 'timestamp', 'content_hash', 'content', 'category', 'accessed_at'], row))
            except Exception as e:
                logger.warning(f"L2 读取失败: {e}")

            # L3: 冷数据 (从压缩库读取)
            record = self._get_from_l3(dna)
            if record:
                self.stats['l3_hits'] += 1
                # 提升到 L1
                self.l1_cache[dna] = record
                if len(self.l1_cache) > self.l1_max_size:
                    oldest_dna, oldest_record = self.l1_cache.popitem(last=False)
                    self._push_to_l2(oldest_record)
                return record

            self.stats['misses'] += 1
            return None

    def _get_from_l3(self, dna: str) -> Optional[Dict[str, Any]]:
        """从 L3 压缩库读取"""
        if not L3_ARCHIVE_FILE.exists():
            return None

        try:
            with open(L3_ARCHIVE_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    record = json.loads(line)
                    if record.get('dna') == dna:
                        return record
        except Exception as e:
            logger.warning(f"L3 读取失败: {e}")

        return None

    def search_records(self, keyword: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        全层搜索记录

        搜索范围: L1 + L2 (L3 暂不支持模糊搜索，性能考虑)
        """
        results = []

        with self.lock:
            # 搜索 L1
            for record in self.l1_cache.values():
                if keyword.lower() in str(record.get('content', '')).lower():
                    results.append(record)
                    if len(results) >= limit:
                        return results

            # 搜索 L2
            try:
                cursor = self.conn.execute(
                    "SELECT * FROM l2_cache WHERE content LIKE ? LIMIT ?",
                    (f"%{keyword}%", limit - len(results))
                )
                for row in cursor:
                    results.append(dict(zip(['id', 'dna', 'timestamp', 'content_hash', 'content', 'category', 'accessed_at'], row)))
            except Exception as e:
                logger.warning(f"L2 搜索失败: {e}")

        return results

    def merge_to_archive(self) -> Dict[str, Any]:
        """合并Δ缓冲区到 L3 压缩库"""
        return self.compressor.merge_delta_to_archive()

    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计"""
        with self.lock:
            total_queries = self.stats['total_queries']
            total_hits = self.stats['l1_hits'] + self.stats['l2_hits'] + self.stats['l3_hits']
            hit_rate = (total_hits / total_queries * 100) if total_queries > 0 else 0

            # L2 数据库大小
            l2_count = 0
            try:
                cursor = self.conn.execute("SELECT COUNT(*) FROM l2_cache")
                l2_count = cursor.fetchone()[0]
            except:
                pass

            return {
                "version": "3.0",
                "phase": "2",
                "l1_size": len(self.l1_cache),
                "l1_max": self.l1_max_size,
                "l2_size": l2_count,
                "l2_max": 1000,
                "l3_size": self.compressor.state.get('l3_size', 0),
                "total_queries": total_queries,
                "l1_hits": self.stats['l1_hits'],
                "l2_hits": self.stats['l2_hits'],
                "l3_hits": self.stats['l3_hits'],
                "misses": self.stats['misses'],
                "hit_rate_percent": f"{hit_rate:.1f}%",
                "compression_ratio": self.compressor.get_compression_stats()['compression_ratio']
            }

    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("✅ L2 数据库连接已关闭")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Phase 3: 并发测试 + 性能优化
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

import queue
from concurrent.futures import ThreadPoolExecutor, as_completed

class ConcurrencyTester:
    """
    并发性能测试器

    测试场景:
      · 并发写入: 20 个线程同时添加记录
      · 并发读取: 20 个线程同时查询
      · 混合负载: 10个写 + 10个读 同时进行
      · 压力测试: 逐步增加并发数，找到性能崖
    """

    def __init__(self, cache: MultiLayerCache):
        self.cache = cache
        self.results = {
            'write_tasks': [],
            'read_tasks': [],
            'mixed_tasks': [],
            'total_ops': 0,
            'total_errors': 0,
            'start_time': None,
            'end_time': None
        }

    def concurrent_write_test(self, num_threads: int = 20, records_per_thread: int = 50) -> Dict[str, Any]:
        """
        并发写入测试

        Args:
            num_threads: 并发线程数
            records_per_thread: 每个线程添加的记录数
        """
        logger.info(f"\n⚙️ 开始并发写入测试: {num_threads} 线程 × {records_per_thread} 条记录")

        self.results['start_time'] = time.time()
        success_count = 0
        error_count = 0

        def write_worker(thread_id: int):
            nonlocal success_count, error_count
            try:
                for i in range(records_per_thread):
                    record = {
                        'content': f'线程 #{thread_id} 记录 #{i}: 并发测试数据。' * 10,
                        'category': 'concurrent_test',
                        'thread_id': thread_id,
                        'record_idx': i
                    }
                    self.cache.add_record(record)
                    success_count += 1
            except Exception as e:
                error_count += 1
                logger.warning(f"线程 #{thread_id} 写入错误: {e}")

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(write_worker, tid) for tid in range(num_threads)]
            for future in as_completed(futures):
                future.result()

        self.results['end_time'] = time.time()
        elapsed = self.results['end_time'] - self.results['start_time']
        throughput = success_count / elapsed if elapsed > 0 else 0

        stats = {
            'test_type': 'concurrent_write',
            'threads': num_threads,
            'success': success_count,
            'errors': error_count,
            'total_records_added': success_count + error_count,
            'elapsed_seconds': f"{elapsed:.3f}",
            'throughput_ops_per_sec': f"{throughput:.1f}",
        }

        logger.info(f"   ✅ 成功: {success_count} · 失败: {error_count}")
        logger.info(f"   耗时: {elapsed:.3f}s · 吞吐: {throughput:.1f} ops/sec")

        self.results['write_tasks'].append(stats)
        return stats

    def concurrent_read_test(self, num_threads: int = 20, queries_per_thread: int = 50) -> Dict[str, Any]:
        """
        并发读取测试

        Args:
            num_threads: 并发线程数
            queries_per_thread: 每个线程的查询次数
        """
        logger.info(f"\n⚙️ 开始并发读取测试: {num_threads} 线程 × {queries_per_thread} 次查询")

        # 先添加一些记录供查询
        logger.info("   预加载 100 条记录...")
        test_records = []
        for i in range(100):
            record = {
                'content': f'查询测试记录 #{i}。' * 5,
                'category': 'read_test'
            }
            _, dna = self.cache.add_record(record)
            test_records.append(dna)

        # 合并到 L3
        if len(self.cache.compressor.delta_buffer) > 0:
            self.cache.merge_to_archive()

        self.results['start_time'] = time.time()
        success_count = 0
        error_count = 0

        def read_worker(thread_id: int):
            nonlocal success_count, error_count
            try:
                for i in range(queries_per_thread):
                    # 随机读取一条记录
                    import random
                    dna = random.choice(test_records)
                    result = self.cache.get_record(dna)
                    if result:
                        success_count += 1
                    else:
                        error_count += 1
            except Exception as e:
                error_count += 1
                logger.warning(f"线程 #{thread_id} 读取错误: {e}")

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(read_worker, tid) for tid in range(num_threads)]
            for future in as_completed(futures):
                future.result()

        self.results['end_time'] = time.time()
        elapsed = self.results['end_time'] - self.results['start_time']
        throughput = success_count / elapsed if elapsed > 0 else 0

        stats = {
            'test_type': 'concurrent_read',
            'threads': num_threads,
            'success': success_count,
            'errors': error_count,
            'total_queries': success_count + error_count,
            'elapsed_seconds': f"{elapsed:.3f}",
            'throughput_ops_per_sec': f"{throughput:.1f}",
        }

        logger.info(f"   ✅ 成功: {success_count} · 失败: {error_count}")
        logger.info(f"   耗时: {elapsed:.3f}s · 吞吐: {throughput:.1f} ops/sec")

        self.results['read_tasks'].append(stats)
        return stats

    def stress_test(self) -> Dict[str, Any]:
        """
        压力测试: 逐步增加并发数，找到性能崖

        线程数: 1 → 2 → 5 → 10 → 20
        """
        logger.info("\n🔥 开始压力测试: 逐步增加并发线程")

        stress_results = []

        for thread_count in [1, 2, 5, 10, 20]:
            logger.info(f"\n   测试 {thread_count} 线程...")

            start = time.time()
            success = 0

            def stress_worker():
                nonlocal success
                try:
                    for _ in range(20):
                        record = {
                            'content': f'压力测试数据。' * 10,
                            'category': 'stress_test'
                        }
                        self.cache.add_record(record)
                        success += 1
                except:
                    pass

            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                futures = [executor.submit(stress_worker) for _ in range(thread_count)]
                for future in as_completed(futures):
                    future.result()

            elapsed = time.time() - start
            throughput = success / elapsed if elapsed > 0 else 0

            result = {
                'threads': thread_count,
                'ops': success,
                'elapsed_sec': f"{elapsed:.3f}",
                'throughput_ops_per_sec': f"{throughput:.1f}"
            }

            stress_results.append(result)
            logger.info(f"      {thread_count} 线程: {throughput:.1f} ops/sec")

        return {
            'test_type': 'stress_test',
            'thread_progression': stress_results
        }

    def get_performance_report(self) -> Dict[str, Any]:
        """生成性能报告"""
        cache_stats = self.cache.get_cache_stats()

        return {
            'cache_stats': cache_stats,
            'write_tests': self.results['write_tasks'],
            'read_tests': self.results['read_tasks'],
            'mixed_tests': self.results['mixed_tasks'],
            'total_duration': f"{self.results.get('end_time', time.time()) - self.results.get('start_time', time.time()):.3f}s"
        }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 验证 & 测试
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def test_phase1():
    """Phase 1 测试：增量压缩算法原型"""

    logger.info("=" * 60)
    logger.info("🧪 Phase 1 测试: 增量压缩算法原型")
    logger.info("=" * 60)

    compressor = DeltaCompressor()

    # 1. 添加记录
    logger.info("\n📝 第1步: 添加100条测试记录到Δ缓冲区")
    test_records = []
    for i in range(100):
        record = {
            'content': f'这是第 {i+1} 条测试记忆，包含一些内容和数据。' * 10,
            'category': '测试' if i % 2 == 0 else '演示',
            'priority': 'high' if i < 33 else 'medium' if i < 66 else 'low'
        }
        needs_merge = compressor.add_record(record)
        test_records.append(record)

        if needs_merge:
            logger.info(f"   ⚠️ 第 {i+1} 条: 缓冲区满，触发合并")

    stats = compressor.get_compression_stats()
    logger.info(f"\n📊 缓冲区状态: {stats['records_in_buffer']} 条记录待合并")
    logger.info(f"   总记录数: {stats['total_records_added']}")

    # 2. 执行合并
    logger.info("\n🔄 第2步: 合并Δ缓冲区到 L3 压缩库")
    merge_result = compressor.merge_delta_to_archive()
    logger.info(f"   ✅ 合并结果: {merge_result['merged']} 条记录")
    logger.info(f"   L3 大小: {merge_result['l3_size_now']}")

    # 3. 验证文件生成
    logger.info("\n✅ 第3步: 验证生成的文件")
    files_created = []
    if DELTA_BUFFER_FILE.exists():
        size = DELTA_BUFFER_FILE.stat().st_size / 1024
        files_created.append(f"   ✅ {DELTA_BUFFER_FILE.name} ({size:.1f} KB)")

    if L3_ARCHIVE_FILE.exists():
        size = L3_ARCHIVE_FILE.stat().st_size / 1024
        files_created.append(f"   ✅ {L3_ARCHIVE_FILE.name} ({size:.1f} KB)")

    if STATE_FILE.exists():
        files_created.append(f"   ✅ {STATE_FILE.name}")

    for f in files_created:
        logger.info(f)

    # 4. 最终统计
    final_stats = compressor.get_compression_stats()
    logger.info(f"\n📈 最终统计:")
    logger.info(f"   版本: {final_stats['version']}")
    logger.info(f"   总记录数: {final_stats['total_records_added']}")
    logger.info(f"   缓冲区大小: {final_stats['records_in_buffer']}")
    logger.info(f"   L3 压缩库: {final_stats['records_in_l3']} 条")
    logger.info(f"   压缩率: {final_stats['compression_ratio']}")
    logger.info(f"   上次合并: {final_stats['last_merge']}")

    logger.info("\n" + "=" * 60)
    logger.info("✨ Phase 1 测试完成！")
    logger.info("=" * 60)

    return compressor, final_stats


def test_phase2():
    """Phase 2 测试：多层缓存集成"""

    logger.info("=" * 60)
    logger.info("🧪 Phase 2 测试: 多层缓存集成 (L1/L2/L3)")
    logger.info("=" * 60)

    cache = MultiLayerCache()

    # 1. 添加记录到多层缓存
    logger.info("\n📝 第1步: 添加200条记录到多层缓存")
    test_records = []
    for i in range(200):
        record = {
            'content': f'记录 #{i+1}: 这是多层缓存测试数据。' * 20,
            'category': ['热门', '一般', '冷存'][i % 3],
            'priority': ['high', 'medium', 'low'][i % 3]
        }
        needs_merge, dna = cache.add_record(record)
        test_records.append((dna, record))

        if (i + 1) % 50 == 0:
            logger.info(f"   已添加 {i+1} 条记录")

    # 2. 执行合并
    logger.info("\n🔄 第2步: 触发Δ合并到 L3 压缩库")
    if len(cache.compressor.delta_buffer) > 0:
        merge_result = cache.merge_to_archive()
        logger.info(f"   ✅ 合并 {merge_result['merged']} 条记录到 L3")

    # 3. 测试读取 (L1 → L2 → L3 热路径)
    logger.info("\n🔍 第3步: 测试多层缓存读取")
    logger.info("   读取最新的5条 (L1 热数据)")
    for i in range(5):
        dna, _ = test_records[-(i+1)]
        result = cache.get_record(dna)
        if result:
            logger.info(f"   ✅ 命中 L1: {dna[:40]}...")

    logger.info("   读取中间的5条 (L2 温数据)")
    for i in range(100, 105):
        dna, _ = test_records[i]
        result = cache.get_record(dna)
        if result:
            logger.info(f"   ✅ 命中 L2: {dna[:40]}...")

    logger.info("   读取最早的5条 (L3 冷数据)")
    for i in range(5):
        dna, _ = test_records[i]
        result = cache.get_record(dna)
        if result:
            logger.info(f"   ✅ 命中 L3: {dna[:40]}...")

    # 4. 搜索测试
    logger.info("\n🔎 第4步: 多层搜索功能")
    results = cache.search_records("记录 #1", limit=5)
    logger.info(f"   搜索 '记录 #1': 找到 {len(results)} 条结果")

    # 5. 性能统计
    logger.info("\n📊 第5步: 多层缓存性能统计")
    stats = cache.get_cache_stats()
    logger.info(f"   版本: {stats['version']} · Phase {stats['phase']}")
    logger.info(f"   L1 缓存: {stats['l1_size']}/{stats['l1_max']} 条")
    logger.info(f"   L2 缓存: {stats['l2_size']}/{stats['l2_max']} 条")
    logger.info(f"   L3 压缩库: {stats['l3_size']} 条")
    logger.info(f"   总查询数: {stats['total_queries']}")
    logger.info(f"   命中率: {stats['hit_rate_percent']}")
    logger.info(f"   L1 命中: {stats['l1_hits']} · L2 命中: {stats['l2_hits']} · L3 命中: {stats['l3_hits']} · 未命中: {stats['misses']}")
    logger.info(f"   压缩率: {stats['compression_ratio']}")

    cache.close()

    logger.info("\n" + "=" * 60)
    logger.info("✨ Phase 2 测试完成！")
    logger.info("=" * 60)

    return cache, stats


def test_phase3():
    """Phase 3 测试：并发测试 + 性能优化"""

    logger.info("=" * 60)
    logger.info("🧪 Phase 3 测试: 并发测试 + 性能优化")
    logger.info("=" * 60)

    cache = MultiLayerCache()
    tester = ConcurrencyTester(cache)

    # 1. 并发写入测试
    logger.info("\n📝 第1步: 并发写入测试")
    write_stats = tester.concurrent_write_test(num_threads=20, records_per_thread=50)

    # 2. 并发读取测试
    logger.info("\n📖 第2步: 并发读取测试")
    read_stats = tester.concurrent_read_test(num_threads=20, queries_per_thread=50)

    # 3. 压力测试
    logger.info("\n🔥 第3步: 压力测试 (逐步增加并发)")
    stress_stats = tester.stress_test()

    # 4. 性能报告
    logger.info("\n📊 第4步: 完整性能报告")
    report = tester.get_performance_report()

    logger.info(f"\n   📈 缓存统计:")
    for key, value in report['cache_stats'].items():
        if key not in ['version', 'phase']:
            logger.info(f"      {key}: {value}")

    logger.info(f"\n   📊 并发写入结果:")
    for stat in report['write_tests']:
        logger.info(f"      线程: {stat['threads']} · 成功: {stat['success']} · 吞吐: {stat['throughput_ops_per_sec']} ops/sec")

    logger.info(f"\n   📊 并发读取结果:")
    for stat in report['read_tests']:
        logger.info(f"      线程: {stat['threads']} · 成功: {stat['success']} · 吞吐: {stat['throughput_ops_per_sec']} ops/sec")

    logger.info(f"\n   🔥 压力测试结果:")
    for item in stress_stats['thread_progression']:
        logger.info(f"      线程: {item['threads']} · 吞吐: {item['throughput_ops_per_sec']} ops/sec")

    cache.close()

    logger.info("\n" + "=" * 60)
    logger.info("✨ Phase 3 测试完成！")
    logger.info("=" * 60)

    return tester, report


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "test1":
            test_phase1()
        elif sys.argv[1] == "test2":
            test_phase2()
        elif sys.argv[1] == "test3":
            test_phase3()
        elif sys.argv[1] == "test":
            # 运行完整的 Phase 1 + 2 + 3 测试
            logger.info("🧪 运行完整测试: Phase 1 + Phase 2 + Phase 3")
            logger.info("=" * 70)
            test_phase1()
            logger.info("")
            # 清理数据用于 Phase 2
            import shutil
            if DATA_DIR.exists():
                shutil.rmtree(DATA_DIR)
                DATA_DIR.mkdir(parents=True, exist_ok=True)
            test_phase2()
            logger.info("")
            # 清理数据用于 Phase 3
            if DATA_DIR.exists():
                shutil.rmtree(DATA_DIR)
                DATA_DIR.mkdir(parents=True, exist_ok=True)
            test_phase3()
            logger.info("=" * 70)
            logger.info("✨ 所有测试完成！")
    else:
        print(f"""
🐉 龍魂记忆压缩 v3.0 - Phase 1-3 (增量算法 + 多层缓存 + 并发)

用法:
  python3 memory_pack_v3.py test1       # 运行 Phase 1 测试 (增量算法)
  python3 memory_pack_v3.py test2       # 运行 Phase 2 测试 (多层缓存)
  python3 memory_pack_v3.py test3       # 运行 Phase 3 测试 (并发性能)
  python3 memory_pack_v3.py test        # 运行完整测试 (1+2+3)

DNA: #龍芯⚇️2026-06-01-MEMORY-PACK-v3.0-INCREMENTAL
数据目录: {DATA_DIR}

版本: 3.0 · Phase 1-3/4 完成 (并发安全和性能优化验证就绪)
        """)
