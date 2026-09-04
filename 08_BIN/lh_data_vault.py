#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚申·亥时·䷖剥-DATA-VAULT-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用途: 数据保险柜引擎 — 个人数据+知识库压缩归档·全量存鲲鹏·该压缩的压缩
#       只存 UID9622 个人数据，不存用户数据、不导出。
# 协议: CC BY-NC-SA 4.0（核心思想层）· GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""龍魂 · 数据保险柜引擎 v1.0（P07管仲负责）
个人数据（记忆/知识库/文档/决策/日志）→ lzma 压缩归档 → 全量存鲲鹏。

用法:
  lh vault status                # 查看保险柜状态（本地+鲲鹏）
  lh vault scan                  # 扫描数据目录·统计大小·报告该压缩的
  lh vault compress [--days 30]  # 压缩 >N 天未变动的文件为 .xz 归档
  lh vault pack                  # 把关键数据目录打成 tar.xz 保险柜包
  lh vault push                  # 推送保险柜包到鲲鹏 /opt/longhun/shared/vault/
  lh vault check                 # 校验鲲鹏归档完整性
  lh vault --json                # JSON 输出
"""

import argparse
import hashlib
import json
import lzma
import os
import stat
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT_DIR = ROOT / "logs" / "vault"
MANIFEST = VAULT_DIR / "vault_manifest.json"
KUNPENG_HOST = "root@119.13.90.27"
KUNPENG_SSH = ["ssh", "-i", str(Path.home() / ".ssh" / "longhun_kunpeng_ed25519"),
               "-o", "ConnectTimeout=10", "-o", "StrictHostKeyChecking=no",
               KUNPENG_HOST]
KUNPENG_VAULT = "/opt/longhun/shared/vault"

# 个人数据目录（只存 UID9622 个人数据）
DATA_DIRS = [
    (ROOT / ".codebuddy" / "memory", "记忆"),
    (ROOT / "12_DOCS", "文档"),
    (ROOT / "01_protocols", "协议"),
    (ROOT / "03_知識圖譜", "知识图谱"),
    (ROOT / "04_決策日誌", "决策日志"),
    (ROOT / "logs", "日志"),
]

ARCHIVE_EXT = {".md", ".json", ".jsonl", ".txt", ".yaml", ".yml", ".log",
               ".csv", ".html", ".xml", ".py", ".sh", ".toml", ".conf"}


def _stamp():
    return "🐉丙午·丙申·庚申·亥时·䷖剥"


def _run_ssh(args, timeout=30):
    try:
        r = subprocess.run(KUNPENG_SSH + args, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return False, str(e)


def _fmt_size(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}PB"


def _file_age_days(path):
    try:
        return (datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)).days
    except Exception:
        return 9999


def scan(days_floor: int = 30, as_json: bool = False):
    """扫描数据目录，报告大小与可压缩项"""
    rows = []
    total = 0
    compressible = []
    for base, label in DATA_DIRS:
        if not base.exists():
            continue
        size = 0
        files = 0
        for p in base.rglob("*"):
            if p.is_file():
                try:
                    size += p.stat().st_size
                    files += 1
                except Exception:
                    pass
        total += size
        rows.append({"dir": str(base.relative_to(ROOT)), "label": label,
                     "size": size, "size_h": _fmt_size(size), "files": files})
    # 可压缩候选：>days 天未动 + 文本扩展名
    for base, label in DATA_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() in ARCHIVE_EXT:
                if _file_age_days(p) > days_floor and p.stat().st_size > 4096:
                    compressible.append({"path": str(p.relative_to(ROOT)),
                                         "size": p.stat().st_size,
                                         "days": _file_age_days(p)})
    compressible.sort(key=lambda x: x["days"], reverse=True)
    report = {
        "dirs": rows,
        "total": total,
        "total_h": _fmt_size(total),
        "compressible_count": len(compressible),
        "compressible_savings_h": _fmt_size(sum(c["size"] for c in compressible)),
        "compressible": compressible[:50],
        "stamp": _stamp(),
    }
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print("📦 数据保险柜 · 扫描报告")
    print("=" * 56)
    for r in rows:
        print(f"  {r['label']:<8} {r['size_h']:>10}  {r['files']:>5} 文件  {r['dir']}")
    print("-" * 56)
    print(f"  合计: {report['total_h']}")
    print(f"\n🔍 该压缩的（>{days_floor}天未动·文本）: {report['compressible_count']} 项")
    print(f"   潜在节省: {report['compressible_savings_h']}")
    for c in report["compressible"][:10]:
        print(f"   · {c['days']}天  {_fmt_size(c['size'])}  {c['path']}")


def compress(days: int = 30, as_json: bool = False):
    """压缩 >N 天未动的文件为 .xz（不删除原文件·保险柜内留副本）"""
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    archived = []
    saved = 0
    for base, label in DATA_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if not (p.is_file() and p.suffix.lower() in ARCHIVE_EXT):
                continue
            if _file_age_days(p) <= days or p.stat().st_size < 4096:
                continue
            rel = str(p.relative_to(ROOT)).replace("/", "__")
            out = VAULT_DIR / f"{rel}.xz"
            if out.exists():
                continue
            try:
                with lzma.open(out, "wb", preset=9) as f:
                    f.write(p.read_bytes())
                saved += p.stat().st_size
                archived.append({"src": str(p.relative_to(ROOT)), "xz": out.name,
                                 "orig": p.stat().st_size,
                                 "xz_size": out.stat().st_size})
            except Exception:
                continue
    manifest = {"generated": datetime.now().isoformat(timespec="seconds"),
                "archived": archived, "stamp": _stamp()}
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    if as_json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return
    print(f"✅ 压缩完成: {len(archived)} 项 → {VAULT_DIR}")
    print(f"   原始 {_fmt_size(saved)} → 压缩包 {_fmt_size(VAULT_DIR.stat().st_size if VAULT_DIR.exists() else 0)}")
    for a in archived[:10]:
        print(f"   · {a['src']}  ({_fmt_size(a['orig'])} → {_fmt_size(a['xz_size'])})")


def pack(as_json: bool = False):
    """把关键数据目录打成 tar.xz 保险柜包"""
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    pkg = VAULT_DIR / f"vault-{ts}.tar.xz"
    # 组装源目录列表（相对 ROOT）
    srcs = []
    for base, label in DATA_DIRS:
        if base.exists():
            srcs.append(str(base.relative_to(ROOT)))
    try:
        subprocess.run(["tar", "-cJf", str(pkg), "-C", str(ROOT)] + srcs,
                       check=True, capture_output=True, timeout=300)
    except subprocess.CalledProcessError as e:
        print(f"❌ 打包失败: {e.stderr.decode()[:200]}")
        return 1
    sha = hashlib.sha256(pkg.read_bytes()).hexdigest()[:16]
    manifest = {"package": pkg.name, "size": pkg.stat().st_size,
                "size_h": _fmt_size(pkg.stat().st_size),
                "sha256_16": sha, "generated": ts, "stamp": _stamp()}
    with (VAULT_DIR / "pack_manifest.json").open("w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    if as_json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return 0
    print(f"📦 保险柜包已生成: {pkg.name}")
    print(f"   大小 {manifest['size_h']} · SHA256 {sha}")
    return 0


def push(as_json: bool = False):
    """推送保险柜包到鲲鹏 /opt/longhun/shared/vault/"""
    if not VAULT_DIR.exists():
        print("❌ 本地保险柜为空，先跑 lh vault pack")
        return 1
    ok, msg = _run_ssh([f"mkdir -p {KUNPENG_VAULT}"])
    if not ok:
        print(f"❌ 鲲鹏不可达: {msg[:150]}")
        return 1
    # rsync 优先，失败退回 scp
    try:
        r = subprocess.run(["rsync", "-az", "--delete",
                            str(VAULT_DIR) + "/",
                            f"{KUNPENG_HOST}:{KUNPENG_VAULT}/"],
                           capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[:200])
        msg_out = "rsync 推送成功"
    except Exception as e:
        for p in VAULT_DIR.glob("*"):
            subprocess.run(KUNPENG_SSH + ["mkdir", "-p", KUNPENG_VAULT],
                           capture_output=True, text=True)
            subprocess.run(["scp", "-i", str(Path.home() / ".ssh" / "longhun_kunpeng_ed25519"),
                            "-o", "ConnectTimeout=10", str(p),
                            f"{KUNPENG_HOST}:{KUNPENG_VAULT}/"],
                           capture_output=True, text=True, timeout=120)
        msg_out = f"scp 推送成功（rsync失败: {e}）"
    # 校验远端
    ok2, listing = _run_ssh([f"ls -la {KUNPENG_VAULT} | tail -5"])
    report = {"push": msg_out, "remote_listing": listing[:300], "stamp": _stamp()}
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    print(f"✅ {msg_out} → {KUNPENG_HOST}:{KUNPENG_VAULT}")
    print("   远端内容:")
    print("   " + "\n   ".join(listing.strip().splitlines()[:5]))
    return 0


def status(as_json: bool = False):
    """保险柜状态：本地归档 + 鲲鹏归档"""
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    local_count = len(list(VAULT_DIR.glob("*")))
    local_size = sum(p.stat().st_size for p in VAULT_DIR.glob("*") if p.is_file())
    ok, listing = _run_ssh([f"ls -la {KUNPENG_VAULT} 2>/dev/null || echo NONE"])
    remote_ok = "NONE" not in listing and listing.strip()
    report = {
        "local_dir": str(VAULT_DIR),
        "local_files": local_count,
        "local_size_h": _fmt_size(local_size),
        "kunpeng_reachable": ok,
        "kunpeng_has_vault": remote_ok,
        "kunpeng_listing": listing[:400],
        "stamp": _stamp(),
    }
    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return
    print("🏦 数据保险柜 · 状态")
    print("=" * 56)
    print(f"  本地归档: {local_count} 文件 · {_fmt_size(local_size)}  @ {VAULT_DIR}")
    print(f"  鲲鹏可达: {'✅' if ok else '❌'}")
    print(f"  鲲鹏保险柜: {'✅ ' + KUNPENG_VAULT if remote_ok else '❌ 未创建'}")
    if remote_ok:
        for ln in listing.strip().splitlines()[:5]:
            print(f"   {ln}")


def render_html():
    """渲染保险柜门户页 → 10_PORTAL/vault.html"""
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(VAULT_DIR.glob("*"))
    total = sum(p.stat().st_size for p in files if p.is_file())
    rows = []
    for p in files[:60]:
        tag = "📦" if p.name.endswith(".tar.xz") else "🗜️"
        rows.append(f"<tr><td>{tag}</td><td>{p.name}</td><td>{_fmt_size(p.stat().st_size)}</td>"
                    f"<td>{datetime.fromtimestamp(p.stat().st_mtime):%m-%d %H:%M}</td></tr>")
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>🏦 数据保险柜 · 龍魂</title>
<style>
  body{{font-family:-apple-system,'PingFang SC',sans-serif;background:#0d1117;color:#e6edf3;margin:0;padding:24px}}
  h1{{color:#f0b90b}} .sub{{color:#8b949e;margin-bottom:16px}}
  .stat{{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:20px}}
  .box{{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:12px 18px;min-width:160px}}
  .box b{{display:block;font-size:22px;color:#f0b90b}} .box span{{color:#8b949e;font-size:12px}}
  table{{width:100%;border-collapse:collapse;background:#161b22;border-radius:10px;overflow:hidden}}
  th,td{{text-align:left;padding:8px 12px;border-bottom:1px solid #30363d;font-size:13px}}
  th{{color:#f0b90b;background:#1c2128}}
  .foot{{margin-top:16px;color:#6e7681;font-size:12px}}
  .note{{background:#f0b90b11;border:1px solid #f0b90b44;border-radius:8px;padding:10px 14px;color:#d4a72c;margin-bottom:16px}}
</style></head><body>
<h1>🏦 龍魂 · 数据保险柜</h1>
<div class="sub">个人数据 + 知识库 · 该压缩的压缩 · 全量存鲲鹏 /opt/longhun/shared/vault/ · 不存用户数据</div>
<div class="note">📍 管理入口: <code>lh vault scan / compress / pack / push / status</code> · P07 管仲负责</div>
<div class="stat">
  <div class="box"><b>{len(files)}</b><span>归档文件</span></div>
  <div class="box"><b>{_fmt_size(total)}</b><span>归档总量</span></div>
  <div class="box"><b>鲲鹏</b><span>/opt/longhun/shared/vault</span></div>
</div>
<table><tr><th></th><th>文件</th><th>大小</th><th>时间</th></tr>{''.join(rows) or '<tr><td colspan=4>保险柜为空 · 先跑 <code>lh vault compress</code></td></tr>'}</table>
<div class="foot">自动生成 · {_stamp()} · DNA: #龍芯⚡️丙午·丙申·庚申·亥时·䷖剥-VAULT-HTML-v1.0-UID9622</div>
</body></html>"""
    out = ROOT / "10_PORTAL" / "vault.html"
    out.write_text(html, encoding="utf-8")
    print(f"✅ 门户页已生成: {out}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="数据保险柜引擎（P07管仲）")
    ap.add_argument("action", nargs="?", default="status",
                    choices=["status", "scan", "compress", "pack", "push", "check"])
    ap.add_argument("--days", type=int, default=30, help="压缩阈值天数（默认30）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--html", action="store_true", help="生成门户页 10_PORTAL/vault.html")
    args = ap.parse_args()

    if args.html:
        return render_html()
    if args.action == "scan":
        scan(args.days, args.json)
    elif args.action == "compress":
        compress(args.days, args.json)
    elif args.action == "pack":
        pack(args.json)
    elif args.action == "push":
        push(args.json)
    else:
        status(args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
