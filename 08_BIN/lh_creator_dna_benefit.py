#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂创作者DNA受益算法 v1.1（修复版）
破解专利护城河 · 把选择权还给老百姓

DNA: #龍芯⚡️丙午·癸未·壬午-CREATOR-DNA-BENEFIT-v1.1-UID9622

修复: 连接生命周期 / 防自证 / 验证去重 / 分配校验 / SHA-256 ID / 三色审计

用法:
    作为库: from lh_creator_dna_benefit import CreatorBenefitEngine
    命令行:
        python3 lh_creator_dna_benefit.py --register --creator-id UID9622 --creator-name "Lucky" --content "算法描述" --category algorithm
        python3 lh_creator_dna_benefit.py --verify <DNA> --verifier-id UID1001 --score 0.9
        python3 lh_creator_dna_benefit.py --benefit <DNA>
        python3 lh_creator_dna_benefit.py --audit <DNA>
        python3 lh_creator_dna_benefit.py --profile <creator_id>
        python3 lh_creator_dna_benefit.py --distribute --source <DNA> --recipient <ID> --amount 88.8
        python3 lh_creator_dna_benefit.py --tree <DNA>
        python3 lh_creator_dna_benefit.py --list-creations
"""

import hashlib
import time
import sqlite3
import logging
import argparse
import sys
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

DNA_PREFIX = "#龍芯⚡️丙午·癸未·壬午"

CATEGORY_WEIGHTS = {
    "code": 1.2, "design": 1.1, "idea": 0.9,
    "document": 0.8, "creation": 1.0, "algorithm": 1.3,
}

# 反女巫参数（§6）
MAX_WEIGHT_PER_CREATION = 100.0   # 单创作验证权重封顶
SELF_VERIFY_FORBIDDEN = True      # 禁止自证（军规）

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("creator_benefit")


def generate_creator_dna(creator_id: str, content: str, category: str = "CREATION") -> str:
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    h = hashlib.sha256(f"{creator_id}{content}{ts}".encode()).hexdigest()[:8].upper()
    return f"{DNA_PREFIX}-{category.upper()}-{creator_id}-{h}"


@dataclass
class CreationRecord:
    dna: str
    creator_id: str
    creator_name: str
    content: str
    category: str
    timestamp: str
    parent_dna: Optional[str] = None
    content_hash: str = ""
    proof: str = "timestamp"
    weight: float = 1.0
    community_score: float = 0.0
    benefit_share: float = 0.0
    status: str = "pending"


@dataclass
class BenefitDistribution:
    distribution_id: str
    source_dna: str
    recipient_id: str
    amount: float
    reason: str
    timestamp: str
    distribution_hash: str


class CreatorBenefitEngine:
    """创作者受益算法引擎 v1.1"""

    def __init__(self, db_path: Path = None):
        self.db_path = db_path or Path.home() / ".龍魂" / "creator_benefit.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _conn(self):
        c = sqlite3.connect(str(self.db_path))
        c.execute("PRAGMA foreign_keys = ON")
        return c

    def _init_db(self):
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS creations (
                dna TEXT PRIMARY KEY, creator_id TEXT, creator_name TEXT,
                content TEXT, category TEXT, timestamp TEXT, parent_dna TEXT,
                content_hash TEXT, proof TEXT, weight REAL,
                community_score REAL, benefit_share REAL, status TEXT)""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS distributions (
                distribution_id TEXT PRIMARY KEY, source_dna TEXT,
                recipient_id TEXT, amount REAL, reason TEXT,
                timestamp TEXT, distribution_hash TEXT)""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS creators (
                creator_id TEXT PRIMARY KEY, creator_name TEXT,
                total_weight REAL DEFAULT 0, total_benefit REAL DEFAULT 0,
                contribution_count INTEGER DEFAULT 0, last_active TEXT,
                trust_score REAL DEFAULT 0.5)""")
        # 🆕 v1.1: 验证记录表（去重 + 防自证 + 互刷分析依据）
        cur.execute("""
            CREATE TABLE IF NOT EXISTS verifications (
                dna TEXT, verifier_id TEXT, score REAL, timestamp TEXT,
                PRIMARY KEY (dna, verifier_id))""")
        conn.commit()
        conn.close()

    # ---------- 1. 创造行为锚定 ----------
    def register_creation(self, creator_id, creator_name, content,
                          category="creation", parent_dna=None, proof="timestamp"):
        category = category.lower()          # 🆕 归一化（修复缺陷4）
        dna = generate_creator_dna(creator_id, content, category)
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        ts = datetime.now().isoformat()
        record = CreationRecord(dna, creator_id, creator_name, content,
                                category, ts, parent_dna, content_hash, proof)
        conn = self._conn()
        conn.execute("""
            INSERT OR REPLACE INTO creations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (dna, creator_id, creator_name, content, category, ts,
             parent_dna, content_hash, proof, 1.0, 0.0, 0.0, "pending"))
        conn.commit(); conn.close()
        self._update_creator_credit(creator_id, creator_name)
        logger.info(f"🧬 创作锚定: {dna}")
        return record

    # ---------- 2. 社区验证（修复缺陷1/2/5）----------
    def verify_creation(self, dna: str, verifier_id: str, score: float = 1.0):
        if not 0.0 <= score <= 1.0:            # 🆕 分数钳制
            logger.warning(f"🟡 验证分数越界 {score}，拒绝")
            return False
        conn = self._conn()
        cur = conn.cursor()
        cur.execute("SELECT creator_id, community_score, weight FROM creations WHERE dna=?", (dna,))
        row = cur.fetchone()
        if not row:
            conn.close(); return False
        creator_id, cur_score, cur_weight = row
        if SELF_VERIFY_FORBIDDEN and verifier_id == creator_id:   # 🆕 禁自证
            conn.close()
            logger.warning(f"🔴 拒绝自证: {verifier_id} -> {dna}")
            return False
        try:                                      # 🆕 验证去重
            conn.execute("INSERT INTO verifications VALUES (?,?,?,?)",
                         (dna, verifier_id, score, datetime.now().isoformat()))
        except sqlite3.IntegrityError:
            conn.close(); return False            # 已验证过，不重复计权
        if cur_weight >= MAX_WEIGHT_PER_CREATION: # 🆕 权重封顶
            conn.commit(); conn.close(); return True
        new_score = (cur_score * cur_weight + score) / (cur_weight + 1)
        conn.execute("UPDATE creations SET community_score=?, weight=?, status='verified' WHERE dna=?",
                     (new_score, cur_weight + 1, dna))
        conn.commit(); conn.close()
        self._update_creator_trust(creator_id)
        return True

    # ---------- 3. 受益权计算 ----------
    def calculate_benefit(self, dna: str) -> Dict:
        conn = self._conn()
        row = conn.execute(
            "SELECT creator_id, creator_name, community_score, weight, timestamp, category "
            "FROM creations WHERE dna=?", (dna,)).fetchone()
        conn.close()
        if not row:
            return {"error": "创作不存在"}
        creator_id, creator_name, cscore, weight, ts, category = row
        try:
            days_old = max(0, (datetime.now() - datetime.fromisoformat(ts)).days)
            time_factor = 1.0 / (1 + days_old * 0.01)
        except Exception:
            time_factor = 0.5
        community_factor = 0.5 + cscore * 0.5
        category_factor = CATEGORY_WEIGHTS.get(category, 1.0)
        benefit_index = weight * community_factor * time_factor * category_factor
        return {
            "dna": dna, "creator_id": creator_id, "creator_name": creator_name,
            "benefit_index": round(benefit_index, 4),
            "community_score": round(cscore, 3), "weight": weight,
            "time_factor": round(time_factor, 3), "category_factor": category_factor,
            "status": "active" if benefit_index > 0.5 else "low_impact",
        }

    # ---------- 4. 受益分配（修复缺陷3）----------
    def distribute_benefit(self, source_dna, recipient_id, amount, reason=""):
        if amount <= 0:
            raise ValueError("🟡 分配金额必须为正")
        conn = self._conn()
        cur = conn.cursor()
        if not cur.execute("SELECT 1 FROM creations WHERE dna=?", (source_dna,)).fetchone():
            conn.close(); raise ValueError(f"🔴 源DNA不存在: {source_dna}")
        if not cur.execute("SELECT 1 FROM creators WHERE creator_id=?", (recipient_id,)).fetchone():
            conn.close(); raise ValueError(f"🔴 接收者未登记: {recipient_id}")
        ts = datetime.now().isoformat()
        dist_id = "DIST-" + hashlib.sha256(
            f"{source_dna}{recipient_id}{amount}{ts}".encode()).hexdigest()[:16].upper()
        dist_hash = hashlib.sha256(
            f"{dist_id}{source_dna}{recipient_id}{amount}{ts}".encode()).hexdigest()
        cur.execute("INSERT INTO distributions VALUES (?,?,?,?,?,?,?)",
                    (dist_id, source_dna, recipient_id, amount, reason, ts, dist_hash))
        cur.execute("UPDATE creators SET total_benefit=total_benefit+? WHERE creator_id=?",
                    (amount, recipient_id))
        cur.execute("UPDATE creations SET benefit_share=benefit_share+? WHERE dna=?",
                    (amount, source_dna))
        conn.commit(); conn.close()
        return BenefitDistribution(dist_id, source_dna, recipient_id, amount, reason, ts, dist_hash)

    # ---------- 5. 🆕 三色审计 ----------
    def audit_creation(self, dna: str) -> Dict:
        """三色审计：🟢健康 / 🟡待审 / 🔴熔断"""
        info = self.calculate_benefit(dna)
        if "error" in info:
            return {"dna": dna, "color": "🔴", "reason": "无DNA=匿名=不可信"}
        conn = self._conn()
        verifiers = [r[0] for r in conn.execute(
            "SELECT verifier_id FROM verifications WHERE dna=?", (dna,)).fetchall()]
        conn.close()
        unique_ratio = len(set(verifiers)) / max(1, len(verifiers))
        if unique_ratio < 1.0:
            return {"dna": dna, "color": "🔴", "reason": "存在重复验证（互刷嫌疑）", **info}
        if info["weight"] >= MAX_WEIGHT_PER_CREATION * 0.9:
            return {"dna": dna, "color": "🟡", "reason": "权重接近封顶，待人工复核", **info}
        if info["community_score"] == 0:
            return {"dna": dna, "color": "🟡", "reason": "尚无社区验证", **info}
        return {"dna": dna, "color": "🟢", "reason": "健康", **info}

    # ---------- 6. 内部工具 ----------
    def _update_creator_credit(self, creator_id, creator_name=""):
        conn = self._conn()
        cur = conn.cursor()
        if cur.execute("SELECT 1 FROM creators WHERE creator_id=?", (creator_id,)).fetchone():
            cur.execute("UPDATE creators SET contribution_count=contribution_count+1, last_active=? WHERE creator_id=?",
                        (datetime.now().isoformat(), creator_id))
        else:
            cur.execute("INSERT INTO creators (creator_id, creator_name, contribution_count, last_active, trust_score) VALUES (?,?,1,?,0.5)",
                        (creator_id, creator_name, datetime.now().isoformat()))
        conn.commit(); conn.close()

    def _update_creator_trust(self, creator_id):
        conn = self._conn()
        row = conn.execute(
            "SELECT COUNT(*), SUM(community_score) FROM creations WHERE creator_id=? AND community_score>0",
            (creator_id,)).fetchone()
        if row and row[0] > 0:
            trust = min(1.0, 0.3 + 0.7 * ((row[1] or 0) / row[0]))
            conn.execute("UPDATE creators SET trust_score=? WHERE creator_id=?", (trust, creator_id))
        conn.commit(); conn.close()

    # ---------- 7. 查询接口 ----------
    def get_creator_profile(self, creator_id: str) -> Dict:
        conn = self._conn()
        row = conn.execute(
            "SELECT creator_name, total_weight, total_benefit, contribution_count, trust_score "
            "FROM creators WHERE creator_id=?", (creator_id,)).fetchone()
        conn.close()
        if not row:
            return {"error": "创作者不存在"}
        return {"creator_id": creator_id, "name": row[0],
                "total_weight": round(row[1], 2), "total_benefit": round(row[2], 2),
                "contribution_count": row[3], "trust_score": round(row[4], 3)}

    def get_creation_tree(self, dna: str) -> List[Dict]:
        conn = self._conn()
        rows = conn.execute(
            "SELECT dna, creator_name, content, timestamp, weight FROM creations "
            "WHERE parent_dna=? OR dna=? ORDER BY timestamp", (dna, dna)).fetchall()
        conn.close()
        return [{"dna": r[0], "creator": r[1],
                 "content": r[2][:100] + "..." if len(r[2]) > 100 else r[2],
                 "timestamp": r[3], "weight": r[4]} for r in rows]

    def list_all_creations(self) -> List[Dict]:
        conn = self._conn()
        rows = conn.execute(
            "SELECT dna, creator_name, category, community_score, weight, status, timestamp "
            "FROM creations ORDER BY timestamp DESC LIMIT 100").fetchall()
        conn.close()
        return [{"dna": r[0], "creator": r[1], "category": r[2],
                 "score": round(r[3], 3), "weight": r[4], "status": r[5],
                 "timestamp": r[6]} for r in rows]

    def list_all_creators(self) -> List[Dict]:
        conn = self._conn()
        rows = conn.execute(
            "SELECT creator_id, creator_name, total_weight, total_benefit, "
            "contribution_count, trust_score FROM creators ORDER BY trust_score DESC").fetchall()
        conn.close()
        return [{"creator_id": r[0], "name": r[1], "weight": round(r[2], 2),
                 "benefit": round(r[3], 2), "contributions": r[4],
                 "trust": round(r[5], 3)} for r in rows]


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂创作者DNA受益算法 v1.1 · 破解专利护城河",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh 受益 --register --creator-id UID9622 --creator-name "Lucky" --content "统一视觉渲染算法" --category algorithm
  lh 受益 --verify <DNA> --verifier-id UID1001 --score 0.9
  lh 受益 --benefit <DNA>
  lh 受益 --audit <DNA>
  lh 受益 --profile <creator_id>
  lh 受益 --distribute --source <DNA> --recipient <ID> --amount 88.8
  lh 受益 --list-creations
  lh 受益 --list-creators
        """
    )

    # 注册创作
    parser.add_argument("--register", action="store_true", help="注册新创作")
    parser.add_argument("--creator-id", type=str, help="创作者ID")
    parser.add_argument("--creator-name", type=str, help="创作者名称")
    parser.add_argument("--content", type=str, help="创作内容描述")
    parser.add_argument("--category", type=str, default="creation",
                        choices=["code","design","idea","document","creation","algorithm"],
                        help="创作类别")
    parser.add_argument("--parent-dna", type=str, help="父创作DNA")

    # 社区验证
    parser.add_argument("--verify", type=str, help="验证指定DNA的创作")
    parser.add_argument("--verifier-id", type=str, help="验证者ID")
    parser.add_argument("--score", type=float, default=1.0, help="验证分数 [0,1]")

    # 受益计算
    parser.add_argument("--benefit", type=str, help="计算指定DNA的受益指数")

    # 三色审计
    parser.add_argument("--audit", type=str, help="对指定DNA进行三色审计")

    # 分配
    parser.add_argument("--distribute", action="store_true", help="分配受益")
    parser.add_argument("--source", type=str, help="源DNA")
    parser.add_argument("--recipient", type=str, help="接收者ID")
    parser.add_argument("--amount", type=float, help="分配金额")
    parser.add_argument("--reason", type=str, default="", help="分配原因")

    # 查询
    parser.add_argument("--profile", type=str, help="查询创作者档案")
    parser.add_argument("--tree", type=str, help="查询创作树")
    parser.add_argument("--list-creations", action="store_true", help="列出所有创作")
    parser.add_argument("--list-creators", action="store_true", help="列出所有创作者")

    args = parser.parse_args()
    engine = CreatorBenefitEngine()

    # === 路由 ===

    if args.register:
        if not args.creator_id or not args.creator_name or not args.content:
            print("❌ --register 需要 --creator-id, --creator-name, --content")
            sys.exit(1)
        rec = engine.register_creation(args.creator_id, args.creator_name,
                                        args.content, args.category, args.parent_dna)
        print(f"\n✅ 创作已锚定")
        print(f"   DNA: {rec.dna}")
        print(f"   创作者: {rec.creator_name} ({rec.creator_id})")
        print(f"   类别: {rec.category}")
        print(f"   时间: {rec.timestamp}")
        print(f"   状态: {rec.status}")
        print(f"   哈希: {rec.content_hash[:16]}")
        return

    if args.verify:
        if not args.verifier_id:
            print("❌ --verify 需要 --verifier-id")
            sys.exit(1)
        ok = engine.verify_creation(args.verify, args.verifier_id, args.score)
        print(f"\n{'✅ 验证成功' if ok else '❌ 验证失败'} → {args.verify}")
        if not ok:
            print("   可能原因: 自证被拒 / 重复验证 / 分数越界 / DNA不存在")
        return

    if args.benefit:
        result = engine.calculate_benefit(args.benefit)
        print(f"\n📊 受益评估 → {args.benefit}")
        for k, v in result.items():
            print(f"   {k}: {v}")
        return

    if args.audit:
        result = engine.audit_creation(args.audit)
        print(f"\n⚖️ 三色审计 → {args.audit}")
        print(f"   判定: {result['color']} {result['reason']}")
        if "benefit_index" in result:
            print(f"   受益指数: {result['benefit_index']}")
            print(f"   社区评分: {result['community_score']}")
            print(f"   权重: {result['weight']}")
        return

    if args.distribute:
        if not args.source or not args.recipient or not args.amount:
            print("❌ --distribute 需要 --source, --recipient, --amount")
            sys.exit(1)
        try:
            dist = engine.distribute_benefit(args.source, args.recipient, args.amount, args.reason)
            print(f"\n💰 分配完成")
            print(f"   分配ID: {dist.distribution_id}")
            print(f"   源DNA: {dist.source_dna}")
            print(f"   接收者: {dist.recipient_id}")
            print(f"   金额: ¥{dist.amount}")
            print(f"   哈希: {dist.distribution_hash[:32]}")
        except ValueError as e:
            print(f"❌ 分配失败: {e}")
            sys.exit(1)
        return

    if args.profile:
        profile = engine.get_creator_profile(args.profile)
        if "error" in profile:
            print(f"❌ {profile['error']}")
            return
        print(f"\n👤 创作者档案")
        for k, v in profile.items():
            print(f"   {k}: {v}")
        return

    if args.tree:
        tree = engine.get_creation_tree(args.tree)
        print(f"\n🌳 创作树 → {args.tree}")
        for item in tree:
            print(f"   ├─ {item['dna']} ({item['creator']})")
            print(f"   │  {item['content']}")
            print(f"   │  w={item['weight']} · {item['timestamp']}")
        return

    if args.list_creations:
        creations = engine.list_all_creations()
        print(f"\n📋 全部创作（{len(creations)}件）:")
        for c in creations:
            print(f"   {c['dna']} | {c['creator']} | {c['category']} | "
                  f"score={c['score']} | w={c['weight']} | {c['status']}")
        return

    if args.list_creators:
        creators = engine.list_all_creators()
        print(f"\n👥 全部创作者（{len(creators)}人）:")
        for c in creators:
            print(f"   {c['creator_id']} | {c['name']} | trust={c['trust']} | "
                  f"贡献{c['contributions']} | 受益¥{c['benefit']}")
        return

    # 无参数 = 显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
