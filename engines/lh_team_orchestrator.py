#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · TeamOrchestrator 军团指挥中枢 v2.0
DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-TEAM-ORCHESTRATOR-v2.0-军团指挥
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

v2.0 从单兵到军团：
  任务拆解器 → 军阵模式(5种) → 冲突检测/裁决 → 战后复盘 → 安全层一票否决

焊死规矩：
  1. 所有AI协作必须走总线，绕过总线的私自通信视为恶意
  2. 协作审计必须上链，决策过程不可篡改
  3. 最终决策权归老大，任何输出只是建议
  4. 安全层(P77/P72/P05)拥有一票否决权
"""

import hashlib, json, sys, threading, time, uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass, field, asdict
from enum import Enum
SYSTEM_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SYSTEM_ROOT))

from engines.lh_inter_agent_bus import get_bus
from engines.lh_persona_runner import get_runner
from engines.lh_shared_blackboard import SharedBlackboard, EntryType, Visibility

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 五层职能矩阵（焊死在引擎里）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FIVE_TIER_MATRIX = {
    "战略层": {"priority": 1, "personas": ["P00", "P01"], "desc": "意图解析·推演决策", "veto": False},
    "执行层": {"priority": 2, "personas": ["P02", "P03", "P04", "P07", "P14"], "desc": "落地执行", "veto": False},
    "文化层": {"priority": 3, "personas": ["P08", "P09", "P10", "P11", "P12"], "desc": "文化守卫", "veto": False},
    "守护层": {"priority": 4, "personas": ["P05", "P06", "P13", "P15", "P72"], "desc": "审计守护", "veto": False},
    "安全层": {"priority": 5, "personas": ["P72", "P77", "P05"], "desc": "安全·熔断·底线", "veto": True},  # ← 一票否决权
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 军阵模式（五种预设 + 可自定义注册）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FORMATION_MODES: Dict[str, Dict[str, Any]] = {
    "blitzkrieg": {
        "name": "闪电战",
        "icon": "⚡",
        "desc": "快速原型·最小链路·极速交付",
        "personas": {"P00": "意图解析", "P04": "代码工程", "P03": "归档"},
        "mode": "chain",
        "strategy": "串行·每一步不等待审计·最后统一过",
        "max_duration_seconds": 300,
    },
    "encirclement": {
        "name": "围猎",
        "icon": "🎯",
        "desc": "多视角审计·安全优先·全方位围剿",
        "personas": {"P05": "上帝之眼", "P77": "黑天使", "P07": "管仲", "P13": "姜子牙", "P12": "屈原"},
        "mode": "parallel_merge",
        "strategy": "并发出击→结果汇总→冲突裁决→最终报告",
        "max_duration_seconds": 600,
    },
    "fortification": {
        "name": "筑城",
        "icon": "🏰",
        "desc": "全链路搭建·从零到生产就绪",
        "personas": {"P01": "诸葛亮", "P04": "鲁班", "P05": "上帝之眼", "P14": "吕蒙", "P15": "乔前辈"},
        "mode": "chain",
        "strategy": "推演→开发→审计→部署→签章·一道不落",
        "max_duration_seconds": 900,
    },
    "minesweeping": {
        "name": "排雷",
        "icon": "💣",
        "desc": "安全扫描·漏洞排查·风险清零",
        "personas": {"P77": "黑天使(四编队)", "P05": "上帝之眼", "P06": "数学大师", "P12": "屈原"},
        "mode": "parallel_merge",
        "strategy": "四天使并行→漏洞汇总→安全建议→熔断评估",
        "max_duration_seconds": 1200,
    },
    "lecture": {
        "name": "讲武",
        "icon": "📚",
        "desc": "教学推演·知识传递·由浅入深",
        "personas": {"P02": "宝宝(温度)", "P08": "仓颉(术语)", "P11": "李白(类比)", "P01": "诸葛亮(推演)", "P05": "上帝之眼(审计)"},
        "mode": "chain",
        "strategy": "温度调节→术语桥接→创意类比→战略推演→审计抽检",
        "max_duration_seconds": 600,
    },
}

# 保留旧版模板兼容性
TEAM_TEMPLATES = {
    "audit": {"name": "审计链路", "chain": ["P05", "P06", "P13", "P15"], "desc": "审计→验证→授权→签章"},
    "dev": {"name": "开发链路", "chain": ["P00", "P01", "P04", "P03"], "desc": "意图→推演→实现→归档"},
    "deploy": {"name": "部署链路", "chain": ["P14", "P05", "P15", "P03"], "desc": "部署→审计→签章→归档"},
    "cultural": {"name": "文化协同", "members": ["P08", "P09", "P10", "P11", "P12"], "desc": "五维并行"},
    "quick": {"name": "快速三连", "chain": ["P05", "P06", "P04"], "desc": "审计→验证→修复"},
}

# 缩写→军阵名映射
FORMATION_ALIASES = {
    "闪电战": "blitzkrieg", "闪电": "blitzkrieg", "快速": "blitzkrieg",
    "围猎": "encirclement", "围剿": "encirclement", "猎杀": "encirclement", "审查": "encirclement",
    "筑城": "fortification", "搭建": "fortification", "全链路": "fortification",
    "排雷": "minesweeping", "扫雷": "minesweeping", "安全扫描": "minesweeping", "安全": "minesweeping",
    "讲武": "lecture", "教学": "lecture", "上课": "lecture", "讲解": "lecture",
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class RunStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    MELTED = "melted"


@dataclass
class SubTask:
    """子任务"""
    sid: str                      # 子任务ID
    persona: str                  # 执行人格
    objective: str                # 目标
    deliverable: str              # 交付物标准
    priority: int = 1             # 优先级 1-5 (5最高)
    tier: str = ""                # 所属层级
    result: Optional[Dict[str, Any]] = None # 执行结果
    start_time: Optional[str] = None
    end_time: Optional[str] = None


@dataclass
class ConflictRecord:
    """冲突记录"""
    conflict_id: str
    between: List[str]                      # 冲突的人格
    issue: str                              # 冲突点
    position_a: str                         # 立场A
    position_b: str                         # 立场B
    adjudication: str = ""                  # 裁决结果
    rationale: str = ""                     # 裁决理由
    resolution: str = ""                    # 最终方案
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AfterActionReport:
    """战后复盘报告"""
    task_id: str
    task: str
    formation: str
    persona_count: int
    contributions: list[dict[str, Any]] = field(default_factory=list)  # [{persona, contribution, score}]
    conflicts: list[ConflictRecord] = field(default_factory=list)
    adjudication_log: list[dict[str, Any]] = field(default_factory=list)
    final_verdict: str = ""
    dna: str = ""
    total_duration_ms: int = 0
    audit_color: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TeamRun:
    run_id: str
    team_name: str
    task: str
    chain: List[str]
    formation: str = ""
    subtasks: List[SubTask] = field(default_factory=list)
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: Optional[str] = None
    results: list[dict[str, Any]] = field(default_factory=list)
    blackboard_keys: List[str] = field(default_factory=list)
    audit: Dict[str, Any] = field(default_factory=dict)
    status: RunStatus = RunStatus.PENDING
    after_action: Optional[AfterActionReport] = None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 任务拆解器
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TaskDecomposer:
    """将老大一句话指令拆解为子任务·指定人格·优先级·交付物"""

    # 关键词→人格映射（基于五层职能矩阵）
    KEYWORD_PERSONA_MAP = {
        # 审计安全
        "审计": ["P05"], "检查": ["P05"], "审查": ["P05"], "scan": ["P05"],
        "安全": ["P77", "P05"], "漏洞": ["P77"], "渗透": ["P77"], "攻击": ["P77"],
        "熔断": ["P72"], "底线": ["P12"], "原则": ["P12"],
        # 计算数学
        "算": ["P06"], "数字": ["P06"], "权重": ["P06"], "五行": ["P06", "S2"],
        "洛书": ["S2"], "369": ["S2"], "卦": ["P06"],
        # 代码工程
        "写": ["P04"], "开发": ["P04"], "代码": ["P04"], "修复": ["P04"],
        "bug": ["P04"], "架构": ["P01", "P04"], "重构": ["P04"],
        # 部署
        "部署": ["P14"], "上线": ["P14"], "发布": ["P14"],
        # 经济
        "成本": ["P07"], "钱": ["P07"], "预算": ["P07"], "资源": ["P07"],
        "值不值": ["P01", "P07"], "ROI": ["P07"],
        # 命名文档
        "命名": ["P08"], "术语": ["P08"], "符号": ["P08"], "归档": ["P03"],
        "文档": ["P03"], "整理": ["P03"],
        # 文化创意
        "创意": ["P11"], "诗": ["P11"], "设计": ["P11"], "类比": ["P11"],
        "调解": ["P10"], "沟通": ["P10"],
        # 诊断
        "诊断": ["P09"], "健康": ["P09"], "体检": ["P09"],
        # 授权权限
        "授权": ["P13"], "权限": ["P13"], "注册": ["P13"],
        # 签章
        "签章": ["P15"], "盖章": ["P15"], "DNA": ["P15"],
        # 教学
        "教学": ["P02", "P08", "P11"], "教": ["P02", "P08", "P11"],
        "小白": ["P02", "P08", "P11"], "解释": ["P02", "P08"],
        # 法律维权
        "法律": ["S1"], "维权": ["S3"], "投诉": ["S3"],
        # 意图推演
        "推演": ["P01"], "预测": ["P01"], "评估": ["P01"], "分析": ["P01", "P05"],
        # 情感
        "情绪": ["P02"], "温度": ["P02"],
    }

    def decompose(self, task: str, formation: str = "") -> List[SubTask]:
        """拆解任务"""
        subtasks = []
        matched_personas: Set[str] = set()

        # Keyword match
        for keyword, personas in self.KEYWORD_PERSONA_MAP.items():
            if keyword in task:
                for p in personas:
                    if p not in matched_personas:
                        matched_personas.add(p)
                        tier = self._find_tier(p)
                        subtasks.append(SubTask(
                            sid=f"sub_{len(subtasks):03d}",
                            persona=p,
                            objective=f"执行与「{keyword}」相关的分析",
                            deliverable=f"{p}的专长输出",
                            priority=min(len(personas), 5),
                            tier=tier,
                        ))

        # 如果没匹配到任何关键词→默认拆分
        if not subtasks:
            subtasks = [
                SubTask(sid="sub_000", persona="P00", objective="解析意图",
                        deliverable="任务意图分析", priority=5, tier="战略层"),
                SubTask(sid="sub_001", persona="P01", objective="多路径推演",
                        deliverable="推演方案", priority=5, tier="战略层"),
                SubTask(sid="sub_002", persona="P05", objective="审计审查",
                        deliverable="审计报告", priority=4, tier="守护层"),
            ]
            matched_personas = {"P00", "P01", "P05"}

        # 总是加审计步骤（如果还没）
        if "P05" not in matched_personas:
            subtasks.append(SubTask(
                sid=f"sub_{len(subtasks):03d}", persona="P05",
                objective="审计所有子任务输出", deliverable="三色审计报告",
                priority=4, tier="守护层",
            ))

        # 按优先级降序
        subtasks.sort(key=lambda s: s.priority, reverse=True)
        return subtasks

    @staticmethod
    def _find_tier(persona: str) -> str:
        for tier_name, info in FIVE_TIER_MATRIX.items():
            if persona in info["personas"]:
                return tier_name
        return "执行层"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 冲突检测与裁决
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ConflictDetector:
    """检测并行人格输出中的矛盾·自动裁决

    裁决原则: 安全层 > 守护层 > 战略层 > 执行层 > 文化层
    """

    # 对立关键词对（A ↔ B 是矛盾）
    CONTRADICT_PAIRS = [
        (["通过", "安全", "无风险", "允许", "可以", "放行", "可行"],
         ["禁止", "拒绝", "高风险", "不允许", "危险", "报错", "不通过"]),
        (["需要重写", "推倒重来", "大规模重构", "重新设计"],
         ["小幅修改", "最小改动", "微调", "保持现状"]),
        (["成本过高", "预算不足", "不划算", "太贵"],
         ["值得投入", "性价比高", "划算", "不贵"]),
        (["部署", "上线", "发布"],
         ["暂缓", "延迟", "先不要", "停止"]),
    ]

    DANGER_KEYWORDS = ["漏洞", "泄露", "越权", "未授权", "明文", "裸奔",
                       "注入", "XSS", "SQL注入", "硬编码", "熔断"]

    def detect(self, results: list[dict[str, Any]]) -> list[ConflictRecord]:
        """检测所有结果中的冲突"""
        conflicts = []
        if len(results) < 2:
            return conflicts

        for i, r1 in enumerate(results):
            for j, r2 in enumerate(results):
                if j <= i:
                    continue
                conflict = self._check_pair(r1, r2)
                if conflict:
                    conflicts.append(conflict)

        return conflicts

    def _check_pair(self, r1: dict[str, Any], r2: dict[str, Any]) -> Optional[ConflictRecord]:
        """检查两个人格输出是否矛盾"""
        text1 = self._extract_text(r1).lower()
        text2 = self._extract_text(r2).lower()
        p1 = r1.get("persona", "?")
        p2 = r2.get("persona", "?")

        for pos_words, neg_words in self.CONTRADICT_PAIRS:
            a_pos = any(w in text1 for w in pos_words)
            b_neg = any(w in text2 for w in neg_words)
            b_pos = any(w in text2 for w in pos_words)
            a_neg = any(w in text1 for w in neg_words)

            if (a_pos and b_neg) or (b_pos and a_neg):
                issue = "结论相反"
                conflict = ConflictRecord(
                    conflict_id=f"cf_{hashlib.sha256(f'{p1}{p2}{text1[:50]}{text2[:50]}'.encode()).hexdigest()[:10]}",
                    between=[p1, p2],
                    issue=issue,
                    position_a=f"{p1}: {text1[:100]}",
                    position_b=f"{p2}: {text2[:100]}",
                )
                self._adjudicate(conflict)
                return conflict

        # 危险关键词检测
        has_danger_1 = any(kw in text1 for kw in self.DANGER_KEYWORDS)
        has_danger_2 = any(kw in text2 for kw in self.DANGER_KEYWORDS)
        if has_danger_1 and not has_danger_2:
            conflict = ConflictRecord(
                conflict_id=f"cf_danger_{p1}_{p2}_{int(time.time())}",
                between=[p1, p2],
                issue=f"{p1}发现安全隐患·{p2}未指出",
                position_a=f"{p1}: {text1[:100]}",
                position_b=f"{p2}: {text2[:100]}",
            )
            self._adjudicate(conflict)
            return conflict

        return None

    def _adjudicate(self, conflict: ConflictRecord):
        """自动裁决冲突

        规则：
        1. 安全层拥有一票否决权
        2. 守护层 > 战略层 > 执行层 > 文化层
        3. 危险关键词出现时→安全优先
        """
        p1, p2 = conflict.between
        tier1 = self._get_tier_priority(p1)
        tier2 = self._get_tier_priority(p2)

        # 检查安全层
        safety_personas = set(FIVE_TIER_MATRIX["安全层"]["personas"])
        p1_is_safety = p1 in safety_personas
        p2_is_safety = p2 in safety_personas

        if p1_is_safety and not p2_is_safety:
            conflict.adjudication = f"安全层({p1})一票否决·采纳{p1}立场"
            conflict.rationale = f"安全层({p1})拥有最高裁决权·非安全层({p2})的相反意见被覆盖"
            conflict.resolution = conflict.position_a
            return
        if p2_is_safety and not p1_is_safety:
            conflict.adjudication = f"安全层({p2})一票否决·采纳{p2}立场"
            conflict.rationale = f"安全层({p2})拥有最高裁决权·非安全层({p1})的相反意见被覆盖"
            conflict.resolution = conflict.position_b
            return

        # 优先级裁决
        if tier1 > tier2:
            winner = p1
        elif tier2 > tier1:
            winner = p2
        else:
            winner = p1 if "危险" in conflict.position_a or "漏洞" in conflict.position_a else p2

        conflict.adjudication = f"层级裁决: {winner}优先级更高·采纳其立场"
        conflict.rationale = f"p{tier1}={p1} vs p{tier2}={p2} → 高优先级者胜"
        conflict.resolution = conflict.position_a if winner == p1 else conflict.position_b

    @staticmethod
    def _get_tier_priority(persona: str) -> int:
        for _, info in FIVE_TIER_MATRIX.items():
            if persona in info["personas"]:
                return info["priority"]
        return 0

    @staticmethod
    def _extract_text(r: dict[str, Any]) -> str:
        result = r.get("result", "")
        if isinstance(result, dict):
            for k in ("output", "text", "content", "response"):
                if k in result:
                    return str(result[k])
            return json.dumps(result, ensure_ascii=False)
        return str(result)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 战后复盘引擎
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class AfterActionEngine:
    """每次协作结束自动生成复盘报告"""

    def generate(self, run: TeamRun) -> AfterActionReport:
        contributions = self._calc_contributions(run)
        conflicts = run.after_action.conflicts if run.after_action else []

        # 评分
        for c in contributions:
            c["score"] = self._score_contribution(c, run)

        # 按评分排序
        contributions.sort(key=lambda c: c["score"], reverse=True)

        dna = self._gen_dna(run)
        total_ms = int((datetime.fromisoformat(run.end_time) -
                        datetime.fromisoformat(run.start_time)).total_seconds() * 1000) if run.end_time else 0

        report = AfterActionReport(
            task_id=run.run_id,
            task=run.task,
            formation=run.formation or run.team_name,
            persona_count=len(run.chain or []),
            contributions=contributions,
            conflicts=conflicts,
            adjudication_log=[{
                "conflict_id": c.conflict_id,
                "between": c.between,
                "adjudication": c.adjudication,
                "resolution": c.resolution[:100] if c.resolution else "",
            } for c in conflicts],
            final_verdict=self._summarize(run),
            dna=dna,
            total_duration_ms=total_ms,
            audit_color=run.audit.get("status", "🟡"),
        )

        return report

    def _calc_contributions(self, run: TeamRun) -> list[dict[str, Any]]:
        contributions = []
        for r in run.results:
            pid = r.get("persona", "?")
            status = r.get("status", "unknown")
            contributions.append({
                "persona": pid,
                "status": status,
                "output_sample": str(r.get("result", ""))[:150],
                "score": 0.0,
            })
        return contributions

    def _score_contribution(self, contrib: dict[str, Any], run: TeamRun) -> float:
        score = 5.0  # 基础分
        if contrib["status"] == "ok":
            score += 2.0

        # 守护/安全层加权
        if contrib["persona"] in FIVE_TIER_MATRIX["安全层"]["personas"]:
            score += 1.5
        elif contrib["persona"] in FIVE_TIER_MATRIX["守护层"]["personas"]:
            score += 1.0
        elif contrib["persona"] in FIVE_TIER_MATRIX["战略层"]["personas"]:
            score += 0.5

        # 输出长度（有实质内容）
        sample = contrib.get("output_sample", "")
        if len(sample) > 100:
            score += 1.0
        elif len(sample) < 20:
            score -= 1.0

        return round(score, 1)

    def _summarize(self, run: TeamRun) -> str:
        err = run.audit.get("error", 0)
        total = run.audit.get("total", 0)
        if err == 0:
            return f"✅ 全部通过 · {total}个人格一致 · 无冲突 · 可交付"
        elif err <= total * 0.3:
            return f"🟡 {err}/{total}异常 · 需人工关注 · 建议签章前复查"
        else:
            return f"🔴 {err}/{total}严重异常 · 建议暂停 · 等待老大裁定"

    @staticmethod
    def _gen_dna(run: TeamRun) -> str:
        now = datetime.now(timezone.utc)
        tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
        dizhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
        gz = f"{tiangan[now.year%10]}{dizhi[now.month%12]}·{tiangan[(now.day+9)%10]}{dizhi[(now.day+1)%12]}"
        return f"#龍芯⚡️{gz}-TEAM-AFTER_ACTION-{run.run_id[:8]}"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TeamOrchestrator v2.0 核心
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class TeamOrchestrator:
    """龍魂军团指挥中枢 — 21人格协同作战总控"""

    def __init__(self):
        self._bus = get_bus()
        self._runner = get_runner()
        self._blackboard = SharedBlackboard()
        self._history: List[TeamRun] = []
        self._active_runs: Dict[str, TeamRun] = {}
        self._decomposer = TaskDecomposer()
        self._conflict_detector = ConflictDetector()
        self._after_action = AfterActionEngine()
        self._bootstrap = None
        self._formations: dict[str, dict[str, Any]] = dict(FORMATION_MODES)
        self._lock = threading.Lock()

        if not self._runner.is_booted:
            self._runner.boot()

    # ── 自举集成 ──

    def _get_bootstrap(self):
        if self._bootstrap is None:
            from engines.lh_symbiotic_bootstrap_engine import SymbioticBootstrapEngine
            self._bootstrap = SymbioticBootstrapEngine()
        return self._bootstrap

    def enable_bootstrap(self):
        """开启数据自举·每次协作自动造血"""
        self._get_bootstrap().capture.enable()

    def disable_bootstrap(self):
        """暂停数据自举"""
        self._get_bootstrap().capture.disable()

    @property
    def bootstrap_active(self) -> bool:
        if self._bootstrap is None:
            return True  # 默认开启（懒加载后即开启）
        return self._bootstrap.capture.enabled

    # ── 任务执行（入口） ──

    def run_team(self, team_name: str, task: str, **kw: Any) -> TeamRun:
        """执行团队协作——兼容旧版模板 + 新版军阵

        Args:
            team_name: 旧版模板名(audit/dev/deploy/cultural/quick) 或 军阵名(blitzkrieg等)
            task: 任务描述
            auto_decompose: 是否自动拆解任务（默认True）
            dry_run: 只拆解不执行（默认False）
        """
        auto_decompose = kw.pop("auto_decompose", True)
        dry_run = kw.pop("dry_run", False)

        # 检查是否为军阵模式
        formation = self._resolve_formation(team_name)

        if formation and auto_decompose:
            # 军阵模式：任务拆解 + 军阵调度
            return self._execute_formation(formation, task, dry_run=dry_run, **kw)

        # 旧版模板模式（向后兼容）
        tmpl = TEAM_TEMPLATES.get(team_name)
        if not tmpl:
            available = list(TEAM_TEMPLATES) + list(self._formations)
            raise ValueError(f"未知团队/军阵: {team_name}。可用: {available}")

        chain = tmpl.get("chain", [])
        members = tmpl.get("members", [])

        run = TeamRun(
            run_id=self._gen_run_id(team_name, task),
            team_name=team_name,
            task=task,
            chain=chain or members,
            formation=team_name,
            status=RunStatus.RUNNING,
        )

        if dry_run:
            run.status = RunStatus.PENDING
            return run

        return self._execute_run(run, chain, members, task, **kw)

    def execute(self, task: str, formation: str = "encirclement", **kw: Any) -> TeamRun:
        """执行一次团队协作（新入口）

        Args:
            task: 任务描述
            formation: 军阵模式名/别名
        """
        formation_key = self._resolve_formation(formation)
        if not formation_key:
            available = list(FORMATION_ALIASES.keys())
            raise ValueError(f"未知军阵: {formation}。可用: {available}")
        return self.run_team(formation_key, task, **kw)

    def _resolve_formation(self, name: str) -> Optional[str]:
        """解析军阵名→标准化键名"""
        name_lower = name.lower().strip()
        # 直接匹配
        if name_lower in self._formations:
            return name_lower
        # 别名匹配
        return FORMATION_ALIASES.get(name_lower, FORMATION_ALIASES.get(name.strip()))

    # ── 军阵执行 ──

    def _execute_formation(self, formation_key: str, task: str,
                           dry_run: bool = False, **kw: Any) -> TeamRun:
        """按军阵模式执行任务"""
        fm = self._formations[formation_key]
        personas = fm["personas"]
        mode = fm["mode"]
        strategy = fm.get("strategy", "")

        # 1. 任务拆解
        subtasks = self._decomposer.decompose(task, formation_key)

        # 确保军阵指定的人格参与
        for pid in personas:
            if pid not in [s.persona for s in subtasks]:
                tier_name = ""
                for t_name, t_info in FIVE_TIER_MATRIX.items():
                    if pid in t_info["personas"]:
                        tier_name = t_name
                        break
                subtasks.append(SubTask(
                    sid=f"sub_{len(subtasks):03d}",
                    persona=pid,
                    objective=f"从{pid}专长角度分析任务",
                    deliverable=f"{pid}的专业输出",
                    priority=3,
                    tier=tier_name,
                ))

        run_id = self._gen_run_id(formation_key, task)
        run = TeamRun(
            run_id=run_id,
            team_name=formation_key,
            formation=formation_key,
            task=task,
            chain=list(personas.keys()),
            subtasks=subtasks,
            status=RunStatus.RUNNING,
        )

        if dry_run:
            run.status = RunStatus.PENDING
            return run

        with self._lock:
            self._active_runs[run_id] = run

        # 2. 执行
        prefix = f"team:{run_id}"
        self._blackboard.announce(f"{prefix}:start",
                                  {"team": formation_key, "task": task, "formation": fm["name"],
                                   "strategy": strategy}, "orch", ttl=3600)
        run.blackboard_keys.append(f"{prefix}:start")

        chain_pids = list(personas.keys())

        if mode == "chain":
            rr = self._runner.dispatch_chain(chain_pids, task, **kw)
            if isinstance(rr, dict) and "results" in rr:
                for pid, r in rr["results"].items():
                    run.results.append({"persona": pid, "chain_step": True, **r})
                    self._blackboard.put(f"{prefix}:step:{pid}",
                                         {"pid": pid, "result": r}, pid, EntryType.DECISION, ttl=3600)

        elif mode == "parallel_merge":
            task_map = {p: task for p in chain_pids}
            rr = self._runner.dispatch_parallel(task_map, **kw)
            for pid, r in rr.items():
                run.results.append({"persona": pid, "parallel": True, **r})

        # 3. 冲突检测
        if mode in ("parallel_merge",) or len(run.results) >= 2:
            conflicts = self._conflict_detector.detect(run.results)

        else:
            conflicts = []

        run.end_time = datetime.now().isoformat()
        run.audit = self._audit(run)

        # 4. 战后复盘
        run.after_action = self._after_action.generate(run)

        self._blackboard.announce(f"{prefix}:done", run.audit, "orch", ttl=3600)

        with self._lock:
            self._history.append(run)
            self._active_runs.pop(run_id, None)

        # 5. 数据自举
        if self._bootstrap and self._bootstrap.capture.enabled:
            self._bootstrap.capture.capture_team_run(run, formation_key, domain=kw.get("domain", ""))
            if self._bootstrap.capture.pending_count() >= 10:
                self._bootstrap.pool.flush_capture(self._bootstrap.capture)

        run.status = RunStatus.COMPLETED
        return run

    # ── 旧版兼容 ──

    def _execute_run(self, run: TeamRun, chain: list[str], members: list[str],
                     task: str, **kw: Any) -> TeamRun:
        """旧版执行逻辑"""
        run.status = RunStatus.RUNNING
        prefix = f"team:{run.run_id}"
        self._blackboard.announce(f"{prefix}:start",
                                  {"team": run.team_name, "task": task}, "orch", ttl=3600)
        run.blackboard_keys.append(f"{prefix}:start")

        if chain:
            rr = self._runner.dispatch_chain(chain, task, **kw)
            if isinstance(rr, dict) and "results" in rr:
                for pid, r in rr["results"].items():
                    run.results.append({"persona": pid, "chain_step": True, **r})
                    self._blackboard.put(f"{prefix}:step:{pid}",
                                         {"pid": pid, "result": r}, pid, EntryType.DECISION, ttl=3600)

        if members:
            rr = self._runner.dispatch_parallel({p: task for p in members}, **kw)
            for pid, r in rr.items():
                run.results.append({"persona": pid, "parallel": True, **r})

        run.end_time = datetime.now().isoformat()
        run.audit = self._audit(run)
        self._blackboard.announce(f"{prefix}:done", run.audit, "orch", ttl=3600)

        with self._lock:
            self._history.append(run)

        if self._bootstrap and self._bootstrap.capture.enabled:
            self._bootstrap.capture.capture_team_run(run, run.team_name,
                                                     domain=kw.get("domain", ""))
            if self._bootstrap.capture.pending_count() >= 10:
                self._bootstrap.pool.flush_capture(self._bootstrap.capture)

        run.status = RunStatus.COMPLETED
        return run

    # ── 审计 ──

    def _audit(self, run: TeamRun) -> dict[str, Any]:
        ok = sum(1 for r in run.results if r.get("status") == "ok")
        err = len(run.results) - ok
        dur = 0
        if run.end_time:
            dur = int((datetime.fromisoformat(run.end_time) -
                       datetime.fromisoformat(run.start_time)).total_seconds() * 1000)
        return {
            "status": "🟢" if err == 0 else ("🟡" if err <= len(run.results) * 0.3 else "🔴"),
            "total": len(run.results), "ok": ok, "error": err, "duration_ms": dur,
        }

    # ── 跨团队协作 ──

    def cross_team(self, target: str, **kw: Any) -> dict[str, Any]:
        report = {"target": target, "steps": []}
        a = self.run_team("audit", f"审计:{target}", domain="系统审计")
        report["steps"].append({"step": "audit", "run_id": a.run_id, "audit": a.audit})
        if a.audit.get("error", 0) > 0:
            f = self.run_team("quick", f"修复:{target}", domain="系统审计")
            report["steps"].append({"step": "fix", "run_id": f.run_id, "audit": f.audit})
            v = self.run_team("audit", f"复审计:{target}", domain="系统审计")
            report["steps"].append({"step": "verify", "run_id": v.run_id, "audit": v.audit})
        report["final_status"] = report["steps"][-1]["audit"]["status"]
        if self._bootstrap and self._bootstrap.capture.enabled:
            self._bootstrap.capture.capture_cross_team(report, target)
        return report

    # ── 查询接口 ──

    def status_report(self) -> dict[str, Any]:
        return {
            "agents": self._runner.agent_count,
            "booted": self._runner.list_agents(),
            "teams": list(TEAM_TEMPLATES),
            "formations": list(self._formations),
            "formation_count": len(self._formations),
            "history": len(self._history),
            "active": len(self._active_runs),
            "bb_entries": self._blackboard.size,
            "bootstrap_active": self.bootstrap_active,
        }

    def get_task_status(self, task_id: str) -> Optional[dict[str, Any]]:
        """查询任务进度"""
        # 先查活跃任务
        if task_id in self._active_runs:
            run = self._active_runs[task_id]
            return {
                "task_id": task_id,
                "status": run.status.value,
                "task": run.task,
                "formation": run.formation or run.team_name,
                "subtasks": [{"sid": s.sid, "persona": s.persona,
                              "objective": s.objective} for s in run.subtasks],
                "completed_steps": len(run.results),
                "start_time": run.start_time,
                "active": True,
            }

        # 查历史
        for run in reversed(self._history):
            if run.run_id == task_id:
                return {
                    "task_id": task_id,
                    "status": run.status.value,
                    "task": run.task,
                    "formation": run.formation or run.team_name,
                    "audit": run.audit,
                    "results_count": len(run.results),
                    "start_time": run.start_time,
                    "end_time": run.end_time,
                    "active": False,
                }
        return None

    def get_after_action(self, task_id: str) -> Optional[dict[str, Any]]:
        """获取战后复盘报告"""
        for run in reversed(self._history):
            if run.run_id == task_id:
                if run.after_action:
                    return asdict(run.after_action)
        return None

    def list_formations(self) -> dict[str, dict[str, Any]]:
        """列出所有军阵模式"""
        return {
            key: {
                "name": fm["name"],
                "icon": fm["icon"],
                "desc": fm["desc"],
                "personas": fm["personas"],
                "mode": fm["mode"],
                "strategy": fm["strategy"],
                "max_duration_seconds": fm.get("max_duration_seconds", 0),
            }
            for key, fm in self._formations.items()
        }

    def register_formation(self, name: str, icon: str, desc: str,
                           personas: dict[str, str], mode: str = "chain",
                           strategy: str = "", max_duration: int = 600) -> dict[str, Any]:
        """注册新军阵"""
        key = name.lower().strip().replace(" ", "_")
        if key in self._formations:
            return {"ok": False, "error": f"军阵 '{key}' 已存在"}

        self._formations[key] = {
            "name": name,
            "icon": icon,
            "desc": desc,
            "personas": personas,
            "mode": mode,
            "strategy": strategy,
            "max_duration_seconds": max_duration,
        }
        return {"ok": True, "key": key, "name": name}

    def list_teams(self):
        return {k: {"name": v["name"], "desc": v["desc"]}
                for k, v in TEAM_TEMPLATES.items()}

    @property
    def agent_count(self):
        return self._runner.agent_count

    # ── helper ──

    @staticmethod
    def _gen_run_id(team_name: str, task: str) -> str:
        return hashlib.sha256(
            f"{team_name}:{task}:{time.time()}:{uuid.uuid4()}".encode()
        ).hexdigest()[:12]


# ═══════════════════════════════════════════════════════════════
# 全链路集成测试
# ═══════════════════════════════════════════════════════════════

def integration_test() -> tuple[bool, str]:
    errors = []

    def chk(name, cond, detail=""):
        s = "✅" if cond else "❌"
        print(f"  {s} {name}" + (f" — {detail}" if detail else ""))
        if not cond:
            errors.append(name)
        return cond

    print("╔══════════════════════════════════════════════════════════╗")
    print("║   龍魂 军团指挥中枢 · 全链路集成测试 v2.0                 ║")
    print("║   DNA: #龍芯⚡️丙午·乙未·TEAM-ORCH-V2.0                   ║")
    print("╚══════════════════════════════════════════════════════════╝\n")

    orch = TeamOrchestrator()

    # [1] 四组件就绪
    print("[1/8] 核心组件就绪")
    chk("InterAgentBus", get_bus() is not None)
    chk("PersonaRunner", orch.agent_count >= 17, f"{orch.agent_count} agents")
    chk("SharedBlackboard", orch._blackboard is not None)
    chk("TaskDecomposer", orch._decomposer is not None)
    chk("ConflictDetector", orch._conflict_detector is not None)
    chk("AfterActionEngine", orch._after_action is not None)
    print()

    # [2] 任务拆解
    print("[2/8] 任务拆解器测试")
    subtasks = orch._decomposer.decompose("审计并修复安全漏洞")
    chk("生成子任务", len(subtasks) >= 3, f"{len(subtasks)} subtasks")
    chk("包含P05审计", any(s.persona == "P05" for s in subtasks))
    chk("包含P77安全", any(s.persona == "P77" for s in subtasks))
    chk("包含P04修复", any(s.persona == "P04" for s in subtasks))
    print()

    # [3] 军阵模式
    print("[3/8] 五种军阵模式")
    formations = orch.list_formations()
    chk("闪电战", "blitzkrieg" in formations)
    chk("围猎", "encirclement" in formations)
    chk("筑城", "fortification" in formations)
    chk("排雷", "minesweeping" in formations)
    chk("讲武", "lecture" in formations)
    print()

    # [4] 链式调度（旧版兼容）
    print("[4/8] 链式调度 (审计链路)")
    r1 = orch.run_team("audit", "集成测试: 审计 engines/ 目录", auto_decompose=False)
    chk("链路完成", r1.audit["status"] in ("🟢", "🟡"), f"{r1.audit['ok']}/{r1.audit['total']} ok")
    chk("P05+P06参与", any("P05" in str(r) for r in r1.results) and any("P06" in str(r) for r in r1.results))
    print()

    # [5] 并行调度（旧版兼容）
    print("[5/8] 并行调度 (文化层)")
    r2 = orch.run_team("cultural", "创作一首关于龍魂的诗", auto_decompose=False)
    chk("并行完成", r2.audit["total"] >= 4, f"{r2.audit['total']} members")
    print()

    # [6] 总线+黑板
    print("[6/8] 总线通信+黑板共享")
    p00 = orch._runner.get_agent("P00")
    if p00:
        mid = p00.send_to("P05", {"test": "integration_ping"}, "test")
        chk("P00→P05 总线通信", bool(mid), f"msg_id={mid}")
    eid = orch._blackboard.put("test:hello", "world", writer="P00")
    chk("黑板写入", bool(eid))
    val = orch._blackboard.get("test:hello", pid="P00")
    chk("黑板读取", val == "world")
    eid2 = orch._blackboard.put("test:priv", "secret", writer="P00", visibility=Visibility.PRIVATE)
    chk("私有可见性隔离", orch._blackboard.get("test:priv", pid="P05") is None)
    print()

    # [7] 冲突检测
    print("[7/8] 冲突检测与裁决")
    mock_results = [
        {"persona": "P04", "status": "ok",
         "result": "建议重写引擎，性能可提升50%"},
        {"persona": "P07", "status": "ok",
         "result": "成本过高，不建议重写，小幅优化即可"},
        {"persona": "P77", "status": "ok",
         "result": "当前代码存在安全隐患，必须停止发布"},
        {"persona": "P14", "status": "ok",
         "result": "可以部署，风险评估为低"},
    ]
    conflicts = orch._conflict_detector.detect(mock_results)
    chk("检测到P04vsP07冲突", any(c.between == ["P04", "P07"] or c.between == ["P07", "P04"] for c in conflicts))
    chk("P77安全否决P14", any(("P77" in c.between or "P14" in c.between) and "安全" in c.between for c in conflicts),
        f"{len(conflicts)} conflicts detected")
    print()

    # [8] 战后复盘
    print("[8/8] 战后复盘报告")
    if r1.end_time:
        report = orch._after_action.generate(r1)
        chk("复盘报告生成", report is not None)
        chk("包含贡献评分", len(report.contributions) >= 1)
        chk("DNA追溯码", bool(report.dna))
        chk("审计色", bool(report.audit_color))
    print()

    # 状态汇总
    st = orch.status_report()
    print(f"\n系统状态: {st['agents']} agents | {st['formations']} formations "
          f"| {st['history']} history | bootstrap={'✅' if st['bootstrap_active'] else '⏸️'}")

    passed = len(errors) == 0
    print(f"\n{'='*56}")
    print(f"  结果: {'✅ 全部通过' if passed else f'❌ {len(errors)} 项失败'}")
    if errors:
        for e in errors:
            print(f"    - {e}")
    print(f"{'='*56}")
    return passed, ", ".join(errors) if errors else "ALL_PASS"


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="龍魂 TeamOrchestrator 军团指挥中枢 v2.0")
    p.add_argument("--test", action="store_true", help="运行全链路集成测试")
    p.add_argument("--list", action="store_true", help="列出可用团队模板")
    p.add_argument("--formations", action="store_true", help="列出所有军阵模式")
    p.add_argument("--run", type=str, nargs=2, metavar=("TEAM", "TASK"), help="运行指定团队")
    p.add_argument("--execute", type=str, nargs=2, metavar=("FORMATION", "TASK"),
                   help="军阵模式执行")
    p.add_argument("--status", action="store_true", help="系统状态报告")
    p.add_argument("--decompose", type=str, metavar="TASK", help="测试任务拆解（不执行）")
    args = p.parse_args()

    orch = TeamOrchestrator()

    if args.test:
        passed, msg = integration_test()
        sys.exit(0 if passed else 1)

    if args.list:
        print("旧版团队模板:")
        for k, v in orch.list_teams().items():
            print(f"  {k:10s} {v['name']:10s} {v['desc']}")

    if args.formations:
        print("五种军阵模式:")
        for k, fm in orch.list_formations().items():
            print(f"  {fm['icon']} {fm['name']:8s} [{k}]")
            print(f"     {fm['desc']}")
            print(f"     人格: {', '.join(fm['personas'])}")
            print(f"     策略: {fm['strategy']}")

    if args.decompose:
        print(f"任务拆解: {args.decompose}")
        subtasks = orch._decomposer.decompose(args.decompose)
        for s in subtasks:
            print(f"  [{s.sid}] P={s.priority} {s.persona:6s} | {s.tier:6s} | {s.objective}")

    if args.run:
        team, task = args.run
        print(f"运行团队 [{team}]: {task}")
        run = orch.run_team(team, task)
        print(f"  审计: {run.audit['status']} | {run.audit['ok']}/{run.audit['total']} ok | {run.audit['duration_ms']}ms")
        for r in run.results:
            pid = r.get("persona", "?")
            stt = r.get("status", "?")
            print(f"  {'✅' if stt == 'ok' else '❌'} {pid}")
        if run.after_action:
            print(f"  复盘: {run.after_action.final_verdict}")

    if args.execute:
        formation, task = args.execute
        print(f"军阵执行 [{formation}]: {task}")
        run = orch.execute(task, formation)
        print(f"  审计: {run.audit['status']} | {run.audit['ok']}/{run.audit['total']} ok | {run.audit['duration_ms']}ms")
        if run.after_action:
            print(f"  复盘: {run.after_action.final_verdict}")

    if args.status:
        st = orch.status_report()
        print(json.dumps(st, ensure_ascii=False, indent=2))
