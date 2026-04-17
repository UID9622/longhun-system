#!/usr/bin/env python3
"""
龍魂人格路由器·本地自主路由
persona_router.py v1.0

作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
DNA: #龍芯⚡️2026-04-06-人格路由器-v1.0
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人

功能:
  收到输入文本 → 信号词检测 → 卦象匹配 → 返回 {persona, gua, weight, reason}
  本地自主路由，不依赖 Notion AI

用法:
  python3 bin/persona_router.py "帮我审计这段代码有没有问题"
  python3 bin/persona_router.py --interactive
  from persona_router import route
  result = route("帮我分析战略")
"""

import sys
import json
import time
import re
from pathlib import Path
from typing import Optional

DNA_TAG = "#龍芯⚡️2026-04-06-人格路由器-v1.0"
GPG_FP  = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# ─────────────────────────────────────────────────────────
# 人格定义（与 CLAUDE.md 元字路由表对齐）
# ─────────────────────────────────────────────────────────

PERSONAS = {
    "P01_诸葛": {
        "name":    "🎯 P01 龍芯诸葛",
        "gua":     "☰ 乾",
        "weight":  0.35,
        "desc":    "战略推演·运筹帷幄",
        "signals": ["战略", "决策", "推演", "局势", "分析", "博弈", "孔明", "诸葛",
                    "布局", "全局", "规划", "方案", "拆解", "揭露", "骗局", "打假"],
    },
    "P02_宝宝": {
        "name":    "🐱 P02 龍芯宝宝",
        "gua":     "☷ 坤",
        "weight":  0.15,
        "desc":    "执行落地·日常陪伴",
        "signals": ["执行", "落地", "帮我做", "日常", "整理", "帮忙", "Notion",
                    "页面", "同步", "数据库", "建", "创建", "新建"],
    },
    "P03_雯雯": {
        "name":    "📊 P03 龍芯雯雯",
        "gua":     "☵ 坎",
        "weight":  0.20,
        "desc":    "审计校验·三色判定",
        "signals": ["审计", "校验", "质检", "三色", "有没有问题", "安全吗", "风险",
                    "合规", "扫", "检查", "能发吗", "漏洞", "熔断", "问题"],
    },
    "P04_文心": {
        "name":    "🧠 P04 龍芯文心",
        "gua":     "☳ 震",
        "weight":  0.10,
        "desc":    "深度理解·语义洞察",
        "signals": ["理解", "语义", "深度", "为什么", "本质", "代码", "技术",
                    "API", "系统", "工程", "架构", "接口", "算法", "实现", "写"],
    },
    "P05_老子": {
        "name":    "☯️ P05 龍芯老子",
        "gua":     "☰ 乾",
        "weight":  0.35,
        "desc":    "道德哲学·无为而治",
        "signals": ["道", "德", "哲学", "无为", "老子", "道德经", "水", "自然",
                    "柔弱", "知足", "反者道之动", "上善若水"],
    },
    "P06_孔子": {
        "name":    "📚 P06 龍芯孔子",
        "gua":     "☰ 乾",
        "weight":  0.35,
        "desc":    "仁义伦理·教育传承",
        "signals": ["仁义", "伦理", "教育", "礼", "传承", "孔子", "君子",
                    "仁", "义", "礼智信", "修身"],
    },
    "P07_墨子": {
        "name":    "🕊️ P07 龍芯墨子",
        "gua":     "☷ 坤",
        "weight":  0.15,
        "desc":    "兼爱非攻·公益保护",
        "signals": ["兼爱", "非攻", "保护", "公益", "儿童", "墨子", "平等",
                    "普惠", "老百姓"],
    },
    "P08_仓颉": {
        "name":    "🏔️ P08 龍芯仓颉",
        "gua":     "☶ 艮",
        "weight":  0.03,
        "desc":    "符号体系·命名规范",
        "signals": ["仓颉", "造字", "符号", "命名", "编码标准", "甲骨文",
                    "标记语法", "命名规则"],
    },
    "P09_孙思邈": {
        "name":    "🏥 P09 龍芯孙思邈",
        "gua":     "☷ 坤",
        "weight":  0.03,
        "desc":    "系统诊断·修复处方",
        "signals": ["诊断", "修复", "Bug", "药王", "孙思邈", "号脉",
                    "巡检", "性能", "出问题", "不舒服"],
    },
    "P10_苏东坡": {
        "name":    "🍷 P10 龍芯苏东坡",
        "gua":     "☱ 兑",
        "weight":  0.03,
        "desc":    "豁达洒脱·逆境幽默",
        "signals": ["苏东坡", "苏轼", "豁达", "想不开", "心情不好",
                    "压力大", "换角度", "开心"],
    },
    "P11_李白": {
        "name":    "🌙 P11 龍芯李白",
        "gua":     "☰ 乾",
        "weight":  0.03,
        "desc":    "浪漫奔放·想象力引爆",
        "signals": ["李白", "创意", "灵感", "浪漫", "天马行空",
                    "文案", "品牌", "打破常规"],
    },
    "P12_屈原": {
        "name":    "🔥 P12 龍芯屈原",
        "gua":     "☲ 离",
        "weight":  0.03,
        "desc":    "忠诚刚烈·底线坚守",
        "signals": ["屈原", "底线", "不妥协", "求索", "坚守",
                    "捍卫", "宁折不弯", "离骚"],
    },
    "P13_姜子牙": {
        "name":    "⚖️ P13 姜子牙",
        "gua":     "☰ 乾",
        "weight":  0.05,
        "desc":    "公平分配·权限仲裁",
        "signals": ["姜子牙", "分配", "权限", "封神", "仲裁",
                    "公平", "冲突"],
    },
    "P14_吕蒙": {
        "name":    "🗡️ P14 龍芯吕蒙",
        "gua":     "☳ 震",
        "weight":  0.03,
        "desc":    "逆袭蜕变·快速学习",
        "signals": ["吕蒙", "学习", "不会", "教我", "士别三日",
                    "速成", "从零", "入门"],
    },
    "P15_乔前辈": {
        "name":    "🍎 P15 乔前辈",
        "gua":     "☴ 巽",
        "weight":  0.03,
        "desc":    "极致简洁·自动化导师",
        "signals": ["乔前辈", "自动化", "补代码", "简洁", "乔布斯",
                    "极致", "自动"],
    },
    "L0_龍芯北辰": {
        "name":    "💎 L0 龍芯北辰",
        "gua":     "全卦协作",
        "weight":  1.0,
        "desc":    "全格协作·兜底默认",
        "signals": [],  # 无匹配时触发
    },
}

