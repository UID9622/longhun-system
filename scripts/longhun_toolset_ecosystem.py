#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自适应工具集生态引擎

把“集思广益”从被动收集升级成主动进化的工具集生态：
  - 每个功能模块是 1，每个用户是 1，每条意见是 1。
  - 功能上不上下下，由真实使用数据打分决定。
  - 系统主动识别用户接触新功能/新用法，弹出 DNA 反馈提醒。
  - 用户一键提交反馈，无需填表，自动关联上下文与身份。
  - 高权重意见自动生成脱敏公开包；低分意见归档不公开。

DNA:#龍芯⚡️2026-06-30-LONGHUN-TOOLSET-ECOSYSTEM-FILE1-v1.0
"""

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HOME = Path.home()
TE_ROOT = HOME / ".longhun" / "toolset_ecosystem"
TE_DB = TE_ROOT / "toolset_ecosystem.db"
PUBLIC_PACKAGES_DIR = TE_ROOT / "public_packages"
DNA_PREFIX = "#龍芯⚡️"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _dna(event: str, seed: str = "") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256(f"{event}|{seed}|{ts}".encode("utf-8")).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}{ts}-{event}-{h}"


def _short_hash(text: str, length: int = 6) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length].upper()


def _safe_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, default=str)


def _parse_duration_ms(start: Optional[str], end: Optional[str]) -> float:
    """计算两个 ISO 时间字符串之间的毫秒数。"""
    if not start or not end:
        return 0.0
    try:
        s = datetime.fromisoformat(start)
        e = datetime.fromisoformat(end)
        return max(0.0, (e - s).total_seconds() * 1000)
    except Exception:
        return 0.0


def _load_module_safely(module_name: str, path: Path):
    try:
        if str(path.parent) not in sys.path:
            sys.path.insert(0, str(path.parent))
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, str(path))
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    except Exception:
        pass
    return None


class ToolsetEcosystemEngine:
    """
    自适应工具集生态引擎。
    """

    # 状态流转阈值（可调）
    ACTIVE_THRESHOLD = 0.6
    DEPRECATE_THRESHOLD = 0.3
    MIN_USERS_FOR_ACTIVE = 2
    REMIND_COOLDOWN_HOURS = 24

    def __init__(self, db_path: Path = TE_DB, founder: str = "UID9622") -> None:
        self.db_path = db_path
        self.founder = founder
        TE_ROOT.mkdir(parents=True, exist_ok=True)
        PUBLIC_PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
        self._conn = self._init_db()
        self._cw_engine = None
        self._load_plugins()

    def _load_plugins(self) -> None:
        cw_path = HOME / "longhun-system" / "scripts" / "longhun_collective_wisdom.py"
        cw_mod = _load_module_safely("collective_wisdom", cw_path)
        if cw_mod:
            try:
                self._cw_engine = cw_mod.CollectiveWisdomEngine()
            except Exception:
                pass

    def _init_db(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")

        # 功能模块注册表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS functions (
                function_id TEXT PRIMARY KEY,
                function_name TEXT NOT NULL,
                version TEXT DEFAULT 'v1.0',
                description TEXT,
                status TEXT DEFAULT 'pending',
                score REAL DEFAULT 0.0,
                compatible_with TEXT DEFAULT '[]',
                incompatible_with TEXT DEFAULT '[]',
                adoption_time TEXT,
                dna TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_func_status ON functions(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_func_score ON functions(score)")

        # 用户使用聚合表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS function_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                function_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0,
                total_duration_ms REAL DEFAULT 0.0,
                satisfaction_sum REAL DEFAULT 0.0,
                satisfaction_count INTEGER DEFAULT 0,
                recommendation_count INTEGER DEFAULT 0,
                last_used_at TEXT,
                first_used_at TEXT,
                UNIQUE(function_id, user_id)
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_usage_func ON function_usage(function_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_usage_user ON function_usage(user_id)")

        # 使用事件明细（append-only）
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usage_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE NOT NULL,
                function_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                duration_ms REAL DEFAULT 0.0,
                context TEXT,
                is_test INTEGER DEFAULT 0,
                dna TEXT,
                timestamp TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_func ON usage_events(function_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_user ON usage_events(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_test ON usage_events(is_test)")

        # 提醒记录
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reminder_id TEXT UNIQUE NOT NULL,
                function_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                context TEXT,
                shown_at TEXT,
                responded_at TEXT,
                feedback_idea_code TEXT,
                is_test INTEGER DEFAULT 0,
                dna TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_reminders_user ON reminders(user_id)")

        # 公开意见包
        conn.execute("""
            CREATE TABLE IF NOT EXISTS opinion_packages (
                package_id TEXT PRIMARY KEY,
                title TEXT,
                idea_codes TEXT,
                public_path TEXT,
                is_test INTEGER DEFAULT 0,
                dna TEXT,
                created_at TEXT
            )
        """)

        conn.commit()
        return conn

    # ---------- 功能注册 ----------
    def register_function(
        self,
        function_name: str,
        version: str = "v1.0",
        description: str = "",
        function_id: Optional[str] = None,
        compatible_with: Optional[List[str]] = None,
        incompatible_with: Optional[List[str]] = None,
        status: str = "pending",
    ) -> Dict[str, Any]:
        """注册一个功能模块。可显式指定 function_id，否则根据名称生成。"""
        if not function_id:
            date = datetime.now(timezone.utc).strftime("%y%m%d")
            safe_name = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", function_name)[:12] or "功能"
            function_id = f"FUNC-{date}-{safe_name}-{_short_hash(function_name + version, 4)}"
        dna = _dna("FUNC-REGISTER", function_id)
        now = _now()
        record = {
            "function_id": function_id,
            "function_name": function_name,
            "version": version,
            "description": description,
            "status": status,
            "score": 0.0,
            "compatible_with": _safe_json(compatible_with or []),
            "incompatible_with": _safe_json(incompatible_with or []),
            "adoption_time": now if status == "active" else None,
            "dna": dna,
            "created_at": now,
            "updated_at": now,
        }
        try:
            self._conn.execute(
                """INSERT INTO functions
                   (function_id, function_name, version, description, status, score,
                    compatible_with, incompatible_with, adoption_time, dna, created_at, updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    record["function_id"],
                    record["function_name"],
                    record["version"],
                    record["description"],
                    record["status"],
                    record["score"],
                    record["compatible_with"],
                    record["incompatible_with"],
                    record["adoption_time"],
                    record["dna"],
                    record["created_at"],
                    record["updated_at"],
                ),
            )
            self._conn.commit()
        except sqlite3.IntegrityError:
            return {"ok": False, "code": "DUPLICATE", "message": "功能 ID 已存在"}
        return {"ok": True, "code": "REGISTERED", "message": f"🟢 功能已注册：{function_id}", "record": record}

    def get_function(self, function_id: str) -> Optional[Dict[str, Any]]:
        row = self._conn.execute("SELECT * FROM functions WHERE function_id=?", (function_id,)).fetchone()
        if not row:
            return None
        rec = dict(row)
        rec["compatible_with"] = json.loads(rec.get("compatible_with") or "[]")
        rec["incompatible_with"] = json.loads(rec.get("incompatible_with") or "[]")
        return rec

    # ---------- 使用记录 ----------
    def record_usage(
        self,
        function_id: str,
        user_id: str,
        event_type: str = "use",
        duration_ms: float = 0.0,
        context: str = "",
        is_test: bool = False,
    ) -> Dict[str, Any]:
        """记录一次功能使用事件，并更新聚合统计。"""
        # 自动注册未知功能（兜底），使用调用方传入的标识作为稳定 function_id
        func = self.get_function(function_id)
        if not func:
            reg = self.register_function(
                function_name=function_id,
                function_id=function_id,
                description="自动注册的功能模块",
            )
            if not reg.get("ok"):
                # 可能并发或重入导致已存在，再次尝试读取
                func = self.get_function(function_id)
                if not func:
                    return reg
            if not func:
                func = self.get_function(function_id)

        event_id = f"EVT-{datetime.now(timezone.utc).strftime('%y%m%d')}-{_short_hash(function_id + user_id + _now(), 6)}"
        dna = _dna("USAGE-EVENT", event_id)
        now = _now()

        self._conn.execute(
            """INSERT INTO usage_events
               (event_id, function_id, user_id, event_type, duration_ms, context, is_test, dna, timestamp)
               VALUES(?,?,?,?,?,?,?,?,?)""",
            (event_id, function_id, user_id, event_type, duration_ms, context, int(is_test), dna, now),
        )

        # 更新聚合
        row = self._conn.execute(
            "SELECT * FROM function_usage WHERE function_id=? AND user_id=?",
            (function_id, user_id),
        ).fetchone()
        if row:
            rec = dict(row)
            new_count = rec["usage_count"] + 1
            new_total = rec["total_duration_ms"] + duration_ms
            self._conn.execute(
                """UPDATE function_usage
                   SET usage_count=?, total_duration_ms=?, last_used_at=?
                   WHERE function_id=? AND user_id=?""",
                (new_count, new_total, now, function_id, user_id),
            )
        else:
            self._conn.execute(
                """INSERT INTO function_usage
                   (function_id, user_id, usage_count, total_duration_ms, last_used_at, first_used_at)
                   VALUES(?,?,?,?,?,?)""",
                (function_id, user_id, 1, duration_ms, now, now),
            )
        self._conn.commit()

        # 重新打分并尝试状态流转
        self._rescore(function_id)
        self._transition_status(function_id)

        return {
            "ok": True,
            "code": "USAGE_RECORDED",
            "event_id": event_id,
            "function_id": function_id,
            "dna": dna,
        }

    def record_satisfaction(
        self,
        function_id: str,
        user_id: str,
        score: float,
        is_test: bool = False,
    ) -> Dict[str, Any]:
        """用户给功能满意度打分（0-10）。"""
        score = max(0.0, min(10.0, score))
        self.record_usage(function_id, user_id, event_type="rating", duration_ms=0.0, context=f"满意度:{score}", is_test=is_test)
        self._conn.execute(
            """UPDATE function_usage
               SET satisfaction_sum = satisfaction_sum + ?, satisfaction_count = satisfaction_count + 1
               WHERE function_id=? AND user_id=?""",
            (score, function_id, user_id),
        )
        self._conn.commit()
        self._rescore(function_id)
        return {"ok": True, "code": "SATISFACTION_RECORDED", "function_id": function_id, "score": score}

    def record_recommendation(
        self,
        function_id: str,
        user_id: str,
        is_test: bool = False,
    ) -> Dict[str, Any]:
        """用户推荐该功能给别人。"""
        self.record_usage(function_id, user_id, event_type="recommend", duration_ms=0.0, context="推荐", is_test=is_test)
        self._conn.execute(
            "UPDATE function_usage SET recommendation_count = recommendation_count + 1 WHERE function_id=? AND user_id=?",
            (function_id, user_id),
        )
        self._conn.commit()
        self._rescore(function_id)
        return {"ok": True, "code": "RECOMMENDATION_RECORDED", "function_id": function_id}

    # ---------- 打分与状态流转 ----------
    def _rescore(self, function_id: str) -> float:
        rows = self._conn.execute(
            "SELECT * FROM function_usage WHERE function_id=?", (function_id,)
        ).fetchall()
        if not rows:
            return 0.0

        total_usage = sum(r["usage_count"] for r in rows)
        total_recs = sum(r["recommendation_count"] for r in rows)
        sat_count = sum(r["satisfaction_count"] for r in rows)
        sat_sum = sum(r["satisfaction_sum"] for r in rows)
        user_count = len(rows)

        # 各因子归一化到 0-1
        usage_score = min(total_usage / 50.0, 1.0)  # 50 次使用封顶
        rec_score = min(total_recs / 10.0, 1.0)    # 10 次推荐封顶
        sat_score = (sat_sum / sat_count) / 10.0 if sat_count > 0 else 0.5
        user_score = min(user_count / 10.0, 1.0)   # 10 个用户封顶

        # 加权
        score = (
            usage_score * 0.35 +
            sat_score * 0.35 +
            rec_score * 0.15 +
            user_score * 0.15
        )
        score = round(score, 4)

        self._conn.execute(
            "UPDATE functions SET score=?, updated_at=? WHERE function_id=?",
            (score, _now(), function_id),
        )
        self._conn.commit()
        return score

    def _transition_status(self, function_id: str) -> str:
        func = self.get_function(function_id)
        if not func:
            return "unknown"
        status = func["status"]
        score = func["score"]
        user_count = self._conn.execute(
            "SELECT COUNT(DISTINCT user_id) FROM function_usage WHERE function_id=?",
            (function_id,),
        ).fetchone()[0]

        new_status = status
        if status == "pending" and score >= self.ACTIVE_THRESHOLD and user_count >= self.MIN_USERS_FOR_ACTIVE:
            new_status = "active"
        elif status == "active" and score < self.DEPRECATE_THRESHOLD:
            new_status = "deprecated"
        elif status == "deprecated" and score >= self.ACTIVE_THRESHOLD and user_count >= self.MIN_USERS_FOR_ACTIVE:
            new_status = "active"

        if new_status != status:
            adoption_time = _now() if new_status == "active" else func.get("adoption_time")
            self._conn.execute(
                "UPDATE functions SET status=?, adoption_time=?, updated_at=? WHERE function_id=?",
                (new_status, adoption_time, _now(), function_id),
            )
            self._conn.commit()
        return new_status

    def get_recommendation(self, function_id_a: str, function_id_b: str) -> Dict[str, Any]:
        """判断两个功能是否可共存，推荐高分版本。"""
        a = self.get_function(function_id_a)
        b = self.get_function(function_id_b)
        if not a or not b:
            return {"ok": False, "message": "功能不存在"}

        incompatible = function_id_b in a.get("incompatible_with", [])
        if not incompatible:
            return {"ok": True, "coexist": True, "message": "两个功能可共存"}

        winner = a if a["score"] >= b["score"] else b
        return {
            "ok": True,
            "coexist": False,
            "recommended": winner["function_id"],
            "reason": f"{winner['function_name']} 当前分数更高（{winner['score']:.2f}），建议优先使用",
        }

    # ---------- 主动提醒 ----------
    def should_remind(self, function_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """判断是否应该向用户弹出反馈提醒。"""
        func = self.get_function(function_id)
        if not func:
            return None

        # 新功能（pending）或用户首次使用
        user_row = self._conn.execute(
            "SELECT * FROM function_usage WHERE function_id=? AND user_id=?",
            (function_id, user_id),
        ).fetchone()
        if not user_row:
            return None
        user_usage = dict(user_row)

        # 冷却期：同一功能 24 小时内不重复提醒
        last_reminder = self._conn.execute(
            "SELECT MAX(shown_at) FROM reminders WHERE function_id=? AND user_id=?",
            (function_id, user_id),
        ).fetchone()[0]
        if last_reminder:
            try:
                if datetime.now(timezone.utc) - datetime.fromisoformat(last_reminder) < timedelta(hours=self.REMIND_COOLDOWN_HOURS):
                    return None
            except Exception:
                pass

        # 触发条件：pending 状态 或 用户使用次数 <= 3
        if func["status"] == "pending" or user_usage["usage_count"] <= 3:
            return {
                "function_id": function_id,
                "function_name": func["function_name"],
                "usage_count": user_usage["usage_count"],
                "reason": "新功能/新用法接触提醒",
            }
        return None

    def create_reminder(self, function_id: str, user_id: str, context: str = "", is_test: bool = False) -> Dict[str, Any]:
        reminder_id = f"REM-{datetime.now(timezone.utc).strftime('%y%m%d')}-{_short_hash(function_id + user_id + _now(), 6)}"
        dna = _dna("REMINDER", reminder_id)
        now = _now()
        self._conn.execute(
            """INSERT INTO reminders
               (reminder_id, function_id, user_id, context, shown_at, is_test, dna)
               VALUES(?,?,?,?,?,?,?)""",
            (reminder_id, function_id, user_id, context, now, int(is_test), dna),
        )
        self._conn.commit()
        return {
            "ok": True,
            "reminder_id": reminder_id,
            "dna": dna,
            "message": f"🟢 已为 {user_id} 创建 {function_id} 的反馈提醒",
        }

    # ---------- 一键 DNA 反馈 ----------
    def submit_feedback(
        self,
        user_id: str,
        function_id: str,
        content: str,
        context: str = "",
        level: str = "L0",
        is_test: bool = False,
    ) -> Dict[str, Any]:
        """用户一键提交功能反馈，自动关联功能上下文和 DNA。"""
        if not self._cw_engine:
            return {"ok": False, "code": "CW_NOT_LOADED", "message": "集思广益引擎未加载"}

        full_content = f"【功能反馈·{function_id}】\n{content}"
        if context:
            full_content += f"\n上下文：{context}"

        result = self._cw_engine.submit(
            full_content,
            submitter=user_id,
            level=level,
            source="toolset_feedback",
        )

        # 关联提醒（如果有）
        if result.get("ok"):
            idea_code = result["record"]["idea_code"]
            self._conn.execute(
                "UPDATE reminders SET feedback_idea_code=? WHERE function_id=? AND user_id=? AND feedback_idea_code IS NULL",
                (idea_code, function_id, user_id),
            )
            self._conn.commit()

            # 记录反馈事件
            self.record_usage(function_id, user_id, event_type="feedback", context=f"意见码:{idea_code}", is_test=is_test)

        return result

    # ---------- 公开意见包 ----------
    def generate_public_package(
        self,
        title: str = "龍魂工具集 · 公开意见集",
        min_weight: float = 2.0,
        limit: int = 50,
        is_test: bool = False,
    ) -> Dict[str, Any]:
        """生成脱敏公开意见包。"""
        if not self._cw_engine:
            return {"ok": False, "code": "CW_NOT_LOADED", "message": "集思广益引擎未加载"}

        ideas = self._cw_engine.list_ideas(status=None, sort_by="weight", limit=limit * 2)
        selected = [i for i in ideas if i.get("weight", 0) >= min_weight and i.get("status") in ("archived", "adopted", "verified")]
        selected = selected[:limit]

        if not selected:
            return {"ok": False, "code": "NO_IDEAS", "message": "没有满足条件的公开意见"}

        package_id = f"PKG-{datetime.now(timezone.utc).strftime('%y%m%d')}-{_short_hash(title, 6)}"
        dna = _dna("PUBLIC-PACKAGE", package_id)

        # 脱敏
        deidentified = []
        for i in selected:
            deidentified.append({
                "idea_code": i["idea_code"],
                "content": i["content"],
                "status": i["status"],
                "weight": i["weight"],
                "mention_count": i["mention_count"],
                "verified_count": i["verified_count"],
                "submitter_level": i["level"],
                # 不暴露 submitter 真实身份
            })

        md_lines = [
            f"# {title}",
            "",
            f"**DNA**: `{dna}`",
            f"**生成时间**: {_now()}",
            f"**意见数**: {len(deidentified)}",
            "",
            "---",
            "",
        ]
        for idx, item in enumerate(deidentified, 1):
            md_lines.append(f"## {idx}. {item['idea_code']}")
            md_lines.append(f"- 状态：{item['status']} · 权重：{item['weight']:.2f}")
            md_lines.append(f"- 提及 {item['mention_count']} 次 · 验证 {item['verified_count']} 次")
            md_lines.append("")
            md_lines.append(f"{item['content']}")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")

        public_path = PUBLIC_PACKAGES_DIR / f"{package_id}.md"
        public_path.write_text("\n".join(md_lines), encoding="utf-8")

        self._conn.execute(
            """INSERT INTO opinion_packages
               (package_id, title, idea_codes, public_path, is_test, dna, created_at)
               VALUES(?,?,?,?,?,?,?)""",
            (
                package_id,
                title,
                _safe_json([i["idea_code"] for i in selected]),
                str(public_path),
                int(is_test),
                dna,
                _now(),
            ),
        )
        self._conn.commit()

        return {
            "ok": True,
            "code": "PACKAGE_GENERATED",
            "package_id": package_id,
            "dna": dna,
            "public_path": str(public_path),
            "idea_count": len(deidentified),
        }

    # ---------- 统计 ----------
    def stats(self) -> Dict[str, Any]:
        func_count = self._conn.execute("SELECT COUNT(*) FROM functions").fetchone()[0]
        active_count = self._conn.execute("SELECT COUNT(*) FROM functions WHERE status='active'").fetchone()[0]
        pending_count = self._conn.execute("SELECT COUNT(*) FROM functions WHERE status='pending'").fetchone()[0]
        event_count = self._conn.execute("SELECT COUNT(*) FROM usage_events WHERE is_test=0").fetchone()[0]
        reminder_count = self._conn.execute("SELECT COUNT(*) FROM reminders WHERE is_test=0").fetchone()[0]
        package_count = self._conn.execute("SELECT COUNT(*) FROM opinion_packages WHERE is_test=0").fetchone()[0]
        return {
            "functions": {"total": func_count, "active": active_count, "pending": pending_count},
            "usage_events": event_count,
            "reminders": reminder_count,
            "public_packages": package_count,
            "db_path": str(self.db_path),
            "dna": _dna("TE-STATS"),
        }

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
        if self._cw_engine:
            self._cw_engine.close()
            self._cw_engine = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂自适应工具集生态引擎")
    parser.add_argument("--register", type=str, help="注册功能名称")
    parser.add_argument("--version", default="v1.0", help="功能版本")
    parser.add_argument("--description", default="", help="功能描述")
    parser.add_argument("--use", type=str, help="记录使用：功能ID")
    parser.add_argument("--user", default="UID9622", help="用户ID")
    parser.add_argument("--rating", type=float, help="满意度打分 0-10")
    parser.add_argument("--recommend", action="store_true", help="记录推荐")
    parser.add_argument("--feedback", type=str, help="提交反馈内容")
    parser.add_argument("--package", action="store_true", help="生成公开意见包")
    parser.add_argument("--stats", action="store_true", help="统计")
    parser.add_argument("--test", action="store_true", help="标记为测试数据")
    args = parser.parse_args()

    engine = ToolsetEcosystemEngine()

    if args.register:
        result = engine.register_function(args.register, args.version, args.description)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.use:
        result = engine.record_usage(args.use, args.user, is_test=args.test)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
        # 尝试提醒
        remind = engine.should_remind(args.use, args.user)
        if remind:
            engine.create_reminder(args.use, args.user, context="命令行测试", is_test=args.test)
            print("\n提醒触发：", json.dumps(remind, ensure_ascii=False, indent=2, default=str))
    elif args.rating is not None and args.use:
        result = engine.record_satisfaction(args.use, args.user, args.rating, is_test=args.test)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.recommend and args.use:
        result = engine.record_recommendation(args.use, args.user, is_test=args.test)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.feedback and args.use:
        result = engine.submit_feedback(args.user, args.use, args.feedback, is_test=args.test)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.package:
        result = engine.generate_public_package(is_test=args.test)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.stats:
        print(json.dumps(engine.stats(), ensure_ascii=False, indent=2, default=str))
    else:
        print(__doc__)
        print("\n当前统计：", json.dumps(engine.stats(), ensure_ascii=False, indent=2, default=str))

    engine.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
