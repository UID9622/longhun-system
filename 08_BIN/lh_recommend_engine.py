#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·辛未·丙戌·未时·需-RECOMMEND-ENGINE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# 🐉 龍魂 · 触角推荐引擎 v1.0
# DNA: #龍芯⚡️丙午·辛未·丙戌·未时·需-RECOMMEND-ENGINE-v1.0
"""
龍魂触角推荐引擎 — 不用你记技能，系统根据上下文主动推荐

核心原理：
  1. DNA认证 → 确定推荐等级
  2. 上下文理解 → 语义匹配技能
  3. 三色审计 → 每项技能过审计
  4. 数字根 → 每项技能算数字根
  5. 异常检测 → 自动发现风险
  6. 推荐排序 → 从高到低推荐 → 你点确认执行

分级策略：
  L0 本尊 UID9622 → 全推荐·全执行
  L1 中国·DNA干净·积极贡献 → 有推荐·可执行
  L2 中国·未验证DNA → 基础推荐·需确认
  L3 境外·干净 → 受限推荐·审计后放行
  L4 未知/可疑 → 只审计·不推荐

用法：
  python3 bin/lh_recommend_engine.py --context "我要部署一个新服务"
  python3 bin/lh_recommend_engine.py --assess --uid UID9622-XXXXXX
  python3 bin/lh_recommend_engine.py --dashboard  # 启动推荐仪表盘
"""

import hashlib
import json
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict

# ── 常量 ──
龍魂根 = Path(__file__).resolve().parent.parent
技能注册表路径 = 龍魂根 / "skills" / "longhun-skills.json"
总线注册表路径 = 龍魂根 / "bin" / "lh_skill_bus.py"  # 存在即导入映射

DNA_FULL = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️"
UID_MASTER = "9622"
CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


# ═══════════ 数字根 ═══════════
def digital_root(n: int) -> int:
    """dr(n)=1+((n-1) mod 9)"""
    n = abs(n)
    return 0 if n == 0 else 1 + (n - 1) % 9


def dr_gate(n: int) -> Tuple[str, str]:
    """数字根闸门：返回颜色 + 含义"""
    dr = digital_root(n)
    if dr in (3, 9):
        return "🔴", "不动点·高权重决策"
    elif dr == 6:
        return "🟡", "临界态·需谨慎"
    else:
        return "🟢", "流通态·正常"


# ═══════════ DNA 等级 ═══════════
class DNALevel(Enum):
    L0_本尊 = "L0"        # UID9622 本人
    L1_中国干净 = "L1"     # 中国·DNA验证·积极贡献
    L2_中国未验证 = "L2"   # 中国·未验证DNA
    L3_境外干净 = "L3"     # 境外·通过基础审计
    L4_未知 = "L4"         # 未知/可疑


# ═══════════ 三色审计 ═══════════
RED_KEYWORDS = [
    "伪造", "假冒", "攻击", "窃取", "泄露", "root", "admin",
    "匿名", "anonymous", "fake", "test", "example", "rm -rf", "push --force",
]
# 注意：不包含"篡改"因为会和"防篡改"误匹配
# 上下文关键词：key=危险词, value=保护性前缀整体词
RED_SAFE_PHRASES = [
    "防篡改",  # "防篡改"整体是安全操作
]

YELLOW_KEYWORDS = [
    "代理", "代办", "临时", "未实名", "待审", "异常", "注意", "warning",
]

GREEN_KEYWORDS = [
    "真实", "实名", "合规", "通过", "可信", "龍魂", "UID9622", "中国",
    "人民", "数据主权",
]


