#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 年轮哈希链 v1.1（审查修正版）
DNA: #龍芯⚡️丙午·丙申·丙辰·甲午·䷁坤-YEAR-RING-CHAIN-V1.1-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰

修正清单（相对原始稿）:
  ① 干支口径统一 —— 弃用仅年干支的简易算法，改用与 ganzhi_dna_engine.py
     一致的四柱算法（年/月/日/时），全网只认一个口径
  ② DNA 干支 壬寅→丙辰（万年历口径v3.0，禁止手写）
  ③ event_id 的 md5 改为 sha256（统一哈希族）
  ④ verify_chain 的 verbose 判定逻辑修正（prev_hash 更新前判定）
  ⑤ 存储路径支持环境变量 LONGHUN_YEARRING_DIR 覆盖，
     /opt 不可写时自动降级到 ./yearring（开发机/Mac 可跑）
  ⑥ 空圈占位事件 DNA 格式对齐 v∞ 规范

功能:
- 每日一圈，UTC+8 0点封圈
- 圈内存储当天所有事件摘要哈希（简化Merkle根）
- 哈希链式结构：前一圈哈希 + 当天日期 + 事件根哈希 + 天干地支
- 验证方式：从头跑，任意圈对不上→整条链失效
- 存储位置: $LONGHUN_YEARRING_DIR 或 /opt/longhun/data/yearring/
"""

import os
import json
import hashlib
import time
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import argparse
import sys


# ============================================================
# 天干地支基表 · L0 不可变（与 ganzhi_dna_engine.py 同口径）
# ============================================================

十天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
十二地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
十二时辰 = ["子时", "丑时", "寅时", "卯时", "辰时", "巳时",
            "午时", "未时", "申时", "酉时", "戌时", "亥时"]


def _年干支(year: int) -> str:
    base = year - 4  # 公元4年为甲子年
    return 十天干[base % 10] + 十二地支[base % 12]


def _月干支(year: int, month: int) -> str:
    """年上起月法（五虎遁），阳历月近似"""
    月支映射 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0]
    月支_idx = 月支映射[month - 1]
    年干 = 十天干.index(_年干支(year)[0])
    寅月干映射 = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0]
    寅月干 = 寅月干映射[年干]
    offset = (月支_idx - 2) % 12
    return 十天干[(寅月干 + offset) % 10] + 十二地支[月支_idx]


def _日干支(year: int, month: int, day: int) -> str:
    yy = year % 100
    base = (yy + 7) * 5 + 15 + (yy + 19) // 4
    base %= 60
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    月天数 = [31, 29 if is_leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day_of_year = sum(月天数[:month - 1]) + day
    seq = (base + day_of_year) % 60
    return 十天干[(seq - 1) % 10] + 十二地支[(seq - 1) % 12]


def _时辰(hour: int) -> str:
    return 十二时辰[((hour + 1) // 2) % 12]


def 四柱干支(dt: datetime) -> str:
    """统一口径：年·月·日·时 四柱（与 ganzhi_dna_engine.py 一致）"""
    return f"{_年干支(dt.year)}·{_月干支(dt.year, dt.month)}·{_日干支(dt.year, dt.month, dt.day)}·{_时辰(dt.hour)}"


def get_ganzhi(dt: datetime) -> str:
    """对外接口：返回四柱干支串（保持原函数名兼容）"""
    return 四柱干支(dt)


# ============================================================
# 年轮数据结构
# ============================================================

@dataclass
class Ring:
    """单个年轮圈"""
    date: str                      # 日期 YYYY-MM-DD
    ganzhi: str                    # 四柱干支（统一口径）
    prev_hash: str                 # 前一圈的哈希
    events_root_hash: str          # 当天所有事件的根哈希（Merkle根）
    event_count: int               # 当天事件数量
    created_at: str                # 创建时间 ISO
    hash: str = ""                 # 本圈哈希
    signature: str = ""            # GPG签名(可选)

    def compute_hash(self) -> str:
        content = f"{self.date}{self.ganzhi}{self.prev_hash}{self.events_root_hash}{self.event_count}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class RingEvent:
    """年轮事件（圈内记录）"""
    event_id: str
    timestamp: str
    event_type: str                # dna_generate | timestamp | log | audit | empty
    data_hash: str
    dna: str


# ============================================================
# 年轮哈希链引擎
# ============================================================

class YearRingChain:
    """年轮哈希链引擎"""

    DEFAULT_STORAGE = "/opt/longhun/data/yearring/"
    CHAIN_FILE = "chain.json"
    EVENTS_DIR = "events/"

    def __init__(self, storage_path: Optional[str] = None):
        # ⑤ 路径优先级：参数 > 环境变量 > /opt（不可写则降级 ./yearring）
        if storage_path:
            base = Path(storage_path)
        elif os.environ.get("LONGHUN_YEARRING_DIR"):
            base = Path(os.environ["LONGHUN_YEARRING_DIR"])
        else:
            base = Path(self.DEFAULT_STORAGE)
            try:
                base.mkdir(parents=True, exist_ok=True)
                probe = base / ".probe"
                probe.touch()
                probe.unlink()
            except (PermissionError, OSError):
                base = Path("./yearring")
        self.storage_path = base
        self.chain_file = self.storage_path / self.CHAIN_FILE
        self.events_dir = self.storage_path / self.EVENTS_DIR
        self._ensure_storage()
        self._chain: List[Ring] = []
        self._load_chain()

    def _ensure_storage(self):
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.events_dir.mkdir(parents=True, exist_ok=True)

    def _load_chain(self):
        if self.chain_file.exists():
            with open(self.chain_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._chain = [Ring(**r) for r in data.get('rings', [])]
        else:
            self._chain = []

    def _save_chain(self):
        data = {
            'version': '1.1',
            'created_at': datetime.now().isoformat(),
            'ring_count': len(self._chain),
            'rings': [r.__dict__ for r in self._chain]
        }
        with open(self.chain_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _get_today(self) -> str:
        tz = timezone(timedelta(hours=8))
        return datetime.now(tz).strftime("%Y-%m-%d")

    def _compute_events_root_hash(self, events: List[RingEvent]) -> str:
        if not events:
            return hashlib.sha256(b"empty").hexdigest()[:16]
        combined = "".join([e.data_hash for e in events])
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def _get_prev_hash(self) -> str:
        if not self._chain:
            return "0" * 16  # 创世圈
        return self._chain[-1].hash

    def _get_events_for_date(self, date: str) -> List[RingEvent]:
        events_file = self.events_dir / f"{date}.json"
        if not events_file.exists():
            return []
        with open(events_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [RingEvent(**e) for e in data.get('events', [])]

    def _save_events(self, date: str, events: List[RingEvent]):
        events_file = self.events_dir / f"{date}.json"
        data = {
            'date': date,
            'event_count': len(events),
            'events': [e.__dict__ for e in events]
        }
        with open(events_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_event(self, event_type: str, data: Dict) -> Tuple[RingEvent, Ring]:
        tz = timezone(timedelta(hours=8))
        now = datetime.now(tz)
        today = now.strftime("%Y-%m-%d")
        ganzhi = get_ganzhi(now)

        # ③ event_id 统一 sha256
        id_src = f"{now.isoformat()}|{json.dumps(data, sort_keys=True, ensure_ascii=False)}"
        event_id = f"EVT-{now.strftime('%Y%m%d%H%M%S')}-{hashlib.sha256(id_src.encode()).hexdigest()[:6]}"
        event = RingEvent(
            event_id=event_id,
            timestamp=now.isoformat(),
            event_type=event_type,
            data_hash=hashlib.sha256(
                json.dumps(data, sort_keys=True, ensure_ascii=False).encode()
            ).hexdigest()[:16],
            dna=data.get('dna', f"#龍芯⚡️{ganzhi}-EVENT-{event_id[-6:]}-UID9622")
        )

        events = self._get_events_for_date(today)
        events.append(event)
        self._save_events(today, events)

        if not self._chain or self._chain[-1].date != today:
            ring = self._create_ring_for_date(today, events)
            self._chain.append(ring)
            self._save_chain()
            return event, ring

        # 更新今天的圈（事件根哈希变化；圈在封圈前可更新，封圈后不再变）
        ring = self._chain[-1]
        ring.events_root_hash = self._compute_events_root_hash(events)
        ring.event_count = len(events)
        ring.hash = ring.compute_hash()
        self._save_chain()
        return event, ring

    def _create_ring_for_date(self, date: str, events: List[RingEvent]) -> Ring:
        prev_hash = self._get_prev_hash()
        ganzhi = get_ganzhi(datetime.strptime(date, "%Y-%m-%d"))
        ring = Ring(
            date=date,
            ganzhi=ganzhi,
            prev_hash=prev_hash,
            events_root_hash=self._compute_events_root_hash(events),
            event_count=len(events),
            created_at=datetime.now().isoformat()
        )
        ring.hash = ring.compute_hash()
        return ring

    def close_today(self) -> Optional[Ring]:
        tz = timezone(timedelta(hours=8))
        now = datetime.now(tz)
        today = now.strftime("%Y-%m-%d")

        if self._chain and self._chain[-1].date == today:
            return self._chain[-1]

        events = self._get_events_for_date(today)
        if not events:
            empty_event = RingEvent(
                event_id=f"EMPTY-{today}",
                timestamp=f"{today}T00:00:00+08:00",
                event_type="empty",
                data_hash=hashlib.sha256(b"empty").hexdigest()[:16],
                dna=f"#龍芯⚡️{get_ganzhi(now)}-EMPTY-{today}-UID9622"
            )
            events.append(empty_event)
            self._save_events(today, events)

        ring = self._create_ring_for_date(today, events)
        self._chain.append(ring)
        self._save_chain()
        return ring

    def verify_chain(self, verbose: bool = False) -> Tuple[bool, List[str]]:
        errors = []
        if not self._chain:
            return False, ["链为空"]

        prev_hash = "0" * 16
        for i, ring in enumerate(self._chain):
            computed = ring.compute_hash()
            prev_ok = (ring.prev_hash == prev_hash)
            hash_ok = (ring.hash == computed)

            if not prev_ok:
                errors.append(f"圈 {i} ({ring.date}): prev_hash 不匹配 (期望 {prev_hash}, 实际 {ring.prev_hash})")
            if not hash_ok:
                errors.append(f"圈 {i} ({ring.date}): hash 不匹配 (计算值 {computed}, 存储值 {ring.hash})")

            events = self._get_events_for_date(ring.date)
            computed_root = self._compute_events_root_hash(events)
            if ring.events_root_hash != computed_root:
                errors.append(f"圈 {i} ({ring.date}): events_root_hash 不匹配")

            if verbose:
                status = "✅" if (prev_ok and hash_ok) else "❌"  # ④ 修正：更新 prev_hash 前判定
                print(f"  {status} {ring.date} | {ring.ganzhi} | hash: {ring.hash}")

            prev_hash = ring.hash

        return len(errors) == 0, errors

    def get_ring_by_date(self, date: str) -> Optional[Ring]:
        for ring in self._chain:
            if ring.date == date:
                return ring
        return None

    def get_events_by_date(self, date: str) -> List[RingEvent]:
        return self._get_events_for_date(date)

    def get_stats(self) -> Dict:
        tz = timezone(timedelta(hours=8))
        now = datetime.now(tz)
        return {
            'total_rings': len(self._chain),
            'start_date': self._chain[0].date if self._chain else None,
            'end_date': self._chain[-1].date if self._chain else None,
            'current_date': now.strftime("%Y-%m-%d"),
            'current_ganzhi': get_ganzhi(now),
            'is_today_closed': bool(self._chain) and self._chain[-1].date == now.strftime("%Y-%m-%d"),
            'storage_path': str(self.storage_path),
        }

    def export_chain(self, format: str = 'json') -> str:
        if format == 'json':
            data = {
                'version': '1.1',
                'total_rings': len(self._chain),
                'rings': [r.__dict__ for r in self._chain]
            }
            return json.dumps(data, ensure_ascii=False, indent=2)
        elif format == 'dot':
            lines = ["digraph YearRingChain {",
                     "  rankdir=LR;",
                     "  node [shape=box, style=filled, fillcolor=lightyellow];"]
            for i, ring in enumerate(self._chain):
                label = f"{ring.date}\\n{ring.ganzhi}\\n{ring.hash[:8]}"
                lines.append(f'  ring_{i} [label="{label}"];')
                if i > 0:
                    lines.append(f'  ring_{i-1} -> ring_{i} [label="hash"];')
            lines.append("}")
            return "\n".join(lines)
        return ""


# ============================================================
# 命令行工具
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 年轮哈希链 v1.1（审查修正版）",
        epilog="DNA: #龍芯⚡️丙午·丙申·丙辰·甲午·䷁坤-YEAR-RING-CHAIN-V1.1-UID9622"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    p_event = subparsers.add_parser("add", help="添加事件")
    p_event.add_argument("--type", required=True, help="事件类型")
    p_event.add_argument("--data", required=True, help="事件数据(JSON格式)")

    subparsers.add_parser("close", help="封圈")

    p_verify = subparsers.add_parser("verify", help="验证链完整性")
    p_verify.add_argument("--verbose", "-v", action="store_true", help="详细输出")

    subparsers.add_parser("stats", help="查看统计信息")

    p_export = subparsers.add_parser("export", help="导出链数据")
    p_export.add_argument("--format", "-f", default="json", choices=["json", "dot"])

    subparsers.add_parser("list", help="列出所有圈")

    p_get = subparsers.add_parser("get", help="查询圈")
    p_get.add_argument("date", help="日期 YYYY-MM-DD")

    args = parser.parse_args()
    engine = YearRingChain()

    if args.command == "add":
        data = json.loads(args.data)
        event, ring = engine.add_event(args.type, data)
        print(f"✅ 事件已添加: {event.event_id}")
        print(f"   圈: {ring.date} | {ring.ganzhi} | hash: {ring.hash}")
        print(f"   DNA: {event.dna}")

    elif args.command == "close":
        ring = engine.close_today()
        print(f"✅ 封圈完成: {ring.date} | {ring.ganzhi} | hash: {ring.hash}")

    elif args.command == "verify":
        valid, errors = engine.verify_chain(args.verbose)
        if valid:
            print("✅ 链验证通过")
        else:
            print("❌ 链验证失败:")
            for err in errors:
                print(f"  - {err}")
        sys.exit(0 if valid else 1)

    elif args.command == "stats":
        stats = engine.get_stats()
        print("📊 年轮统计")
        print("=" * 40)
        for k, v in stats.items():
            print(f"  {k}: {v}")

    elif args.command == "export":
        print(engine.export_chain(args.format))

    elif args.command == "list":
        for ring in engine._chain:
            print(f"  {ring.date} | {ring.ganzhi} | {ring.hash} | {ring.event_count} events")

    elif args.command == "get":
        ring = engine.get_ring_by_date(args.date)
        if ring:
            print(f"📅 {ring.date} | {ring.ganzhi}")
            print(f"  prev_hash: {ring.prev_hash}")
            print(f"  hash: {ring.hash}")
            print(f"  events_root_hash: {ring.events_root_hash}")
            print(f"  event_count: {ring.event_count}")
            print(f"  created_at: {ring.created_at}")
            events = engine.get_events_by_date(args.date)
            print(f"  事件列表:")
            for e in events[:10]:
                print(f"    - {e.event_id} | {e.event_type} | {e.dna}")
            if len(events) > 10:
                print(f"    ... 还有 {len(events) - 10} 条")
        else:
            print(f"❌ 未找到 {args.date} 的圈")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
