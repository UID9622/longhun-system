#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️2026-08-31-NEW-CONTENT-ALIGN-PROTOCOL-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
龍魂·新增内容自动对齐器 v1.0（幂等 · 缺啥补啥 · 重复跑不破坏）
协议: 01_protocols/LH-NEW-CONTENT-ALIGN-PROTOCOL-v1.0.md

功能: 新增/修改任何内容时，自动检查并补齐龍魂系统深度集成标准:
  ① 归属名（实名·诸葛鑫）② DNA 追溯码 ③ 确认码
  ④ 分层许可（md→CC BY-NC-SA 4.0 / 代码→MulanPSL v2）⑤ P0 声明（协议类）
  ⑥ GPG 签名（.asc）⑦ 反向链接（提示）⑧ 登记提示（提示）

用法:
  python3 08_BIN/lh_standard_align.py <文件或目录> [--fix]  # 对齐本次变更
  python3 08_BIN/lh_standard_align.py --git-staged [--fix]  # 对齐 git 暂存区变更
  python3 08_BIN/lh_standard_align.py scan                  # 存量巡检（只报不修·≤1次/月）

安全: 只插入标准头不改正文 · 幂等 · 二进制/数据/签名文件零触碰
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path.home() / "longhun-system"
FROZEN_DIR = BASE_DIR / "archive" / "frozen"

# ── 判定标记 ──
HAS_ATTRIBUTION = ("诸葛鑫", "归属名", "ZHUGEXIN")
HAS_DNA = ("#龍芯⚡️", "DNA:", "DNA：")
HAS_CONFIRM = ("CONFIRM", "确认码", "确认码：")
HAS_LICENSE = ("MulanPSL", "CC BY-NC-SA", "分层许可")
HAS_P0 = ("P0", "焊死", "永恒定锚")

# ── 豁免扩展名（天然无 DNA/归属名）──
NON_TEXT_EXT = {".asc", ".sig", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf",
                ".zip", ".gz", ".xz", ".bz2", ".7z", ".mp4", ".mp3", ".wav",
                ".woff", ".woff2", ".ttf", ".otf", ".exe", ".so", ".dll", ".pyc",
                ".class", ".jar", ".jsonl", ".db", ".sqlite3", ".sha256", ".csv",
                ".vsix", ".skill", ".lock", ".pem", ".key", ".plist", ".tsx",
                ".dockerignore"}
# 代码类（# 注释）
CODE_EXT = {".py", ".sh", ".js", ".ts", ".yaml", ".yml", ".toml", ".ini", ".cfg"}
# Markdown
MD_EXT = {".md", ".markdown"}

CONFIRM_LINE_CODE = "# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
CONFIRM_LINE_MD = "> CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
LICENSE_CODE = "# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)"
LICENSE_MD = "> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·详见 LH-LAYERED-LICENSE-v1.0）"
P0_LINE_MD = "> 【文档性质】P0-ETERNAL（永恒定锚级）"
ATTR_CODE = "# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰"
ATTR_MD = "归属名: 诸葛鑫 | UID9622 · 龍芯北辰"

# 协议类文件名提示（文件名含这些词视为协议/铁律）
PROTOCOL_HINT = ("协议", "protocol", "PROTOCOL", "宪法", "铁律", "CONTRACT",
                 "SOVEREIGNTY", "KILL-SWITCH", "LAW", "WELD")


def is_text_file(p: Path) -> bool:
    """文本判定：后缀豁免 + 前8KB无NUL + UTF-8替换率<=2%"""
    if p.suffix.lower() in NON_TEXT_EXT:
        return False
    if not p.suffix:  # 无后缀不可判定
        return False
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


def is_protocol_file(name: str) -> bool:
    return any(h in name for h in PROTOCOL_HINT)


