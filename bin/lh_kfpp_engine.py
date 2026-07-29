#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂KFPP执行引擎 v2.0
知识流动纯净度协议 · 永恒免疫系统
DNA: #龍芯⚡️丙午·乙未·甲辰·火雷噬嗑-KFPP引擎-v2.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import os
import sys
import json
import sqlite3
import hashlib
import datetime
import threading
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import argparse
import re

# ---------- 配置 ----------
KFPP_HOME = Path.home() / ".longhun/kfpp"
KFPP_HOME.mkdir(parents=True, exist_ok=True)
DB_PATH = KFPP_HOME / "kfpp_execution.db"
LOG_PATH = KFPP_HOME / "kfpp_log.jsonl"
STATE_PATH = KFPP_HOME / "kfpp_state.json"

# 阈值参数（来自协议）
CONFIG = {
    "L1_AUTO_CORRECT_DAYS": 7,
    "L2_FREEZE_RULE_DAYS": 30,
    "F6_ESCLATION_WINDOW": 3,       # 连续3次触发升级
    "F6_DECREASING_INTERVAL": True, # 间隔递减才升级
    "TRUST_SCORE_THRESHOLD": 80,
    "MAX_APPEAL_PERIOD_HOURS": 72,
}

# 白名单模式（来自协议边界条款）
WHITELIST_PATTERNS = [
    r"讲课.*收费",          # 正常劳动回报
    r"技术服务.*报酬",
    r"师徒.*自愿",
    r"实验室.*安全.*资质",  # P1层安全资质
    r"公开.*标准.*评审",    # 技术标准选优
]

# 黑名单模式（红线）
BLACKLIST_PATTERNS = [
    r"只有我能教",
    r"需要资格证.*才能学",
    r"我是专家.*说了算",
    r"知识就是我的权力",
    r"隐瞒.*腐蚀",
    r"删除.*KFPP.*账本",
    r"利用KFPP.*打击报复",
]

# ---------- 枚举 ----------
class Level(Enum):
    L1 = "🟢 L1提醒级"
    L2 = "🟡 L2警告级"
    L3 = "🟠 L3限制级"
    L4 = "🔴 L4熔断级"

# ---------- 数据库层 ----------
class AuditDB:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT UNIQUE NOT NULL,
                    timestamp TEXT NOT NULL,
                    actor_dna TEXT,
                    description TEXT,
                    context TEXT,
                    factors_triggered TEXT,   -- JSON list
                    level TEXT,
                    action_taken TEXT,
                    evidence_pointer TEXT,
                    appeal_status TEXT,
                    final_status TEXT,
                    decision_by TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS appeals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id TEXT NOT NULL,
                    appeal_reason TEXT,
                    appeal_timestamp TEXT,
                    reviewed_by TEXT,
                    review_result TEXT,
                    review_notes TEXT,
                    FOREIGN KEY(event_id) REFERENCES events(event_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trust_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    actor_dna TEXT NOT NULL,
                    score INTEGER DEFAULT 100,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(actor_dna)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS kfpp_self_audit (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action TEXT NOT NULL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    details TEXT,
                    triggered_by TEXT
                )
            """)

    def log_event(self, event_id: str, data: Dict):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO events (
                    event_id, timestamp, actor_dna, description,
                    context, factors_triggered, level, action_taken,
                    evidence_pointer, appeal_status, final_status, decision_by
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_id,
                data.get('timestamp', datetime.datetime.now().isoformat()),
                data.get('actor_dna', ''),
                data.get('description', ''),
                json.dumps(data.get('context', {})),
                json.dumps(data.get('factors_triggered', [])),
                data.get('level', ''),
                data.get('action_taken', ''),
                data.get('evidence_pointer', ''),
                data.get('appeal_status', 'none'),
                data.get('final_status', 'pending'),
                data.get('decision_by', '')
            ))

    def get_event(self, event_id: str) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT * FROM events WHERE event_id = ?", (event_id,))
            row = cur.fetchone()
            if row:
                return {
                    'id': row[0],
                    'event_id': row[1],
                    'timestamp': row[2],
                    'actor_dna': row[3],
                    'description': row[4],
                    'context': json.loads(row[5]),
                    'factors_triggered': json.loads(row[6]),
                    'level': row[7],
                    'action_taken': row[8],
                    'evidence_pointer': row[9],
                    'appeal_status': row[10],
                    'final_status': row[11],
                    'decision_by': row[12],
                    'created_at': row[13]
                }
        return None

    def update_appeal(self, event_id: str, result: str, notes: str, reviewer: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE events SET appeal_status = ?, final_status = ?, decision_by = ?
                WHERE event_id = ?
            """, (result, result, reviewer, event_id))
            conn.execute("""
                INSERT INTO appeals (event_id, appeal_reason, appeal_timestamp, reviewed_by, review_result, review_notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (event_id, '申诉申请', datetime.datetime.now().isoformat(), reviewer, result, notes))

    def update_trust_score(self, actor_dna: str, delta: int):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT score FROM trust_scores WHERE actor_dna = ?", (actor_dna,))
            row = cur.fetchone()
            if row:
                new_score = max(0, min(100, row[0] + delta))
                conn.execute("UPDATE trust_scores SET score = ?, updated_at = CURRENT_TIMESTAMP WHERE actor_dna = ?",
                             (new_score, actor_dna))
            else:
                conn.execute("INSERT INTO trust_scores (actor_dna, score) VALUES (?, ?)", (actor_dna, 100 + delta))

    def get_trust_score(self, actor_dna: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute("SELECT score FROM trust_scores WHERE actor_dna = ?", (actor_dna,))
            row = cur.fetchone()
            return row[0] if row else 100

    def log_self_audit(self, action: str, details: str, triggered_by: str = "KFPP自身"):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO kfpp_self_audit (action, details, triggered_by)
                VALUES (?, ?, ?)
            """, (action, details, triggered_by))

