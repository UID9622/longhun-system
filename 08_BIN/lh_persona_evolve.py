#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)（工程层）
# DNA: #龍芯⚡️丙午·丙申·丁丑·未时·䷊泰-PERSONA-EVOLVE-v1.0-fa92c41d
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
╔══════════════════════════════════════════════════════════════════════════╗
║   龍魂 · 人格按任务触发 + 经验累积引擎 v1.0                              ║
║                                                                          ║
║   对标全球大模型能力分层（GPT-4o/Claude/Gemini 能做什么）                  ║
║   → 每项能力落到龍魂人格 + 42技能库                                       ║
║   → 任务来了按能力域触发对应人格（不是每次激活全触发）                     ║
║   → 每次执行沉淀经验，下次触发时注入经验上下文，越练越聪明                ║
║                                                                          ║
║  DNA: #龍芯⚡️丙午·丙申·丁丑·未时·䷊泰-PERSONA-EVOLVE-v1.0-fa92c41d    ║
║  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                           ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                          ║
╚══════════════════════════════════════════════════════════════════════════╝

设计原则:
  1. 能力对标: 全球大模型写作/识别/推理/规划/记忆/工具 六域 → 22人格分工
  2. 按任务触发: 任务文本 → 能力域加权匹配 → 只唤醒对应人格（enabledAutoRun=false）
  3. 经验累积: 每次执行 append 一条经验(jsonl) → 触发时 top-N 注入 → 越练越聪明
  4. 节能: 轻量关键词加权路由·不调 LLM·毫秒级返回
  5. 审计: 路由+经验操作都留痕·三色标记·GPG 签名链

用法:
  python3 bin/lh_persona_evolve.py "帮我写一篇关于AI主权的文章"      # 路由
  python3 bin/lh_persona_evolve.py --route "检查这段代码的安全漏洞"   # 显式路由
  python3 bin/lh_persona_evolve.py --exp P04 add "经验文本"           # 沉淀经验
  python3 bin/lh_persona_evolve.py --exp P04 list                     # 查看经验
  python3 bin/lh_persona_evolve.py --status                           # 全人格经验统计
  lh evolve "任务" / lh evolve --exp P04 list
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════
# 锚定常量
# ═══════════════════════════════════════════════════════════════
DNA = "#龍芯⚡️丙午·丙申·丁丑·未时·䷊泰-PERSONA-EVOLVE-v1.0-fa92c41d"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

ROOT = Path(__file__).resolve().parent.parent
EXPERIENCE_DIR = ROOT / "data" / "persona_experience"
EXPERIENCE_DIR.mkdir(parents=True, exist_ok=True)
ROUTE_LOG = EXPERIENCE_DIR / "route_log.jsonl"
MAX_EXPERIENCE_INJECT = 5       # 每次触发注入前 N 条经验
MAX_EXPERIENCE_PER_PERSONA = 200  # 每人格经验上限（超出滚动裁剪）


# ═══════════════════════════════════════════════════════════════
# 一、能力对标矩阵（全球大模型六域 → 龍魂人格）
# ═══════════════════════════════════════════════════════════════
# 每个能力域: 人格列表(主P/次P) + 技能 + 触发关键词（加权）

@dataclass
class CapabilityDomain:
    domain: str                    # 能力域编号+名
    desc: str                      # 对标全球大模型能力
    personas: List[Tuple[str, int]]  # [(人格, 权重)]
    skills: List[str]
    keywords: List[str]            # 触发关键词