def read_safe(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _insert_after(lines: list, keyword: str, new_line: str) -> list:
    """在首个含 keyword 的行后插入；无则文件头（跳 shebang/编码声明/空行）"""
    for i, ln in enumerate(lines):
        if keyword in ln:
            lines.insert(i + 1, new_line)
            return lines
    idx = 0
    while idx < len(lines) and (not lines[idx].strip() or lines[idx].startswith(("#!", "# -*-"))):
        idx += 1
    lines.insert(idx, new_line)
    return lines


def _insert_head(lines: list, new_line: str) -> list:
    idx = 0
    while idx < len(lines) and (not lines[idx].strip() or lines[idx].startswith(("#!", "# -*-"))):
        idx += 1
    lines.insert(idx, new_line)
    return lines


def check_file(p: Path):
    """返回 (missing_set, is_protocol)"""
    if not p.exists() or not is_text_file(p):
        return None, False
    c = read_safe(p)
    proto = is_protocol_file(p.name)
    missing = set()
    if not any(m in c for m in HAS_ATTRIBUTION):
        missing.add("归属名")
    if not any(m in c for m in HAS_DNA):
        missing.add("DNA")
    if not any(m in c for m in HAS_CONFIRM):
        missing.add("确认码")
    if not any(m in c for m in HAS_LICENSE):
        missing.add("许可")
    if proto and not any(m in c for m in HAS_P0):
        missing.add("P0")
    return missing, proto


def fix_file(p: Path) -> list:
    """补齐标准头，返回修复动作列表（幂等）"""
    missing, proto = check_file(p)
    if missing is None:
        return []
    actions = []
    try:
        raw = p.read_bytes()
        lines = raw.decode("utf-8").split("\n")
    except Exception:
        return []

    ext = p.suffix.lower()
    is_code = ext in CODE_EXT
    is_md = ext in MD_EXT

    # 冻结原版（仅首次修改时）
    if missing:
        fname = f"{p.name}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.align"
        try:
            FROZEN_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, FROZEN_DIR / fname)
        except Exception:
            pass

    if "归属名" in missing:
        line = ATTR_CODE if is_code else ATTR_MD
        lines = _insert_head(lines, line)
        actions.append("归属名")
    if "确认码" in missing:
        line = CONFIRM_LINE_CODE if is_code else CONFIRM_LINE_MD
        lines = _insert_head(lines, line)
        actions.append("确认码")
    if "许可" in missing:
        line = LICENSE_CODE if is_code else LICENSE_MD
        lines = _insert_head(lines, line)
        actions.append("许可")
    if proto and "P0" in missing:
        lines = _insert_head(lines, P0_LINE_MD)
        actions.append("P0")
    if "DNA" in missing:
        dna = f"# DNA: #龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{_slug(p.stem)}-v1.0-UID9622"
        lines = _insert_head(lines, dna)
        actions.append("DNA")

    try:
        p.write_text("\n".join(lines), encoding="utf-8")
    except Exception:
        return []
    return actions


def _slug(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff_-]+", "-", name).strip("-")
    return s[:48] or "NEW"


def sign_file(p: Path) -> bool:
    """GPG 分离签名（.asc 与源同目录）"""
    asc = Path(str(p) + ".asc")
    if asc.exists():
        return False  # 已签名
    script = BASE_DIR / "bin" / "lh_gpg_sign.py"
    if not script.exists():
        return False
    try:
        r = subprocess.run([sys.executable, str(script), "sign", "--force", str(p)],
                           capture_output=True, text=True, timeout=60)
        return asc.exists()
    except Exception:
        return False


def align(targets, fix: bool) -> dict:
    report = {"checked": 0, "fixed": 0, "signed": 0, "ok": 0, "issues": []}
    for p in targets:
        missing, proto = check_file(p)
        if missing is None:
            continue
        report["checked"] += 1
        if missing:
            if fix:
                acts = fix_file(p)
                # 补完后重新检查
                missing2, _ = check_file(p)
                if missing2:
                    report["issues"].append(f"{p}: 修复后仍缺 {missing2}")
                else:
                    report["fixed"] += len(acts)
                    # 补完后自动签名（若缺 .asc）
                    if sign_file(p):
                        report["signed"] += 1
            else:
                report["issues"].append(f"{p}: 缺 {sorted(missing)}")
        else:
            report["ok"] += 1
            # 无缺项但缺签名 → 提示（fix 时补）
            if not Path(str(p) + ".asc").exists():
                if fix:
                    if sign_file(p):
                        report["signed"] += 1
                else:
                    report["issues"].append(f"{p}: 🟡 缺GPG签名(需 --fix)")
    return report


def collect(paths) -> list:
    out = []
    for p in paths:
        p = Path(p)
        if p.is_dir():
            for root, dirs, files in os.walk(p):
                # 节能：跳过大目录
                dirs[:] = [d for d in dirs if d not in
                           (".git", "node_modules", ".venv", "weights", "models",
                            "dist", "archive", "backups", "_work", "11_DATA", ".codebuddy")]
                for f in files:
                    out.append(Path(root) / f)
        elif p.exists():
            out.append(p)
    return out


def main():
    parser = argparse.ArgumentParser(description="🐉 龍魂·新增内容自动对齐器 v1.0")
    parser.add_argument("targets", nargs="*", help="文件或目录")
    parser.add_argument("--fix", action="store_true", help="自动修复（幂等）")
    parser.add_argument("--git-staged", action="store_true", help="对齐 git 暂存区变更")
    args = parser.parse_args()

    if args.git_staged:
        r = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                           capture_output=True, text=True, cwd=BASE_DIR)
        targets = [Path(BASE_DIR) / f for f in r.stdout.strip().split("\n") if f]
    else:
        targets = collect(args.targets)

    if not targets:
        print("✅ 无目标文件")
        return 0

    rep = align(targets, args.fix)

    # 节能输出（≤3行）
    line1 = f"🐉 对齐器: 检查{rep['checked']} · 已对齐{rep['ok']} · 修复{rep['fixed']}项 · 补签{rep['signed']}"
    if rep["issues"]:
        print(line1)
        for i in rep["issues"][:5]:
            print(f"  🟡 {i}")
    else:
        print(f"🟢 {line1} · 全绿")
    return 0 if not rep["issues"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
