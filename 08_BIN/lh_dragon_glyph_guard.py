#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·#龍芯⚡️丙午·丙申·POSTAUDIT-LH_DRAGON_GLYPH_GUAR-BBEDD978
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍芯⚡️丙午·丙申·辛酉·未时·☰乾-DRAGON-GLYPH-GUARD-v1.0
"""
🐉 龍魂 · 龍字主权守卫 v1.0

协议:
  1. 所有简体中文「龙」自动升级为繁体文化主权字「龍」。
  2. 英文/代码/URL/标识符保持原样，不误伤。
  3. 「龍芯⚡️」为文化主权符号，永不翻译、永不改写。
  4. 输出带 DNA 追溯，可审计。

用法:
  echo "龙魂系统" | python3 08_BIN/lh_dragon_glyph_guard.py
  python3 08_BIN/lh_dragon_glyph_guard.py --input file.txt --output file.txt
  python3 08_BIN/lh_dragon_glyph_guard.py --fix-repo  # 扫描仓库文本文件
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


# 不应被改写的上下文（URL、代码标识符、hex、emoji 短码等）
SKIP_PATTERNS = [
    r"https?://\S+",
    r"\b[a-fA-F0-9]{6,}\b",
    r"\b[\w.-]+@[\w.-]+\.\w+\b",
    r":\w+:",
    r"`[^`]+`",
]


def _now() -> str:
    return datetime.now().isoformat()


def _dna() -> str:
    return f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-DRAGON-GLYPH-GUARD"


def guard_text(text: str) -> str:
    """将文本中的简体「龙」安全升级为「龍」。"""
    if not text:
        return text

    # 先保护跳过区间
    protected = []
    placeholders = []
    placeholder_id = 0
    working = text

    for pat in SKIP_PATTERNS:
        for m in re.finditer(pat, working):
            ph = f"\x00{placeholder_id}\x00"
            placeholders.append((ph, m.group()))
            placeholder_id += 1
        for ph, orig in placeholders:
            working = working.replace(orig, ph, 1)

    # 升级龙字（保留已有龍字）
    working = working.replace("龙", "龍")

    # 恢复保护区间
    for ph, orig in placeholders:
        working = working.replace(ph, orig, 1)

    return working


def guard_file(path: Path, inplace: bool = False) -> dict:
    text = path.read_text(encoding="utf-8")
    new_text = guard_text(text)
    changed = new_text != text
    if changed and inplace:
        path.write_text(new_text, encoding="utf-8")
    return {
        "path": str(path),
        "changed": changed,
        "replacements": text.count("龙"),
        "dna": _dna(),
    }


def scan_repo(root: Path, inplace: bool = False) -> list:
    """扫描仓库文本文件。"""
    results = []
    # 常见文本扩展名
    exts = {
        ".py", ".md", ".txt", ".json", ".jsonl", ".yaml", ".yml",
        ".sh", ".bash", ".zsh", ".cnsh", ".toml", ".cfg", ".ini",
    }
    exclude = {
        ".git", ".venv", "__pycache__", "node_modules", ".kimi-code",
        ".cache", ".idea", ".vscode", ".longhun", "models",
    }
    for p in root.rglob("*"):
        if any(part in exclude for part in p.parts):
            continue
        if p.is_file() and p.suffix.lower() in exts:
            try:
                res = guard_file(p, inplace=inplace)
                if res["changed"]:
                    results.append(res)
            except Exception as e:
                results.append({
                    "path": str(p),
                    "error": str(e),
                    "dna": _dna(),
                })
    return results


def guard_jsonl(in_path: Path, out_path: Path) -> dict:
    """处理 jsonl 文件：递归守卫所有字符串值（安全原地写）。"""
    count = 0
    tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
    with open(in_path, "r", encoding="utf-8") as fin, open(tmp_path, "w", encoding="utf-8") as fout:
        for line in fin:
            if not line.strip():
                continue
            obj = json.loads(line)

            def _walk(o):
                nonlocal count
                if isinstance(o, str):
                    before = o.count("龙")
                    o = guard_text(o)
                    count += before
                    return o
                elif isinstance(o, list):
                    return [_walk(x) for x in o]
                elif isinstance(o, dict):
                    return {k: _walk(v) for k, v in o.items()}
                return o

            obj = _walk(obj)
            fout.write(json.dumps(obj, ensure_ascii=False) + "\n")
    tmp_path.replace(out_path)
    return {"path": str(out_path), "replacements": count}


def main():
    parser = argparse.ArgumentParser(description="龍魂 · 龍字主权守卫")
    parser.add_argument("--input", help="输入文件（默认 stdin）")
    parser.add_argument("--output", help="输出文件（默认 stdout）")
    parser.add_argument("--jsonl", action="store_true", help="按 jsonl 格式处理（逐行 JSON）")
    parser.add_argument("--fix-repo", action="store_true", help="扫描并修复仓库文本文件")
    parser.add_argument("--dry-run", action="store_true", help="只报告不写入")
    args = parser.parse_args()

    if args.fix_repo:
        root = Path(__file__).resolve().parent.parent
        results = scan_repo(root, inplace=not args.dry_run)
        total = sum(r.get("replacements", 0) for r in results if "error" not in r)
        print(json.dumps({
            "dna": _dna(),
            "timestamp": _now(),
            "mode": "dry-run" if args.dry_run else "inplace",
            "files_changed": len(results),
            "total_replacements": total,
            "details": results[:50],
        }, ensure_ascii=False, indent=2))
        return

    if args.jsonl and args.input:
        in_path = Path(args.input)
        out_path = Path(args.output) if args.output else in_path
        res = guard_jsonl(in_path, out_path)
        print(json.dumps({"dna": _dna(), "timestamp": _now(), **res}, ensure_ascii=False))
        return

    if args.input:
        text = Path(args.input).read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    out = guard_text(text)

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"✅ 已输出: {args.output}")
    else:
        sys.stdout.write(out)


if __name__ == "__main__":
    main()
