#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丁酉·戊寅·辰时·䷝离-LH-HEALTH-v1.0-SELFTEST
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
#
# 龍魂系统自检 v1.0 — `lh health`
# 一键三色状态表：核心引擎在位 / 主控可路由 / GPG签名 / 命令索引完整性 / 全局命令
# 输出: 人类可读（默认）· --json（AI 干净可解析，符合 CIL v4.0 输出标准）

import argparse
import contextlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # longhun-system/
BIN = ROOT / "08_BIN"
CMD_INDEX = ROOT / ".codebuddy" / "COMMAND_INDEX.md"
AUTOGEN = ROOT / "docs" / "LH-COMMANDS-AUTOGEN.md"
TOPO_DIR = ROOT / "docs" / "topology"   # 知识图谱拓扑缓存 (lh topo sync)


def check_file(path: Path, name: str) -> tuple:
    ok = path.exists()
    return name, ok, "存在" if ok else "缺失", f"{path.relative_to(ROOT)}"


def check_exec(path: Path, name: str) -> tuple:
    ok = path.exists() and os.access(path, os.X_OK)
    return name, ok, "可执行" if ok else "缺失/不可执行", f"{path.relative_to(ROOT)}"


def check_asc(script: str) -> tuple:
    """GPG 分离签名文件是否在位（.asc 与源文件同目录）"""
    base = BIN / script
    asc = base.with_suffix(base.suffix + ".asc")
    ok = base.exists() and asc.exists()
    return f"{script}.asc", ok, "签名在位" if ok else "缺签名", str(asc.relative_to(ROOT))


def _dh_kb_state() -> dict:
    """数字人知识库挂载状态（lh_dh_dispatch v1.1 落盘 ~/.longhun/dh_kb_state.json）"""
    p = Path.home() / ".longhun" / "dh_kb_state.json"
    with contextlib.suppress(Exception):
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
    return {}


def kg_stats() -> dict:
    """知识图谱节点统计：聚合 docs/topology/*.topo.json（多图谱取节点最多者为主）
    含数字人知识库接入状态 kb_loaded（B4·2026-09-02）"""
    s = {"ok": False, "topo": "", "nodes": 0, "green": 0, "yellow": 0,
         "neutral": 0, "last_sync": "未同步", "where": "docs/topology/*.topo.json",
         "kb_loaded": False, "kb_entries": 0, "kb_last_load": ""}
    if not TOPO_DIR.is_dir():
        kb = _dh_kb_state()
        s.update({"kb_loaded": bool(kb.get("loaded")),
                  "kb_entries": kb.get("entries", 0),
                  "kb_last_load": kb.get("loaded_at", "")})
        return s
    best = None
    graphs = []
    for f in TOPO_DIR.iterdir():
        if not (f.is_file() and f.name.endswith("_topo.json")):
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        green = yellow = neutral = 0
        for g in d.get("groups", []):
            for a in g.get("assets", []):
                st = (a.get("status") or "").strip()
                if st.startswith("🟢"):
                    green += 1
                elif st.startswith("🟡"):
                    yellow += 1
                else:
                    neutral += 1
        total = green + yellow + neutral
        graphs.append({"topo": d.get("display", f.stem), "nodes": total,
                       "green": green, "yellow": yellow, "neutral": neutral,
                       "last_sync": d.get("last_sync", "?"),
                       "where": str(f.relative_to(ROOT))})
        if best is None or total > best["nodes"]:
            best = {"ok": bool(d.get("groups")) and total > 0,
                    "topo": d.get("display", f.stem), "nodes": total,
                    "green": green, "yellow": yellow, "neutral": neutral,
                    "last_sync": d.get("last_sync", "?"), "where": str(f.relative_to(ROOT))}
    if best is None:
        best = s
    kb = _dh_kb_state()   # 数字人知识库接入（未挂载时也如实上报 False）
    best.update({"kb_loaded": bool(kb.get("loaded")),
                 "kb_entries": kb.get("entries", 0),
                 "kb_last_load": kb.get("loaded_at", ""),
                 "kb_error": kb.get("error", ""),
                 "graphs": graphs})   # 全图谱列表 v1.3（多图谱并列，不止最大者）
    return best


