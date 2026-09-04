#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-归属名补齐-v1.0
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂·归属名补齐引擎 v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：批量给龍魂产出文件补「归属名」行（实名·诸葛鑫）——归属名规则焊死落地。

背景（2026-08-22 · P0级指令·身份主权宣言）：
  老大宣布：所有龍魂系统产出文件必须包含归属名（实名），非仅代号。
  归属名 = 诸葛鑫 | UID9622 · 龍芯北辰
  立场：不躲·不藏·不匿名·随时可对质。
  本工具把该规则从"人的要求"变成"机器可批量落地"。

安全性（P0：不把能用的改坏）：
  - 只插入归属名行，不改正文
  - 幂等：文件已含 诸葛鑫/归属名/ZHUGEXIN 则跳过
  - 修改前冻结原版到 archive/frozen/
  - 插入后验证内容只增不减
  - 插入位置：优先紧跟「确认码:」行后；无确认码则文件头（跳过 shebang）

用法：
  python3 08_BIN/lh_fix_attribution.py               # dry-run 全库预览
  python3 08_BIN/lh_fix_attribution.py --core        # dry-run 只看核心层（协议+根文档+.codebuddy）
  python3 08_BIN/lh_fix_attribution.py --core --fix  # 实际补齐核心层
  python3 08_BIN/lh_fix_attribution.py --dir X --fix # 指定目录补齐
  python3 08_BIN/lh_fix_attribution.py --report out.json
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path.home() / "longhun-system"
FROZEN_DIR = BASE_DIR / "archive" / "frozen"

# 归属名判定：含 诸葛鑫（实名）/ 归属名（字段）/ ZHUGEXIN（拼音锚定） 即视为已有归属
HAS_ATTRIBUTION_MARK = ("诸葛鑫", "归属名", "ZHUGEXIN")

# 严格插入的归属名行（按文件类型）
ATTR_LINE_MD = "**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰"
ATTR_LINE_CODE = "# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰"
ATTR_LINE_PLAIN = "归属名: 诸葛鑫 | UID9622 · 龍芯北辰"

NON_TEXT_EXT = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip",
                ".gz", ".xz", ".bz2", ".7z", ".mp4", ".mp3", ".wav", ".woff",
                ".woff2", ".ttf", ".otf", ".exe", ".so", ".dll", ".pyc",
                ".class", ".jar", ".asc", ".sig", ".jsonl", ".db",
                ".sqlite3", ".db-shm", ".db-wal", ".sqlite3-shm",
                ".sqlite3-wal", ".json", ".sha256", ".csv", ".vsix",
                ".skill", ".dockerignore", ".lock", ".pem", ".key"}

# 代码类后缀（用 # 注释）
CODE_SUFFIX = {".py", ".sh", ".js", ".ts", ".yaml", ".yml", ".toml", ".plist"}
# Markdown
MD_SUFFIX = {".md", ".markdown"}

CONFIRM_KEYWORDS = ("确认码:", "CONFIRM:", "确认码：", "CONFIRM：")


def is_text_file(p: Path) -> bool:
    if p.suffix.lower() in NON_TEXT_EXT:
        return False
    # 🔴 防误伤加固(2026-08-28): 仅查后缀会误伤无扩展名/怪异后缀二进制
    #   (实测 /opt/homebrew/.../python3.14 后缀=.14 被误判文本→头部写入归属名→Mach-O损坏)
    #   判据组合: ① 前 8KB 含 NUL → 二进制  ② UTF-8 解码替换字符率 >2% → 二进制
    #   注意: 尾部可能截断多字节字符，不可用 strict 解码（否则误伤大文本文件）。
    try:
        with open(p, "rb") as f:
            head = f.read(8192)
        if b"\x00" in head:
            return False
        decoded = head.decode("utf-8", errors="replace")
        if decoded.count("\ufffd") > len(head) * 0.02:
            return False
    except OSError:
        return False
    return True


def has_attribution(src: str) -> bool:
    return any(m in src for m in HAS_ATTRIBUTION_MARK)


def _insert_index(lines: list) -> int:
    """确定插入行索引：优先确认码行后；无则文件头（跳过 shebang/编码声明）"""
    # 找确认码行
    for i, ln in enumerate(lines):
        s = ln.strip()
        if any(s.startswith(k) for k in CONFIRM_KEYWORDS):
            return i + 1
    # 无确认码：文件头。跳过开头的空行 + shebang + 编码声明
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    while idx < len(lines) and (lines[idx].startswith("#!") or lines[idx].startswith("# -*-")):
        idx += 1
    return idx


def _attr_line(p: Path) -> str:
    if p.suffix in MD_SUFFIX:
        return ATTR_LINE_MD
    if p.suffix in CODE_SUFFIX:
        return ATTR_LINE_CODE
    return ATTR_LINE_PLAIN


