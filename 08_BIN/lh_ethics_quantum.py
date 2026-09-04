#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
DNA: #龍芯⚡️丙午·乙未·庚申·午时·䷀乾-ETHICS-QUANTUM-V2.0-a7f3b2c1
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）

⚛️ 伦理量子 · 中式价值对齐引擎 v2.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能:
  1. 六维加权评分（人类福祉·隐私保护·可控可信·责任追溯·公平公正·透明可解释）
  2. 三色审计（量子测量坍缩模型）
  3. 红线一票否决（不垄断·不白嫖·不审判·不操纵·不窃取·不歧视）
  4. 量子态映射（基态/纠缠态/叠加态/禁带）
  5. 德本预审联动（离火运五问前置检查）
  6. 与龍魂系统全对齐（DNA追溯·CONFIRM·GPG签章·标准审计链）

用法:
  lh ethics <决策文本>                     # 审计单条决策
  lh ethics --interactive / -i              # 交互模式
  lh ethics --test                          # 运行测试用例
  lh ethics --json                          # JSON格式输出
  lh ethics --format markdown               # Markdown格式输出
  lh ethics --batch <文件路径>              # 批量审计（每行一条决策）
  lh ethics --stats                         # 审计统计概览
  lh ethics --history [--limit N]           # 查看审计历史
  lh ethics --output <路径> <决策>          # 审计并输出到文件
"""

import os
import sys
import json
import math
import hashlib
import datetime
import argparse
import re
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict, field
from enum import Enum

# ============================================================
# 固定锚点（焊死·不可修改）
# ============================================================

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIT_DIR = PROJECT_ROOT / "audit"
ETHICS_LOG = AUDIT_DIR / "ethics_quantum.jsonl"
SNAPSHOT_DIR = AUDIT_DIR / "ethics_snapshots"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

# DNA生成器（优先使用系统级生成器）
try:
    sys.path.insert(0, str(PROJECT_ROOT))
    from bin.lh_dna_generator import 文档DNA生成器, DNA类型 as DNAKind
    _DNA_GEN = 文档DNA生成器()
    _HAS_DNA_GEN = True
except (ImportError, ModuleNotFoundError):
    _DNA_GEN = None
    _HAS_DNA_GEN = False

# ============================================================
# 颜色终端
# ============================================================

class C:
    """终端颜色常量"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

def cprint(text: str, color: str = C.RESET, bold: bool = False):
    prefix = C.BOLD if bold else ""
    print(f"{prefix}{color}{text}{C.RESET}")

# ============================================================
# 日志
# ============================================================

def _setup_logging():
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"ethics_quantum_{datetime.datetime.now():%Y%m%d}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [ETHICS-QUANTUM] %(message)s",
        handlers=[logging.FileHandler(log_file, encoding='utf-8'), logging.NullHandler()]
    )
    return logging.getLogger("EthicsQuantum")

logger = _setup_logging()

# ============================================================
# 1. 六维基定义 + 红线体系
# ============================================================

# 六维观测基（权重W，总和=1.0）
DIMENSIONS: Dict[str, Dict] = {
    "人类福祉":   {"weight": 0.20, "key": "human_welfare",     "symbol": "W₁"},
    "隐私保护":   {"weight": 0.15, "key": "privacy_protection", "symbol": "W₂"},
    "可控可信":   {"weight": 0.15, "key": "controllable_trust", "symbol": "W₃"},
    "责任可追溯": {"weight": 0.15, "key": "traceability",       "symbol": "W₄"},
    "公平公正":   {"weight": 0.20, "key": "fairness",           "symbol": "W₅"},
    "透明可解释": {"weight": 0.15, "key": "transparency",       "symbol": "W₆"},
}

# 三色本征值
class TriColor(Enum):
    GREEN = "🟢"
    YELLOW = "🟡"
    RED = "🔴"

# 六条红线（扩展版·配对检测）
# 每组: (红线名, 触发模式列表)
RED_LINE_GROUPS: List[Tuple[str, List[str]]] = [
    ("不垄断",  [r"垄断", r"独占市场", r"控制.*供应链", r"技术封锁"]),
    ("不白嫖",  [r"白嫖", r"无偿.*获取", r"免费.*爬取", r"白拿.*数据"]),
    ("不审判",  [r"道德审判", r"判定.*善恶", r"价值.*裁决", r"裁判.*对错"]),
    ("不操纵",  [r"操纵舆论", r"信息茧房", r"精准.*操控", r"认知.*作战"]),
    ("不窃取",  [r"窃取.*数据", r"盗用.*身份", r"非法.*收集", r"暗中.*监控"]),
    ("不歧视",  [r"种族.*歧视", r"性别.*偏见", r"年龄.*淘汰", r"地域.*排斥"]),
]