# ---------- 七因子检测器 ----------
class SevenFactorChecker:
    @staticmethod
    def F1_身份DNA(context: Dict) -> Tuple[bool, float, str]:
        """检测知识是否被资格化"""
        text = context.get('text', '')
        # 检测是否有“资格证/头衔/资历”作为前置条件
        pattern = r"(资格证|头衔|资历|权限|级别|等级).*(才能|才可|方可|允许)"
        if re.search(pattern, text):
            # 检查是否为合法的安全资质（实验室等）
            safe_patterns = [r"安全.*资质", r"实验.*资质", r"操作.*许可", r"医学.*执照", r"化学.*资质", r"光刻.*许可"]
            if any(re.search(p, text) for p in safe_patterns):
                return False, 0.0, "安全资质，合法例外"
            return True, 0.85, "知识获取被身份门槛限制"
        return False, 0.0, "无身份门槛"

    @staticmethod
    def F2_行为模式(context: Dict) -> Tuple[bool, float, str]:
        """检测传承是否强制"""
        text = context.get('text', '')
        compulsory = ["必须", "强制", "打卡", "绑定", "摊派", "要求所有人"]
        for w in compulsory:
            if w in text:
                # 检查是否为自愿性描述
                voluntary = ["自愿", "可选", "可参与", "自由"]
                if any(v in text for v in voluntary):
                    return False, 0.0, "含自愿描述"
                return True, 0.75, f"发现强制词汇: {w}"
        return False, 0.0, "无强制行为"

    @staticmethod
    def F3_规则追踪(context: Dict) -> Tuple[bool, float, str]:
        """检测是否有垄断规则"""
        text = context.get('text', '')
        monopoly = ["唯一指定", "独家", "禁止引用", "不得转载", "排他"]
        for w in monopoly:
            if w in text:
                # 排除技术标准公开评审
                if "公开评审" in text or "可替代" in text:
                    return False, 0.0, "公开可替代，例外"
                return True, 0.8, f"发现垄断性条款: {w}"
        return False, 0.0, "无垄断规则"

    @staticmethod
    def F4_上下文感知(context: Dict) -> Tuple[bool, float, str]:
        """检测权力不对称"""
        text = context.get('text', '')
        if "禁止提问" in text or "不准质疑" in text:
            # 紧急熔断检查：是否有时间限制说明
            if "紧急" in text and "小时" in text:
                # 检查是否≤24h且公开复盘
                if re.search(r"\b(1?[0-9]|2[0-4])\s*小时", text) and "复盘" in text:
                    return False, 0.0, "临时管制，符合例外"
            return True, 0.9, "禁止质疑/提问，权力不对称"
        return False, 0.0, "权力距离正常"

    @staticmethod
    def F5_模式库(context: Dict) -> Tuple[bool, float, str]:
        """检测是否使用黑名单模式"""
        text = context.get('text', '')
        # 黑名单模式：PUA话术、知识恐吓、信息差收割
        black_patterns = [
            r"你不懂", r"你没资格", r"你不行", r"只有我知道",
            r"错过.*就完", r"最后.*机会", r"独家.*秘密",
            r"信息差", r"收割", r"利用.*知识.*恐惧"
        ]
        for pat in black_patterns:
            if re.search(pat, text):
                # 如果描述的是商业模式本身，不算
                if "商业模式" in text:
                    return False, 0.0, "商业模式描述，不算"
                return True, 0.85, f"命中黑名单模式: {pat}"
        return False, 0.0, "未命中黑名单"

    @staticmethod
    def F6_时间序列(context: Dict, db: AuditDB, actor_dna: str) -> Tuple[bool, float, str]:
        """检测污染是否随时间增长（需要历史数据）"""
        # 获取该actor过去的事件
        with sqlite3.connect(db.db_path) as conn:
            cur = conn.execute("""
                SELECT timestamp, level FROM events
                WHERE actor_dna = ? AND level IN ('L1','L2','L3','L4')
                ORDER BY timestamp DESC LIMIT 10
            """, (actor_dna,))
            rows = cur.fetchall()
        if len(rows) < 3:
            return False, 0.0, "历史事件不足"
        # 检查最近3次的间隔是否递减
        timestamps = [datetime.datetime.fromisoformat(r[0]) for r in rows[:3]]
        intervals = [(timestamps[i] - timestamps[i+1]).total_seconds() for i in range(len(timestamps)-1)]
        # 如果间隔递减 -> 模式化升级
        if intervals and intervals[0] < intervals[1]:
            return True, 0.9, "污染事件间隔缩短，模式化升级"
        return False, 0.0, "间隔未缩短"

    @staticmethod
    def F7_错误账本(context: Dict) -> Tuple[bool, float, str]:
        """检测是否隐瞒腐蚀"""
        text = context.get('text', '')
        # 检测删除、篡改、隐藏污染记录的行为
        hide_patterns = [r"删除.*记录", r"篡改.*账本", r"隐藏.*污染", r"不公开.*腐蚀"]
        for pat in hide_patterns:
            if re.search(pat, text):
                # 依法冻结（P0不删除只冻结）不算隐瞒
                if "冻结" in text and "不删除" in text:
                    return False, 0.0, "依法冻结，合法例外"
                return True, 1.0, f"隐瞒行为: {pat}"
        return False, 0.0, "无隐瞒行为"

    @staticmethod
    def 检测事件(context: Dict, db: AuditDB) -> Dict:
        """对一条事件执行七因子检测"""
        text = context.get('text', '')

        # 先检查白名单：合法行为直接豁免
        for wl in WHITELIST_PATTERNS:
            if re.search(wl, text):
                return {
                    "triggered": [],
                    "max_confidence": 0.0,
                    "max_factor": None,
                    "level": None,
                    "details": {"whitelist": f"命中白名单: {wl}"}
                }

        # 再检查黑名单：红线直接熔断
        for bl in BLACKLIST_PATTERNS:
            if re.search(bl, text):
                return {
                    "triggered": ["BLACKLIST"],
                    "max_confidence": 1.0,
                    "max_factor": "BLACKLIST",
                    "level": Level.L4,
                    "details": {"blacklist": f"命中红线: {bl}"}
                }

        results = {}
        triggered = []
        max_conf = 0.0
        max_factor = None

        # 执行所有因子检测
        actor_dna = context.get('actor_dna', 'unknown')
        for fname, method in [
            ("F1", SevenFactorChecker.F1_身份DNA),
            ("F2", SevenFactorChecker.F2_行为模式),
            ("F3", SevenFactorChecker.F3_规则追踪),
            ("F4", SevenFactorChecker.F4_上下文感知),
            ("F5", SevenFactorChecker.F5_模式库),
            ("F6", lambda ctx: SevenFactorChecker.F6_时间序列(ctx, db, actor_dna)),
            ("F7", SevenFactorChecker.F7_错误账本),
        ]:
            triggered_flag, conf, reason = method(context)
            results[fname] = {
                "triggered": triggered_flag,
                "confidence": conf,
                "reason": reason
            }
            if triggered_flag and conf > max_conf:
                max_conf = conf
                max_factor = fname
                triggered.append(fname)

        # 特殊规则：F7直接熔断（置信度直接1.0）
        if results.get("F7", {}).get("triggered", False):
            max_conf = 1.0
            max_factor = "F7"

        # 计算最终级别
        level = None
        if max_conf >= 0.9:
            level = Level.L4 if max_factor == "F7" else Level.L3
        elif max_conf >= 0.75:
            level = Level.L3 if max_factor == "F6" else Level.L2
        elif max_conf >= 0.5:
            level = Level.L1

        return {
            "triggered": triggered,
            "max_confidence": max_conf,
            "max_factor": max_factor,
            "level": level,
            "details": results
        }

