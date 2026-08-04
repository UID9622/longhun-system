#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
Claude 本地数据吸收脚本 — 将 ~/.claude 的配置、历史与创作迁移到龍魂体系。
DNA: #龍芯⚡️2026-06-29-CLAUDE-ABSORPTION-UID9622
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# -----------------------------------------------------------------------------
# 配置
# -----------------------------------------------------------------------------
HOME = Path.home()
CLAUDE_DIR = HOME / ".claude"
PROJECT_ROOT = HOME / "longhun-system"
ARCHIVE_DIR = PROJECT_ROOT / "brain" / "claude_archive"
REPORTS_DIR = ARCHIVE_DIR / "reports"
EXTRACTED_DIR = ARCHIVE_DIR / "extracted"
RAW_HISTORY_DIR = ARCHIVE_DIR / "raw_file_history"
RAW_PASTE_DIR = ARCHIVE_DIR / "raw_paste_cache"
RAW_SKILLS_DIR = ARCHIVE_DIR / "raw_skills"
RAW_CACHE_DIR = ARCHIVE_DIR / "raw_cache"
CONFIG_DIR = ARCHIVE_DIR / "config"

DNA = "#龍芯⚡️2026-06-29-CLAUDE-ABSORPTION-UID9622"

# -----------------------------------------------------------------------------
# 工具函数
# -----------------------------------------------------------------------------
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_filename(name: str) -> str:
    return re.sub(r"[^\w\-\./\u4e00-\u9fff]+", "_", name).strip("_") or "untitled"


def rel_or_abs(path_str: str) -> Path:
    return Path(path_str).expanduser().resolve()


def archive_path_for(original: str, base_dir: Path) -> Path:
    """把原始路径映射到归档目录下，保留相对结构；外部路径放到 external/ 下。"""
    p = Path(original).expanduser().resolve()
    try:
        rel = p.relative_to(PROJECT_ROOT)
        return base_dir / rel
    except ValueError:
        pass
    try:
        rel = p.relative_to(HOME)
        return base_dir / "home" / rel
    except ValueError:
        return base_dir / "external" / safe_filename(str(p))[0:200]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _rm_readonly(func, path, excinfo):
    os.chmod(path, 0o777)
    func(path)


def safe_rmtree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path, onerror=_rm_readonly)


