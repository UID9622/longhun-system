#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-GLYPH-UNIFY-CHECKER-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂·龍字统一检查器 v1.0

铁律（老大焊死 2026-08-21）: 全系统品牌核心字统一繁体「龍」。
简体「龙」禁止出现在 代码标识/文件名/配置/人格定义/注释 中；
需要说明只能加注释，不能翻译成其它字或英文。

分级:
  🔴 核心层 (bin|08_BIN|personas|20_CONFIG|.codebuddy/rules|01_protocols|engines):
     出现简体「龙」= 红线，必须修复
  🟡 普通层: 出现 = 待核，需加注释或人工确认
  ⚪ 历史白名单: Notion镜像/CSDN草稿/隔离区/归档/备份/审计快照
     = 不批量改名（断外部同步链），仅提示，不算违规

用法:
    python3 lh_glyph_unify.py scan            # 全量扫描
    python3 lh_glyph_unify.py scan --json     # JSON 输出(供自愈引擎/巡检调用)
    python3 lh_glyph_unify.py list            # 仅列出违规文件名
"""

import argparse
import json
import os
import sys
from pathlib import Path

龍魂根 = Path(__file__).resolve().parent.parent

# ── 历史白名单（不批量改名·只注释原则） ──
HISTORY_MARKERS = (
    "dragon-soul-open-hub",   # Notion 镜像 hash 命名·外部同步锁死
    "csdn_drafts",            # CSDN 草稿·对外发布同步
    "kimi-deliverables",      # Kimi 交付物·外部产物
    "_QUARANTINE",            # 隔离区·只冻结
    "archive",                # 归档
    "backups",                # 备份
    "backup",                 # 备份
    "dist",                   # 发布包快照
    "models",                 # 模型/权重
    "_work",                  # 临时工作副本
    "03_KNOWLEDGE_GRAPH",     # 知识图谱审计快照
    "11_DATA",                # 数据层
    "notion_mirror",          # Notion 镜像
    "notion-mirror",
    "desktop-knowledge-matrix",  # 桌面知识矩阵·历史同步镜像
    "knowledge-matrix-src",      # 知识矩阵源·历史同步镜像
    "legacy_bin",                # 冻结旧 bin·只注释原则
    "third_party",               # 第三方(ComfyUI/GPT-SoVITS): 音译词如「艾普西龙」非品牌字
    ".codebuddy/memory",         # 记忆日志: 历史记录·说明性文字(注释性质)
)

# ── 全局排除（不扫描） ──
EXCLUDE_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", ".idea", ".vscode"}
EXCLUDE_SUFFIX = {".asc", ".glyph-backup", ".pyc", ".png", ".jpg", ".jpeg", ".gif", ".webp",
                  ".mp4", ".wav", ".mp3", ".pdf", ".zip", ".tar", ".gz", ".bin", ".db",
                  ".sqlite", ".woff", ".woff2", ".ttf", ".otf", ".ico", ".svg", ".plist"}
MAX_TEXT_SIZE = 2 * 1024 * 1024  # >2MB 视为非文本跳过

# ── 核心层目录前缀（相对龍魂根） ──
CORE_DIRS = ("bin", "08_BIN", "personas", "20_CONFIG", "01_protocols", "engines",
             ".codebuddy", "deploy", "config", "core")

# 文本扩展名（只扫这些）
TEXT_EXTS = {".py", ".md", ".sh", ".json", ".yaml", ".yml", ".toml", ".txt", ".html",
             ".js", ".ts", ".css", ".csv", ".ini", ".cfg", ".conf"}

# 简体「龙」vs 繁体「龍」——严禁用翻译/替代，只允许繁体
GLYPH_SIMPLIFIED = "龙"
GLYPH_TRADITIONAL = "龍"

# 检查器自身文件名（豁免：检测目标定义处必须提到简体字）
SELF_FILENAME = "lh_glyph_unify.py"

# 专职处理简体字的工具本体（豁免：本体协议/示例/关键词必须出现简体字）
TOOL_EXEMPT_FILES = (
    "lh_dragon_glyph_guard.py",  # 龍字守卫引擎本体: 协议说明+用法示例演示简转繁
    "lh_notion_full_export.py",  # Notion 导出关键词: 需简繁双收才能匹配历史文档
)

# ── 内容豁免规则 ──
# 1) 转换器: 合法存在 replace("龙","龍") 等繁简归一代码（这就是"只注释"的正解）
# 2) 注释行: 注释里说明简体字=允许（"只能注释"铁律本身允许注释说明）
# 3) 文档字符串: 同理豁免
CONVERTER_PATTERNS = (
    'replace("龙", "龍")',
    "replace('龙', '龍')",
    'replace("龙",\"龍")',
)
COMMENT_MARKERS = ("#", "//", "--", "/*", "*", "<!--", ">", "%")


def _is_excluded(path: Path, rel: str) -> bool:
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    if path.suffix in EXCLUDE_SUFFIX:
        return True
    return False


def _is_history(rel: str) -> bool:
    return any(m in rel for m in HISTORY_MARKERS)


def _is_core(rel: str) -> bool:
    return rel.startswith(CORE_DIRS)


def _iter_text_files():
    """产出 (绝对路径, 相对路径) 的文本文件"""
    for root, dirs, files in os.walk(龍魂根):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in files:
            p = Path(root) / name
            if p.suffix not in TEXT_EXTS:
                continue
            try:
                if p.stat().st_size > MAX_TEXT_SIZE:
                    continue
            except OSError:
                continue
            yield p, p.relative_to(龍魂根).as_posix()


def scan(only_list: bool = False) -> dict:
    report = {
        "引擎": "lh_glyph_unify.py v1.0",
        "铁律": "全系统统一繁体「龍」·简体「龙」禁止·只能注释不能翻译",
        "文件名违规": [],   # 文件名含简体龙
        "内容违规": [],     # (文件, 行号, 内容)
        "统计": {"扫描文件数": 0, "🔴核心": 0, "🟡普通": 0, "⚪历史提示": 0},
        "状态": "🟢",
    }

    # ── 第一遍: 文件名扫描 ──
    for root, dirs, files in os.walk(龍魂根):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in files:
            if GLYPH_SIMPLIFIED in name:
                p = Path(root) / name
                rel = p.relative_to(龍魂根).as_posix()
                if _is_excluded(p, rel):
                    continue
                if _is_history(rel):
                    report["统计"]["⚪历史提示"] += 1
                    continue
                level = "🔴" if _is_core(rel) else "🟡"
                report["文件名违规"].append({"path": rel, "level": level})
                report["统计"][("🔴核心" if level == "🔴" else "🟡普通")] += 1

    # ── 第二遍: 内容扫描 ──
    for p, rel in _iter_text_files():
        if _is_excluded(p, rel):
            continue
        report["统计"]["扫描文件数"] += 1
        if _is_history(rel):
            continue  # 历史文件只查文件名不查内容
        if rel == SELF_FILENAME or rel.endswith("/" + SELF_FILENAME):
            continue  # 检查器自身: 检测目标定义处必须出现简体字
        if rel in TOOL_EXEMPT_FILES or any(rel.endswith("/" + f) for f in TOOL_EXEMPT_FILES):
            continue  # 工具本体: 专职处理简体字·协议/示例/关键词需简体
        try:
            with open(p, "r", encoding="utf-8", errors="ignore") as f:
                for ln, line in enumerate(f, 1):
                    if GLYPH_SIMPLIFIED not in line:
                        continue
                    # ── 豁免判断 ──
                    stripped = line.lstrip()
                    # 转换器: 繁简归一代码 = 合法
                    if any(cp in line for cp in CONVERTER_PATTERNS):
                        continue
                    # 检测/统计操作: count("龙") 等 = 守卫/审计引擎合法逻辑
                    if 'count("龙")' in line or "count('龙')" in line:
                        continue
                    # 繁简对照行: 行内同时含「龙」+「龍」 = 转换/对照/说明逻辑
                    if GLYPH_TRADITIONAL in line:
                        continue
                    # 注释行: "只能注释"铁律允许在注释中说明
                    if stripped and stripped[0] in COMMENT_MARKERS:
                        continue
                    # 文档字符串内容
                    if '"""' in line or "'''" in line:
                        continue
                    level = "🔴" if _is_core(rel) else "🟡"
                    report["内容违规"].append({
                        "file": rel, "line": ln,
                        "text": line.strip()[:80], "level": level,
                    })
                    report["统计"][("🔴核心" if level == "🔴" else "🟡普通")] += 1
        except (OSError, UnicodeDecodeError):
            continue

    if report["统计"]["🔴核心"] > 0:
        report["状态"] = "🔴"
    elif report["统计"]["🟡普通"] > 0:
        report["状态"] = "🟡"
    return report