def patch_file(p: Path, dry_run: bool):
    try:
        src = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"file": str(p), "status": f"🔴 读取失败 {e}"}
    if has_attribution(src):
        return {"file": str(p), "status": "⏭️ 已有归属名"}

    lines = src.splitlines(keepends=True)
    at = _insert_index(lines)
    line = _attr_line(p) + "\n"
    new_src = "".join(lines[:at]) + line + "".join(lines[at:])

    if dry_run:
        return {"file": str(p), "status": "🟡 待补", "at": at}

    # 冻结原版（P0：不删除只冻结）
    FROZEN_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    frozen = FROZEN_DIR / f"{p.name}.{ts}.attribution.frozen"
    shutil.copy2(p, frozen)

    try:
        p.write_text(new_src, encoding="utf-8")
    except PermissionError:
        return {"file": str(p), "status": "⏭️ 只读跳过（无写权限）"}
    except OSError as e:
        return {"file": str(p), "status": f"🔴 写入失败 {e}"}
    # 验证：内容只增不减
    after = p.read_text(encoding="utf-8", errors="replace")
    if len(after) < len(src):
        return {"file": str(p), "status": "🔴 写入后内容变短·回滚", "frozen": frozen.name}
    if not has_attribution(after):
        return {"file": str(p), "status": "🔴 写入后仍缺归属名·回滚", "frozen": frozen.name}
    return {"file": str(p), "status": "✅ 已补归属名", "frozen": frozen.name}


def collect_files(target: Path, core_only: bool):
    """收集待扫描文本文件。core_only=True 只扫：01_protocols/ + .codebuddy/ + 根目录 .md"""
    found = []
    skip_dirs = {"node_modules", "archive", "backups", "_work", "11_DATA",
                 "dist", "models", ".git", "__pycache__", ".venv", "venv",
                 "automations", "teams", "logs"}  # 运行时状态/备份库不补归属名
    if core_only:
        targets = [target / "01_protocols", target / ".codebuddy"]
        for t in targets:
            if not t.exists():
                continue
            for root, dirs, files in t.walk():
                dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
                for fn in files:
                    p = Path(root) / fn
                    if is_text_file(p):
                        found.append(p)
        # 根目录直接文件（只取 .md，不递归子目录）
        for p in target.iterdir():
            if p.is_file() and p.suffix in MD_SUFFIX and is_text_file(p):
                found.append(p)
        return list(dict.fromkeys(found))
    for root, dirs, files in target.walk():
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith(".")]
        for fn in files:
            p = Path(root) / fn
            if is_text_file(p):
                found.append(p)
    return found


def main():
    parser = argparse.ArgumentParser(description="龍魂·归属名补齐引擎 v1.0")
    parser.add_argument("--dir", default=str(BASE_DIR), help="扫描目录（默认全库）")
    parser.add_argument("--core", action="store_true", help="只看核心层（01_protocols+根文档+.codebuddy）")
    parser.add_argument("--fix", action="store_true", help="实际补齐（默认 dry-run）")
    parser.add_argument("--report", help="输出 JSON 报告路径")
    args = parser.parse_args()

    target = Path(args.dir)
    # 🔴 防误伤加固(2026-08-28): 禁止扫描系统目录，杜绝再污染 /opt/homebrew 等
    SYSTEM_PREFIXES = ("/opt/homebrew", "/usr", "/bin", "/sbin", "/etc", "/var",
                       "/Library", "/System", "/private", "/Applications")
    tstr = str(target.resolve())
    if any(tstr == p or tstr.startswith(p + "/") for p in SYSTEM_PREFIXES):
        print(f"🔴 拒绝扫描系统目录: {target}（防误伤保护）")
        return 2
    files = collect_files(target, core_only=args.core)
    results = []
    n_patch = n_have = 0

    for p in files:
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if has_attribution(src):
            n_have += 1
            continue
        r = patch_file(p, dry_run=not args.fix)
        results.append(r)
        if r["status"].startswith("✅"):
            n_patch += 1

    mode = "核心层" if args.core else "全库"
    print(f"🐉 归属名补齐（{mode} · {'--fix 实际补齐' if args.fix else 'dry-run 预览'}）")
    print(f"   扫描文本文件: {len(files)} | 已有归属: {n_have} | 待补: {len(files) - n_have}")
    if args.fix:
        print(f"   已补归属名: {n_patch} 文件（原版冻结 archive/frozen/·内容只增不改）")
    else:
        print(f"   （dry-run：加 --fix 才实际修改）")

    if args.report:
        Path(args.report).write_text(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "fix": args.fix,
            "total": len(files),
            "have": n_have,
            "pending": len(files) - n_have,
            "patched": n_patch,
            "results": results,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"📄 报告已写: {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