def tri_color_audit(text: str, dna_level: DNALevel) -> Dict[str, Any]:
    """三色审计：输入文本 → 🔴/🟡/🟢 判定"""
    text_lower = text.lower()
    rules_triggered: List[str] = []

    # 红词检测（基础词）
    for kw in RED_KEYWORDS:
        if kw.lower() in text_lower:
            rules_triggered.append(f"🔴 红线命中: {kw}")
            return {
                "level": "🔴",
                "reason": f"包含禁止内容: {kw}",
                "rules": rules_triggered,
                "allow_execute": False,
                "allow_recommend": False,
            }

    # 上下文红词检测（排除保护性短语）
    # "篡改"单独出现是红线，但"防篡改"整体是保护性操作
    if "篡改" in text_lower:
        safe = any(sp in text_lower for sp in RED_SAFE_PHRASES)
        if not safe:
            rules_triggered.append("🔴 红线命中: 篡改")
            return {
                "level": "🔴",
                "reason": "包含禁止内容: 篡改",
                "rules": rules_triggered,
                "allow_execute": False,
                "allow_recommend": False,
            }

    # L4 未知直接黄灯
    if dna_level == DNALevel.L4_未知:
        rules_triggered.append("🟡 DNA未知来源·只审计不推荐")
        return {
            "level": "🟡",
            "reason": "DNA未知·仅审计",
            "rules": rules_triggered,
            "allow_execute": False,
            "allow_recommend": False,
        }

    # 黄词检测
    for kw in YELLOW_KEYWORDS:
        if kw.lower() in text_lower:
            rules_triggered.append(f"🟡 黄线命中: {kw}")
            return {
                "level": "🟡",
                "reason": f"包含警示内容: {kw}",
                "rules": rules_triggered,
                "allow_execute": dna_level in (DNALevel.L0_本尊, DNALevel.L1_中国干净),
                "allow_recommend": dna_level != DNALevel.L4_未知,
            }

    # 绿词确认
    green_hits = [kw for kw in GREEN_KEYWORDS if kw.lower() in text_lower]
    if green_hits:
        rules_triggered.append(f"🟢 绿线确认: {', '.join(green_hits)}")

    # 放行
    allow_exec = dna_level in (
        DNALevel.L0_本尊, DNALevel.L1_中国干净, DNALevel.L2_中国未验证
    )
    allow_rec = dna_level != DNALevel.L4_未知

    return {
        "level": "🟢",
        "reason": "三色审计通过",
        "rules": rules_triggered,
        "allow_execute": allow_exec,
        "allow_recommend": allow_rec,
    }


# ═══════════ DNA 等级判定 ═══════════
def detect_dna_level(uid: str = "", dna_signature: str = "", 
                     location_hint: str = "", verified: bool = False) -> Tuple[DNALevel, Dict[str, Any]]:
    """判定用户DNA等级"""
    info: Dict[str, Any] = {}

    # L0: 本尊
    if uid == UID_MASTER or CONFIRM_SEAL in dna_signature:
        info["match"] = "本尊DNA确认"
        info["privilege"] = "全部技能·全部推荐·直接执行"
        return DNALevel.L0_本尊, info

    # L1: 中国·已验证DNA
    china_keywords = ["🇨🇳", "中国", "CN", "zh", "龙", "龍", "华"]
    # 境外关键词（优先检测）
    overseas_keywords = ["境外", "海外", "overseas", "US", "UK", "JP", "KR", "EU"]
    is_overseas = any(kw.lower() in location_hint.lower() for kw in overseas_keywords)
    is_china = (not is_overseas) and any(
        kw.lower() in (uid + dna_signature + location_hint).lower() 
        for kw in china_keywords
    )

    if is_china and verified and dna_signature.startswith("#龍芯"):
        info["match"] = "中国·DNA验证通过·积极贡献"
        info["privilege"] = "有推荐·可执行·信任通道"
        return DNALevel.L1_中国干净, info

    # L2: 中国·未验证
    if is_china:
        info["match"] = "中国·DNA未验证"
        info["privilege"] = "基础推荐·需确认执行"
        return DNALevel.L2_中国未验证, info

    # L3: 境外·通过基础审计
    if is_overseas and (verified or dna_signature):
        info["match"] = "境外·基础审计通过"
        info["privilege"] = "受限推荐·审计后放行"
        return DNALevel.L3_境外干净, info

    # L4: 未知
    info["match"] = "未知来源"
    info["privilege"] = "只审计·不推荐·不执行"
    return DNALevel.L4_未知, info


