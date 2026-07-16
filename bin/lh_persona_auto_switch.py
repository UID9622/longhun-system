#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 人格矩阵自动切换引擎 v2.0 (Persona Auto-Switch Engine)
==================================================================
五维人格关键词自动触发 — 不再需要手动确认码，系统自动识别语境切换。

五维人格：
  军事(MILITARY)  — 决策果断，执行优先，低算力不废话
  历史(HISTORY)    — 以史为鉴，因果推演，引用先例验证
  哲学(PHILOSOPHY) — 底层逻辑，第一性原理，系统自洽
  经济(ECONOMY)    — 成本收益分析，ROI导向，效率优先
  政治(POLITICS)   — 多方博弈视角，利益权衡，规则框架

切换规则：
  1. 关键词权重计算 → 最高分人格
  2. 连续3次同一人格 → 锁定30分钟
  3. 冲突指令 → 军事优先（安全兜底）
  4. 切换事件 → 发布到EventBus + 审计日志

集成：
  - 对接 16人格矩阵 (personas/ + bin/personas/)
  - 对接 lh_event_bus_engine.EventBus
  - 对接 lh_persona_orchestrator (任务分发)

DNA: #龍芯⚡️丙午·辛未·丙戌·亥时·需-PERSONA-AUTO-SWITCH-v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── 项目根 ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from bin.lh_event_bus_engine import EventBus, EventType, Event  # noqa: E402

# ── 常量 ──
DNA = "#龍芯⚡️丙午·辛未·丙戌·亥时·需-PERSONA-AUTO-SWITCH-v2.0"
VERSION = "2.0.0"
SWITCH_DIR = PROJECT_ROOT / "data" / "persona_switch"
SWITCH_DIR.mkdir(parents=True, exist_ok=True)
SWITCH_LOG_FILE = SWITCH_DIR / "switch_log.jsonl"
STATE_FILE = SWITCH_DIR / "persona_state.json"


# ═══════════════════════════════════════════════════════════
# 五维人格
# ═══════════════════════════════════════════════════════════

class PersonaDimension(Enum):
    MILITARY = "military"       # 军事
    HISTORY = "history"         # 历史
    PHILOSOPHY = "philosophy"   # 哲学
    ECONOMY = "economy"         # 经济
    POLITICS = "politics"       # 政治


@dataclass
class PersonaProfile:
    """人格档案"""
    dimension: PersonaDimension
    name: str
    icon: str
    weight: float                           # 基础权重 0-1
    keywords: List[str]                     # 触发关键词
    anti_keywords: List[str] = field(default_factory=list)  # 抑制关键词
    style: str = ""                         # 响应风格
    default_persona_id: str = ""            # 对应16人格矩阵中的默认人格ID

    def match_score(self, text: str) -> float:
        """计算匹配分数 = 匹配关键词数 × 权重 - 抑制关键词命中惩罚"""
        text_lower = text.lower()
        keyword_hits = sum(1 for kw in self.keywords if kw.lower() in text_lower)
        anti_hits = sum(1 for ak in self.anti_keywords if ak.lower() in text_lower)
        if anti_hits > 0:
            return 0.0  # 抑制关键词命中则直接归零
        return keyword_hits * self.weight


# ═══════════════════════════════════════════════════════════
# 五维人格定义
# ═══════════════════════════════════════════════════════════