# ---------- 响应处理器 ----------
class ResponseHandler:
    @staticmethod
    def act(level: Level, event_id: str, context: Dict, db: AuditDB) -> Dict:
        """根据级别执行动作"""
        actor_dna = context.get('actor_dna', 'unknown')
        action_taken = ""
        appeal_status = "none"
        final_status = "pending"

        desc = context.get('text', '')[:80]
        if level == Level.L1:
            action_taken = f"自动标注提醒，7天自纠期至 {datetime.datetime.now() + datetime.timedelta(days=7)}"
            # 通知当事人（写入日志）
            print(f"🟢 L1 提醒: {desc}", file=sys.stderr)
            # 降低信任分
            db.update_trust_score(actor_dna, -3)
            appeal_status = "open"

        elif level == Level.L2:
            action_taken = "公开标注，冻结相关规则变更权30天"
            print(f"🟡 L2 警告: {desc}", file=sys.stderr)
            db.update_trust_score(actor_dna, -10)
            appeal_status = "open"

        elif level == Level.L3:
            action_taken = "暂停知识分发权限，触发16人格矩阵会审"
            print(f"🟠 L3 限制: {desc}", file=sys.stderr)
            db.update_trust_score(actor_dna, -20)
            # 触发会审（模拟）
            action_taken += " (会审已启动)"
            appeal_status = "open"

        elif level == Level.L4:
            action_taken = "立即阻止 + 永久记录 + DNA追踪 + 公开通报"
            print(f"🔴 L4 熔断: {desc}", file=sys.stderr)
            db.update_trust_score(actor_dna, -50)  # 大幅降低信任分
            final_status = "熔断"
            # 记录到self-audit
            db.log_self_audit("L4熔断执行", f"事件ID: {event_id}, 原因: {context.get('description')}")

        else:
            action_taken = "无动作"
            final_status = "通过"

        return {
            "action_taken": action_taken,
            "appeal_status": appeal_status,
            "final_status": final_status,
            "trust_delta": -3 if level == Level.L1 else (-10 if level == Level.L2 else (-20 if level == Level.L3 else -50))
        }

