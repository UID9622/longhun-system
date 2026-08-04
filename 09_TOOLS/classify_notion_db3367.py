#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · Notion DB3367 批量四分分类器 v1.0

把知识库条目自动归类为：
  已落地  → 本地已有实现或可调用模块
  有代码  → 偏工程实现，值得优先写成代码/模块
  纯概念  → 偏理论理解，先建索引
  待淘汰  → 空标题、占位符、重复、无价值

用法：
  python3 classify_notion_db3367.py

DNA: #龍芯⚡️2026-07-05-LONGHUN-NOTION-DB3367-CLASSIFY-v1.0
"""
from __future__ import annotations

import json
import os
import re
import datetime
from pathlib import Path
from typing import List, Any

HOME = Path.home()
LONGHUN_ROOT = Path(os.environ.get("LONGHUN_ROOT", HOME / "longhun-system"))
INDEX_PATH = LONGHUN_ROOT / "docs" / "notion_mirror" / "db_3367_knowledge_index.json"
OUT_JSON = LONGHUN_ROOT / "docs" / "notion_mirror" / "db_3367_classification.json"
OUT_MD = LONGHUN_ROOT / "docs" / "notion_mirror" / "db_3367_classification.md"
MANIFEST_PATH = LONGHUN_ROOT / "outputs" / "manifest.json"

DNA = "#龍芯⚡️2026-07-05-LONGHUN-NOTION-DB3367-CLASSIFY-v1.1"


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()


def normalize(text: str) -> str:
    """移除 emoji、特殊符号、版本号，保留中英文字符"""
    text = re.sub(r"[\u4e00-\u9fff]", lambda m: m.group(0), text)  # 保留中文
    text = re.sub(r"[^\u4e00-\u9fff\w\s]", " ", text)
    text = re.sub(r"\bv\d+(\.\d+)*\b", "", text, flags=re.I)
    text = re.sub(r"\b\d+\b", "", text)
    return text.lower().strip()


def extract_tokens(title: str) -> List[str]:
    """提取有意义的词/字串"""
    norm = normalize(title)
    # 中文按字切，过滤短词；英文按空格切
    tokens = set()
    for w in norm.split():
        if len(w) >= 2:
            tokens.add(w)
    # 中文连续 2-4 字也作为 token
    norm_no_space = norm.replace(" ", "")
    for L in (4, 3, 2):
        for i in range(len(norm_no_space) - L + 1):
            t = norm_no_space[i:i + L]
            if any(c.isalpha() or '\u4e00' <= c <= '\u9fff' for c in t):
                tokens.add(t)
    return [t for t in tokens if t not in STOP_TOKENS]


STOP_TOKENS = {
    "the", "and", "for", "with", "from", "this", "that", "基于", "的", "与", "和",
    "一个", "以及", "介绍", "概述", "详解", "入门", "基础", "原理", "概念",
}

# 标题里出现这些文件后缀，通常说明已有本地实现
LANDING_FILE_EXT = re.compile(r"\b\w+\.(py|sh|js|swift|html|go|rs|c|cpp|h)\b", re.I)

IMPL_KEYWORDS = {
    "算法", "引擎", "系统", "工具", "模块", "服务器", "代理", "优化器", "网络",
    "模型", "库", "运行时", "解析器", "编译器", "协议", "网关", "可视化", "渲染",
    "模拟", "压缩", "加密", "审计", "评分", "识别", "路由", "存储", "同步器",
    "生成器", "框架", "平台", "驱动", "集成", "数据库", "接口", "服务", "函数",
    "脚本", "命令", "守护", "监控", "面板", "工作台", "连接器", "同步", "导出",
    "导入", "部署", "pipeline", "sdk", "api", "cli", "gui", "ui", "bot", "agent",
    "automation", "workflow", "extension", "plugin", "adapter", "server",
    "engine", "framework", "library", "tool", "module", "runtime", "parser",
}

CONCEPT_KEYWORDS = {
    "概念", "原理", "理论", "定理", "变换", "方法", "几何", "信息论", "量子",
    "傅里叶", "采样", "数值", "优化", "回归", "聚类", "分类", "神经网络",
    "贝叶斯", "梯度", "熵", "微分", "积分", "方程", "矩阵", "向量", "概率",
    "统计", "分布", "假设", "检验", "空间", "坐标", "拓扑", "图论", "数论",
    "线性", "非线性", "离散", "连续", "确定性", "随机", "马尔可夫", "蒙特卡洛",
    "attention", "transformer", "gan", "cnn", "rnn", "lstm", "bert", "gpt",
    "diffusion", "svm", "k-means", "k-nn", "pca", "mlp", "xgboost",
    "光线追踪", "光栅化", "全局光照", "pbr", "lod", "抗锯齿", "材质", "贴图",
}

PLACEHOLDER_PATTERNS = [
    r"^\s*$",
    r"在这里写",
    r"填入",
    r"未命名",
    r"无标题",
    r"untitled",
    r"todo",
    r"占位",
    r"^\[?\]?$",
    r"^\(?\)?$",
]


def classify(entry: dict[str, Any]) -> str:
    title = entry.get("title", "") or ""
    status = entry.get("status") or ""
    tags = set(entry.get("tags") or [])
    norm = normalize(title)

    # 待淘汰
    if any(re.search(p, title, re.I) for p in PLACEHOLDER_PATTERNS):
        return "待淘汰"
    if len(title.strip()) <= 1:
        return "待淘汰"

    # 已落地：状态已接入 或 标题里直接带代码文件后缀
    if status == "✅ 已接入":
        return "已落地"
    if LANDING_FILE_EXT.search(title):
        return "已落地"

    # 有代码：接入中 / 含技术落地标签 / 标题含工程关键词
    if status == "🔧 接入中":
        return "有代码"
    if "技术落地" in tags:
        return "有代码"
    if any(kw in norm for kw in IMPL_KEYWORDS):
        return "有代码"

    # 纯概念：概念理解/架构推演标签 或 标题偏理论
    if tags & {"概念理解", "架构推演"}:
        return "纯概念"
    if any(kw in norm for kw in CONCEPT_KEYWORDS):
        return "纯概念"

    # 默认纯概念
    return "纯概念"


def update_manifest_entry(manifest: list[Any], path: str, topic: str, dna: str):
    """按 file_path 更新已有条目，避免重复追加"""
    for m in manifest:
        if m.get("file_path") == path:
            m["dna"] = dna
            m["topic"] = topic
            m["created_at"] = now_iso()
            return
    manifest.append({
        "dna": dna,
        "content_type": "classification_report" if path.endswith(".md") else "classification_data",
        "topic": topic,
        "file_path": path,
        "created_at": now_iso(),
    })


def main():
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    entries = data["entries"]

    groups = {"已落地": [], "有代码": [], "纯概念": [], "待淘汰": []}
    for e in entries:
        cat = classify(e)
        e["lh_category"] = cat
        groups[cat].append(e)

    # 写回索引
    INDEX_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 生成报告
    lines = []
    lines.append("# Notion DB3367 四分分类报告")
    lines.append("")
    lines.append(f"- **DNA：** `{DNA}`")
    lines.append(f"- **总条目：** {len(entries)}")
    lines.append(f"- **生成时间：** {now_iso()}")
    lines.append("")
    lines.append("## 分类统计")
    for cat in ["已落地", "有代码", "纯概念", "待淘汰"]:
        c = len(groups[cat])
        pct = round(c / len(entries) * 100, 1)
        lines.append(f"- **{cat}**：{c} 条（{pct}%）")
    lines.append("")

    for cat in ["已落地", "有代码", "纯概念", "待淘汰"]:
        lines.append(f"## {cat}（{len(groups[cat])} 条）")
        lines.append("")
        if not groups[cat]:
            lines.append("- 无")
        for e in groups[cat]:
            st = e.get("status") or "-"
            tags = "、".join(e.get("tags") or ["-"])
            lines.append(f"- [{e['title']}]({e['url']}) · status={st} · tags={tags}")
        lines.append("")

    lines.append("## 分类规则")
    lines.append("")
    lines.append("1. **待淘汰**：空标题、占位符、长度 ≤1 的条目。")
    lines.append("2. **已落地**：Notion 状态为 ✅ 已接入；或标题里直接出现 `.py/.sh/.js/.swift` 等代码文件后缀。")
    lines.append("3. **有代码**：接入中状态；或标签含「技术落地」；或标题含算法/引擎/系统/工具/模块/优化器/网络/可视化等工程关键词。")
    lines.append("4. **纯概念**：标签含「概念理解」/「架构推演」；或标题偏理论/模型/定理/方法/几何/统计等，无明确工程实现标识。")
    lines.append("")
    lines.append("## 使用说明")
    lines.append("")
    lines.append("- 本分类为自动推断，老大可手动调整 `docs/notion_mirror/db_3367_knowledge_index.json` 中的 `lh_category` 字段。")
    lines.append("- 调整后可重新生成本报告：`python3 tools/classify_notion_db3367.py`")
    lines.append("")
    lines.append(f"---\n**签章：** `{DNA}` · UID9622")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    classification_data = {
        "dna": DNA,
        "generated_at": now_iso(),
        "total": len(entries),
        "counts": {cat: len(groups[cat]) for cat in groups},
        "entries": [
            {
                "page_id": e["page_id"],
                "title": e["title"],
                "url": e["url"],
                "status": e.get("status") or "",
                "lh_category": e["lh_category"],
            }
            for e in entries
        ],
    }
    OUT_JSON.write_text(json.dumps(classification_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 更新 manifest（按 file_path 去重更新）
    if MANIFEST_PATH.exists():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        update_manifest_entry(
            manifest,
            str(OUT_MD),
            "Notion DB3367 四分分类报告（已落地/有代码/纯概念/待淘汰）",
            DNA,
        )
        update_manifest_entry(
            manifest,
            str(OUT_JSON),
            "Notion DB3367 四分分类数据",
            DNA + "-JSON",
        )
        MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"manifest updated, total entries: {len(manifest)}")

    print(f"classification complete: {dict((k, len(v)) for k, v in groups.items())}")
    print(f"report: {OUT_MD}")
    print(f"data:   {OUT_JSON}")


if __name__ == "__main__":
    main()