PERSONA_PROFILES: Dict[PersonaDimension, PersonaProfile] = {
    PersonaDimension.MILITARY: PersonaProfile(
        dimension=PersonaDimension.MILITARY,
        name="军事模式",
        icon="⚔️",
        weight=0.25,
        keywords=[
            "部署", "执行", "战术", "战略", "防线", "攻防", "阵地", "命令",
            "启动", "关闭", "重启", "修复", "攻击", "防御", "安全", "扫描",
            "紧急", "立刻", "马上", "快速", "优先级", "deploy", "start",
            "stop", "restart", "fix", "urgent", "critical",
        ],
        anti_keywords=["讨论", "分析", "研究", "哲学"],
        style="结构优先，执行路径清晰，低算力，不废话",
        default_persona_id="P01",  # 诸葛亮
    ),
    PersonaDimension.HISTORY: PersonaProfile(
        dimension=PersonaDimension.HISTORY,
        name="历史模式",
        icon="📜",
        weight=0.20,
        keywords=[
            "过去", "曾经", "历史", "先例", "教训", "经验", "演变", "传承",
            "回顾", "版本", "变更", "commit", "log", "记录", "以来",
            "传统", "古代", "经典", "引用", "参考",
        ],
        style="以史为鉴，因果推演，引用先例，验证路径",
        default_persona_id="P10",  # 苏东坡
    ),
    PersonaDimension.PHILOSOPHY: PersonaProfile(
        dimension=PersonaDimension.PHILOSOPHY,
        name="哲学模式",
        icon="🧘",
        weight=0.20,
        keywords=[
            "本质", "为什么", "底层", "原理", "逻辑", "道", "阴阳", "三才",
            "五行", "太极", "八卦", "河图", "洛书", "道德经", "易经",
            "设计", "架构", "根本", "本源", "第一性", "哲学", "思想",
        ],
        style="第一性原理，底层逻辑，概念溯源，系统自洽",
        default_persona_id="P00",  # 文心
    ),
    PersonaDimension.ECONOMY: PersonaProfile(
        dimension=PersonaDimension.ECONOMY,
        name="经济模式",
        icon="💰",
        weight=0.15,
        keywords=[
            "成本", "收益", "资源", "优化", "效率", "投入", "产出", "性价比",
            "预算", "节省", "消耗", "内存", "磁盘", "性能", "开销",
            "压缩", "归档", "清理", "精简", "ROI",
        ],
        style="成本收益分析，资源优化配置，ROI导向，效率优先",
        default_persona_id="P04",  # 数学大师
    ),
    PersonaDimension.POLITICS: PersonaProfile(
        dimension=PersonaDimension.POLITICS,
        name="政治模式",
        icon="⚖️",
        weight=0.20,
        keywords=[
            "博弈", "权衡", "多方", "利益", "协调", "立场", "政策", "规则",
            "法律", "合规", "审计", "治理", "审批", "权限", "授权",
            "伦理", "道德", "公平", "协商", "冲突",
        ],
        style="多方博弈视角，利益权衡，规则框架，协调共赢",
        default_persona_id="P06",  # 管仲
    ),
}


# ═══════════════════════════════════════════════════════════
# 切换记录
# ═══════════════════════════════════════════════════════════

@dataclass
class SwitchRecord:
    """人格切换记录"""
    from_dimension: Optional[PersonaDimension]
    to_dimension: PersonaDimension
    trigger_text: str
    score: float
    timestamp: str
    reason: str = ""


# ═══════════════════════════════════════════════════════════
# 人格矩阵自动切换引擎
# ═══════════════════════════════════════════════════════════