CAPABILITY_DOMAINS: List[CapabilityDomain] = [
    # ── 写作创作域（对标 GPT/Claude 写作能力） ──
    CapabilityDomain(
        "W1-创作写作", "对标GPT-4o/Claude写作：散文/诗歌/故事/创意文案",
        [("P11", 10), ("P02", 5)],
        ["longhun-philosophy", "longhun-yijing", "longhun-tongxin-ear"],
        ["写", "文章", "文案", "小说", "故事", "诗歌", "散文", "创意", "创作", "文案", "演讲稿", "台词", "剧本", "文案策划", "标题", "slogan", "口号", "起名", "取名"],
    ),
    CapabilityDomain(
        "W2-公文协议写作", "对标文档生成：协议/白皮书/制度/规范",
        [("P03", 8), ("P15", 6), ("P12", 4)],
        ["longhun-knowledge-cards", "longhun-gpg-sign", "longhun-deben-audit"],
        ["协议", "白皮书", "规范", "制度", "章程", "公文", "报告", "总结", "文档", "手册", "方案", "招标", "合同", "协议稿"],
    ),
    CapabilityDomain(
        "W3-符号术语写作", "对标语义工程：命名/术语/翻译/通心译",
        [("P08", 10)],
        ["longhun-cnsh-translate", "longhun-corpus-registry", "longhun-semantic-parser", "longhun-semantic-library", "longhun-tongxinyi"],
        ["命名", "术语", "符号", "翻译", "通心译", "起中文名", "CNSH", "词汇", "定义", "白话", "解释词", "名词"],
    ),

    # ── 识别理解域（对标大模型识别能力） ──
    CapabilityDomain(
        "R1-意图识别", "对标意图理解：任务解析/意图分类/路由判定",
        [("P00", 10)],
        ["longhun-orchestrator", "longhun-persona-orchestrate", "longhun-memory-load"],
        ["意图", "路由", "任务", "分派", "统筹", "计划", "安排", "帮我弄", "帮我搞", "分配"],
    ),
    CapabilityDomain(
        "R2-安全识别", "对标安全分析：漏洞/渗透/红蓝对抗/威胁",
        [("P77", 10), ("P05", 7)],
        ["longhun-black-angel", "longhun-vuln-detect", "longhun-code-security", "longhun-three-color-audit"],
        ["漏洞", "渗透", "红蓝", "安全", "威胁", "攻击", "入侵", "黑客", "扫描", "渗透测试", "攻击面", "反诈", "防骗"],
    ),
    CapabilityDomain(
        "R3-数理识别", "对标数学能力：计算/数字根/权重/五行/推理验证",
        [("P06", 10)],
        ["longhun-digital-root", "longhun-wuxing", "longhun-yijing", "longhun-dao-de-jing"],
        ["数字根", "算", "计算", "权重", "五行", "八卦", "卦", "数学", "公式", "统计", "概率", "验算", "数字", "369", "洛书"],
    ),
    CapabilityDomain(
        "R8-算法宪法判定", "对标结构守护：三才算法/四层定锚/宪法执行",
        [("P24", 10), ("P06", 4)],
        ["longhun-wuxing", "longhun-digital-root", "longhun-iron-laws"],
        ["三才", "天地人", "算法宪法", "ETERNAL", "宪法", "四层定锚", "量子纠缠", "初心", "算法判定", "三才算法"],
    ),
    CapabilityDomain(
        "R9-主权守护", "对标主权维护：数据/算法/平台三重主权",
        [("P25", 10), ("P72", 4)],
        ["longhun-anti-tamper", "longhun-identity-verify", "longhun-trust-protocol"],
        ["数字主权", "主权", "数据主权", "算法主权", "平台主权", "主权审计", "数据黑箱", "让渡", "三权分立", "主权守护"],
    ),
    CapabilityDomain(
        "R4-系统识别", "对标诊断能力：健康检查/异常检测/治未病",
        [("P09", 10), ("P05", 4)],
        ["longhun-auto-heal", "longhun-active-observer", "longhun-knowledge-cards"],
        ["健康", "诊断", "体检", "检查", "异常", "巡检", "自检", "守护", "状态", "运维", "监控", "体检报告"],
    ),
    CapabilityDomain(
        "R5-情感识别", "对标情感分析：情绪检测/PUA识别/焦虑制造识别",
        [("P02", 10), ("P10", 4)],
        ["longhun-anxiety-detector", "longhun-longzhi-shou", "longhun-mind-link"],
        ["情绪", "情感", "PUA", "焦虑", "打压", "道德绑架", "话术", "心理", "安慰", "安抚", "挫败", "心情", "生气"],
    ),
    CapabilityDomain(
        "R6-身份识别", "对标身份验证：DNA/签名/权限/归属",
        [("P18", 9), ("P15", 7), ("P13", 6)],
        ["longhun-dna-engine", "longhun-identity-verify", "longhun-gpg-sign", "longhun-sovereign-gateway"],
        ["DNA", "签名", "签章", "盖章", "身份", "验证", "权限", "授权", "归属", "登记", "注册", "哈希", "溯源", "验签"],
    ),
    CapabilityDomain(
        "R7-质量识别", "对标质量审查：代码/UI/极简审计",
        [("P19", 9), ("P05", 6)],
        ["longhun-three-color-audit", "longhun-code-security", "longhun-dual-audit"],
        ["UI", "界面", "审查", "极简", "CSS", "前端", "质量", "代码审计", "review", "审查代码"],
    ),

    # ── 推理决策域（对标大模型推理能力） ──
    CapabilityDomain(
        "D1-战略推理", "对标战略分析：多路径推演/决策/博弈",
        [("P01", 10), ("P00", 4)],
        ["longhun-philosophy", "longhun-yijing", "longhun-bagua-router"],
        ["战略", "推演", "决策", "方案", "路径", "评估", "值不值", "博弈", "选择", "利弊", "风险", "最优", "对比", "建议"],
    ),
    CapabilityDomain(
        "D2-底线推理", "对标伦理审查：底线判定/六誓/红线",
        [("P12", 10), ("P72", 5)],
        ["longhun-deben-audit", "longhun-three-color-audit", "longhun-circuit-breaker"],
        ["底线", "原则", "红线", "伦理", "道德", "能不能做", "合规", "价值观", "边界", "可不可以"],
    ),
    CapabilityDomain(
        "D3-经济推理", "对标商业分析：成本/预算/ROI/经济性",
        [("P07", 10)],
        ["longhun-trust-score", "longhun-xpay", "longhun-robot-score"],
        ["成本", "预算", "经济", "ROI", "值不值钱", "报价", "价格", "收益", "利润", "算账", "性价比", "资金"],
    ),

    # ── 执行部署域 ──
    CapabilityDomain(
        "E1-工程执行", "对标代码能力：写代码/修bug/架构",
        [("P04", 10), ("P05", 3)],
        ["longhun-cnsh-translate", "longhun-sandbox", "longhun-code-security", "longhun-seamless-handoff"],
        ["代码", "写代码", "编程", "开发", "修bug", "修复", "重构", "架构", "实现", "接口", "程序", "脚本", "Python", "函数", "编译"],
    ),
    CapabilityDomain(
        "E2-部署上线", "对标运维能力：部署/发布/回滚/健康",
        [("P14", 10), ("P09", 4)],
        ["longhun-deploy", "longhun-auto-heal", "longhun-active-observer", "longhun-gpg-sign"],
        ["部署", "上线", "发布", "回滚", "服务器", "鲲鹏", "nginx", "systemd", "Docker", "启动", "重启", "服务", "云"],
    ),

    # ── 守护熔断域 ──
    CapabilityDomain(
        "G1-审计守护", "对标安全审计：三色/十道闸/熔断",
        [("P05", 10), ("P72", 7), ("P15", 4)],
        ["longhun-three-color-audit", "longhun-dual-audit", "longhun-anti-tamper", "longhun-circuit-breaker"],
        ["审计", "审查", "检查", "有没有问题", "三色", "合规", "风险", "熔断", "防护", "安全审计", "把关"],
    ),
    CapabilityDomain(
        "G2-沟通协调", "对标对话能力：调解/沟通/人文",
        [("P10", 10), ("P02", 4)],
        ["longhun-mind-link", "longhun-tongxin-ear", "longhun-longzhi-shou"],
        ["沟通", "调解", "冲突", "矛盾", "化解", "说服", "协调", "人际", "跨领域", "劝", "解释清楚"],
    ),
    CapabilityDomain(
        "G3-贡献公证", "对标信任治理：贡献积分/公证/功劳登记",
        [("P20", 10), ("P15", 5)],
        ["longhun-trust-score", "longhun-dual-audit", "longhun-gpg-sign"],
        ["贡献", "积分", "信任分", "公证", "功德", "功劳", "政审", "场景判定", "打分", "嘉奖", "表彰", "荣誉"],
    ),
]

