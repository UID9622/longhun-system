#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
editor_memory_extractor.py
从 macOS 本地 VSCode / Cursor 编辑器中提取记忆与创作，归档到 Longhun 脑库。

用法：
    python3 scripts/editor_memory_extractor.py

输出：
    brain/editor_memory_archive/

DNA: #龍芯⚡️2026-06-29-EDITOR-MEMORY-EXTRACTION-UID9622
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sqlite3
import stat
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# --------------------------------------------------------------------------- #
# 常量与 DNA
# --------------------------------------------------------------------------- #
DNA: str = "#龍芯⚡️2026-06-29-EDITOR-MEMORY-EXTRACTION-UID9622"

HOME: Path = Path.home()

# 源路径（只读，禁止修改）
VSCODE_USER_DIR: Path = HOME / "Library" / "Application Support" / "Code" / "User"
CURSOR_USER_DIR: Path = HOME / "Library" / "Application Support" / "Cursor" / "User"
AGENTS_HOOKS_DIR: Path = HOME / ".agents" / "hooks"

# 归档根目录
LONGHUN_ROOT: Path = HOME / "longhun-system"
ARCHIVE_ROOT: Path = LONGHUN_ROOT / "brain" / "editor_memory_archive"
REPORTS_DIR: Path = ARCHIVE_ROOT / "reports"

# 超大值阈值（字节）
LARGE_VALUE_THRESHOLD: int = 2 * 1024 * 1024

# --------------------------------------------------------------------------- #
# 辅助函数
# --------------------------------------------------------------------------- #


