#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
🗂️ 龍魂·剪贴板容器 v1.0
======================
DNA: #龍芯⚡️丙午·丙申·庚申·子时·䷤家人-CLIPBOARD-VAULT-v1.0-P1

把每一次复制/粘贴变成带 DNA 的本地 markdown 文件，按主题归档，
并支持一键进入龍魂知识图谱。

用法:
  from engines.lh_clipboard_vault import save, classify, list_vault, vault_to_kg_json
  save("要保存的内容", source="clipboard")
  save("论文摘要", source="notion", topic="论文", tags=["AI","主权"])

CLI:
  python3 engines/lh_clipboard_vault.py save "内容"
  python3 engines/lh_clipboard_vault.py list
  python3 engines/lh_clipboard_vault.py kg-ready
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "bin"))

import yaml
from ganzhi_dna_engine import DNA生成

CST = timezone(timedelta(hours=8))
DNA_PREFIX = "#龍芯⚡️"

VAULT_ROOT = PROJECT_ROOT / "06_CONTAINERS" / "clipboard-vault"
INBOX_DIR = VAULT_ROOT / "inbox"
BY_TOPIC_DIR = VAULT_ROOT / "by-topic"
KG_PENDING_FILE = VAULT_ROOT / "kg-pending" / "pending.json"

# 简单主题分类规则（关键词命中）
TOPIC_RULES: List[tuple] = [
    ("论文/顶刊", ["论文", "顶刊", "投稿", "Nature", "JMLR", "NeurIPS", "POPL", "IEEE", "AAAI", "IJCAI", "FAccT", "DCC", "TOPLAS", "Minds and Machines"]),
    ("代码/脚本", ["def ", "import ", "class ", "function", "python", "bash", "javascript", "typescript", "dockerfile", "```python", "```js", "```bash"]),
    ("URL/网页", ["http://", "https://", "www.", ".com/", ".cn/", ".net/"]),
    ("命令/CLI", ["git ", "python3 ", "npm ", "pip ", "brew ", "ssh ", "curl ", "lh-"]),
    ("CNSH/龍魂", ["CNSH", "龍魂", "龍芯", "DNA", "三色审计", "通心译", "河图", "洛书", "八卦", "五行"]),
    ("AI/大模型", ["LLM", "GPT", "Kimi", "Claude", "模型", "RAG", "Agent", "prompt", "微调", "训练", "推理"]),
    ("安全/审计", ["审计", "漏洞", "渗透", "GPG", "签名", "加密", "密钥", "熔断", "安全"]),
    ("法律/主权", ["法律", "主权", "数据主权", "隐私", "合规", "宪法", "协议", "专利", "知识产权"]),
    ("产品/设计", ["产品", "设计", "UI", "UX", "用户", "体验", "交互", "原型"]),
    ("民生/社会", ["老百姓", "人民", "社区", "民生", "公益", "服务", "基层"]),
]


def _now_iso() -> str:
    """返回北京时间 ISO 8601 字符串。"""
    return datetime.now(CST).isoformat(timespec="seconds")


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _find_existing_by_hash(content_hash: str) -> Optional[Path]:
    """全局扫描容器，查找相同 content_hash 的 markdown 文件。"""
    for md_file in INBOX_DIR.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        meta = _parse_frontmatter(text)
        if meta and meta.get("content_hash") == content_hash:
            return md_file
    return None


def classify(content: str) -> str:
    """根据关键词自动判断内容主题。"""
    text = content.lower()
    scores: Dict[str, int] = {}
    for topic, keywords in TOPIC_RULES:
        score = sum(1 for kw in keywords if kw.lower() in text)
        if score:
            scores[topic] = score
    if not scores:
        return "未分类"
    return max(scores, key=scores.get)


def _extract_tags(content: str, topic: str) -> List[str]:
    """提取内容标签：命中关键词 + 主题。"""
    text = content.lower()
    tags: List[str] = []
    # 通用技术标签
    tag_keywords = [
        ("python", "Python"), ("javascript", "JS"), ("typescript", "TS"),
        ("bash", "Bash"), ("docker", "Docker"), ("kubernetes", "K8s"),
        ("neo4j", "Neo4j"), ("fastapi", "FastAPI"), ("notion", "Notion"),
        ("cnsg", "CNSH"), ("龍魂", "龍魂"), ("dna", "DNA"),
        ("安全", "安全"), ("审计", "审计"), ("论文", "论文"),
    ]
    for kw, label in tag_keywords:
        if kw in text and label not in tags:
            tags.append(label)
    if topic != "未分类" and topic not in tags:
        tags.append(topic)
    return tags[:8]