def run_checks() -> list:
    results = []

    # ── 1. 主控层 ──
    results.append(check_exec(BIN / "lh.py", "lh.py 主控(08_BIN)"))
    results.append(check_exec(ROOT / "bin" / "lh.py", "lh.py 主控(bin)"))

    # ── 2. 核心引擎 ──
    for eng in ("lh_wuxing.py", "lh_cil.py", "lh_root.py",
                "lh_time_engine.py", "lh_yijing_algo_engine.py"):
        results.append(check_file(BIN / eng, f"引擎 {eng}"))

    # ── 3. CIL v4.0 可调 ──
    try:
        r = subprocess.run([sys.executable, str(BIN / "lh_cil.py"), "--version"],
                           capture_output=True, text=True, timeout=15)
        cil_ok = r.returncode == 0 and "CIL" in (r.stdout + r.stderr)
        results.append(("CIL v4.0 可调", cil_ok,
                        r.stdout.strip()[:40] if cil_ok else "调用失败", "lh cil --version"))
    except Exception as e:
        results.append(("CIL v4.0 可调", False, f"异常 {e}", "lh cil --version"))

    # ── 4. GPG 签名在位置 ──
    for eng in ("lh.py", "lh_cil.py", "lh_wuxing.py", "lh_health.py"):
        if (BIN / eng).exists():
            results.append(check_asc(eng))

    # ── 5. 命令索引完整性 ──
    if CMD_INDEX.exists():
        text = CMD_INDEX.read_text(encoding="utf-8", errors="ignore")
        missing = [k for k in ("lh health", "lh doc-sync", "lh cil", "lh wuxing")
                   if k not in text]
        idx_ok = not missing
        results.append(("COMMAND_INDEX 完整性", idx_ok,
                        "已含关键命令" if idx_ok else f"缺 {missing}",
                        ".codebuddy/COMMAND_INDEX.md"))
    else:
        results.append(("COMMAND_INDEX 完整性", False, "文件缺失", "COMMAND_INDEX.md"))

    # ── 6. 全局 lh 命令 ──
    lh_cmd = shutil.which("lh")
    if lh_cmd:
        results.append(("全局 lh 命令", True, f"→ {lh_cmd}", "任意目录可用"))
    else:
        results.append(("全局 lh 命令", False, "未注册(建议 ~/bin/lh)", "lh health"))

    # ── 7. 文档同步产物 ──
    results.append(("文档同步产物", AUTOGEN.exists(),
                    f"{AUTOGEN.stat().st_size} bytes" if AUTOGEN.exists() else "未生成(lh doc-sync)",
                    "docs/LH-COMMANDS-AUTOGEN.md"))

    # ── 8. 知识图谱拓扑节点（Notion 知识库正式接入）──
    kg = kg_stats()
    if kg["ok"]:
        results.append(("知识图谱拓扑", True,
                        f"{kg['topo']} · {kg['nodes']}节点 · 🟢{kg['green']} · 🟡{kg['yellow']}"
                        f"{(' · ⚪'+str(kg['neutral'])) if kg['neutral'] else ''}"
                        f" · 同步 {kg['last_sync']}",
                        kg["where"]))
    else:
        results.append(("知识图谱拓扑", False, "缓存缺失", "docs/topology/ (lh topo sync 通心译)"))

    return results


def render_table(results) -> str:
    lines = ["", "  🏥 龍魂系统自检 · lh health"]
    lines.append("  " + "=" * 52)
    greens = reds = yellows = 0
    for name, ok, detail, where in results:
        mark = "🟢" if ok else "🔴"
        if ok:
            greens += 1
        else:
            reds += 1
        lines.append(f"  {mark} {name:<22} {detail}")
        lines.append(f"      ↳ {where}")
    lines.append("  " + "=" * 52)
    lines.append(f"  ✅ {greens} 项就绪 · ❌ {reds} 项缺失")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="龍魂系统自检 v1.0 (lh health)")
    ap.add_argument("--json", action="store_true", help="JSON 输出（AI 可解析）")
    args = ap.parse_args()

    results = run_checks()

    # ── v2.2 Webhook 钩子: 健康检查失败 → health 事件推送（失败不影响主流程）
    try:
        fails = [(n, w) for n, ok, d, w in results if not ok]
        if fails:
            from lh_webhook import fire_event
            fire_event("health", f"健康异常 {len(fails)} 项: "
                       + " · ".join(str(n) for n, _ in fails)[:200])
    except Exception:  # noqa: BLE001
        pass

    if args.json:
        out = {
            "tool": "lh-health",
            "version": "1.1",
            "checks": [
                {"name": n, "ok": ok, "detail": d, "where": w}
                for n, ok, d, w in results
            ],
            "summary": {
                "ok": sum(1 for _, ok, _, _ in results if ok),
                "fail": sum(1 for _, ok, _, _ in results if not ok),
                "total": len(results),
            },
            "knowledge_graph": kg_stats(),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(0 if out["summary"]["fail"] == 0 else 1)

    print(render_table(results))
    sys.exit(0 if all(ok for _, ok, _, _ in results) else 1)


if __name__ == "__main__":
    main()
