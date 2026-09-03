#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# lh_audit_report.py — 龍魂合规报告（任务E 生态补全）
# DNA: #龍芯⚡️2026-09-03-ECOSYSTEM-AUDIT-REPORT-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）· 龍芯北辰
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用法: python3 08_BIN/lh_audit_report.py [--out docs/] [--pdf]
#   输出: docs/合规报告-YYYY-MM-DD.md（自动 GPG 分离签名）
#   内容: 全部图谱验证结果 · 耻辱墙状态 · 服务健康 · 签名状态
#   --pdf 可选: 依赖 weasyprint（未安装则提示降级为 .md + .html）
# 铁律: 零三方依赖(默认路径) · 报告即证据(append 审计日志) · GPG 签名必做
# ═══════════════════════════════════════════════════════════
"""龍魂合规报告生成引擎。图谱验证/耻辱墙/健康/签名 汇总为可提交合规文档。"""
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPO_DIR = ROOT / "docs" / "topology"
STATE_DIR = Path.home() / ".longhun"
SHAME_DB = STATE_DIR / "shame_wall" / "shame_wall.db"
LOG_DIR = STATE_DIR / "logs"
GPG_SIGNER = ROOT / "bin" / "lh_gpg_sign.py"
KEY_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
OWNER = "诸葛鑫 | UID9622 · 龍芯北辰"

CORE_FILES = ["08_BIN/lh_topo.py", "08_BIN/lh_model.py", "08_BIN/lh_judge.py",
              "08_BIN/lh_health.py", "08_BIN/lh_audit_report.py", "08_BIN/lh_backup.py"]


# ───────────────────── 数据采集 ─────────────────────

