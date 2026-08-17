#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·庚申·亥时·䷖剥-DUTY-VIEW-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 用途: 人格分工矩阵查看器 — 谁负责什么·焊死·自动路由
# 协议: CC BY-NC-SA 4.0（核心思想层）· GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

"""龍魂 · 人格分工矩阵查看器 v1.0
用法:
  lh duty            # 查看全量分工矩阵
  lh duty --who P03  # 查看某人格职责
  lh duty --json     # JSON 输出
"""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DUTY_FILE = ROOT / "20_CONFIG" / "persona-duty-matrix.json"


def _stamp():
    return "🐉丙午·丙申·庚申·亥时·䷖剥"


def load():
    if not DUTY_FILE.exists():
        print("❌ 分工矩阵未找到:", DUTY_FILE)
        return None
    return json.loads(DUTY_FILE.read_text(encoding="utf-8"))


def view_matrix(as_json=False):
    m = load()
    if not m:
        return 1
    if as_json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0
    print("🧩 龍魂 · 人格分工矩阵 v1.0（谁负责什么·焊死·自动路由）")
    print("=" * 68)
    for g in m.get("总则", []):
        print(f"  📜 {g}")
    print("-" * 68)
    for p in m.get("维护分工", []):
        print(f"\n  【{p['人格']} {p['称号']}】({p['层']})")
        print(f"   负责: {', '.join(p['负责领域'])}")
        for a in p.get("自动动作", []):
            print(f"     ⚡ {a}")
        if p.get("触发词"):
            print(f"     🔑 触发: {', '.join(p['触发词'])}")
        if p.get("产出位置"):
            print(f"     📍 产出: {', '.join(p['产出位置'])}")
    print("\n" + "=" * 68)
    print(f"✅ 分工焊死 · 会话启动自动加载 · {_stamp()}")
    return 0


def view_who(pid: str, as_json=False):
    m = load()
    if not m:
        return 1
    p = next((x for x in m.get("维护分工", []) if x["人格"].upper() == pid.upper()), None)
    if not p:
        print(f"❌ 未找到人格 {pid}。可用: " + ", ".join(x["人格"] for x in m["维护分工"]))
        return 1
    if as_json:
        print(json.dumps(p, ensure_ascii=False, indent=2))
        return 0
    print(f"🧩 {p['人格']} {p['称号']}（{p['层']}）")
    print("=" * 56)
    print(f"  负责: {', '.join(p['负责领域'])}")
    for a in p.get("自动动作", []):
        print(f"  ⚡ {a}")
    if p.get("触发词"):
        print(f"  🔑 触发: {', '.join(p['触发词'])}")
    if p.get("产出位置"):
        print(f"  📍 产出: {', '.join(p['产出位置'])}")
    return 0


def render_html():
    """渲染分工矩阵门户页 → 10_PORTAL/duty.html"""
    m = load()
    if not m:
        return 1
    cards = []
    for p in m.get("维护分工", []):
        duties = "".join(f"<li>{d}</li>" for d in p.get("负责领域", []))
        acts = "".join(f"<li>{a}</li>" for a in p.get("自动动作", []))
        triggers = " · ".join(p.get("触发词", [])) or "-"
        cards.append(f"""
      <div class="card">
        <div class="card-head"><span class="pid">{p['人格']}</span> {p['称号']}<span class="layer">{p['层']}</span></div>
        <div class="duty"><b>负责：</b><ul>{duties}</ul></div>
        <div class="act"><b>自动动作：</b><ul>{acts}</ul></div>
        <div class="trig"><b>触发：</b>{triggers}</div>
      </div>""")
    rules = "".join(f"<li>{g}</li>" for g in m.get("总则", []))
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>🧩 人格分工矩阵 · 龍魂</title>
<style>
  body{{font-family:-apple-system,'PingFang SC',sans-serif;background:#0d1117;color:#e6edf3;margin:0;padding:24px}}
  h1{{color:#f0b90b}} .sub{{color:#8b949e;margin-bottom:16px}}
  .rules{{background:#161b22;border:1px solid #f0b90b55;border-radius:8px;padding:12px 16px;margin-bottom:20px}}
  .rules li{{margin:4px 0}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:14px}}
  .card{{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:14px}}
  .card-head{{font-size:16px;font-weight:700;margin-bottom:8px}}
  .pid{{color:#f0b90b;background:#f0b90b22;border-radius:4px;padding:1px 6px;margin-right:6px}}
  .layer{{float:right;color:#8b949e;font-size:12px;font-weight:400}}
  .duty,.act{{font-size:13px;color:#c9d1d9;margin:6px 0}}
  ul{{margin:2px 0 2px 18px;padding:0}} .trig{{font-size:12px;color:#8b949e}}
  .foot{{margin-top:20px;color:#6e7681;font-size:12px}}
</style></head><body>
<h1>🧩 龍魂 · 人格分工矩阵</h1>
<div class="sub">谁负责什么 · 焊死 · AI 会话启动自动加载 · 老大无需重复交代</div>
<div class="rules"><b>总则：</b><ul>{rules}</ul></div>
<div class="grid">{''.join(cards)}</div>
<div class="foot">自动生成 · {_stamp()} · DNA: #龍芯⚡️丙午·丙申·庚申·亥时·䷖剥-DUTY-HTML-v1.0-UID9622</div>
</body></html>"""
    out = ROOT / "10_PORTAL" / "duty.html"
    out.write_text(html, encoding="utf-8")
    print(f"✅ 门户页已生成: {out}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="人格分工矩阵查看器")
    ap.add_argument("action", nargs="?", default="matrix", choices=["matrix", "view"])
    ap.add_argument("--who", default="", help="查看单个人格职责，如 P03")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--html", action="store_true", help="生成门户页 10_PORTAL/duty.html")
    args = ap.parse_args()
    if args.html:
        return render_html()
    if args.who:
        return view_who(args.who, args.json)
    return view_matrix(args.json)


if __name__ == "__main__":
    sys.exit(main())