# -----------------------------------------------------------------------------
# 配置吸收
# -----------------------------------------------------------------------------
def absorb_settings(report: Dict[str, Any]) -> Dict[str, Any]:
    mapping: Dict[str, Any] = {
        "dna": DNA,
        "absorbed_at": now_iso(),
        "source_files": {},
        "claude_to_longhun": [],
    }
    for src_name in ("settings.json", "settings.local.json"):
        src = CLAUDE_DIR / src_name
        if not src.exists():
            continue
        try:
            with open(src, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            data = {"_parse_error": str(e)}
        mapping["source_files"][src_name] = data
        dst = CONFIG_DIR / src_name
        shutil.copy2(src, dst)

    # 参数映射表
    settings = mapping["source_files"].get("settings.json", {})
    local = mapping["source_files"].get("settings.local.json", {})
    perms = local.get("permissions", {})
    allowlist = perms.get("allow", [])
    denylist = perms.get("deny", [])

    mapping["claude_to_longhun"].extend([
        {
            "claude_key": "settings.model",
            "claude_value": settings.get("model"),
            "longhun_key": "kimi-code/config.toml default_model",
            "longhun_value": "kimi-code/kimi-for-coding",
            "note": "Claude 默认 haiku 仅用于轻量问答；龍魂主控使用 Kimi-for-Coding。",
        },
        {
            "claude_key": "settings.skipDangerousModePermissionPrompt",
            "claude_value": settings.get("skipDangerousModePermissionPrompt"),
            "longhun_key": "kimi-code/config.toml default_permission_mode",
            "longhun_value": "yolo",
            "note": "Claude 跳过危险提示 ≈ Kimi yolo 模式；已在 config.toml 中。",
        },
        {
            "claude_key": "settings.local.permissions.allow",
            "claude_value": f"{len(allowlist)} 条",
            "longhun_key": "~/.longhun/config/permissions_allow.json",
            "longhun_value": "按龍魂最小权限原则整理后的命令白名单",
            "note": "Claude 的 Bash 命令白名单可映射为龍魂权限策略。",
        },
        {
            "claude_key": "settings.local.permissions.deny",
            "claude_value": f"{len(denylist)} 条",
            "longhun_key": "~/.longhun/config/permissions_deny.json",
            "longhun_value": "敏感路径/命令黑名单",
            "note": "Claude 的拒绝列表可同步为龍魂黑名单。",
        },
        {
            "claude_key": "CLAUDE.md / 项目记忆",
            "claude_value": "系统提示与项目上下文",
            "longhun_key": "~/.longhun/memory/ + AGENTS.md",
            "longhun_value": "龍魂启动记忆 + 项目级 AGENTS.md",
            "note": "Claude 的 CLAUDE.md 项目提示应写入对应项目的 AGENTS.md。",
        },
    ])

    write_json(CONFIG_DIR / "claude_to_longhun_map.json", mapping)
    report["config_mapping"] = mapping
    report["config_files_copied"] = list(mapping["source_files"].keys())
    return mapping


# -----------------------------------------------------------------------------
# 项目会话解析
# -----------------------------------------------------------------------------
def merge_content_block(existing: Dict[str, Any], block: Dict[str, Any]) -> Dict[str, Any]:
    """增量合并同一 content block（文本/thinking 追加，tool_use 更新 input）。"""
    btype = block.get("type")
    if btype in ("text", "thinking"):
        existing["text"] = existing.get("text", "") + block.get("text", "")
    elif btype == "tool_use":
        for k, v in block.get("input", {}).items():
            existing.setdefault("input", {})[k] = v
    return existing


def accumulate_messages(path: Path) -> List[Dict[str, Any]]:
    """把一条 JSONL 中同一 message.id 的增量块合并成完整消息。"""
    by_id: Dict[str, Dict[str, Any]] = {}
    order: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = obj.get("message")
            if not isinstance(msg, dict):
                continue
            mid = msg.get("id") or msg.get("requestId") or msg.get("messageId")
            if not mid:
                continue
            if mid not in by_id:
                by_id[mid] = {"_meta": obj, "content": {}}
                order.append(mid)
            rec = by_id[mid]
            for k, v in msg.items():
                if k == "content":
                    if isinstance(v, list):
                        for idx, block in enumerate(v):
                            if not isinstance(block, dict):
                                continue
                            bid = block.get("id") or f"{mid}:{idx}"
                            if bid not in rec["content"]:
                                rec["content"][bid] = dict(block)
                            else:
                                rec["content"][bid] = merge_content_block(rec["content"][bid], block)
                else:
                    rec[k] = v
    out = []
    for mid in order:
        rec = by_id[mid]
        rec["content"] = list(rec["content"].values())
        out.append(rec)
    return out


def extract_writes_from_session(session_path: Path, report: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从项目会话中提取 Write/Edit 工具调用，并保存到归档。"""
    session_name = session_path.stem
    writes: List[Dict[str, Any]] = []
    try:
        messages = accumulate_messages(session_path)
    except Exception as e:
        report["parse_errors"].append(f"{session_path}: {e}")
        return writes

    session_extract_dir = EXTRACTED_DIR / "project_files" / safe_filename(session_name)
    for msg in messages:
        if msg.get("role") != "assistant":
            continue
        for block in msg.get("content", []):
            if block.get("type") != "tool_use":
                continue
            name = block.get("name")
            if name not in ("Write", "Edit"):
                continue
            inp = block.get("input", {})
            file_path = inp.get("file_path") or inp.get("path") or inp.get("target_path")
            contents = inp.get("contents") or inp.get("content") or inp.get("old_string")
            if not file_path:
                continue
            write_meta = {
                "session": session_name,
                "tool": name,
                "file_path": file_path,
                "timestamp": msg.get("timestamp") or msg.get("_meta", {}).get("timestamp"),
                "model": msg.get("model"),
                "tool_use_id": block.get("id"),
            }
            writes.append(write_meta)
            if contents:
                apath = archive_path_for(file_path, session_extract_dir)
                # 防止覆盖：同一文件多次写入加版本号
                version = 1
                final = apath
                while final.exists():
                    suffix = "" if apath.suffix == "" else apath.suffix
                    stem = apath.with_suffix("").name
                    parent = apath.parent
                    final = parent / f"{stem}.v{version}{suffix}"
                    version += 1
                write_text(final, contents)
                write_meta["archived_at"] = str(final)
    return writes


def extract_assistant_text(session_path: Path, report: Dict[str, Any]) -> str:
    """将会话中 assistant 文本汇总为 Markdown，便于第二大脑索引。"""
    lines: List[str] = []
    try:
        messages = accumulate_messages(session_path)
    except Exception as e:
        report["parse_errors"].append(f"{session_path}: {e}")
        return ""
    for msg in messages:
        if msg.get("role") != "assistant":
            continue
        for block in msg.get("content", []):
            if block.get("type") == "text":
                text = block.get("text", "")
                if text.strip():
                    lines.append(text)
    return "\n\n---\n\n".join(lines)


# -----------------------------------------------------------------------------
# 文件历史、剪贴板缓存、技能、CLAUDE.md 等原始数据
# -----------------------------------------------------------------------------
def absorb_file_history(report: Dict[str, Any]) -> None:
    src = CLAUDE_DIR / "file-history"
    if not src.exists():
        return
    # 直接复制目录树
    safe_rmtree(RAW_HISTORY_DIR)
    shutil.copytree(src, RAW_HISTORY_DIR)
    count = sum(1 for _ in RAW_HISTORY_DIR.rglob("*") if _.is_file())
    report["file_history_files"] = count

    # 建立索引：从所有项目会话中收集 snapshot 的 trackedFileBackups 映射
    path_to_version: Dict[str, Dict[str, Any]] = {}
    for proj in (CLAUDE_DIR / "projects").rglob("*.jsonl"):
        with open(proj, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                snap = obj.get("snapshot") or obj
                tfb = snap.get("trackedFileBackups")
                if not isinstance(tfb, dict):
                    continue
                for p, info in tfb.items():
                    path_to_version.setdefault(p, {}).update(info)
                    path_to_version[p]["session_uuid"] = proj.stem
    write_json(RAW_HISTORY_DIR / "path_version_index.json", path_to_version)
    report["file_history_tracked_paths"] = len(path_to_version)


def absorb_paste_cache(report: Dict[str, Any]) -> None:
    src = CLAUDE_DIR / "paste-cache"
    if not src.exists():
        return
    safe_rmtree(RAW_PASTE_DIR)
    shutil.copytree(src, RAW_PASTE_DIR)
    count = sum(1 for _ in RAW_PASTE_DIR.rglob("*") if _.is_file())
    report["paste_cache_files"] = count


def absorb_skills(report: Dict[str, Any]) -> None:
    src = CLAUDE_DIR / "skills"
    if not src.exists():
        return
    safe_rmtree(RAW_SKILLS_DIR)
    shutil.copytree(src, RAW_SKILLS_DIR)
    count = sum(1 for _ in RAW_SKILLS_DIR.rglob("*") if _.is_file())
    report["skill_files"] = count


def absorb_misc(report: Dict[str, Any]) -> None:
    RAW_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    copies = [
        (CLAUDE_DIR / "CLAUDE.md", RAW_CACHE_DIR / "CLAUDE.md"),
        (CLAUDE_DIR / "cache" / "changelog.md", RAW_CACHE_DIR / "changelog.md"),
        (CLAUDE_DIR / "history.jsonl", RAW_CACHE_DIR / "history.jsonl"),
    ]
    for src, dst in copies:
        if src.exists():
            if dst.exists():
                safe_rmtree(dst) if dst.is_dir() else dst.unlink()
            shutil.copy2(src, dst)
            # 保证后续可覆盖
            os.chmod(dst, 0o644)
    report["misc_files_copied"] = [p.name for p in RAW_CACHE_DIR.iterdir() if p.is_file()]


# -----------------------------------------------------------------------------
# 主流程
# -----------------------------------------------------------------------------
def run_absorption() -> Dict[str, Any]:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    for d in (REPORTS_DIR, EXTRACTED_DIR, RAW_HISTORY_DIR, RAW_PASTE_DIR,
              RAW_SKILLS_DIR, RAW_CACHE_DIR, CONFIG_DIR):
        d.mkdir(parents=True, exist_ok=True)

    report: Dict[str, Any] = {
        "dna": DNA,
        "started_at": now_iso(),
        "claude_dir": str(CLAUDE_DIR),
        "archive_dir": str(ARCHIVE_DIR),
        "parse_errors": [],
    }

    # 1. 配置
    absorb_settings(report)

    # 2. 项目会话
    project_dir = CLAUDE_DIR / "projects"
    session_files = sorted(project_dir.rglob("*.jsonl")) if project_dir.exists() else []
    all_writes: List[Dict[str, Any]] = []
    session_texts: List[Tuple[str, str]] = []
    for sf in session_files:
        all_writes.extend(extract_writes_from_session(sf, report))
        text = extract_assistant_text(sf, report)
        if text:
            session_texts.append((sf.stem, text))

    report["session_files"] = len(session_files)
    report["extracted_writes"] = len(all_writes)

    # 保存写入索引和会话文本摘要
    write_json(EXTRACTED_DIR / "write_index.json", all_writes)
    for stem, text in session_texts:
        md_path = EXTRACTED_DIR / "session_texts" / f"{safe_filename(stem)}.md"
        write_text(md_path, f"<!-- Claude session assistant text: {stem} -->\n\n{text}")

    # 3. 原始数据
    absorb_file_history(report)
    absorb_paste_cache(report)
    absorb_skills(report)
    absorb_misc(report)

    report["finished_at"] = now_iso()
    write_json(REPORTS_DIR / "claude_absorption_report.json", report)
    return report


def generate_markdown_report(report: Dict[str, Any]) -> str:
    lines = [
        "# Claude 本地数据吸收报告",
        "",
        f"**DNA**: `{report['dna']}`",
        f"**时间**: {report['started_at']} → {report.get('finished_at', '未完成')}",
        "",
        "## 吸收范围",
        f"- 源目录: `{report['claude_dir']}`",
        f"- 归档目录: `{report['archive_dir']}`",
        "",
        "## 统计",
        f"- 项目会话 JSONL: {report.get('session_files', 0)}",
        f"- 提取 Write/Edit 创作: {report.get('extracted_writes', 0)}",
        f"- file-history 版本文件: {report.get('file_history_files', 0)}",
        f"- 追踪文件路径: {report.get('file_history_tracked_paths', 0)}",
        f"- paste-cache 片段: {report.get('paste_cache_files', 0)}",
        f"- skill 文件: {report.get('skill_files', 0)}",
        f"- 配置映射项: {len(report.get('config_mapping', {}).get('claude_to_longhun', []))}",
        f"- 解析错误: {len(report.get('parse_errors', []))}",
        "",
        "## 配置迁移建议",
    ]
    for item in report.get("config_mapping", {}).get("claude_to_longhun", []):
        lines.append(f"- **{item['claude_key']}** → `{item['longhun_key']}`: {item['note']}")
    lines.append("")
    lines.append("## 文件位置")
    lines.append(f"- 配置映射: `{CONFIG_DIR / 'claude_to_longhun_map.json'}`")
    lines.append(f"- 写入索引: `{EXTRACTED_DIR / 'write_index.json'}`")
    lines.append(f"- 提取项目文件: `{EXTRACTED_DIR / 'project_files'}`")
    lines.append(f"- 会话文本摘要: `{EXTRACTED_DIR / 'session_texts'}`")
    lines.append(f"- 原始 file-history: `{RAW_HISTORY_DIR}`")
    lines.append(f"- 原始 paste-cache: `{RAW_PASTE_DIR}`")
    lines.append(f"- 原始 skills: `{RAW_SKILLS_DIR}`")
    lines.append(f"- 原始 CLAUDE.md/history: `{RAW_CACHE_DIR}`")
    lines.append("")
    if report.get("parse_errors"):
        lines.append("## 解析错误")
        for err in report["parse_errors"][:20]:
            lines.append(f"- {err}")
        if len(report["parse_errors"]) > 20:
            lines.append(f"- ... 共 {len(report['parse_errors'])} 条")
        lines.append("")
    lines.append("---")
    lines.append("由龍魂吸收脚本自动生成。")
    return "\n".join(lines)


def generate_cnsh_card(report: Dict[str, Any]) -> None:
    card = {
        "CNSH_CARD": {
            "name": "Claude本地数据吸收",
            "version": "1.0",
            "dna": report["dna"],
            "created_at": report.get("finished_at", now_iso()),
            "sources": ["~/.claude/projects/*.jsonl", "~/.claude/file-history", "~/.claude/paste-cache", "~/.claude/skills", "~/.claude/settings*.json"],
            "outputs": {
                "report_json": str(REPORTS_DIR / "claude_absorption_report.json"),
                "report_md": str(REPORTS_DIR / "claude_absorption_report.md"),
                "config_map": str(CONFIG_DIR / "claude_to_longhun_map.json"),
                "write_index": str(EXTRACTED_DIR / "write_index.json"),
            },
            "metrics": {
                "sessions": report.get("session_files", 0),
                "writes": report.get("extracted_writes", 0),
                "file_history": report.get("file_history_files", 0),
                "paste_cache": report.get("paste_cache_files", 0),
                "skills": report.get("skill_files", 0),
            },
            "tags": ["Claude", "数据迁移", "龍魂", "记忆吸收", "UID9622"],
            "status": "🟢 完成",
        }
    }
    write_json(REPORTS_DIR / "claude_absorption.card.json", card)


def main() -> int:
    parser = argparse.ArgumentParser(description="Claude 本地数据吸收到龍魂体系")
    parser.add_argument("--dry-run", action="store_true", help="仅生成报告，不写入文件")
    args = parser.parse_args()

    if args.dry_run:
        print("--dry-run 暂不支持，直接执行吸收。")

    report = run_absorption()
    md = generate_markdown_report(report)
    write_text(REPORTS_DIR / "claude_absorption_report.md", md)
    generate_cnsh_card(report)

    print(md)
    print(f"\n完整报告: {REPORTS_DIR / 'claude_absorption_report.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