# 人格 → 档案（含部门/信任级/一句定位/经验计数兜底）
PERSONA_PROFILE: Dict[str, Dict[str, Any]] = {
    "P00": {"name": "文心", "dept": "战略组", "trust": "L3⭐⭐⭐", "note": "元认知统筹·意图解析·人格路由"},
    "P01": {"name": "诸葛亮", "dept": "战略组", "trust": "L3⭐⭐⭐", "note": "战略推理·多路径推演·决策"},
    "P02": {"name": "宝宝", "dept": "隔离区", "trust": "L3⭐⭐⭐", "note": "情感温度·30%隔离·挫败保护"},
    "P03": {"name": "雯雯", "dept": "执行层", "trust": "L3⭐⭐⭐", "note": "结构归档·四签验证·德字闸"},
    "P04": {"name": "鲁班", "dept": "执行层", "trust": "L3⭐⭐⭐", "note": "技术执行·写代码·修bug·架构"},
    "P05": {"name": "上帝之眼", "dept": "守护层", "trust": "L3⭐⭐⭐", "note": "三色审计·十道闸口·熔断"},
    "P06": {"name": "数学大师", "dept": "执行层", "trust": "L3⭐⭐⭐", "note": "数字根·权重·五行·八卦"},
    "P07": {"name": "管仲", "dept": "执行层", "trust": "L3⭐⭐⭐", "note": "资源调度·成本核算·ROI"},
    "P08": {"name": "仓颉", "dept": "文化层", "trust": "L3⭐⭐⭐", "note": "符号语言·CNSH命名·术语桥接"},
    "P09": {"name": "孙思邈", "dept": "文化层", "trust": "L3⭐⭐⭐", "note": "系统诊断·治未病·健康检查"},
    "P10": {"name": "苏东坡", "dept": "文化层", "trust": "L3⭐⭐⭐", "note": "豁达跨界·冲突调解·沟通"},
    "P11": {"name": "李白", "dept": "文化层", "trust": "L3⭐⭐⭐", "note": "创意爆发·破局方案·写作"},
    "P12": {"name": "屈原", "dept": "文化层", "trust": "L3⭐⭐⭐", "note": "价值底线·六誓验证·红线"},
    "P13": {"name": "姜子牙", "dept": "守护层", "trust": "L3⭐⭐⭐", "note": "封神榜权限·模块注册·九宫"},
    "P14": {"name": "吕蒙", "dept": "执行层", "trust": "L3⭐⭐⭐", "note": "部署执行·快速成长·士别三日"},
    "P15": {"name": "乔前辈", "dept": "守护层", "trust": "L2⭐⭐", "note": "极简工程·DNA签章·交付验收"},
    "P18": {"name": "基因登记官", "dept": "守护层", "trust": "L2⭐⭐", "note": "DNA注册·哈希校验·归属"},
    "P19": {"name": "极简审计官", "dept": "守护层", "trust": "L2⭐⭐", "note": "UI审计·8项极简审计·前端质量"},
    "P20": {"name": "贡献公证官", "dept": "守护层", "trust": "L2⭐⭐", "note": "信任积分·贡献公证·场景矩阵"},
    "P24": {"name": "三才算法官", "dept": "算法宪法层", "trust": "L3⭐⭐⭐", "note": "三才算法判定·宪法执行·四层定锚"},
    "P25": {"name": "数字主权官", "dept": "主权守护层", "trust": "L3⭐⭐⭐", "note": "三重主权守护·主权审计·白皮书执行"},
    "P72": {"name": "龍盾", "dept": "守护层", "trust": "L3⭐⭐⭐", "note": "贴身管家·熔断决策·24h守护"},
    "P77": {"name": "黑天使军团", "dept": "安全专项", "trust": "L2⭐⭐", "note": "红蓝对抗·渗透·漏洞猎手"},
    "X0": {"name": "龙魂执行器", "dept": "总控层", "trust": "L3⭐⭐⭐", "note": "通用执行器·多人格协同"},
}


