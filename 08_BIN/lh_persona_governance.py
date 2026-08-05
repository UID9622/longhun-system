#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 人格治理引擎 v2.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-PERSONA-GOVERNANCE-v2.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 人格执行历史管理（只追加，不删除）
  2. 职责冲突检测与解决
  3. 权限继承链管理
  4. 三色审计标记冲突
  5. DNA追溯历史记录

用法：
  python3 bin/lh_persona_governance.py --resolve-conflicts   # 解决历史冲突
  python3 bin/lh_persona_governance.py --assign-duty P01     # 分配职责给P01
  python3 bin/lh_persona_governance.py --inherit P00 P01     # P01继承P00配置
  python3 bin/lh_persona_governance.py --audit-history       # 审计所有历史
  python3 bin/lh_persona_governance.py --stats               # 统计状态
  python3 bin/lh_persona_governance.py --review-history      # 回顾历史
"""

import os
import sys
import json
import sqlite3
import hashlib
import datetime
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

# ============================================================
# 固定锚点（不可篡改）
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path.home() / "longhun-system"
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "persona_governance.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def rows_to_dict(rows):
    """将 sqlite3.Row 转为纯 dict，确保 JSON 可序列化。
    sqlite3.Row 不支持 json.dumps()，所有 fetchone/fetchall 结果必须过此层。
    """
    if rows is None:
        return []
    if isinstance(rows, list):
        return [dict(r) for r in rows]
    if hasattr(rows, 'keys'):
        return dict(rows)
    return {}


# ============================================================
# 数据库初始化（只追加历史）
# ============================================================

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 1. 人格执行历史表（只追加，不删除）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS execution_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id TEXT NOT NULL,
            action TEXT NOT NULL,
            target TEXT,
            parameters TEXT,
            dna_trace TEXT NOT NULL,
            tricolor_status TEXT DEFAULT '🟢',
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            conflict_marker INTEGER DEFAULT 0
        )
    ''')

    # 2. 职责分配表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS duty_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id TEXT NOT NULL UNIQUE,
            primary_duty TEXT,
            secondary_duties TEXT,
            trigger_keywords TEXT,
            priority INTEGER DEFAULT 50,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            assigned_by TEXT DEFAULT 'system'
        )
    ''')

    # 3. 权限继承链
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inheritance_chain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            child_persona TEXT NOT NULL,
            parent_persona TEXT NOT NULL,
            inherit_config TEXT DEFAULT 'all',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            active INTEGER DEFAULT 1,
            UNIQUE(child_persona, parent_persona)
        )
    ''')

    # 4. 人格治理审计日志（只追加）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS governance_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            persona_id TEXT,
            event_type TEXT,
            description TEXT,
            dna_trace TEXT NOT NULL,
            tricolor_status TEXT DEFAULT '🟢',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    return True

# ============================================================
# DNA追溯生成
# ============================================================

def generate_dna(persona_id: str, event_type: str = "EXEC") -> str:
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = hashlib.md5(f"{persona_id}{now}{event_type}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{now}-{persona_id}-{event_type}-{suffix}"

# ============================================================
# ROOT_CARD生成
# ============================================================

def generate_root_card(action: str, status: str = "🟢", data_level: str = "L1_INTERNAL") -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
【ROOT_CARD｜人格治理审计】
Action: {action}
Status: {status}
DataLevel: {data_level}
Timestamp: {now}
DNA: {generate_dna('ROOT', 'GOV')}
CONFIRM: {CONFIRM}
SEAL: {SEAL}
GPG: {GPG}
"""

# ============================================================
# 核心引擎
# ============================================================