def main():
    ap = argparse.ArgumentParser(description="龍字统一检查器")
    ap.add_argument("cmd", nargs="?", default="scan", choices=["scan", "list"])
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    r = scan(only_list=args.cmd == "list")

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return

    print(f"╔══ 龍字统一检查器 v1.0 ══╗")
    print(f"铁律: 统一繁体「龍」· 简体「龙」禁止 · 只能注释不能翻译")
    print(f"扫描: {r['统计']['扫描文件数']} 文件 | 🔴核心 {r['统计']['🔴核心']} | "
          f"🟡普通 {r['统计']['🟡普通']} | ⚪历史提示 {r['统计']['⚪历史提示']}")
    print(f"状态: {r['状态']}")
    if r["文件名违规"]:
        print("\n[文件名含简体龙]")
        for it in r["文件名违规"][:20]:
            print(f"  {it['level']} {it['path']}")
        if len(r["文件名违规"]) > 20:
            print(f"  ... 共 {len(r['文件名违规'])} 个")
    if r["内容违规"]:
        print("\n[内容含简体龙]")
        for it in r["内容违规"][:20]:
            print(f"  {it['level']} {it['file']}:{it['line']}  {it['text']}")
        if len(r["内容违规"]) > 20:
            print(f"  ... 共 {len(r['内容违规'])} 个")
    print("=" * 40)


if __name__ == "__main__":
    main()
