#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔏 龍魂 CONFIRM 签名封印脚本 v1.0
DNA: #龍芯⚡️丙午·丙申·甲寅·申时·噬嗑-CONFIRM-SEAL-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

功能：扫描指定目录，为缺少确认码的文件追加 CONFIRM 签名（按文件类型自动选择注释格式）。
原则：只追加、不删除、不覆盖已有签名。
用法：
    python3 bin/lh_confirm_seal.py scan <dir>...          # 仅扫描
    python3 bin/lh_confirm_seal.py seal <dir>...          # 执行封印
    python3 bin/lh_confirm_seal.py seal --dry-run <dir>... # 试运行
"""

import hashlib
import json
import sys
import time
import importlib.util
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
ROOT = Path(__file__).resolve().parent.parent
MAX_SIZE = 5 * 1024 * 1024

IGNORE_PATTERNS = [
    ".git", "__pycache__", ".venv", "node_modules", ".DS_Store",
    ".codebuddy/memory", "agents/daemon_logs", "L7_数据层/handoff",
    "L7_数据层/data", "L7_数据层/auto_compressor", "L7_数据层/auto_crawl_daemon",
]

EXT_COMMENT = {
    ".py": ("# ", ""),
    ".sh": ("# ", ""),
    ".service": ("# ", ""),
    ".md": ("<!-- ", " -->"),
    ".html": ("<!-- ", " -->"),
    ".css": ("/* ", " */"),
    ".js": ("// ", ""),
    ".json": ("// ", ""),
    ".toml": ("# ", ""),
    ".yaml": ("# ", ""),
    ".yml": ("# ", ""),
}


@dataclass
class SealResult:
    scanned: int = 0
    already_sealed: int = 0
    sealed: int = 0
    skipped: int = 0
    errors: List[str] = field(default_factory=list)
    dna: str = ""


def _load_calendar_core():
    path = ROOT / "calendar-context-logger" / "calendar_core.py"
    spec = importlib.util.spec_from_file_location("calendar_core", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.LunarEngine()


def _dna_stamp(module: str, action: str) -> str:
    le = _load_calendar_core()
    gz = le.get_ganzhi()
    hour = int(time.strftime('%H'))
    shi_branches = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    shi = shi_branches[(hour + 1) // 2 % 12]
    base = f"{module}-{action}-{time.time()}"
    h = hashlib.sha256(base.encode()).hexdigest()[:8].upper()
    gua_names = ["乾", "坤", "屯", "蒙", "需", "讼", "师", "比", "小畜", "履", "泰", "否",
                 "同人", "大有", "谦", "豫", "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
                 "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒", "遁", "大壮", "晋", "明夷",
                 "家人", "睽", "蹇", "解", "损", "益", "夬", "姤", "萃", "升", "困", "井",
                 "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅", "巽", "兑", "涣", "节",
                 "中孚", "小过", "既济", "未济"]
    gua = gua_names[int(hashlib.sha256(base.encode()).hexdigest(), 16) % 64]
    return f"#龍芯⚡️{gz['year_zhu']}·{gz['month_zhu']}·{gz['day_zhu']}·{shi}时·{gua}-{module}-{action}-{h}"


def _should_ignore(path: Path) -> bool:
    s = str(path)
    return any(p in s for p in IGNORE_PATTERNS)


def _find_files(dirs: List[Path]) -> List[Path]:
    files = []
    for d in dirs:
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if not p.is_file():
                continue
            if p.stat().st_size > MAX_SIZE:
                continue
            if _should_ignore(p):
                continue
            if p.suffix.lower() in EXT_COMMENT or p.name in {"Dockerfile", "Makefile", ".gitignore"}:
                files.append(p)
    return files


def _comment_style(path: Path) -> Tuple[str, str]:
    ext = path.suffix.lower()
    if ext in EXT_COMMENT:
        return EXT_COMMENT[ext]
    if path.name == "Dockerfile":
        return ("# ", "")
    if path.name == "Makefile":
        return ("# ", "")
    if path.name == ".gitignore":
        return ("# ", "")
    return ("# ", "")


def _seal_file(path: Path, dry_run: bool) -> Tuple[str, str]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return "error", str(e)

    if CONFIRM in text:
        return "already_sealed", ""

    prefix, suffix = _comment_style(path)
    seal_lines = [
        f"",
        f"{prefix}CONFIRM: {CONFIRM}{suffix}",
        f"{prefix}DNA: {_dna_stamp('CONFIRM-SEAL', path.stem[:20])}{suffix}",
    ]
    if path.suffix.lower() == ".html":
        # 插入到 </body> 前，若不存在则追加到末尾
        if "</body>" in text.lower():
            new_text = text.lower().replace("</body>", "\n".join(seal_lines) + "\n</body>", 1)
            if not dry_run:
                try:
                    path.write_text(new_text, encoding="utf-8")
                except Exception as e:
                    return "error", str(e)
            return "sealed", ""

    if not dry_run:
        try:
            path.write_text(text.rstrip() + "\n" + "\n".join(seal_lines) + "\n", encoding="utf-8")
        except Exception as e:
            return "error", str(e)
    return "sealed", ""


def run(dirs: List[str], dry_run: bool = False) -> SealResult:
    result = SealResult(dna=_dna_stamp("CONFIRM-SEAL", "BATCH"))
    paths = _find_files([Path(d) for d in dirs])
    result.scanned = len(paths)
    for p in paths:
        status, err = _seal_file(p, dry_run)
        if status == "already_sealed":
            result.already_sealed += 1
        elif status == "sealed":
            result.sealed += 1
        elif status == "error":
            result.errors.append(f"{p}: {err}")
            result.skipped += 1
        else:
            result.skipped += 1
    return result


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    args = sys.argv[2:]
    dry_run = "--dry-run" in args
    dirs = [a for a in args if not a.startswith("--")]

    if cmd == "scan":
        result = run(dirs, dry_run=True)
        print(f"扫描完成：{result.scanned} 个文件")
        print(f"  已有签名：{result.already_sealed}")
        print(f"  待封印：{result.scanned - result.already_sealed}")
        return

    if cmd == "seal":
        result = run(dirs, dry_run=dry_run)
        mode = "【试运行】" if dry_run else ""
        print(f"{mode} 封印完成：")
        print(f"  扫描：{result.scanned}")
        print(f"  已有签名：{result.already_sealed}")
        print(f"  新封印：{result.sealed}")
        print(f"  跳过：{result.skipped}")
        print(f"  错误：{len(result.errors)}")
        print(f"  DNA：{result.dna}")
        # 写日志
        log = ROOT / "L7_数据层" / "strategy_reports" / "execution_logs" / f"confirm_seal_{int(time.time())}.json"
        log.parent.mkdir(parents=True, exist_ok=True)
        with open(log, "w", encoding="utf-8") as f:
            json.dump({
                "command": cmd,
                "dry_run": dry_run,
                "dirs": dirs,
                "scanned": result.scanned,
                "already_sealed": result.already_sealed,
                "sealed": result.sealed,
                "skipped": result.skipped,
                "errors": result.errors,
                "dna": result.dna,
                "timestamp": time.time(),
            }, f, ensure_ascii=False, indent=2)
        print(f"  日志：{log}")
        return

    print(__doc__)


if __name__ == "__main__":
    main()
