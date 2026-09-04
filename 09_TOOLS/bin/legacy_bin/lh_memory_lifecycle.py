#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# ═══════════════════════════════════════════
# 龍魂体系 | 记忆生命周期管理器 v1.0
# ═══════════════════════════════════════════
# DNA: #龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-MEMORY-LIFECYCLE-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: UID9622（诸葛鑫·Lucky）
# 三色审计: 🟢 通过
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 上游协议: 记忆永存与外脑压缩总协议 v1.0 · 第七章
# ═══════════════════════════════════════════
# 五态状态机: 热层→温层→冷层 ⇄ 封存 ⇄ ROM
# 用法:
#   python3 bin/lh_memory_lifecycle.py state <记忆ID>     # 查当前态
#   python3 bin/lh_memory_lifecycle.py transition <ID> <目标态> # 态变
#   python3 bin/lh_memory_lifecycle.py rollback <ID>      # 回滚
#   python3 bin/lh_memory_lifecycle.py snapshot <ID>      # 快照
#   python3 bin/lh_memory_lifecycle.py list [--tier=<层>]  # 列出
# ═══════════════════════════════════════════
"""

import json
import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ─── 项目路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = PROJECT_ROOT / "state" / "exobrain"
STATE_DIR.mkdir(parents=True, exist_ok=True)
LIFECYCLE_DB = STATE_DIR / "lifecycle_db.json"
SNAPSHOT_DIR = STATE_DIR / "snapshots"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


class 记忆态(str, Enum):
    """五态 + ROM（7.1）"""
    热层 = "热层"
    温层 = "温层"
    冷层 = "冷层"
    封存 = "封存"
    ROM = "ROM永久"


# 合法态变规则（单向为主，回滚为受控回路）
TRANSITIONS: Dict[记忆态, List[记忆态]] = {
    记忆态.热层: [记忆态.温层, 记忆态.封存, 记忆态.ROM],
    记忆态.温层: [记忆态.热层, 记忆态.冷层, 记忆态.封存],
    记忆态.冷层: [记忆态.温层, 记忆态.封存],
    记忆态.封存: [记忆态.热层, 记忆态.温层, 记忆态.冷层],  # 解封回原层
    记忆态.ROM: [],  # 只进不出，不可回滚
}

# 态变触发条件
TRANSITION_RULES = {
    ("热层", "温层"): lambda m: m.get("最近访问天数", 0) > 30,
    ("温层", "冷层"): lambda m: m.get("最近访问天数", 999) > 90 and m.get("I", 0) < 0.2,
    ("热层", "封存"): lambda m: m.get("违规", False) or m.get("涉敏", False),
    ("温层", "封存"): lambda m: m.get("违规", False) or m.get("涉敏", False),
    ("冷层", "封存"): lambda m: m.get("违规", False) or m.get("涉敏", False),
    ("热层", "ROM"): lambda m: m.get("不动点核", False) or m.get("用户焊死", False),
}


@dataclass
class 记忆单元:
    """外脑中的单个记忆对象"""
    id: str = ""
    标题: str = ""
    内容摘要: str = ""
    当前态: str = "热层"
    重要性I: float = 0.5
    创建时间: str = ""
    最后访问: str = ""
    最近访问天数: int = 0
    访问次数: int = 0
    违规: bool = False
    涉敏: bool = False
    不动点核: bool = False
    用户焊死: bool = False
    dna: str = ""
    历史态变: List[dict] = field(default_factory=list)
    快照代数: int = 0
    来源: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class 记忆生命周期管理器:
    """五态状态机 + 回滚机制 v1.0"""

    DNA = "#龍芯⚡️丙午·乙未·乙未·壬午·䷖剥-MEMORY-LIFECYCLE-v1.0"

    def __init__(self, state_dir: Path = None):
        self.state_dir = state_dir or STATE_DIR
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.db = self._load_db()

    def _load_db(self) -> Dict[str, dict]:
        if LIFECYCLE_DB.exists():
            return json.loads(LIFECYCLE_DB.read_text())
        return {}

    def _save_db(self):
        LIFECYCLE_DB.write_text(json.dumps(self.db, ensure_ascii=False, indent=2))

    def _生成DNA(self, action: str) -> str:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"#龍芯⚡️{ts}-LIFECYCLE-{action}-{hashlib.sha256(ts.encode()).hexdigest()[:8]}"

    # ═══════════════════════════════════════
    # 创建记忆单元
    # ═══════════════════════════════════════
    def 创建(self, 标题: str, 内容摘要: str = "", I: float = 0.5,
             来源: str = "", 不动点核: bool = False) -> dict[str, Any]:
        now = datetime.now().isoformat()
        mid = f"MEM-{int(time.time())}-{hashlib.sha256(f'{标题}{now}'.encode()).hexdigest()[:8]}"

        unit = 记忆单元(
            id=mid,
            标题=标题,
            内容摘要=内容摘要[:200],
            当前态="热层",
            重要性I=round(I, 3),
            创建时间=now,
            最后访问=now,
            最近访问天数=0,
            访问次数=1,
            不动点核=不动点核,
            dna=self._生成DNA("CREATE"),
            来源=来源,
        )

        if 不动点核:
            unit.当前态 = "ROM永久"

        self.db[mid] = unit.to_dict()
        self._save_db()
        return unit.to_dict()

    # ═══════════════════════════════════════
    # 查询当前态
    # ═══════════════════════════════════════
    def 查态(self, mid: str) -> dict[str, Any]:
        if mid not in self.db:
            return {"error": f"记忆不存在: {mid}", "level": "NOT_FOUND"}
        m = self.db[mid]
        天数 = (datetime.now() - datetime.fromisoformat(m["最后访问"])).days
        m["最近访问天数"] = 天数
        return m

    # ═══════════════════════════════════════
    # 态变 (7.1-7.2)
    # ═══════════════════════════════════════
    def 态变(self, mid: str, 目标态: str, 原因: str = "", 操作者: str = "system",
             skip_checks: bool = False) -> dict[str, Any]:
        """执行态变，写DNA审计日志"""
        if mid not in self.db:
            return {"error": f"记忆不存在: {mid}", "level": "NOT_FOUND"}

        m = self.db[mid]
        当前态 = 记忆态(m["当前态"])

        try:
            目标态_enum = 记忆态(目标态)
        except ValueError:
            return {"error": f"无效态: {目标态}", "valid": [t.value for t in 记忆态]}

        # ROM不可回滚
        if 当前态 == 记忆态.ROM:
            return {"error": "🔴 ROM态不可回滚/态变", "level": "REJECTED"}

        # 合法性检查
        if not skip_checks and 目标态_enum not in TRANSITIONS.get(当前态, []):
            return {
                "error": f"禁止的态变: {当前态.value} → {目标态}",
                "允许的态变": [t.value for t in TRANSITIONS.get(当前态, [])],
                "level": "REJECTED",
            }

        # 条件检查
        if not skip_checks:
            rule = TRANSITION_RULES.get((当前态.value, 目标态))
            if rule and not rule(m):
                return {
                    "error": f"态变条件不满足: {当前态.value} → {目标态}",
                    "level": "REJECTED",
                }

        # 执行态变
        旧态 = 当前态.value
        now = datetime.now().isoformat()
        dna = self._生成DNA(f"TRANSITION-{旧态}-{目标态}")

        履历 = {
            "时间": now,
            "从": 旧态,
            "到": 目标态,
            "原因": 原因,
            "操作者": 操作者,
            "dna": dna,
        }

        m["当前态"] = 目标态
        m.setdefault("历史态变", []).append(履历)
        m["dna"] = dna

        self.db[mid] = m
        self._save_db()

        return {
            "id": mid,
            "态变": f"{旧态} → {目标态}",
            "原因": 原因,
            "dna": dna,
            "状态": "🟢 完成",
        }

    # ═══════════════════════════════════════
    # 回滚 (7.4)
    # ═══════════════════════════════════════
    def 回滚(self, mid: str, 原因: str = "", 操作者: str = "UID9622",
             目标代: int = None) -> dict[str, Any]:
        """回滚到上一代快照"""
        if mid not in self.db:
            return {"error": f"记忆不存在: {mid}", "level": "NOT_FOUND"}

        m = self.db[mid]
        if 记忆态(m["当前态"]) == 记忆态.ROM:
            return {"error": "🔴 ROM态不可回滚", "level": "REJECTED"}

        # 找快照
        snap_files = sorted(SNAPSHOT_DIR.glob(f"{mid}_v*.json"))
        if not snap_files:
            return {"error": "无可回滚快照", "level": "NO_SNAPSHOT"}

        if 目标代 is not None:
            snap_files = [f for f in snap_files if f"_{mid}_v{目标代}" in str(f)]
        else:
            snap_files = [snap_files[-1]]  # 最新一代

        if not snap_files:
            return {"error": f"未找到目标快照 v{目标代}", "level": "NO_SNAPSHOT"}

        snap = json.loads(snap_files[0].read_text())

        旧态 = m["当前态"]
        now = datetime.now().isoformat()
        dna = self._生成DNA("ROLLBACK")

        # 恢复快照中的态
        m.update(snap.get("数据", {}))
        m["当前态"] = snap.get("数据", {}).get("当前态", 旧态)
        履历 = {
            "时间": now,
            "从": 旧态,
            "到": m["当前态"],
            "原因": f"回滚: {原因}",
            "操作者": 操作者,
            "dna": dna,
        }
        m.setdefault("历史态变", []).append(履历)
        m["dna"] = dna

        self.db[mid] = m
        self._save_db()

        return {
            "id": mid,
            "回滚到": snap_files[0].name,
            "态": m["当前态"],
            "原因": 原因,
            "dna": dna,
            "状态": "🟢 回滚完成",
        }

    # ═══════════════════════════════════════
    # 快照
    # ═══════════════════════════════════════
    def 快照(self, mid: str) -> dict[str, Any]:
        """创建当前态快照（保留≥10代）"""
        if mid not in self.db:
            return {"error": f"记忆不存在: {mid}", "level": "NOT_FOUND"}
        m = self.db[mid]
        m["快照代数"] = m.get("快照代数", 0) + 1

        快照名 = f"{mid}_v{m['快照代数']}.json"
        快照数据 = {
            "id": mid,
            "代数": m["快照代数"],
            "时间": datetime.now().isoformat(),
            "数据": dict(m),
            "dna": self._生成DNA("SNAPSHOT"),
        }

        (SNAPSHOT_DIR / 快照名).write_text(json.dumps(快照数据, ensure_ascii=False, indent=2))

        # 保留≥10代，清理更旧的
        all_snaps = sorted(SNAPSHOT_DIR.glob(f"{mid}_v*.json"))
        if len(all_snaps) > 15:
            for old in all_snaps[:-15]:
                old.unlink()

        self.db[mid] = m
        self._save_db()

        return {"id": mid, "快照": 快照名, "代数": m["快照代数"], "状态": "🟢 已快照"}

    # ═══════════════════════════════════════
    # 列表
    # ═══════════════════════════════════════
    def 列表(self, tier: str | None = None) -> List[dict]:
        items = list(self.db.values())
        if tier:
            items = [m for m in items if m.get("当前态") == tier]
        return sorted(items, key=lambda m: m.get("重要性I", 0), reverse=True)

    # ═══════════════════════════════════════
    # 访问（自动回热）
    # ═══════════════════════════════════════
    def 访问(self, mid: str) -> dict[str, Any]:
        if mid not in self.db:
            return {"error": f"记忆不存在: {mid}", "level": "NOT_FOUND"}
        m = self.db[mid]
        now = datetime.now().isoformat()

        m["最后访问"] = now
        m["访问次数"] = m.get("访问次数", 0) + 1
        m["最近访问天数"] = 0

        # 自动回热：冷/温层+被访问→热层
        if m["当前态"] in ("冷层", "温层"):
            return self.态变(mid, "热层", 原因="访问触发回热")

        self.db[mid] = m
        self._save_db()
        return m


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

def main():
    mgr = 记忆生命周期管理器()

    if len(sys.argv) < 2:
        print(__doc__)
        items = mgr.列表()
        print(f"\n📊 内存记忆: {len(items)} 条")
        for m in items[:10]:
            print(f"  [{m['当前态']}] {m['标题'][:40]} | I={m.get('重要性I',0):.2f}")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "state":
        mid = sys.argv[2] if len(sys.argv) > 2 else None
        if not mid:
            print("用法: python3 bin/lh_memory_lifecycle.py state <记忆ID>")
            sys.exit(1)
        result = mgr.查态(mid)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "transition":
        if len(sys.argv) < 4:
            print("用法: python3 bin/lh_memory_lifecycle.py transition <ID> <目标态> [原因]")
            sys.exit(1)
        mid, target = sys.argv[2], sys.argv[3]
        reason = sys.argv[4] if len(sys.argv) > 4 else ""
        result = mgr.态变(mid, target, 原因=reason)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "rollback":
        mid = sys.argv[2] if len(sys.argv) > 2 else None
        if not mid:
            print("用法: python3 bin/lh_memory_lifecycle.py rollback <ID> [原因]")
            sys.exit(1)
        reason = sys.argv[3] if len(sys.argv) > 3 else ""
        目标代 = int(sys.argv[4]) if len(sys.argv) > 4 else None
        result = mgr.回滚(mid, 原因=reason, 目标代=目标代)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "snapshot":
        mid = sys.argv[2] if len(sys.argv) > 2 else None
        if not mid:
            print("用法: python3 bin/lh_memory_lifecycle.py snapshot <ID>")
            sys.exit(1)
        result = mgr.快照(mid)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif cmd == "list":
        tier = None
        for a in sys.argv[2:]:
            if a.startswith("--tier="):
                tier = a.split("=")[1]
        items = mgr.列表(tier=tier)
        print(f"📊 记忆列表 ({len(items)}条)")
        for m in items:
            print(f"  [{m['当前态']}] {m['标题'][:50]} | I={m.get('重要性I',0):.2f} | 访问{m.get('访问次数',0)}次")

    elif cmd == "create":
        if len(sys.argv) < 3:
            print("用法: python3 bin/lh_memory_lifecycle.py create <标题> [摘要] [I值]")
            sys.exit(1)
        title = sys.argv[2]
        summary = sys.argv[3] if len(sys.argv) > 3 else ""
        I = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        result = mgr.创建(title, summary, I=I)
        print(f"✅ 创建: {result['id']}")

    elif cmd == "access":
        mid = sys.argv[2] if len(sys.argv) > 2 else None
        if not mid:
            print("用法: python3 bin/lh_memory_lifecycle.py access <ID>")
            sys.exit(1)
        result = mgr.访问(mid)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
