#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
Claude local-agent-mode-sessions 清单生成器
扫描 ~/Library/Application Support/Claude/local-agent-mode-sessions，
整理技能、功能模块、会话、输入输出、审计备份等元数据，输出：
  - claude_sessions_manifest.json
  - claude_sessions_index.md
  - 同步追加到 graph_data.json 并重生成 graph_index.md

执行：
  cd /Users/zuimeidedeyihan/longhun-system/03_知識圖譜
  python3 generate_claude_sessions_inventory.py
"""

import json
import os
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter, defaultdict

PROJECT_ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
KG_DIR = PROJECT_ROOT / "03_知識圖譜"
BASE = Path.home() / "Library" / "Application Support" / "Claude" / "local-agent-mode-sessions"

MANIFEST = KG_DIR / "claude_sessions_manifest.json"
INDEX_MD = KG_DIR / "claude_sessions_index.md"
GRAPH_DATA = KG_DIR / "graph_data.json"
GRAPH_INDEX = KG_DIR / "graph_index.md"

NOISE = {".DS_Store", "Thumbs.db"}


def human_size(n):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.2f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024
    return f"{n:.2f} PB"


def slugify(name: str) -> str:
    s = name.strip()
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"[\s·./\\]+", "-", s)
    s = re.sub(r"[^\w\u4e00-\u9fff-]", "", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return (s or "item").lower()[:80]


def parse_frontmatter(text: str):
    fm = {}
    if text.startswith("---"):
        end = text.find("---", 3)
        if end > 3:
            key = None
            value_lines = []
            mode = None  # None, '|', '>'
            for line in text[3:end].splitlines():
                # 检测新的顶层键（非缩进）
                m = re.match(r"^(\w+):\s*(.*)$", line)
                if m and (not value_lines or not re.match(r"^[ \t]", line)):
                    if key is not None:
                        val = "\n".join(value_lines).strip() if value_lines else ""
                        val = val.strip('"').strip("'")
                        fm[key] = val
                    key = m.group(1).strip()
                    rest = m.group(2).strip()
                    if rest in ("|", ">"):
                        mode = rest
                        value_lines = []
                    else:
                        mode = None
                        value_lines = [rest]
                elif key is not None and mode in ("|", ">"):
                    value_lines.append(line)
            if key is not None:
                val = "\n".join(value_lines).strip() if value_lines else ""
                val = val.strip('"').strip("'")
                fm[key] = val
    return fm


def read_first_lines(path: Path, n=30):
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            return "".join(f.readline() for _ in range(n))
    except Exception:
        return ""


def extract_python_summary(path: Path):
    text = read_first_lines(path, 40)
    m = re.search(r'"""(.*?)"""', text, re.S)
    if m:
        lines = [l.strip() for l in m.group(1).splitlines() if l.strip()]
        return lines[0] if lines else ""
    return ""


def extract_html_title(path: Path):
    text = read_first_lines(path, 30)
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    return m.group(1).strip() if m else ""


def count_lines(path: Path):
    try:
        with path.open("rb") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(BASE))
    except Exception:
        return str(path)


def fmt_time(ms):
    if not ms:
        return ""
    try:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return str(ms)


def scan():
    stats = {
        "total_files": 0,
        "total_dirs": 0,
        "total_size": 0,
        "file_types": Counter(),
    }

    skills = {}  # (skill_id, source) -> dict
    plugins = []
    extensions = []
    sessions = []
    modules = []
    html_tools = []
    uploads = []
    outputs = []
    audits = []
    backups = []
    conversations = []
    snapshots = []

    for root, dirs, files in os.walk(BASE):
        root_path = Path(root)
        # 跳过非项目隐藏目录（避免 .git 等）
        dirs[:] = [d for d in dirs if not d.startswith(".") or d in {".claude"}]
        rel_parts = rel(root_path).split(os.sep)

        for d in dirs:
            if d not in NOISE:
                stats["total_dirs"] += 1

        for f in files:
            if f in NOISE:
                continue
            p = root_path / f
            try:
                size = p.stat().st_size
            except Exception:
                continue
            stats["total_files"] += 1
            stats["total_size"] += size
            ext = p.suffix.lower()
            stats["file_types"][ext] += 1
            rp = rel(p)
            internal = "skills-plugin/" in rp or "rpm/plugin_" in rp

            # 技能文件
            if f == "SKILL.md":
                fm = parse_frontmatter(p.read_text(encoding="utf-8", errors="ignore"))
                skill_id = fm.get("name", p.parent.name)
                # 判断来源
                src = "user"
                if "skills-plugin" in rp:
                    src = "anthropic"
                elif "rpm/plugin_" in rp:
                    src = "cowork-plugin"
                # 用户自定义 dragon-soul-agent 可能同时出现在 user sessions
                if "dragon-soul-agent" in skill_id.lower():
                    src = "user"
                key = (skill_id, src)
                if key not in skills:
                    skills[key] = {
                        "skill_id": skill_id,
                        "name": skill_id,
                        "source": src,
                        "description": fm.get("description", ""),
                        "paths": [rp],
                        "tags": ["#skill", f"#{src}"],
                    }
                else:
                    skills[key]["paths"].append(rp)

            # manifest.json
            elif f == "manifest.json":
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                except Exception:
                    continue
                if "skills" in data:
                    for s in data["skills"]:
                        src = s.get("creatorType", "unknown")
                        key = (s["skillId"], src)
                        if key not in skills:
                            skills[key] = {
                                "skill_id": s["skillId"],
                                "name": s.get("name", s["skillId"]),
                                "source": src,
                                "description": s.get("description", ""),
                                "paths": [rp],
                                "tags": ["#skill", f"#{src}"],
                            }
                        else:
                            skills[key]["description"] = skills[key]["description"] or s.get("description", "")
                            skills[key]["paths"].append(rp)
                elif "plugins" in data:
                    for pl in data["plugins"]:
                        plugins.append({
                            "id": pl.get("id", ""),
                            "name": pl.get("name", ""),
                            "type": "cowork-plugin",
                            "description": "",
                            "path": rp,
                            "tags": ["#plugin", "#cowork-plugin"],
                        })
                elif "manifest_version" in data:
                    extensions.append({
                        "name": data.get("name", ""),
                        "version": data.get("version", ""),
                        "description": data.get("description", ""),
                        "path": rp,
                        "tags": ["#browser-extension", "#output"],
                    })

            # 二进制 skill 文件
            elif f.endswith(".skill"):
                modules.append({
                    "name": p.stem,
                    "type": "skill-binary",
                    "description": "已打包的 skill 二进制文件（需解压读取）",
                    "path": rp,
                    "size": size,
                    "tags": ["#skill", "#binary", "#output"],
                })

            # Python 模块
            elif f.endswith(".py"):
                desc = extract_python_summary(p)
                sess = guess_session(rel_parts)
                modules.append({
                    "name": p.name,
                    "type": "python-module",
                    "category": "skill-internal" if internal else "user-output",
                    "description": desc,
                    "path": rp,
                    "size": size,
                    "session": sess,
                    "tags": ["#module", "#python"] + (["#skill-internal"] if internal else ["#user-output"]) + (["#longhun"] if "龍魂" in desc or "longhun" in p.name.lower() else []),
                })

            # JS 模块
            elif f.endswith(".js"):
                sess = guess_session(rel_parts)
                modules.append({
                    "name": p.name,
                    "type": "javascript-module",
                    "category": "skill-internal" if internal else "user-output",
                    "description": "",
                    "path": rp,
                    "size": size,
                    "session": sess,
                    "tags": ["#module", "#javascript"] + (["#skill-internal"] if internal else ["#user-output"]),
                })

            # HTML 工具/页面
            elif f.endswith(".html"):
                title = extract_html_title(p)
                name = title or p.stem
                if internal:
                    loc = "skill-internal"
                elif "终极流场" in rp:
                    loc = "终极流场"
                elif "outputs" in rp:
                    loc = "outputs"
                else:
                    loc = "other"
                html_tools.append({
                    "name": name,
                    "filename": p.name,
                    "location": loc,
                    "category": "skill-internal" if internal else "user-output",
                    "path": rp,
                    "size": size,
                    "tags": ["#html-tool", f"#{loc}"] + (["#longhun"] if "龍魂" in name else []),
                })

            # 会话元数据 JSON
            elif f.startswith("local_") and f.endswith(".json") and "audit" not in f:
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                except Exception:
                    continue
                sid = data.get("sessionId", p.stem)
                sess = {
                    "session_id": sid,
                    "title": data.get("title", ""),
                    "process_name": data.get("processName", ""),
                    "model": data.get("model", ""),
                    "created_at": fmt_time(data.get("createdAt")),
                    "last_activity": fmt_time(data.get("lastActivityAt")),
                    "cwd": data.get("cwd", ""),
                    "slash_commands": data.get("slashCommands", []),
                    "initial_message": (data.get("initialMessage", "") or "")[:80],
                    "path": rp,
                    "workspace": rel(p.with_suffix("").parent / p.stem),
                    "tags": ["#session", "#claude-local"],
                }
                sessions.append(sess)

            # audit.jsonl
            elif f == "audit.jsonl":
                audits.append({
                    "path": rp,
                    "size": size,
                    "lines": count_lines(p),
                    "tags": ["#audit", "#session"],
                })

            # .claude.json backups
            elif f.startswith(".claude.json.backup"):
                backups.append({
                    "path": rp,
                    "size": size,
                    "tags": ["#backup", "#config"],
                })

            # shell snapshots
            elif "shell-snapshots" in rp and f.endswith(".sh"):
                snapshots.append({
                    "path": rp,
                    "size": size,
                    "tags": ["#snapshot", "#shell"],
                })

            # conversation jsonl
            elif f.endswith(".jsonl") and ".claude/projects" in rp:
                conversations.append({
                    "path": rp,
                    "size": size,
                    "lines": count_lines(p),
                    "tags": ["#conversation", "#session"],
                })

            # uploads
            elif "/uploads/" in rp:
                uploads.append({
                    "name": p.name,
                    "type": ext or "unknown",
                    "path": rp,
                    "size": size,
                    "tags": ["#upload", f"#{ext.lstrip('.') or 'unknown'}"],
                })

            # outputs（未被上面捕获的）
            elif "/outputs/" in rp:
                outputs.append({
                    "name": p.name,
                    "type": ext or "unknown",
                    "path": rp,
                    "size": size,
                    "tags": ["#output", f"#{ext.lstrip('.') or 'unknown'}"],
                })

    # 会话工作区补充计数
    sess_by_id = {s["session_id"]: s for s in sessions}
    for s in sessions:
        ws = BASE / s["workspace"]
        if ws.exists():
            s["outputs_count"] = sum(1 for _ in (ws / "outputs").rglob("*") if _.is_file() and _.name not in NOISE) if (ws / "outputs").exists() else 0
            s["uploads_count"] = sum(1 for _ in (ws / "uploads").rglob("*") if _.is_file() and _.name not in NOISE) if (ws / "uploads").exists() else 0
            s["audit_lines"] = next((a["lines"] for a in audits if a["path"].startswith(s["workspace"])), 0)
        else:
            s["outputs_count"] = 0
            s["uploads_count"] = 0
            s["audit_lines"] = 0

    return {
        "stats": stats,
        "skills": sorted(skills.values(), key=lambda x: (x["source"], x["skill_id"])),
        "plugins": plugins,
        "extensions": extensions,
        "sessions": sorted(sessions, key=lambda x: x.get("created_at", "") or "", reverse=True),
        "modules": modules,
        "html_tools": html_tools,
        "uploads": uploads,
        "outputs": outputs,
        "audits": audits,
        "backups": backups,
        "conversations": conversations,
        "snapshots": snapshots,
    }


def guess_session(parts):
    # 从路径中找 local_<uuid> 或 agent/<uuid>
    for i, p in enumerate(parts):
        if p.startswith("local_"):
            return p
        if p == "agent" and i + 1 < len(parts):
            return parts[i + 1]
    return ""


def build_manifest(scan_result):
    now = datetime.now().strftime("%Y-%m-%d")
    manifest = {
        "generated_at": datetime.now().isoformat(),
        "dna": f"#龍芯⚡️{now}-CLAUDE-LOCAL-SESSIONS-v1.0",
        "stats": {
            "total_files": scan_result["stats"]["total_files"],
            "total_dirs": scan_result["stats"]["total_dirs"],
            "total_size": scan_result["stats"]["total_size"],
            "human_size": human_size(scan_result["stats"]["total_size"]),
            "file_types": dict(scan_result["stats"]["file_types"].most_common()),
            "skills": len(scan_result["skills"]),
            "plugins": len(scan_result["plugins"]),
            "extensions": len(scan_result["extensions"]),
            "sessions": len(scan_result["sessions"]),
            "modules": len(scan_result["modules"]),
            "html_tools": len(scan_result["html_tools"]),
            "uploads": len(scan_result["uploads"]),
            "outputs": len(scan_result["outputs"]),
            "audits": len(scan_result["audits"]),
            "conversations": len(scan_result["conversations"]),
            "backups": len(scan_result["backups"]),
            "snapshots": len(scan_result["snapshots"]),
        },
        "skills": scan_result["skills"],
        "plugins": scan_result["plugins"],
        "extensions": scan_result["extensions"],
        "sessions": scan_result["sessions"],
        "modules": scan_result["modules"],
        "html_tools": scan_result["html_tools"],
        "uploads": scan_result["uploads"],
        "outputs": scan_result["outputs"],
        "audits": scan_result["audits"],
        "conversations": scan_result["conversations"],
        "backups": scan_result["backups"],
        "snapshots": scan_result["snapshots"],
    }
    return manifest


def generate_markdown(manifest, sr):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st = manifest["stats"]
    lines = []
    lines.append("# Claude Local Agent Mode Sessions 索引")
    lines.append("")
    lines.append(f"**扫描路径**: `{BASE}`")
    lines.append(f"**生成时间**: {now}")
    lines.append(f"**DNA**:`{manifest['dna']}`")
    lines.append("")
    lines.append("## 执行摘要")
    lines.append("")
    lines.append(f"本次扫描 Claude 本地代理会话目录，共识别 **{st['total_files']}** 个文件、**{st['total_dirs']}** 个目录，")
    lines.append(f"总占用空间 **{st['human_size']}**；覆盖 **{len(st['file_types'])}** 种文件扩展名。")
    lines.append(f"其中：技能 **{st['skills']}** 个、插件 **{st['plugins']}** 个、浏览器扩展 **{st['extensions']}** 个、")
    lines.append(f"会话 **{st['sessions']}** 个、功能模块 **{st['modules']}** 个、HTML 工具 **{st['html_tools']}** 个；")
    lines.append(f"上传物料 **{st['uploads']}** 个、输出物料 **{st['outputs']}** 个、审计日志 **{st['audits']}** 条、")
    lines.append(f"对话记录 **{st['conversations']}** 条、配置备份 **{st['backups']}** 个、Shell 快照 **{st['snapshots']}** 个。")
    lines.append("")

    lines.append("## 统计概览")
    lines.append("")
    lines.append("| 指标 | 数值 |")
    lines.append("|---|---|")
    lines.append(f"| 文件总数 | {st['total_files']} |")
    lines.append(f"| 目录总数 | {st['total_dirs']} |")
    lines.append(f"| 总大小 | {st['human_size']} |")
    lines.append(f"| 技能 | {st['skills']} |")
    lines.append(f"| 插件 | {st['plugins']} |")
    lines.append(f"| 浏览器扩展 | {st['extensions']} |")
    lines.append(f"| 会话 | {st['sessions']} |")
    lines.append(f"| 功能模块 | {st['modules']} |")
    lines.append(f"| HTML 工具 | {st['html_tools']} |")
    lines.append(f"| 上传物料 | {st['uploads']} |")
    lines.append(f"| 输出物料 | {st['outputs']} |")
    lines.append(f"| 审计日志 | {st['audits']} |")
    lines.append(f"| 对话记录 | {st['conversations']} |")
    lines.append(f"| 配置备份 | {st['backups']} |")
    lines.append(f"| Shell 快照 | {st['snapshots']} |")
    lines.append("")

    lines.append("### 文件类型分布（Top 20）")
    lines.append("")
    lines.append("| 扩展名 | 数量 |")
    lines.append("|---|---|")
    for ext, cnt in list(Counter(st['file_types']).most_common(20)):
        lines.append(f"| {ext or '(无)'} | {cnt} |")
    lines.append("")

    # 技能清单
    lines.append("## 技能清单（Skills）")
    lines.append("")
    lines.append("| 技能 ID | 来源 | 描述 | 路径数 | 标签 |")
    lines.append("|---|---|---|---|---|")
    for s in manifest["skills"]:
        desc = (s["description"] or "")[:80].replace("|", "｜").replace("\n", " ")
        paths = len(s.get("paths", []))
        tags = " ".join(s["tags"])
        lines.append(f"| `{s['skill_id']}` | {s['source']} | {desc} | {paths} | {tags} |")
    lines.append("")

    # 插件
    if manifest["plugins"]:
        lines.append("## 插件清单（Plugins）")
        lines.append("")
        lines.append("| 插件 ID | 名称 | 路径 | 标签 |")
        lines.append("|---|---|---|---|")
        for p in manifest["plugins"]:
            lines.append(f"| `{p.get('id','')}` | {p.get('name','')} | `{p['path']}` | {' '.join(p['tags'])} |")
        lines.append("")

    # 浏览器扩展
    if manifest["extensions"]:
        lines.append("## 浏览器扩展（Browser Extensions）")
        lines.append("")
        lines.append("| 名称 | 版本 | 描述 | 路径 | 标签 |")
        lines.append("|---|---|---|---|---|")
        for e in manifest["extensions"]:
            desc = (e.get("description") or "").replace("|", "｜")
            lines.append(f"| {e.get('name','')} | {e.get('version','')} | {desc} | `{e['path']}` | {' '.join(e['tags'])} |")
        lines.append("")

    # 会话
    lines.append("## 会话清单（Sessions）")
    lines.append("")
    lines.append("| 会话 ID | 标题 | 模型 | 创建时间 | 最后活跃 | 加载技能数 | 输出数 | 上传数 | 审计行数 | 标签 |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for s in manifest["sessions"]:
        title = (s.get("title") or "").replace("|", "｜")[:30]
        cmd_count = len(s.get("slash_commands", []))
        tags = " ".join(s["tags"])
        lines.append(f"| `{s['session_id'][:20]}...` | {title} | {s.get('model','')} | {s.get('created_at','')} | {s.get('last_activity','')} | {cmd_count} | {s.get('outputs_count',0)} | {s.get('uploads_count',0)} | {s.get('audit_lines',0)} | {tags} |")
    lines.append("")

    # 功能模块
    user_modules = [m for m in manifest["modules"] if m.get("category") != "skill-internal"]
    internal_modules = [m for m in manifest["modules"] if m.get("category") == "skill-internal"]
    if user_modules or internal_modules:
        lines.append("## 功能模块（Modules）")
        lines.append("")
        if user_modules:
            lines.append(f"### 用户输出模块（{len(user_modules)} 个）")
            lines.append("")
            lines.append("| 名称 | 类型 | 描述 | 来源会话 | 大小 | 标签 |")
            lines.append("|---|---|---|---|---|---|")
            for m in user_modules:
                desc = (m.get("description") or "").replace("|", "｜").replace("\n", " ")[:60]
                sess = m.get("session", "")[:20]
                tags = " ".join(m["tags"])
                lines.append(f"| `{m['name']}` | {m['type']} | {desc} | `{sess}` | {human_size(m.get('size',0))} | {tags} |")
            lines.append("")
        if internal_modules:
            lines.append(f"### 技能内部脚本（{len(internal_modules)} 个）")
            lines.append("")
            lines.append("来自 Anthropic 官方 skill 与 cowork plugin 的实现脚本，通常无需手动迁移。")
            lines.append("")
            lines.append("| 名称 | 类型 | 描述 | 路径片段 | 大小 | 标签 |")
            lines.append("|---|---|---|---|---|---|")
            for m in internal_modules:
                desc = (m.get("description") or "").replace("|", "｜").replace("\n", " ")[:40]
                path_hint = "/".join(Path(m["path"]).parts[-3:-1])
                tags = " ".join(m["tags"])
                lines.append(f"| `{m['name']}` | {m['type']} | {desc} | `{path_hint}` | {human_size(m.get('size',0))} | {tags} |")
            lines.append("")

    # HTML 工具
    user_html = [h for h in manifest["html_tools"] if h.get("category") != "skill-internal"]
    internal_html = [h for h in manifest["html_tools"] if h.get("category") == "skill-internal"]
    if user_html or internal_html:
        lines.append("## 前端/HTML 工具")
        lines.append("")
        if user_html:
            lines.append(f"### 用户前端工具（{len(user_html)} 个）")
            lines.append("")
            lines.append("| 名称/标题 | 文件名 | 位置 | 大小 | 标签 |")
            lines.append("|---|---|---|---|---|")
            for h in user_html:
                name = (h.get("name") or "").replace("|", "｜")[:40]
                tags = " ".join(h["tags"])
                lines.append(f"| {name} | `{h['filename']}` | {h['location']} | {human_size(h.get('size',0))} | {tags} |")
            lines.append("")
        if internal_html:
            lines.append(f"### 技能内部 HTML 模板（{len(internal_html)} 个）")
            lines.append("")
            lines.append("| 名称/标题 | 文件名 | 所属 skill | 大小 | 标签 |")
            lines.append("|---|---|---|---|---|")
            for h in internal_html:
                name = (h.get("name") or "").replace("|", "｜")[:40]
                path_hint = "/".join(Path(h["path"]).parts[-3:-1])
                tags = " ".join(h["tags"])
                lines.append(f"| {name} | `{h['filename']}` | `{path_hint}` | {human_size(h.get('size',0))} | {tags} |")
            lines.append("")

    # 输入/上传物料
    if manifest["uploads"]:
        lines.append("## 输入/上传物料（Uploads）")
        lines.append("")
        type_counts = Counter(u["type"] for u in manifest["uploads"])
        lines.append("| 类型 | 数量 | 示例 |")
        lines.append("|---|---|---|")
        for t, cnt in type_counts.most_common(20):
            examples = [u["name"] for u in manifest["uploads"] if u["type"] == t][:3]
            lines.append(f"| {t or 'unknown'} | {cnt} | {', '.join(f'`{e}`' for e in examples)} |")
        lines.append("")

    # 输出物料
    if manifest["outputs"]:
        lines.append("## 输出物料（Outputs）")
        lines.append("")
        type_counts = Counter(o["type"] for o in manifest["outputs"])
        lines.append("| 类型 | 数量 | 示例 |")
        lines.append("|---|---|---|")
        for t, cnt in type_counts.most_common(20):
            examples = [o["name"] for o in manifest["outputs"] if o["type"] == t][:3]
            lines.append(f"| {t or 'unknown'} | {cnt} | {', '.join(f'`{e}`' for e in examples)} |")
        lines.append("")

    # 审计与备份
    lines.append("## 审计、备份与对话记录")
    lines.append("")
    lines.append("| 类型 | 数量 | 总大小 | 说明 |")
    lines.append("|---|---|---|---|")
    total_audit_size = sum(a.get("size", 0) for a in manifest["audits"])
    total_conv_size = sum(c.get("size", 0) for c in manifest["conversations"])
    total_backup_size = sum(b.get("size", 0) for b in manifest["backups"])
    total_snap_size = sum(s.get("size", 0) for s in manifest["snapshots"])
    lines.append(f"| 审计日志 audit.jsonl | {st['audits']} | {human_size(total_audit_size)} | 每条会话的行为审计 |")
    lines.append(f"| 对话记录 .jsonl | {st['conversations']} | {human_size(total_conv_size)} | .claude/projects 下的会话流水 |")
    lines.append(f"| 配置备份 .claude.json.backup | {st['backups']} | {human_size(total_backup_size)} | 配置历史快照 |")
    lines.append(f"| Shell 快照 | {st['snapshots']} | {human_size(total_snap_size)} | 命令行环境快照 |")
    lines.append("")

    # 自动化与完善建议
    lines.append("## 自动化与完善建议")
    lines.append("")
    lines.append("1. **技能同步**：将 `dragon-soul-agent` 等用户自定义 skill 与项目 `01_技能库/`、`~/.kimi-code/skills/` 保持一致，避免本地会话与主干版本漂移。")
    lines.append("2. **模块入主干**：`bone_retriever.py`、`gua_classifier.py`、`shield_engine.py` 等 Python 模块建议迁移到 `cnsh-core/` 或对应功能模块目录，统一版本管理。")
    lines.append("3. **扩展归档**：`龍魂工具箱-v3` 浏览器扩展可纳入 `baobao-guardian/` 或独立 `extensions/` 目录，保留 manifest 与图标资源。")
    lines.append("4. **HTML 工具入库**：`终极流场` 系列 HTML 页面可迁移到 `public/` 或 `_archive/artifacts/`，并建立入口索引。")
    lines.append("5. **会话元数据定期扫描**：可配置 cron 每周执行本脚本，跟踪新增会话、输出物与技能变化。")
    lines.append("6. **审计日志治理**：audit.jsonl 只增不减，建议按月轮转并归档到 `audit/` 或 `_archive/audit-logs/`。")
    lines.append("7. **去重与硬链接**：对 `skills-plugin` 多用户副本（anthropic 官方 skill 被复制多份）可考虑内容级去重，减少磁盘占用。")
    lines.append("")

    # 补充区块说明
    lines.append("## 已补充的区块与标签")
    lines.append("")
    lines.append("- 新增「执行摘要」「统计概览」「文件类型分布」等概览区块，避免只看清单丢失全局信息。")
    lines.append("- 按「技能」「插件」「扩展」「会话」「模块」「HTML 工具」「上传/输出物料」「审计备份」八大维度拆分，结构清晰。")
    lines.append("- 每条记录自动标注 `#skill` `#module` `#session` `#output` `#upload` `#audit` `#backup` 等标签，并区分 `#anthropic` / `#user` / `#cowork-plugin` 来源。")
    lines.append("- 对 `.skill` 二进制、`.py` 第一行 docstring、`.html` `<title>` 等遗漏内容类型进行了补全。")
    lines.append("- 所有关键交付物均已生成 DNA 追溯码，便于后续 `longhun-dna-align` 对齐审计。")
    lines.append("")
    lines.append("---")
    lines.append(f"**自动生成于**: {datetime.now().isoformat()}")
    return "\n".join(lines)


def fix_json_text(text: str) -> str:
    return re.sub(r'"dna":#([^",\n]+)"?', r'"dna":"#\1"', text)


def load_graph_data():
    if not GRAPH_DATA.exists():
        return {"timestamp": datetime.now().isoformat(), "nodes": {}, "edges": [], "dna": "#龍芯⚡️2026-06-06-KNOWLEDGE-GRAPH-DATA-v1.0"}
    text = GRAPH_DATA.read_text(encoding="utf-8")
    text = fix_json_text(text)
    return json.loads(text)


def update_graph_data(manifest):
    data = load_graph_data()
    data["timestamp"] = datetime.now().isoformat()
    existing_edges = {(e["source"], e["target"], e.get("relationship")) for e in data["edges"]}

    root_id = "claude-local-sessions"
    data["nodes"][root_id] = {
        "node_id": root_id,
        "label": "Claude Local Agent Sessions",
        "type": "inbox",
        "dna": manifest["dna"],
        "description": f"Claude 本地代理会话目录盘点 · {manifest['stats']['human_size']} · {manifest['stats']['total_files']} 个文件",
        "related_nodes": [],
    }

    categories = {
        "skills": {"label": "Skills", "type": "skill", "tag": "#skill"},
        "plugins": {"label": "Plugins", "type": "plugin", "tag": "#plugin"},
        "extensions": {"label": "Extensions", "type": "extension", "tag": "#browser-extension"},
        "sessions": {"label": "Sessions", "type": "session", "tag": "#session"},
        "modules": {"label": "Modules", "type": "module", "tag": "#module"},
        "html_tools": {"label": "HTML Tools", "type": "html_tool", "tag": "#html-tool"},
        "uploads": {"label": "Uploads", "type": "upload", "tag": "#upload"},
        "outputs": {"label": "Outputs", "type": "output", "tag": "#output"},
        "audits": {"label": "Audits", "type": "audit", "tag": "#audit"},
    }

    for cat, cfg in categories.items():
        cat_id = f"{root_id}/{cat}"
        data["nodes"][cat_id] = {
            "node_id": cat_id,
            "label": cfg["label"],
            "type": cfg["type"],
            "dna": f"{manifest['dna']}-{cat.upper()}",
            "description": f"{cfg['label']} 分类 · 共 {manifest['stats'].get(cat, 0)} 项",
            "related_nodes": [root_id],
        }
        edge_key = (root_id, cat_id, "contains")
        if edge_key not in existing_edges:
            data["edges"].append({"source": root_id, "target": cat_id, "relationship": "contains", "strength": 0.9})
            existing_edges.add(edge_key)

    # 添加代表节点，避免图过于拥挤：每种类型只添加部分关键项
    key_items = []
    for s in manifest["skills"]:
        key_items.append((f"claude-skill/{slugify(s['skill_id'])}", s.get("name", s["skill_id"]), "skill", s.get("description", "")[:60], f"{root_id}/skills", s["tags"]))
    for e in manifest["extensions"]:
        key_items.append((f"claude-ext/{slugify(e.get('name',''))}", e.get("name", ""), "extension", e.get("description", ""), f"{root_id}/extensions", e["tags"]))
    for m in manifest["modules"][:30]:
        key_items.append((f"claude-mod/{slugify(m['name'])}", m["name"], "module", m.get("description", ""), f"{root_id}/modules", m["tags"]))
    for h in manifest["html_tools"][:30]:
        key_items.append((f"claude-html/{slugify(h['filename'])}", h.get("name", h["filename"]), "html_tool", h["filename"], f"{root_id}/html_tools", h["tags"]))

    for node_id, label, ntype, desc, parent_id, tags in key_items:
        if not label:
            continue
        data["nodes"][node_id] = {
            "node_id": node_id,
            "label": label,
            "type": ntype,
            "dna": f"{manifest['dna']}-{slugify(label)[:20].upper()}",
            "description": desc,
            "related_nodes": [parent_id, "l0-core"] if "longhun" in " ".join(tags).lower() else [parent_id],
        }
        edge_key = (parent_id, node_id, "contains")
        if edge_key not in existing_edges:
            data["edges"].append({"source": parent_id, "target": node_id, "relationship": "contains", "strength": 0.85})
            existing_edges.add(edge_key)
        if "l0-core" in data["nodes"] and "longhun" in " ".join(tags).lower():
            edge_key2 = (node_id, "l0-core", "relates_to")
            if edge_key2 not in existing_edges:
                data["edges"].append({"source": node_id, "target": "l0-core", "relationship": "relates_to", "strength": 0.6})
                existing_edges.add(edge_key2)

    return data


def regenerate_graph_index(data):
    nodes = data["nodes"]
    edges = data["edges"]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    type_counts = Counter(n.get("type", "unknown") for n in nodes.values())
    lines = []
    lines.append("# 龍魂系统·知识图谱")
    lines.append("")
    lines.append(f"**生成时间**: {now}")
    lines.append(f"**DNA**:`#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-KNOWLEDGE-GRAPH-v2.0`")
    lines.append("")
    lines.append("## 图谱概览")
    lines.append(f"- **节点总数**: {len(nodes)}")
    lines.append(f"- **边总数**: {len(edges)}")
    avg_degree = round(2 * len(edges) / len(nodes), 2) if nodes else 0
    lines.append(f"- **平均度数**: {avg_degree}")
    lines.append("")
    lines.append("## 节点类型分布")
    for t, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"- **{t}**: {count} 个")
    lines.append("")
    lines.append("## 节点详情")
    by_type = defaultdict(list)
    for n in nodes.values():
        by_type[n.get("type", "unknown")].append(n)
    for t, ns in sorted(by_type.items(), key=lambda x: x[0]):
        lines.append(f"### {t.upper()}")
        lines.append("")
        for n in sorted(ns, key=lambda x: x.get("label", x["node_id"])):
            lines.append(f"#### [[{n.get('label', n['node_id'])}]]")
            lines.append(f"- **ID**: `{n['node_id']}`")
            lines.append(f"- **类型**: {n.get('type', '')}")
            lines.append(f"- **DNA**:`{n.get('dna', '')}`")
            lines.append(f"- **描述**: {n.get('description', '')}")
            rels = n.get("related_nodes", [])
            if rels:
                lines.append(f"- **相关节点**: {' '.join(f'[[{r}]]' for r in rels)}")
            lines.append("")
    lines.append("## 依赖关系")
    rel_groups = defaultdict(list)
    for e in edges:
        rel_groups[e.get("relationship", "relates_to")].append(e)
    for rel, es in sorted(rel_groups.items()):
        lines.append(f"### {rel}")
        lines.append("")
        for e in es:
            src_label = nodes.get(e["source"], {}).get("label", e["source"])
            tgt_label = nodes.get(e["target"], {}).get("label", e["target"])
            lines.append(f"- [[{src_label}]] → [[{tgt_label}]] (强度: {e.get('strength', 0.5)})")
        lines.append("")
    lines.append("---")
    lines.append(f"**自动生成于**: {datetime.now().isoformat()}")
    return "\n".join(lines)


def main():
    if not BASE.exists():
        print(f"路径不存在: {BASE}")
        return
    sr = scan()
    manifest = build_manifest(sr)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    INDEX_MD.write_text(generate_markdown(manifest, sr), encoding="utf-8")
    data = update_graph_data(manifest)
    GRAPH_DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    GRAPH_INDEX.write_text(regenerate_graph_index(data), encoding="utf-8")
    st = manifest["stats"]
    print(f"完成：{st['total_files']} 个文件，{st['skills']} 个技能，{st['sessions']} 个会话，总大小 {st['human_size']}")
    print(f"输出文件：\n  {MANIFEST}\n  {INDEX_MD}\n  {GRAPH_DATA}\n  {GRAPH_INDEX}")


if __name__ == "__main__":
    main()

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·大壮-CONFIRM-SEAL-generate_claude_sess-28BE2E8E