# ═══════════ 技能匹配 ═══════════
# 从技能总线映射中提取分类-技能对应关系
SKILL_CATEGORIES: Dict[str, List[Dict[str, str]]] = {
    "安全": [
        {"id": "anti_tamper", "name": "防篡改扫描", "desc": "外部AI内容三色审计·红线熔断"},
        {"id": "water_detect", "name": "水军检测", "desc": "行为指纹·水军模式识别"},
        {"id": "red_team", "name": "红队引擎", "desc": "渗透测试·漏洞发现"},
        {"id": "auto_heal", "name": "自动自愈", "desc": "四道体检·自动修复·留痕"},
        {"id": "dual_audit", "name": "双重审计", "desc": "双引擎交叉验证审计"},
    ],
    "治理": [
        {"id": "dna_registry", "name": "DNA统一登记", "desc": "物理+虚拟+身份全维登记"},
        {"id": "dna_audit", "name": "DNA审计", "desc": "登记册完整性审计"},
        {"id": "persona_orchestrator", "name": "人格编排", "desc": "16个人格路由调度"},
        {"id": "innovation_tracer", "name": "创新溯源", "desc": "五维证据·谁先自研的"},
        {"id": "contrib_eval", "name": "贡献评估", "desc": "龍魂公式·贡献值计算"},
    ],
    "开发": [
        {"id": "cnsh_absorb", "name": "CNSH吸收器", "desc": "代码→中文可编辑"},
        {"id": "daoyin", "name": "道引器", "desc": "开源吸收·许可证检查"},
        {"id": "self_extract", "name": "自解压引擎", "desc": "DNA硬编码·落地即运行"},
    ],
    "AI": [
        {"id": "lora_trainer", "name": "LoRA训练器", "desc": "本地LoRA微调训练"},
        {"id": "semantic_engine", "name": "语义上下文引擎", "desc": "语义抽屉·意图推断"},
        {"id": "tongxinyi_router", "name": "通心译IPA路由", "desc": "语义→人格路由"},
        {"id": "brain_sync", "name": "脑同步", "desc": "本地大脑↔云端记忆同步"},
    ],
    "经济": [
        {"id": "wishpool", "name": "许愿池", "desc": "人民资源池·取之于民"},
        {"id": "trust_score", "name": "信任积分", "desc": "三分桶·贡献公证"},
        {"id": "ecny_cross", "name": "数字人民币跨境", "desc": "e-CNY跨境支付通道"},
    ],
    "数字人": [
        {"id": "voice_twin", "name": "声音克隆", "desc": "语音克隆·数字分身"},
        {"id": "tongxinyi", "name": "通心译", "desc": "场景词典·一词多义"},
    ],
    "运维": [
        {"id": "cross_awareness", "name": "联动感知", "desc": "跨模块依赖检查·自动报警"},
        {"id": "memory_load", "name": "记忆加载", "desc": "会话启动记忆加载"},
        {"id": "server_check", "name": "服务器巡检", "desc": "服务器在线状态检测"},
        {"id": "health_check", "name": "健康检查", "desc": "系统全维度健康检查"},
    ],
    "生态": [
        {"id": "ecosystem_passport", "name": "生态通行证", "desc": "DNA绑定·四层会员"},
        {"id": "recommend_engine", "name": "触角推荐引擎", "desc": "智能推荐·上下文匹配"},
    ],
}

# 关键词 → 分类映射（语义匹配）
KEYWORD_CATEGORY_MAP: Dict[str, List[str]] = {
    "安全": ["安全", "审计", "攻击", "漏洞", "水军", "篡改", "熔断", "防护", "红队", "渗透", "自愈", "修复"],
    "治理": ["治理", "DNA", "人格", "注册", "登记", "溯源", "贡献", "主权", "身份", "注册"],
    "开发": ["开发", "代码", "CNSH", "编程", "道引", "开源", "压缩", "打包", "部署", "构建"],
    "AI": ["AI", "训练", "模型", "学习", "语义", "路由", "翻译", "记忆", "同步", "LoRA"],
    "经济": ["经济", "许愿", "积分", "支付", "e-CNY", "信任", "资源", "金融"],
    "数字人": ["数字人", "声音", "克隆", "分身", "通心译", "语音"],
    "运维": ["运维", "巡检", "监控", "健康", "检查", "启动", "加载", "联动"],
    "生态": ["生态", "通行证", "推荐", "总线", "调度", "服务"],
}


