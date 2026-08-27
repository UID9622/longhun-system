#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 压缩枢纽引擎 v1.0 (COMPRESS HUB)
DNA: #龍芯⚡️丙午·丙申·戊申·申时·䷯井-COMPRESS-HUB-ENGINE-v1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

统一压缩枢纽：把「快照备份 → 语义压缩 → 人格编排 → 恢复全文」焊成一个闭环。
压缩前强制快照全文（可恢复），压缩后自动联动人格编排审计。

用法:
    python3 bin/lh_compress_hub.py run [--persona] [--no-snapshot]
    python3 bin/lh_compress_hub.py restore <文件路径>
    python3 bin/lh_compress_hub.py list [--detail]
    python3 bin/lh_compress_hub.py audit
    python3 bin/lh_compress_hub.py watch [--interval 3600]

子命令:
    run       快照备份 → 调 compress_all --run 压缩 → 联动人格编排 → 战报
    restore   从最新快照恢复指定文件全文（可恢复）
    list      列出快照/备份记录
    audit     只扫描超限文件（不写不压）
    watch     守护模式：定时自动触发 run（自动压缩+人格编排）
"""

import json
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# ────────────────────────────────────────────────
# § 0 常量
# ────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_ROOT = ROOT / "_work" / "compress_vault"
MANIFEST = SNAPSHOT_ROOT / "index.json"
ORCHESTRATOR = ROOT / "bin" / "lh_persona_orchestrator.py"
COMPRESS_ALL = ROOT / "bin" / "compress_all.py"
TIME_ENGINE = ROOT / "bin" / "lh_time_engine.py"
MAX_SNAPSHOTS = 20          # 快照保留上限（超限删最旧）
DEFAULT_INTERVAL = 3600     # watch 默认间隔（秒）

# 受管文件清单（与 compress_all.py 对齐；快照覆盖全部，恢复可覆盖压缩/报告两类）
MANAGED_PATTERNS = [
    (".codebuddy/memory/MEMORY.md", 7_500),
    (".codebuddy/COMMAND_INDEX.md", 12_000),
    (".codebuddy/memory/2026-*.md", 5_000),
]

# 默认人格链：P03归档 → P05审计 → P06验证 → P15签章（压缩审计闭环）
DEFAULT_PERSONA_CHAIN = "P03→P05→P06→P15"


def stamp() -> str:
    """取系统时间戳（full 格式）；引擎不可达时降级纯时间。"""
    try:
        r = subprocess.run(
            ["python3", str(TIME_ENGINE), "--stamp"],
            capture_output=True, text=True, timeout=15,
        )
        out = (r.stdout or "").strip()
        if out:
            return out.splitlines()[-1]
    except Exception:
        pass
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")


def snap_hash(text: bytes) -> str:
    """sha256 前 12 位（禁 MD5，规则第七层）。"""
    import hashlib
    return hashlib.sha256(text).hexdigest()[:12]


def _safe_name(path: Path) -> str:
    """相对路径转快照安全名（/ → __）。"""
    try:
        rel = path.resolve().relative_to(ROOT.resolve())
    except ValueError:
        rel = path.name
    return str(rel).replace("/", "__")


def managed_files() -> List[Path]:
    """扫描受管文件（存在才返回）。"""
    out = []
    for pattern, _limit in MANAGED_PATTERNS:
        for f in sorted(ROOT.glob(pattern)):
            if f.exists():
                out.append(f)
    return out


# ────────────────────────────────────────────────
# § 1 快照备份（可恢复全文的核心）
# ────────────────────────────────────────────────

def snapshot_all(force: bool = False) -> Dict[str, Any]:
    """
    压缩前把受管文件全文快照到 _work/compress_vault/<ts>/。
    返回记录清单；index.json 追加（append-only 审计）。
    """
    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    snap_dir = SNAPSHOT_ROOT / ts
    snap_dir.mkdir(parents=True, exist_ok=True)

    records = []
    for f in managed_files():
        raw = f.read_bytes()
        h = snap_hash(raw)
        dest = snap_dir / f"{h}__{_safe_name(f)}"
        shutil.copy2(f, dest)
        records.append({
            "file": str(f.relative_to(ROOT)),
            "snapshot": str(dest.relative_to(ROOT)),
            "sha256": h,
            "bytes": len(raw),
            "ts": ts,
        })

    # 追加 manifest（append-only）
    manifest_records = []
    if MANIFEST.exists():
        try:
            manifest_records = json.loads(MANIFEST.read_text(encoding="utf-8"))
            if not isinstance(manifest_records, list):
                manifest_records = []
        except Exception:
            manifest_records = []
    manifest_records.extend(records)

    # 快照上限裁剪（删最旧目录）
    snap_dirs = sorted([d for d in SNAPSHOT_ROOT.iterdir() if d.is_dir()])
    while len(snap_dirs) > MAX_SNAPSHOTS:
        oldest = snap_dirs.pop(0)
        shutil.rmtree(oldest, ignore_errors=True)
        manifest_records = [r for r in manifest_records if not r["snapshot"].startswith(f"_work/compress_vault/{oldest.name}")]

    MANIFEST.write_text(
        json.dumps(manifest_records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"📸 快照完成: {len(records)} 个文件 → {snap_dir.relative_to(ROOT)}/")
    for r in records:
        print(f"   · {r['file']}  ({r['bytes']:,}B · sha256={r['sha256']})")
    return {"ts": ts, "records": records}


def restore_file(target: str, dry_run: bool = False) -> Dict[str, Any]:
    """
    从最新快照恢复指定文件全文。
    target 可以是受管文件路径（.codebuddy/memory/MEMORY.md）或文件名（MEMORY.md）。
    """
    if not MANIFEST.exists():
        print("❌ 无快照索引（从未压缩过）")
        return {"ok": False, "reason": "no_snapshot"}

    try:
        records = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        records = []

    target = str(target)
    matches = []
    for r in records:
        if r["file"] == target or Path(r["file"]).name == Path(target).name:
            matches.append(r)

    if not matches:
        print(f"❌ 快照中找不到: {target}")
        print(f"   可用文件: {sorted({r['file'] for r in records})}")
        return {"ok": False, "reason": "not_found"}

    # 取最新一条
    latest = sorted(matches, key=lambda r: r["ts"])[-1]
    snap_path = ROOT / latest["snapshot"]
    if not snap_path.exists():
        print(f"❌ 快照文件丢失: {latest['snapshot']}")
        return {"ok": False, "reason": "snapshot_lost"}

    dest = ROOT / latest["file"]
    if dry_run:
        print(f"🔍 预演恢复: {snap_path.relative_to(ROOT)} → {latest['file']} "
              f"({latest['bytes']:,}B · sha256={latest['sha256']})")
        return {"ok": True, "dry_run": True}

    shutil.copy2(snap_path, dest)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"✅ 已恢复全文: {latest['file']}  ({latest['bytes']:,}B · sha256={latest['sha256']})")
    print(f"   ⏱ 快照时间: {latest['ts']} · 恢复时间: {now}")
    return {"ok": True, "file": latest["file"], "bytes": latest["bytes"]}


def list_snapshots(detail: bool = False) -> None:
    """列出快照索引。"""
    if not MANIFEST.exists():
        print("📭 无快照记录")
        return
    try:
        records = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        print("❌ 快照索引损坏")
        return

    by_ts: Dict[str, List] = {}
    for r in records:
        by_ts.setdefault(r["ts"], []).append(r)

    print(f"🗂  压缩快照索引 · 共 {len(records)} 条记录 · {len(by_ts)} 次压缩")
    for ts in sorted(by_ts, reverse=True):
        recs = by_ts[ts]
        total = sum(r["bytes"] for r in recs)
        print(f"  · {ts}  文件 {len(recs)} 个 · 全文 {total:,}B")
        if detail:
            for r in recs:
                print(f"      - {r['file']} ({r['bytes']:,}B · {r['sha256']})")

    print("\n💡 恢复用法: python3 bin/lh_compress_hub.py restore <文件路径>")


# ────────────────────────────────────────────────
# § 2 人格编排联动
# ────────────────────────────────────────────────

def run_persona_chain(chain: str = DEFAULT_PERSONA_CHAIN, task: str = "") -> Dict[str, Any]:
    """调用人格编排器跑人格链（P03归档→P05审计→P06验证→P15签章）。"""
    if not ORCHESTRATOR.exists():
        print("  ⚠️ 人格编排器缺失，跳过联动")
        return {"ok": False, "reason": "missing_orchestrator"}

    task = task or f"压缩枢纽审计 {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    cmd = ["python3", str(ORCHESTRATOR), "--pipeline", chain, "--task", task]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        out = (r.stdout or "").strip()
        if r.returncode == 0:
            print(f"  🧩 人格链 [{chain}] 执行完成 · 见上方输出")
            # 简要摘要
            lines = [l.strip() for l in out.splitlines() if l.strip()]
            summary = lines[-12:] if len(lines) > 12 else lines
            print("  " + "\n  ".join(summary))
        else:
            print(f"  ⚠️ 人格链退出码 {r.returncode}: {(r.stderr or '')[:200]}")
        return {"ok": r.returncode == 0, "chain": chain}
    except subprocess.TimeoutExpired:
        print("  ⚠️ 人格链超时（180s），继续主流程")
        return {"ok": False, "reason": "timeout"}


# ────────────────────────────────────────────────
# § 3 主流程
# ────────────────────────────────────────────────

def run_compress(persona: bool = True, snapshot: bool = True, dry_run: bool = False) -> Dict[str, Any]:
    """
    压缩枢纽主流程：
      快照备份 → compress_all --run → 人格编排 → 战报
    """
    ts = stamp()
    print(f"🐉 龍魂 · 压缩枢纽引擎 v1.0  {ts}")
    print("─" * 60)

    result: Dict[str, Any] = {"ts": ts, "persona": persona, "snapshot": snapshot}

    # 1. 快照备份（可恢复全文）
    if snapshot:
        snap = snapshot_all()
        result["snapshot_records"] = len(snap["records"])
    else:
        print("  ⏭️ 已跳过快照（--no-snapshot）")

    # 2. 全库扫描压缩
    print("\n🗜️ 全库扫描压缩...")
    ca_cmd = ["python3", str(COMPRESS_ALL), "--run"]
    if dry_run:
        ca_cmd = ["python3", str(COMPRESS_ALL), "--dry-run"]
    r = subprocess.run(ca_cmd, text=True, timeout=600)
    result["compress_exit"] = r.returncode

    # 3. 人格编排联动（自动启动人格审计）
    if persona:
        print("\n🧩 联动人格编排...")
        pr = run_persona_chain(task="压缩枢纽审计 · 快照→压缩→验证闭环")
        result["persona_result"] = pr

    print("\n✅ 压缩枢纽完成 · 全文快照已存档（可 restore 恢复）")
    return result


def watch_mode(interval: int) -> None:
    """守护模式：定时自动触发 run（自动压缩+人格编排）。"""
    print(f"👁️ 压缩枢纽守护模式 · 每 {interval}s 自动巡检压缩")
    print(f"   受管文件: {[p for p, _ in MANAGED_PATTERNS]}")
    print("   Ctrl+C 退出\n")
    while True:
        try:
            run_compress(persona=True, snapshot=True)
            print(f"\n😴 休眠 {interval}s ...  {stamp()}\n")
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 守护退出")
            break
        except Exception as e:
            print(f"⚠️ 巡检异常: {e}")
            time.sleep(60)


def audit_only() -> None:
    """只扫描超限文件，不写不压。"""
    r = subprocess.run(["python3", str(COMPRESS_ALL), "--audit"], text=True, timeout=300)
    sys.exit(r.returncode)


# ────────────────────────────────────────────────
# § 4 入口
# ────────────────────────────────────────────────

def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.split("用法:")[0])
        print(__doc__.split("用法:")[1].split("子命令:")[0])
        print("子命令:")
        print("  run          快照→压缩→人格编排（默认全开）")
        print("  restore <f>  从最新快照恢复全文")
        print("  list         列出快照索引")
        print("  audit        只扫描超限文件")
        print("  watch        守护模式自动触发")
        return 0

    cmd = args[0]

    if cmd == "run":
        persona = "--no-persona" not in args
        snapshot = "--no-snapshot" not in args
        dry = "--dry-run" in args
        run_compress(persona=persona, snapshot=snapshot, dry_run=dry)
        return 0

    if cmd == "restore":
        if len(args) < 2:
            print("❌ 用法: lh_compress_hub.py restore <文件路径>")
            return 1
        dry = "--dry-run" in args
        restore_file(args[1], dry_run=dry)
        return 0

    if cmd == "list":
        list_snapshots(detail="--detail" in args)
        return 0

    if cmd == "audit":
        audit_only()
        return 0

    if cmd == "watch":
        interval = DEFAULT_INTERVAL
        if "--interval" in args:
            try:
                i = args.index("--interval")
                interval = int(args[i + 1])
            except (ValueError, IndexError):
                pass
        watch_mode(interval)
        return 0

    print(f"❌ 未知子命令: {cmd}（用 --help 查看用法）")
    return 1


if __name__ == "__main__":
    sys.exit(main())
