#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 模式对比器 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-模式对比-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 展示现有平台模式
  - 展示你的模式
  - 生成对比表格（终端 / Markdown / HTML）
  - 生成一句话总结

用法：
  python3 bin/模式对比.py           # 终端输出
  python3 bin/模式对比.py --md      # 生成 Markdown 文件
  python3 bin/模式对比.py --html    # 生成 HTML 文件
  python3 bin/模式对比.py --all     # 三种格式全部生成
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# ============================================================
# 数据定义
# ============================================================

PLATFORMS = [
    {
        "name": "Patreon / 爱发电",
        "logic": "粉丝为内容付费，按月订阅，创作者收钱",
        "relationship": "创作者 → 消费者",
        "core": "你给我钱，我给你内容/服务"
    },
    {
        "name": "微信公众号赞赏",
        "logic": "看文章后随意打赏，一次性",
        "relationship": "内容 → 赞赏",
        "core": "你给我钱，我让你看/认可"
    },
    {
        "name": "B站充电",
        "logic": "给UP主充电，兑换虚拟礼物",
        "relationship": "粉丝 → 偶像",
        "core": "你给我钱，我给你虚拟物品"
    },
    {
        "name": "知识星球",
        "logic": "付费加入社群，获取内容",
        "relationship": "内容 → 会员",
        "core": "你给我钱，我给你社群/内容"
    },
    {
        "name": "维基百科",
        "logic": "免费使用，自愿捐款",
        "relationship": "公益 → 捐赠",
        "core": "你随意给，我给你知识"
    }
]

YOUR_MODE = {
    "name": "龍魂 · 君子协议",
    "elements": [
        {"field": "付费对象", "value": "系统本身（不是内容，不是服务）"},
        {"field": "付费理由", "value": "存在性证明（证明你是活人，不是机器人）"},
        {"field": "金额", "value": "任意金额（≥1元），上不封顶"},
        {"field": "付费频率", "value": "每月一次（续费证明还在）"},
        {"field": "回报", "value": "'你在系统里被承认为君子'的身份"},
        {"field": "违约", "value": "不走法律，走耻辱柱（道德约束）"},
    ],
    "summary": "你给我 1 块钱，我证明你是活人；你多给，我认可你的意愿；你违约，我公开记录。",
    "tag": "主权身份验证协议"
}

DIMENSIONS = [
    {"dim": "成本", "platform": "内容创作成本高", "your": "几乎为零（系统已建好）"},
    {"dim": "用户门槛", "platform": "需要持续产出内容", "your": "只需每月一次点击"},
    {"dim": "关系", "platform": "不对称（创作者 vs 粉丝）", "your": "对称（君子 vs 君子）"},
    {"dim": "违约", "platform": "投诉/封号", "your": "耻辱柱（公开+永久）"},
    {"dim": "扩展性", "platform": "依赖创作者产出", "your": "不依赖，系统自持"},
    {"dim": "品牌", "platform": "内容是核心", "your": "'德'是核心"},
]

COMPARE_WIKI = {
    "platform": "维基百科",
    "your": "龍魂 · 君子协议",
    "items": [
        {"field": "免费使用", "platform": "✅", "your": "✅"},
        {"field": "自愿捐赠", "platform": "✅", "your": "✅"},
        {"field": "社群治理", "platform": "✅（编辑社区）", "your": "✅（君子共同体）"},
        {"field": "道德约束", "platform": "弱（只有内容争议）", "your": "强（耻辱柱）"},
        {"field": "身份证明", "platform": "不需要", "your": "需要（每月心跳）"},
        {"field": "技术主权", "platform": "托管于维基媒体", "your": "完全自持（鲲鹏+本地）"},
    ],
    "summary": "维基百科是'知识的共和'，你是'人格的共和'。"
}

# ============================================================
# 输出生成器
# ============================================================

