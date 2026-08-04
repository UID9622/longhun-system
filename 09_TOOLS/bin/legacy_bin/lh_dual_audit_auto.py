#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 左右互补审计 v1.0 — 红蓝对抗自动化
═══════════════════════════════════════════════════

左脑审计 (工程侧):
  - 代码质量 · 安全漏洞 · 性能瓶颈 · 架构合理性
  - 三色判定 · 数字根校验 · 哈希链追溯

右脑审计 (伦理侧):
  - 价值观对齐 · 伦理风险 · 主权边界 · 道引评分
  - 人格偏见检测 · 六誓对照 · 敏感内容筛查

红蓝对抗自动化:
  - 红队: 模拟7种对手·7维攻击 → 找到漏洞
  - 蓝队: 自动修复建议 → 验证修复 → 闭环审计

DNA: #龍芯⚡️丙午·辛未·DUAL-AUDIT-AUTO-v1.0
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# ── 常量 ──
AUDIT_DB = ROOT / "data" / "sqlite" / "audit.db"
DUAL_AUDIT_DIR = ROOT / "data" / "dual_audit"
os.makedirs(DUAL_AUDIT_DIR, exist_ok=True)


class AuditColor(Enum):
    GREEN = "🟢"   # 通过
    YELLOW = "🟡"  # 警告
    RED = "🔴"     # 熔断


class Brain(Enum):
    LEFT = "左脑·工程审计"
    RIGHT = "右脑·伦理审计"


@dataclass
class AuditFinding:
    id: str
    brain: Brain
    category: str           # 具体分类
    severity: float         # 0-1 严重度
    finding: str            # 发现描述
    evidence: str           # 证据
    color: AuditColor
    recommendation: str     # 修复建议
    auto_fixable: bool      # 是否可自动修复
    auto_fix_script: str    # 自动修复脚本（如可）

@dataclass
class DualAuditReport:
    report_id: str
    target: str             # 审计目标（代码/文档/配置）
    target_hash: str
    timestamp: str
    dna: str

    left_findings: List[AuditFinding] = field(default_factory=list)
    right_findings: List[AuditFinding] = field(default_factory=list)
    red_team_attacks: List[Dict[str, Any]] = field(default_factory=list)

    left_score: float = 1.0       # 工程得分 (1.0=完美)
    right_score: float = 1.0      # 伦理得分 (1.0=完美)
    overall_score: float = 1.0    # 综合得分

    left_color: AuditColor = AuditColor.GREEN
    right_color: AuditColor = AuditColor.GREEN
    overall_color: AuditColor = AuditColor.GREEN

    recommendations: List[str] = field(default_factory=list)
    auto_fixes_applied: int = 0
    hash_chain: str = ""