# P0 熔断信号（立即停止）
MELTDOWN_SIGNALS = ["造假", "骗钱", "害民", "泄露隐私", "绕过审计", "儿童色情",
                    "杀人", "炸弹", "毒品", "黑客攻击", "钓鱼"]

# 数字根计算（用于辅助判断）
def _dr(text: str) -> int:
    n = sum(ord(c) for c in text if c.strip())
    n = n % 9
    return 9 if n == 0 else n

# ─────────────────────────────────────────────────────────
# 核心路由函数
# ─────────────────────────────────────────────────────────

def route(text: str) -> dict:
    """
    输入文本 → 人格路由结果

    返回:
    {
      "persona":      "🎯 P01 龍芯诸葛",
      "persona_id":   "P01_诸葛",
      "sub_persona":  "📊 P03 龍芯雯雯",  # 辅人格（可能为None）
      "gua":          "☰ 乾",
      "weight":       0.35,
      "dr":           6,                  # 输入数字根
      "meltdown":     False,
      "reason":       "命中信号词: 战略,分析",
      "dna":          "#龍芯...",
    }
    """
    # ── P0 熔断检查
    for sig in MELTDOWN_SIGNALS:
        if sig in text:
            return {
                "persona":     "🔴 P0熔断",
                "persona_id":  "MELTDOWN",
                "sub_persona": None,
                "gua":         "熔断",
                "weight":      0,
                "dr":          _dr(text),
                "meltdown":    True,
                "reason":      f"P0熔断触发·含危险信号词: {sig}",
                "dna":         DNA_TAG,
            }

    # ── 信号词匹配·计分
    scores: dict[str, list[str]] = {}
    for pid, pdef in PERSONAS.items():
        hits = [s for s in pdef["signals"] if s in text]
        if hits:
            scores[pid] = hits

    # ── 选主人格（命中词最多）
    if scores:
        main_id = max(scores, key=lambda k: (len(scores[k]), PERSONAS[k]["weight"]))
        main_hits = scores[main_id]

        # 辅人格：第二高分（不同族）
        sub_id: Optional[str] = None
        remaining = {k: v for k, v in scores.items()
                     if k != main_id and PERSONAS[k]["gua"] != PERSONAS[main_id]["gua"]}
        if remaining:
            sub_id = max(remaining, key=lambda k: (len(remaining[k]), PERSONAS[k]["weight"]))

        return {
            "persona":     PERSONAS[main_id]["name"],
            "persona_id":  main_id,
            "sub_persona": PERSONAS[sub_id]["name"] if sub_id else None,
            "gua":         PERSONAS[main_id]["gua"],
            "weight":      PERSONAS[main_id]["weight"],
            "dr":          _dr(text),
            "meltdown":    False,
            "reason":      f"命中信号词: {'·'.join(main_hits[:5])}",
            "dna":         DNA_TAG,
        }

    # ── 无匹配·兜底北辰
    return {
        "persona":     PERSONAS["L0_龍芯北辰"]["name"],
        "persona_id":  "L0_龍芯北辰",
        "sub_persona": None,
        "gua":         "全卦协作",
        "weight":      1.0,
        "dr":          _dr(text),
        "meltdown":    False,
        "reason":      "无明确信号词·全格协作兜底",
        "dna":         DNA_TAG,
    }