def match_skills(context: str, dna_level: DNALevel) -> List[Dict[str, Any]]:
    """语义匹配技能列表"""
    context_lower = context.lower()
    category_scores: Dict[str, float] = {}

    for cat, keywords in KEYWORD_CATEGORY_MAP.items():
        score = 0.0
        for kw in keywords:
            if kw.lower() in context_lower:
                score += 1.0
        if score > 0:
            category_scores[cat] = score

    # 无匹配时默认推荐运维和治理
    if not category_scores:
        category_scores["运维"] = 0.5
        category_scores["治理"] = 0.3

    # 构建推荐列表
    recommendations: List[Dict[str, Any]] = []
    for cat, score in sorted(category_scores.items(), key=lambda x: -x[1]):
        if cat not in SKILL_CATEGORIES:
            continue
        for skill in SKILL_CATEGORIES[cat]:
            audit = tri_color_audit(
                f"{skill['name']} {skill['desc']} {context}", dna_level
            )
            dr_color, dr_meaning = dr_gate(hash(skill["id"]) % 100)

            # L3境外只给安全+治理基础推荐
            if dna_level == DNALevel.L3_境外干净:
                if cat not in ("安全", "治理"):
                    continue

            recommendations.append({
                **skill,
                "category": cat,
                "relevance": round(score / max(category_scores.values()), 2),
                "audit_level": audit["level"],
                "audit_reason": audit["reason"],
                "audit_rules": audit["rules"],
                "allow_execute": audit["allow_execute"],
                "digital_root": dr_color,
                "dr_meaning": dr_meaning,
                "dr_value": digital_root(hash(skill["id"]) % 100),
            })

    # 按相关度排序
    recommendations.sort(key=lambda x: -x["relevance"])
    return recommendations


# ═══════════ 异常检测 ═══════════
def detect_anomalies(context: str, dna_level: DNALevel) -> List[Dict[str, Any]]:
    """检测上下文中的异常"""
    anomalies: List[Dict[str, Any]] = []

    # 1. 检测高危操作
    dangerous_patterns = [
        ("rm -rf", "🔴", "检测到强制删除命令"),
        ("DROP TABLE", "🔴", "检测到数据库删除操作"),
        ("chmod 777", "🟡", "检测到危险权限设置"),
        ("sudo", "🟡", "检测到提权操作"),
        ("eval(", "🟡", "检测到eval执行"),
        ("exec(", "🟡", "检测到exec执行"),
        ("subprocess", "🟡", "检测到子进程调用"),
    ]
    for pattern, color, desc in dangerous_patterns:
        if pattern.lower() in context.lower():
            anomalies.append({
                "type": "高危操作",
                "level": color,
                "detail": desc,
                "pattern": pattern,
            })

    # 2. L4未知来源 → 标记
    if dna_level == DNALevel.L4_未知:
        anomalies.append({
            "type": "身份异常",
            "level": "🔴",
            "detail": "DNA来源未知·禁止推荐执行",
            "suggestion": "先完成DNA身份注册",
        })

    # 3. L2未验证 → 提醒
    if dna_level == DNALevel.L2_中国未验证:
        anomalies.append({
            "type": "身份提醒",
            "level": "🟡",
            "detail": "DNA未验证·部分功能受限",
            "suggestion": "建议完成DNA绑定验证",
        })

    # 4. 检测外部依赖请求
    external_patterns = ["pip install", "npm install", "brew install", "apt-get"]
    for ep in external_patterns:
        if ep in context.lower():
            anomalies.append({
                "type": "外部依赖",
                "level": "🟡",
                "detail": f"检测到外部依赖安装请求: {ep}",
                "suggestion": "考虑道引本地替代方案",
            })

    return anomalies


# ═══════════ 主推荐引擎 ═══════════
@dataclass
class RecommendResult:
    """推荐结果"""
    # 身份
    dna_level: str
    dna_level_name: str
    dna_info: Dict[str, Any]

    # 审计
    context_audit: Dict[str, Any]

    # 数字根
    context_dr_color: str
    context_dr_meaning: str
    context_dr_value: int

    # 异常
    anomalies: List[Dict[str, Any]]

    # 推荐
    recommendations: List[Dict[str, Any]]
    recommendation_count: int

    # 时间
    timestamp: str
    dna_trace: str

    # 一句话总结
    summary: str


def recommend(context: str, uid: str = "", dna_signature: str = "",
              location_hint: str = "", verified: bool = False) -> RecommendResult:
    """
    核心推荐函数 — 一站式：DNA → 审计 → 数字根 → 技能匹配 → 异常检测

    Args:
        context: 用户输入/上下文
        uid: 用户UID
        dna_signature: DNA签名
        location_hint: 位置线索
        verified: 是否已验证
    """
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dna_trace = _make_dna_trace("recommend", context)

    # 1. DNA等级
    dna_level, dna_info = detect_dna_level(uid, dna_signature, location_hint, verified)

    # 2. 上下文审计
    context_audit = tri_color_audit(context, dna_level)

    # 3. 数字根
    dr_n = hash(context) % 100
    dr_color, dr_meaning = dr_gate(dr_n)

    # 4. 异常检测
    anomalies = detect_anomalies(context, dna_level)

    # 5. 技能匹配
    skills = match_skills(context, dna_level)

    # 6. 一句话总结
    summary = _gen_summary(dna_level, context_audit, anomalies, skills)

    return RecommendResult(
        dna_level=dna_level.value,
        dna_level_name=_level_name(dna_level),
        dna_info=dna_info,
        context_audit=context_audit,
        context_dr_color=dr_color,
        context_dr_meaning=dr_meaning,
        context_dr_value=digital_root(dr_n),
        anomalies=anomalies,
        recommendations=skills,
        recommendation_count=len(skills),
        timestamp=ts,
        dna_trace=dna_trace,
        summary=summary,
    )


