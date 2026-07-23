#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人民主权守护 / LongHun People's Sovereignty Guard

DNA:#龍芯⚡️2026-06-21-PEOPLE-SOVEREIGNTY-GUARD-v2.0

设计思想：
  ① 主权在人民，不在平台。
  ② UID9622 是创始人、守灯人，不是皇帝。
  ③ 熟悉场域自动认，陌生场域只守望、不拒绝。
  ④ 坏人处理，好人放行，不把人一竿子拍死。
  ⑤ 技术不是特权，是服务人民的器。

使用极简：
  - 你说，系统听。
  - 你去哪，说一声，系统随行。
  - 核心宪法改动只问一句："UID9622，确认吗？"
"""

import os
import re
import json
from enum import Enum
from dataclasses import dataclass, field, replace
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime
from pathlib import Path

# 人民行为引擎集成
try:
    from people_behavior_engine import PeopleBehaviorEngine, PersonProfile
    HAS_BEHAVIOR_ENGINE = True
except ImportError:
    HAS_BEHAVIOR_ENGINE = False


DNA_RE = re.compile(r'#龍芯[\u26a1\ufe0f]*(\d{4}-\d{2}-\d{2})-(.+?)-v([\d.]+)')

LAYER_NAMES = {
    "L0_ETERNAL": "永恒宪法",
    "L1_SEASONAL": "季节骨架",
    "L2_DECISION": "决策流场",
    "L3_GENERATIONAL": "生成功能",
    "L4_INSTANT": "瞬时报告",
}


class Verdict(str, Enum):
    """三句话判定"""
    ALLOW = "🟢 通过"
    ASK = "🟡 请确认"
    WATCH = "🟠 守望中"
    BLOCK_PLATFORM = "🔴 平台越权"


@dataclass
class Context:
    """人民请求时的场域上下文"""
    who: str = "anonymous"          # 谁
    device: Optional[str] = None    # 设备指纹
    network: Optional[str] = None   # WiFi/热点名
    ip: Optional[str] = None        # IP
    where: Optional[str] = None     # 在哪（瑞安老家 / 北京 / 机场等）
    said_where: Optional[str] = None  # 用户提前报备的行程
    is_founder: bool = False        # 是否是 UID9622
    is_known_person: bool = False   # 是否是已识别的人民
    is_platform: bool = False       # 是否是商户/APP/服务商


@dataclass
class DNAEntry:
    file: str
    dna: str
    date: str
    module: str
    version: str
    valid: bool
    layer: str
    status: str
    priority: int
    weight: float
    size: int
    mtime: float


class PeopleSovereigntyGuard:
    """
    人民主权守护。

    对外只有三句话：
      - "过"（🟢）
      - "请确认"（🟡）
      - "守望中，已记录"（🟠）
      - "平台越权，拒绝"（🔴）
    """

    FOUNDER_UID = {"UID9622", "9622", "诸葛鑫", "龍芯北辰"}
    FAMILIAR_NETWORKS = {"瑞安老家", "ruian-home", "LONGHUN-HOTSPOT", "iPhone(9622)"}
    FAMILIAR_IP_PREFIXES = {"192.168.", "127.0.0.1", "::1"}

    def __init__(self, registry_path: Optional[str] = None):
        self.registry_path = registry_path or self._default_registry_path()
        self.trip_path = self._default_trip_path()
        self.entries: Dict[str, DNAEntry] = {}
        self.dna_index: Dict[str, DNAEntry] = {}
        self.known_people: Set[str] = set()
        self.founder_trips: Dict[str, str] = {}  # where -> 报备时间
        self.ready = False
        self.load()

    @staticmethod
    def _default_registry_path() -> str:
        home = os.path.expanduser("~")
        return os.path.join(
            home, "longhun-system", ".longhun", "dna-audit", "dna_registry.json"
        )

    @staticmethod
    def _default_trip_path() -> str:
        home = os.path.expanduser("~")
        return os.path.join(
            home, "longhun-system", ".longhun", "founder_trips.json"
        )

    def load(self) -> Tuple[bool, str]:
        if not os.path.exists(self.registry_path):
            return False, f"注册表不存在: {self.registry_path}"
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for raw in data.get("entries", []):
                entry = DNAEntry(**raw)
                self.entries[entry.file] = entry
                if entry.dna:
                    self.dna_index[entry.dna] = entry
            self._load_trips()
            self.ready = True
            return True, f"已守护 {len(self.entries)} 个文件"
        except Exception as e:
            return False, f"加载失败: {e}"

    def _load_trips(self):
        if os.path.exists(self.trip_path):
            try:
                with open(self.trip_path, 'r', encoding='utf-8') as f:
                    self.founder_trips = json.load(f)
            except Exception:
                self.founder_trips = {}

    def _save_trips(self):
        os.makedirs(os.path.dirname(self.trip_path), exist_ok=True)
        with open(self.trip_path, 'w', encoding='utf-8') as f:
            json.dump(self.founder_trips, f, ensure_ascii=False, indent=2)

    # ═════════════════════════════════════════════════════════
    # 识主：你是谁？
    # ═════════════════════════════════════════════════════════

    def recognize(self, ctx: Context) -> Tuple[str, Dict[str, Any]]:
        """
        识主 + 识场域。
        返回 (场景标签, 详情)
        """
        detail = {
            "who": ctx.who,
            "device": ctx.device,
            "network": ctx.network,
            "ip": ctx.ip,
            "where": ctx.where,
        }

        if ctx.who in self.FOUNDER_UID:
            ctx.is_founder = True

        if ctx.is_platform:
            return "平台", detail

        if ctx.is_founder:
            # 创始人：熟悉场域直接过，陌生场域守望
            if self._is_familiar(ctx):
                return "创始人在熟悉场域", detail
            if ctx.where and ctx.where == ctx.said_where:
                return "创始人已报备行程", detail
            return "创始人在陌生场域", detail

        if ctx.is_known_person:
            return "已知人民", detail

        return "未知人民", detail

    def _is_familiar(self, ctx: Context) -> bool:
        """是否熟悉场域"""
        if ctx.network and any(k in ctx.network for k in self.FAMILIAR_NETWORKS):
            return True
        if ctx.ip:
            for prefix in self.FAMILIAR_IP_PREFIXES:
                if ctx.ip.startswith(prefix):
                    return True
        if ctx.where and any(k in ctx.where for k in ("瑞安", "老家", "home")):
            return True
        return False

    # ═════════════════════════════════════════════════════════
    # 三句话门控
    # ═════════════════════════════════════════════════════════

    def check(
        self,
        ctx: Context,
        file_or_dna: Optional[str] = None,
        intent: str = "read",
    ) -> Tuple[Verdict, str, Dict[str, Any]]:
        """
        人民主权门控。

        返回: (判定, 原因, 详情)
        """
        scene, detail = self.recognize(ctx)
        detail["scene"] = scene
        detail["intent"] = intent

        # 平台没有主权，永远拒绝直接访问核心
        if ctx.is_platform:
            if intent in ("write", "execute", "admin"):
                return Verdict.BLOCK_PLATFORM, "平台不是人民，没有主权，不能改核心", detail

        # 创始人
        if ctx.is_founder:
            return self._founder_check(ctx, file_or_dna, intent, detail)

        # 已知人民
        if ctx.is_known_person:
            return self._people_check(ctx, file_or_dna, intent, detail)

        # 未知人民：可读、可问，写核心要确认
        return self._unknown_check(ctx, file_or_dna, intent, detail)

    def _founder_check(
        self, ctx: Context, file_or_dna: str, intent: str, detail: Dict
    ) -> Tuple[Verdict, str, Dict]:
        """创始人判定：信任最大，但改宪法要确认"""
        entry = self.lookup(file_or_dna) if file_or_dna else None
        layer = entry.layer if entry else "L3_GENERATIONAL"

        if layer == "L0_ETERNAL" and intent in ("write", "execute", "admin"):
            return Verdict.ASK, "UID9622，你要动永恒宪法，请确认", detail

        is_traveling_with_notice = ctx.where and ctx.where == ctx.said_where
        if not self._is_familiar(ctx) and not is_traveling_with_notice and intent in ("write", "execute", "admin"):
            # 陌生场域只守望，不拒绝，但留痕
            return Verdict.WATCH, f"UID9622 在陌生场域执行 {intent}，已记录", detail

        return Verdict.ALLOW, f"UID9622 {intent} 通过", detail

    def _people_check(
        self, ctx: Context, file_or_dna: str, intent: str, detail: Dict
    ) -> Tuple[Verdict, str, Dict]:
        """已知人民：读自由，写/执行 L0-L2 要确认"""
        entry = self.lookup(file_or_dna) if file_or_dna else None
        layer = entry.layer if entry else "L3_GENERATIONAL"

        if intent == "read":
            return Verdict.ALLOW, "人民读取，通过", detail

        if layer in ("L0_ETERNAL", "L1_SEASONAL", "L2_DECISION") and intent in ("write", "execute"):
            return Verdict.ASK, f"人民要改 {LAYER_NAMES.get(layer, layer)}，请 UID9622 或本人确认", detail

        return Verdict.ALLOW, f"人民 {intent} 通过", detail

    def _unknown_check(
        self, ctx: Context, file_or_dna: str, intent: str, detail: Dict
    ) -> Tuple[Verdict, str, Dict]:
        """未知人民：不拒绝，只守望和确认"""
        entry = self.lookup(file_or_dna) if file_or_dna else None
        layer = entry.layer if entry else "L3_GENERATIONAL"

        if intent == "read":
            return Verdict.ALLOW, "未知人民读取，通过并记录", detail

        if layer in ("L0_ETERNAL", "L1_SEASONAL"):
            return Verdict.BLOCK_PLATFORM, "陌生身份不能动永恒宪法和季节骨架", detail

        return Verdict.ASK, "陌生人民，请确认身份", detail

    # ═════════════════════════════════════════════════════════
    # 创始人行程
    # ═════════════════════════════════════════════════════════

    def founder_going_to(self, where: str) -> str:
        """创始人报备行程"""
        self.founder_trips[where] = datetime.now().isoformat()
        self._save_trips()
        return f"已记录：UID9622 将前往 {where}，系统随行守望"

    def add_known_person(self, uid: str) -> str:
        """添加已知人民"""
        self.known_people.add(uid)
        return f"已识别人民: {uid}"

    # ═════════════════════════════════════════════════════════
    # 查询
    # ═════════════════════════════════════════════════════════

    def lookup(self, key: str) -> Optional[DNAEntry]:
        if not key:
            return None
        if key.startswith("#龍芯"):
            return self.dna_index.get(key)
        return self.lookup_by_file(key)

    def lookup_by_dna(self, dna: str) -> Optional[DNAEntry]:
        return self.dna_index.get(dna)

    def lookup_by_file(self, path: str) -> Optional[DNAEntry]:
        rel = str(path).replace(os.path.expanduser("~") + "/", "")
        if rel in self.entries:
            return self.entries[rel]
        base = os.path.basename(path)
        for e in self.entries.values():
            if e.file.endswith(base) or e.file == base:
                return e
        return None

    def lock_level(self, entry: DNAEntry):
        """兼容旧调用：返回简化的锁等级对象"""
        class _Lock:
            def __init__(self, v): self.value = v
        if entry.layer == "L0_ETERNAL":
            return _Lock("⚫")
        return _Lock("🟠")

    def personalized_message(
        self,
        ctx: Context,
        verdict: Verdict,
        reason: str,
    ) -> str:
        """
        结合人民行为引擎，用这个人最能听懂的话解释判定。
        不装大神，像邻居一样说话。
        """
        if not HAS_BEHAVIOR_ENGINE:
            return reason

        try:
            engine = PeopleBehaviorEngine()
            profile = engine.load_profile(ctx.who)
            if not profile:
                return reason

            lang = engine.assess(profile).get("language", "")
            if "做" in lang:
                return f"{reason}。你先动手试一小步，有问题再叫我。"
            if "听" in lang:
                return f"{reason}。我慢慢跟你说，不着急。"
            if "看" in lang:
                return f"{reason}。我给你画清楚，一眼就能看明白。"
            if "问" in lang:
                return f"{reason}。你先想想哪里不清楚，我们再聊。"
        except Exception:
            pass
        return reason

    def stats(self) -> Dict[str, Any]:
        return {
            "ready": self.ready,
            "files": len(self.entries),
            "known_people": len(self.known_people),
            "founder_trips": len(self.founder_trips),
        }


# ═══════════════════════════════════════════════════════════════
# 全局单例
# ═══════════════════════════════════════════════════════════════

_GUARD: Optional[PeopleSovereigntyGuard] = None


def get_guard() -> PeopleSovereigntyGuard:
    global _GUARD
    if _GUARD is None:
        _GUARD = PeopleSovereigntyGuard()
    return _GUARD


if __name__ == "__main__":
    print("🐉 龍魂人民主权守护 · 自检")
    guard = get_guard()
    print(guard.stats())

    founder = Context(who="UID9622", network="瑞安老家", ip="192.168.1.5")
    guest = Context(who="GUEST", network="机场 WiFi", ip="10.0.0.1")
    platform = Context(who="某APP", is_platform=True)

    print("\n创始人读宪法:", guard.check(founder, "cnsh-core/constitution/longhun_foundation_config.py", "read"))
    print("创始人写宪法:", guard.check(founder, "cnsh-core/constitution/longhun_foundation_config.py", "write"))
    print("创始人机场写:", guard.check(replace(guest, who="UID9622"), "ops-console/index.html", "write"))
    print("平台写核心:", guard.check(platform, "cnsh-core/constitution/longhun_foundation_config.py", "write"))

    print("\n" + guard.founder_going_to("北京"))
    print(guard.check(Context(who="UID9622", where="北京", said_where="北京"), "ops-console/index.html", "write"))

    print("\n✅ 自检完成")
