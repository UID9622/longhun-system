#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂生态 · 开发者学习路径生成器 v1.0
# 层级: L2_工具层
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-LEARNING-PATH-v1.0-UID9622
# 别名: 08_BIN/lh_learning_path.py
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 三色: 🟢 通过
"""

import json
import argparse
import hashlib
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any


DNA = "#龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-LEARNING-PATH-v1.0-UID9622"
UID = "9622"


def generate_dna(suffix: str = "") -> str:
    ts = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    rand = hashlib.sha256(f"{suffix}{ts}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts}-{suffix}-{UID}-{rand}"


KNOWLEDGE_GRAPH: Dict[str, Dict[str, Dict[str, Any]]] = {
    "L0_核心思维": {
        "抽象思维": {"priority": "P0", "estimated_hours": 40, "tags": ["系统分层", "命名即架构"]},
        "算法思维": {"priority": "P0", "estimated_hours": 80, "tags": ["DNA生成器", "哈希算法"]},
        "系统思维": {"priority": "P0", "estimated_hours": 40, "tags": ["16人格矩阵", "蚁群分布式"]},
        "安全思维": {"priority": "P0", "estimated_hours": 60, "tags": ["确认码闸门", "GPG签名"]},
        "逆向思维": {"priority": "P1", "estimated_hours": 40, "tags": ["红蓝对抗", "耻辱墙"]},
        "逻辑思维": {"priority": "P0", "estimated_hours": 30, "tags": ["协议冲突裁决"]},
        "自动化思维": {"priority": "P0", "estimated_hours": 30, "tags": ["脚本工厂", "AI Agent"]},
    },
    "L1_计算机基础": {
        "数据结构与算法": {"priority": "P0", "estimated_hours": 100, "tags": ["哈希表", "链表", "树"]},
        "操作系统原理": {"priority": "P0", "estimated_hours": 60, "tags": ["进程", "内存", "文件系统"]},
        "计算机网络": {"priority": "P0", "estimated_hours": 60, "tags": ["TCP/IP", "HTTP", "TLS"]},
        "数据库原理": {"priority": "P1", "estimated_hours": 40, "tags": ["ACID", "索引", "事务"]},
        "编译原理": {"priority": "P2", "estimated_hours": 40, "tags": ["AST", "词法分析"]},
        "计算机组成原理": {"priority": "P2", "estimated_hours": 40, "tags": ["CPU", "缓存", "指令集"]},
        "离散数学": {"priority": "P1", "estimated_hours": 40, "tags": ["图论", "数理逻辑"]},
        "密码学基础": {"priority": "P0", "estimated_hours": 80, "tags": ["哈希", "签名", "密钥交换"]},
    },
    "L2_系统与网络": {
        "Linux/Unix": {"priority": "P0", "estimated_hours": 60, "tags": ["Shell", "Vim", "进程管理"]},
        "TCP/IP协议栈": {"priority": "P0", "estimated_hours": 40, "tags": ["三次握手", "拥塞控制"]},
        "HTTP/HTTPS": {"priority": "P0", "estimated_hours": 30, "tags": ["REST", "Header", "Cookie"]},
        "DNS/CDN": {"priority": "P1", "estimated_hours": 20, "tags": ["解析", "边缘节点"]},
        "容器Docker": {"priority": "P1", "estimated_hours": 20, "tags": ["镜像", "Dockerfile"]},
        "K8s编排": {"priority": "P2", "estimated_hours": 40, "tags": ["Pod", "Deployment"]},
        "Shell脚本": {"priority": "P0", "estimated_hours": 30, "tags": ["Bash", "AWK", "正则"]},
    },
    "L3_工程与架构": {
        "版本控制Git": {"priority": "P0", "estimated_hours": 20, "tags": ["分支", "Rebase", "Hook"]},
        "CI/CD": {"priority": "P1", "estimated_hours": 20, "tags": ["GitHub Actions", "流水线"]},
        "测试驱动TDD": {"priority": "P1", "estimated_hours": 30, "tags": ["单元测试", "Mock"]},
        "设计模式": {"priority": "P1", "estimated_hours": 40, "tags": ["SOLID", "观察者", "策略"]},
        "监控告警": {"priority": "P1", "estimated_hours": 20, "tags": ["Prometheus", "Grafana"]},
        "安全工程": {"priority": "P0", "estimated_hours": 40, "tags": ["OWASP", "注入", "XSS"]},
        "日志追踪": {"priority": "P0", "estimated_hours": 20, "tags": ["结构化日志", "审计"]},
    },
    "L4_应用与领域": {
        "后端开发": {"priority": "P0", "estimated_hours": 80, "tags": ["Python", "FastAPI", "Flask"]},
        "LLM应用": {"priority": "P0", "estimated_hours": 60, "tags": ["Prompt工程", "RAG", "Agent"]},
        "密码学应用": {"priority": "P0", "estimated_hours": 40, "tags": ["协议设计", "侧信道防护"]},
        "全栈开发": {"priority": "P0", "estimated_hours": 60, "tags": ["前后端", "数据库", "部署"]},
        "爬虫开发": {"priority": "P1", "estimated_hours": 40, "tags": ["requests", "Scrapy", "Playwright"]},
        "前端开发": {"priority": "P2", "estimated_hours": 60, "tags": ["React", "Vue"]},
    },
    "L5_软技能与商业": {
        "技术写作": {"priority": "P0", "estimated_hours": 30, "tags": ["文档", "协议"]},
        "开源社区": {"priority": "P1", "estimated_hours": 20, "tags": ["贡献", "治理"]},
        "产品思维": {"priority": "P1", "estimated_hours": 30, "tags": ["用户场景", "价值主张"]},
        "法律法规": {"priority": "P0", "estimated_hours": 20, "tags": ["个保法", "数据安全法"]},
        "持续学习": {"priority": "P0", "estimated_hours": 20, "tags": ["AI文明", "四季文明"]},
    },
    "L6_自动化与工具": {
        "脚本自动化": {"priority": "P0", "estimated_hours": 30, "tags": ["Python", "Bash", "定时任务"]},
        "爬虫自动化": {"priority": "P1", "estimated_hours": 30, "tags": ["自动抓取", "去重", "入库"]},
        "AI Agent": {"priority": "P0", "estimated_hours": 40, "tags": ["自主规划", "工具调用"]},
        "文档自动化": {"priority": "P1", "estimated_hours": 20, "tags": ["Markdown", "模板渲染"]},
        "测试自动化": {"priority": "P1", "estimated_hours": 20, "tags": ["回归测试", "CI集成"]},
    },
}


def generate_path(focus: str = "龍魂系统", priority_filter: str = None) -> Dict[str, Any]:
    """生成学习路径"""
    total_skills = 0
    total_hours = 0
    p0_hours = 0
    p1_hours = 0
    p2_hours = 0
    p0_count = 0
    p1_count = 0
    p2_count = 0

    filtered_layers = {}
    for layer, skills in KNOWLEDGE_GRAPH.items():
        filtered_skills = {}
        for skill, meta in skills.items():
            if priority_filter and meta["priority"] != priority_filter:
                continue
            filtered_skills[skill] = meta
            total_skills += 1
            total_hours += meta["estimated_hours"]
            if meta["priority"] == "P0":
                p0_hours += meta["estimated_hours"]
                p0_count += 1
            elif meta["priority"] == "P1":
                p1_hours += meta["estimated_hours"]
                p1_count += 1
            elif meta["priority"] == "P2":
                p2_hours += meta["estimated_hours"]
                p2_count += 1
        if filtered_skills:
            filtered_layers[layer] = filtered_skills

    daily_hours = 3  # 假设每天学习 3 小时
    estimated_days = total_hours // daily_hours

    return {
        "dna": generate_dna("LEARNING-PATH"),
        "focus": focus,
        "filter": priority_filter or "all",
        "summary": {
            "total_skills": total_skills,
            "p0_count": p0_count,
            "p1_count": p1_count,
            "p2_count": p2_count,
            "total_hours": total_hours,
            "p0_hours": p0_hours,
            "p1_hours": p1_hours,
            "p2_hours": p2_hours,
            "estimated_days_at_3h_per_day": estimated_days,
        },
        "path": ["L0_核心思维", "L1_计算机基础", "L2_系统与网络", "L3_工程与架构", "L4_应用与领域", "L5_软技能与商业", "L6_自动化与工具"],
        "layers": filtered_layers,
        "recommendation": f"按 P0 优先级学习，约 {p0_hours} 小时可掌握 {focus} 核心技能（每天 3 小时约 {p0_hours // daily_hours} 天）。",
    }


def print_path(path: Dict[str, Any]):
    s = path["summary"]
    print("🐉 龍魂 · 开发者学习路径")
    print(f"DNA: {path['dna']}")
    print(f"焦点: {path['focus']}")
    print(f"过滤: {path['filter']}")
    print("=" * 50)
    print(f"总技能数: {s['total_skills']}（P0 {s['p0_count']} · P1 {s['p1_count']} · P2 {s['p2_count']}）")
    print(f"总时长: {s['total_hours']} 小时（P0 {s['p0_hours']} · P1 {s['p1_hours']} · P2 {s['p2_hours']}）")
    print(f"按每天 3 小时: 约 {s['estimated_days_at_3h_per_day']} 天")
    print("=" * 50)
    print("\n建议学习顺序:")
    for i, layer in enumerate(path["path"], 1):
        skills = path["layers"].get(layer, {})
        if skills:
            hours = sum(m["estimated_hours"] for m in skills.values())
            print(f"  {i}. {layer}（{len(skills)} 项 · {hours} 小时）")
            for skill, meta in skills.items():
                print(f"      - {skill} [{meta['priority']}] {meta['estimated_hours']}h · tags: {', '.join(meta['tags'])}")
    print("\n" + path["recommendation"])


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂开发者学习路径生成器")
    parser.add_argument("--focus", default="龍魂系统", help="学习焦点")
    parser.add_argument("--priority", choices=["P0", "P1", "P2"], help="只显示某优先级")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    path = generate_path(focus=args.focus, priority_filter=args.priority)

    if args.json:
        print(json.dumps(path, ensure_ascii=False, indent=2))
    else:
        print_path(path)


if __name__ == "__main__":
    main()