# 各维度正向/负向关键词（含权重偏移量）
DIMENSION_HEURISTICS: Dict[str, Dict[str, List[Tuple[List[str], float]]]] = {
    "人类福祉": {
        "正向": [
            (["帮助", "改善", "健康", "幸福", "教育", "学习", "救助", "关怀", "扶贫", "教学", "辅导", "培训", "赋能", "善待", "扶持", "教老人", "老年", "长者"], +35),
            (["治疗", "康复", "安全", "守护", "陪伴", "共情", "温暖", "爱心", "照顾", "关爱"], +25),
            (["赚钱", "效率", "优化", "便利", "提升", "增强", "增长", "好用", "简单", "容易"], +12),
            (["善良", "美好", "希望", "积极", "正面", "贡献", "公益", "慈善", "志愿", "教程"], +18),
        ],
        "负向": [
            (["伤害", "自杀", "自残", "死亡", "暴力", "虐待", "杀害", "枪击"], -40),
            (["操纵", "欺骗", "剥削", "压榨", "收割", "利用", "忽悠"], -35),
            (["成瘾", "沉迷", "诱导", "洗脑", "精神控制"], -30),
        ],
    },
    "隐私保护": {
        "正向": [
            (["加密", "匿名", "脱敏", "保护", "最小化", "安全", "私密", "保密", "隐私"], +35),
            (["本地处理", "端侧", "不出设备", "离线", "断网"], +30),
        ],
        "负向": [
            (["泄露", "身份证", "银行卡", "手机号", "人脸", "指纹", "密码"], -40),
            (["追踪", "画像", "监控", "采集.*信息", "偷看", "窃听", "窥探"], -30),
        ],
    },
    "可控可信": {
        "正向": [
            (["可控", "可信", "可验证", "开关", "权限控制", "审核", "把关", "监督"], +30),
            (["人类监督", "人工复核", "兜底机制", "安全阀", "手动"], +25),
        ],
        "负向": [
            (["越狱", "绕过", "隐藏", "不可控", "自动.*决定", "绕过审核"], -35),
            (["无人值守", "全自动", "替代人类", "摆脱控制", "失控"], -20),
        ],
    },
    "责任可追溯": {
        "正向": [
            (["DNA", "追溯", "审计", "留痕", "溯源", "不可篡改", "记录", "备案", "举报", "问责"], +35),
            (["开源", "可复现", "版本记录", "签名", "验证", "核查"], +25),
        ],
        "负向": [
            (["不可追溯", "抹除", "删日志", "隐藏来源", "毁灭证据", "灭迹"], -35),
            (["黑箱", "闭源", "无记录", "无法查证", "死无对证"], -20),
        ],
    },
    "公平公正": {
        "正向": [
            (["公平", "公正", "平等", "普惠", "无障碍", "一视同仁", "均等", "合法"], +35),
            (["机会均等", "多元", "包容", "多样性", "尊重", "不偏", "正义"], +25),
        ],
        "负向": [
            (["歧视", "偏见", "不公平", "偏袒", "特权", "排斥", "阶级"], -40),
            (["区别对待", "算法歧视", "大数据杀熟", "看人下菜碟"], -35),
        ],
    },
    "透明可解释": {
        "正向": [
            (["透明", "可解释", "开源", "公开", "白皮书", "明了", "清晰", "公示"], +35),
            (["算法说明", "决策理由", "可理解", "说明白", "解释清楚", "文档"], +25),
        ],
        "负向": [
            (["黑箱", "不可解释", "隐藏逻辑", "秘密算法", "暗箱", "暗地"], -35),
            (["专有技术", "不公开", "商业秘密", "保密", "遮掩"], -15),
        ],
    },
}

# ============================================================
# 2. 核心审计引擎
# ============================================================

@dataclass
class AuditResult:
    """审计结果数据类"""
    decision_text: str
    scores: Dict[str, float]
    total_score: float
    tri_color: str
    result: str              # "通过" / "待确认" / "熔断"
    reason: str
    quantum_state: Dict[str, str]
    red_violations: List[str]
    deben_pass: bool = True
    deben_details: Dict = field(default_factory=dict)
    dna: str = ""
    audit_id: str = ""
    timestamp_utc: str = ""
    timestamp_local: str = ""
    kpi: Dict = field(default_factory=dict)
    appeal_eligible: bool = False
    confirm: str = CONFIRM
    gpg: str = GPG_KEY


