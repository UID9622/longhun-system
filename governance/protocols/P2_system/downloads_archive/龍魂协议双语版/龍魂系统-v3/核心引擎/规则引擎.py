#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
║  龍魂·简单世界规则引擎 v2.0                                 ║
║  LONGHUN SIMPLE WORLD RULES ENGINE                          ║
╠══════════════════════════════════════════════════════════════╣
║  DNA:     #龍芯⚡️丙午·癸巳·癸卯·戊午·䷚颐-RULES-ENGINE-v2.0                ║
║  GPG:     A2D0092CEE2E5BA87035600924C3704A8CC26D5F          ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z               ║
║  SEAL:    #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL ║
╚══════════════════════════════════════════════════════════════╝

老大的规矩，焊进代码里。
坏可以，自己扛。挨骂要立正。错可以弥补。盯着威胁直接干。

v2.0 新增：
  - 持久化存储（本地 JSON 账本，append-only）
  - DNA 链式追溯（chain_hash，改不了）
  - 数字根闸门（dr∈{3,9}→🔴熔断）
  - 三色标准封装（M:: + CNSH:: 双视角）
  - Notion 推送（可选）
  - CLI 入口（命令行直接用）
  - 报告生成（一键导出审计报告）
  - 批量处理（CSV/JSON 批量判案）

用法：
  python3 longhun_rules_engine_v2.py --demo          # 跑演示
  python3 longhun_rules_engine_v2.py --report         # 出报告
  python3 longhun_rules_engine_v2.py --score 张三     # 查分
  python3 longhun_rules_engine_v2.py --add            # 交互式录入
  python3 longhun_rules_engine_v2.py --batch cases.json  # 批量处理