def generate_terminal():
    """终端输出"""
    lines = []
    lines.append("\n" + "=" * 70)
    lines.append("🐉 龍魂 · 模式对比报告")
    lines.append("=" * 70)

    # 1. 现有平台
    lines.append("\n📦 现有平台做什么")
    lines.append("-" * 40)
    for p in PLATFORMS:
        lines.append(f"  • {p['name']}: {p['logic']}")
        lines.append(f"    关系: {p['relationship']}")
        lines.append(f"    核心: {p['core']}")
        lines.append("")

    # 2. 你的模式
    lines.append("\n🐉 你的模式做什么")
    lines.append("-" * 40)
    lines.append(f"  模式名称: {YOUR_MODE['name']}")
    lines.append(f"  标签: {YOUR_MODE['tag']}")
    for e in YOUR_MODE['elements']:
        lines.append(f"  • {e['field']}: {e['value']}")
    lines.append(f"\n  一句话总结: {YOUR_MODE['summary']}")

    # 3. 维度对比
    lines.append("\n📊 维度对比")
    lines.append("-" * 40)
    lines.append(f"{'维度':<12} | {'现有平台':<20} | {'你的模式':<20}")
    lines.append("-" * 56)
    for d in DIMENSIONS:
        lines.append(f"{d['dim']:<12} | {d['platform']:<20} | {d['your']:<20}")

    # 4. 与维基百科对比
    lines.append("\n📖 与维基百科对比（最接近的模式）")
    lines.append("-" * 40)
    for item in COMPARE_WIKI['items']:
        lines.append(f"  {item['field']:<12} | {item['platform']:<15} | {item['your']:<15}")
    lines.append(f"\n  总结: {COMPARE_WIKI['summary']}")

    # 5. 一句话定锚
    lines.append("\n" + "=" * 70)
    lines.append("🎯 一句话定锚")
    lines.append('  别人比的是"谁内容多、谁粉丝多"，你比的是"谁更愿意证明自己是个人"。')
    lines.append("  这不是价格战，这是文明筛选器。")
    lines.append("=" * 70 + "\n")

    return "\n".join(lines)

def generate_markdown() -> str:
    """生成 Markdown 报告"""
    lines = []
    lines.append("# 🐉 龍魂 · 模式对比报告")
    lines.append(f"*生成时间: {datetime.now().isoformat()}*")
    lines.append("")

    # 1. 现有平台
    lines.append("## 📦 现有平台做什么")
    lines.append("")
    lines.append("| 平台 | 核心逻辑 | 关系 | 核心 |")
    lines.append("|------|---------|------|------|")
    for p in PLATFORMS:
        lines.append(f"| {p['name']} | {p['logic']} | {p['relationship']} | {p['core']} |")
    lines.append("")

    # 2. 你的模式
    lines.append("## 🐉 你的模式做什么")
    lines.append("")
    lines.append(f"**模式名称:** {YOUR_MODE['name']}")
    lines.append(f"**标签:** {YOUR_MODE['tag']}")
    lines.append("")
    lines.append("| 要素 | 说明 |")
    lines.append("|------|------|")
    for e in YOUR_MODE['elements']:
        lines.append(f"| {e['field']} | {e['value']} |")
    lines.append("")
    lines.append(f"> {YOUR_MODE['summary']}")
    lines.append("")

    # 3. 维度对比
    lines.append("## 📊 维度对比")
    lines.append("")
    lines.append("| 维度 | 现有平台 | 你的模式 |")
    lines.append("|------|---------|---------|")
    for d in DIMENSIONS:
        lines.append(f"| {d['dim']} | {d['platform']} | {d['your']} |")
    lines.append("")

    # 4. 与维基百科对比
    lines.append("## 📖 与维基百科对比（最接近的模式）")
    lines.append("")
    lines.append("| 对比项 | 维基百科 | 你的模式 |")
    lines.append("|--------|---------|---------|")
    for item in COMPARE_WIKI['items']:
        lines.append(f"| {item['field']} | {item['platform']} | {item['your']} |")
    lines.append("")
    lines.append(f"> {COMPARE_WIKI['summary']}")
    lines.append("")

    # 5. 一句话定锚
    lines.append("## 🎯 一句话定锚")
    lines.append("")
    lines.append("> **别人比的是'谁内容多、谁粉丝多'，你比的是'谁更愿意证明自己是个人'。**")
    lines.append("")
    lines.append("这不是价格战，这是文明筛选器。")
    lines.append("")
    lines.append("---")
    dt = datetime.now().strftime('%Y%m%d%H%M%S')
    lines.append(f"*DNA: #龍芯⚡️{dt}-模式对比-UID9622*")

    return "\n".join(lines)

