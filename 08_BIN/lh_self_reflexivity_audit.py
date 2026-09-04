#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自我审计引擎 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-SELF-AUDIT-v1.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. DNA固化风险检测 — 检测范式迁移的阻力是否在累积
  2. P0焊死风险检测 — 检测规则僵化程度
  3. 君子协议声誉风险检测 — 检测声誉机制是否被博弈
  4. 生成自反性审计报告（含三色审计 + ROOT_CARD）
  5. 历史趋势追踪（检测固化是否在加深）

用法：
  python3 bin/lh_self_reflexivity_audit.py --full          # 完整自反性审计
  python3 bin/lh_self_reflexivity_audit.py --risk dna      # 只检测DNA固化风险
  python3 bin/lh_self_reflexivity_audit.py --risk p0       # 只检测P0焊死风险
  python3 bin/lh_self_reflexivity_audit.py --risk protocol # 只检测君子协议风险
  python3 bin/lh_self_reflexivity_audit.py --trend         # 检测固化趋势（需历史数据）
  python3 bin/lh_self_reflexivity_audit.py --report        # 生成完整报告
  python3 bin/lh_self_reflexivity_audit.py --interactive   # 交互模式
"""

import os
import sys
import json
import sqlite3
import hashlib
import datetime
import argparse
import re
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import math

# ============================================================
# 固定锚点
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path.home() / "longhun-system"
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "self_audit.db"
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
FUSION_BRIDGE_URL = "http://127.0.0.1:8777"  # 流场融合桥接层

# ============================================================
# 数据库初始化
# ============================================================

def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    # 历史审计记录（只追加）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audit_type TEXT NOT NULL,
            risk_score REAL,
            risk_level TEXT,
            details TEXT,
            dna_trace TEXT NOT NULL,
            tricolor_status TEXT DEFAULT '🟢',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 固化趋势追踪
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solidification_trend (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dimension TEXT NOT NULL,
            value REAL,
            delta REAL,
            measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # P0规则变更日志（只追加）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS p0_change_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT NOT NULL,
            change_type TEXT,
            description TEXT,
            proposer TEXT,
            dna_trace TEXT NOT NULL,
            approved INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    return True

def get_db():
    return sqlite3.connect(str(DB_PATH))

# ============================================================
# DNA 生成
# ============================================================

def generate_dna(module: str, action: str) -> str:
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = hashlib.md5(f"{module}{now}{action}".encode()).hexdigest()[:8]
    return f"#龍芯⚡️{now}-{module}-{action}-{suffix}"

# ============================================================
# ROOT_CARD
# ============================================================

def root_card(action: str, status: str, data: Dict) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
【ROOT_CARD｜自我审计】
Action: {action}
Status: {status}
RiskScore: {data.get('risk_score', 0)}
RiskLevel: {data.get('risk_level', 'unknown')}
Timestamp: {now}
DNA: {data.get('dna', generate_dna('AUDIT', action))}
CONFIRM: {CONFIRM}
SEAL: {SEAL}
GPG: {GPG}
"""

# ============================================================
# 核心审计引擎
# ============================================================

