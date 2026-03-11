#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·iOS桥接引擎 v1.0
DNA: #龍芯⚡️2026-03-07-IOS-BRIDGE-☴巽-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能: 读取本地 memory.jsonl → 生成 cnsh_status.json → 写入 iCloud Drive
Widget 通过 iCloud 容器读取此文件，实现 Mac ↔ iPhone 数据桥接
"""

import json
import datetime
import hashlib
import os
from pathlib import Path

# ─── 路径 ────────────────────────────────────────────────
BASE       = Path.home() / "longhun-system"
MEMORY     = BASE / "memory.jsonl"
SKILL_IDX  = BASE / "skill-index.json"
KNOW_DB    = BASE / "knowledge-db.jsonl"

# iCloud Drive 容器路径 (iOS App 的 iCloud 文档目录)
# Bundle ID: com.uid9622.longhun  →  iCloud 目录名: iCloud~com~uid9622~longhun
ICLOUD_DIR = Path.home() / "Library" / "Mobile Documents" / "iCloud~com~uid9622~longhun" / "Documents"
OUTPUT_FILE = ICLOUD_DIR / "cnsh_status.json"

# 备用路径：iCloud Drive 通用目录
ICLOUD_FALLBACK = Path.home() / "Library" / "CloudStorage" / "iCloudDrive" / "龙魂系统"

# ─── 卦象映射 ────────────────────────────────────────────
def _检测卦象(dna: str, event: str) -> tuple:
    """从DNA和事件文字推断当前卦象"""
    文本 = (dna + event).lower()
    if any(w in 文本 for w in ["brain", "sync", "巽", "notion", "同步"]):
        return ("☴", "巽", "协同", 0.07)
    elif any(w in 文本 for w in ["crawl", "know", "absorb", "坎", "技术", "代码", "api"]):
        return ("☵", "坎", "技术", 0.20)
    elif any(w in 文本 for w in ["star", "memory", "backup", "坤", "归档", "存储"]):
        return ("☷", "坤", "架构", 0.15)
    elif any(w in 文本 for w in ["dragon", "对话", "震", "进化", "ollama"]):
        return ("☳", "震", "进化", 0.10)
    elif any(w in 文本 for w in ["离", "创新", "ui", "设计", "发布"]):
        return ("☲", "离", "创新", 0.08)
    elif any(w in 文本 for w in ["兑", "量子", "交互", "对话"]):
        return ("☱", "兑", "量子", 0.05)
    elif any(w in 文本 for w in ["strategy", "决策", "战略", "乾", "哲学"]):
        return ("☰", "乾", "战略", 0.35)
    else:
        return ("☰", "乾", "北辰", 0.35)

def _检测人格(dna: str, event: str) -> tuple:
    """推断当前活跃人格"""
    文本 = (dna + event).lower()
    if "p01" in 文本 or "诸葛" in 文本 or "战略" in 文本:
        return ("P01", "🎯诸葛")
    elif "p02" in 文本 or "宝宝" in 文本 or "执行" in 文本:
        return ("P02", "🐱宝宝")
    elif "p03" in 文本 or "雯雯" in 文本 or "审计" in 文本:
        return ("P03", "📊雯雯")
    elif "p04" in 文本 or "文心" in 文本 or "语义" in 文本:
        return ("P04", "🧠文心")
    elif "p05" in 文本 or "老子" in 文本 or "道" in 文本:
        return ("P05", "☯老子")
    elif "p08" in 文本 or "数据" in 文本 or "分析" in 文本:
        return ("P08", "📈数据大师")
    elif "p10" in 文本 or "侦察" in 文本:
        return ("P10", "🕵侦察兵")
    elif "p11" in 文本 or "上帝之眼" in 文本 or "安全" in 文本:
        return ("P11", "👁上帝之眼")
    else:
        return ("L0", "💎北辰")

def _解析审计色(记录: dict) -> tuple:
    """从记录中提取审计分数和颜色"""
    分数 = 记录.get("score", 记录.get("audit_score", 100))
    颜色标记 = 记录.get("audit", "")
    weight = float(记录.get("weight", 0.8))

    if isinstance(分数, int) and 分数 > 0:
        if 分数 >= 80:
            return (分数, "Green")
        elif 分数 >= 50:
            return (分数, "Yellow")
        else:
            return (分数, "Red")

    # 从weight推断
    推断分 = int(weight * 100)
    if "🟢" in 颜色标记 or 推断分 >= 80:
        return (max(推断分, 85), "Green")
    elif "🟡" in 颜色标记 or 推断分 >= 50:
        return (max(推断分, 60), "Yellow")
    elif "🔴" in 颜色标记:
        return (30, "Red")
    return (88, "Green")

# ─── 主生成逻辑 ──────────────────────────────────────────
def 生成状态文件():
    """读取 memory.jsonl，生成 cnsh_status.json"""

    # 读取最新记录
    最新记录 = {}
    记忆条数 = 0
    if MEMORY.exists():
        行列表 = []
        with open(MEMORY, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    行列表.append(line)
        记忆条数 = len(行列表)
        for line in reversed(行列表):
            try:
                最新记录 = json.loads(line)
                break
            except:
                continue

    # 系统统计
    知识节点 = 0
    if KNOW_DB.exists():
        with open(KNOW_DB, "r", encoding="utf-8") as f:
            知识节点 = sum(1 for _ in f)

    技能域 = 0
    if SKILL_IDX.exists():
        with open(SKILL_IDX, "r", encoding="utf-8") as f:
            idx = json.load(f)
        技能域 = len([d for d, v in idx.get("domains", {}).items() if v])

    # 解析字段
    dna   = 最新记录.get("dna", "")
    event = 最新记录.get("event", "系统待机")
    ts    = 最新记录.get("timestamp", datetime.datetime.now().isoformat())

    gua符号, gua名, gua维度, gua权重 = _检测卦象(dna, event)
    人格编号, 人格名 = _检测人格(dna, event)
    审计分, 审计色 = _解析审计色(最新记录)

    # 检测Ollama状态
    ollama在线 = False
    try:
        import urllib.request
        r = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2)
        模型列表 = json.loads(r.read()).get("models", [])
        ollama在线 = True
        ollama模型数 = len(模型列表)
    except:
        ollama模型数 = 0

    # 构建状态JSON
    今天 = datetime.date.today().isoformat()
    状态 = {
        "_meta": {
            "version": "1.0",
            "dna": f"#龍芯⚡️{今天}-IOS-BRIDGE-☴巽-v1.0",
            "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            "generated_at": datetime.datetime.now().isoformat(),
            "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
        },
        "yuanzi": {
            "gua_symbol": gua符号,
            "gua_name": gua名,
            "gua_dimension": gua维度,
            "gua_weight": gua权重,
            "persona_id": 人格编号,
            "persona_name": 人格名,
            "display": f"{gua符号}{gua名}·{gua维度}"
        },
        "audit": {
            "score": 审计分,
            "color": 审计色,
            "label": "🟢通过" if 审计色 == "Green" else ("🟡待审" if 审计色 == "Yellow" else "🔴熔断")
        },
        "last_event": {
            "summary": event[:50],
            "timestamp": ts[:19],
            "dna_tail": dna[-20:] if dna else ""
        },
        "system": {
            "memory_count": 记忆条数,
            "knowledge_nodes": 知识节点,
            "skill_domains": 技能域,
            "ollama_online": ollama在线,
            "ollama_models": ollama模型数
        },
        "cnsh": {
            "url_scheme": "cnsh://open",
            "status": "ready"
        }
    }

    return 状态

def 写入文件(状态: dict) -> str:
    """写入到 iCloud 容器目录"""
    内容 = json.dumps(状态, ensure_ascii=False, indent=2)

    # 优先写入 iCloud App 容器
    写入路径 = None
    for 候选 in [ICLOUD_DIR, ICLOUD_FALLBACK, BASE]:
        try:
            候选.mkdir(parents=True, exist_ok=True)
            目标 = 候选 / "cnsh_status.json"
            目标.write_text(内容, encoding="utf-8")
            写入路径 = str(目标)
            break
        except Exception as e:
            continue

    if not 写入路径:
        # 兜底写到本地
        本地 = BASE / "cnsh_status.json"
        本地.write_text(内容, encoding="utf-8")
        写入路径 = str(本地)

    return 写入路径

def main():
    print("┌─────────────────────────────────────────┐")
    print("│  龍魂·iOS桥接引擎 v1.0                  │")
    print("│  Mac → iCloud → iPhone Widget           │")
    print("└─────────────────────────────────────────┘")

    状态 = 生成状态文件()
    路径 = 写入文件(状态)

    y = 状态["yuanzi"]
    a = 状态["audit"]
    s = 状态["system"]

    print(f"\n卦象: {y['display']}")
    print(f"人格: {y['persona_name']}")
    print(f"审计: {a['label']} ({a['score']}/100)")
    print(f"记忆: {s['memory_count']} 条")
    print(f"知识: {s['knowledge_nodes']} 节点")
    print(f"Ollama: {'🟢在线' if s['ollama_online'] else '🔴离线'}")
    print(f"\n写入: {路径}")
    print(f"DNA:  {状态['_meta']['dna']}")
    print("三色: 🟢 桥接完成")

if __name__ == "__main__":
    main()