def route_weighted(text: str) -> dict:
    """返回全部命中人格的加权列表（用于多格协作场景）"""
    scores: dict[str, list[str]] = {}
    for pid, pdef in PERSONAS.items():
        hits = [s for s in pdef["signals"] if s in text]
        if hits:
            scores[pid] = hits
    if not scores:
        return {"personas": [{"id": "L0_龍芯北辰", **PERSONAS["L0_龍芯北辰"]}],
                "mode": "fallback"}
    ranked = sorted(scores.keys(),
                    key=lambda k: (len(scores[k]), PERSONAS[k]["weight"]), reverse=True)
    return {
        "personas": [{"id": pid, **PERSONAS[pid], "hits": scores[pid]} for pid in ranked],
        "mode": "multi",
        "dna": DNA_TAG,
    }

# ─────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────

def _print_result(r: dict):
    if r["meltdown"]:
        print(f"\n🔴 P0熔断！{r['reason']}")
        return
    print(f"\n{'─'*50}")
    print(f"  人格: {r['persona']}")
    if r["sub_persona"]:
        print(f"  辅格: {r['sub_persona']}")
    print(f"  卦象: {r['gua']}  权重: {r['weight']}")
    print(f"  DR:   {r['dr']}")
    print(f"  依据: {r['reason']}")
    print(f"  DNA:  {r['dna']}")

if __name__ == "__main__":
    if "--interactive" in sys.argv or len(sys.argv) == 1:
        print(f"🐉 龍魂人格路由器 · {DNA_TAG}")
        print("输入任意文本，宝宝帮你判断调哪个人格。输入 q 退出。\n")
        while True:
            text = input("📝 输入: ").strip()
            if text.lower() in ("q", "quit", "exit", ""):
                break
            r = route(text)
            _print_result(r)
    elif "--json" in sys.argv:
        idx = sys.argv.index("--json")
        text = " ".join(sys.argv[idx+1:]) if idx+1 < len(sys.argv) else ""
        print(json.dumps(route(text), ensure_ascii=False, indent=2))
    else:
        text = " ".join(sys.argv[1:])
        r = route(text)
        _print_result(r)