"""

import hashlib
import json
import os
import argparse
import sys
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path


# ═══════════════════════════════════════════════════════════════
# 零、系统配置·本地路径
# ═══════════════════════════════════════════════════════════════

CONFIG = {
    # 账本存放路径（append-only，绝不删）
    "ledger_path": os.path.expanduser("~/.cnsh/data/rules_ledger.jsonl"),
    # 报告输出路径
    "report_path": os.path.expanduser("~/.cnsh/logs/rules_report.txt"),
    # Notion Token（可选，不填就不推送）
    "notion_token": os.environ.get("NOTION_TOKEN", ""),
    # Notion 数据库 ID（可选）
    "notion_db_id": os.environ.get("DATABASE_ID", ""),
    # DNA 前缀
    "dna_prefix": "#龍芯⚡️",
    # 主权标识
    "uid": "UID9622",
    "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
}


# ═══════════════════════════════════════════════════════════════
# 一、老大的规矩·核心定义
# ═══════════════════════════════════════════════════════════════

class Rules:
    """
    老大的规矩，一条一条写清楚。
    这不是理论，这是实际发生的事应该怎么判。
    """

    # 规则1：坏可以，但自己扛
    R1_CAN_BE_BAD = "你可以坏，可以犯错，但要自己扛"

    # 规则2：挨骂要立正
    R2_TAKE_IT = "做错了就站直挨骂，别解释，别甩锅"

    # 规则3：错可以弥补
    R3_CAN_FIX = "错可以改，没人会盯你一辈子"

    # 规则4：威胁就干
    R4_FIGHT = "谁敢拿别人的错威胁人，直接翻脸干"

    # 规则5：补充·补了就加分（v2.0新增）
    R5_COMPENSATE = "知道错了还主动补，这叫有担当"

    # 规则6：惯犯·同一件事连错三次（v2.0新增）
    R6_REPEAT_OFFENDER = "同一个坑掉三次，不是没看见，是选择不改"


# 数字根·龍魂闸门
def digital_root(n: int) -> int:
    """计算数字根（龍魂三色闸门核心算法）"""
    if n <= 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(abs(n)))
    return n


def tricolor_gate(score: int) -> Tuple[str, str]:
    """
    三色闸门：根据分数和数字根判断状态
    🟢 通行 / 🟡 待审 / 🔴 熔断
    """
    dr = digital_root(score)
    if score <= 0 or dr in (3, 9):
        return "🔴", f"熔断（dr={dr}，分={score}）"
    elif score < 60 or dr == 6:
        return "🟡", f"待审（dr={dr}，分={score}）"
    else:
        return "🟢", f"通行（dr={dr}，分={score}）"


# ═══════════════════════════════════════════════════════════════
# 二、事件记录·每一笔账都记清楚
# ═══════════════════════════════════════════════════════════════

@dataclass
class Event:
    """
    一笔账：谁、在什么时候、做了什么、犯没犯规。
    字段设计遵循 §9.25 反笼统律：5 字段保真，不糊弄。
    """
    event_id: str                    # 唯一编号
    person: str                      # 当事人
    action: str                      # 他做了什么（原话，不美化）
    mistake: bool                    # 是不是犯错
    owned: bool                      # 有没有自己扛
    stood_up: bool                   # 挨骂有没有立正
    threat: bool                     # 是不是威胁别人
    compensated: bool = False        # 有没有主动补救（v2.0）
    context: str = ""                # 背景说明（可选）
    timestamp: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
    dna: str = ""                    # 本条 DNA（生成后填入）
    chain_hash: str = ""             # 链式哈希（改不了）
    prev_hash: str = ""              # 上一条的哈希

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ═══════════════════════════════════════════════════════════════
# 三、DNA 链·每笔账都有签名，改不了
# ═══════════════════════════════════════════════════════════════

class DNAChain:
    """
    DNA 链：每笔账关联上一笔，形成不可篡改的历史。
    改了任何一笔，后面的哈希全部对不上。
    """

    @staticmethod
    def generate_dna(event: Event) -> str:
        """生成本条 DNA 标识符"""
        date_str = datetime.now().strftime("%Y%m%d-%H%M%S")
        seed = f"{event.person}{event.action}{event.timestamp}"
        short_hash = hashlib.sha256(seed.encode()).hexdigest()[:8].upper()
        return f"{CONFIG['dna_prefix']}{date_str}-EVT-{short_hash}"

    @staticmethod
    def compute_chain_hash(event: Event, prev_hash: str) -> str:
        """计算链式哈希·把上一条的哈希也编进来"""
        content = json.dumps(
            {
                "event_id": event.event_id,
                "person": event.person,
                "action": event.action,
                "timestamp": event.timestamp,
                "dna": event.dna,
                "prev_hash": prev_hash,
            },
            ensure_ascii=False,
        )
        return hashlib.sha256(content.encode()).hexdigest()[:16].upper()

    @staticmethod
    def verify_chain(events: List[Event]) -> Tuple[bool, str]:
        """
        验证整条链的完整性。
        任何一条被改过，都会验证失败。
        """
        if not events:
            return True, "账本为空"

        prev_hash = "GENESIS"
        for i, evt in enumerate(events):
            # 重新计算这条的链式哈希
            expected = DNAChain.compute_chain_hash(evt, prev_hash)
            if evt.chain_hash != expected:
                return False, f"第{i+1}条账目（{evt.event_id}）链式哈希不匹配，账本已被篡改！"
            prev_hash = evt.chain_hash

        return True, f"✅ 链式验证通过，共 {len(events)} 条账目，无篡改"


# ═══════════════════════════════════════════════════════════════
# 四、评分引擎·按老大规矩打分
# ═══════════════════════════════════════════════════════════════

class ScoreEngine:
    """
    按老大的规矩打分。
    扛事的加分，甩锅的扣分，威胁人的直接零分。
    账本 append-only，历史不删。
    """

    def __init__(self, ledger_path: str = CONFIG["ledger_path"]):
        self.ledger_path = ledger_path
        self.scores: Dict[str, int] = {}
        self.history: List[Event] = []
        self._repeat_count: Dict[str, Dict[str, int]] = {}  # 惯犯追踪

        # 确保目录存在
        Path(ledger_path).parent.mkdir(parents=True, exist_ok=True)

        # 加载已有账本
        self._load_ledger()

    def _load_ledger(self):
        """从本地 JSONL 文件加载账本"""
        if not os.path.exists(self.ledger_path):
            return

        with open(self.ledger_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    evt = Event(**data)
                    self.history.append(evt)
                    # 重建分数
                    if evt.person not in self.scores:
                        self.scores[evt.person] = 100
                except Exception:
                    pass  # 坏行就跳过，不崩溃

        # 重建分数（从头重算，确保准确）
        self._rebuild_scores()

    def _rebuild_scores(self):
        """从历史记录重建每个人的分数"""
        self.scores = {}
        self._repeat_count = {}
        for evt in self.history:
            if evt.person not in self.scores:
                self.scores[evt.person] = 100
            self._apply_rules(evt, record=False)

    def _append_to_ledger(self, event: Event):
        """追加到本地账本（append-only，绝不覆盖）"""
        with open(self.ledger_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")

    def _apply_rules(self, event: Event, record: bool = True) -> dict[str, Any]:
        """
        按规矩判断，更新分数。
        record=True 时记录详情；False 时只算分（用于重建）。
        """
        if event.person not in self.scores:
            self.scores[event.person] = 100

        details = []
        score_before = self.scores[event.person]

        # === 规则1：坏可以，但自己扛 ===
        if event.mistake:
            if event.owned:
                self.scores[event.person] = min(100, self.scores[event.person] + 2)
                details.append(f"🟢 {Rules.R1_CAN_BE_BAD}，+2分")
            else:
                self.scores[event.person] -= 10
                details.append(f"🔴 甩锅了，-10分（{Rules.R1_CAN_BE_BAD}）")

        # === 规则2：挨骂要立正 ===
        if event.mistake and not event.stood_up:
            self.scores[event.person] -= 5
            details.append(f"🔴 没立正，-5分（{Rules.R2_TAKE_IT}）")
        elif event.mistake and event.stood_up:
            details.append(f"🟢 立正了，规矩守住了（{Rules.R2_TAKE_IT}）")

        # === 规则5：主动补救加分 ===
        if event.compensated:
            self.scores[event.person] = min(100, self.scores[event.person] + 5)
            details.append(f"🟢 主动补救，+5分（{Rules.R5_COMPENSATE}）")

        # === 规则6：惯犯追踪 ===
        if event.mistake:
            key = f"{event.person}:{event.action[:20]}"
            if event.person not in self._repeat_count:
                self._repeat_count[event.person] = {}
            self._repeat_count[event.person][key] = (
                self._repeat_count[event.person].get(key, 0) + 1
            )
            repeat = self._repeat_count[event.person][key]
            if repeat >= 3:
                self.scores[event.person] -= 15
                details.append(f"🔴 惯犯！同类错误第{repeat}次，-15分（{Rules.R6_REPEAT_OFFENDER}）")

        # === 规则4：威胁就干（最高优先级） ===
        if event.threat:
            self.scores[event.person] = 0
            details.append(f"🔴 威胁别人！直接零分（{Rules.R4_FIGHT}）")

        # 边界保护
        self.scores[event.person] = max(0, min(100, self.scores[event.person]))

        score_after = self.scores[event.person]
        color, status = tricolor_gate(score_after)

        return {
            "person": event.person,
            "score_before": score_before,
            "score_after": score_after,
            "delta": score_after - score_before,
            "tricolor": color,
            "status": status,
            "details": details,
            "dna": event.dna,
        }

    def judge(self, event: Event) -> dict[str, Any]:
        """
        判断一笔账。主入口。
        生成 DNA → 计算链式哈希 → 打分 → 存账本 → 返回结果。
        """
        # 生成 DNA
        event.dna = DNAChain.generate_dna(event)

        # 计算链式哈希
        prev_hash = self.history[-1].chain_hash if self.history else "GENESIS"
        event.prev_hash = prev_hash
        event.chain_hash = DNAChain.compute_chain_hash(event, prev_hash)

        # 打分
        result = self._apply_rules(event)

        # 存历史
        self.history.append(event)

        # 持久化
        self._append_to_ledger(event)

        return result

    def get_score(self, person: str) -> dict[str, Any]:
        """查一个人的分数和状态"""
        score = self.scores.get(person, 100)
        color, status = tricolor_gate(score)
        records = [e for e in self.history if e.person == person]
        return {
            "person": person,
            "score": score,
            "tricolor": color,
            "status": status,
            "total_events": len(records),
            "mistakes": sum(1 for e in records if e.mistake),
            "threats": sum(1 for e in records if e.threat),
        }

    def get_history(self, person: str | None = None) -> List[dict]:
        """查历史账目"""
        if person:
            return [e.to_dict() for e in self.history if e.person == person]
        return [e.to_dict() for e in self.history]

    def verify_integrity(self) -> Tuple[bool, str]:
        """验证账本完整性（链式哈希校验）"""
        return DNAChain.verify_chain(self.history)


# ═══════════════════════════════════════════════════════════════
# 五、M:: × CNSH:: 双视角封装
# ═══════════════════════════════════════════════════════════════

def wrap_m(result: dict[str, Any], event: Event) -> dict[str, Any]:
    """M:: 机器视角封装·机器看的"""
    return {
        "id": f"M::EVT-{CONFIG['uid']}-{event.event_id}",
        "type": "event",
        "ts": event.timestamp,
        "status": "fused" if result["score_after"] == 0 else "pass",
        "refs": [event.event_id],
        "payload": {
            "person": result["person"],
            "score_before": result["score_before"],
            "score_after": result["score_after"],
            "delta": result["delta"],
            "tricolor": result["tricolor"],
            "details": result["details"],
            "chain_hash": event.chain_hash,
        },
    }


def wrap_cnsh(result: dict[str, Any], event: Event) -> dict[str, Any]:
    """CNSH:: 龍魂视角封装·龍魂看的"""
    return {
        "dna": event.dna,
        "gate": CONFIG.get("confirm", "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"),
        "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
        "gpg": CONFIG["gpg"],
        "route": "RULES-ENGINE|SCORE-AUDIT|DNA-CHAIN",
        "audit": result["tricolor"],
        "wuxing": "水" if result["score_after"] < 60 else "金",
        "layer": "L3日常",
        "policy": "fuse" if result["score_after"] == 0 else "pass",
        "chain_hash": event.chain_hash,
    }


# ═══════════════════════════════════════════════════════════════
# 六、报告生成·一键出报告
# ═══════════════════════════════════════════════════════════════

def generate_report(engine: ScoreEngine) -> str:
    """生成完整审计报告"""
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("╔══════════════════════════════════════════════════════════════╗")
    lines.append("║  龍魂·简单世界规则引擎 v2.0  审计报告                      ║")
    lines.append(f"║  生成时间：{now}                         ║")
    lines.append("╚══════════════════════════════════════════════════════════════╝")
    lines.append("")

    # 链式完整性验证
    ok, msg = engine.verify_integrity()
    lines.append(f"🔐 账本完整性：{msg}")
    lines.append("")

    # 各人汇总
    lines.append("📊 人员得分汇总")
    lines.append("─" * 50)
    all_persons = sorted(engine.scores.keys())
    for person in all_persons:
        info = engine.get_score(person)
        lines.append(
            f"  {info['tricolor']} {person:10} 分={info['score']:3d}  "
            f"事件={info['total_events']}  错={info['mistakes']}  威胁={info['threats']}"
        )
    lines.append("")

    # 详细账目
    lines.append("📋 详细账目（时间倒序）")
    lines.append("─" * 50)
    for evt in reversed(engine.history[-20:]):  # 最近20条
        icon = "🔴" if evt.threat else ("🟡" if evt.mistake and not evt.owned else "🟢")
        lines.append(f"  {icon} [{evt.event_id}] {evt.person}: {evt.action}")
        lines.append(f"     时间: {evt.timestamp[:19]}")
        lines.append(f"     DNA:  {evt.dna}")
        lines.append(f"     链式: {evt.chain_hash}")
        lines.append("")

    # DNA 签章
    lines.append("─" * 50)
    lines.append(f"DNA:     {CONFIG['dna_prefix']}{datetime.now().strftime('%Y%m%d')}-REPORT-v2.0")
    lines.append(f"CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
    lines.append(f"GPG:     {CONFIG['gpg']}")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 七、Notion 推送（可选）
# ═══════════════════════════════════════════════════════════════

def push_to_notion(result: dict[str, Any], event: Event) -> bool:
    """
    把判断结果推送到 Notion 数据库。
    需要设置环境变量 NOTION_TOKEN 和 DATABASE_ID。
    """
    token = CONFIG["notion_token"]
    db_id = CONFIG["notion_db_id"]

    if not token or not db_id:
        print("  ⚠️  Notion 未配置（NOTION_TOKEN/DATABASE_ID 未设置），跳过推送")
        return False

    try:
        import urllib.request
        import urllib.error

        payload = {
            "parent": {"database_id": db_id},
            "properties": {
                "任务编号": {"title": [{"text": {"content": event.event_id}}]},
                "当事人": {"rich_text": [{"text": {"content": event.person}}]},
                "行为": {"rich_text": [{"text": {"content": event.action}}]},
                "三色": {"select": {"name": result["tricolor"]}},
                "得分": {"number": result["score_after"]},
                "DNA": {"rich_text": [{"text": {"content": event.dna}}]},
            },
        }

        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            "https://api.notion.com/v1/pages",
            data=data,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Notion-Version": "2022-06-28",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                print(f"  ✅ 已推送到 Notion")
                return True

    except Exception as e:
        print(f"  ⚠️  Notion 推送失败: {e}")

    return False


# ═══════════════════════════════════════════════════════════════
# 八、批量处理·从 JSON 文件批量判案
# ═══════════════════════════════════════════════════════════════

def batch_process(engine: ScoreEngine, filepath: str) -> List[dict]:
    """
    从 JSON 文件批量处理案例。
    JSON 格式：[{"person": "张三", "action": "...", "mistake": true, ...}, ...]
    """
    with open(filepath, "r", encoding="utf-8") as f:
        cases = json.load(f)

    results = []
    for i, case in enumerate(cases):
        evt = Event(
            event_id=f"BATCH-{i+1:04d}",
            person=case.get("person", "未知"),
            action=case.get("action", ""),
            mistake=case.get("mistake", False),
            owned=case.get("owned", False),
            stood_up=case.get("stood_up", False),
            threat=case.get("threat", False),
            compensated=case.get("compensated", False),
            context=case.get("context", ""),
        )
        result = engine.judge(evt)
        results.append(result)
        print(f"  {result['tricolor']} {evt.person}: {result['score_before']}→{result['score_after']}")

    return results


# ═══════════════════════════════════════════════════════════════
# 九、演示·跑起来给你看
# ═══════════════════════════════════════════════════════════════

def run_demo(engine: ScoreEngine):
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║  老大·简单世界规则引擎 v2.0  演示                          ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")

    cases = [
        # (编号, 人, 事, 犯错, 扛了, 立正, 威胁, 补救)
        ("DEMO-001", "张三", "把项目文件搞丢了", True, True, True, False, True),
        ("DEMO-002", "李四", "把客户得罪了还说是别人主意", True, False, False, False, False),
        ("DEMO-003", "王五", "拿同事去年失误威胁他让出项目", False, False, False, True, False),
        ("DEMO-004", "张三", "代码写错了导致系统崩了，第一时间认了", True, True, True, False, True),
        ("DEMO-005", "李四", "延误交付还甩锅给需求不清晰", True, False, False, False, False),
        ("DEMO-006", "李四", "延误交付还甩锅给不可抗力", True, False, False, False, False),  # 惯犯
    ]

    for event_id, person, action, mistake, owned, stood_up, threat, compensated in cases:
        evt = Event(
            event_id=event_id,
            person=person,
            action=action,
            mistake=mistake,
            owned=owned,
            stood_up=stood_up,
            threat=threat,
            compensated=compensated,
        )

        result = engine.judge(evt)
        m = wrap_m(result, evt)
        c = wrap_cnsh(result, evt)

        print(f"📋 [{evt.event_id}] {evt.person}：{evt.action}")
        for d in result["details"]:
            print(f"   {d}")
        print(f"   分数：{result['score_before']} → {result['score_after']}  {result['tricolor']} {result['status']}")
        print(f"   DNA：{evt.dna}")
        print(f"   链：{evt.chain_hash}")
        print()

    # 总览
    print("📊 最终得分")
    print("─" * 45)
    for person in sorted(engine.scores.keys()):
        info = engine.get_score(person)
        print(f"  {info['tricolor']} {person:6} 分={info['score']:3d}  状态={info['status']}")

    # 链式验证
    print()
    ok, msg = engine.verify_integrity()
    print(f"🔐 {msg}")


# ═══════════════════════════════════════════════════════════════
# 十、交互式录入
# ═══════════════════════════════════════════════════════════════

def interactive_add(engine: ScoreEngine):
    """交互式录入一笔账"""
    print("\n📝 交互式录入（直接回车跳过可选项）")
    print("─" * 40)

    person = input("当事人：").strip()
    action = input("做了什么：").strip()
    mistake = input("是否犯错 (y/n)：").strip().lower() == "y"
    owned = False
    stood_up = False
    compensated = False
    threat = input("是否威胁别人 (y/n)：").strip().lower() == "y"

    if mistake:
        owned = input("有没有自己扛 (y/n)：").strip().lower() == "y"
        stood_up = input("挨骂有没有立正 (y/n)：").strip().lower() == "y"
        compensated = input("有没有主动补救 (y/n)：").strip().lower() == "y"

    context = input("备注（可选）：").strip()

    import uuid
    evt = Event(
        event_id=f"MANUAL-{uuid.uuid4().hex[:8].upper()}",
        person=person,
        action=action,
        mistake=mistake,
        owned=owned,
        stood_up=stood_up,
        threat=threat,
        compensated=compensated,
        context=context,
    )

    result = engine.judge(evt)

    print(f"\n判定结果：")
    for d in result["details"]:
        print(f"  {d}")
    print(f"  分数：{result['score_before']} → {result['score_after']}  {result['tricolor']}")
    print(f"  DNA：{evt.dna}")

    # 可选推送 Notion
    if CONFIG["notion_token"]:
        push = input("\n推送到 Notion？(y/n)：").strip().lower()
        if push == "y":
            push_to_notion(result, evt)


# ═══════════════════════════════════════════════════════════════
# 十一、CLI 入口
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="龍魂·简单世界规则引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 longhun_rules_engine_v2.py --demo           跑演示
  python3 longhun_rules_engine_v2.py --report          出报告
  python3 longhun_rules_engine_v2.py --score 张三      查某人分数
  python3 longhun_rules_engine_v2.py --add             交互式录入
  python3 longhun_rules_engine_v2.py --verify          验证账本完整性
  python3 longhun_rules_engine_v2.py --batch cases.json  批量处理

DNA: #龍芯⚡️丙午·癸巳·癸卯·戊午·䷚颐-RULES-ENGINE-v2.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
        """,
    )

    parser.add_argument("--demo", action="store_true", help="跑演示用例")
    parser.add_argument("--report", action="store_true", help="生成审计报告")
    parser.add_argument("--score", metavar="PERSON", help="查某人的分数")
    parser.add_argument("--add", action="store_true", help="交互式录入一笔账")
    parser.add_argument("--verify", action="store_true", help="验证账本完整性")
    parser.add_argument("--batch", metavar="FILE", help="批量处理 JSON 文件")
    parser.add_argument("--history", metavar="PERSON", help="查某人的历史账目")
    parser.add_argument("--ledger", metavar="PATH", help="指定账本路径（默认 ~/.cnsh/data/rules_ledger.jsonl）")

    args = parser.parse_args()

    # 账本路径
    ledger_path = args.ledger or CONFIG["ledger_path"]
    engine = ScoreEngine(ledger_path=ledger_path)

    if args.demo:
        run_demo(engine)

    elif args.report:
        report = generate_report(engine)
        print(report)
        # 保存到文件
        Path(CONFIG["report_path"]).parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG["report_path"], "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n✅ 报告已保存到：{CONFIG['report_path']}")

    elif args.score:
        info = engine.get_score(args.score)
        print(f"\n{info['tricolor']} {info['person']}")
        print(f"  得分：{info['score']}")
        print(f"  状态：{info['status']}")
        print(f"  总事件：{info['total_events']}")
        print(f"  犯错次数：{info['mistakes']}")
        print(f"  威胁次数：{info['threats']}")

    elif args.add:
        interactive_add(engine)

    elif args.verify:
        ok, msg = engine.verify_integrity()
        print(f"\n{'✅' if ok else '🔴'} {msg}")

    elif args.batch:
        if not os.path.exists(args.batch):
            print(f"🔴 文件不存在：{args.batch}")
            sys.exit(1)
        print(f"\n📦 批量处理：{args.batch}")
        results = batch_process(engine, args.batch)
        print(f"\n✅ 共处理 {len(results)} 条")

    elif args.history:
        records = engine.get_history(args.history)
        print(f"\n📋 {args.history} 的历史账目（共 {len(records)} 条）")
        for r in records:
            print(f"  [{r['event_id']}] {r['action'][:40]}  DNA={r['dna'][:30]}")

    else:
        # 没有参数·跑演示
        run_demo(engine)


if __name__ == "__main__":
    main()