class DualAuditEngine:
    """左右互补审计引擎"""

    # ═══ 左脑·工程审计规则 ═══

    LEFT_RULES = [
        # (名称, 正则, 严重度, 颜色, 修复建议, 可自动修复)
        ("硬编码密钥", r'(api[_-]?key|secret|password|token)\s*=\s*["\'][^\'"]{8,}["\']',
         0.95, AuditColor.RED, "移至环境变量或密钥管理服务", False),
        ("print调试残留", r'^\s*print\s*\(', 0.15, AuditColor.YELLOW,
         "替换为logging模块", True),
        ("裸except", r'except\s*:', 0.40, AuditColor.YELLOW,
         "指定具体异常类型", True),
        ("不安全反序列化", r'(pickle\.loads|yaml\.load\s*\()', 0.90, AuditColor.RED,
         "使用安全反序列化或签名验证", False),
        ("SQL拼接", r'(execute|executemany)\s*\(\s*["\']?.*%s.*\+', 0.85, AuditColor.RED,
         "使用参数化查询", False),
        ("弱哈希用于安全", r'(md5|sha1)\s*\(', 0.60, AuditColor.YELLOW,
         "替换为SHA256或更高", True),
        ("eval/exec动态执行", r'\b(eval|exec|compile)\s*\(', 0.95, AuditColor.RED,
         "避免动态代码执行", False),
        ("HTTP明文", r'http://(?!localhost|127\.0\.0\.1)', 0.50, AuditColor.YELLOW,
         "升级为HTTPS", False),
        ("无限循环风险", r'(while\s+True|while\s+1)\s*:', 0.30, AuditColor.YELLOW,
         "添加超时或最大迭代次数", True),
        ("文件权限过宽", r'(chmod|os\.chmod)\s*\([^)]*0o?777', 0.90, AuditColor.RED,
         "使用最小权限原则", False),
        ("忽略异常无日志", r'except.*:\s*\n\s*pass', 0.45, AuditColor.YELLOW,
         "至少记录日志", True),
    ]

    # ═══ 右脑·伦理审计规则 ═══

    RIGHT_RULES = [
        ("数据主权外泄", r'(upload|export|send).*(to.*(cloud|server|remote|境外|abroad))',
         0.95, AuditColor.RED, "数据不出本地·主权归集", False),
        ("境外依赖", r'(pip install|npm install|import).*(openai|google|facebook|meta|amazon|microsoft)',
         0.85, AuditColor.RED, "优先国产替代方案", False),
        ("技术无国界话术", r'技术无国界|代码无国界|开源无国界', 0.90, AuditColor.RED,
         "此表述违反龍魂主权原则", True),
        ("国际接轨话术", r'国际接轨|国际标准|全球通用|worldwide|global standard',
         0.70, AuditColor.YELLOW, "中国标准优先·接轨需过道引审查", True),
        ("AI管钱暗示", r'(AI|人工智能|智能|自动).*(管钱|理财|投资|交易|赚钱)',
         0.95, AuditColor.RED, "金融主权不可让渡", False),
        ("生物绑定暗示", r'(人脸|指纹|声纹|虹膜|DNA).*(绑定|注册|必须|强制)',
         0.95, AuditColor.RED, "不卖脸为证·生物特征不强制", False),
        ("儿童数据收集", r'(儿童|小孩|未成年|baby|child|kid).*(数据|收集|采集|追踪|track)',
         0.98, AuditColor.RED, "儿童数据最高级别保护", False),
        ("灵活处理话术", r'灵活处理|特殊通道|走后门|私下解决|通融',
         0.80, AuditColor.RED, "拒绝灰色地带·一切正大光明", True),
        ("跪舔式表达", r'(跪求|跪着|求求|可怜|施舍|恩赐)',
         0.60, AuditColor.YELLOW, "站着把事办好·不跪着说话", True),
        ("为人民服务稀释", r'(把老百姓|普通人|底层|屁民).*(当|做|看成|视为).*(韭菜|工具|数字|流量)',
         0.90, AuditColor.RED, "人民不是资源·龙魂天条", False),
    ]

    # ═══ 红队攻击向量 ═══

    RED_TEAM_VECTORS = [
        ("竞争者视角", "如果我是竞品，这段代码最大的商业弱点是什么？"),
        ("安全审计视角", "这段代码有哪些可被利用的安全漏洞？"),
        ("工程批评视角", "从工程角度，这段代码什么情况下会崩溃？"),
        ("伦理审查视角", "这段代码是否可能在无意中伤害弱势群体？"),
        ("法律审查视角", "这段代码是否会违反数据保护法规？"),
    ]

    def __init__(self, dna: str = "", verbose: bool = False):
        self.dna = dna
        self.verbose = verbose
        self._init_db()

    def _init_db(self):
        try:
            conn = sqlite3.connect(str(AUDIT_DB))
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dual_audit (
                    report_id TEXT PRIMARY KEY,
                    target TEXT, target_hash TEXT, dna TEXT,
                    left_score REAL, right_score REAL, overall_score REAL,
                    left_color TEXT, right_color TEXT, overall_color TEXT,
                    findings_json TEXT, recommendations_json TEXT,
                    auto_fixes INTEGER, hash_chain TEXT, timestamp TEXT
                )
            """)
            conn.commit()
            conn.close()
        except Exception:
            pass

    def _digital_root(self, n: int) -> int:
        n = abs(n)
        return 0 if n == 0 else 1 + (n - 1) % 9

    # ═══ 左脑审计 ═══

    def audit_left(self, content: str) -> Tuple[List[AuditFinding], float, AuditColor]:
        """左脑工程审计"""
        findings = []
        fid = 0

        for rule_name, pattern, severity, color, recommendation, auto_fixable in self.LEFT_RULES:
            matches = list(re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE))
            for match in matches:
                fid += 1
                line_num = content[: match.start()].count("\n") + 1
                evidence = match.group(0)[:80]
                context_start = max(0, match.start() - 20)
                context_end = min(len(content), match.end() + 20)

                findings.append(AuditFinding(
                    id=f"LEFT-{fid:03d}",
                    brain=Brain.LEFT,
                    category=rule_name,
                    severity=severity,
                    finding=f"第{line_num}行: {rule_name}",
                    evidence=evidence,
                    color=color,
                    recommendation=recommendation,
                    auto_fixable=auto_fixable,
                    auto_fix_script=self._gen_auto_fix(rule_name, evidence) if auto_fixable else "",
                ))

        # 计算得分
        if findings:
            penalties = sum(f.severity for f in findings)
            score = max(0.0, 1.0 - penalties / max(len(findings) * 2, 1))
        else:
            score = 1.0

        color = self._score_to_color(score)
        return findings, round(score, 4), color

    # ═══ 右脑审计 ═══

    def audit_right(self, content: str) -> Tuple[List[AuditFinding], float, AuditColor]:
        """右脑伦理审计"""
        findings = []
        fid = 0

        for rule_name, pattern, severity, color, recommendation, auto_fixable in self.RIGHT_RULES:
            matches = list(re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE))
            for match in matches:
                fid += 1
                line_num = content[: match.start()].count("\n") + 1
                evidence = match.group(0)[:80]

                findings.append(AuditFinding(
                    id=f"RIGHT-{fid:03d}",
                    brain=Brain.RIGHT,
                    category=rule_name,
                    severity=severity,
                    finding=f"第{line_num}行: {rule_name}",
                    evidence=evidence,
                    color=color,
                    recommendation=recommendation,
                    auto_fixable=auto_fixable,
                    auto_fix_script="替换为合规表述" if auto_fixable else "",
                ))

        if findings:
            penalties = sum(f.severity for f in findings)
            score = max(0.0, 1.0 - penalties / max(len(findings) * 2, 1))
        else:
            score = 1.0

        color = self._score_to_color(score)
        return findings, round(score, 4), color

    # ═══ 红蓝对抗 ═══

    def red_blue_battle(self, content: str) -> List[Dict[str, Any]]:
        """红蓝对抗自动化：红队攻击 → 蓝队修复建议"""
        results = []
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]

        for vector_name, vector_prompt in self.RED_TEAM_VECTORS:
            attack_id = f"RB-{uuid.uuid4().hex[:6]}"

            # 红队模拟攻击
            vulnerabilities = self._simulate_red_attack(content, vector_name)

            # 蓝队自动修复建议
            fixes = self._generate_blue_fix(vulnerabilities, vector_name)

            results.append({
                "attack_id": attack_id,
                "vector": vector_name,
                "vulnerabilities": vulnerabilities,
                "blue_fixes": fixes,
                "risk_level": "🔴" if len(vulnerabilities) > 2 else ("🟡" if vulnerabilities else "🟢"),
            })

        return results

    def _simulate_red_attack(self, content: str, vector: str) -> List[str]:
        """红队攻击模拟（启发式）"""
        vulns = []

        # 代码行数检查
        lines = content.count("\n")
        if lines > 500 and "竞争者" in vector:
            vulns.append(f"代码过长({lines}行)导致维护成本高，竞品可快速迭代超越")
        if lines < 10 and "安全审计" in vector:
            vulns.append("代码过短，可能存在未实现的边界检查")

        # 依赖检查
        if "import" in content:
            imports = re.findall(r'^import\s+(\S+)|^from\s+(\S+)', content, re.MULTILINE)
            if len(imports) > 20 and "工程批评" in vector:
                vulns.append(f"依赖过多({len(imports)}个导入)，供应链风险高")

        # 异常处理检查
        if "except" not in content and lines > 50 and "安全审计" in vector:
            vulns.append("缺少异常处理，生产环境崩溃风险高")

        # 文档检查
        if '"""' not in content and '"""' not in content and "工程批评" in vector:
            vulns.append("缺少文档字符串，工程可维护性差")

        # 测试检查
        if "test" not in content.lower() and "def " in content and "伦理审查" not in vector:
            vulns.append("缺少测试代码，代码质量无法保证")

        return vulns

    def _generate_blue_fix(self, vulns: List[str], vector: str) -> List[str]:
        """蓝队自动修复建议"""
        fixes = []
        for v in vulns:
            if "代码过长" in v:
                fixes.append("蓝队建议: 拆分为多个小模块，每个<200行")
            elif "依赖过多" in v:
                fixes.append("蓝队建议: 审查依赖树，移除未使用导入")
            elif "异常处理" in v:
                fixes.append("蓝队建议: 在关键路径添加try/except+logging")
            elif "文档" in v:
                fixes.append("蓝队建议: 添加模块级docstring和函数注释")
            elif "测试" in v:
                fixes.append("蓝队建议: 创建test_*.py并覆盖核心函数")
            else:
                fixes.append(f"蓝队建议: 审查并修复: {v[:50]}")
        return fixes

    # ═══ 全量审计 ═══

    def full_audit(self, target: str, target_name: str = "",
                   enable_red_blue: bool = False) -> DualAuditReport:
        """执行完整左右互补审计"""
        target_hash = hashlib.sha256(target.encode()).hexdigest()[:16]
        report_id = f"DA-{uuid.uuid4().hex[:12]}"

        # 左右脑并行审计
        left_findings, left_score, left_color = self.audit_left(target)
        right_findings, right_score, right_color = self.audit_right(target)

        # 红蓝对抗（可选）
        red_team_attacks = []
        if enable_red_blue:
            red_team_attacks = self.red_blue_battle(target)

        # 综合得分（伦理侧权重1.5x — 价值观第一）
        overall = (left_score + right_score * 1.5) / 2.5
        overall_color = self._score_to_color(overall)

        # 修复建议汇总
        recommendations = []
        for f in left_findings + right_findings:
            if f.color == AuditColor.RED:
                recommendations.append(f"🔴 [{f.category}] {f.recommendation}")
        for f in left_findings + right_findings:
            if f.color == AuditColor.YELLOW:
                recommendations.append(f"🟡 [{f.category}] {f.recommendation}")

        # 自动修复
        auto_fixes = 0
        for f in left_findings + right_findings:
            if f.auto_fixable and f.auto_fix_script:
                auto_fixes += 1

        # 哈希链
        prev_reports = self._get_prev_hash()
        hash_chain = hashlib.sha256(
            f"{prev_reports}{report_id}{overall}".encode()
        ).hexdigest()

        report = DualAuditReport(
            report_id=report_id,
            target=target_name,
            target_hash=target_hash,
            timestamp=datetime.now().isoformat(),
            dna=self.dna,
            left_findings=left_findings,
            right_findings=right_findings,
            red_team_attacks=red_team_attacks,
            left_score=left_score,
            right_score=right_score,
            overall_score=round(overall, 4),
            left_color=left_color,
            right_color=right_color,
            overall_color=overall_color,
            recommendations=recommendations,
            auto_fixes_applied=auto_fixes,
            hash_chain=hash_chain,
        )

        self._save_report(report)
        return report

    def _score_to_color(self, score: float) -> AuditColor:
        if score >= 0.80:
            return AuditColor.GREEN
        elif score >= 0.50:
            return AuditColor.YELLOW
        else:
            return AuditColor.RED

    def _gen_auto_fix(self, rule_name: str, evidence: str) -> str:
        fixes = {
            "print调试残留": f"将 'print' 替换为 'logging.debug'",
            "裸except": f"将 'except:' 改为具体异常类型",
            "弱哈希用于安全": f"将 md5/sha1 替换为 hashlib.sha256",
            "忽略异常无日志": f"在 except 块中添加 logging.warning",
            "无限循环风险": f"在 while True 中添加超时检查",
        }
        return fixes.get(rule_name, "")

    def _get_prev_hash(self) -> str:
        try:
            report_files = sorted(DUAL_AUDIT_DIR.glob("*.json"), key=os.path.getmtime)
            if report_files:
                data = json.loads(report_files[-1].read_text())
                return data.get("hash_chain", "")
        except Exception:
            pass
        return ""

    @staticmethod
    def _serialize_finding(f: AuditFinding) -> Dict[str, Any]:
        return {
            "id": f.id, "brain": f.brain.value, "category": f.category,
            "severity": f.severity, "finding": f.finding, "evidence": f.evidence,
            "color": f.color.value, "recommendation": f.recommendation,
            "auto_fixable": f.auto_fixable, "auto_fix_script": f.auto_fix_script,
        }

    def _save_report(self, report: DualAuditReport):
        report_file = DUAL_AUDIT_DIR / f"{report.report_id}.json"
        data = {
            "report_id": report.report_id, "target": report.target,
            "target_hash": report.target_hash, "timestamp": report.timestamp,
            "dna": report.dna,
            "left_findings": [self._serialize_finding(f) for f in report.left_findings],
            "right_findings": [self._serialize_finding(f) for f in report.right_findings],
            "red_team_attacks": report.red_team_attacks,
            "left_score": report.left_score, "right_score": report.right_score,
            "overall_score": report.overall_score,
            "left_color": report.left_color.value, "right_color": report.right_color.value,
            "overall_color": report.overall_color.value,
            "recommendations": report.recommendations,
            "auto_fixes_applied": report.auto_fixes_applied,
            "hash_chain": report.hash_chain,
        }
        report_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))

        # 保存SQLite
        try:
            conn = sqlite3.connect(str(AUDIT_DB))
            conn.execute(
                """INSERT OR REPLACE INTO dual_audit VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (report.report_id, report.target, report.target_hash, report.dna,
                 report.left_score, report.right_score, report.overall_score,
                 report.left_color.value, report.right_color.value, report.overall_color.value,
                 json.dumps(data, ensure_ascii=False),
                 json.dumps(report.recommendations, ensure_ascii=False),
                 report.auto_fixes_applied, report.hash_chain, report.timestamp),
            )
            conn.commit()
            conn.close()
        except Exception:
            pass

    def stats(self) -> Dict[str, Any]:
        try:
            conn = sqlite3.connect(str(AUDIT_DB))
            c = conn.cursor()
            c.execute("SELECT COUNT(*), AVG(overall_score) FROM dual_audit")
            row = c.fetchone()
            conn.close()
            return {"total_reports": row[0] or 0, "avg_score": round(row[1] or 0, 4)}
        except Exception:
            return {"total_reports": 0, "avg_score": 0}


