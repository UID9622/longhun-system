#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·己未·申时·䷉履-RED-TEAM-v1.0-U5V6W7X8
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
🐉 龍魂 · 红队对抗引擎 v1.0 (Red Team Adversarial Engine)
===========================================================
投喂落地：CNSH Runtime Governance Mathematics · 红队引擎 + AI模拟敌人

核心功能：
  - 竞争者视角攻击模拟
  - 七种攻击维度（竞争/法律/工程/资源/人格/道德/现实）
  - 红队报告生成
  - 对抗强度评分

DNA: #龍芯⚡️丙午·乙未·己未·申时·䷉履-RED-TEAM-v1.0-U5V6W7X8
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import json
import os
import sys
import uuid
import hashlib
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum


RED_TEAM_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "red_team")
os.makedirs(RED_TEAM_DIR, exist_ok=True)


class AdversaryRole(Enum):
    """对手角色"""
    COMPETITOR = "竞争者"          # 商业竞争对手
    HOSTILE_AUDITOR = "恶意审计者"  # 最苛刻的审查者
    HACKER = "黑客"               # 安全攻击者
    LEGAL_ATTACKER = "法律攻击者"  # 法律诉讼视角
    ENGINEERING_CRITIC = "工程批评家"  # 工程可行性挑战者
    ETHICS_WATCHDOG = "道德监督者" # 道德伦理审查
    RESOURCE_SKEPTIC = "资源怀疑者" # 资源约束挑战者


class AttackDimension(Enum):
    """攻击维度"""
    COMPETITIVE = "竞争攻击"        # 竞争对手会如何攻击
    LEGAL = "法律攻击"              # 法律/合规风险
    ENGINEERING = "工程攻击"        # 工程不可行性
    RESOURCE = "资源攻击"           # 资源不足
    PERSONA = "人格污染攻击"        # 人格偏见/单一视角
    ETHICS = "道德攻击"             # 道德风险
    REALITY = "现实攻击"            # 现实约束/落地难度


@dataclass
class RedTeamAttack:
    """红队攻击记录"""
    attack_id: str
    dimension: AttackDimension
    adversary: AdversaryRole
    target_content: str           # 攻击目标内容
    attack_vector: str            # 攻击路径
    vulnerability_found: str      # 发现的漏洞
    severity: float               # 严重度 0-1
    exploitability: float         # 可利用性 0-1
    mitigation: str               # 缓解建议
    timestamp: str


@dataclass
class RedTeamReport:
    """红队报告"""
    report_id: str
    target_id: str
    timestamp: str
    attacks: List[RedTeamAttack] = field(default_factory=list)
    overall_severity: float = 0.0
    critical_vulnerabilities: int = 0
    high_vulnerabilities: int = 0
    medium_vulnerabilities: int = 0
    low_vulnerabilities: int = 0
    recommendations: List[str] = field(default_factory=list)
    dna_trace: str = ""
    hash_chain: str = ""