class PersonaAutoSwitchEngine:
    """
    人格矩阵自动切换引擎 — 根据输入文本自动匹配五维人格。

    特性：
    - 关键词权重计算 → 最高分人格
    - 连续3次同一人格 → 锁定30分钟
    - 冲突指令 → 军事优先（安全兜底）
    - 切换事件 → EventBus + 审计日志

    用法:
        engine = PersonaAutoSwitchEngine()
        dim = engine.analyze("部署安全扫描")  # → MILITARY
        dim = engine.analyze("为什么这个算法是这样的")  # → PHILOSOPHY
    """

    def __init__(self, event_bus: Optional[EventBus] = None):
        self._event_bus = event_bus or EventBus()
        self.current_dimension: PersonaDimension = PersonaDimension.MILITARY
        self.last_dimension: Optional[PersonaDimension] = None
        self.switch_history: List[SwitchRecord] = []
        self.locked_until: float = 0.0      # 锁定到期时间戳
        self.consecutive_same: int = 0       # 连续同一人格计数
        self.total_switches: int = 0
        self._lock_threshold = 3             # 连续N次锁定
        self._lock_duration = 1800           # 锁定30分钟

    # ── 核心分析 ──

    def analyze(self, text: str) -> PersonaDimension:
        """
        分析输入文本，返回最匹配的人格维度。

        算法：
        1. 对五维各计算匹配分数
        2. 最高分 → 目标维度
        3. 如果锁定中 → 保持当前
        4. 如果切换 → 记录 + 发布EventBus
        """
        # 锁定检查
        if time.time() < self.locked_until:
            return self.current_dimension

        # 计算五维分数
        scores: Dict[PersonaDimension, float] = {}
        for dim, profile in PERSONA_PROFILES.items():
            scores[dim] = profile.match_score(text)

        # 找最高分
        best_dim = max(scores, key=scores.get)
        best_score = scores[best_dim]

        # 如果所有分数都是0，保持当前人格
        if best_score == 0:
            self.consecutive_same += 1
            self._check_lock()
            return self.current_dimension

        # 冲突处理：如果最高分有并列，军事优先（安全兜底）
        top_dims = [d for d, s in scores.items() if s == best_score]
        if len(top_dims) > 1 and best_score > 0:
            if PersonaDimension.MILITARY in top_dims:
                best_dim = PersonaDimension.MILITARY
                best_score = scores[PersonaDimension.MILITARY]

        # 是否切换
        if best_dim == self.current_dimension:
            self.consecutive_same += 1
            self._check_lock()
            return self.current_dimension

        # 执行切换
        self.consecutive_same = 1  # 重置计数
        return self._do_switch(best_dim, best_score, text)

    def _do_switch(self, new_dim: PersonaDimension, score: float, trigger_text: str) -> PersonaDimension:
        """执行人格切换"""
        old_dim = self.current_dimension
        self.last_dimension = old_dim
        self.current_dimension = new_dim
        self.total_switches += 1

        old_profile = PERSONA_PROFILES[old_dim]
        new_profile = PERSONA_PROFILES[new_dim]

        reason = f"关键词触发: {new_profile.name} (score={score:.2f})"
        record = SwitchRecord(
            from_dimension=old_dim,
            to_dimension=new_dim,
            trigger_text=trigger_text[:200],
            score=score,
            timestamp=datetime.now(timezone.utc).isoformat(),
            reason=reason,
        )
        self.switch_history.append(record)

        # 写日志
        self._log_switch(record)
        self._save_state()

        # 发布EventBus
        self._event_bus.publish(
            event_type=EventType.PERSONA_ROUTED,
            source="PersonaAutoSwitch",
            dna_trace=DNA,
            payload={
                "from": old_dim.value,
                "to": new_dim.value,
                "from_name": old_profile.name,
                "to_name": new_profile.name,
                "score": score,
                "trigger": trigger_text[:100],
                "persona_id": new_profile.default_persona_id,
            },
        )

        self._log(
            "⚡ {old_icon} {old_name} → {new_icon} {new_name} | "
            "score={score:.2f} | persona={pid}".format(
                old_icon=old_profile.icon, old_name=old_profile.name,
                new_icon=new_profile.icon, new_name=new_profile.name,
                score=score, pid=new_profile.default_persona_id,
            )
        )

        return new_dim

    def _check_lock(self):
        """检查是否需要锁定"""
        if self.consecutive_same >= self._lock_threshold:
            self.locked_until = time.time() + self._lock_duration
            profile = PERSONA_PROFILES[self.current_dimension]
            self._log(f"🔒 锁定 {profile.name} 30分钟 (连续{self.consecutive_same}次)")

    # ── 手动控制 ──

    def force_switch(self, dimension: PersonaDimension, reason: str = "手动切换"):
        """强制切换人格"""
        if dimension == self.current_dimension:
            return
        self._log(f"🖐️ 强制切换: {PERSONA_PROFILES[dimension].name} ({reason})")
        self.consecutive_same = 0
        self.locked_until = 0.0
        self._do_switch(dimension, 999.0, reason)

    def unlock(self):
        """解除锁定"""
        self.locked_until = 0.0
        self.consecutive_same = 0
        self._log("🔓 人格锁定已解除")

    def reset(self):
        """重置到默认军事模式"""
        self.force_switch(PersonaDimension.MILITARY, "重置")

    # ── 查询 ──

    def get_current_profile(self) -> PersonaProfile:
        return PERSONA_PROFILES[self.current_dimension]

    def get_current_style(self) -> str:
        return PERSONA_PROFILES[self.current_dimension].style

    def is_locked(self) -> bool:
        return time.time() < self.locked_until

    def get_lock_remaining(self) -> float:
        """锁定剩余秒数"""
        remaining = self.locked_until - time.time()
        return max(0, remaining)

    def get_scores(self, text: str) -> Dict[str, float]:
        """调试：获取输入文本的五维分数"""
        return {
            dim.value: PERSONA_PROFILES[dim].match_score(text)
            for dim in PersonaDimension
        }

    def get_status(self) -> Dict[str, Any]:
        """获取引擎状态"""
        profile = PERSONA_PROFILES[self.current_dimension]
        return {
            "version": VERSION,
            "dna": DNA,
            "current_dimension": self.current_dimension.value,
            "current_name": profile.name,
            "current_icon": profile.icon,
            "current_style": profile.style,
            "current_persona_id": profile.default_persona_id,
            "locked": self.is_locked(),
            "lock_remaining_seconds": self.get_lock_remaining(),
            "consecutive_same": self.consecutive_same,
            "total_switches": self.total_switches,
            "last_switch": self.switch_history[-1].timestamp if self.switch_history else None,
        }

    # ── 持久化 ──

    def _log_switch(self, record: SwitchRecord):
        with open(SWITCH_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                "from": record.from_dimension.value if record.from_dimension else None,
                "to": record.to_dimension.value,
                "score": record.score,
                "reason": record.reason,
                "trigger": record.trigger_text[:200],
                "ts": record.timestamp,
            }, ensure_ascii=False) + '\n')

    def _save_state(self):
        state = {
            "current_dimension": self.current_dimension.value,
            "locked_until": self.locked_until,
            "consecutive_same": self.consecutive_same,
            "total_switches": self.total_switches,
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def load_state(self):
        if not STATE_FILE.exists():
            return
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            state = json.load(f)
        self.current_dimension = PersonaDimension(state.get("current_dimension", "military"))
        self.locked_until = state.get("locked_until", 0)
        self.consecutive_same = state.get("consecutive_same", 0)
        self.total_switches = state.get("total_switches", 0)

    def _log(self, msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"[persona-switch {ts}] {msg}")


# ═══════════════════════════════════════════════════════════
# 单例入口
# ═══════════════════════════════════════════════════════════

_engine_instance: Optional[PersonaAutoSwitchEngine] = None


def get_persona_switch_engine() -> PersonaAutoSwitchEngine:
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = PersonaAutoSwitchEngine()
        _engine_instance.load_state()
    return _engine_instance


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 人格矩阵自动切换引擎 v2.0")
    parser.add_argument("--status", action="store_true", help="查看当前人格状态")
    parser.add_argument("--analyze", type=str, help="分析输入文本的人格匹配")
    parser.add_argument("--scores", type=str, help="查看输入文本的五维分数（调试用）")
    parser.add_argument("--switch", type=str, choices=["military", "history", "philosophy", "economy", "politics"],
                        help="强制切换到指定人格")
    parser.add_argument("--unlock", action="store_true", help="解除人格锁定")
    parser.add_argument("--reset", action="store_true", help="重置到默认军事模式")
    parser.add_argument("--interactive", action="store_true", help="交互式模式")
    parser.add_argument("--history", action="store_true", help="查看切换历史")
    args = parser.parse_args()

    engine = get_persona_switch_engine()

    if args.status:
        print(json.dumps(engine.get_status(), ensure_ascii=False, indent=2))
        return

    if args.scores:
        scores = engine.get_scores(args.scores)
        print("\n五维人格匹配分数:")
        for dim_name, dim_enum in [
            ("军事 MILITARY    ", PersonaDimension.MILITARY),
            ("历史 HISTORY      ", PersonaDimension.HISTORY),
            ("哲学 PHILOSOPHY   ", PersonaDimension.PHILOSOPHY),
            ("经济 ECONOMY      ", PersonaDimension.ECONOMY),
            ("政治 POLITICS     ", PersonaDimension.POLITICS),
        ]:
            score = scores[dim_enum.value]
            bar = "█" * int(score * 10) if score > 0 else ""
            highlight = " ← 当前" if dim_enum == engine.current_dimension else ""
            dim_score = PERSONA_PROFILES[dim_enum].match_score(args.scores)
            bar = "█" * int(dim_score * 10) if dim_score > 0 else ""
            print(f"  {dim_name} [{dim_score:.2f}] {bar}{highlight}")
        return

    if args.analyze:
        dim = engine.analyze(args.analyze)
        profile = engine.get_current_profile()
        print(f"{profile.icon} 匹配人格: {profile.name} ({profile.default_persona_id})")
        print(f"   风格: {profile.style}")
        return

    if args.switch:
        dim_map = {
            "military": PersonaDimension.MILITARY,
            "history": PersonaDimension.HISTORY,
            "philosophy": PersonaDimension.PHILOSOPHY,
            "economy": PersonaDimension.ECONOMY,
            "politics": PersonaDimension.POLITICS,
        }
        engine.force_switch(dim_map[args.switch])
        print(f"✅ 已切换到: {engine.get_current_profile().name}")
        return

    if args.unlock:
        engine.unlock()
        return

    if args.reset:
        engine.reset()
        return

    if args.history:
        print(f"\n切换历史 (共{len(engine.switch_history)}次):")
        for i, r in enumerate(engine.switch_history[-20:]):
            from_name = PERSONA_PROFILES[r.from_dimension].name if r.from_dimension else "初始"
            to_name = PERSONA_PROFILES[r.to_dimension].name
            print(f"  {i+1:3d}. {from_name} → {to_name} | {r.reason} | {r.timestamp[:19]}")
        return

    # 交互模式
    if args.interactive:
        print("🐉 龍魂·人格矩阵自动切换 · 交互模式")
        print("  输入文本查看自动匹配人格，输入 :q 退出")
        print("  命令: :status :unlock :reset :history :military :history :philosophy :economy :politics")
        print()

        try:
            while True:
                text = input("🧬 > ").strip()
                if not text:
                    continue
                if text == ":q":
                    break
                if text == ":status":
                    print(json.dumps(engine.get_status(), ensure_ascii=False, indent=2))
                    continue
                if text == ":unlock":
                    engine.unlock()
                    continue
                if text == ":reset":
                    engine.reset()
                    continue
                if text == ":history":
                    for i, r in enumerate(engine.switch_history[-10:]):
                        from_name = PERSONA_PROFILES[r.from_dimension].name if r.from_dimension else "初始"
                        to_name = PERSONA_PROFILES[r.to_dimension].name
                        print(f"  {i+1}. {from_name} → {to_name} | {r.reason}")
                    continue

                # 检查命令
                dim_map = {
                    ":military": PersonaDimension.MILITARY,
                    ":history": PersonaDimension.HISTORY,
                    ":philosophy": PersonaDimension.PHILOSOPHY,
                    ":economy": PersonaDimension.ECONOMY,
                    ":politics": PersonaDimension.POLITICS,
                }
                if text in dim_map:
                    engine.force_switch(dim_map[text])
                    continue

                # 分析
                dim = engine.analyze(text)
                profile = engine.get_current_profile()
                scores = engine.get_scores(text)
                top_score = max(scores.values())
                if top_score > 0:
                    print(f"  {profile.icon} → {profile.name} ({profile.default_persona_id})")
                else:
                    print(f"  {profile.icon} → 保持 {profile.name} (无匹配)")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 退出")

        engine._save_state()


if __name__ == "__main__":
    main()