class PersonaGovernance:
    def __init__(self):
        if not DB_PATH.exists():
            init_db()
        self.conn = sqlite3.connect(str(DB_PATH))
        self.conn.row_factory = sqlite3.Row
        self.conflicts = []

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    # ---------- 1. 记录执行历史（只追加） ----------
    def record_execution(self, persona_id: str, action: str, target: str = "",
                         parameters: Dict = None, dna: str = None) -> Dict:
        if dna is None:
            dna = generate_dna(persona_id, "EXEC")
        params_json = json.dumps(parameters or {}, ensure_ascii=False)
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO execution_history (persona_id, action, target, parameters, dna_trace)
            VALUES (?, ?, ?, ?, ?)
        ''', (persona_id, action, target, params_json, dna))
        self.conn.commit()
        return {
            "status": "recorded",
            "persona_id": persona_id,
            "dna": dna,
            "action": action,
            "id": cursor.lastrowid,
            "confirm": CONFIRM
        }

    # ---------- 2. 冲突检测 ----------
    def detect_conflicts(self) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT h1.*, h2.id as conflict_id, h2.dna_trace as conflict_dna
            FROM execution_history h1
            JOIN execution_history h2 
            ON h1.persona_id = h2.persona_id 
            AND h1.action = h2.action
            AND h1.target = h2.target
            AND h1.id < h2.id
            AND julianday(h2.executed_at) - julianday(h1.executed_at) < 1
            WHERE h1.conflict_marker = 0
            ORDER BY h1.id
        ''')
        rows = cursor.fetchall()
        raw = rows_to_dict(rows)
        conflicts = []
        for c in raw:
            conflicts.append({
                "original_id": c["id"],
                "conflict_id": c["conflict_id"],
                "persona_id": c["persona_id"],
                "action": c["action"],
                "target": c["target"],
                "original_dna": c["dna_trace"],
                "conflict_dna": c["conflict_dna"],
                "executed_at": c["executed_at"]
            })
            cursor.execute(
                "UPDATE execution_history SET conflict_marker = 1 WHERE id = ?",
                (c["conflict_id"],)
            )
        self.conn.commit()
        self.conflicts = conflicts
        return conflicts

    # ---------- 3. 解决冲突 ----------
    def resolve_conflicts(self, resolution: str = "keep_new") -> Dict:
        conflicts = self.detect_conflicts()
        if not conflicts:
            return {"status": "ok", "message": "无冲突需要解决", "count": 0, "confirm": CONFIRM}

        resolved = 0
        cursor = self.conn.cursor()
        for c in conflicts:
            cursor.execute('''
                UPDATE execution_history 
                SET conflict_marker = 2, 
                    dna_trace = dna_trace || '-RESOLVED'
                WHERE id = ?
            ''', (c["original_id"],))
            resolved += 1

            cursor.execute('''
                INSERT INTO governance_audit (persona_id, event_type, description, dna_trace, tricolor_status)
                VALUES (?, 'resolve_conflict', ?, ?, '🟢')
            ''', (
                c["persona_id"],
                f"解决冲突: 保留 {c['conflict_dna']}，标记 {c['original_dna']} 为已解决",
                generate_dna(c["persona_id"], "RESOLVE")
            ))

        self.conn.commit()
        return {
            "status": "success",
            "resolved": resolved,
            "total": len(conflicts),
            "confirm": CONFIRM
        }

    # ---------- 4. 分配职责 ----------
    def assign_duty(self, persona_id: str, primary: str, secondary: str = "",
                    triggers: str = "", priority: int = 50) -> Dict:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO duty_assignments 
            (persona_id, primary_duty, secondary_duties, trigger_keywords, priority, assigned_at, assigned_by)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, 'system')
        ''', (persona_id, primary, secondary, triggers, priority))

        self.conn.commit()
        return {
            "status": "assigned",
            "persona_id": persona_id,
            "primary_duty": primary,
            "dna": generate_dna(persona_id, "DUTY"),
            "confirm": CONFIRM
        }

    # ---------- 5. 权限继承 ----------
    def set_inheritance(self, child: str, parent: str, config: str = "all") -> Dict:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO inheritance_chain (child_persona, parent_persona, inherit_config, active)
            VALUES (?, ?, ?, 1)
        ''', (child, parent, config))
        self.conn.commit()
        return {
            "status": "inheritance_set",
            "child": child,
            "parent": parent,
            "config": config,
            "dna": generate_dna(child, "INHERIT"),
            "confirm": CONFIRM
        }

    # ---------- 6. 获取继承链 ----------
    def get_inheritance_chain(self, persona_id: str) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute('''
            WITH RECURSIVE chain AS (
                SELECT child_persona, parent_persona, inherit_config, 1 as level
                FROM inheritance_chain WHERE child_persona = ?
                UNION ALL
                SELECT ic.child_persona, ic.parent_persona, ic.inherit_config, c.level + 1
                FROM inheritance_chain ic
                JOIN chain c ON ic.child_persona = c.parent_persona
                WHERE c.level < 10
            )
            SELECT * FROM chain
        ''', (persona_id,))
        rows = cursor.fetchall()
        return rows_to_dict(rows)

    # ---------- 7. 审计历史 ----------
    def audit_history(self, persona_id: str = None, limit: int = 50) -> Dict:
        cursor = self.conn.cursor()
        query = "SELECT * FROM execution_history"
        params = []
        if persona_id:
            query += " WHERE persona_id = ?"
            params.append(persona_id)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        history = rows_to_dict(rows)

        for h in history:
            if h.get("conflict_marker", 0) == 1:
                h["tricolor_status"] = "🟡"
            elif h.get("conflict_marker", 0) == 2:
                h["tricolor_status"] = "🔴"
            else:
                h["tricolor_status"] = "🟢"

        return {
            "total": len(history),
            "history": history,
            "tricolor_summary": {
                "🟢": sum(1 for h in history if h.get("tricolor_status") == "🟢"),
                "🟡": sum(1 for h in history if h.get("tricolor_status") == "🟡"),
                "🔴": sum(1 for h in history if h.get("tricolor_status") == "🔴")
            },
            "confirm": CONFIRM
        }

    # ---------- 8. 统计状态 ----------
    def get_stats(self) -> Dict:
        cursor = self.conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM execution_history")
        total_history = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM execution_history WHERE conflict_marker > 0")
        conflicts = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM duty_assignments")
        duties = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM inheritance_chain WHERE active = 1")
        inheritances = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM governance_audit")
        audit_entries = cursor.fetchone()[0]

        return {
            "total_history": total_history,
            "conflicts": conflicts,
            "duty_assignments": duties,
            "inheritance_chain": inheritances,
            "audit_entries": audit_entries,
            "status": "🟢" if conflicts == 0 else "🟡",
            "confirm": CONFIRM
        }

    # ---------- 9. 回顾历史 ----------
    def review_history(self, persona_id: str = None, days: int = 7) -> str:
        cursor = self.conn.cursor()
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()

        query = '''
            SELECT h.*, d.primary_duty
            FROM execution_history h
            LEFT JOIN duty_assignments d ON h.persona_id = d.persona_id
            WHERE h.executed_at > ?
        '''
        params = [cutoff]
        if persona_id:
            query += " AND h.persona_id = ?"
            params.append(persona_id)
        query += " ORDER BY h.id DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        if not rows:
            return f"📭 过去 {days} 天内无执行记录"

        lines = []
        lines.append(f"# 🐉 人格执行历史回顾 (过去{days}天)")
        lines.append(f"DNA: {generate_dna('REVIEW', 'HIST')}")
        lines.append(f"CONFIRM: {CONFIRM}")
        lines.append("")
        lines.append("| 时间 | 人格 | 操作 | 目标 | DNA | 状态 |")
        lines.append("|------|------|------|------|-----|------|")

        for row in rows:
            status = "🟢" if row["conflict_marker"] == 0 else ("🟡" if row["conflict_marker"] == 1 else "🔴")
            lines.append(
                f"| {row['executed_at'][:16] if row['executed_at'] else '-'} "
                f"| {row['persona_id']} | {row['action']} "
                f"| {row['target'] or '-'} "
                f"| {row['dna_trace'][:20]}... | {status} |"
            )

        return "\n".join(lines)

    # ---------- 9b. 回顾历史 (JSON输出) ----------
    def _review_history_json(self, persona_id: str = None, days: int = 7) -> List[Dict]:
        """返回结构化dict列表，供 --json 模式使用"""
        cursor = self.conn.cursor()
        cutoff = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()

        query = '''
            SELECT h.*, d.primary_duty
            FROM execution_history h
            LEFT JOIN duty_assignments d ON h.persona_id = d.persona_id
            WHERE h.executed_at > ?
        '''
        params = [cutoff]
        if persona_id:
            query += " AND h.persona_id = ?"
            params.append(persona_id)
        query += " ORDER BY h.id DESC"

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows_to_dict(rows)

    # ---------- 10. 清理冲突标记 ----------
    def clear_conflicts(self, persona_id: str = None) -> Dict:
        cursor = self.conn.cursor()
        if persona_id:
            cursor.execute(
                "UPDATE execution_history SET conflict_marker = 0 WHERE persona_id = ? AND conflict_marker = 2",
                (persona_id,)
            )
        else:
            cursor.execute("UPDATE execution_history SET conflict_marker = 0 WHERE conflict_marker = 2")
        affected = cursor.rowcount
        self.conn.commit()
        return {"status": "cleared", "affected": affected, "confirm": CONFIRM}


# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 人格治理引擎 v2.1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-PERSONA-GOVERNANCE-v2.1
CONFIRM: {CONFIRM}
GPG: {GPG}
示例:
  lh persona-governance --detect-conflicts
  lh persona-governance --resolve-conflicts
  lh persona-governance --assign-duty P01 --primary "战略推演" --triggers "推演,战略"
  lh persona-governance --inherit P01 --from P00
  lh persona-governance --audit-history --persona P01
  lh persona-governance --review-history --days 7
  lh persona-governance --stats --json | jq .
        """
    )

    parser.add_argument("--detect-conflicts", action="store_true", help="检测冲突")
    parser.add_argument("--resolve-conflicts", action="store_true", help="解决冲突")
    parser.add_argument("--assign-duty", type=str, help="分配职责 (人格ID)")
    parser.add_argument("--primary", type=str, default="", help="主要职责")
    parser.add_argument("--secondary", type=str, default="", help="次要职责")
    parser.add_argument("--triggers", type=str, default="", help="触发关键词")
    parser.add_argument("--priority", type=int, default=50, help="优先级(1-100)")
    parser.add_argument("--inherit", type=str, help="设置继承 (子人格)")
    parser.add_argument("--from", dest="from_persona", type=str, help="父人格")
    parser.add_argument("--audit-history", action="store_true", help="审计历史")
    parser.add_argument("--persona", type=str, help="人格ID (配合其他命令)")
    parser.add_argument("--review-history", action="store_true", help="回顾历史")
    parser.add_argument("--days", type=int, default=7, help="回顾天数")
    parser.add_argument("--record", type=str, help="记录执行 (人格ID)")
    parser.add_argument("--action", type=str, default="unknown", help="操作名称")
    parser.add_argument("--target", type=str, default="", help="目标")
    parser.add_argument("--stats", action="store_true", help="统计状态")
    parser.add_argument("--clear-conflicts", action="store_true", help="清理已解决的冲突标记")
    parser.add_argument("--json", action="store_true", help="纯JSON输出（不含ROOT_CARD，适合管道|jq）")

    args = parser.parse_args()
    gov = PersonaGovernance()
    use_json = args.json
    any_cmd = False

    if not DB_PATH.exists():
        init_db()
        if use_json:
            print(json.dumps({"status": "initialized", "confirm": CONFIRM}, ensure_ascii=False))
        else:
            print("✅ 人格治理数据库已初始化")
            print(generate_root_card("INIT", "🟢"))

    if args.detect_conflicts:
        any_cmd = True
        conflicts = gov.detect_conflicts()
        if use_json:
            print(json.dumps({"conflicts": conflicts, "count": len(conflicts),
                              "status": "🟡" if conflicts else "🟢", "confirm": CONFIRM},
                             ensure_ascii=False, indent=2))
        else:
            if conflicts:
                print(f"⚠️ 发现 {len(conflicts)} 个冲突:")
                for c in conflicts:
                    print(f"  {c['persona_id']}: {c['action']} → {c['target']} ({c['original_dna'][:20]}...)")
            else:
                print("✅ 无冲突")
            print(generate_root_card("DETECT", "🟢"))

    if args.resolve_conflicts:
        any_cmd = True
        result = gov.resolve_conflicts()
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print(generate_root_card("RESOLVE", "🟢"))

    if args.assign_duty and args.primary:
        any_cmd = True
        result = gov.assign_duty(args.assign_duty, args.primary, args.secondary, args.triggers, args.priority)
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print(generate_root_card("ASSIGN", "🟢"))

    if args.inherit and args.from_persona:
        any_cmd = True
        result = gov.set_inheritance(args.inherit, args.from_persona)
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print(generate_root_card("INHERIT", "🟢"))

    if args.audit_history:
        any_cmd = True
        result = gov.audit_history(args.persona)
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("📋 审计结果:")
            print(f"  总记录: {result['total']}")
            print(f"  三色分布: 🟢{result['tricolor_summary']['🟢']} 🟡{result['tricolor_summary']['🟡']} 🔴{result['tricolor_summary']['🔴']}")
            if result["history"]:
                print("\n  最近记录:")
                for h in result["history"][:10]:
                    status = h.get("tricolor_status", "🟢")
                    print(f"    {status} {h['persona_id']}: {h['action']} → {h.get('target', '-')} ({h['dna_trace'][:20]}...)")
            print(generate_root_card("AUDIT", "🟢"))

    if args.review_history:
        any_cmd = True
        if use_json:
            rows = gov._review_history_json(args.persona, args.days)
            print(json.dumps({"review": rows, "count": len(rows), "confirm": CONFIRM},
                             ensure_ascii=False, indent=2))
        else:
            report = gov.review_history(args.persona, args.days)
            print(report)
            print(generate_root_card("REVIEW", "🟢"))

    if args.record:
        any_cmd = True
        result = gov.record_execution(args.record, args.action, args.target)
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"✅ 已记录: {result['persona_id']} → {result['action']} (DNA: {result['dna']})")
            print(generate_root_card("RECORD", "🟢"))

    if args.stats:
        any_cmd = True
        stats = gov.get_stats()
        if use_json:
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print("📊 人格治理统计")
            print(f"  总执行记录: {stats['total_history']}")
            print(f"  冲突记录: {stats['conflicts']}")
            print(f"  职责分配: {stats['duty_assignments']}")
            print(f"  继承链: {stats['inheritance_chain']}")
            print(f"  审计条目: {stats['audit_entries']}")
            print(f"  状态: {stats['status']}")
            print(generate_root_card("STATS", stats['status']))

    if args.clear_conflicts:
        any_cmd = True
        result = gov.clear_conflicts(args.persona)
        if use_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"✅ 已清理 {result['affected']} 个冲突标记")
            print(generate_root_card("CLEAR", "🟢"))

    if not any_cmd:
        parser.print_help()

if __name__ == "__main__":
    main()