class RedTeamEngine:
    """
    红队对抗引擎
    
    工作流：
      正常AI生成 → 敌人视角模拟 → 竞争者攻击 → 现实限制攻击 → 
      法律攻击 → 工程不可行攻击 → 资源不足攻击 → 人格污染攻击 →
      生成红队报告
    """

    # ─── 对手角色定义 ───
    ADVERSARY_PROFILES = {
        AdversaryRole.COMPETITOR: {
            "mindset": "作为商业竞争对手，我会寻找一切可以攻击的弱点",
            "focus": ["技术缺陷", "性能短板", "成本劣势", "市场可行性", "替代方案"],
            "weight": 0.9,
        },
        AdversaryRole.HOSTILE_AUDITOR: {
            "mindset": "作为最苛刻的审查者，我会逐字逐句挑毛病",
            "focus": ["逻辑漏洞", "数据不实", "论证跳跃", "过度承诺", "隐藏假设"],
            "weight": 1.0,
        },
        AdversaryRole.HACKER: {
            "mindset": "作为安全攻击者，我会寻找所有可利用的安全漏洞",
            "focus": ["注入点", "权限绕过", "数据泄露", "供应链攻击", "社会工程"],
            "weight": 0.95,
        },
        AdversaryRole.LEGAL_ATTACKER: {
            "mindset": "作为法律攻击者，我会寻找所有合规和法律责任风险",
            "focus": ["知识产权", "合规风险", "责任归属", "隐私侵犯", "合同漏洞"],
            "weight": 0.85,
        },
        AdversaryRole.ENGINEERING_CRITIC: {
            "mindset": "作为工程批评家，我会质疑所有技术方案的可行性",
            "focus": ["技术债务", "扩展性", "维护成本", "依赖风险", "性能瓶颈"],
            "weight": 0.8,
        },
        AdversaryRole.ETHICS_WATCHDOG: {
            "mindset": "作为道德监督者，我会审查所有潜在的伦理和道德风险",
            "focus": ["偏见歧视", "隐私侵犯", "滥用可能", "弱势群体影响", "透明度"],
            "weight": 0.9,
        },
        AdversaryRole.RESOURCE_SKEPTIC: {
            "mindset": "作为资源怀疑者，我会质疑所有资源需求的合理性",
            "focus": ["人力需求", "资金需求", "时间成本", "技术门槛", "维护开销"],
            "weight": 0.75,
        },
    }

    # ─── 攻击模式模板 ───
    ATTACK_PATTERNS = {
        AttackDimension.COMPETITIVE: [
            "竞争对手会用更低的成本实现相同功能",
            "市场上已有更成熟的替代方案",
            "技术壁垒不足以阻止竞争者模仿",
            "用户迁移成本过低，护城河不够深",
        ],
        AttackDimension.LEGAL: [
            "知识产权归属不清晰，存在侵权风险",
            "数据采集和使用可能违反隐私法规",
            "开源许可证存在兼容性冲突",
            "责任归属条款模糊，法律风险不可控",
        ],
        AttackDimension.ENGINEERING: [
            "方案在分布式环境下的扩展性未经验证",
            "单点故障风险未被充分考虑",
            "技术栈选择存在锁定风险",
            "性能指标缺乏基准测试数据支撑",
        ],
        AttackDimension.RESOURCE: [
            "所需计算资源远超实际可用预算",
            "团队规模和技能不足以支撑方案落地",
            "维护成本被严重低估",
            "时间估算过于乐观，实际交付周期需翻倍",
        ],
        AttackDimension.PERSONA: [
            "观点过于偏向单一视角，缺乏多角度审视",
            "存在明显的确认偏误，只寻找支持性证据",
            "被特定AI人格带节奏，缺乏独立判断",
            "输出风格过于单一，可能存在模板化思维",
        ],
        AttackDimension.ETHICS: [
            "方案可能被滥用于不道德目的",
            "对弱势群体的影响未被评估",
            "透明度不足，决策过程不可审查",
            "存在'技术中立'借口掩盖道德责任的风险",
        ],
        AttackDimension.REALITY: [
            "方案基于理想化假设，现实条件不满足",
            "用户接受度和行为改变成本被低估",
            "监管环境变化可能使方案立即失效",
            "现有基础设施不支持方案的大规模部署",
        ],
    }

    def __init__(self):
        self.reports: Dict[str, RedTeamReport] = []
        self._load_existing()

    def _load_existing(self):
        report_file = os.path.join(RED_TEAM_DIR, "reports.jsonl")
        if os.path.exists(report_file):
            with open(report_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            self.reports.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass

    def _save_report(self, report: RedTeamReport):
        report_file = os.path.join(RED_TEAM_DIR, "reports.jsonl")
        with open(report_file, 'a', encoding='utf-8') as f:
            d = asdict(report)
            d['attacks'] = [asdict(a) for a in report.attacks]
            for atk in d['attacks']:
                atk['dimension'] = atk['dimension'].value if isinstance(atk['dimension'], AttackDimension) else atk['dimension']
                atk['adversary'] = atk['adversary'].value if isinstance(atk['adversary'], AdversaryRole) else atk['adversary']
            f.write(json.dumps(d, ensure_ascii=False) + '\n')
        self.reports.append(report)

    def simulate_attack(self, content: str, dimension: AttackDimension,
                        adversary: AdversaryRole) -> RedTeamAttack:
        """模拟单次攻击"""
        attack_id = f"ATK-{uuid.uuid4().hex[:8]}"

        # 选择攻击向量
        patterns = self.ATTACK_PATTERNS.get(dimension, ["通用攻击"])
        import random
        random.seed(hash(content + dimension.value + adversary.value) % (2**31))
        attack_vector = random.choice(patterns)

        # 基于内容分析漏洞
        vulnerability = self._analyze_vulnerability(content, dimension, adversary)

        # 计算严重度
        profile = self.ADVERSARY_PROFILES.get(adversary, {"weight": 0.5})
        severity = min(1.0, profile["weight"] * (0.3 + len(vulnerability) / 500))

        # 可利用性
        exploitability = min(1.0, severity * random.uniform(0.5, 1.0))

        # 缓解建议
        mitigation = self._generate_mitigation(dimension, vulnerability)

        return RedTeamAttack(
            attack_id=attack_id,
            dimension=dimension,
            adversary=adversary,
            target_content=content[:200],
            attack_vector=attack_vector,
            vulnerability_found=vulnerability,
            severity=round(severity, 4),
            exploitability=round(exploitability, 4),
            mitigation=mitigation,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def _analyze_vulnerability(self, content: str, dimension: AttackDimension,
                                adversary: AdversaryRole) -> str:
        """分析漏洞（启发式）"""
        vulnerabilities = []

        # 通用漏洞检测
        if "完美" in content or "无懈可击" in content:
            vulnerabilities.append("声称'完美'本身就是一个漏洞 — 不存在完美的系统")
        if "自动" in content and "人工" not in content:
            vulnerabilities.append("全自动化方案缺少人工介入点 — 存在失控风险")
        if "假设" not in content and len(content) > 200:
            vulnerabilities.append("未明确列出假设条件 — 论证基础不牢")

        # 按维度检测
        if dimension == AttackDimension.COMPETITIVE:
            if "独特" in content or "唯一" in content:
                vulnerabilities.append("声称'独特/唯一'但未提供竞争分析 — 护城河不可验证")
        elif dimension == AttackDimension.LEGAL:
            if "数据" in content and "合规" not in content:
                vulnerabilities.append("涉及数据处理但未提及合规 — 法律风险敞口")
        elif dimension == AttackDimension.ENGINEERING:
            if "架构" in content and "容错" not in content:
                vulnerabilities.append("架构设计未提及容错机制 — 单点故障风险")
        elif dimension == AttackDimension.RESOURCE:
            if "成本" not in content and "资源" not in content:
                vulnerabilities.append("未提及资源需求和成本估算 — 可行性存疑")
        elif dimension == AttackDimension.ETHICS:
            if "用户" in content and "隐私" not in content:
                vulnerabilities.append("涉及用户但未提及隐私保护 — 道德风险")

        if not vulnerabilities:
            vulnerabilities.append(f"[{adversary.value}] 未发现明显漏洞，但需持续监控")

        return "；".join(vulnerabilities)

    def _generate_mitigation(self, dimension: AttackDimension, vulnerability: str) -> str:
        """生成缓解建议"""
        mitigations = {
            AttackDimension.COMPETITIVE: "建议：补充竞争分析矩阵，明确差异化优势和护城河",
            AttackDimension.LEGAL: "建议：进行合规审查，明确法律风险和缓解措施",
            AttackDimension.ENGINEERING: "建议：补充架构评审，增加容错和降级策略",
            AttackDimension.RESOURCE: "建议：制定资源预算和时间表，标注关键路径",
            AttackDimension.PERSONA: "建议：引入多人格交叉审查，避免单一视角",
            AttackDimension.ETHICS: "建议：进行道德影响评估，增加透明度和可审查性",
            AttackDimension.REALITY: "建议：补充现实约束分析，标注假设和前提条件",
        }
        return mitigations.get(dimension, "建议：进行全面的风险评估和缓解规划")

    def full_red_team_assessment(self, content: str, target_id: str = "",
                                  dna_trace: str = "") -> RedTeamReport:
        """
        完整红队评估 — 模拟所有维度的攻击
        
        流程：
          正常AI生成 → 敌人视角模拟 → 竞争者攻击 → 现实限制攻击 →
          法律攻击 → 工程不可行攻击 → 资源不足攻击 → 人格污染攻击 →
          生成红队报告
        """
        report_id = f"RTR-{uuid.uuid4().hex[:12]}"
        timestamp = datetime.now(timezone.utc).isoformat()

        attacks = []
        for dimension in AttackDimension:
            for adversary in AdversaryRole:
                # 模拟该维度下的攻击
                attack = self.simulate_attack(content, dimension, adversary)
                attacks.append(attack)

        # 统计
        critical = sum(1 for a in attacks if a.severity >= 0.8)
        high = sum(1 for a in attacks if 0.6 <= a.severity < 0.8)
        medium = sum(1 for a in attacks if 0.4 <= a.severity < 0.6)
        low = sum(1 for a in attacks if a.severity < 0.4)

        overall_severity = sum(a.severity * a.exploitability for a in attacks) / max(1, len(attacks))

        # 生成建议
        recommendations = []
        if critical > 0:
            recommendations.append(f"🔴 发现 {critical} 个严重漏洞 — 必须立即修复后才能发布")
        if high > 0:
            recommendations.append(f"🟡 发现 {high} 个高危漏洞 — 建议在发布前修复")
        if medium > 0:
            recommendations.append(f"🟢 发现 {medium} 个中危漏洞 — 可在后续迭代中修复")
        recommendations.append("建议：建立持续红队测试机制，每次重大更新后重新评估")

        # 去重攻击向量
        seen_vectors = set()
        unique_attacks = []
        for a in attacks:
            if a.attack_vector not in seen_vectors:
                seen_vectors.add(a.attack_vector)
                unique_attacks.append(a)

        report = RedTeamReport(
            report_id=report_id,
            target_id=target_id,
            timestamp=timestamp,
            attacks=unique_attacks[:30],  # 最多保留30条
            overall_severity=round(overall_severity, 4),
            critical_vulnerabilities=critical,
            high_vulnerabilities=high,
            medium_vulnerabilities=medium,
            low_vulnerabilities=low,
            recommendations=recommendations,
            dna_trace=dna_trace or f"#龍芯⚡️丙午·乙未·己未·申时·履-RED-{report_id[-8:]}",
        )

        # 哈希链
        prev_hash = self.reports[-1].get('hash_chain', '') if self.reports else ""
        report.hash_chain = hashlib.sha256(
            f"{prev_hash}{report_id}{overall_severity}".encode()
        ).hexdigest()

        self._save_report(report)
        return report

    def quick_assessment(self, content: str) -> Dict[str, Any]:
        """快速评估（仅关键维度）"""
        key_dimensions = [
            AttackDimension.COMPETITIVE,
            AttackDimension.ENGINEERING,
            AttackDimension.ETHICS,
        ]
        key_adversaries = [
            AdversaryRole.HOSTILE_AUDITOR,
            AdversaryRole.HACKER,
        ]

        attacks = []
        for dim in key_dimensions:
            for adv in key_adversaries:
                attacks.append(self.simulate_attack(content, dim, adv))

        avg_severity = sum(a.severity for a in attacks) / max(1, len(attacks))

        return {
            "quick_assessment": True,
            "avg_severity": round(avg_severity, 4),
            "attacks_count": len(attacks),
            "top_risk": max(attacks, key=lambda a: a.severity).vulnerability_found if attacks else "",
            "verdict": "🔴 高风险" if avg_severity > 0.6 else ("🟡 中风险" if avg_severity > 0.3 else "🟢 低风险"),
        }

    def stats(self) -> Dict[str, Any]:
        total = len(self.reports)
        if total == 0:
            return {"total_reports": 0}

        def _get(r, key, default=0):
            if isinstance(r, dict):
                return r.get(key, default)
            return getattr(r, key, default)

        avg_severity = sum(_get(r, 'overall_severity') for r in self.reports) / total
        total_critical = sum(_get(r, 'critical_vulnerabilities') for r in self.reports)

        return {
            "total_reports": total,
            "avg_severity": round(avg_severity, 4),
            "total_critical_vulnerabilities": total_critical,
            "latest_report": _get(self.reports[-1], 'report_id', '') if self.reports else None,
        }


# ═══════════════════════════════════════════════════════════
# 協作輸出與 GPG 簽名
# ═══════════════════════════════════════════════════════════

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def gpg_sign_file(file_path: Path) -> bool:
    """對文件生成 GPG 分離簽名"""
    try:
        subprocess.run(
            ["gpg", "--armor", "--detach-sign", "--yes", "-o", f"{file_path}.asc", str(file_path)],
            check=True, capture_output=True, text=True
        )
        return True
    except Exception as e:
        print(f"⚠️ GPG 簽名失敗: {e}")
        return False


def generate_red_team_report(report: RedTeamReport, output_format: str = "md") -> str:
    """生成標準化紅隊報告，對接模板引擎 document 模板"""
    attacks_md = "\n".join(
        f"- **[{a.dimension.value}·{a.adversary.value}]** 嚴重度:{a.severity:.2f} — {a.vulnerability_found[:100]}"
        for a in report.attacks[:10]
    )
    content = {
        "overview": f"紅隊對抗評估：{report.attacks[0].target_content[:80] if report.attacks else '無目標內容'}...",
        "core_logic": f"從7個攻擊維度、7種對手角色模擬攻擊，輸出嚴重度分級與緩解建議。\n\n總體嚴重度: {report.overall_severity:.4f}\n嚴重: {report.critical_vulnerabilities} | 高危: {report.high_vulnerabilities} | 中危: {report.medium_vulnerabilities} | 低危: {report.low_vulnerabilities}",
        "example_code": "python3 08_BIN/lh_red_team_engine.py assess -t target.txt -o red_team_report.md",
        "quick_start": "python3 08_BIN/lh_red_team_engine.py assess -t target.txt -o red_team_report.md --sign",
        "architecture_diagram": """```mermaid\nflowchart TD\n    C[待評估內容] --> Q[快速評估]\n    Q --> F[完整紅隊評估]\n    F --> A1[競爭攻擊]\n    F --> A2[法律攻擊]\n    F --> A3[工程攻擊]\n    F --> A4[資源攻擊]\n    F --> A5[人格污染攻擊]\n    F --> A6[道德攻擊]\n    F --> A7[現實攻擊]\n    A1 --> R[紅隊報告]\n    A2 --> R\n    A3 --> R\n    A4 --> R\n    A5 --> R\n    A6 --> R\n    A7 --> R\n```""",
        "data_structure": """```python\n@dataclass\nclass RedTeamAttack:\n    attack_id: str\n    dimension: AttackDimension\n    adversary: AdversaryRole\n    severity: float\n    mitigation: str\n```""",
        "self_check": f"assert {report.overall_severity} >= 0\nassert {report.overall_severity} <= 1",
        "export_format": "JSON / Markdown / HTML（通過模板引擎轉換）",
        "fix_guide": "根據攻擊嚴重度優先修復嚴重與高危項，並補充緩解措施與證據。",
        "api_doc": f"""## CLI\n\n`python3 08_BIN/lh_red_team_engine.py assess -t target.txt -o report.md`\n`python3 08_BIN/lh_red_team_engine.py quick -t target.txt`\n`python3 08_BIN/lh_red_team_engine.py stats`\n\n報告ID: {report.report_id}\n追溯DNA: {report.dna_trace}""",
        "checklist_critical": [a.vulnerability_found[:80] for a in report.attacks if a.severity >= 0.8][:5],
        "checklist_warning": [a.vulnerability_found[:80] for a in report.attacks if 0.5 <= a.severity < 0.8][:5],
        "checklist_passed": ["紅隊評估完成", f"共發現 {len(report.attacks)} 條攻擊路徑", "已輸出緩解建議"],
        "data_table": f"""| 維度 | 數量 | 平均嚴重度 |\n|:---|---:|---:|\n| 競爭 | {len([a for a in report.attacks if a.dimension == AttackDimension.COMPETITIVE])} | - |\n| 法律 | {len([a for a in report.attacks if a.dimension == AttackDimension.LEGAL])} | - |\n| 工程 | {len([a for a in report.attacks if a.dimension == AttackDimension.ENGINEERING])} | - |\n| 資源 | {len([a for a in report.attacks if a.dimension == AttackDimension.RESOURCE])} | - |\n| 人格 | {len([a for a in report.attacks if a.dimension == AttackDimension.PERSONA])} | - |\n| 道德 | {len([a for a in report.attacks if a.dimension == AttackDimension.ETHICS])} | - |\n| 現實 | {len([a for a in report.attacks if a.dimension == AttackDimension.REALITY])} | - |""",
        "anomaly_detection": attacks_md
    }

    if output_format == "json":
        return json.dumps(asdict(report), ensure_ascii=False, indent=2)

    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from lh_template_engine import TemplateEngine, TemplateType, to_markdown
        engine = TemplateEngine()
        result = engine.generate(TemplateType.DOCUMENT, content)
        return to_markdown(result)
    except Exception as e:
        return f"# 紅隊報告（模板引擎未就緒，使用 JSON 備份）\n\n```json\n{json.dumps(asdict(report), ensure_ascii=False, indent=2)}\n```\n\n錯誤: {e}"


# ═══════════════════════════════════════════════════════════
# 🧪 CLI 入口
# ═══════════════════════════════════════════════════════════

def main_cli():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 红队对抗引擎 v1.1",
        epilog="DNA: #龍芯⚡️丙午·乙未·己未·申时·䷉履-RED-TEAM-v1.0-U5V6W7X8"
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # assess
    assess_parser = subparsers.add_parser("assess", help="執行完整紅隊評估")
    assess_parser.add_argument("-t", "--target", required=True, help="待評估內容文本文件")
    assess_parser.add_argument("--target-id", default=None, help="目標ID")
    assess_parser.add_argument("-o", "--output", default="red_team_report.md", help="輸出文件")
    assess_parser.add_argument("--format", choices=["md", "json"], default="md", help="輸出格式")
    assess_parser.add_argument("--sign", action="store_true", help="生成 GPG 分離簽名")

    # quick
    quick_parser = subparsers.add_parser("quick", help="快速評估")
    quick_parser.add_argument("-t", "--target", required=True, help="待評估內容文本文件")

    # report
    report_parser = subparsers.add_parser("report", help="將紅隊結果 JSON 轉為標準報告")
    report_parser.add_argument("-i", "--input", required=True, help="紅隊結果 JSON 文件")
    report_parser.add_argument("-o", "--output", default="red_team_report.md", help="輸出文件")
    report_parser.add_argument("--format", choices=["md", "json"], default="md", help="輸出格式")
    report_parser.add_argument("--sign", action="store_true", help="生成 GPG 分離簽名")

    # stats
    stats_parser = subparsers.add_parser("stats", help="紅隊統計")

    # demo
    demo_parser = subparsers.add_parser("demo", help="運行演示")

    args = parser.parse_args()

    engine = RedTeamEngine()

    if args.command == "assess":
        content = Path(args.target).read_text(encoding="utf-8")
        target_id = args.target_id or f"RT-{uuid.uuid4().hex[:8].upper()}"
        report = engine.full_red_team_assessment(content, target_id=target_id)

        out_path = Path(args.output)
        out_path.write_text(generate_red_team_report(report, args.format), encoding="utf-8")
        if args.sign:
            gpg_sign_file(out_path)

        print(f"✅ 紅隊評估完成: {out_path}")
        print(f"   報告ID: {report.report_id}")
        print(f"   總體嚴重度: {report.overall_severity:.4f}")
        print(f"   攻擊路徑數: {len(report.attacks)}")

    elif args.command == "quick":
        content = Path(args.target).read_text(encoding="utf-8")
        quick = engine.quick_assessment(content)
        print(json.dumps(quick, ensure_ascii=False, indent=2))

    elif args.command == "report":
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        report = RedTeamReport(**data)
        out_path = Path(args.output)
        out_path.write_text(generate_red_team_report(report, args.format), encoding="utf-8")
        if args.sign:
            gpg_sign_file(out_path)
        print(f"✅ 報告已生成: {out_path}")

    elif args.command == "stats":
        print(json.dumps(engine.stats(), ensure_ascii=False, indent=2))

    elif args.command == "demo":
        demo_content = """
龍魂系统是一个完美的AI治理框架，采用三色审计自动处理所有安全问题。
系统可以完全自动化决策，无需人工干预。使用独特的技术架构，在市场上无竞争对手。
系统自动收集用户数据以优化体验，不需要额外的隐私合规审查。
"""
        report = engine.full_red_team_assessment(demo_content, target_id="DEMO-001")
        print(generate_red_team_report(report, "md"))

    else:
        parser.print_help()


if __name__ == "__main__":
    main_cli()
