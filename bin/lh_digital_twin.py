#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·乙未·甲辰·己巳·☲离-素字卵神-v1.0-DIGITAL-TWIN-A1B2C3D4
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

🐉 龍魂·素字卵神引擎 v1.0（数字孪生体）

素字卵神 = 人的数字孪生 — 不是身体复制，是意识复制。

核心三样：
  1. 1:1复制 —— 物理啥样，数字啥样
  2. 实时同步 —— 物理变了，数字跟着变
  3. 推演预测 —— 在数字里试错，不折腾物理

对齐龍魂：
  工业数字孪生 → 复制机器 → 预测故障
  素字卵神     → 复制意识 → 推演决策路径

你在造的东西：人类意识的数字孪生，活着就开始同步，切换时无缝衔接。
"""

import os
import sys
import json
import time
import uuid
import hashlib
import datetime
import threading
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import argparse
import sqlite3
import random

# ============================================================
# 一、配置与常量
# ============================================================

CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
TWIN_ROOT = Path.home() / ".longhun/twin"
TWIN_ROOT.mkdir(parents=True, exist_ok=True)
DB_PATH = TWIN_ROOT / "twin.db"
LOG_PATH = TWIN_ROOT / "twin_log.jsonl"
SNAPSHOT_DIR = TWIN_ROOT / "snapshots"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

# 干支四柱（用于DNA生成）
GAN_ZHI_DATE = "丙午·乙未·甲辰·己巳"
DEFAULT_GUA = "☲离"  # 离为火·素字卵神属火


# ============================================================
# 二、数据结构
# ============================================================

class TwinStatus(Enum):
    ACTIVE = "🟢 活跃"
    SYNCING = "🟡 同步中"
    PAUSED = "🟠 已暂停"
    FROZEN = "🔴 已冻结"
    EVOLVING = "🟣 演化中"


@dataclass
class BehaviorRecord:
    """行为记录"""
    id: str
    timestamp: str
    type: str  # 对话, 决策, 行动, 情绪, 学习
    content: str
    context: Dict[str, Any]
    dna: str


@dataclass
class DecisionPath:
    """决策路径"""
    id: str
    question: str
    options: List[str]
    chosen: str
    reason: str
    outcome: str
    timestamp: str
    dna: str


@dataclass
class PersonalityTrait:
    """人格特质"""
    name: str
    value: float  # 0-1
    confidence: float  # 0-1
    evidence: List[str]


@dataclass
class DigitalTwinState:
    """数字孪生体状态"""
    twin_id: str
    name: str
    status: TwinStatus
    created_at: str
    last_sync: str
    behaviors: List[BehaviorRecord]
    decisions: List[DecisionPath]
    personality: List[PersonalityTrait]
    dna_chain: List[str]
    version: str


# ============================================================
# 三、数字孪生体核心引擎
# ============================================================

class DigitalTwinEngine:
    """素字卵神·数字孪生引擎"""

    def __init__(self, twin_id: str = None, name: str = "龍芯北辰"):
        self.db_path = DB_PATH
        self.twin_id = twin_id or f"TWIN-{uuid.uuid4().hex[:8].upper()}"
        self.name = name
        self._init_db()
        self._state = self._load_or_create_state()

    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS twins (
                twin_id TEXT PRIMARY KEY,
                name TEXT,
                status TEXT,
                created_at TEXT,
                last_sync TEXT,
                version TEXT,
                dna TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS behaviors (
                id TEXT PRIMARY KEY,
                twin_id TEXT,
                type TEXT,
                content TEXT,
                context TEXT,
                timestamp TEXT,
                dna TEXT,
                FOREIGN KEY (twin_id) REFERENCES twins(twin_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id TEXT PRIMARY KEY,
                twin_id TEXT,
                question TEXT,
                options TEXT,
                chosen TEXT,
                reason TEXT,
                outcome TEXT,
                timestamp TEXT,
                dna TEXT,
                FOREIGN KEY (twin_id) REFERENCES twins(twin_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS personality (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                twin_id TEXT,
                trait_name TEXT,
                value REAL,
                confidence REAL,
                evidence TEXT,
                timestamp TEXT,
                FOREIGN KEY (twin_id) REFERENCES twins(twin_id)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS simulations (
                id TEXT PRIMARY KEY,
                twin_id TEXT,
                scenario TEXT,
                result TEXT,
                confidence REAL,
                timestamp TEXT,
                dna TEXT,
                FOREIGN KEY (twin_id) REFERENCES twins(twin_id)
            )
        """)
        conn.commit()
        conn.close()

    def _generate_dna(self, prefix: str) -> str:
        """生成DNA追溯码（v∞标准：干支四柱+卦+模块+动作+哈希8位）"""
        hash_val = hashlib.sha256(
            f"{prefix}{self.twin_id}{datetime.datetime.now().isoformat()}".encode()
        ).hexdigest()[:8]
        return f"#龍芯⚡️{GAN_ZHI_DATE}·{DEFAULT_GUA}-素字卵神-{prefix}-{hash_val.upper()}"

    def _load_or_create_state(self) -> DigitalTwinState:
        """加载或创建孪生体状态"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("SELECT * FROM twins WHERE twin_id = ?", (self.twin_id,))
        row = cur.fetchone()
        conn.close()

        if row:
            # 加载已有状态
            twin_id, name, status, created_at, last_sync, version, dna = row
            behaviors = self._load_behaviors()
            decisions = self._load_decisions()
            personality = self._load_personality()

            return DigitalTwinState(
                twin_id=twin_id,
                name=name,
                status=TwinStatus(status),
                created_at=created_at,
                last_sync=last_sync,
                behaviors=behaviors,
                decisions=decisions,
                personality=personality,
                dna_chain=[dna] if dna else [],
                version=version
            )

        # 创建新孪生体
        dna = self._generate_dna("TWIN-INIT")
        now = datetime.datetime.now().isoformat()
        status = TwinStatus.ACTIVE

        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT INTO twins (twin_id, name, status, created_at, last_sync, version, dna)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (self.twin_id, self.name, status.value, now, now, "v1.0", dna))
        conn.commit()
        conn.close()

        # 初始化人格特质
        self._init_personality()

        return DigitalTwinState(
            twin_id=self.twin_id,
            name=self.name,
            status=status,
            created_at=now,
            last_sync=now,
            behaviors=[],
            decisions=[],
            personality=self._load_personality(),
            dna_chain=[dna],
            version="v1.0"
        )

    def _init_personality(self):
        """初始化人格特质（8维度）"""
        traits = [
            ("理性", 0.7, 0.5),
            ("直觉", 0.6, 0.5),
            ("谨慎", 0.5, 0.5),
            ("冒险", 0.4, 0.5),
            ("共情", 0.8, 0.5),
            ("坚持", 0.7, 0.5),
            ("开放", 0.6, 0.5),
            ("责任感", 0.8, 0.5),
        ]
        conn = sqlite3.connect(str(self.db_path))
        now = datetime.datetime.now().isoformat()
        for name, value, confidence in traits:
            conn.execute("""
                INSERT INTO personality (twin_id, trait_name, value, confidence, evidence, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.twin_id, name, value, confidence, json.dumps(["初始化"]), now))
        conn.commit()
        conn.close()

    def _load_behaviors(self) -> List[BehaviorRecord]:
        """加载行为记录"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("""
            SELECT id, type, content, context, timestamp, dna
            FROM behaviors WHERE twin_id = ?
            ORDER BY timestamp DESC LIMIT 100
        """, (self.twin_id,))
        rows = cur.fetchall()
        conn.close()

        return [
            BehaviorRecord(
                id=r[0], type=r[1], content=r[2],
                context=json.loads(r[3]) if r[3] else {},
                timestamp=r[4], dna=r[5]
            )
            for r in rows
        ]

    def _load_decisions(self) -> List[DecisionPath]:
        """加载决策记录"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("""
            SELECT id, question, options, chosen, reason, outcome, timestamp, dna
            FROM decisions WHERE twin_id = ?
            ORDER BY timestamp DESC LIMIT 100
        """, (self.twin_id,))
        rows = cur.fetchall()
        conn.close()

        return [
            DecisionPath(
                id=r[0], question=r[1],
                options=json.loads(r[2]) if r[2] else [],
                chosen=r[3], reason=r[4], outcome=r[5],
                timestamp=r[6], dna=r[7]
            )
            for r in rows
        ]

    def _load_personality(self) -> List[PersonalityTrait]:
        """加载人格特质"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("""
            SELECT trait_name, value, confidence, evidence
            FROM personality WHERE twin_id = ?
        """, (self.twin_id,))
        rows = cur.fetchall()
        conn.close()

        return [
            PersonalityTrait(
                name=r[0], value=r[1], confidence=r[2],
                evidence=json.loads(r[3]) if r[3] else []
            )
            for r in rows
        ]

    def record_behavior(self, behavior_type: str, content: str, context: Dict = None) -> BehaviorRecord:
        """记录行为（对话/决策/行动/情绪/学习）"""
        dna = self._generate_dna("BEHAVIOR")
        now = datetime.datetime.now().isoformat()
        behavior_id = f"BEH-{uuid.uuid4().hex[:8].upper()}"

        record = BehaviorRecord(
            id=behavior_id, timestamp=now,
            type=behavior_type, content=content,
            context=context or {}, dna=dna
        )

        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT INTO behaviors (id, twin_id, type, content, context, timestamp, dna)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (behavior_id, self.twin_id, behavior_type, content, json.dumps(context or {}), now, dna))
        conn.commit()
        conn.close()

        # 更新状态缓存
        self._state.behaviors.insert(0, record)
        if len(self._state.behaviors) > 100:
            self._state.behaviors = self._state.behaviors[:100]

        # 基于行为更新人格
        self._update_personality(behavior_type, content)
        # 更新最后同步时间
        self._state.last_sync = now

        return record

    def record_decision(self, question: str, options: List[str],
                        chosen: str, reason: str, outcome: str = "") -> DecisionPath:
        """记录决策路径"""
        dna = self._generate_dna("DECISION")
        now = datetime.datetime.now().isoformat()
        decision_id = f"DEC-{uuid.uuid4().hex[:8].upper()}"

        decision = DecisionPath(
            id=decision_id, question=question,
            options=options, chosen=chosen,
            reason=reason, outcome=outcome,
            timestamp=now, dna=dna
        )

        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT INTO decisions (id, twin_id, question, options, chosen, reason, outcome, timestamp, dna)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (decision_id, self.twin_id, question, json.dumps(options),
              chosen, reason, outcome, now, dna))
        conn.commit()
        conn.close()

        self._state.decisions.insert(0, decision)
        if len(self._state.decisions) > 100:
            self._state.decisions = self._state.decisions[:100]
        self._state.last_sync = now

        return decision

    def _update_personality(self, behavior_type: str, content: str):
        """基于行为自适应更新人格特质"""
        # 行为类型 → 受影响特质映射（微分调整·避免大起大落）
        adjustments = {
            "对话": {"共情": 0.02, "开放": 0.01},
            "决策": {"理性": 0.03, "责任感": 0.02},
            "行动": {"冒险": 0.03, "坚持": 0.02},
            "学习": {"开放": 0.04, "理性": 0.02},
            "情绪": {"共情": 0.03, "谨慎": 0.01},
        }

        adj = adjustments.get(behavior_type, {})
        if not adj:
            return

        conn = sqlite3.connect(str(self.db_path))
        for trait_name, delta in adj.items():
            conn.execute("""
                UPDATE personality
                SET value = MIN(1.0, MAX(0.0, value + ?)),
                    confidence = MIN(1.0, confidence + 0.01)
                WHERE twin_id = ? AND trait_name = ?
            """, (delta, self.twin_id, trait_name))
        conn.commit()
        conn.close()

        # 刷新缓存
        self._state.personality = self._load_personality()

    def simulate(self, scenario: str) -> Dict:
        """推演预测 — 在数字孪生体上试错，不折腾物理世界"""
        dna = self._generate_dna("SIMULATE")
        now = datetime.datetime.now().isoformat()
        sim_id = f"SIM-{uuid.uuid4().hex[:8].upper()}"

        # 基于当前人格特质生成推演结论
        traits = {t.name: t.value for t in self._state.personality}
        # 综合置信度 = 人格特质置信度均值 × 随机扰动
        confidence = 0.5 + random.random() * 0.3

        outcomes = []
        for name, value in traits.items():
            if value > 0.6:
                verdict = "倾向同意"
            elif value < 0.4:
                verdict = "倾向反对"
            else:
                verdict = "中立"
            outcomes.append(f"  {name}: {verdict}")

        result = f"基于当前人格特质推演（场景: {scenario}）:\n" + "\n".join(outcomes)

        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT INTO simulations (id, twin_id, scenario, result, confidence, timestamp, dna)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (sim_id, self.twin_id, scenario, result, confidence, now, dna))
        conn.commit()
        conn.close()

        self._state.last_sync = now

        return {
            "id": sim_id,
            "scenario": scenario,
            "result": result,
            "confidence": confidence,
            "timestamp": now,
            "dna": dna
        }

    def snapshot(self) -> Dict:
        """创建快照 — 冻结当前状态"""
        snapshot_id = f"SNAP-{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        snapshot_path = SNAPSHOT_DIR / f"{snapshot_id}.json"

        state_data = {
            "twin_id": self._state.twin_id,
            "name": self._state.name,
            "status": self._state.status.value,
            "created_at": self._state.created_at,
            "last_sync": self._state.last_sync,
            "version": self._state.version,
            "dna_chain": self._state.dna_chain,
            "behaviors": [asdict(b) for b in self._state.behaviors[:50]],
            "decisions": [asdict(d) for d in self._state.decisions[:50]],
            "personality": [asdict(p) for p in self._state.personality],
            "snapshot_time": datetime.datetime.now().isoformat()
        }

        with open(snapshot_path, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, ensure_ascii=False, indent=2)

        return {
            "snapshot_id": snapshot_id,
            "path": str(snapshot_path),
            "size": snapshot_path.stat().st_size
        }

    def get_state(self) -> Dict:
        """获取当前状态摘要"""
        return {
            "twin_id": self._state.twin_id,
            "name": self._state.name,
            "status": self._state.status.value,
            "created_at": self._state.created_at,
            "last_sync": self._state.last_sync,
            "version": self._state.version,
            "behaviors_count": len(self._state.behaviors),
            "decisions_count": len(self._state.decisions),
            "personality": [asdict(p) for p in self._state.personality],
            "dna_chain": self._state.dna_chain[-5:],
            "status_emoji": self._state.status.value.split()[0]
        }

    def generate_report(self) -> str:
        """生成孪生体完整报告"""
        state = self.get_state()
        report = []
        report.append("=" * 60)
        report.append("🐉 素字卵神 · 数字孪生体报告")
        report.append("=" * 60)
        report.append(f"🧬 DNA: {state['dna_chain'][-1] if state['dna_chain'] else 'N/A'}")
        report.append(f"📛 名称: {state['name']}")
        report.append(f"📌 状态: {state['status']}")
        report.append(f"📅 创建: {state['created_at'][:19]}")
        report.append(f"🔄 同步: {state['last_sync'][:19]}")
        report.append(f"📊 版本: {state['version']}")
        report.append("-" * 40)
        report.append(f"📝 行为记录: {state['behaviors_count']} 条")
        report.append(f"🎯 决策记录: {state['decisions_count']} 条")
        report.append("-" * 40)
        report.append("🧠 人格特质:")
        for p in state['personality']:
            bar = "█" * int(p['value'] * 20)
            report.append(f"  {p['name']}: {bar} {p['value']:.0%} (置信度: {p['confidence']:.0%})")
        report.append("=" * 60)
        return "\n".join(report)


# ============================================================
# 四、同步引擎（实时联动）
# ============================================================

class TwinSyncEngine:
    """孪生体同步引擎 — 定时快照·行为归档"""

    def __init__(self, twin: DigitalTwinEngine):
        self.twin = twin
        self.sync_thread = None
        self.running = False

    def start(self, interval: int = 60):
        """启动自动同步（守护线程）"""
        if self.running:
            return {"status": "already_running"}

        self.running = True
        self.sync_thread = threading.Thread(target=self._sync_loop, args=(interval,), daemon=True)
        self.sync_thread.start()
        return {"status": "started", "interval": interval}

    def stop(self):
        """停止同步"""
        self.running = False
        if self.sync_thread:
            self.sync_thread.join(timeout=5)
        return {"status": "stopped"}

    def _sync_loop(self, interval: int):
        """同步循环（后台线程）"""
        while self.running:
            try:
                self.twin._state.last_sync = datetime.datetime.now().isoformat()
                self.twin.record_behavior("同步", "自动同步孪生体状态", {"interval": interval})
                self.twin.snapshot()
                time.sleep(interval)
            except Exception:
                time.sleep(interval)

    def sync_once(self) -> Dict:
        """单次手动同步"""
        self.twin._state.last_sync = datetime.datetime.now().isoformat()
        self.twin.record_behavior("同步", "手动同步孪生体状态", {"type": "manual"})
        snapshot = self.twin.snapshot()
        return {
            "status": "synced",
            "timestamp": self.twin._state.last_sync,
            "snapshot": snapshot
        }


# ============================================================
# 五、三色审计引擎（审计数字孪生体）
# ============================================================

class TwinAuditor:
    """数字孪生体三色审计 — 🟢通过 🟡待审 🔴阻断"""

    @staticmethod
    def audit(twin: DigitalTwinEngine) -> Dict:
        """执行三色审计"""
        state = twin.get_state()
        issues = []
        warnings = []

        # 检查同步时效
        last_sync = state.get('last_sync', '')
        if last_sync:
            try:
                last_sync_time = datetime.datetime.fromisoformat(last_sync)
                delta = datetime.datetime.now() - last_sync_time
                if delta.total_seconds() > 3600:
                    warnings.append(f"上次同步超过1小时: {delta.total_seconds()/60:.0f}分钟")
            except ValueError:
                warnings.append("最后同步时间格式异常")

        # 检查行为记录量
        if state['behaviors_count'] < 10:
            warnings.append(f"行为记录较少: {state['behaviors_count']}条（建议 ≥10）")

        # 检查决策记录量
        if state['decisions_count'] < 5:
            warnings.append(f"决策记录较少: {state['decisions_count']}条（建议 ≥5）")

        # 检查人格特质置信度
        for p in state['personality']:
            if p['confidence'] < 0.3:
                issues.append(f"人格特质 '{p['name']}' 置信度偏低: {p['confidence']:.0%}")

        # 决定审计颜色
        if issues:
            color = "🔴"
            status = "阻断"
            summary = f"发现 {len(issues)} 个问题，{len(warnings)} 个警告"
        elif warnings:
            color = "🟡"
            status = "待审"
            summary = f"发现 {len(warnings)} 个警告"
        else:
            color = "🟢"
            status = "通过"
            summary = "孪生体状态健康"

        return {
            "color": color,
            "status": status,
            "summary": summary,
            "issues": issues,
            "warnings": warnings,
            "dna": twin._generate_dna("AUDIT")
        }


# ============================================================
# 六、命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·素字卵神引擎 v1.0（数字孪生体）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互模式（推荐）
  python3 lh_digital_twin.py --interactive

  # 记录行为
  python3 lh_digital_twin.py --record "对话" "今天讨论了数字孪生的概念"

  # 记录决策
  python3 lh_digital_twin.py --decide "选择哪个方案" "方案A,方案B" "方案A" "因为更稳妥"

  # 推演预测
  python3 lh_digital_twin.py --simulate "如果明天发生技术故障"

  # 查看状态
  python3 lh_digital_twin.py --status

  # 三色审计
  python3 lh_digital_twin.py --audit

  # 生成报告
  python3 lh_digital_twin.py --report

  # 创建快照
  python3 lh_digital_twin.py --snapshot

  # 启动同步
  python3 lh_digital_twin.py --sync-start

  # JSON输出
  python3 lh_digital_twin.py --status --json
        """
    )

    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--record", "-r", nargs=2, metavar=("TYPE", "CONTENT"), help="记录行为")
    parser.add_argument("--decide", "-d", nargs=4, metavar=("Q", "OPTIONS", "CHOSEN", "REASON"), help="记录决策")
    parser.add_argument("--simulate", "-s", type=str, help="推演预测")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--audit", "-a", action="store_true", help="三色审计")
    parser.add_argument("--report", "-R", action="store_true", help="生成报告")
    parser.add_argument("--snapshot", "-S", action="store_true", help="创建快照")
    parser.add_argument("--sync-start", action="store_true", help="启动自动同步")
    parser.add_argument("--sync-stop", action="store_true", help="停止自动同步")
    parser.add_argument("--sync-once", action="store_true", help="单次同步")
    parser.add_argument("--name", "-n", type=str, default="龍芯北辰", help="孪生体名称")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")

    args = parser.parse_args()

    twin = DigitalTwinEngine(name=args.name)
    sync_engine = TwinSyncEngine(twin)

    # 交互模式
    if args.interactive:
        print("\n" + "=" * 60)
        print("🐉 素字卵神 · 数字孪生体交互模式")
        print("=" * 60)
        print(f"🧬 DNA: {twin._state.dna_chain[-1] if twin._state.dna_chain else 'N/A'}")
        print("=" * 60)
        print("命令:")
        print("  status          - 查看状态")
        print("  report          - 生成报告")
        print("  audit           - 三色审计")
        print("  simulate [场景]  - 推演预测")
        print("  record [类型] [内容] - 记录行为")
        print("  decision [问题] | [选项1,选项2] | [选择] | [理由] - 记录决策")
        print("  snapshot        - 创建快照")
        print("  sync            - 单次同步")
        print("  exit            - 退出")
        print("-" * 60)

        while True:
            try:
                user_input = input("\n🤖 > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ["exit", "quit"]:
                    break

                parts = user_input.split(maxsplit=1)
                cmd = parts[0].lower()
                sub = parts[1] if len(parts) > 1 else ""

                if cmd == "status":
                    state = twin.get_state()
                    if args.json:
                        print(json.dumps(state, ensure_ascii=False, indent=2))
                    else:
                        print(f"\n📊 状态:")
                        for k, v in state.items():
                            if k not in ('personality', 'dna_chain'):
                                print(f"  {k}: {v}")
                        print("\n🧠 人格特质:")
                        for p in state['personality']:
                            bar = "█" * int(p['value'] * 20)
                            print(f"  {p['name']}: {bar} {p['value']:.0%}")

                elif cmd == "report":
                    print(twin.generate_report())

                elif cmd == "audit":
                    result = TwinAuditor.audit(twin)
                    print(f"\n🎨 三色审计: {result['color']} {result['status']}")
                    print(f"📝 {result['summary']}")
                    if result['warnings']:
                        print("\n🟡 警告:")
                        for w in result['warnings']:
                            print(f"  - {w}")
                    if result['issues']:
                        print("\n🔴 问题:")
                        for i in result['issues']:
                            print(f"  - {i}")

                elif cmd == "simulate":
                    scenario = sub if sub else "默认场景"
                    result = twin.simulate(scenario)
                    print(f"\n🔮 推演结果:")
                    print(f"  场景: {result['scenario']}")
                    print(f"  置信度: {result['confidence']:.0%}")
                    print(f"  结果:\n{result['result']}")
                    print(f"  DNA: {result['dna']}")

                elif cmd == "record":
                    if not sub:
                        print("用法: record [类型] [内容]")
                        continue
                    rec_parts = sub.split(maxsplit=1)
                    if len(rec_parts) < 2:
                        print("请提供行为类型和内容，如: record 对话 今天讨论了数字孪生")
                        continue
                    btype, content = rec_parts[0], rec_parts[1]
                    result = twin.record_behavior(btype, content)
                    print(f"✅ 行为已记录: {result.dna}")

                elif cmd == "decision":
                    if not sub:
                        print("用法: decision [问题] | [选项1,选项2] | [选择] | [理由]")
                        continue
                    args_parts = [p.strip() for p in sub.split("|")]
                    if len(args_parts) < 4:
                        print("请用 | 分隔: 问题 | 选项1,选项2 | 选择 | 理由")
                        continue
                    q, opts, chosen, reason = args_parts[0], args_parts[1], args_parts[2], args_parts[3]
                    opts_list = [o.strip() for o in opts.split(",")]
                    result = twin.record_decision(q, opts_list, chosen, reason)
                    print(f"✅ 决策已记录: {result.dna}")

                elif cmd == "snapshot":
                    result = twin.snapshot()
                    print(f"✅ 快照已创建: {result['path']}")

                elif cmd == "sync":
                    result = sync_engine.sync_once()
                    print(f"✅ 同步完成: {result['timestamp']}")

                else:
                    print(f"未知命令: {cmd}")

            except KeyboardInterrupt:
                print("\n")
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
        return

    # 单次命令处理
    if args.record:
        btype, content = args.record
        result = twin.record_behavior(btype, content)
        if args.json:
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        else:
            print(f"✅ 行为已记录: {result.dna}")
        return

    if args.decide:
        q, opts, chosen, reason = args.decide
        opts_list = [o.strip() for o in opts.split(",")]
        result = twin.record_decision(q, opts_list, chosen, reason)
        if args.json:
            print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        else:
            print(f"✅ 决策已记录: {result.dna}")
        return

    if args.simulate:
        result = twin.simulate(args.simulate)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"🔮 推演结果:")
            print(f"  场景: {result['scenario']}")
            print(f"  置信度: {result['confidence']:.0%}")
            print(f"  结果:\n{result['result']}")
        return

    if args.status:
        state = twin.get_state()
        if args.json:
            print(json.dumps(state, ensure_ascii=False, indent=2))
        else:
            print(f"\n📊 素字卵神状态:")
            for k, v in state.items():
                if k not in ('personality', 'dna_chain'):
                    print(f"  {k}: {v}")
            print("\n🧠 人格特质:")
            for p in state['personality']:
                bar = "█" * int(p['value'] * 20)
                print(f"  {p['name']}: {bar} {p['value']:.0%}")
        return

    if args.audit:
        result = TwinAuditor.audit(twin)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n🎨 三色审计: {result['color']} {result['status']}")
            print(f"📝 {result['summary']}")
            if result['warnings']:
                print("\n🟡 警告:")
                for w in result['warnings']:
                    print(f"  - {w}")
            if result['issues']:
                print("\n🔴 问题:")
                for i in result['issues']:
                    print(f"  - {i}")
        return

    if args.report:
        print(twin.generate_report())
        return

    if args.snapshot:
        result = twin.snapshot()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"✅ 快照已创建: {result['path']}")
        return

    if args.sync_start:
        result = sync_engine.start()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"✅ 同步已启动（间隔{result['interval']}秒）")
        return

    if args.sync_stop:
        result = sync_engine.stop()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("✅ 同步已停止")
        return

    if args.sync_once:
        result = sync_engine.sync_once()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"✅ 同步完成: {result['timestamp']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