def ensure_dir(path: Path) -> Path:
    """确保目录存在，不存在则创建。"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def normalize_permissions(path: Path) -> None:
    """将归档文件/目录权限设置为当前用户可读写，避免复制到只读源文件后无法再次写入。"""
    try:
        if path.is_dir():
            path.chmod(path.stat().st_mode | stat.S_IRWXU)
        else:
            path.chmod(path.stat().st_mode | stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def safe_read_text(path: Path, default: str = "") -> str:
    """安全读取文本，失败返回默认值。"""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return default


def safe_read_json(path: Path, default: Optional[Any] = None) -> Any:
    """安全读取 JSON，失败返回默认值。"""
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError):
        return default


def dump_json(path: Path, data: Any, indent: int = 2) -> None:
    """将数据以 JSON 格式写入文件，并归一化权限。"""
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent, default=str), encoding="utf-8")
    normalize_permissions(path)


def copy_tree_robust(src: Path, dst: Path, stats: Dict[str, Any], category: str) -> None:
    """递归复制目录树，跳过不存在源，累计统计。"""
    if not src.exists():
        return
    ensure_dir(dst)
    normalize_permissions(dst)

    category_count = 0
    category_bytes = 0

    def _copy_item(s: Path, d: Path) -> None:
        nonlocal category_count, category_bytes
        ensure_dir(d.parent)
        try:
            shutil.copy2(str(s), str(d))
            normalize_permissions(d)
            size = d.stat().st_size
            stats["copied_files"] += 1
            stats["total_bytes"] += size
            category_count += 1
            category_bytes += size
            stats.setdefault("largest_files", []).append((str(d.relative_to(ARCHIVE_ROOT)), size))
        except (OSError, shutil.Error):
            stats["errors"].append(f"copy:{s}")

    for root, dirs, files in os.walk(src):
        root_path = Path(root)
        rel = root_path.relative_to(src)
        cur_dst = dst / rel

        for d in list(dirs):
            dpath = root_path / d
            # 跳过 macOS 资源叉与隐藏废纸篓
            if d == ".DS_Store" or d.startswith("."):
                dirs.remove(d)
                continue
            subdir = ensure_dir(cur_dst / d)
            normalize_permissions(subdir)

        for f in files:
            if f == ".DS_Store":
                continue
            _copy_item(root_path / f, cur_dst / f)

    stats["categories"][category] = {"files": category_count, "bytes": category_bytes}


def readable_strings(blob: bytes, limit: int = 50 * 1024) -> str:
    """从二进制块中提取可打印字符串（近似），用于生成 .txt 摘要。"""
    try:
        text = blob.decode("utf-8", errors="ignore")
    except Exception:
        text = ""
    # 过滤掉过短的随机字节段，保留至少 4 个可打印字符
    chunks = re.findall(r"[\x20-\x7E\u4e00-\u9fff]{4,}", text)
    out = "\n".join(chunks)
    if len(out.encode("utf-8")) > limit:
        out = out.encode("utf-8")[:limit].decode("utf-8", errors="ignore")
    return out


def structural_summary(value: Any) -> Any:
    """对超大 JSON 值生成顶层结构摘要：类型名、数组长度、键列表。"""
    if value is None:
        return None
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return type(value).__name__
    if isinstance(value, str):
        return f"str({len(value)})"
    if isinstance(value, list):
        return {
            "type": "list",
            "length": len(value),
            "items": [structural_summary(v) for v in value[:10]],
        }
    if isinstance(value, dict):
        keys = list(value.keys())
        return {
            "type": "dict",
            "key_count": len(keys),
            "keys": keys[:200],
            "sample": {k: structural_summary(value[k]) for k in keys[:10]},
        }
    return type(value).__name__


# --------------------------------------------------------------------------- #
# SQLite 状态库提取
# --------------------------------------------------------------------------- #


def decode_sqlite_value(raw: Any) -> Tuple[Any, bool]:
    """尝试将 SQLite 值解析为 JSON；失败则返回原始值与 is_raw 标记。"""
    if isinstance(raw, str):
        try:
            return json.loads(raw), False
        except json.JSONDecodeError:
            return raw, True
    if isinstance(raw, (bytes, bytearray)):
        try:
            text = raw.decode("utf-8")
            return json.loads(text), False
        except (UnicodeDecodeError, json.JSONDecodeError):
            try:
                return json.loads(raw.decode("utf-8", errors="replace")), False
            except json.JSONDecodeError:
                return raw, True
    return raw, True


def extract_state_vscdb(
    db_path: Path,
    out_dir: Path,
    important_keys: List[str],
    pattern_keys: List[str],
    stats: Dict[str, Any],
    editor_name: str,
) -> None:
    """提取 state.vscdb（含 ItemTable），保留所有键，重点导出给定键。"""
    if not db_path.exists():
        stats["errors"].append(f"missing:{db_path}")
        return

    ensure_dir(out_dir)
    all_keys: Dict[str, Any] = {}
    extracted_count = 0
    largest_keys: List[Tuple[str, int]] = []

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM ItemTable;")
        for key, value in cursor:
            is_important = key in important_keys or any(re.match(p, key) for p in pattern_keys)
            decoded, is_raw = decode_sqlite_value(value)
            size = len(value)
            largest_keys.append((key, size))

            record: Dict[str, Any] = {
                "key": key,
                "size": size,
                "important": is_important,
                "raw": is_raw,
            }
            if is_raw:
                # 原始字节/字符串存 .bin，摘要存 .json
                bin_path = out_dir / f"{key.replace('/', '__').replace(':', '_')}.bin"
                payload = decoded if isinstance(decoded, (bytes, bytearray)) else str(decoded).encode("utf-8", errors="replace")
                bin_path.write_bytes(payload)
                normalize_permissions(bin_path)
                record["bin_file"] = str(bin_path.name)
            else:
                record["value"] = decoded

            all_keys[key] = record
            extracted_count += 1
        conn.close()
    except sqlite3.Error as e:
        stats["errors"].append(f"sqlite:{db_path}:{e}")
        return

    dump_json(out_dir / "all_item_table_keys.json", all_keys, indent=2)

    # 重点键单独存一份便于人工查看
    important: Dict[str, Any] = {k: v for k, v in all_keys.items() if v.get("important")}
    dump_json(out_dir / "important_keys.json", important, indent=2)

    largest_keys.sort(key=lambda x: x[1], reverse=True)
    stats["sqlite"][editor_name] = {
        "extracted_keys": extracted_count,
        "important_keys": len(important),
        "largest_keys": largest_keys[:20],
        "db_size": db_path.stat().st_size,
    }


# --------------------------------------------------------------------------- #
# Cursor cursorDiskKV 提取
# --------------------------------------------------------------------------- #


def extract_cursor_disk_kv(db_path: Path, out_dir: Path, stats: Dict[str, Any]) -> None:
    """提取 Cursor globalStorage 中的 cursorDiskKV 表，按前缀分类归档。"""
    if not db_path.exists():
        stats["errors"].append(f"missing:{db_path}")
        return

    ensure_dir(out_dir)
    categories = {
        "bubbleId:*": {"count": 0, "total_bytes": 0},
        "checkpointId:*": {"count": 0, "total_bytes": 0},
        "agentKv:blob:*": {"count": 0, "total_bytes": 0},
        "other": {"count": 0, "total_bytes": 0},
    }

    prefix_map = [
        ("bubbleId:*", re.compile(r"^bubbleId:")),
        ("checkpointId:*", re.compile(r"^checkpointId:")),
        ("agentKv:blob:*", re.compile(r"^agentKv:blob:")),
    ]

    def classify(key: str) -> str:
        for cat, pat in prefix_map:
            if pat.match(key):
                return cat
        return "other"

    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        # cursorDiskKV 表结构通常为 (key TEXT PRIMARY KEY, value BLOB)
        cursor.execute("SELECT key, value FROM cursorDiskKV;")
        rows = list(cursor)
        conn.close()
    except sqlite3.Error as e:
        stats["errors"].append(f"sqlite_cursorDiskKV:{db_path}:{e}")
        return

    for key, value in rows:
        category = classify(key)
        categories[category]["count"] += 1
        categories[category]["total_bytes"] += len(value) if value else 0

        safe_name = re.sub(r"[^\w\-]", "_", key)[:120]
        # 用短哈希保证唯一性，避免键名过长导致文件名超限
        short_hash = hashlib.sha256(key.encode("utf-8")).hexdigest()[:8]
        base_path = out_dir / category.replace(":", "_").replace("*", "star") / f"{safe_name}_{short_hash}"
        ensure_dir(base_path.parent)

        if value is None:
            dump_json(base_path.with_suffix(".summary.json"), {
                "key": key, "category": category, "size": 0, "raw": True, "note": "NULL value"
            })
            continue

        decoded, is_raw = decode_sqlite_value(value)
        if is_raw:
            bin_path = base_path.with_suffix(".bin")
            payload = decoded if isinstance(decoded, (bytes, bytearray)) else str(decoded).encode("utf-8", errors="replace")
            bin_path.write_bytes(payload)
            normalize_permissions(bin_path)
            summary = {
                "key": key,
                "category": category,
                "size": len(value),
                "raw": True,
                "bin_file": str(bin_path.relative_to(ARCHIVE_ROOT)),
            }
            dump_json(base_path.with_suffix(".summary.json"), summary)
            continue

        # JSON 值
        size = len(value) if isinstance(value, (bytes, str)) else len(str(value))
        if size > LARGE_VALUE_THRESHOLD:
            # 超大值：完整 pretty-print + 结构摘要 + 可读字符串摘要
            dump_json(base_path.with_suffix(".json"), decoded)
            dump_json(base_path.with_suffix(".summary.json"), {
                "key": key,
                "category": category,
                "size": size,
                "structure": structural_summary(decoded),
            })
            txt_path = base_path.with_suffix(".txt")
            txt_path.write_text(readable_strings(decoded), encoding="utf-8")
            normalize_permissions(txt_path)
        else:
            dump_json(base_path.with_suffix(".json"), decoded)

    stats["cursor_disk_kv"] = {
        "total_keys": len(rows),
        "categories": categories,
    }


# --------------------------------------------------------------------------- #
# Cursor commits / checkpoints 提取
# --------------------------------------------------------------------------- #


def extract_cursor_commits(checkpoints_dir: Path, out_dir: Path, stats: Dict[str, Any]) -> None:
    """解析 Cursor checkpoints 目录，为每个 checkpoint 生成 Markdown 摘要。"""
    if not checkpoints_dir.exists():
        stats["errors"].append(f"missing:{checkpoints_dir}")
        return

    ensure_dir(out_dir)
    checkpoint_count = 0

    for cp_dir in checkpoints_dir.iterdir():
        if not cp_dir.is_dir():
            continue
        cp_id = cp_dir.name
        meta_path = cp_dir / "metadata.json"
        if not meta_path.exists():
            continue

        metadata = safe_read_json(meta_path, {})
        checkpoint_count += 1

        # 收集 diff 文件与其他文件
        diffs: List[Path] = []
        files: List[Path] = []
        for item in cp_dir.rglob("*"):
            if item.is_file():
                if item.name.endswith(".diff") or "diff" in item.name.lower():
                    diffs.append(item)
                elif item.name != "metadata.json":
                    files.append(item)

        changed_files: List[str] = []
        for d in diffs:
            try:
                content = d.read_text(encoding="utf-8", errors="replace")
                # diff 文件头通常包含 --- a/... +++ b/...
                for line in content.splitlines()[:20]:
                    m = re.match(r"^[-+]{3}\s+\w?/(.*)", line)
                    if m:
                        changed_files.append(m.group(1))
            except OSError:
                pass
        changed_files = list(dict.fromkeys(changed_files))  # 去重保序

        created = metadata.get("createdAt") or metadata.get("timestamp") or metadata.get("date")
        message = metadata.get("message") or metadata.get("commitMessage") or metadata.get("description") or ""

        md_lines: List[str] = [
            f"# Checkpoint {cp_id}",
            "",
            f"- **ID**: `{cp_id}`",
            f"- **时间**: {created}",
            f"- **消息**: {message}",
            f"- **元数据文件**: `{meta_path}`",
            "",
            "## 变更文件",
            "",
        ]
        if changed_files:
            for f in changed_files:
                md_lines.append(f"- `{f}`")
        else:
            md_lines.append("- （未从 diff 中识别到文件路径）")

        md_lines.extend([
            "",
            "## 原始元数据",
            "",
            "```json",
            json.dumps(metadata, ensure_ascii=False, indent=2),
            "```",
            "",
            "## 包含的 diff / 文件",
            "",
        ])
        for d in diffs:
            md_lines.append(f"- `{d.relative_to(cp_dir)}`")
        for f in files:
            md_lines.append(f"- `{f.relative_to(cp_dir)}`")

        md_path = out_dir / f"{cp_id}.md"
        md_path.write_text("\n".join(md_lines), encoding="utf-8")
        normalize_permissions(md_path)

        # 同时保留原始 metadata.json
        shutil.copy2(str(meta_path), str(out_dir / f"{cp_id}_metadata.json"))
        normalize_permissions(out_dir / f"{cp_id}_metadata.json")

    stats["cursor_commits"] = {"checkpoint_count": checkpoint_count}


# --------------------------------------------------------------------------- #
# History 目录索引
# --------------------------------------------------------------------------- #


def extract_history(history_src: Path, history_dst: Path, stats: Dict[str, Any], editor_name: str) -> None:
    """复制 History 目录，并为每个 entries.json 建立索引。"""
    if not history_src.exists():
        return

    ensure_dir(history_dst)
    copy_tree_robust(history_src, history_dst, stats, f"{editor_name}_history")

    index: Dict[str, Any] = {}
    for entries_file in history_dst.rglob("entries.json"):
        data = safe_read_json(entries_file, {})
        rel_parent = str(entries_file.parent.relative_to(history_dst))
        entries = data if isinstance(data, list) else data.get("entries", [])
        index[rel_parent] = {
            "entries_file": str(entries_file.relative_to(ARCHIVE_ROOT)),
            "entries": [],
        }
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            eid = entry.get("id")
            resource = entry.get("resource") or entry.get("file") or entry.get("originalPath")
            versions = [str(v.relative_to(ARCHIVE_ROOT)) for v in entries_file.parent.iterdir() if v.is_file() and v.name.startswith(f"{eid}_")]
            index[rel_parent]["entries"].append({
                "id": eid,
                "resource": resource,
                "versions": sorted(versions),
            })

    dump_json(history_dst / "index.json", index, indent=2)
    stats["history"][editor_name] = {"indexed_entries": sum(len(v["entries"]) for v in index.values())}


# --------------------------------------------------------------------------- #
# settings.json 与迁移提示
# --------------------------------------------------------------------------- #


def copy_settings(settings_src: Path, settings_dst: Path, stats: Dict[str, Any], editor_name: str) -> Dict[str, Any]:
    """复制 settings.json，返回解析后的字典。"""
    if not settings_src.exists():
        return {}
    shutil.copy2(str(settings_src), str(settings_dst))
    normalize_permissions(settings_dst)
    size = settings_dst.stat().st_size
    stats["settings"] = {editor_name: {"path": str(settings_dst.relative_to(ARCHIVE_ROOT)), "size": size}}
    return safe_read_json(settings_src, {})


def build_settings_migration_map(vscode_settings: Dict[str, Any], cursor_settings: Dict[str, Any]) -> Dict[str, Any]:
    """根据 VSCode/Cursor 设置生成 Longhun 配置迁移提示。"""
    migration: Dict[str, Any] = {
        "_meta": {
            "dna": DNA,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "description": "编辑器设置 -> Longhun 配置迁移提示",
        },
        "vscode": {},
        "cursor": {},
    }

    # 通用映射规则：键 -> (Longhun 目标, 数据类型)
    rules: Dict[str, Tuple[str, str]] = {
        "cursor.composer.shouldChimeAfterChatFinishes": ("longhun.notifications.after_chat_chime", "bool"),
        "files.autoSave": ("longhun.editor.autosave", "string"),
        "files.autoSaveDelay": ("longhun.editor.autosave_delay_ms", "number"),
        "gitlens.ai.model": ("longhun.ai.model.preference", "string"),
        "chat.hookFilesLocations": ("longhun.hooks.paths", "list"),
        "editor.fontSize": ("longhun.editor.font.size", "number"),
        "editor.fontFamily": ("longhun.editor.font.family", "string"),
        "editor.tabSize": ("longhun.editor.tab_size", "number"),
        "workbench.colorTheme": ("longhun.ui.theme", "string"),
        "terminal.integrated.defaultProfile.osx": ("longhun.terminal.default_profile", "string"),
        "mcp.servers": ("longhun.mcp.servers", "dict"),
        "github.copilot.enable": ("longhun.ai.copilot.enabled", "bool"),
    }

    def apply_rules(source: Dict[str, Any], target: Dict[str, Any]) -> None:
        for key, (longhun_key, dtype) in rules.items():
            if key in source:
                target[longhun_key] = {
                    "source_key": key,
                    "value": source[key],
                    "type": dtype,
                    "action": "migrate",
                }
        # 对任意包含 cursor.composer 前缀的键也做提示
        for key, value in source.items():
            if key.startswith("cursor.composer"):
                target[f"longhun.cursor.{key}"] = {
                    "source_key": key,
                    "value": value,
                    "type": type(value).__name__,
                    "action": "review",
                }

    apply_rules(vscode_settings, migration["vscode"])
    apply_rules(cursor_settings, migration["cursor"])
    return migration


# --------------------------------------------------------------------------- #
# Hooks 吸收
# --------------------------------------------------------------------------- #


def absorb_hooks(src: Path, dst: Path, stats: Dict[str, Any]) -> None:
    """将 .agents/hooks 吸收到归档 hooks/ 子目录。"""
    if not src.exists():
        stats["errors"].append(f"missing:{src}")
        return
    copy_tree_robust(src, dst, stats, "hooks")


# --------------------------------------------------------------------------- #
# 报告生成
# --------------------------------------------------------------------------- #


def build_report(stats: Dict[str, Any]) -> Dict[str, Any]:
    """汇总统计信息并返回报告字典。"""
    report = {
        "dna": DNA,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "archive_root": str(ARCHIVE_ROOT),
        "summary": {
            "copied_files": stats["copied_files"],
            "total_bytes": stats["total_bytes"],
            "errors": stats["errors"],
        },
        "categories": stats["categories"],
        "history": stats["history"],
        "sqlite": stats["sqlite"],
        "cursor_disk_kv": stats.get("cursor_disk_kv", {}),
        "cursor_commits": stats.get("cursor_commits", {}),
        "settings": stats.get("settings", {}),
        "largest_files": sorted(stats.get("largest_files", []), key=lambda x: x[1], reverse=True)[:20],
    }
    return report


def write_markdown_report(report: Dict[str, Any], md_path: Path) -> None:
    """生成 Markdown 版本报告。"""
    lines: List[str] = [
        "# 编辑器记忆提取报告",
        "",
        f"- **DNA**: `{report['dna']}`",
        f"- **生成时间**: {report['generated_at']}",
        f"- **归档根目录**: `{report['archive_root']}`",
        "",
        "## 统计摘要",
        "",
        f"- 复制文件总数: {report['summary']['copied_files']}",
        f"- 总字节数: {report['summary']['total_bytes']:,}",
        f"- 错误数: {len(report['summary']['errors'])}",
        "",
        "## 分类",
        "",
    ]
    for cat, info in report["categories"].items():
        files = info.get("files", 0) if isinstance(info, dict) else info
        bytes_ = info.get("bytes", 0) if isinstance(info, dict) else 0
        lines.append(f"- {cat}: {files} 文件, {bytes_:,} bytes")

    lines.extend(["", "## SQLite 状态库", ""])
    for editor, info in report["sqlite"].items():
        lines.append(f"### {editor}")
        lines.append(f"- 提取键数: {info.get('extracted_keys', 0)}")
        lines.append(f"- 重点键数: {info.get('important_keys', 0)}")
        lines.append(f"- 数据库大小: {info.get('db_size', 0):,} bytes")
        if info.get("largest_keys"):
            lines.append("- 最大键:")
            for key, size in info["largest_keys"][:10]:
                lines.append(f"  - `{key}`: {size:,} bytes")

    cdkv = report.get("cursor_disk_kv", {})
    if cdkv:
        lines.extend(["", "## Cursor Disk KV", ""])
        lines.append(f"- 总键数: {cdkv.get('total_keys', 0)}")
        for cat, info in cdkv.get("categories", {}).items():
            lines.append(f"- {cat}: {info.get('count', 0)} 键, {info.get('total_bytes', 0):,} bytes")

    cp = report.get("cursor_commits", {})
    lines.extend(["", "## Cursor Checkpoints", ""])
    lines.append(f"- Checkpoint 数量: {cp.get('checkpoint_count', 0)}")

    lines.extend(["", "## 最大文件 Top 10", ""])
    for path, size in report["largest_files"][:10]:
        lines.append(f"- `{path}`: {size:,} bytes")

    if report["summary"]["errors"]:
        lines.extend(["", "## 错误", ""])
        for err in report["summary"]["errors"]:
            lines.append(f"- {err}")

    md_path.write_text("\n".join(lines), encoding="utf-8")
    normalize_permissions(md_path)


def write_card(report: Dict[str, Any], card_path: Path) -> None:
    """生成 .card.json 摘要卡片。"""
    card = {
        "title": "编辑器记忆归档",
        "dna": report["dna"],
        "generated_at": report["generated_at"],
        "type": "editor_memory_extraction",
        "stats": {
            "copied_files": report["summary"]["copied_files"],
            "total_bytes": report["summary"]["total_bytes"],
            "cursor_checkpoints": report.get("cursor_commits", {}).get("checkpoint_count", 0),
            "cursor_disk_kv_keys": report.get("cursor_disk_kv", {}).get("total_keys", 0),
        },
        "source_editors": ["vscode", "cursor"],
    }
    dump_json(card_path, card)


# --------------------------------------------------------------------------- #
# 主流程
# --------------------------------------------------------------------------- #


def run_extraction() -> Dict[str, Any]:
    """执行完整的编辑器记忆提取流程。"""
    stats: Dict[str, Any] = {
        "copied_files": 0,
        "total_bytes": 0,
        "errors": [],
        "categories": {},
        "history": {},
        "sqlite": {},
        "largest_files": [],
    }

    # 创建归档根目录
    ensure_dir(ARCHIVE_ROOT)
    ensure_dir(REPORTS_DIR)

    # ---------------------------- VSCode ----------------------------
    vscode_root = ARCHIVE_ROOT / "vscode"
    ensure_dir(vscode_root)

    vscode_settings = copy_settings(
        VSCODE_USER_DIR / "settings.json",
        vscode_root / "settings.json",
        stats,
        "vscode",
    )

    extract_history(
        VSCODE_USER_DIR / "History",
        vscode_root / "history",
        stats,
        "vscode",
    )

    extract_state_vscdb(
        VSCODE_USER_DIR / "globalStorage" / "state.vscdb",
        vscode_root / "state_vscdb",
        important_keys=[
            "GitHub.copilot-chat",
            "chat.cachedLanguageModels.v2",
            "terminal.history.entries.commands",
            "mcp.json",
        ],
        pattern_keys=[],
        stats=stats,
        editor_name="vscode",
    )

    copy_tree_robust(
        VSCODE_USER_DIR / "snippets",
        vscode_root / "snippets",
        stats,
        "vscode_snippets",
    )
    copy_tree_robust(
        VSCODE_USER_DIR / "workspaceStorage",
        vscode_root / "workspaceStorage",
        stats,
        "vscode_workspaceStorage",
    )

    # ---------------------------- Cursor ----------------------------
    cursor_root = ARCHIVE_ROOT / "cursor"
    ensure_dir(cursor_root)

    cursor_settings = copy_settings(
        CURSOR_USER_DIR / "settings.json",
        cursor_root / "settings.json",
        stats,
        "cursor",
    )

    extract_history(
        CURSOR_USER_DIR / "History",
        cursor_root / "history",
        stats,
        "cursor",
    )

    extract_state_vscdb(
        CURSOR_USER_DIR / "globalStorage" / "state.vscdb",
        cursor_root / "state_vscdb",
        important_keys=[
            "composer.composerHeaders",
            "cursorai/serverConfig",
            "cursor.commands.globalCommands.classic",
            "cursor.commands.globalCommands.glass",
            "terminal.history.entries.commands",
        ],
        pattern_keys=[
            r"^cursor/glass\.tabs\.v2/.*",
            r"^agentData\.cacheStorage\.agentEnvironment\.slashMenuItems\.local\..*",
        ],
        stats=stats,
        editor_name="cursor",
    )

    extract_cursor_disk_kv(
        CURSOR_USER_DIR / "globalStorage" / "state.vscdb",
        cursor_root / "cursor_disk_kv",
        stats,
    )

    extract_cursor_commits(
        CURSOR_USER_DIR / "globalStorage" / "anysphere.cursor-commits" / "checkpoints",
        cursor_root / "cursor_commits",
        stats,
    )

    copy_tree_robust(
        CURSOR_USER_DIR / "snippets",
        cursor_root / "snippets",
        stats,
        "cursor_snippets",
    )
    copy_tree_robust(
        CURSOR_USER_DIR / "workspaceStorage",
        cursor_root / "workspaceStorage",
        stats,
        "cursor_workspaceStorage",
    )

    # ---------------------------- Hooks ----------------------------
    absorb_hooks(AGENTS_HOOKS_DIR, ARCHIVE_ROOT / "hooks", stats)

    # ---------------------------- 迁移提示 ----------------------------
    migration_map = build_settings_migration_map(vscode_settings, cursor_settings)
    dump_json(REPORTS_DIR / "editor_to_longhun_map.json", migration_map)

    # ---------------------------- 报告 ----------------------------
    report = build_report(stats)
    dump_json(REPORTS_DIR / "editor_memory_report.json", report)
    write_markdown_report(report, REPORTS_DIR / "editor_memory_report.md")
    write_card(report, REPORTS_DIR / "editor_memory.card.json")

    return report


def main() -> None:
    """入口函数。"""
    print(f"[龍魂] 启动编辑器记忆提取器")
    print(f"[DNA] {DNA}")
    print(f"[归档] {ARCHIVE_ROOT}")

    report = run_extraction()

    summary = report["summary"]
    print()
    print("=" * 60)
    print("提取完成")
    print(f"  复制文件数: {summary['copied_files']}")
    print(f"  总字节数:   {summary['total_bytes']:,}")
    print(f"  错误数:     {len(summary['errors'])}")
    print(f"  报告目录:   {REPORTS_DIR}")
    print("=" * 60)

    if summary["errors"]:
        print()
        print("部分源读取失败（不影响整体归档）：")
        for err in summary["errors"][:10]:
            print(f"  - {err}")


if __name__ == "__main__":
    main()