def _level_name(level: DNALevel) -> str:
    names = {
        DNALevel.L0_本尊: "本尊 UID9622",
        DNALevel.L1_中国干净: "中国·干净DNA",
        DNALevel.L2_中国未验证: "中国·待验证",
        DNALevel.L3_境外干净: "境外·基础通行",
        DNALevel.L4_未知: "未知来源",
    }
    return names.get(level, "未知")


def _make_dna_trace(func: str, seed: str) -> str:
    h = hashlib.sha256((func + seed).encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️丙午·辛未·丙戌·{func}-{h}"


def _gen_summary(level: DNALevel, audit: Dict[str, Any], anomalies: List[Dict[str, Any]], skills: List[Dict[str, Any]]) -> str:
    parts: List[str] = []
    
    if level == DNALevel.L0_本尊:
        parts.append("🐉 本尊驾到·全推荐开启")
    elif level == DNALevel.L1_中国干净:
        parts.append("🇨🇳 干净DNA·信任通道")
    elif level == DNALevel.L2_中国未验证:
        parts.append("🟡 未验证·基础推荐")
    elif level == DNALevel.L3_境外干净:
        parts.append("🌍 境外·受限推荐")
    else:
        parts.append("🔴 未知来源·只审计")

    if audit["level"] == "🔴":
        parts.append("⚠️ 审计红线·部分技能已阻断")
    elif audit["level"] == "🟡":
        parts.append("🟡 审计黄线·需确认执行")

    red_anomalies = [a for a in anomalies if a["level"] == "🔴"]
    if red_anomalies:
        parts.append(f"🔴 {len(red_anomalies)}个高危异常")

    parts.append(f"📋 推荐{len(skills)}项技能")
    return " | ".join(parts)


# ═══════════ 仪表盘输出 ═══════════
def format_recommend_dashboard(result: RecommendResult) -> str:
    """格式化为可读的仪表盘输出"""
    lines: List[str] = []
    sep = "═" * 60

    lines.append(f"\n{sep}")
    lines.append(f"🐉 龍魂触角 · 推荐仪表盘")
    lines.append(f"{sep}")
    lines.append(f"⏰ {result.timestamp}")
    lines.append(f"🧬 {result.dna_trace}")
    lines.append(f"")

    # ── 身份区 ──
    lines.append(f"┌── 🔑 身份认证")
    level_icon = {"L0": "🐉", "L1": "🇨🇳", "L2": "🟡", "L3": "🌍", "L4": "🔴"}
    icon = level_icon.get(result.dna_level, "❓")
    lines.append(f"│ 等级: {icon} {result.dna_level_name} ({result.dna_level})")
    lines.append(f"│ 权限: {result.dna_info.get('privilege', '—')}")
    lines.append(f"│ 匹配: {result.dna_info.get('match', '—')}")
    lines.append(f"")

    # ── 审计区 ──
    lines.append(f"┌── 🔍 三色审计")
    lines.append(f"│ 判定: {result.context_audit['level']} {result.context_audit['reason']}")
    for rule in result.context_audit.get("rules", []):
        lines.append(f"│  ∟ {rule}")
    lines.append(f"")

    # ── 数字根区 ──
    lines.append(f"┌── 🔢 数字根")
    lines.append(f"│ {result.context_dr_color} dr={result.context_dr_value} → {result.context_dr_meaning}")
    lines.append(f"")

    # ── 异常区 ──
    lines.append(f"┌── ⚠️ 异常检测 ({len(result.anomalies)}项)")
    if not result.anomalies:
        lines.append(f"│  🟢 未检测到异常")
    for a in result.anomalies:
        lines.append(f"│  {a['level']} [{a['type']}] {a['detail']}")
        if a.get("suggestion"):
            lines.append(f"│    → {a['suggestion']}")
    lines.append(f"")

    # ── 推荐区 ──
    lines.append(f"┌── 📋 技能推荐 ({result.recommendation_count}项)")
    if not result.recommendations:
        lines.append(f"│  无推荐（DNA等级限制）")
    for i, rec in enumerate(result.recommendations[:15], 1):
        exec_icon = "✅" if rec["allow_execute"] else "⛔"
        lines.append(
            f"│  {i:2d}. [{rec['category']}] {rec['name']} "
            f"{rec['audit_level']} DR={rec['dr_value']}{rec['digital_root']} {exec_icon}"
        )
        lines.append(f"│      {rec['desc']} (相关度: {rec['relevance']:.0%})")
    lines.append(f"")

    # ── 一句话 ──
    lines.append(f"┌── 💬 总结")
    lines.append(f"│  {result.summary}")
    lines.append(f"{sep}")
    lines.append(f"")

    return "\n".join(lines)


def format_simple_recommend(result: RecommendResult) -> str:
    """精简输出 — 只给关键推荐"""
    lines: List[str] = []

    # 一句话
    lines.append(f"🐉 {result.summary}")

    # 数字根
    lines.append(f"🔢 数字根: {result.context_dr_color} dr={result.context_dr_value}")

    # 审计
    if result.context_audit["level"] != "🟢":
        lines.append(f"🔍 审计: {result.context_audit['level']} {result.context_audit['reason']}")

    # 异常
    for a in result.anomalies:
        lines.append(f"⚠️ {a['level']} {a['detail']}")

    # 推荐技能（最多5个）
    lines.append(f"\n📋 推荐执行:")
    for i, rec in enumerate(result.recommendations[:5], 1):
        exec_label = "✓ 可直接执行" if rec["allow_execute"] else "✗ 需确认"
        lines.append(f"  {i}. {rec['name']} — {rec['desc']} [{exec_label}]")

    return "\n".join(lines)


# ═══════════ CLI ═══════════
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂触角推荐引擎 v1.0 — 不用记技能·系统主动推荐"
    )
    parser.add_argument("--context", type=str, default="", help="上下文/用户输入")
    parser.add_argument("--uid", type=str, default=UID_MASTER, help="用户UID")
    parser.add_argument("--dna", type=str, default=DNA_FULL, help="DNA签名")
    parser.add_argument("--location", type=str, default="🇨🇳中国", help="位置线索")
    parser.add_argument("--verified", action="store_true", help="是否已验证DNA")
    parser.add_argument("--simple", action="store_true", help="精简输出模式")
    parser.add_argument("--assess", action="store_true", help="评估模式（仅审计+异常）")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--demo", action="store_true", help="演示四种身份场景")

    args = parser.parse_args()

    if args.demo:
        _run_demo()
        return

    ctx = args.context or " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "系统健康检查"

    result = recommend(
        context=ctx,
        uid=args.uid,
        dna_signature=args.dna,
        location_hint=args.location,
        verified=args.verified,
    )

    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2, default=str))
    elif args.simple:
        print(format_simple_recommend(result))
    else:
        print(format_recommend_dashboard(result))


def _run_demo():
    """演示四种身份的推荐结果"""
    scenarios = [
        ("UID9622 本尊", UID_MASTER, DNA_FULL, "🇨🇳中国", True),
        ("中国·干净DNA", "UID9622-LK9X", "#龍芯⚡️2026-REG-772Z", "🇨🇳中国·北京", True),
        ("中国·未验证", "", "", "🇨🇳中国", False),
        ("境外·干净", "UID9622-EX01", "#龍芯⚡️2026-REG-EX01", "🌍境外", True),
        ("未知来源", "", "", "", False),
    ]

    contexts = [
        "我要部署一个新服务到鲲鹏服务器上",
        "需要审计系统的DNA对齐",
        "帮我打包压缩龍魂系统分发给用户",
    ]

    for label, uid, dna, loc, verified in scenarios:
        print(f"\n{'='*70}")
        print(f"  🎭 场景: {label}")
        print(f"{'='*70}")
        ctx = contexts[hash(label) % len(contexts)]
        result = recommend(
            context=ctx, uid=uid, dna_signature=dna,
            location_hint=loc, verified=verified
        )
        print(format_simple_recommend(result))
        print()


if __name__ == "__main__":
    main()
