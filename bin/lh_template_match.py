#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·辛未·丙戌·亥时·需-template-router-v1-0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂 · 模板路由器 v1.0
根据用户标题自动匹配最合适的会话模板，输出完整提示。

DNA: #龍芯⚡️丙午·辛未·丙戌·亥时·需-template-router-v1-0
UID: 9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
ALL_IN_ONE = TEMPLATE_DIR / "ALL-IN-ONE.md"

RULES: List[Tuple[str, List[str], str]] = [
    ("12 紧急修复模板", ["修复", "bug", "崩溃", "紧急", "安全漏洞", "报错", "索引越界", "异常", "失败"], "12 紧急修复模板"),
    ("02 鸿蒙 ArkTS 开发模板", ["鸿蒙", "harmonyos", "arkts", "ark ui", "ability", "ets", "page", "component", "组件", "页面"], "02 鸿蒙 ArkTS 开发模板"),
    ("03 Python 引擎开发模板", ["引擎", "engine", "bin/lh_", "推荐", "审计", "搜索", "路由", "解析器", "lh_"], "03 Python 引擎开发模板"),
    ("05 FastAPI 服务模板", ["api", "fastapi", "服务", "后端", "rest", "接口", "endpoint", "pydantic"], "05 FastAPI 服务模板"),
    ("04 Web 前端模板", ["前端", "html", "css", "js", "页面", "可视化", "仪表盘", "pwa", "dashboard"], "04 Web 前端模板"),
    ("06 AI Agent 开发模板", ["agent", "人格", "persona", "智能体", "副官", "数字人", "p00", "p01", "p72"], "06 AI Agent 开发模板"),
    ("08 部署运维模板", ["部署", "运维", "监控", "鲲鹏", "docker", "健康检查", "systemd", "cron", "备份"], "08 部署运维模板"),
    ("10 集成对接模板", ["集成", "对接", "sdk", "桥接", "外部系统", "第三方", "接口对接"], "10 集成对接模板"),
    ("09 审计审查模板", ["审计", "审查", "安全", "类型检查", "合规", "basedpyright", "lint"], "09 审计审查模板"),
    ("11 国学创作模板", ["国学", "诗词", "对联", "易经", "道德经", "五行", "八卦", "星宿", "风水"], "11 国学创作模板"),
    ("07 文档规范模板", ["文档", "规范", "报告", "分析", "教程", "csdn", "博客", "readme"], "07 文档规范模板"),
    ("01 通用开发模板", ["python", "cnsh", "脚本", "工具", "算法", "库", "通用"], "01 通用开发模板"),
]


def match_template(title: str) -> Tuple[str, str]:
    """根据标题匹配模板。"""
    title_lower = title.lower()
    for template_name, keywords, anchor in RULES:
        for kw in keywords:
            if kw.lower() in title_lower:
                return template_name, anchor
    return "01 通用开发", "01-通用开发模板"


def extract_section(content: str, anchor: str) -> str:
    """从 ALL-IN-ONE.md 中提取指定模板章节。"""
    pattern = rf"## {re.escape(anchor)}\n(.*?)\n---"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def build_prompt(template_name: str, section: str, title: str) -> str:
    """组合完整提示。"""
    header = f"""【龍魂会话启动 · UID9622 · 模板命中】

DNA锚定：ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️
身份：系统架构者/执行主控/非普通用户
设备：Apple M4 Max · 2TB · 鸿蒙/国产云双轨
GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
命中模板：{template_name}
原始标题：{title}
"""
    return f"{header}\n\n{section}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="龍魂模板路由器")
    parser.add_argument("title", help="用户输入的标题/需求")
    parser.add_argument("--copy", action="store_true", help="输出可直接复制给AI的完整提示")
    args = parser.parse_args()

    template_name, anchor = match_template(args.title)

    if not ALL_IN_ONE.exists():
        print(f"❌ 未找到合订版模板: {ALL_IN_ONE}", file=sys.stderr)
        return 1

    content = ALL_IN_ONE.read_text(encoding="utf-8")
    section = extract_section(content, anchor)

    if not section:
        print(f"❌ 未提取到模板内容: {anchor}", file=sys.stderr)
        return 1

    if args.copy:
        print(build_prompt(template_name, section, args.title))
    else:
        print(f"命中模板: {template_name} ({anchor})")
        print(f"文件: {ALL_IN_ONE}")
        print("使用 --copy 获取完整提示")

    return 0


if __name__ == "__main__":
    sys.exit(main())