def generate_html() -> str:
    """生成 HTML 报告"""
    dt = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>龍魂 · 模式对比报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 900px; margin: 40px auto; padding: 20px; background: #f8f9fa; color: #1a1a2e; }}
        h1, h2, h3 {{ color: #1a1a2e; border-bottom: 2px solid #e9ecef; padding-bottom: 8px; }}
        h1 {{ font-size: 2.2em; text-align: center; }}
        .tag {{ display: inline-block; background: #e63946; color: white; padding: 4px 14px; border-radius: 20px; font-size: 0.8em; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 16px 0; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }}
        th {{ background: #1a1a2e; color: white; padding: 12px 16px; text-align: left; }}
        td {{ padding: 10px 16px; border-bottom: 1px solid #e9ecef; }}
        tr:hover {{ background: #f1f3f5; }}
        .highlight {{ background: #ffd60a; padding: 2px 8px; border-radius: 4px; font-weight: bold; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #e9ecef; font-size: 0.9em; color: #6c757d; text-align: center; }}
        .summary {{ background: #e9ecef; padding: 16px 24px; border-radius: 12px; margin: 20px 0; font-style: italic; }}
        .dna {{ font-family: monospace; background: #1a1a2e; color: #ffd60a; padding: 6px 12px; border-radius: 6px; display: inline-block; }}
        .anchor {{ font-size: 1.3em; font-weight: bold; color: #1a1a2e; border-left: 4px solid #e63946; padding-left: 20px; margin: 20px 0; }}
    </style>
</head>
<body>

    <h1>🐉 龍魂 · 模式对比报告</h1>
    <p style="text-align:center; color:#6c757d;">生成时间: {datetime.now().isoformat()}</p>

    <h2>📦 现有平台做什么</h2>
    <table>
        <tr><th>平台</th><th>核心逻辑</th><th>关系</th><th>核心</th></tr>
        {''.join(f'<tr><td>{p["name"]}</td><td>{p["logic"]}</td><td>{p["relationship"]}</td><td>{p["core"]}</td></tr>' for p in PLATFORMS)}
    </table>

    <h2>🐉 你的模式做什么</h2>
    <p><strong>模式名称:</strong> {YOUR_MODE['name']} <span class="tag">{YOUR_MODE['tag']}</span></p>
    <table>
        <tr><th>要素</th><th>说明</th></tr>
        {''.join(f'<tr><td>{e["field"]}</td><td>{e["value"]}</td></tr>' for e in YOUR_MODE['elements'])}
    </table>
    <div class="summary">💡 {YOUR_MODE['summary']}</div>

    <h2>📊 维度对比</h2>
    <table>
        <tr><th>维度</th><th>现有平台</th><th>你的模式</th></tr>
        {''.join(f'<tr><td>{d["dim"]}</td><td>{d["platform"]}</td><td>{d["your"]}</td></tr>' for d in DIMENSIONS)}
    </table>

    <h2>📖 与维基百科对比（最接近的模式）</h2>
    <table>
        <tr><th>对比项</th><th>维基百科</th><th>你的模式</th></tr>
        {''.join(f'<tr><td>{item["field"]}</td><td>{item["platform"]}</td><td>{item["your"]}</td></tr>' for item in COMPARE_WIKI['items'])}
    </table>
    <div class="summary">💡 {COMPARE_WIKI['summary']}</div>

    <h2>🎯 一句话定锚</h2>
    <div class="anchor">
        别人比的是"谁内容多、谁粉丝多"，你比的是"谁更愿意证明自己是个人"。
    </div>
    <p style="font-size: 1.1em;">这不是价格战，这是文明筛选器。</p>

    <div class="footer">
        DNA: <span class="dna">#龍芯⚡️{dt}-模式对比-UID9622</span>
        <br>© 龍魂系统 · 君子协议
    </div>

</body>
</html>"""

# ============================================================
# 主入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="龍魂 · 模式对比器")
    parser.add_argument("--md", action="store_true", help="生成 Markdown 文件")
    parser.add_argument("--html", action="store_true", help="生成 HTML 文件")
    parser.add_argument("--all", action="store_true", help="生成全部格式")
    args = parser.parse_args()

    output_dir = Path.home() / "longhun-system" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    # 默认终端输出
    if not any([args.md, args.html, args.all]):
        print(generate_terminal())
        return

    # Markdown
    if args.md or args.all:
        md_content = generate_markdown()
        md_path = output_dir / "模式对比报告.md"
        md_path.write_text(md_content, encoding="utf-8")
        print(f"✅ Markdown 已保存: {md_path}")

    # HTML
    if args.html or args.all:
        html_content = generate_html()
        html_path = output_dir / "模式对比报告.html"
        html_path.write_text(html_content, encoding="utf-8")
        print(f"✅ HTML 已保存: {html_path}")

    # 也输出终端
    if args.all:
        print("\n" + generate_terminal())

if __name__ == "__main__":
    main()