def save(
    content: str,
    source: str = "clipboard",
    topic: Optional[str] = None,
    tags: Optional[List[str]] = None,
    parent_dna: Optional[str] = None,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    保存一条剪贴内容到本地容器。

    返回字典包含：dna, path, topic, tags, hash, timestamp
    """
    if not content or not content.strip():
        raise ValueError("内容不能为空")

    text = content.strip()
    auto_topic = topic or classify(text)
    auto_tags = tags or _extract_tags(text, auto_topic)
    content_hash = _sha256(text)

    dna = DNA生成(
        模块="CLIPBOARD",
        动作="VAULT-SAVE",
        版本="V1.0",
        级别="P1",
        内容锚点=text[:64],
    )

    # ═══════════════════════════════════════════════════════════════
    # 全局去重：相同内容只更新元数据，不生成新文件
    # ═══════════════════════════════════════════════════════════════
    existing_file = _find_existing_by_hash(content_hash)
    if existing_file and not dry_run:
        existing_text = existing_file.read_text(encoding="utf-8")
        meta = _parse_frontmatter(existing_text) or {}
        now = _now_iso()

        # 升级旧 frontmatter：补齐 copy_count / updated_at / sources
        sources = meta.get("sources", [])
        if not sources and "source" in meta:
            sources.append({"source": meta["source"], "at": meta.get("timestamp", "")})
        # 追加新来源（如果该来源+近1秒内没有重复）
        if not any(s.get("source") == source for s in sources):
            sources.append({"source": source, "at": now})

        meta["source"] = source  # 最近一次来源
        meta["sources"] = sources
        meta["updated_at"] = now
        meta["copy_count"] = meta.get("copy_count", 1) + 1
        # 如果用户显式指定了 topic/tags，允许更新；否则保持原样
        if topic:
            meta["topic"] = topic
        if tags:
            meta["tags"] = tags

        yaml_front = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
        # 保留 body（剪贴内容 + 底部归档信息）
        body_match = re.search(r"\n---\n\n(.*)$", existing_text, re.S)
        body = body_match.group(1) if body_match else f"# 剪贴内容\n\n{text}\n"
        new_text = f"---\n{yaml_front}---\n\n{body}"
        existing_file.write_text(new_text, encoding="utf-8")

        return {
            "dna": meta.get("dna", dna),
            "path": str(existing_file.relative_to(PROJECT_ROOT)),
            "topic": meta.get("topic", auto_topic),
            "tags": meta.get("tags", auto_tags),
            "hash": content_hash,
            "timestamp": meta.get("timestamp", now),
            "updated_at": now,
            "copy_count": meta.get("copy_count", 1),
            "source": source,
            "status": "dedup",
            "note": "内容已存在，已更新元数据",
        }

    # ═══════════════════════════════════════════════════════════════
    # 新内容：创建 markdown 文件
    # ═══════════════════════════════════════════════════════════════
    date_key = datetime.now(CST).strftime("%Y-%m-%d")
    inbox_date_dir = INBOX_DIR / date_key
    file_stem = f"CLIP-{content_hash[:8]}"
    file_path = inbox_date_dir / f"{file_stem}.md"

    parent_dna_list = [parent_dna] if parent_dna else []
    now = _now_iso()

    frontmatter = {
        "dna": dna,
        "source": source,
        "sources": [{"source": source, "at": now}],
        "topic": auto_topic,
        "tags": auto_tags,
        "timestamp": now,
        "updated_at": now,
        "content_hash": content_hash,
        "copy_count": 1,
        "parent_dna": parent_dna_list,
        "vault_version": "v1.1",
    }

    yaml_front = yaml.safe_dump(frontmatter, allow_unicode=True, sort_keys=False)
    md_body = f"""---
{yaml_front}---

# 剪贴内容

{text}

---

*归档于 {frontmatter['timestamp']} · 更新于 {frontmatter['updated_at']} · DNA `{dna}`*
"""

    if not dry_run:
        inbox_date_dir.mkdir(parents=True, exist_ok=True)
        file_path.write_text(md_body, encoding="utf-8")

        # 同时按主题做软链接/引用索引（不复制文件，只写索引）
        topic_index = BY_TOPIC_DIR / auto_topic
        topic_index.mkdir(parents=True, exist_ok=True)
        (topic_index / f"{file_stem}.ref").write_text(
            str(file_path.relative_to(PROJECT_ROOT)), encoding="utf-8"
        )

    return {
        "dna": dna,
        "path": str(file_path.relative_to(PROJECT_ROOT)) if not dry_run else str(file_path),
        "topic": auto_topic,
        "tags": auto_tags,
        "hash": content_hash,
        "timestamp": now,
        "updated_at": now,
        "copy_count": 1,
        "source": source,
        "status": "saved" if not dry_run else "dry-run",
    }


def _parse_frontmatter(text: str) -> Optional[Dict[str, Any]]:
    """解析 markdown frontmatter，支持 YAML 和 JSON。"""
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return None
    raw = m.group(1)
    try:
        return yaml.safe_load(raw) or {}
    except Exception:
        try:
            return json.loads(raw) or {}
        except Exception:
            return None


def list_vault() -> List[Dict[str, Any]]:
    """列出容器中所有剪贴项。"""
    items: List[Dict[str, Any]] = []
    for md_file in sorted(INBOX_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        meta = _parse_frontmatter(text)
        if meta is None:
            continue
        items.append({
            "path": str(md_file.relative_to(PROJECT_ROOT)),
            "dna": meta.get("dna", ""),
            "source": meta.get("source", ""),
            "sources": meta.get("sources", []),
            "topic": meta.get("topic", "未分类"),
            "tags": meta.get("tags", []),
            "timestamp": meta.get("timestamp", ""),
            "updated_at": meta.get("updated_at", meta.get("timestamp", "")),
            "content_hash": meta.get("content_hash", ""),
            "copy_count": meta.get("copy_count", 1),
        })
    return items


def vault_to_kg_json() -> Dict[str, Any]:
    """把容器内容转换为知识图谱可导入的 JSON。"""
    items = list_vault()
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    topic_ids: Dict[str, str] = {}
    tag_ids: Dict[str, str] = {}

    for item in items:
        clip_id = f"CLIP:{item['content_hash'][:16]}"
        nodes.append({
            "id": clip_id,
            "type": "Clip",
            "label": item["path"].split("/")[-1].replace(".md", ""),
            "props": {
                "dna": item["dna"],
                "source": item["source"],
                "topic": item["topic"],
                "timestamp": item["timestamp"],
                "path": item["path"],
                "hash": item["content_hash"],
            },
        })

        topic = item["topic"]
        if topic not in topic_ids:
            topic_id = f"TOPIC:{hashlib.md5(topic.encode()).hexdigest()[:8]}"
            topic_ids[topic] = topic_id
            nodes.append({"id": topic_id, "type": "Topic", "label": topic})
        edges.append({"from": clip_id, "to": topic_ids[topic], "type": "belongs_to", "label": "属于主题"})

        for tag in item.get("tags", []):
            if tag not in tag_ids:
                tag_id = f"TAG:{hashlib.md5(tag.encode()).hexdigest()[:8]}"
                tag_ids[tag] = tag_id
                nodes.append({"id": tag_id, "type": "Tag", "label": tag})
            edges.append({"from": clip_id, "to": tag_ids[tag], "type": "has_tag", "label": "含标签"})

    return {
        "dna": DNA生成(模块="CLIPBOARD", 动作="VAULT-KG-EXPORT", 版本="V1.0", 级别="P1"),
        "timestamp": _now_iso(),
        "nodes": nodes,
        "edges": edges,
        "count": len(items),
    }


def _main():
    raw_argv = sys.argv[1:]

    # 预处理：把 -- 之后的内容合并为一个 content 参数
    if "--" in raw_argv:
        idx = raw_argv.index("--")
        content_after_dash = " ".join(raw_argv[idx + 1:]).strip()
        raw_argv = raw_argv[:idx]
        if content_after_dash:
            raw_argv.append(content_after_dash)

    # 简单命令解析：第一个位置参数是 save/list/kg-ready 时为子命令，否则默认 save
    command = "save"
    content: Optional[str] = None
    if raw_argv and raw_argv[0] in ("save", "list", "kg-ready"):
        command = raw_argv[0]
        raw_argv = raw_argv[1:]

    parser = argparse.ArgumentParser(description="龍魂·剪贴板容器")
    parser.add_argument("content", nargs="?", help="要保存的内容")
    parser.add_argument("--source", default="clipboard", help="来源标识")
    parser.add_argument("--topic", default=None, help="指定主题")
    parser.add_argument("--tags", default=None, help="逗号分隔标签")
    parser.add_argument("--parent-dna", default=None, help="父DNA")
    parser.add_argument("--dry-run", action="store_true", help="只演示不保存")

    args = parser.parse_args(raw_argv)
    content = args.content

    if command == "save":
        if not content:
            print(json.dumps({"status": "error", "reason": "内容不能为空"}, ensure_ascii=False))
            sys.exit(1)
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
        result = save(
            content,
            source=args.source,
            topic=args.topic,
            tags=tags,
            parent_dna=args.parent_dna,
            dry_run=args.dry_run,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif command == "list":
        items = list_vault()
        print(json.dumps(items, ensure_ascii=False, indent=2))
    elif command == "kg-ready":
        data = vault_to_kg_json()
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _main()