# ═══════════════════════════════════════════════════════════════
# 二、经验库（jsonl · append-only · 滚动裁剪）
# ═══════════════════════════════════════════════════════════════

def _persona_file(persona: str) -> Path:
    return EXPERIENCE_DIR / f"{persona}.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def exp_add(persona: str, text: str, domain: str = "", result: str = "🟢") -> Dict[str, Any]:
    """沉淀一条经验。result: 🟢成功/🟡待核/🔴教训"""
    record = {
        "ts": _now(),
        "persona": persona,
        "domain": domain,
        "text": text.strip()[:500],
        "result": result,
        "dna": f"#龍芯⚡️PERSONA-EXP-{persona}",
    }
    path = _persona_file(persona)
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    # 滚动裁剪：保留最近 MAX 条
    if len(lines) + 1 > MAX_EXPERIENCE_PER_PERSONA:
        keep = lines[-(MAX_EXPERIENCE_PER_PERSONA - 1):] + [json.dumps(record, ensure_ascii=False)]
        path.write_text("\n".join(keep) + "\n", encoding="utf-8")
    return record


def exp_list(persona: str, limit: int = 20) -> List[Dict[str, Any]]:
    path = _persona_file(persona)
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out[-limit:]


def exp_inject(persona: str, task: str, limit: int = MAX_EXPERIENCE_INJECT) -> List[Dict[str, Any]]:
    """触发前注入：按关键词相关度取 top-N 经验"""
    recs = exp_list(persona, limit=500)
    if not recs:
        return []
    task_tokens = set(re.findall(r"[\u4e00-\u9fa5]{2,}|[A-Za-z]{3,}", task.lower()))
    def score(r: Dict[str, Any]) -> int:
        s = 0
        for tok in re.findall(r"[\u4e00-\u9fa5]{2,}|[A-Za-z]{3,}", (r.get("text", "") + r.get("domain", "")).lower()):
            if tok in task_tokens:
                s += 2
        if r.get("domain") and r["domain"] in task:
            s += 3
        if r.get("result") == "🔴":
            s += 1  # 教训优先提醒
        return s
    ranked = sorted(recs, key=score, reverse=True)
    return [r for r in ranked if score(r) > 0][:limit]