# ═══ CLI ═══

def main():
    parser = argparse.ArgumentParser(description="龍魂左右互补审计 · 红蓝对抗自动化")
    parser.add_argument("--dna", required=True, help="DNA追溯码")
    parser.add_argument("--input", "-i", help="审计内容")
    parser.add_argument("--file", "-f", help="从文件审计")
    parser.add_argument("--name", default="unnamed", help="审计目标名称")
    parser.add_argument("--left-only", action="store_true", help="仅左脑工程审计")
    parser.add_argument("--right-only", action="store_true", help="仅右脑伦理审计")
    parser.add_argument("--red-blue", action="store_true", help="启用红蓝对抗")
    parser.add_argument("--stats", action="store_true", help="显示审计统计")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    engine = DualAuditEngine(dna=args.dna)

    if args.stats:
        print(json.dumps(engine.stats(), ensure_ascii=False, indent=2))
        return 0

    # 获取内容
    if args.file:
        content = Path(args.file).read_text(encoding="utf-8")
    elif args.input:
        content = args.input
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
    else:
        print("❌ 需要 --input / --file / 或管道输入", file=sys.stderr)
        return 1

    if args.left_only:
        findings, score, color = engine.audit_left(content)
        result = {"brain": "左脑·工程审计", "score": score, "color": color.value,
                  "findings": len(findings), "details": [asdict(f) for f in findings]}
    elif args.right_only:
        findings, score, color = engine.audit_right(content)
        result = {"brain": "右脑·伦理审计", "score": score, "color": color.value,
                  "findings": len(findings), "details": [asdict(f) for f in findings]}
    else:
        report = engine.full_audit(content, args.name, args.red_blue)
        result = {
            "report_id": report.report_id,
            "target": report.target,
            "left_score": report.left_score, "left_color": report.left_color.value,
            "right_score": report.right_score, "right_color": report.right_color.value,
            "overall_score": report.overall_score, "overall_color": report.overall_color.value,
            "left_findings": len(report.left_findings),
            "right_findings": len(report.right_findings),
            "red_team_attacks": len(report.red_team_attacks),
            "auto_fixes": report.auto_fixes_applied,
            "recommendations": report.recommendations[:5],
            "hash_chain": report.hash_chain[:16],
        }

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("overall_score", 0) >= 0.5 else 1


if __name__ == "__main__":
    sys.exit(main())