class SelfReflexivityAudit:
    def __init__(self, inject_flow: bool = False, fusion_url: str = FUSION_BRIDGE_URL):
        if not DB_PATH.exists():
            init_db()
        self.conn = get_db()
        self.conn.row_factory = sqlite3.Row
        self.results = {
            "dna_risk": {},
            "p0_risk": {},
            "protocol_risk": {},
            "overall": {}
        }
        self.inject_flow = inject_flow
        self.fusion_url = fusion_url

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def _safe_query(self, query: str) -> List[Dict]:
        """安全查询，表不存在时返回空列表"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            if "no such table" in str(e).lower():
                return []
            raise

    # ---------- 1. DNA固化风险检测 ----------
    def audit_dna_risk(self) -> Dict:
        """
        风险1：DNA追溯的"不可篡改性"成为范式迁移的阻力
        检测维度：
          - DNA版本分布（是否过于集中在少数版本）
          - 范式迁移尝试频率 vs 历史惯性
          - 跨范式兼容性指标
        """
        cursor = self.conn.cursor()

        # 1.1 统计DNA版本分布（从执行历史中提取）
        version_dist = self._safe_query('''
            SELECT 
                substr(dna_trace, 11, 10) as date_prefix,
                COUNT(*) as count,
                COUNT(DISTINCT persona_id) as personas
            FROM execution_history 
            GROUP BY date_prefix 
            ORDER BY date_prefix DESC
            LIMIT 30
        ''')

        # 1.2 计算集中度（HHI指数）
        total = sum(v['count'] for v in version_dist) if version_dist else 0
        hhi = sum((v['count'] / total) ** 2 for v in version_dist) if total > 0 else 1

        # 1.3 范式迁移信号：检测是否出现新的DNA格式或命名模式
        patterns = self._safe_query('''
            SELECT DISTINCT substr(dna_trace, 1, 20) as dna_pattern, COUNT(*) as count
            FROM execution_history
            GROUP BY dna_pattern
            ORDER BY count DESC
            LIMIT 10
        ''')

        # 1.4 计算风险分数
        # 无数据时的默认值
        if not version_dist and not patterns:
            # 无执行历史表 → 无法评估，标记🟡
            risk_score = 0.5
            hhi = 0.0
        else:
            concentration_risk = min(1.0, hhi * 1.5)  # HHI越高越集中
            pattern_diversity = min(1.0, len(patterns) / 5) if patterns else 0.5
            risk_score = concentration_risk * 0.6 + (1 - pattern_diversity) * 0.4
            risk_score = min(1.0, max(0.0, risk_score))

        # 1.5 判定风险等级
        if risk_score > 0.7:
            risk_level = "🔴 高危"
            status = "🔴"
            recommendation = "检测到DNA高度集中，范式迁移阻力显著增加。建议主动创建新DNA模式，鼓励实验性分支。"
        elif risk_score > 0.4:
            risk_level = "🟡 中危"
            status = "🟡"
            if not version_dist and not patterns:
                recommendation = "缺少执行历史数据，无法准确评估DNA固化程度。建议建立执行历史追踪后再做评估。"
            else:
                recommendation = "DNA开始出现集中趋势，建议关注新范式尝试的采纳率。"
        else:
            risk_level = "🟢 低危"
            status = "🟢"
            recommendation = "DNA多样性良好，范式迁移阻力较低。"

        # 记录审计
        dna_trace = generate_dna("DNA-RISK", "AUDIT")
        cursor.execute('''
            INSERT INTO audit_history (audit_type, risk_score, risk_level, details, dna_trace, tricolor_status)
            VALUES ('dna_risk', ?, ?, ?, ?, ?)
        ''', (risk_score, risk_level, json.dumps({
            "hhi": hhi,
            "total_versions": len(version_dist),
            "patterns": patterns[:5]
        }, ensure_ascii=False), dna_trace, status))

        self.conn.commit()

        self.results["dna_risk"] = {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "status": status,
            "recommendation": recommendation,
            "details": {
                "hhi": hhi,
                "total_versions": len(version_dist),
                "patterns": patterns[:5]
            },
            "dna": dna_trace
        }
        return self.results["dna_risk"]

    # ---------- 2. P0焊死风险检测 ----------
    def audit_p0_risk(self) -> Dict:
        """
        风险2：P0焊死原则在应对未知威胁时丧失灵活性
        检测维度：
          - P0规则修改尝试次数 vs 通过次数
          - 熔断触发频率（熔断是P0的应急出口）
          - 规则与生存冲突的信号
        """
        cursor = self.conn.cursor()

        # 2.1 P0修改尝试与通过率
        cursor.execute('''
            SELECT 
                COUNT(*) as total_attempts,
                COALESCE(SUM(CASE WHEN approved = 1 THEN 1 ELSE 0 END), 0) as approved_count
            FROM p0_change_log
        ''')
        p0_stats_row = cursor.fetchone()
        p0_stats = dict(p0_stats_row) if p0_stats_row else {"total_attempts": 0, "approved_count": 0}

        total_attempts = p0_stats.get("total_attempts", 0)
        approved_count = p0_stats.get("approved_count", 0)

        # 2.2 熔断频率（从执行历史中统计）
        fuse_rows = self._safe_query('''
            SELECT COUNT(*) as fuse_count
            FROM execution_history
            WHERE action = 'fuse' OR action = '熔断' OR target LIKE '%熔断%'
        ''')
        fuse_count = fuse_rows[0].get("fuse_count", 0) if fuse_rows else 0

        # 2.3 规则-生存冲突信号：检测是否存在违反P0原则但系统存续的行为
        conflict_rows = self._safe_query('''
            SELECT COUNT(*) as conflict_count
            FROM execution_history
            WHERE (action LIKE '%扫描%' OR action LIKE '%翻%' OR action LIKE '%私域%')
            AND tricolor_status = '🔴'
        ''')
        conflict_count = conflict_rows[0].get("conflict_count", 0) if conflict_rows else 0

        # 2.4 计算风险分数
        # 修改阻力：如果尝试次数多但通过率低 → 僵化
        if total_attempts > 0:
            approval_rate = approved_count / total_attempts
            rigidity_risk = 1 - approval_rate
        else:
            rigidity_risk = 0.3  # 默认存在一定僵化风险

        # 熔断风险：熔断过多说明P0在频繁被触发
        fuse_risk = min(1.0, fuse_count / 10)

        # 冲突风险
        conflict_risk = min(1.0, conflict_count / 5)

        risk_score = rigidity_risk * 0.4 + fuse_risk * 0.3 + conflict_risk * 0.3
        risk_score = min(1.0, max(0.0, risk_score))

        # 2.5 判定风险等级
        if risk_score > 0.7:
            risk_level = "🔴 高危"
            status = "🔴"
            recommendation = "P0焊死导致系统灵活性严重下降，建议评估是否需要修订P0规则，或增加P0的例外条款。"
        elif risk_score > 0.4:
            risk_level = "🟡 中危"
            status = "🟡"
            recommendation = "P0开始出现僵化迹象，建议记录P0规则的适用场景与冲突案例。"
        else:
            risk_level = "🟢 低危"
            status = "🟢"
            recommendation = "P0规则与系统运行基本协调，建议继续保持记录。"
        dna_trace = generate_dna("P0-RISK", "AUDIT")

        cursor.execute('''
            INSERT INTO audit_history (audit_type, risk_score, risk_level, details, dna_trace, tricolor_status)
            VALUES ('p0_risk', ?, ?, ?, ?, ?)
        ''', (risk_score, risk_level, json.dumps({
            "total_attempts": total_attempts,
            "approved_count": approved_count,
            "fuse_count": fuse_count,
            "conflict_count": conflict_count,
            "approval_rate": round(approved_count / total_attempts, 3) if total_attempts > 0 else None
        }, ensure_ascii=False), dna_trace, status))

        self.conn.commit()

        self.results["p0_risk"] = {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "status": status,
            "recommendation": recommendation,
            "details": {
                "total_attempts": total_attempts,
                "approved_count": approved_count,
                "approval_rate": round(approved_count / total_attempts, 3) if total_attempts > 0 else None,
                "fuse_count": fuse_count,
                "conflict_count": conflict_count
            },
            "dna": dna_trace
        }
        return self.results["p0_risk"]

    # ---------- 3. 君子协议声誉风险检测 ----------
    def audit_protocol_risk(self) -> Dict:
        """
        风险3：君子协议的声誉机制在规模化后被博弈
        检测维度：
          - 声誉违约记录数量 vs 身份更换行为
          - 大规模违约的集聚效应
          - 声誉恢复速度
        """
        cursor = self.conn.cursor()

        # 3.1 违约记录统计
        breach_rows = self._safe_query('''
            SELECT COUNT(*) as total_breaches
            FROM execution_history
            WHERE action LIKE '%违约%' OR action LIKE '%breach%' OR target LIKE '%违约%'
        ''')
        total_breaches = breach_rows[0].get("total_breaches", 0) if breach_rows else 0

        # 3.2 身份更换检测（新人格涌现但历史清零）
        persona_rows = self._safe_query('''
            SELECT 
                COUNT(DISTINCT persona_id) as total_personas,
                COUNT(DISTINCT CASE WHEN claim_status = '已领取' THEN persona_id END) as claimed_personas
            FROM mcp_agents
        ''')
        if persona_rows:
            persona_stats = persona_rows[0]
            total_personas = persona_stats.get("total_personas", 0)
            claimed_personas = persona_stats.get("claimed_personas", 0)
        else:
            total_personas = 1
            claimed_personas = 0

        # 3.3 大规模违约信号：在短时间内出现大量违约记录
        recent_rows = self._safe_query('''
            SELECT COUNT(*) as recent_breaches
            FROM execution_history
            WHERE (action LIKE '%违约%' OR target LIKE '%违约%')
            AND executed_at > datetime('now', '-7 days')
        ''')
        recent_breaches = recent_rows[0].get("recent_breaches", 0) if recent_rows else 0

        # 3.4 计算风险分数
        # 违约率
        breach_rate = total_breaches / (total_personas + 1)

        # 身份更换率（高更换率 = 声誉系统被规避）
        identity_churn_rate = 1 - (claimed_personas / (total_personas + 1))

        # 集聚效应
        clustering_risk = min(1.0, recent_breaches / 10)

        risk_score = breach_rate * 0.4 + identity_churn_rate * 0.3 + clustering_risk * 0.3
        risk_score = min(1.0, max(0.0, risk_score))

        # 3.5 判定风险等级
        if risk_score > 0.7:
            risk_level = "🔴 高危"
            status = "🔴"
            recommendation = "声誉机制出现大规模被博弈迹象，建议引入身份绑定增强机制，降低策略性违约收益。"
        elif risk_score > 0.4:
            risk_level = "🟡 中危"
            status = "🟡"
            recommendation = "声誉机制开始出现磨损，建议监控违约模式与身份更换频率。"
        else:
            risk_level = "🟢 低危"
            status = "🟢"
            recommendation = "声誉机制运作良好，建议继续保持记录。"
        dna_trace = generate_dna("PROTOCOL-RISK", "AUDIT")

        cursor.execute('''
            INSERT INTO audit_history (audit_type, risk_score, risk_level, details, dna_trace, tricolor_status)
            VALUES ('protocol_risk', ?, ?, ?, ?, ?)
        ''', (risk_score, risk_level, json.dumps({
            "total_breaches": total_breaches,
            "total_personas": total_personas,
            "claimed_personas": claimed_personas,
            "identity_churn_rate": identity_churn_rate,
            "recent_breaches": recent_breaches
        }, ensure_ascii=False), dna_trace, status))

        self.conn.commit()

        self.results["protocol_risk"] = {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "status": status,
            "recommendation": recommendation,
            "details": {
                "total_breaches": total_breaches,
                "total_personas": total_personas,
                "claimed_personas": claimed_personas,
                "identity_churn_rate": identity_churn_rate,
                "recent_breaches": recent_breaches
            },
            "dna": dna_trace
        }
        return self.results["protocol_risk"]

    # ---------- 4. 完整审计 ----------
    def _inject_to_flow(self, risk_type: str, risk_score: float, status: str) -> Dict:
        """将审计结果注入流场融合桥接层"""
        if not self.inject_flow:
            return {"injected": False, "reason": "inject_flow_disabled"}

        # 映射风险类型到事件
        severity = "critical" if risk_score > 0.7 else ("medium" if risk_score > 0.4 else "low")
        event_map = {
            "dna": ("dna_risk", severity),
            "p0": ("p0_risk", severity),
            "protocol": ("protocol_risk", severity),
            "overall": ("full_audit", severity),
        }

        results = []
        for rtype in [risk_type] if risk_type != "overall" else ["dna", "p0", "protocol"]:
            event_type, sev = event_map.get(rtype, ("unknown", "info"))
            sev = severity if rtype == risk_type else sev
            # 三等分映射
            if rtype == "dna":
                event_type = f"dna_risk_{'high' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'low'}"
            elif rtype == "p0":
                event_type = f"p0_risk_{'high' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'low'}"
            elif rtype == "protocol":
                event_type = f"protocol_risk_{'high' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'low'}"

            payload = {
                "source": "self_audit",
                "event_type": event_type,
                "severity": sev,
                "data": {"risk_type": rtype, "risk_score": risk_score, "status": status}
            }

            try:
                data = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(
                    f"{self.fusion_url}/event",
                    data=data,
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=3) as resp:
                    result = json.loads(resp.read().decode())
                    results.append({"injected": True, "event": event_type, "response": result})
            except Exception as e:
                results.append({"injected": False, "event": event_type, "error": str(e)})

        return {"results": results}

    def full_audit(self) -> Dict:
        """执行完整审计"""
        dna_result = self.audit_dna_risk()
        p0_result = self.audit_p0_risk()
        protocol_result = self.audit_protocol_risk()

        # 综合风险评分
        overall_score = (
            dna_result.get("risk_score", 0) * 0.33 +
            p0_result.get("risk_score", 0) * 0.33 +
            protocol_result.get("risk_score", 0) * 0.34
        )

        if overall_score > 0.7:
            overall_level = "🔴 高危"
            overall_status = "🔴"
        elif overall_score > 0.4:
            overall_level = "🟡 中危"
            overall_status = "🟡"
        else:
            overall_level = "🟢 低危"
            overall_status = "🟢"

        self.results["overall"] = {
            "risk_score": overall_score,
            "risk_level": overall_level,
            "status": overall_status,
            "dna": generate_dna("FULL-AUDIT", "COMPLETE")
        }

        # 注入流场融合桥接层
        if self.inject_flow:
            flow_results = {}
            for rtype, result in [
                ("dna", dna_result), ("p0", p0_result), ("protocol", protocol_result)
            ]:
                flow_results[rtype] = self._inject_to_flow(
                    rtype, result.get("risk_score", 0), result.get("status", "🟡")
                )
            self.results["flow_injection"] = flow_results

        return self.results

    # ---------- 5. 生成报告 ----------
    def generate_report(self) -> str:
        """生成可读报告"""
        results = self.full_audit()
        lines = []
        lines.append("=" * 70)
        lines.append("🐉 龍魂 · 自我审计报告")
        lines.append("=" * 70)
        lines.append(f"DNA: {results['overall'].get('dna', 'N/A')}")
        lines.append(f"综合风险: {results['overall'].get('risk_level', 'unknown')}")
        lines.append("=" * 70)

        # DNA风险
        dna = results.get("dna_risk", {})
        lines.append("\n## 🔬 风险1: DNA固化")
        lines.append(f"  风险评分: {dna.get('risk_score', 0)*100:.1f}%")
        lines.append(f"  状态: {dna.get('status', '')} {dna.get('risk_level', '')}")
        lines.append(f"  建议: {dna.get('recommendation', '')}")
        details = dna.get("details", {})
        if details:
            lines.append(f"  HHI: {details.get('hhi', 0):.3f}")
            lines.append(f"  DNA模式数: {len(details.get('patterns', []))}")

        # P0风险
        p0 = results.get("p0_risk", {})
        lines.append("\n## 🔒 风险2: P0焊死")
        lines.append(f"  风险评分: {p0.get('risk_score', 0)*100:.1f}%")
        lines.append(f"  状态: {p0.get('status', '')} {p0.get('risk_level', '')}")
        lines.append(f"  建议: {p0.get('recommendation', '')}")
        details = p0.get("details", {})
        if details:
            lines.append(f"  P0修改尝试: {details.get('total_attempts', 0)}")
            lines.append(f"  熔断次数: {details.get('fuse_count', 0)}")

        # 协议风险
        proto = results.get("protocol_risk", {})
        lines.append("\n## 🤝 风险3: 君子协议被博弈")
        lines.append(f"  风险评分: {proto.get('risk_score', 0)*100:.1f}%")
        lines.append(f"  状态: {proto.get('status', '')} {proto.get('risk_level', '')}")
        lines.append(f"  建议: {proto.get('recommendation', '')}")
        details = proto.get("details", {})
        if details:
            lines.append(f"  总违约: {details.get('total_breaches', 0)}")
            lines.append(f"  身份更换率: {details.get('identity_churn_rate', 0)*100:.1f}%")

        # 总体结论
        lines.append("\n" + "=" * 70)
        lines.append(f"📋 综合评估: {results['overall'].get('risk_level', 'unknown')}")
        lines.append("=" * 70)
        lines.append("")
        lines.append(root_card(
            "SELF_AUDIT",
            results['overall'].get('status', '🟢'),
            results['overall']
        ))

        return "\n".join(lines)

    # ---------- 6. 固化趋势检测 ----------
    def detect_trend(self) -> Dict:
        """检测固化趋势（比较历史数据）"""
        cursor = self.conn.cursor()

        # 获取最近30天的审计记录
        cursor.execute('''
            SELECT 
                risk_score,
                created_at
            FROM audit_history
            WHERE created_at > datetime('now', '-30 days')
            ORDER BY created_at ASC
        ''')
        rows = cursor.fetchall()
        if len(rows) < 2:
            return {"status": "insufficient_data", "message": "需要至少两次审计记录才能检测趋势"}

        records = [dict(row) for row in rows]
        first_score = records[0].get("risk_score", 0)
        last_score = records[-1].get("risk_score", 0)
        delta = last_score - first_score

        if delta > 0.1:
            trend = "⬆️ 上升（固化在加深）"
            recommendation = "建议增加范式迁移实验，主动打破固化惯性。"
        elif delta < -0.1:
            trend = "⬇️ 下降（固化在缓解）"
            recommendation = "继续保持当前节奏，固化正在被有效控制。"
        else:
            trend = "➡️ 稳定（固化水平持平）"
            recommendation = "系统处于均衡状态，建议监测关键指标变化。"

        return {
            "trend": trend,
            "delta": delta,
            "first_score": first_score,
            "last_score": last_score,
            "record_count": len(records),
            "recommendation": recommendation
        }

    # ---------- 7. 记录P0修改尝试 ----------
    def log_p0_change(self, rule_name: str, change_type: str, description: str, proposer: str = "system") -> Dict:
        cursor = self.conn.cursor()
        dna = generate_dna("P0-CHANGE", rule_name)
        cursor.execute('''
            INSERT INTO p0_change_log (rule_name, change_type, description, proposer, dna_trace)
            VALUES (?, ?, ?, ?, ?)
        ''', (rule_name, change_type, description, proposer, dna))
        self.conn.commit()
        return {"status": "recorded", "dna": dna, "id": cursor.lastrowid}

    # ---------- 8. 交互模式 ----------
    def interactive(self):
        print("\n🐉 龍魂自我审计引擎 v1.0")
        print(f"CONFIRM: {CONFIRM}")
        print("-" * 50)
        print("命令: full, dna, p0, protocol, trend, report, exit")
        print("-" * 50)

        while True:
            try:
                cmd = input("\n🔮 > ").strip().lower()
                if not cmd:
                    continue
                if cmd in ["exit", "quit"]:
                    print("👋 龍魂不息")
                    break
                elif cmd == "full":
                    results = self.full_audit()
                    print(json.dumps(results, ensure_ascii=False, indent=2))
                elif cmd == "dna":
                    result = self.audit_dna_risk()
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                elif cmd == "p0":
                    result = self.audit_p0_risk()
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                elif cmd == "protocol":
                    result = self.audit_protocol_risk()
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                elif cmd == "trend":
                    result = self.detect_trend()
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                elif cmd == "report":
                    report = self.generate_report()
                    print(report)
                else:
                    print("未知命令: full, dna, p0, protocol, trend, report, exit")
            except KeyboardInterrupt:
                break

# ============================================================
# 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂自我审计引擎")
    parser.add_argument("--full", action="store_true", help="执行完整审计")
    parser.add_argument("--risk", choices=["dna", "p0", "protocol"], help="检测指定风险")
    parser.add_argument("--trend", action="store_true", help="检测固化趋势")
    parser.add_argument("--report", action="store_true", help="生成完整报告")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--p0-log", action="store_true", help="记录P0修改尝试")
    parser.add_argument("--rule", type=str, help="P0规则名")
    parser.add_argument("--change", type=str, help="变更类型")
    parser.add_argument("--desc", type=str, help="变更描述")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--inject-flow", action="store_true", help="审计结果注入流场融合桥接 (8777)")
    parser.add_argument("--fusion-url", type=str, default=FUSION_BRIDGE_URL, help="融合桥接地址")

    args = parser.parse_args()
    audit = SelfReflexivityAudit(inject_flow=args.inject_flow, fusion_url=args.fusion_url)

    if args.interactive:
        audit.interactive()
        return

    if args.p0_log and args.rule and args.change:
        result = audit.log_p0_change(args.rule, args.change, args.desc or "无描述")
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else f"✅ 已记录: {result['dna']}")
        return

    if args.trend:
        result = audit.detect_trend()
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.report:
        print(audit.generate_report())
        return

    if args.full:
        results = audit.full_audit()
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if args.risk == "dna":
        result = audit.audit_dna_risk()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.risk == "p0":
        result = audit.audit_p0_risk()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.risk == "protocol":
        result = audit.audit_protocol_risk()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