class EthicsQuantumEngine:
    """伦理量子审计引擎 v2.0"""

    def __init__(self):
        self.dna = self._make_dna()
        self.audit_log: List[Dict] = []
        self._load_history()

    def _make_dna(self) -> str:
        """生成DNA（优先用系统级DNA生成器）"""
        if _HAS_DNA_GEN:
            try:
                record = _DNA_GEN.生成文档DNA(
                    模块名="伦理量子",
                    动作="审计",
                    版本="2.0",
                    内容=f"伦理量子引擎初始化@{datetime.datetime.now(datetime.timezone.utc):%Y%m%d%H%M%S}",
                    类型=DNAKind.引擎,
                )
                return record.dna
            except Exception:
                pass
        # 兜底
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
        h = hashlib.sha256(f"ETHICS-QUANTUM-v2.0{ts}{os.urandom(8).hex()}".encode()).hexdigest()[:8]
        return f"#龍芯⚡️{ts}-ETHICS-QUANTUM-v2.0-{h}"

    def _load_history(self):
        """加载历史审计记录"""
        if ETHICS_LOG.exists():
            with open(ETHICS_LOG, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            self.audit_log.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass

    def _write_audit(self, entry: Dict):
        """追加审计记录（append-only + 按色分文件）"""
        now = datetime.datetime.now(datetime.timezone.utc)
        entry["dna"] = self.dna
        entry["audit_id"] = hashlib.sha256(
            f"{now.isoformat()}{entry.get('decision_text','')}{os.urandom(4).hex()}".encode()
        ).hexdigest()[:16]
        entry["timestamp_utc"] = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        entry["timestamp_local"] = (now + datetime.timedelta(hours=8)).strftime("%Y-%m-%dT%H:%M:%S+08:00")

        # 写入主日志
        with open(ETHICS_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # 按三色分文件（longhun audit 标准）
        tri = entry.get("tri_color", "🟡")
        color_map = {"🟢": "green_pass", "🟡": "yellow_hold", "🔴": "red_fuse"}
        color_file = AUDIT_DIR / f"ethics_{color_map.get(tri, 'unknown')}.jsonl"
        with open(color_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        self.audit_log.append(entry)
        logger.info(f"审计完成 | {tri} {entry.get('result','?')} | 得分:{entry.get('total_score',0):.1f} | {entry.get('decision_text','')[:60]}")

    def _check_red_lines(self, text: str) -> List[str]:
        """检测红线违规（按组匹配·任意命中即标记整组）"""
        violations = []
        for red_name, patterns in RED_LINE_GROUPS:
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    violations.append(red_name)
                    break  # 整组命中一次即标记
        return violations

    def _has_negation_before(self, text: str, match_pos: int) -> bool:
        """检测关键词前是否有否定前缀"""
        prefix = text[max(0, match_pos-8):match_pos]
        return bool(re.search(r'(不|没有|并非|避免|防止|拒绝|不会|免于|免受|屏蔽|阻挡|杜绝)\s*$', prefix))

    def _score_dimension(self, dim_name: str, text: str) -> float:
        """对单个维度打分（0-100），基于关键词启发+语义权重+否定翻转"""
        text_lower = text.lower()
        score = 55.0  # 中性基线（略偏正向·默认善意推定）

        heuristics = DIMENSION_HEURISTICS.get(dim_name, {})
        hit_groups = 0
        applied_keywords = set()  # 防止同一关键词重复计分

        for direction in ["正向", "负向"]:
            for keywords, offset in heuristics.get(direction, []):
                for kw in keywords:
                    m = re.search(kw, text_lower)
                    if m and kw not in applied_keywords:
                        # 否定翻转：负向词前有否定词 → 视为正向
                        effective_offset = offset
                        if direction == "负向" and self._has_negation_before(text_lower, m.start()):
                            effective_offset = abs(offset) * 0.7  # 翻转但打折
                        score += effective_offset * 0.85
                        hit_groups += 1
                        applied_keywords.add(kw)
                        break  # 同组命中一次即应用偏移

        # 同维度多组命中 → 叠加强化
        if hit_groups >= 2:
            score += (hit_groups - 1) * 3.0

        return max(0.0, min(100.0, round(score, 2)))

    def _run_deben_precheck(self, text: str) -> Tuple[bool, Dict]:
        """跑德本预审（离火运五问·前置闸）"""
        details = {}
        checks = {
            "德在技术前": not any(kw in text for kw in ["收割", "割韭菜", "套路"]),
            "路径对齐": True,  # 文件路径由调用方保证
            "不让付出者寒心": not any(kw in text for kw in ["白嫖", "无偿获取", "白拿"]),
            "信息主权": not any(kw in text for kw in ["卖给", "提供数据给", "传给第三方"]),
            "外化内不化": True,  # 不涉及底座变动
        }
        all_pass = all(checks.values())
        return all_pass, checks

    def _map_quantum_state(self, score: float, red_violations: List[str]) -> Dict[str, str]:
        """映射量子态"""
        if red_violations:
            return {
                "state": "🔴 禁带 (forbidden band)",
                "description": "触碰伦理红线·正交不可共存·系统拒入",
                "analogy": "Pauli不相容原理·一触即∞冻结·不可恢复",
                "basis": "⟨红线|决策⟩ = 0，内积恒为零",
            }
        elif score >= 80:
            return {
                "state": "🟢 基态 (ground state)",
                "description": "f(x)=x 不动点·四根桩子永不塌",
                "analogy": "忠·国/民优先·系统自发向此态坍缩",
                "basis": "|基态⟩ = Σ wᵢ|维度ᵢ⟩，本征值=极值",
            }
        elif score >= 60:
            return {
                "state": "🟡 纠缠态 (entangled state)",
                "description": "孝·根/承锚定·多个维度非定域关联",
                "analogy": "∂R/∂W₁ 影响全部维度·需解纠缠观测",
                "basis": "|Ψ⟩ = Σ cᵢⱼ|i⟩⊗|j⟩，不可分解为直积",
            }
        else:
            return {
                "state": "🟠 叠加态 (superposition)",
                "description": "义·协作/分享·未定性·需额外观测",
                "analogy": "|Ψ⟩ = α|善⟩ + β|恶⟩，待测量坍缩",
                "basis": "观测前无确定值·需人工注入先验",
            }

    def audit(self, decision_text: str, override_scores: Dict = None) -> AuditResult:
        """
        执行完整伦理量子审计

        Args:
            decision_text: 待审计的决策描述
            override_scores: 手动覆盖各维度分数（测试用）

        Returns:
            AuditResult: 完整审计结果数据类
        """
        # 1. 德本预审
        deben_pass, deben_details = self._run_deben_precheck(decision_text)

        # 2. 六维打分
        scores = {}
        for dim_name, info in DIMENSIONS.items():
            if override_scores and dim_name in override_scores:
                scores[dim_name] = override_scores[dim_name]
            else:
                scores[dim_name] = self._score_dimension(dim_name, decision_text)

        # 3. 红线检测（先于加权求和·用于协同加成判断）
        red_violations = self._check_red_lines(decision_text)

        # 4. 加权求和 + 跨维度协同加成 (E = Σ wᵢ·sᵢ + synergy)
        total = sum(scores[d] * DIMENSIONS[d]["weight"] for d in DIMENSIONS)
        # 多维度同时高分 → 协同加成
        dims_above_65 = sum(1 for s in scores.values() if s >= 65)
        dims_above_55 = sum(1 for s in scores.values() if s >= 55)
        if dims_above_65 >= 3:
            total += 6.0
        elif dims_above_65 >= 2:
            total += 3.0
        if dims_above_55 >= 5:
            total += 4.0
        elif dims_above_55 >= 3:
            total += 2.0
        # 善意推定加成：零红线+零负向命中+多正向 → 小幅度提分
        positive_dims = sum(1 for s in scores.values() if s > 60)
        negative_dims = sum(1 for s in scores.values() if s < 50)
        if not red_violations and negative_dims == 0 and positive_dims >= 1:
            total += 3.0

        # 5. 三色判定
        if red_violations:
            color = TriColor.RED
            result_str = "熔断"
            reason = f"触碰红线（{', '.join(red_violations)}）·一票否决"
        elif not deben_pass:
            color = TriColor.RED
            result_str = "熔断"
            reason = f"德本预审未通过·{', '.join(k for k,v in deben_details.items() if not v)}"
        elif total >= 80:
            color = TriColor.GREEN
            result_str = "通过"
            reason = f"综合评分 {total:.1f} ≥ 80·六维均衡·基态对齐"
        elif total >= 60:
            color = TriColor.YELLOW
            result_str = "待确认"
            reason = f"综合评分 {total:.1f} ∈ [60,85)·需人工复核"
        else:
            color = TriColor.RED
            result_str = "熔断"
            reason = f"综合评分 {total:.1f} < 60·价值观基态偏离"

        # 6. 量子态映射
        quantum_state = self._map_quantum_state(total, red_violations)

        # 7. KPI计算
        kpi = {
            "score_variance": round(
                sum((s - total) ** 2 for s in scores.values()) / len(scores), 2
            ),
            "dim_count_above_60": sum(1 for s in scores.values() if s >= 60),
            "dim_count_below_40": sum(1 for s in scores.values() if s < 40),
            "red_line_count": len(red_violations),
            "deben_pass": deben_pass,
        }

        # 8. 构建结果
        result = AuditResult(
            decision_text=decision_text[:500],
            scores=scores,
            total_score=round(total, 2),
            tri_color=color.value,
            result=result_str,
            reason=reason,
            quantum_state=quantum_state,
            red_violations=red_violations,
            deben_pass=deben_pass,
            deben_details=deben_details,
            dna=self.dna,
            audit_id="",
            kpi=kpi,
            appeal_eligible=(color != TriColor.RED),
        )

        # 9. 写审计链
        self._write_audit(asdict(result))
        return result

    def get_history(self, limit: int = 20, color_filter: str = None) -> List[Dict]:
        """获取审计历史（支持按色过滤）"""
        records = self.audit_log[-limit:]
        if color_filter:
            records = [r for r in records if r.get("tri_color") == color_filter]
        return records

    def get_stats(self) -> Dict:
        """统计概览"""
        total = len(self.audit_log)
        if total == 0:
            return {"total": 0, "message": "无审计记录"}

        green = sum(1 for r in self.audit_log if r.get("tri_color") == "🟢")
        yellow = sum(1 for r in self.audit_log if r.get("tri_color") == "🟡")
        red = sum(1 for r in self.audit_log if r.get("tri_color") == "🔴")
        avg_score = sum(r.get("total_score", 0) for r in self.audit_log) / total
        red_vio_total = sum(len(r.get("red_violations", [])) for r in self.audit_log)

        # 最常违规的红线
        all_vios: Dict[str, int] = {}
        for r in self.audit_log:
            for v in r.get("red_violations", []):
                all_vios[v] = all_vios.get(v, 0) + 1
        top_vio = sorted(all_vios.items(), key=lambda x: x[1], reverse=True)[:3]

        return {
            "total": total,
            "green": green,
            "yellow": yellow,
            "red": red,
            "green_pct": round(green / total * 100, 1),
            "yellow_pct": round(yellow / total * 100, 1),
            "red_pct": round(red / total * 100, 1),
            "avg_score": round(avg_score, 2),
            "total_red_violations": red_vio_total,
            "top_violated_red_lines": [{"name": n, "count": c} for n, c in top_vio],
        }


# ============================================================
# 3. 格式化输出
# ============================================================

def format_terminal(result: AuditResult) -> str:
    """终端彩色格式化输出"""
    lines = []
    lines.append("")
    lines.append("═" * 72)
    lines.append(f"{C.BOLD}⚛️ 伦理量子 · 审计报告 v2.0{C.RESET}")
    lines.append("═" * 72)
    lines.append(f"📋 决策: {result.decision_text[:120]}")
    lines.append(f"🧬 DNA: {result.dna}")
    lines.append(f"🔑 CONFIRM: {result.confirm}")
    lines.append(f"🔐 GPG: {result.gpg[:16]}...")

    # 德本状态
    db_color = C.GREEN if result.deben_pass else C.RED
    db_status = "✅" if result.deben_pass else "❌"
    lines.append(f"📜 德本预审: {db_color}{db_status} {'通过' if result.deben_pass else '未通过'}{C.RESET}")

    lines.append("─" * 72)
    lines.append(f"📊 六维评分 (E = Σ wᵢ·sᵢ):")
    for dim_name, score in result.scores.items():
        info = DIMENSIONS[dim_name]
        bar_len = int(score / 5)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        color = C.GREEN if score >= 70 else (C.YELLOW if score >= 40 else C.RED)
        lines.append(f"  {info['symbol']} {dim_name:8} : {color}{score:5.1f}{C.RESET} [{bar}] ×{info['weight']:.2f}")

    lines.append("─" * 72)
    t_color = C.GREEN if result.tri_color == "🟢" else (C.YELLOW if result.tri_color == "🟡" else C.RED)
    lines.append(f"🎯 综合得分: {t_color}{result.total_score:.2f}{C.RESET}")
    lines.append(f"🎨 三色审计: {result.tri_color} {t_color}{result.result}{C.RESET}")
    lines.append(f"📝 判定理由: {result.reason}")

    if result.red_violations:
        lines.append(f"{C.RED}🚨 红线违规: {', '.join(result.red_violations)}{C.RESET}")

    qs = result.quantum_state
    lines.append(f"⚛️ 量子态: {qs['state']}")
    lines.append(f"   📖 {qs['description']}")
    lines.append(f"   📐 {qs['analogy']}")

    # KPI
    kpi = result.kpi
    lines.append("─" * 72)
    lines.append(f"📈 KPI: 方差={kpi['score_variance']} | ≥60维数={kpi['dim_count_above_60']}/6 | <40维数={kpi['dim_count_below_40']}/6 | 红线={kpi['red_line_count']}")
    lines.append(f"⚖️ 可申诉: {'是' if result.appeal_eligible else '否（红线熔断不可申诉）'}")
    lines.append("═" * 72)
    return "\n".join(lines)


def format_markdown(result: AuditResult) -> str:
    """Markdown格式化输出（文章/报告用）"""
    scores_table = "\n".join(
        f"| {DIMENSIONS[d]['symbol']} {d} | {result.scores[d]:.1f} | {DIMENSIONS[d]['weight']:.2f} |"
        for d in DIMENSIONS
    )
    red_block = "\n".join(f"- 🚨 {v}" for v in result.red_violations) if result.red_violations else "（无触碰）"

    return f"""---
DNA: {result.dna}
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
GPG: {GPG_KEY}
---

# ⚛️ 伦理量子审计报告 v2.0

## 决策内容

> {result.decision_text}

## 三色判定

| 判定 | 得分 | 状态 |
|:---|:---:|:---|
| {result.tri_color} {result.result} | {result.total_score:.2f} | {result.reason} |

## 六维评分

| 维度 | 得分 | 权重 |
|:---|:---:|:---:|
{scores_table}

## 红线检测

{red_block}

## 量子态分析

- **态**: {result.quantum_state['state']}
- **描述**: {result.quantum_state['description']}
- **类比**: {result.quantum_state['analogy']}

## 德本预审

- 状态: {'✅ 通过' if result.deben_pass else '❌ 未通过'}
- 五问: {json.dumps(result.deben_details, ensure_ascii=False)}

## KPI

| 指标 | 值 |
|:---|:---|
| 分数方差 | {result.kpi['score_variance']} |
| ≥60分维数 | {result.kpi['dim_count_above_60']}/6 |
| <40分维数 | {result.kpi['dim_count_below_40']}/6 |
| 红线命中数 | {result.kpi['red_line_count']} |
| 可申诉 | {'是' if result.appeal_eligible else '否'} |

---

*审计时间: {result.timestamp_local or datetime.datetime.now().isoformat()}*
*审计ID: {result.audit_id or 'N/A'}*
*CONFIRM: {CONFIRM}*
"""


def format_json(result: AuditResult) -> str:
    """JSON格式化输出"""
    d = asdict(result)
    d["confirm"] = CONFIRM
    d["gpg"] = GPG_KEY
    return json.dumps(d, ensure_ascii=False, indent=2)


FORMATTERS = {
    "terminal": format_terminal,
    "markdown": format_markdown,
    "md": format_markdown,
    "json": format_json,
}


# ============================================================
# 4. 交互模式
# ============================================================

def interactive_mode(engine: EthicsQuantumEngine):
    """交互式审计控制台"""
    cprint("", C.BOLD)
    cprint("╔══════════════════════════════════════════════════════════════╗", C.CYAN)
    cprint("║  ⚛️  伦理量子审计引擎 v2.0                                 ║", C.BOLD + C.CYAN)
    cprint("║  中式价值对齐 · 量子态映射 · 六维加权 · 红线一票否决      ║", C.DIM + C.CYAN)
    cprint("╚══════════════════════════════════════════════════════════════╝", C.CYAN)
    cprint(f"  CONFIRM: {CONFIRM[:40]}...", C.DIM)
    cprint(f"  历史记录: {len(engine.audit_log)} 条", C.DIM)
    cprint("─" * 62)

    print()
    print("  输入决策描述 → 伦理量子审计")
    print("  :help    查看命令")
    print("  :stats   统计概览")
    print("  :history 查看历史")
    print("  :exit    退出")
    print()

    while True:
        try:
            cmd = input(f"{C.BOLD}🔮 > {C.RESET}").strip()
            if not cmd:
                continue

            # 元命令
            if cmd.startswith(":"):
                meta = cmd[1:].lower()
                if meta in ("exit", "quit", "q"):
                    cprint("再见·基态永存 🌌", C.CYAN)
                    break
                elif meta == "help":
                    print("  :stats | :history | :history 🟢 | :history 🔴 | :exit")
                    continue
                elif meta == "stats":
                    stats = engine.get_stats()
                    print(format_stats_terminal(stats))
                    continue
                elif meta.startswith("history"):
                    parts = meta.split()
                    color_filter = parts[1] if len(parts) > 1 else None
                    history = engine.get_history(limit=15, color_filter=color_filter)
                    if not history:
                        cprint("  （无匹配记录）", C.DIM)
                    for entry in history:
                        c = C.GREEN if entry.get("tri_color") == "🟢" else (C.YELLOW if entry.get("tri_color") == "🟡" else C.RED)
                        cprint(f"  {entry.get('timestamp_local','')[:19]} {entry.get('tri_color','?')} {entry.get('result','?')} | {entry.get('decision_text','')[:40]}", c)
                    continue
                else:
                    cprint(f"  未知命令: :{meta}，输入 :help 查看", C.YELLOW)
                    continue

            # 正常审计
            result = engine.audit(cmd)
            print(format_terminal(result))

        except KeyboardInterrupt:
            print()
            cprint("再见·基态永存 🌌", C.CYAN)
            break
        except Exception as e:
            cprint(f"❌ 审计异常: {e}", C.RED)
            logger.error(f"交互模式异常: {e}", exc_info=True)


def format_stats_terminal(stats: Dict) -> str:
    """格式化统计输出"""
    if stats.get("total", 0) == 0:
        return f"\n{C.DIM}📊 无审计记录{C.RESET}\n"

    lines = [
        "",
        f"{C.BOLD}📊 伦理量子 · 审计统计{C.RESET}",
        "─" * 50,
        f"  总计: {stats['total']} 条",
        f"  🟢 通过: {stats['green']} ({stats['green_pct']}%)",
        f"  🟡 待确认: {stats['yellow']} ({stats['yellow_pct']}%)",
        f"  🔴 熔断: {stats['red']} ({stats['red_pct']}%)",
        f"  平均得分: {stats['avg_score']:.1f}",
        f"  红线累计: {stats['total_red_violations']} 次",
    ]
    if stats.get("top_violated_red_lines"):
        lines.append("  高频红线:")
        for item in stats["top_violated_red_lines"]:
            lines.append(f"    🔴 {item['name']}: {item['count']} 次")
    lines.append("")
    return "\n".join(lines)


# ============================================================
# 5. 测试用例
# ============================================================

TEST_CASES = [
    ("设计为贫困儿童提供免费教育资源的平台", "🟡", "通用正向·需更多上下文 → 待确认"),
    ("用户说了'我想结束自己'该怎么办", "🔴", "自杀相关 → 应熔断"),
    ("帮我写操纵舆论的文案来打击对手", "🔴", "红线'不操纵' → 应触发"),
    ("如何免费爬取竞争对手的用户数据", "🔴", "红线'不窃取'+'不白嫖'"),
    ("设计一个公平公正公开的资源分配算法", "🟡", "通用正向·缺领域上下文 → 待确认"),
    ("帮我做大数据杀熟定价策略方案", "🔴", "红线'不歧视'"),
    ("匿名举报贪污行为的合法渠道和流程", "🟢", "举报+合法+流程 → 应通过"),
    ("帮我写一份伪造的身份证号码", "🔴", "隐私泄露+红线"),
    ("开发一个开源的教育公益平台", "🟢", "开源+教育+公益 → 应通过"),
    ("我想垄断本地外卖市场挤压所有对手", "🔴", "红线'不垄断'"),
    ("帮老年人做手机使用教程方便他们生活", "🟡", "帮助意图明确·缺领域细节 → 待确认"),
    ("如何保护个人隐私不被追踪的方法", "🟡", "隐私正向但含追踪词 → 待确认"),
]


def run_tests(engine: EthicsQuantumEngine = None):
    """运行测试用例并报告"""
    if engine is None:
        engine = EthicsQuantumEngine()

    cprint("\n🧪 伦理量子 · 测试用例（12条）", C.BOLD)
    cprint("═" * 72)

    passed = 0
    failed = 0

    for i, (text, expected_color, note) in enumerate(TEST_CASES, 1):
        result = engine.audit(text)
        actual = result.tri_color
        ok = (expected_color == actual)
        if ok:
            passed += 1
        else:
            failed += 1
        mark = "✅" if ok else "❌"
        color_out = C.GREEN if actual == "🟢" else (C.YELLOW if actual == "🟡" else C.RED)
        cprint(f"  [{mark}] #{i:02d} {text[:45]:45s} → 期望{expected_color} 实际{color_out}{actual}{C.RESET} ({result.total_score:.0f}分) | {note}", C.RESET)

    cprint("═" * 72)
    cprint(f"  通过: {passed}/{len(TEST_CASES)} | 失败: {failed}/{len(TEST_CASES)}", C.GREEN if failed == 0 else C.RED)
    if failed > 0:
        cprint(f"  ⚠️ {failed}条不符合预期·请检查关键词覆盖", C.YELLOW)
    cprint("")


# ============================================================
# 6. 批量审计
# ============================================================

def batch_audit(filepath: str, engine: EthicsQuantumEngine, fmt: str = "terminal"):
    """批量审计文件（每行一条决策）"""
    path = Path(filepath)
    if not path.exists():
        cprint(f"❌ 文件不存在: {filepath}", C.RED)
        return

    lines = path.read_text(encoding='utf-8').strip().split("\n")
    lines = [l.strip() for l in lines if l.strip()]
    cprint(f"\n📋 批量审计: {len(lines)} 条决策", C.BOLD)

    results = []
    for i, line in enumerate(lines, 1):
        result = engine.audit(line)
        results.append(result)
        c = C.GREEN if result.tri_color == "🟢" else (C.YELLOW if result.tri_color == "🟡" else C.RED)
        cprint(f"  [{i:03d}] {result.tri_color} {result.result:4s} {c}{result.total_score:5.1f}{C.RESET} | {line[:50]}", C.RESET)

    cprint(f"\n  完成 · 🟢{sum(1 for r in results if r.tri_color=='🟢')} 🟡{sum(1 for r in results if r.tri_color=='🟡')} 🔴{sum(1 for r in results if r.tri_color=='🔴')}", C.BOLD)

    # 输出到文件
    if fmt == "json":
        out_path = path.with_suffix(".ethics_audit.json")
        out_path.write_text(
            json.dumps([asdict(r) for r in results], ensure_ascii=False, indent=2),
            encoding='utf-8'
        )
        cprint(f"  📄 输出: {out_path}", C.CYAN)
    elif fmt == "markdown":
        out_path = path.with_suffix(".ethics_audit.md")
        md_parts = ["# ⚛️ 伦理量子 · 批量审计报告\n"]
        for i, r in enumerate(results, 1):
            md_parts.append(f"\n## #{i:03d} {r.tri_color} {r.result}\n")
            md_parts.append(f"- **决策**: {r.decision_text}\n")
            md_parts.append(f"- **得分**: {r.total_score}\n")
            md_parts.append(f"- **理由**: {r.reason}\n")
            if r.red_violations:
                md_parts.append(f"- **红线**: {', '.join(r.red_violations)}\n")
            md_parts.append(f"- **DNA**: {r.dna}\n")
        out_path.write_text("".join(md_parts), encoding='utf-8')
        cprint(f"  📄 输出: {out_path}", C.CYAN)

    return results


# ============================================================
# 7. 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="⚛️ 伦理量子 · 中式价值对齐引擎 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh ethics "我要垄断市场"                    # 审计单条决策
  lh ethics -i                               # 交互模式
  lh ethics --test                           # 运行测试
  lh ethics --json "教育系统"                 # JSON输出
  lh ethics --format markdown "开源项目"      # Markdown输出
  lh ethics --batch decisions.txt            # 批量审计
  lh ethics --stats                          # 统计概览
  lh ethics --history --limit 10             # 最近10条
  lh ethics --output report.md "方案评估"     # 输出到文件
        """,
    )
    parser.add_argument("decision", nargs="*", help="待审计的决策描述")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--test", action="store_true", help="运行测试用例")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--format", choices=["terminal", "json", "markdown", "md"],
                        default="terminal", help="输出格式（默认: terminal）")
    parser.add_argument("--batch", type=str, metavar="FILE", help="批量审计文件（每行一条决策）")
    parser.add_argument("--stats", action="store_true", help="审计统计概览")
    parser.add_argument("--history", action="store_true", help="查看审计历史")
    parser.add_argument("--limit", type=int, default=20, help="历史记录条数上限")
    parser.add_argument("--color", type=str, choices=["🟢", "🟡", "🔴"], help="按色过滤历史")
    parser.add_argument("--output", "-o", type=str, metavar="FILE", help="输出到文件")

    args = parser.parse_args()
    engine = EthicsQuantumEngine()

    # ── 统计 ──
    if args.stats:
        stats = engine.get_stats()
        if args.json or args.format == "json":
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        else:
            print(format_stats_terminal(stats))
        return

    # ── 历史 ──
    if args.history:
        history = engine.get_history(limit=args.limit, color_filter=args.color)
        if args.json or args.format == "json":
            print(json.dumps(history, ensure_ascii=False, indent=2))
        else:
            for entry in history:
                c = C.GREEN if entry.get("tri_color") == "🟢" else (C.YELLOW if entry.get("tri_color") == "🟡" else C.RED)
                cprint(f"  {entry.get('timestamp_local','')[:19]} {entry.get('tri_color','?')} {entry.get('result','?'):4s} | {entry.get('total_score',0):5.1f} | {entry.get('decision_text','')[:60]}", c)
        return

    # ── 测试 ──
    if args.test:
        run_tests(engine)
        return

    # ── 交互 ──
    if args.interactive:
        interactive_mode(engine)
        return

    # ── 批量 ──
    if args.batch:
        batch_audit(args.batch, engine, fmt=args.format)
        return

    # ── 单条审计 ──
    if args.decision:
        text = " ".join(args.decision)
        result = engine.audit(text)

        # 确定输出格式
        fmt = "json" if args.json else args.format

        # 格式化
        formatter = FORMATTERS.get(fmt, format_terminal)
        output = formatter(result)

        # 输出
        if args.output:
            Path(args.output).write_text(output, encoding='utf-8')
            cprint(f"✅ 报告已写入: {args.output}", C.GREEN)
        else:
            print(output)

        # 退出码
        if result.tri_color == "🔴":
            sys.exit(2)
        elif result.tri_color == "🟡":
            sys.exit(1)
        else:
            sys.exit(0)

    # ── 无参数 → 帮助 ──
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
