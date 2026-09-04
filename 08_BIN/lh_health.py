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
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # longhun-system/
BIN = ROOT / "08_BIN"
CMD_INDEX = ROOT / ".codebuddy" / "COMMAND_INDEX.md"
AUTOGEN = ROOT / "docs" / "LH-COMMANDS-AUTOGEN.md"
TOPO_DIR = ROOT / "docs" / "topology"   # 知识图谱拓扑缓存 (lh topo sync)
DOCS_DIR = ROOT / "12_DOCS"             # 对外交付文档 (lh docs check / docs_version)


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


def _notion_mirror_state() -> dict:
    """Notion 数据主控镜像状态（目录快照 catalog.json · 无正文主权在主控）"""
    p = Path.home() / ".longhun" / "notion_mirror" / "catalog.json"
    s = {"catalog": False, "ok": False, "pages": 0, "synced_at": "", "stale_days": None}
    if not p.is_file():
        return s
    s["catalog"] = True
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        s["pages"] = int((d.get("meta") or {}).get("pages", 0))
        s["synced_at"] = (d.get("meta") or {}).get("synced_at", "")
        s["ok"] = s["pages"] > 0
        import datetime
        at = s["synced_at"][:19]
        for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
            try:
                dt = datetime.datetime.strptime(at, fmt)
                days = (datetime.datetime.now() - dt).days
                s["stale_days"] = days if days > 7 else None
                break
            except ValueError:
                continue
    except Exception:
        pass
    return s


def _dh_kb_state() -> dict:
    """数字人知识库挂载状态（lh_dh_dispatch v1.1 落盘 ~/.longhun/dh_kb_state.json）"""
    p = Path.home() / ".longhun" / "dh_kb_state.json"
    with contextlib.suppress(Exception):
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))
    return {}


def _docs_version() -> str:
    """对外文档版本：扫 12_DOCS/*.md 文件头 DNA 行时间戳，取最新 YYYY-MM-DD
    (lh docs check 同口径 · 只认每文件首个 DNA · 缺文档返回 'none')"""
    import re as _re
    pat = _re.compile(r"#龍(?:芯|帳)⚡️[^\n]*?(\d{4}-\d{2}-\d{2})")
    best = ""
    try:
        for p in DOCS_DIR.glob("*.md"):
            txt = p.read_text(encoding="utf-8", errors="ignore")[:900]
            m = pat.search(txt)
            if m and m.group(1) > best:
                best = m.group(1)
    except Exception:  # noqa: BLE001
        pass
    return best or "none"


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


def _sense_stats() -> dict:
    """lh_sense v2.0 感知审计统计（三色闭环 · 读 ~/.longhun/sense_audit.jsonl）"""
    p = Path.home() / ".longhun" / "sense_audit.jsonl"
    s = {"ok": p.is_file(), "total": 0, "green": 0, "yellow": 0, "red": 0,
         "last": "", "where": "~/.longhun/sense_audit.jsonl"}
    if not p.is_file():
        return s
    try:
        for line in p.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
            except Exception:
                continue
            s["total"] += 1
            c = e.get("color")
            if c == "🟢":
                s["green"] += 1
            elif c == "🟡":
                s["yellow"] += 1
            elif c == "🔴":
                s["red"] += 1
            s["last"] = e.get("ts", "") or s["last"]
    except Exception:
        pass
    return s


def _ledger_stats() -> dict:
    """📒 龍魂账法统计（读 ~/.longhun/ledger/ · 2026-09-04）"""
    root = Path.home() / ".longhun" / "ledger"
    s = {"ok": False, "tx_total": 0, "pending": 0, "meltdown": 0,
         "last_dna": "", "last_ts": "", "balance_ok": None,
         "where": "~/.longhun/ledger/"}
    tx_p = root / "transactions.jsonl"
    if not tx_p.is_file():
        return s
    s["ok"] = True
    try:
        last = None
        for line in tx_p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except Exception:
                continue
            s["tx_total"] += 1
            last = e
        if last:
            s["last_dna"] = last.get("dna", "")
            s["last_ts"] = last.get("created_at", "")
        f_pend = root / "pending.jsonl"
        if f_pend.is_file():
            s["pending"] = sum(1 for ln in f_pend.read_text(encoding="utf-8")
                               .splitlines() if ln.strip())
        f_melt = root / "meltdown.jsonl"
        if f_melt.is_file():
            s["meltdown"] = sum(1 for ln in f_melt.read_text(encoding="utf-8")
                                .splitlines() if ln.strip())
    except Exception:
        pass
    return s