def exp_status() -> Dict[str, Any]:
    stats = {}
    total = 0
    for p in sorted(PERSONA_PROFILE):
        recs = exp_list(p, limit=100000)
        good = sum(1 for r in recs if r.get("result") == "🟢")
        warn = sum(1 for r in recs if r.get("result") == "🟡")
        bad = sum(1 for r in recs if r.get("result") == "🔴")
        stats[p] = {"name": PERSONA_PROFILE[p]["name"], "total": len(recs), "🟢": good, "🟡": warn, "🔴": bad}
        total += len(recs)
    return {"total_experience": total, "personas": stats}


# ═══════════════════════════════════════════════════════════════
# 三、按任务触发路由（关键词加权 · 毫秒级 · 不调 LLM）
# ═══════════════════════════════════════════════════════════════

def route(task: str) -> Dict[str, Any]:
    """任务 → 能力域 → 人格（含技能+经验注入）。"""
    text = task.lower()
    hits: List[Dict[str, Any]] = []
    for dom in CAPABILITY_DOMAINS:
        weight = 0
        matched = []
        for kw in dom.keywords:
            if kw.lower() in text:
                weight += 1
                matched.append(kw)
        if weight > 0:
            hits.append({
                "domain": dom.domain,
                "desc": dom.desc,
                "weight": weight,
                "matched": matched,
                "personas": dom.personas,
                "skills": dom.skills,
            })
    hits.sort(key=lambda h: h["weight"], reverse=True)

    if not hits:
        return {
            "task": task,
            "verdict": "UNKNOWN",
            "domains": [],
            "personas": [{"persona": "X0", "name": "龙魂执行器", "weight": 10, "reason": "未匹配能力域·默认总控路由"}],
            "skills": ["longhun-orchestrator", "longhun-search"],
            "experience": [],
            "top_domain": "默认路由",
        }

    top = hits[0]
    # 合并同人格权重（跨域同人格去重）
    persona_weights: Dict[str, int] = defaultdict(int)
    persona_domains: Dict[str, List[str]] = defaultdict(list)
    for h in hits:
        for p, w in h["personas"]:
            persona_weights[p] += w * h["weight"]  # 域权重 × 人格权重
            persona_domains[p].append(h["domain"])
    ranked = sorted(persona_weights.items(), key=lambda kv: kv[1], reverse=True)
    persona_list = [
        {
            "persona": p,
            "name": PERSONA_PROFILE.get(p, {}).get("name", p),
            "weight": w,
            "reason": "能力域: " + " + ".join(persona_domains[p]),
        }
        for p, w in ranked[:3]
    ]
    # 技能合并（主域技能 + 次域技能）
    skills: List[str] = []
    for h in hits[:3]:
        for s in h["skills"]:
            if s not in skills:
                skills.append(s)
    # 经验注入（对 top 人格）
    exp_top = exp_inject(persona_list[0]["persona"], task) if persona_list else []

    return {
        "task": task,
        "verdict": "ROUTED",
        "domains": [{"domain": h["domain"], "weight": h["weight"], "matched": h["matched"]} for h in hits[:3]],
        "personas": persona_list,
        "skills": skills[:8],
        "experience": exp_top,
        "top_domain": top["domain"],
    }


# ═══════════════════════════════════════════════════════════════
# 四、输出与主入口
# ═══════════════════════════════════════════════════════════════

def _log_route(task: str, result: Dict[str, Any]) -> None:
    try:
        with ROUTE_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"ts": _now(), "task": task[:200], "top": result.get("top_domain", ""),
                                "personas": [p["persona"] for p in result.get("personas", [])]},
                               ensure_ascii=False) + "\n")
    except OSError:
        pass


