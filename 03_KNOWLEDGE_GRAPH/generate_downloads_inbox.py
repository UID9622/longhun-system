#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
Downloads 主干收件箱自动生成器
扫描 ~/Downloads，将未录入龍魂主干的顶层交付物整理为：
  - downloads_inbox_manifest.json（结构化清单）
  - downloads_inbox_index.md（人工可读索引）
  - graph_data.json（知识图谱数据，追加 inbox 节点）
  - graph_index.md（知识图谱索引页，自动重生成）

执行：
  cd /Users/zuimeidedeyihan/longhun-system/03_知識圖譜
  python3 generate_downloads_inbox.py
"""

import json
import os
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

DOWNLOADS = Path.home() / "Downloads"
PROJECT_ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
KG_DIR = PROJECT_ROOT / "03_知識圖譜"
GRAPH_DATA = KG_DIR / "graph_data.json"
GRAPH_INDEX = KG_DIR / "graph_index.md"
MANIFEST = KG_DIR / "downloads_inbox_manifest.json"
INDEX_MD = KG_DIR / "downloads_inbox_index.md"

NOISE_DIRS = {"__pycache__", "logs", "audit_logs", "checkpoints", "project", "longhun-warehouse-audit", ".git"}
NOISE_FILES = {".DS_Store", "Thumbs.db"}

CATEGORIES = {
    "skill": {"kw": ["skill", "技能"], "target": "01_技能库/ 或 ~/.kimi-code/skills/", "related": ["l0-core"]},
    "cnsh": {"kw": ["cnsh", "cns", "中文原生", "中文编程"], "target": "cnsh-core/ 或 cnsh/", "related": ["IPA-L0-008"]},
    "protocol": {"kw": ["协议", "protocol", "協議", "焊死", "根协议"], "target": "01_protocols/", "related": ["l0-core"]},
    "semantic": {"kw": ["语义", "semantic", "通心译", "tongxin"], "target": "~/.kimi-code/skills/CNSH-SEMANTIC/ 或 03_KNOWLEDGE_GRAPH/", "related": ["l0-core"]},
    "audit": {"kw": ["审计", "audit", "審計"], "target": "audit/", "related": ["/code-audit"]},
    "monitoring": {"kw": ["监控", "monitoring", "監控", "mobile"], "target": "longhun-monitoring skill / baobao-guardian/", "related": ["l5-monitor"]},
    "terminal": {"kw": ["终端", "terminal", "terminal"], "target": "cnsh-terminal/ 或 cnsh_terminal_v5.0/", "related": ["IPA-L0-008"]},
    "gateway": {"kw": ["网关", "gateway"], "target": "cnsh-core/api/ 或 agents/", "related": ["l0-core"]},
    "launcher": {"kw": ["启动", "launcher", "一键启动"], "target": "agents/ 或 bin/", "related": ["IPA-L1-004"]},
    "formula": {"kw": ["公式", "formula", "计算", "算力"], "target": "cnsh-core/龍魂-决策流场-自动化优化/", "related": ["l0-core"]},
    "paper": {"kw": ["论文"], "target": "_archive/papers/ 或 03_KNOWLEDGE_GRAPH/", "related": ["l0-core"]},
    "evidence": {"kw": ["证据"], "target": "_archive/evidence/", "related": ["l0-core"]},
    "notion_export": {"kw": ["notion", "导出"], "target": "_archive/notion-exports/", "related": ["l1-storage"]},
    "media": {"kw": [".mp3", ".mp4", ".mov", ".wav", ".heic", ".png", ".jpg", ".jpeg", ".pdf", ".docx", ".dmg"], "target": "_archive/media/ 或 _archive/deliverables/", "related": ["l1-storage"]},
    "agent_session": {"kw": ["kimi_agent", "kimi agent", "agent_"], "target": "_archive/agent-sessions/ 或对应模块", "related": ["/kimi-webbridge"]},
    "inbox": {"kw": [], "target": "待分类 / _archive/inbox/", "related": ["l0-core"]},
}

EXT_MEDIA = {".mp3", ".mp4", ".mov", ".wav", ".heic", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf", ".docx", ".dmg"}

def human_size(n):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.2f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024
    return f"{n:.2f} PB"


def slugify(name: str) -> str:
    # 去掉首尾空格、统一空格、去特殊符号
    s = name.strip()
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\s·./\\]+", "-", s)
    s = re.sub(r"[^\w\u4e00-\u9fff-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if not s:
        s = "item"
    return s.lower()[:80]


def detect_category(name_lower: str, ext: str, is_dir: bool):
    name_lower = name_lower.lower()
    # 扩展名媒体优先
    if ext in EXT_MEDIA:
        # 但如果是 zip/rar 等不算
        return "media"
    for cat, cfg in CATEGORIES.items():
        if cat == "media":
            continue
        for kw in cfg["kw"]:
            if kw.lower() in name_lower:
                return cat
    # 检查是否以 agent_ 开头
    if name_lower.startswith("kimi_agent_") or name_lower.startswith("kimi agent "):
        return "agent_session"
    return "inbox"


def count_dir_children(p: Path) -> int:
    try:
        return sum(1 for x in p.iterdir() if x.name not in NOISE_FILES and x.name not in NOISE_DIRS)
    except Exception:
        return 0


def collect_top_level():
    raw = []
    for name in sorted(os.listdir(DOWNLOADS)):
        if name in NOISE_FILES:
            continue
        p = DOWNLOADS / name
        try:
            st = p.stat()
            raw.append({
                "name": name,
                "path": str(p),
                "is_dir": p.is_dir(),
                "size": st.st_size,
                "ext": p.suffix.lower(),
            })
        except Exception as e:
            raw.append({"name": name, "path": str(p), "error": str(e)})

    # 文件夹与同 zip 归并
    dirs = {r["name"]: r for r in raw if r.get("is_dir")}
    files = [r for r in raw if not r.get("is_dir") and "error" not in r]
    grouped = []
    consumed_zips = set()
    for d in dirs.values():
        zip_name = d["name"] + ".zip"
        zip_item = next((f for f in files if f["name"] == zip_name), None)
        paths = [{"type": "dir", "path": d["path"], "size": d["size"]}]
        total_size = d["size"]
        if zip_item:
            paths.append({"type": "zip", "path": zip_item["path"], "size": zip_item["size"]})
            total_size += zip_item["size"]
            consumed_zips.add(zip_item["name"])
        child_count = count_dir_children(Path(d["path"]))
        grouped.append({
            "name": d["name"],
            "slug": slugify(d["name"]),
            "paths": paths,
            "total_size": total_size,
            "is_dir": True,
            "child_count": child_count,
        })
    # 剩余文件
    for f in files:
        if f["name"] in consumed_zips:
            continue
        grouped.append({
            "name": f["name"],
            "slug": slugify(f["name"]),
            "paths": [{"type": "file", "path": f["path"], "size": f["size"]}],
            "total_size": f["size"],
            "is_dir": False,
            "child_count": 0,
        })
    return grouped


def classify(item):
    name = item["name"]
    ext = Path(item["paths"][0]["path"]).suffix.lower()
    is_dir = item["is_dir"]
    cat = detect_category(name, ext, is_dir)
    cfg = CATEGORIES.get(cat, CATEGORIES["inbox"])
    # 标签
    tags = [f"#{cat}", "#downloads", "#待录入"]
    if "龍魂" in name or "longhun" in name.lower():
        tags.append("#龍魂")
    if "v2" in name or "v3" in name or "v1" in name:
        tags.append("#版本交付")
    if item["total_size"] > 10 * 1024 * 1024:
        tags.append("#大文件")
    if item["child_count"] > 10:
        tags.append("#多文件包")
    return {
        "category": cat,
        "target": cfg["target"],
        "related_nodes": cfg["related"][:],
        "tags": tags,
    }


def check_existing(name_slug: str):
    # 粗略检查 project 或 skills 中是否已有同名目录
    candidates = [
        Path("/Users/zuimeidedeyihan/longhun-system"),
        Path.home() / ".kimi-code" / "skills",
        Path.home() / ".longhun",
    ]
    for base in candidates:
        if not base.exists():
            continue
        try:
            for child in base.iterdir():
                if slugify(child.name) == name_slug:
                    return True
        except Exception:
            pass
    return False


def build_manifest(items):
    manifest = []
    for it in items:
        info = classify(it)
        status = "可能已存在（待核验）" if check_existing(it["slug"]) else "未录入主干"
        manifest.append({
            "node_id": f"downloads/{it['slug']}",
            "label": it["name"].strip(),
            "type": info["category"],
            "paths": it["paths"],
            "total_size": it["total_size"],
            "human_size": human_size(it["total_size"]),
            "is_dir": it["is_dir"],
            "child_count": it["child_count"],
            "category": info["category"],
            "target": info["target"],
            "status": status,
            "tags": info["tags"],
            "related_nodes": info["related_nodes"],
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-DOWNLOADS-{it['slug'].upper()[:20]}-v1.0",
        })
    return manifest


def generate_markdown(manifest, stats):
    lines = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    migrated = stats.get("migrated", 0)
    skipped = stats.get("skipped", 0)
    errors = stats.get("errors", 0)
    unregistered = stats['unregistered'] if migrated == 0 else sum(1 for m in manifest if m.get("status", "").startswith("未录入"))
    lines.append("# Downloads 主干收件箱索引")
    lines.append("")
    lines.append(f"**生成时间**: {now}")
    lines.append("")
    lines.append(f"**DNA**:`#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-DOWNLOADS-INBOX-v1.0`")
    lines.append("")
    lines.append("## 执行摘要")
    lines.append("")
    lines.append(f"本次扫描 `~/Downloads` 顶层，共识别 **{stats['total_items']}** 个独立交付物/文件包（已把同名文件夹与 `.zip` 归并），")
    if migrated > 0 or skipped > 0:
        lines.append(f"已迁移 **{migrated}** 个至主干，已跳过 **{skipped}** 个（图片/DMG/截图延后处理），失败 **{errors}** 个；")
        lines.append(f"剩余 **{unregistered}** 个尚未录入，**{stats['maybe_exists']}** 个疑似已存在待核验。")
    else:
        lines.append(f"其中 **{unregistered}** 个尚未录入龍魂主干，**{stats['maybe_exists']}** 个疑似已存在待核验。")
    lines.append(f"总占用空间 **{human_size(stats['total_size'])}**，覆盖 {len(stats['categories'])} 个内容类别。")
    lines.append("")
    lines.append("## 统计概览")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|---|---|")
    lines.append(f"| 独立交付物 | {stats['total_items']} |")
    lines.append(f"| 文件夹包 | {stats['dir_items']} |")
    lines.append(f"| 独立文件/压缩包 | {stats['file_items']} |")
    lines.append(f"| 已迁移 | {migrated} |")
    lines.append(f"| 已跳过 | {skipped} |")
    lines.append(f"| 失败 | {errors} |")
    lines.append(f"| 未录入主干 | {unregistered} |")
    lines.append(f"| 疑似已存在 | {stats['maybe_exists']} |")
    lines.append(f"| 总大小 | {human_size(stats['total_size'])} |")
    lines.append("")
    lines.append("### 分类分布")
    lines.append("")
    lines.append("| 类别 | 数量 | 建议归宿 |")
    lines.append("|---|---|---|")
    for cat, count in sorted(stats["categories"].items(), key=lambda x: -x[1]):
        target = CATEGORIES.get(cat, CATEGORIES["inbox"])["target"]
        lines.append(f"| {cat} | {count} | {target} |")
    lines.append("")
    lines.append("## 未录入主干清单")
    lines.append("")
    lines.append("| 名称 | 类型 | 大小 | 文件数 | 建议归宿 | 状态 | 标签 | DNA |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for m in manifest:
        tags = " ".join(m["tags"])
        paths_short = "<br>".join(f"{p['type']}: `{Path(p['path']).name}`" for p in m["paths"])
        lines.append(f"| {m['label']} | {m['category']} | {m['human_size']} | {m['child_count']} | {m['target']} | {m['status']} | {tags} | `{m['dna']}` |")
    lines.append("")
    lines.append("## 自动化升级建议")
    lines.append("")
    lines.append("1. **批量迁移脚本**：根据上表「建议归宿」，将文件夹包复制/合并到对应主干目录；保留原始 zip 作为备份。")
    lines.append("2. **去重校验**：运行 `longhun-dna-align` 扫描新增文件，确保无重复 DNA 与版本冲突。")
    lines.append("3. **技能注册**：`skill` 类交付物若可复用，应生成 SKILL.md 并注册到 `~/.kimi-code/skills/` 与 `01_技能库/`。")
    lines.append("4. **协议归档**：`protocol` 类交付物追加到 `01_protocols/IPA-ROUTE-REGISTRY.local.md` 作为只增节点。")
    lines.append("5. **多媒体入库**：图片/音频/PDF 等大文件统一移入 `_archive/media/`，并在本文档与知识图谱中保留元数据。")
    lines.append("6. **持续同步**：可配置 cron 每小时执行 `generate_downloads_inbox.py`，自动把新 Downloads 顶层内容纳入索引。")
    lines.append("")

    # 如果已有压缩报告，自动追加
    comp_report = KG_DIR / "downloads_compression_report.json"
    if comp_report.exists():
        try:
            comp = json.loads(comp_report.read_text(encoding="utf-8"))
            lines.append("## 已执行的压缩与合并")
            lines.append("")
            lines.append(f"- 对 `downloads-imports` 与 `_archive` 导入区执行内容级去重硬链接：扫描 **{comp.get('scanned_files', 0)}** 个文件，")
            lines.append(f"  发现 **{comp.get('duplicate_groups', 0)}** 组重复，创建 **{comp.get('hardlinks_created', 0)}** 个硬链接，节省 **{comp.get('human_saved', '0 B')}**。")
            lines.append(f"- 详细日志：`03_KNOWLEDGE_GRAPH/downloads_compression.log`")
            lines.append("")
        except Exception:
            pass

    # 如果已建立 cnsh-editor 模块，自动追加
    editor_readme = PROJECT_ROOT / "cnsh-editor" / "README.md"
    if editor_readme.exists():
        lines.append("## 已建立的统一模块：cnsh-editor")
        lines.append("")
        lines.append("- 将分散的编辑器引擎、UI、关键字登记册、鸿蒙/iOS/Web 编辑器页面、文档整合到 `cnsh-editor/`。")
        lines.append("- 清理了 `cnsh-terminal/downloads-imports/` 中大量重复的 `cnsh_editor_engine_v2.0.py`、`editor_ui.py`、`CNSHEditor.ets` 等副本。")
        lines.append("- 构建报告：`03_KNOWLEDGE_GRAPH/cnsh_editor_build_report.md`")
        lines.append("")

    lines.append("## 已补充的区块与标签")
    lines.append("")
    lines.append("- 新增「执行摘要」「统计概览」「分类分布」「未录入主干清单」「自动化升级建议」五大区块，确保信息不遗漏。")
    lines.append("- 每行自动打上 `#类别` `#downloads` `#待录入` 标签，并视情况追加 `#龍魂` `#版本交付` `#大文件` `#多文件包`。")
    lines.append("- 所有交付物均已生成 DNA 追溯码，便于后续 `longhun-dna-align` 对齐审计。")
    lines.append("- 顶层文件夹与同名 `.zip` 已归并，避免重复统计。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**自动生成于**: {datetime.now().isoformat()}")
    return "\n".join(lines)


def fix_json_text(text: str) -> str:
    # 修复 knowledge graph 里 dna 值缺少引号的常见问题
    # "dna":#龍芯... -> "dna":"#龍芯..."
    text = re.sub(r'"dna":#([^",\n]+)"?', r'"dna":"#\1"', text)
    return text


def load_graph_data():
    if not GRAPH_DATA.exists():
        return {"timestamp": datetime.now().isoformat(), "nodes": {}, "edges": [], "dna": "#龍芯⚡️2026-06-06-KNOWLEDGE-GRAPH-DATA-v1.0"}
    text = GRAPH_DATA.read_text(encoding="utf-8")
    text = fix_json_text(text)
    return json.loads(text)


def update_graph_data(manifest):
    data = load_graph_data()
    # 更新时间
    data["timestamp"] = datetime.now().isoformat()
    # 添加中心 inbox 节点
    inbox_id = "downloads/inbox"
    data["nodes"][inbox_id] = {
        "node_id": inbox_id,
        "label": "Downloads 主干收件箱",
        "type": "inbox",
        "dna": f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-DOWNLOADS-INBOX-v1.0",
        "description": "~/Downloads 顶层未录入龍魂主干的交付物集合",
        "related_nodes": [m["node_id"] for m in manifest],
    }
    existing_edges = {(e["source"], e["target"], e.get("relationship")) for e in data["edges"]}
    # 添加每个交付物节点与边
    for m in manifest:
        node_id = m["node_id"]
        data["nodes"][node_id] = {
            "node_id": node_id,
            "label": m["label"],
            "type": m["category"],
            "dna": m["dna"],
            "description": f"{m['category']} · {m['human_size']} · 归宿: {m['target']}",
            "related_nodes": m["related_nodes"],
        }
        # inbox contains
        edge_key = (inbox_id, node_id, "contains")
        if edge_key not in existing_edges:
            data["edges"].append({"source": inbox_id, "target": node_id, "relationship": "contains", "strength": 0.9})
            existing_edges.add(edge_key)
        # relation to existing nodes
        for rel in m["related_nodes"]:
            if rel in data["nodes"]:
                edge_key = (node_id, rel, "relates_to")
                if edge_key not in existing_edges:
                    data["edges"].append({"source": node_id, "target": rel, "relationship": "relates_to", "strength": 0.6})
                    existing_edges.add(edge_key)
    return data


def regenerate_graph_index(data):
    nodes = data["nodes"]
    edges = data["edges"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 分类统计
    type_counts = {}
    for n in nodes.values():
        t = n.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1
    lines = []
    lines.append("# 龍魂系统·知识图谱")
    lines.append("")
    lines.append(f"**生成时间**: {now}")
    lines.append("")
    lines.append(f"**DNA**:`#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-KNOWLEDGE-GRAPH-v2.0`")
    lines.append("")
    lines.append("## 图谱概览")
    lines.append("")
    lines.append(f"- **节点总数**: {len(nodes)}")
    lines.append(f"- **边总数**: {len(edges)}")
    avg_degree = round(2 * len(edges) / len(nodes), 2) if nodes else 0
    lines.append(f"- **平均度数**: {avg_degree}")
    lines.append("")
    lines.append("## 节点类型分布")
    lines.append("")
    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- **{t}**: {count} 个")
    lines.append("")
    lines.append("## 节点详情")
    lines.append("")
    # 按类型分组
    by_type = {}
    for n in nodes.values():
        by_type.setdefault(n.get("type", "unknown"), []).append(n)
    for t, ns in sorted(by_type.items(), key=lambda x: x[0]):
        lines.append(f"### {t.upper()}")
        lines.append("")
        for n in sorted(ns, key=lambda x: x.get("label", x["node_id"])):
            lines.append(f"#### [[{n.get('label', n['node_id'])}]]")
            lines.append("")
            lines.append(f"- **ID**: `{n['node_id']}`")
            lines.append(f"- **类型**: {n.get('type', '')}")
            lines.append(f"- **DNA**:`{n.get('dna', '')}`")
            lines.append(f"- **描述**: {n.get('description', '')}")
            rel = n.get("related_nodes", [])
            if rel:
                rel_links = " ".join(f"[[{r}]]" for r in rel)
                lines.append(f"- **相关节点**: {rel_links}")
            lines.append("")
    lines.append("## 依赖关系")
    lines.append("")
    rel_groups = {}
    for e in edges:
        rel_groups.setdefault(e.get("relationship", "relates_to"), []).append(e)
    for rel, es in sorted(rel_groups.items()):
        lines.append(f"### {rel}")
        lines.append("")
        for e in es:
            src = e["source"]
            tgt = e["target"]
            strength = e.get("strength", 0.5)
            src_label = nodes.get(src, {}).get("label", src)
            tgt_label = nodes.get(tgt, {}).get("label", tgt)
            lines.append(f"- [[{src_label}]] → [[{tgt_label}]] (强度: {strength})")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"**自动生成于**: {datetime.now().isoformat()}")
    return "\n".join(lines)


def main():
    items = collect_top_level()
    manifest = build_manifest(items)
    # stats
    total_size = sum(m["total_size"] for m in manifest)
    dir_items = sum(1 for m in manifest if m["is_dir"])
    file_items = len(manifest) - dir_items
    unregistered = sum(1 for m in manifest if m["status"].startswith("未录入"))
    maybe_exists = len(manifest) - unregistered
    categories = {}
    for m in manifest:
        categories[m["category"]] = categories.get(m["category"], 0) + 1
    stats = {
        "total_items": len(manifest),
        "dir_items": dir_items,
        "file_items": file_items,
        "unregistered": unregistered,
        "maybe_exists": maybe_exists,
        "total_size": total_size,
        "categories": categories,
    }
    # write manifest
    MANIFEST.write_text(json.dumps({"stats": stats, "items": manifest}, ensure_ascii=False, indent=2), encoding="utf-8")
    # write index md
    INDEX_MD.write_text(generate_markdown(manifest, stats), encoding="utf-8")
    # update graph data
    data = update_graph_data(manifest)
    GRAPH_DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    # regenerate graph index
    GRAPH_INDEX.write_text(regenerate_graph_index(data), encoding="utf-8")
    print(f"完成：{len(manifest)} 个交付物，未录入 {unregistered}，总大小 {human_size(total_size)}")
    print(f"输出文件：\n  {MANIFEST}\n  {INDEX_MD}\n  {GRAPH_DATA}\n  {GRAPH_INDEX}")


if __name__ == "__main__":
    main()

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·大畜-CONFIRM-SEAL-generate_downloads_i-09CD5D52