def _topo_root_check() -> tuple:
    """拓扑根哈希持续自检(v2.2·2026-09-05): 本地重算 vs 线上公开 uid9622.cn/api/topo/status.json
    算法与 lh_topo.topo_root_hash 同口径: group|name|dna 行排序聚合 → SHA-256 前 16 位
    一致🟢 / 不一致🔴(篡改或未同步·立即 export-page) / 线上不可达🟡(待复查·不计硬失败)"""
    import hashlib as _h
    import urllib.request as _u
    p = TOPO_DIR / "对外交付_legion_topo.json"
    if not p.is_file():
        return ("拓扑根哈希在线一致", False, "本地图谱缺失",
                "docs/topology/对外交付_legion_topo.json · lh topo sync 对外交付", "🔴")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        lines = []
        for g in data.get("groups", []):
            for a in g.get("assets", []):
                lines.append(f"{g.get('name')}|{a.get('name')}|{a.get('dna') or ''}")
        local = _h.sha256("\n".join(sorted(lines)).encode("utf-8")).hexdigest()[:16].upper()
    except Exception as e:  # noqa: BLE001
        return ("拓扑根哈希在线一致", False, f"本地重算失败 {e}",
                "docs/topology/对外交付_legion_topo.json", "🔴")
    try:
        req = _u.Request("https://uid9622.cn/api/topo/status.json",
                         headers={"User-Agent": "longhun-health/2.2"})
        with _u.urlopen(req, timeout=8) as r:
            online = str((json.loads(r.read().decode("utf-8")) or {}).get("root_hash", ""))
    except Exception as e:  # noqa: BLE001
        return ("拓扑根哈希在线一致", False,
                f"本地 {local} · 线上不可达({type(e).__name__})",
                "uid9622.cn/api/topo/status.json · lh health 下次复查", "🟡")
    if online.upper() == local:
        return ("拓扑根哈希在线一致", True, f"{local} · 本地 = 线上 ✓",
                "docs/topology ↔ uid9622.cn/api/topo/status.json", "🟢")
    return ("拓扑根哈希在线一致", False,
            f"本地 {local} ≠ 线上 {online}",
            "不一致=篡改/未同步 · 立即 lh topo export-page 对外交付", "🔴")


def _topo_event_state() -> dict:
    """拓扑变更事件审计（v1.9 耻辱墙联动 · 读 ~/.longhun/shame_wall/topo_audit.jsonl）
    最近一条事件为移除/告警（warning）→ 🟡 提醒查看 events；否则 🟢（自愈式，下次正常变更即恢复）"""
    base = {"name": "拓扑变更审计(耻辱墙)", "ok": True, "mark": "🟢",
            "detail": "无未处理事件 · 事件流 append-only",
            "where": "~/.longhun/shame_wall/topo_audit.jsonl · lh topo 对外交付 events"}
    p = Path.home() / ".longhun" / "shame_wall" / "topo_audit.jsonl"
    if not p.is_file():
        return {**base, "detail": "事件流未建立（拓扑首次变更后自动生成）"}
    rows = []
    with contextlib.suppress(Exception):
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    if not rows:
        return base
    last = rows[-1]
    color = last.get("color", "🟢")
    sev = last.get("severity") or (("warning" if (last.get("warn") or last.get("bad")) else "info"))
    detail = str(last.get("detail", ""))
    ts_txt = str(last.get("ts", ""))
    removed = any(o.get("op") == "remove" for o in (last.get("ops") or []))
    removed = removed or bool(re.search(r"移除[1-9]", detail))
    is_warn = sev == "warning" or color in ("🟡", "🔴") or removed
    if is_warn:
        return {**base, "mark": "🟡",
                "detail": f"⚠️ 最近事件需查看 · {ts_txt} · {detail[:56]}",
                "where": "lh topo 对外交付 events（查看明细；下一次正常变更自动恢复 🟢）"}
    return {**base, "detail": f"最近 {ts_txt} · {detail[:64]}"}


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

    # ── 9. Notion 数据主控镜像（v1.0·Mac主控→鲲鹏8768·目录级快照·零正文出主控）──
    nm = _notion_mirror_state()
    results.append(check_file(BIN / "lh_notion_mirror.py", "引擎 lh_notion_mirror"))
    if nm["catalog"]:
        results.append(("Notion 镜像快照", nm["ok"],
                        f"{nm['pages']} 页 · 同步 {nm['synced_at']}"
                        f"{(' · 陈旧 '+str(nm['stale_days'])+'天') if nm.get('stale_days') else ''}",
                        "~/.longhun/notion_mirror/catalog.json"))
    else:
        results.append(("Notion 镜像快照", False,
                        "未同步(先 lh notion sync --no-push)", "~/.longhun/notion_mirror/"))
    results.append(("Notion 审计链", Path.home().joinpath(
        ".longhun", "notion_audit.jsonl").is_file(),
        "append-only 在位" if Path.home().joinpath(
            ".longhun", "notion_audit.jsonl").is_file() else "缺失",
        "~/.longhun/notion_audit.jsonl"))

    # ── 10. 收款钱包（lh wallet v1.0·SOL 自托管·crypto.json 权限600·链上余额不造假）──
    import json as _json
    _cf = Path.home() / ".longhun" / "crypto.json"
    _waddr = ""
    try:
        if _cf.is_file():
            _cfg = _json.loads(_cf.read_text(encoding="utf-8"))
            _waddr = ((_cfg.get("networks") or {}).get("solana") or {}).get("address", "")
    except Exception:
        pass
    _wq = Path.home() / ".longhun" / "static" / "donate.png"
    results.append(check_file(BIN / "lh_wallet.py", "引擎 lh_wallet"))
    if _waddr:
        results.append(("收款钱包(SOL/USDC)", True,
                        f"{_waddr[:10]}…{_waddr[-6:]} · QR "
                        f"{'✅' if _wq.is_file() else '未生成(lh wallet qr)'}",
                        "~/.longhun/crypto.json(600)·种子仅本地永不外传·链上余额需钱包App"))
    else:
        results.append(("收款钱包(SOL/USDC)", False,
                        "未初始化(lh wallet init)", "~/.longhun/crypto.json"))

    # ── 11. 感知审计（lh_sense v2.0 · 识别→决策→编排→反馈 闭环）──
    sa = _sense_stats()
    if sa["total"]:
        detail = (f"共 {sa['total']} 条 · 🟢{sa['green']} · 🟡{sa['yellow']} · "
                  f"🔴{sa['red']}" + (f" · 最近 {sa['last'][:16]}" if sa["last"] else ""))
        results.append(("感知审计(v2.0)", True, detail,
                        "~/.longhun/sense_audit.jsonl · lh sense --auto"))
    else:
        results.append(("感知审计(v2.0)", True, "0 条（lh sense <文件> --auto 启用）",
                        "~/.longhun/sense_audit.jsonl"))

    # ── 12. 拓扑变更事件（v1.9 耻辱墙联动 · 移除/告警未处理 → 🟡）──
    te = _topo_event_state()
    results.append((te["name"], te["ok"], te["detail"], te["where"], te["mark"]))

    # ── 13. 拓扑根哈希持续自检（v2.2 · 本地重算 vs 线上公开 API）──
    results.append(_topo_root_check())

    return results