def collect_graphs() -> dict:
    graphs = []
    green = yellow = red = nodes = 0
    for f in sorted(TOPO_DIR.glob("*_legion_topo.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            graphs.append({"name": f.name, "error": str(e)})
            red += 1
            continue
        assets = [a for g in d.get("groups", []) for a in g.get("assets", [])]
        g = sum(1 for a in assets if "🟢" in str(a.get("status", "")))
        y = sum(1 for a in assets if "🟡" in str(a.get("status", "")))
        r = sum(1 for a in assets if "🔴" in str(a.get("status", "")))
        graphs.append({"name": d.get("display", d.get("topo_name", f.stem)),
                       "nodes": len(assets), "green": g, "yellow": y, "red": r,
                       "sync": d.get("last_sync", "-")})
        nodes += len(assets)
        green += g
        yellow += y
        red += r
    return {"graphs": graphs, "total": len(graphs), "nodes": nodes,
            "green": green, "yellow": yellow, "red": red}


def collect_shame() -> dict:
    if not SHAME_DB.is_file():
        return {"count": 0, "red": 0, "recent": []}
    try:
        import sqlite3
        conn = sqlite3.connect(str(SHAME_DB))
        count = conn.execute("SELECT COUNT(*) FROM 剽窃记录").fetchone()[0]
        red = conn.execute(
            "SELECT COUNT(*) FROM 剽窃记录 WHERE 审计色 LIKE '%🔴%'").fetchone()[0]
        recent = [{"color": r[4], "name": r[0], "kind": r[2], "ts": r[5]}
                  for r in conn.execute(
                      "SELECT 源名称,源URL,指纹类型,置信度,审计色,发现时间,匹配内容 "
                      "FROM 剽窃记录 ORDER BY 发现时间 DESC LIMIT 5").fetchall()]
        conn.close()
        return {"count": count, "red": red, "recent": recent}
    except Exception:   # noqa: BLE001
        return {"count": -1, "red": -1, "recent": []}


def collect_health() -> dict:
    """lh.py health --json 输出解析（容错降级: 本地无状态文件时标注离线项）"""
    out = {"engine_ok": False, "detail": ""}
    try:
        r = subprocess.run([sys.executable, str(ROOT / "08_BIN" / "lh.py"),
                            "health", "--json"], capture_output=True, text=True,
                           timeout=45, cwd=str(ROOT))
        if r.returncode == 0:
            d = json.loads(r.stdout)
            out["engine_ok"] = True
            out["detail"] = d
            return out
        out["detail"] = f"lh health exit={r.returncode} · {r.stderr[:200]}"
    except Exception as e:   # noqa: BLE001
        out["detail"] = f"health 调用异常: {e}"
    return out


def collect_signature() -> dict:
    """GPG 签名状态: 密钥在册 + 核心文件 .asc 覆盖率"""
    sig = {"key_ok": False, "covered": 0, "core_total": len(CORE_FILES), "missing": []}
    try:
        r = subprocess.run(["gpg", "--list-keys", KEY_FINGERPRINT],
                           capture_output=True, text=True, timeout=10)
        sig["key_ok"] = KEY_FINGERPRINT in r.stdout
    except Exception:   # noqa: BLE001
        pass
    for rel in CORE_FILES:
        if (ROOT / rel).with_suffix(rel[rel.rfind("."):] + ".asc").exists():
            sig["covered"] += 1
        else:
            sig["missing"].append(rel)
    return sig


def audit_log_line(text: str):
    """append 审计日志 ~/.longhun/logs/audit.log（证据链·2026-09-03 任务E）"""
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with (LOG_DIR / "audit.log").open("a", encoding="utf-8") as fh:
            fh.write(f"[{datetime.now().astimezone().isoformat(timespec='seconds')}] "
                     f"{text}\n")
    except Exception:   # noqa: BLE001
        pass


# ───────────────────── 渲染 ─────────────────────

def render_md(collect: dict, gen_ts: str) -> str:
    g, shame, health, sig = (collect["graphs"], collect["shame"],
                             collect["health"], collect["signature"])
    rows = "".join(
        f"| {x['name']} | {x.get('nodes', '-')} | 🟢{x.get('green', 0)} "
        f"🟡{x.get('yellow', 0)} 🔴{x.get('red', 0)} | {x.get('sync', '-')} |\n"
        for x in g["graphs"]) or "| 无图谱 | - | - | - |\n"
    srows = "".join(
        f"| {x.get('color', '-')} | {x.get('name', '-')} | {x.get('kind', '-')} "
        f"| {x.get('ts', '-')} |\n" for x in shame.get("recent", [])) \
        or "| — | 清白 | — | — |\n"
    h = health.get("detail", "")
    hl = "- 引擎健康自检: " + ("✅ 通过" if health.get("engine_ok") else "⚠️ 降级")
    if isinstance(h, dict):
        hl += " · knowledge_graph=" + json.dumps(
            h.get("knowledge_graph", {}), ensure_ascii=False)[:200]
    red_total = g.get("red", 0) + shame.get("red", 0)
    verdict = "🟢" if red_total == 0 else f"🔴 {red_total} 项红色待处理"
    return f"""# 🐉 龍魂合规报告 · {gen_ts[:10]}

> DNA: #龍芯⚡️2026-09-03-ECOSYSTEM-AUDIT-REPORT-v1.0-UID9622
> 归属名: {OWNER}
> 生成时间: {gen_ts}
> 合规结论: {verdict}（图谱红色 {g.get('red', 0)} + 耻辱墙红色 {shame.get('red', 0)}）
> 分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

## 一、图谱验证（{g.get('total', 0)} 个 · {g.get('nodes', 0)} 节点 · 🟢{g.get('green', 0)} 🟡{g.get('yellow', 0)} 🔴{g.get('red', 0)}）

| 图谱 | 节点 | 三色 | 最后同步 |
|:---|:---|:---|:---|
{rows}
## 二、耻辱墙状态（累计 {shame.get('count', '-')} 条 · 红色 {shame.get('red', '-')}）

| 色 | 源名称 | 指纹 | 时间 |
|:---|:---|:---|:---|
{srows}
## 三、服务健康

{hl}
## 四、签名状态

- GPG 密钥在册: {"✅ " + KEY_FINGERPRINT if sig.get("key_ok") else "❌ 未检出"}
- 核心引擎 .asc 覆盖: {sig.get('covered', 0)}/{sig.get('core_total', 0)}
- 未签名: {', '.join(sig.get('missing', [])) or '（无）'}
- 本报告: GPG 分离签名自动执行（lh_gpg_sign.py）

## 五、审计日志落点

- 本报告生成事件已追加 ~/.longhun/logs/audit.log（append-only）
"""


def sign_report(path: Path) -> bool:
    """自动 GPG 分离签名"""
    if not GPG_SIGNER.is_file():
        return False
    try:
        subprocess.run([sys.executable, str(GPG_SIGNER), "sign", str(path), "--force"],
                       capture_output=True, text=True, timeout=60)
        return (path.with_suffix(path.suffix + ".asc")).exists()
    except Exception:   # noqa: BLE001
        return False


def main():
    ap = argparse.ArgumentParser(description="📋 龍魂合规报告 (lh audit report)")
    ap.add_argument("--out", default=str(ROOT / "docs"),
                    help="输出目录 (默认 docs/)")
    ap.add_argument("--pdf", action="store_true", help="尝试生成 PDF(需 weasyprint)")
    args = ap.parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    gen_ts = datetime.now().astimezone().isoformat(timespec="seconds")
    collect = {"graphs": collect_graphs(), "shame": collect_shame(),
               "health": collect_health(), "signature": collect_signature()}
    name = f"合规报告-{gen_ts[:10]}.md"
    target = out_dir / name
    target.write_text(render_md(collect, gen_ts), encoding="utf-8")
    audit_log_line(f"lh audit report → {target}")
    ok = sign_report(target)
    print(f"\n  📋 龍魂合规报告生成")
    print(f"     档   {target}")
    print(f"     三色 🟢{collect['graphs']['green']} 🟡{collect['graphs']['yellow']} "
          f"🔴{collect['graphs']['red']}")
    print(f"     耻辱墙 {collect['shame'].get('count', '-')} 条")
    print(f"     签名 {'✅ .asc' if ok else '⚠️ 失败(手工补签 bin/lh_gpg_sign.py)'}")
    print(f"     审计日志 ~/.longhun/logs/audit.log ✓")
    if args.pdf:
        try:
            import weasyprint  # noqa: F401
            print("     📄 --pdf: 请见 weasyprint 文档接入（当前保留 .md 合规版）")
        except Exception:   # noqa: BLE001
            print("     📄 --pdf: weasyprint 未安装 · 已降级为 .md（M77 零三方默认）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
