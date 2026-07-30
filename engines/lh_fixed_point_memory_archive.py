#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·巳时·渐-FIXED-POINT-MEMORY-ARCHIVE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
# ═══════════════════════════════════════════════════════════
# 龍魂 · 不动点记忆归档引擎 v1.0
# ═══════════════════════════════════════════════════════════
# DNA: #龍芯⚡️丙午·丙申·癸酉·巳时·渐-FIXED-POINT-MEMORY-ARCHIVE-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 设计目标：把「压缩」「不动点」「记忆归档」合成一条流水线，
#          不算力的不浪费，不到不动点的不归档。
#
# 统一原则：
#   1. 一次哈希：SHA-256 / SimHash 同时服务于去重、索引、DNA。
#   2. 一次不动点判定：七色不动点 + 排序锚点 + 确认码，三闸同判。
#   3. 只在不动点归档：未达不动点的记忆只进缓冲池，不持久化。
#   4. 轻量压缩：龍魂字典替换 + zlib，不动点的才压。
#   5. 可追溯：每条归档带 DNA、来源、时间锚、父引用。
#
# 替代关系：
#   - 替代 exobrain_compressor 的全量扫描
#   - 替代 memory_eternity 的无差别快照
#   - 承接 fixed_point_bridge 的不动点语义
#   - 复用 compression_engine 的龍魂字典
#
# 用法：
#   python3 engines/lh_fixed_point_memory_archive.py ingest "今天决定..." --source "Kimi"
#   python3 engines/lh_fixed_point_memory_archive.py status
#   python3 engines/lh_fixed_point_memory_archive.py search "DNA"
#   python3 engines/lh_fixed_point_memory_archive.py pending
# ═══════════════════════════════════════════════════════════
"""

import argparse
import hashlib
import json
import math
import re
import zlib
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ============================================================
# 常量与路径
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_DIR = PROJECT_ROOT / "state" / "fp_memory_archive"
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

BUFFER_FILE = ARCHIVE_DIR / "pending_buffer.jsonl"
QUARANTINE_FILE = ARCHIVE_DIR / "quarantine.jsonl"
INDEX_FILE = ARCHIVE_DIR / "fixed_point_index.jsonl"
STATS_FILE = ARCHIVE_DIR / "archive_stats.json"

# 龍魂高频字典（复用 compression_engine 核心词条，一次加载）
LONGHUN_DICT = {
    "龍魂": "LH", "LongHun": "LH", "UID9622": "U9", "CNSH": "CN",
    "DNA": "D", "追溯": "Z", "压缩": "Y", "人格": "R", "模块": "M",
    "系统": "X", "状态": "S", "三色": "3C", "不动点": "FP",
    "归档": "AR", "记忆": "MEM", "确认码": "CF", "审计": "AU",
    "主权": "SV", "铁律": "IL", "熔断": "CB",
}

# 不动点锚词：命中这些说明记忆趋于稳定
FIXED_POINT_ANCHORS = {
    "确认码", "确认", "焊死", "归档", "落地", "完成", "通过", "决定",
    "DNA", "签章", "GPG", "冻结", "永不", "只此一次", "DONE",
}

# 非不动点信号：看到这些说明还在摇摆
PENDING_SIGNALS = {
    "待定", "待确认", "TODO", "考虑一下", " maybe ", "也许", "或者",
    "回头再说", "暂定", "草案", "初稿",
}

# 隐私敏感信号
PRIVACY_SIGNALS = {"隐私", "身份证号", "手机号", "密码", "密钥", "私钥", "银行卡"}

# 法律红线信号
LEGAL_RED_SIGNALS = {"违法", "犯罪", "攻击", "入侵", "窃取", "破坏"}


# ============================================================
# 不动点状态
# ============================================================
class FixedPointState(str, Enum):
    GOLD = "GOLD"       # 金 · 主控确认 · 永存档
    GREEN = "GREEN"     # 绿 · 自动放行 · 留痕归档
    YELLOW = "YELLOW"   # 黄 · 待确认 · 进缓冲池
    RED = "RED"         # 红 · 法律红线 · 阻断不上链
    BLACK = "BLACK"     # 黑 · 隐私敏感 · 本地隔离


class MemoryArchive:
    """不动点记忆归档核心引擎"""

    DNA = "#龍芯⚡️丙午·丙申·癸酉·巳时·渐-FIXED-POINT-MEMORY-ARCHIVE-v1.0"

    def __init__(self, archive_dir: Optional[Path] = None):
        self.archive_dir = Path(archive_dir) if archive_dir else ARCHIVE_DIR
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        self.buffer_file = self.archive_dir / "pending_buffer.jsonl"
        self.quarantine_file = self.archive_dir / "quarantine.jsonl"
        self.index_file = self.archive_dir / "fixed_point_index.jsonl"
        self.stats_file = self.archive_dir / "archive_stats.json"
        self._ensure_files()

    def _ensure_files(self):
        for f in [self.buffer_file, self.quarantine_file, self.index_file]:
            if not f.exists():
                f.touch()

    # ---------- 一次哈希，多处复用 ----------
    @staticmethod
    def sha256(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    @staticmethod
    def simhash(text: str) -> int:
        """64-bit SimHash，用于近似去重"""
        tokens = MemoryArchive._tokenize(text)
        v = [0] * 64
        for token in tokens:
            h = int(hashlib.md5(token.encode("utf-8")).hexdigest()[:16], 16)
            for i in range(64):
                if h & (1 << i):
                    v[i] += 1
                else:
                    v[i] -= 1
        result = 0
        for i in range(64):
            if v[i] > 0:
                result |= (1 << i)
        return result

    @staticmethod
    def hamming_distance(a: int, b: int) -> int:
        return bin(a ^ b).count("1")

    @staticmethod
    def _tokenize(text: str) -> Set[str]:
        tokens = set()
        for m in re.finditer(r"[\u4e00-\u9fff]{2,4}", text):
            tokens.add(m.group())
        for m in re.finditer(r"[a-zA-Z_]\w+", text):
            tokens.add(m.group().lower())
        return tokens

    # ---------- 不动点判定（轻量） ----------
    def judge_fixed_point(self, text: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        三闸同判：
        1. 确认码/锚词闸
        2. 摇摆信号闸
        3. 排序锚点闸（简易版：护弱、人民优先）
        """
        text_lower = text.lower()
        context = context or {}

        score = 0.0
        reasons = []

        # 闸1：正向锚词
        for anchor in FIXED_POINT_ANCHORS:
            if anchor.lower() in text_lower:
                score += 0.35
                reasons.append(f"命中不动点锚词: {anchor}")
                break  # 只加一次

        # 闸2：负向摇摆信号
        for signal in PENDING_SIGNALS:
            if signal.lower() in text_lower:
                score -= 0.45
                reasons.append(f"发现摇摆信号: {signal}")
                break

        # 闸3：排序锚点（简易护弱/人民优先检测）
        if any(w in text for w in ["人民", "老百姓", "弱者", "护童", "公益"]):
            score += 0.20
            reasons.append("符合人民优先排序锚点")

        # 闸4：含确认码/TOKEN/DNA 高度稳定
        if re.search(r"#CONFIRM|DNA:|#龍芯", text):
            score += 0.35
            reasons.append("含高稳定性标记（确认码/DNA）")

        # 强制闸：隐私/法律红线不受得分影响
        if any(s in text for s in PRIVACY_SIGNALS):
            state = FixedPointState.BLACK
            reasons.append("命中隐私敏感信号，强制隔离")
        elif any(s in text for s in LEGAL_RED_SIGNALS):
            state = FixedPointState.RED
            reasons.append("命中法律红线信号，强制阻断")
        elif score >= 0.7:
            state = FixedPointState.GOLD
        elif score >= 0.3:
            state = FixedPointState.GREEN
        elif score < -0.2:
            state = FixedPointState.YELLOW
        else:
            state = FixedPointState.YELLOW

        return {
            "state": state.value,
            "score": round(score, 3),
            "reasons": reasons,
        }

    # ---------- 压缩（只在不动点调用） ----------
    @staticmethod
    def compress(text: str) -> Tuple[bytes, float]:
        """龍魂字典替换 + zlib，返回 (压缩字节, 压缩率)"""
        # 字典替换
        encoded = text
        for full, short in sorted(LONGHUN_DICT.items(), key=lambda x: -len(x[0])):
            encoded = encoded.replace(full, short)

        raw = text.encode("utf-8")
        compressed = zlib.compress(encoded.encode("utf-8"), level=6)
        ratio = len(compressed) / len(raw) if raw else 1.0
        return compressed, round(ratio, 3)

    @staticmethod
    def decompress(data: bytes) -> str:
        encoded = zlib.decompress(data).decode("utf-8")
        for full, short in sorted(LONGHUN_DICT.items(), key=lambda x: -len(x[1])):
            encoded = encoded.replace(short, full)
        return encoded

    # ---------- 核心：摄入记忆 ----------
    def ingest(self, text: str, source: str = "unknown", tags: Optional[List[str]] = None,
               context: Optional[Dict] = None) -> Dict[str, Any]:
        """摄入一条记忆，返回不动点判定与归档结果"""
        text_hash = self.sha256(text)
        text_simhash = self.simhash(text)
        timestamp = datetime.now(timezone.utc).isoformat()

        # 1. 近似去重：与已归档记忆的 SimHash 汉明距离 <= 3
        duplicate = self._find_duplicate(text_simhash)
        if duplicate:
            return {
                "status": "duplicate",
                "message": "近似重复，未归档",
                "reference": duplicate["id"],
                "hash": text_hash,
            }

        # 2. 不动点判定
        judgment = self.judge_fixed_point(text, context)
        state = FixedPointState(judgment["state"])

        entry = {
            "id": text_hash[:16],
            "hash": text_hash,
            "simhash": text_simhash,
            "source": source,
            "tags": tags or [],
            "timestamp": timestamp,
            "state": state.value,
            "score": judgment["score"],
            "reasons": judgment["reasons"],
            "text_preview": text[:200],
        }

        # 3. 只有不动点才归档 + 压缩
        if state in (FixedPointState.GOLD, FixedPointState.GREEN):
            raw_bytes = text.encode("utf-8")
            compressed, ratio = self.compress(text)

            # 短文本压缩可能膨胀，此时存原始文本
            if len(compressed) >= len(raw_bytes):
                archive_path = self.archive_dir / f"{entry['id']}.txt"
                archive_path.write_bytes(raw_bytes)
                ratio = 1.0
                bytes_saved = 0
            else:
                archive_path = self.archive_dir / f"{entry['id']}.fpz"
                archive_path.write_bytes(compressed)
                bytes_saved = len(raw_bytes) - len(compressed)

            entry["archive_path"] = str(archive_path.relative_to(self.archive_dir))
            entry["compressed_bytes"] = archive_path.stat().st_size
            entry["raw_bytes"] = len(raw_bytes)
            entry["compression_ratio"] = ratio
            entry["dna"] = self._generate_dna(entry["id"], text_hash)

            self._append_index(entry)
            self._update_stats(archived=1, bytes_saved=bytes_saved)
            return {"status": "archived", **entry}

        # 4. 非不动点分流：RED/BLACK 隔离，YELLOW 进缓冲池
        else:
            if state in (FixedPointState.RED, FixedPointState.BLACK):
                self._append_quarantine(entry)
                self._update_stats(quarantined=1)
                return {"status": "quarantined", **entry}
            else:
                self._append_buffer(entry)
                self._update_stats(pending=1)
                return {"status": "pending", **entry}

    def _find_duplicate(self, simhash: int, threshold: int = 3) -> Optional[Dict]:
        if not self.index_file.exists():
            return None
        with open(self.index_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if self.hamming_distance(simhash, entry.get("simhash", 0)) <= threshold:
                        return entry
                except json.JSONDecodeError:
                    continue
        return None

    def _append_index(self, entry: Dict):
        with open(self.index_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _append_buffer(self, entry: Dict):
        with open(self.buffer_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _append_quarantine(self, entry: Dict):
        with open(self.quarantine_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _generate_dna(self, short_id: str, text_hash: str) -> str:
        now = datetime.now(timezone.utc)
        return f"#龍芯⚡️{now.strftime('%Y-%m-%d')}-FP-MEMORY-{short_id}-{text_hash[:8]}"

    def _update_stats(self, archived: int = 0, pending: int = 0, quarantined: int = 0, bytes_saved: int = 0):
        stats = self._load_stats()
        stats["archived_count"] = stats.get("archived_count", 0) + archived
        stats["pending_count"] = stats.get("pending_count", 0) + pending
        stats["quarantined_count"] = stats.get("quarantined_count", 0) + quarantined
        stats["bytes_saved"] = stats.get("bytes_saved", 0) + bytes_saved
        stats["last_update"] = datetime.now(timezone.utc).isoformat()
        with open(self.stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)

    def _load_stats(self) -> Dict:
        if self.stats_file.exists():
            return json.loads(self.stats_file.read_text(encoding="utf-8"))
        return {"archived_count": 0, "pending_count": 0, "quarantined_count": 0, "bytes_saved": 0}

    # ---------- 查询 ----------
    def search(self, query: str, n: int = 5) -> List[Dict]:
        query_tokens = self._tokenize(query)
        results = []
        if not self.index_file.exists():
            return results
        with open(self.index_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    entry_tokens = set(entry.get("text_preview", ""))
                    score = len(query_tokens & entry_tokens)
                    if score > 0 or query.lower() in entry.get("text_preview", "").lower():
                        results.append((score, entry))
                except json.JSONDecodeError:
                    continue
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:n]]

    def status(self) -> Dict[str, Any]:
        stats = self._load_stats()
        archived = sum(1 for _ in self._iter_index())
        pending = sum(1 for _ in self._iter_buffer())
        quarantined = sum(1 for _ in self._iter_quarantine())
        return {
            "dna": self.DNA,
            "archive_dir": str(self.archive_dir),
            "archived": archived,
            "pending": pending,
            "quarantined": quarantined,
            "stats": stats,
        }

    def pending_list(self, n: int = 10) -> List[Dict]:
        items = list(self._iter_buffer())
        return items[-n:]

    def quarantine_list(self, n: int = 10) -> List[Dict]:
        items = list(self._iter_quarantine())
        return items[-n:]
        items = list(self._iter_buffer())
        return items[-n:]

    def _iter_index(self):
        if not self.index_file.exists():
            return
        with open(self.index_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue

    def _iter_buffer(self):
        if not self.buffer_file.exists():
            return
        with open(self.buffer_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue

    def _iter_quarantine(self):
        if not self.quarantine_file.exists():
            return
        with open(self.quarantine_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError:
                        continue


# ============================================================
# CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="龍魂 · 不动点记忆归档引擎")
    sub = parser.add_subparsers(dest="cmd")

    p_ingest = sub.add_parser("ingest", help="摄入一条记忆")
    p_ingest.add_argument("text", type=str, help="记忆文本")
    p_ingest.add_argument("--source", "-s", default="cli", help="来源")
    p_ingest.add_argument("--tags", "-t", default="", help="标签，逗号分隔")

    sub.add_parser("status", help="查看归档状态")
    sub.add_parser("pending", help="查看缓冲池")
    sub.add_parser("quarantine", help="查看隔离区")

    p_search = sub.add_parser("search", help="搜索归档")
    p_search.add_argument("query", type=str, help="查询词")
    p_search.add_argument("-n", type=int, default=5, help="返回数量")

    args = parser.parse_args()
    archive = MemoryArchive()

    if args.cmd == "ingest":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        result = archive.ingest(args.text, source=args.source, tags=tags)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == "status":
        print(json.dumps(archive.status(), ensure_ascii=False, indent=2))

    elif args.cmd == "pending":
        print(json.dumps(archive.pending_list(), ensure_ascii=False, indent=2))

    elif args.cmd == "quarantine":
        print(json.dumps(archive.quarantine_list(), ensure_ascii=False, indent=2))

    elif args.cmd == "search":
        print(json.dumps(archive.search(args.query, args.n), ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