def render_table(results) -> str:
    """v1.9 支持 5 元结果 (name, ok, detail, where, mark)；mark 显式 🟢/🟡/🔴（缺省按 ok 派生）"""
    lines = ["", "  🏥 龍魂系统自检 · lh health"]
    lines.append("  " + "=" * 52)
    greens = reds = yellows = 0
    for it in results:
        name, ok, detail, where = it[0], it[1], it[2], it[3]
        mark = it[4] if len(it) > 4 else ("🟢" if ok else "🔴")
        if mark == "🟢":
            greens += 1
        elif mark == "🟡":
            yellows += 1
        else:
            reds += 1
        lines.append(f"  {mark} {name:<22} {detail}")
        lines.append(f"      ↳ {where}")
    lines.append("  " + "=" * 52)
    lines.append(f"  ✅ {greens} 项就绪 · 🟡 {yellows} 项关注 · ❌ {reds} 项缺失")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="龍魂系统自检 v1.0 (lh health)")
    ap.add_argument("--json", action="store_true", help="JSON 输出（AI 可解析）")
    args = ap.parse_args()

    results = run_checks()

    # ── v2.2 Webhook 钩子: 健康检查失败 → health 事件推送（失败不影响主流程 · 🟡 关注不算失败）
    try:
        fails = [(it[0], it[3]) for it in results if not it[1]]
        if fails:
            from lh_webhook import fire_event
            fire_event("health", f"健康异常 {len(fails)} 项: "
                       + " · ".join(str(n) for n, _ in fails)[:200])
    except Exception:  # noqa: BLE001
        pass

    if args.json:
        out = {
            "tool": "lh-health",
            "version": "1.2",
            "checks": [
                {"name": it[0], "ok": it[1], "detail": it[2], "where": it[3],
                 "mark": it[4] if len(it) > 4 else ("🟢" if it[1] else "🔴")}
                for it in results
            ],
            "summary": {
                "ok": sum(1 for it in results if it[1]),
                "fail": sum(1 for it in results if not it[1]),
                "warn": sum(1 for it in results
                            if (it[4] if len(it) > 4 else "") == "🟡"),
                "total": len(results),
            },
            "topo_events": {"has_warn": any(
                it[4] == "🟡" for it in results if len(it) > 4)},
            "knowledge_graph": {**kg_stats(), "docs_version": _docs_version()},
            "sense_audit": _sense_stats(),
            "ledger_status": _ledger_stats(),
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        sys.exit(0 if out["summary"]["fail"] == 0 else 1)

    print(render_table(results))
    sys.exit(0 if all(it[1] for it in results) else 1)


if __name__ == "__main__":
    main()