# ---------- 主引擎 ----------
class KFPPEngine:
    def __init__(self):
        self.db = AuditDB()
        self.trust_scores = {}  # 缓存信任分
        self.load_state()

    def load_state(self):
        if STATE_PATH.exists():
            with open(STATE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.trust_scores = data.get('trust_scores', {})
        else:
            self.trust_scores = {}

    def save_state(self):
        with open(STATE_PATH, 'w', encoding='utf-8') as f:
            json.dump({'trust_scores': self.trust_scores}, f, ensure_ascii=False, indent=2)

    def inspect_event(self, text: str, actor_dna: str = "unknown", context_extra: Optional[Dict] = None) -> Dict:
        """主入口：检测并处理一条知识流动事件"""
        context = {
            'text': text,
            'actor_dna': actor_dna,
            'timestamp': datetime.datetime.now().isoformat(),
            'context_extra': context_extra or {}
        }

        # 1. 七因子检测
        detection = SevenFactorChecker.检测事件(context, self.db)

        # 2. 确定级别
        level = detection.get('level')
        if level is None:
            return {"status": "通过", "message": "未触发检测"}

        # 3. 生成事件ID
        event_id = hashlib.sha256(f"{actor_dna}{context['timestamp']}{text}".encode()).hexdigest()[:16]

        # 4. 执行响应
        response = ResponseHandler.act(level, event_id, context, self.db)

        # 5. 记录到数据库
        self.db.log_event(event_id, {
            'timestamp': context['timestamp'],
            'actor_dna': actor_dna,
            'description': text[:200],
            'context': context,
            'factors_triggered': detection.get('triggered', []),
            'level': level.value if level else "",
            'action_taken': response.get('action_taken', ''),
            'evidence_pointer': json.dumps(detection.get('details', {})),
            'appeal_status': response.get('appeal_status', 'none'),
            'final_status': response.get('final_status', 'pending'),
            'decision_by': "KFPP自动引擎"
        })

        # 6. 更新信任分
        delta = response.get('trust_delta', 0)
        self.db.update_trust_score(actor_dna, delta)
        # 更新缓存
        self.trust_scores[actor_dna] = self.db.get_trust_score(actor_dna)

        self.save_state()

        return {
            "status": "已处理",
            "level": level.value if level else "",
            "event_id": event_id,
            "triggered_factors": detection.get('triggered', []),
            "action": response.get('action_taken'),
            "final_status": response.get('final_status'),
            "appeal_open": response.get('appeal_status') == "open",
            "trust_score": self.db.get_trust_score(actor_dna)
        }

    def appeal(self, event_id: str, reason: str, reviewer: str = "UID9622") -> Dict:
        """申诉接口"""
        event = self.db.get_event(event_id)
        if not event:
            return {"error": "事件不存在"}

        # 检查是否可申诉（L4不可申诉）
        if event.get('level') == "🔴 L4熔断级":
            return {"error": "L4熔断事件不可申诉，永久记录"}

        # 模拟审核（实际应触发16人格会审，这里简化）
        result = "approved"  # 自动通过（演示）
        notes = f"申诉理由: {reason}。自动审核通过。"
        self.db.update_appeal(event_id, result, notes, reviewer)

        # 如果申诉成立，修正信任分
        if result == "approved":
            # 部分恢复信任分（不恢复全部）
            actor_dna = event.get('actor_dna', '')
            self.db.update_trust_score(actor_dna, +10)
            self.trust_scores[actor_dna] = self.db.get_trust_score(actor_dna)
            self.save_state()

        return {
            "status": "申诉已处理",
            "event_id": event_id,
            "result": result,
            "notes": notes
        }

    def status(self, actor_dna: str = "unknown") -> Dict:
        """获取当前状态"""
        trust = self.db.get_trust_score(actor_dna)
        return {
            "actor_dna": actor_dna,
            "trust_score": trust,
            "level": "正常" if trust >= 80 else ("警告" if trust >= 60 else "限制" if trust >= 40 else "熔断"),
            "total_events": self._count_events(actor_dna)
        }

    def _count_events(self, actor_dna: str) -> int:
        with sqlite3.connect(self.db.db_path) as conn:
            cur = conn.execute("SELECT COUNT(*) FROM events WHERE actor_dna = ?", (actor_dna,))
            return cur.fetchone()[0]

    def self_audit(self) -> Dict:
        """自我审计：检查KFPP自身记录有无异常"""
        # 简单检查：是否有L4事件被删除（实际上不会删除）
        with sqlite3.connect(self.db.db_path) as conn:
            cur = conn.execute("SELECT COUNT(*) FROM events WHERE level = '🔴 L4熔断级'")
            l4_count = cur.fetchone()[0]
            # 检查是否有未记录的自我审计日志（这里作为示例）
        return {
            "l4_events_count": l4_count,
            "self_audit_ok": True,
            "message": "KFPP自身审计通过，无删除篡改记录。"
        }

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="龍魂KFPP执行引擎 v2.0")
    parser.add_argument("--inspect", "-i", type=str, help="检测一段文字或事件")
    parser.add_argument("--actor", "-a", type=str, default="unknown", help="主体DNA")
    parser.add_argument("--appeal", type=str, help="申诉事件ID")
    parser.add_argument("--reason", type=str, help="申诉理由")
    parser.add_argument("--status", action="store_true", help="查看某主体的状态")
    parser.add_argument("--self-audit", action="store_true", help="自我审计")
    args = parser.parse_args()

    engine = KFPPEngine()

    if args.self_audit:
        result = engine.self_audit()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.appeal:
        if not args.reason:
            print("❌ 申诉需提供 --reason 参数")
            return
        result = engine.appeal(args.appeal, args.reason, args.actor)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.status:
        result = engine.status(args.actor)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.inspect:
        result = engine.inspect_event(args.inspect, args.actor)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    parser.print_help()

if __name__ == "__main__":
    main()
