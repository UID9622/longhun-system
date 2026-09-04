#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-08-30-丙午·丙申·丙子·未时-TOPOLOGY-VERIFY-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
龍魂 · 拓扑产物校验器 v1.0（三色）
────────────────────────────────────────────
校验 web/topology-viewer 产物与 dist dmg：
  - 产物完整性（index/sw/manifest/icon.svg/icon-*.png/dmg）
  - index.html 无模板残留 · 十区块齐全 · 内嵌 JSON 可解析
  - PWA 要素（SW 注册 · manifest 图标含 PNG · apple-touch-icon）
  - dmg 可挂载（hdiutil attach/detach）

用法:
  python3 bin/lh_topology_verify.py
  可选: --out <产物目录> --dmg <dmg路径>

返回码: 0=🟢通过 1=🔴失败（有必检项失败）
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "web" / "topology-viewer"
DEFAULT_DMG = ROOT / "dist" / "龍魂拓扑.dmg"

MUST_SECTIONS = ["sec-arch", "sec-persona", "sec-neural", "sec-engine",
                 "sec-skill", "sec-digital", "sec-eco", "sec-security",
                 "sec-runtime", "sec-gate"]


def check(name: str, ok: bool, note: str = "", fatal: bool = False) -> tuple:
    """返回 (fatal_failed, all_ok)；fatal=必检项"""
    mark = "🟢" if ok else ("🔴" if fatal else "🟡")
    print(f"  {mark} {name}" + (f" · {note}" if note else ""))
    return (not ok and fatal), ok


def main() -> int:
    ap = argparse.ArgumentParser(description="龍魂拓扑产物校验器")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--dmg", type=Path, default=DEFAULT_DMG)
    args = ap.parse_args()

    out, dmg = args.out, args.dmg
    fatal_fail, all_ok = False, True

    print("── 龍魂拓扑产物校验 ──")
    print(f"[1] 产物完整性 · {out}")
    for f in ("index.html", "sw.js", "manifest.webmanifest", "icon.svg",
              "icon-180.png", "icon-192.png", "icon-512.png"):
        p = out / f
        fatal = f in ("index.html",)
        ff, ok = check(f, p.exists(), f"{p.stat().st_size//1024}KB" if p.exists() else "缺失", fatal)
        fatal_fail, all_ok = fatal_fail or ff, all_ok and ok

    print(f"[2] index.html 内容")
    html = (out / "index.html").read_text(encoding="utf-8") if (out / "index.html").exists() else ""
    ff, ok = check("模板残留清理", "__TOPODATA__" not in html, fatal=True)
    fatal_fail, all_ok = fatal_fail or ff, all_ok and ok
    missing = [s for s in MUST_SECTIONS if f'id="{s}"' not in html]
    ff, ok = check("十区块齐全", not missing, f"缺: {missing}" if missing else "10/10")
    fatal_fail, all_ok = fatal_fail or ff, all_ok and ok
    ff, ok = check("Service Worker 注册", "serviceWorker" in html and "sw.js" in html, fatal=True)
    fatal_fail, all_ok = fatal_fail or ff, all_ok and ok
    ff, ok = check("apple-touch-icon(PNG)", "icon-180.png" in html)
    fatal_fail, all_ok = fatal_fail or ff, all_ok and ok

    print("[3] 内嵌数据可解析")
    data_ok = False
    if "topoData" in html:
        import re
        m = re.search(r'<script id="topoData" type="application/json">(.*?)</script>', html, re.S)
        if m:
            try:
                data = json.loads(m.group(1))
                data_ok = True
                keys = list(data.keys())
            except Exception:
                data_ok = False
    ff, ok = check("topoData JSON 解析", data_ok, f"{len(data)} 顶层字段" if data_ok else "解析失败", fatal=True)
    fatal_fail, all_ok = fatal_fail or ff, all_ok and ok

    print(f"[4] PWA 清单 · {out / 'manifest.webmanifest'}")
    man_ok, man = False, None
    try:
        man = json.loads((out / "manifest.webmanifest").read_text(encoding="utf-8"))
        man_ok = True
    except Exception:
        pass
    ff, ok = check("manifest 可解析", man_ok, fatal=True)
    fatal_fail, all_ok = fatal_fail or ff, all_ok and ok
    if man:
        has_png = any(i.get("type") == "image/png" for i in man.get("icons", []))
        ff, ok = check("manifest 含 PNG 图标", has_png, fatal=True)
        fatal_fail, all_ok = fatal_fail or ff, all_ok and ok

    print(f"[5] dmg 可挂载 · {dmg}")
    if dmg.exists():
        mnt = "/tmp/lh_topo_verify_mnt"
        r = subprocess.run(["hdiutil", "attach", str(dmg), "-nobrowse", "-quiet",
                            "-mountpoint", mnt], capture_output=True, text=True)
        attach_ok = r.returncode == 0
        if attach_ok:
            subprocess.run(["hdiutil", "detach", mnt, "-quiet"], capture_output=True)
        ff, ok = check("dmg attach/detach", attach_ok, str(dmg.stat().st_size // 1024) + "KB", fatal=True)
        fatal_fail, all_ok = fatal_fail or ff, all_ok and ok
    else:
        ff, ok = check("dmg 存在", False, "缺失 · 先跑 lh_topology_make_dmg.sh", fatal=True)
        fatal_fail, all_ok = fatal_fail or ff, all_ok and ok

    verdict = "🔴 校验失败 · 修复后重跑" if fatal_fail else ("🟢 校验通过 · 可发布" if all_ok else "🟡 校验通过但有非必检项缺失")
    print("── " + verdict + " ──")
    return 1 if fatal_fail else 0


if __name__ == "__main__":
    sys.exit(main())