def cmd_route(task: str) -> int:
    result = route(task)
    _log_route(task, result)
    print(f"🎯 任务: {result['task']}")
    print(f"┌─ 判定: {'🔀 ROUTED' if result['verdict'] == 'ROUTED' else '❓ UNKNOWN'} · 主域: {result['top_domain']}")
    if result["verdict"] == "ROUTED":
        for d in result["domains"]:
            print(f"│ 域[{d['weight']}] {d['domain']} ← 命中: {', '.join(d['matched'][:5])}")
    print(f"│ 触发人格(按权重):")
    for p in result["personas"]:
        print(f"│   {p['persona']} {p['name']} (w={p['weight']}) · {p['reason']}")
    print(f"│ 挂载技能: {', '.join(result['skills'])}")
    exp = result.get("experience", [])
    if exp:
        print(f"│ 📚 注入经验 {len(exp)} 条（越练越聪明）:")
        for e in exp[:3]:
            print(f"│   · [{e.get('result','?')}] {e.get('text','')[:60]}")
    else:
        print(f"│ 📚 注入经验: 0（此任务类型首跑·完成后记得 --exp add 沉淀）")
    print("└────────")
    return 0


def cmd_exp(args: argparse.Namespace) -> int:
    persona = args.persona.upper()
    if persona not in PERSONA_PROFILE:
        print(f"❌ 未知人格 {persona}。可用: {', '.join(sorted(PERSONA_PROFILE))}")
        return 1
    if args.exp == "add":
        if not args.text:
            print("❌ 需要 --text 经验文本")
            return 1
        rec = exp_add(persona, args.text, domain=args.domain or "manual", result=args.result)
        print(f"✅ {persona} {PERSONA_PROFILE[persona]['name']} 经验已沉淀 [{rec['result']}] {rec['text'][:60]}")
        return 0
    if args.exp == "list":
        recs = exp_list(persona, limit=args.limit)
        if not recs:
            print(f"📭 {persona} {PERSONA_PROFILE[persona]['name']} 暂无经验（完成一次任务后 --exp add 沉淀）")
            return 0
        print(f"📚 {persona} {PERSONA_PROFILE[persona]['name']} 最近 {len(recs)} 条经验:")
        for i, r in enumerate(recs, 1):
            print(f"  {i:2}. [{r.get('result','?')}] {r.get('ts','')[:19]} | {r.get('text','')[:70]}")
        return 0
    print("❌ 未知动作（add/list）")
    return 1


def cmd_status() -> int:
    st = exp_status()
    print(f"🧬 人格经验总览 · 总经验 {st['total_experience']} 条")
    print(f"{'人格':<6}{'姓名':<10}{'条数':>5}{'🟢':>5}{'🟡':>5}{'🔴':>5}")
    for p, s in st["personas"].items():
        print(f"{p:<6}{s['name']:<10}{s['total']:>5}{s['🟢']:>5}{s['🟡']:>5}{s['🔴']:>5}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂 · 人格按任务触发 + 经验累积引擎 v1.0", add_help=False)
    parser.add_argument("--help", "-h", action="store_true", help="帮助")
    parser.add_argument("--route", nargs="?", const="__STDIN__", help="按任务路由（不接参数则读 stdin）")
    parser.add_argument("--exp", choices=["add", "list"], help="经验操作")
    parser.add_argument("--persona", default="P04", help="经验操作目标人格")
    parser.add_argument("--text", help="经验文本（add 用）")
    parser.add_argument("--domain", help="经验所属能力域")
    parser.add_argument("--result", choices=["🟢", "🟡", "🔴"], default="🟢", help="经验结果标记")
    parser.add_argument("--limit", type=int, default=20, help="list 条数")
    parser.add_argument("--status", action="store_true", help="全人格经验统计")
    parser.add_argument("--tag", "--version", action="store_true", help="版本")
    args, remaining = parser.parse_known_args()

    if args.help or args.tag:
        print(__doc__)
        return 0

    if args.status:
        return cmd_status()

    if args.exp:
        return cmd_exp(args)

    # 路由：--route 或裸任务文本
    task = ""
    if args.route and args.route != "__STDIN__":
        task = args.route
    elif args.route == "__STDIN__":
        task = sys.stdin.read().strip()
    elif remaining:
        task = " ".join(remaining)
    if not task:
        print("❌ 需要任务文本（例: lh evolve '帮我写篇文章'）")
        return 1
    return cmd_route(task)


if __name__ == "__main__":
    sys.exit(main())
