#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·癸巳·未时·䷝离-WUWU-RENDERER-v1.0-MEDIA-SENSE
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 女娲五彩石渲染引擎 v1.0 — 龍魂视觉引擎（感官层·视觉）

能力（龍魂风格图表 → PNG / SVG / HTML 内嵌）:
  wuxing  五行雷达图   数据: {"金":80,"木":65,"水":70,"火":90,"土":55} 或 [80,65,70,90,55]
  audit   三色审计仪表盘 数据: {"🔴":1,"🟡":132,"🟢":1} 或 {"red":1,"yellow":132,"green":1}
  flow    流场节点图   数据: {"nodes":[{"id":"a","label":"节点","x":0.2,"y":0.3}],"edges":[["a","b"]]}（坐标省略自动布局）
  health  健康看板     数据: lh health --json 结构；不传数据则自动调 lh health --json

命令:
  python3 08_BIN/wuwu_renderer.py wuxing '{"金":80,...}' [--format png|svg|html] [--output PATH]
  python3 08_BIN/wuwu_renderer.py health               # 自动联动 lh health --json → 健康看板
  python3 08_BIN/wuwu_renderer.py --self-test          # 自测：三类图各出一张

对齐: lh health --json 输出联动 · 龙魂五行视觉配色 · 繁体「龍」
"""

import argparse
import base64
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# ============================================================
# 常量（龙魂五行视觉 · 与 lh_judge.py 同源）
# ============================================================
五行名 = ["金", "木", "水", "火", "土"]
五行色 = {"金": "#D4AF37", "木": "#2E8B57", "水": "#1E90FF", "火": "#E8402E", "土": "#B8860B"}
三色 = {"🔴": "#E8402E", "红": "#E8402E", "red": "#E8402E",
        "🟡": "#E8B23A", "黄": "#E8B23A", "yellow": "#E8B23A",
        "🟢": "#2E8B57", "绿": "#2E8B57", "green": "#2E8B57"}
背景色 = "#0E1420"
文字色 = "#E8E8E8"
龙金 = "#D4AF37"
ROOT = Path(__file__).resolve().parent.parent
输出默认目录 = ROOT / "data" / "renders"

# PIL 中文字体候选
字体候选 = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]


def _字体(size: int):
    """加载系统中文字体，找不到则用默认"""
    try:
        from PIL import ImageFont
        for p in 字体候选:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    continue
        return ImageFont.load_default()
    except Exception:
        return None


def _加载PIL():
    """PIL 按需导入（SVG/HTML 模式无需 PIL）"""
    from PIL import Image, ImageDraw
    return Image, ImageDraw


# ============================================================
# 数据解析
# ============================================================
def 解析数据(数据) -> dict:
    """接受 dict/list、JSON 字符串、文件路径 或 None"""
    if 数据 is None or 数据 == "":
        return {}
    if isinstance(数据, (dict, list)):
        return 数据
    if isinstance(数据, str):
        if os.path.isfile(数据):
            return json.loads(Path(数据).read_text(encoding="utf-8"))
        return json.loads(数据)
    return {}


def 取五行数据(数据: dict) -> list:
    """统一为 [金,木,水,火,土] 列表（0-100）"""
    if not 数据:
        return [80, 65, 70, 90, 55]
    if isinstance(数据, list):
        vals = 数据[:5]
    else:
        vals = [float(数据.get(k, 数据.get(五行名[i], 50))) for i, k in enumerate(五行名)]
    return [max(0.0, min(100.0, float(v))) for v in vals]


def 取审计数据(数据: dict) -> dict:
    """统一为 {red,yellow,green,count,verdict}"""
    if not 数据:
        return {"red": 1, "yellow": 132, "green": 1}
    def _v(*keys):
        for k in keys:
            if k in 数据:
                return int(数据[k])
        return 0
    red = _v("🔴", "红", "red", "fail")
    yellow = _v("🟡", "黄", "yellow", "warn", "skip")
    green = _v("🟢", "绿", "green", "pass")
    总 = red + yellow + green
    判定 = "🔴" if red > 0 else ("🟡" if yellow > 0 else "🟢")
    return {"red": red, "yellow": yellow, "green": green, "total": 总, "verdict": 判定}


def 取流场数据(数据: dict) -> dict:
    """规范化节点/边；坐标缺失自动布局"""
    nodes = 数据.get("nodes") or []
    edges = 数据.get("edges") or []
    n = len(nodes)
    for i, nd in enumerate(nodes):
        if "x" not in nd or "y" not in nd:
            ang = 2 * math.pi * i / max(n, 1) - math.pi / 2
            nd["x"] = round(0.5 + 0.32 * math.cos(ang), 3)
            nd["y"] = round(0.5 + 0.32 * math.sin(ang), 3)
    return {"nodes": nodes, "edges": edges}


# ============================================================
# 几何工具
# ============================================================
def 五边形点(中心, r, i, count=5, rot=-90):
    cx, cy = 中心
    ang = math.radians(rot + 360.0 * i / count)
    return (cx + r * math.cos(ang), cy + r * math.sin(ang))


def 仪表盘角度(百分比):
    """0-100 → 半圆角度：0=180°(左) 100=0°(右)"""
    return math.radians(180 - 1.8 * max(0.0, min(100.0, 百分比)))


# ============================================================
# PNG 绘制（PIL）
# ============================================================
def 绘制_雷达图_png(数据: list, W=1000, H=800) -> "Image":
    Image, ImageDraw = _加载PIL()
    img = Image.new("RGB", (W, H), 背景色)
    d = ImageDraw.Draw(img)
    cx, cy, r = W / 2, H / 2 + 10, min(W, H) / 2 - 90
    f_小 = _字体(18)
    f_大 = _字体(30)

    # 同心网格
    for 层 in range(1, 6):
        半径 = r * 层 / 5
        点s = [五边形点((cx, cy), 半径, i) for i in range(5)]
        d.line(点s + [点s[0]], fill="#2A3A55", width=1)
    for i in range(5):
        点s = [五边形点((cx, cy), r, i)]
        d.line([(cx, cy), 点s[0]], fill="#2A3A55", width=1)

    # 数据多边形
    vals = 数据
    点s = [五边形点((cx, cy), r * v / 100, i) for i, v in enumerate(vals)]
    d.polygon(点s, outline=龙金, fill=(212, 175, 55, 60))
    for i, (p, v) in enumerate(zip(点s, vals)):
        d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], fill=五行色[五行名[i]])
        # 轴标签
        lp = 五边形点((cx, cy), r + 45, i)
        d.text((lp[0] - 12, lp[1] - 14), 五行名[i], fill=五行色[五行名[i]], font=f_大)
        vp = 五边形点((cx, cy), r + 90, i)
        d.text((vp[0] - 16, vp[1] - 12), f"{int(v)}", fill=文字色, font=f_小)

    d.text((W / 2 - 150, 18), "龍魂·五行雷达图", fill=龙金, font=_字体(42))
    return img


def 绘制_审计仪表盘_png(数据: dict, W=1000, H=800) -> "Image":
    Image, ImageDraw = _加载PIL()
    img = Image.new("RGB", (W, H), 背景色)
    d = ImageDraw.Draw(img)
    cx, cy, r = W / 2, H / 2 + 60, min(W, H) / 2 - 100
    f_大 = _字体(34)
    f_中 = _字体(24)

    # 三色半圆弧（粗弧 = 多个扇形）
    for 百分比 in range(0, 101):
        ang = 仪表盘角度(百分比)
        x = cx + r * math.cos(ang)
        y = cy - r * math.sin(ang)
        col = "#E8402E" if 百分比 < 34 else ("#E8B23A" if 百分比 < 67 else "#2E8B57")
        d.line([(cx, cy), (x, y)], fill=col, width=10)

    # 综合值 = green 占比
    综合 = int(100.0 * 数据["green"] / max(数据["total"], 1))
    ptr = 仪表盘角度(综合)
    px = cx + (r - 30) * math.cos(ptr)
    py = cy - (r - 30) * math.sin(ptr)
    d.line([(cx, cy), (px, py)], fill="#FFFFFF", width=6)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill="#FFFFFF")

    # 判定
    d.text((W / 2 - 80, cy + 40), f"{数据['verdict']} {综合}%", fill=文字色, font=f_大)

    # 三色计数
    三色计数 = [(数据["green"], "🟢 通过", 三色["green"]),
              (数据["yellow"], "🟡 注意", 三色["yellow"]),
              (数据["red"], "🔴 严重", 三色["red"])]
    y0 = cy + 150
    for i, (cnt, label, col) in enumerate(三色计数):
        bx = cx - 320 + i * 240
        d.rectangle([bx, y0, bx + 160, y0 + 60], outline=col, width=3)
        d.text((bx + 10, y0 + 10), f"{label} {cnt}", fill=col, font=f_中)

    d.text((W / 2 - 150, 18), "龍魂·三色审计仪表盘", fill=龙金, font=_字体(42))
    return img


def 绘制_流场_png(数据: dict, W=1000, H=800) -> "Image":
    Image, ImageDraw = _加载PIL()
    img = Image.new("RGB", (W, H), 背景色)
    d = ImageDraw.Draw(img)
    f_中 = _字体(20)
    f_大 = _字体(42)
    节点 = 数据["nodes"]
    边s = 数据["edges"]
    by_id = {nd.get("id"): nd for nd in 节点}

    # 边
    for a, b in 边s:
        if a in by_id and b in by_id:
            pa = (by_id[a]["x"] * W, by_id[a]["y"] * H)
            pb = (by_id[b]["x"] * W, by_id[b]["y"] * H)
            d.line([pa, pb], fill="#3A5A8A", width=2)

    # 节点
    for nd in 节点:
        x, y = nd["x"] * W, nd["y"] * H
        col = nd.get("color", 龙金)
        d.ellipse([x - 22, y - 22, x + 22, y + 22], fill=col, outline="#FFFFFF", width=3)
        label = nd.get("label") or nd.get("id", "")
        d.text((x - 40, y - 60), label, fill=文字色, font=f_中)

    d.text((W / 2 - 160, 18), "龍魂·流场节点可视化", fill=龙金, font=f_大)
    return img


def 绘制_健康看板_png(数据: dict, W=1000, H=800) -> "Image":
    Image, ImageDraw = _加载PIL()
    img = Image.new("RGB", (W, H), 背景色)
    d = ImageDraw.Draw(img)
    f_小 = _字体(18)
    f_中 = _字体(24)
    f_大 = _字体(42)
    checks = 数据.get("checks", [])
    summary = 数据.get("summary", {})
    if not checks:
        checks = [{"name": "无检查项", "ok": False, "detail": ""}]
    pas = sum(1 for c in checks if c.get("ok"))
    fail = len(checks) - pas
    总分 = int(100.0 * pas / max(len(checks), 1))

    d.text((W / 2 - 170, 18), "龍魂·健康看板", fill=龙金, font=f_大)
    d.text((W / 2 - 100, 90), f"健康度 {总分}%  (🟢{pas} / 🔴{fail})",
           fill="#2E8B57" if fail == 0 else "#E8B23A", font=f_中)

    y = 180
    for i, c in enumerate(checks[:12]):
        ok = c.get("ok")
        name = str(c.get("name", ""))[:36]
        detail = str(c.get("detail", ""))[:40]
        col = "#2E8B57" if ok else "#E8402E"
        mark = "✅" if ok else "❌"
        d.text((40, y), f"{mark} {name} {detail}", fill=col, font=f_小)
        y += 48
    return img


# ============================================================
# SVG 生成（纯手写 · 零依赖）
# ============================================================
def _svg_head(W, H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" style="background:{背景色};font-family:PingFang SC,Hiragino Sans GB,sans-serif">')


def 生成SVG_雷达图(数据: list, W=1000, H=800) -> str:
    cx, cy, r = W / 2, H / 2 + 10, min(W, H) / 2 - 90
    s = [_svg_head(W, H), f'<text x="{W/2}" y="46" text-anchor="middle" fill="{龙金}" font-size="40">龍魂·五行雷达图</text>']
    for 层 in range(1, 6):
        点s = [五边形点((cx, cy), r * 层 / 5, i) for i in range(5)]
        pts = " ".join(f"{p[0]},{p[1]}" for p in 点s)
        s.append(f'<polygon points="{pts}" fill="none" stroke="#2A3A55" stroke-width="1"/>')
    for i in range(5):
        p = 五边形点((cx, cy), r, i)
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{p[0]}" y2="{p[1]}" stroke="#2A3A55"/>')
    点s = [五边形点((cx, cy), r * v / 100, i) for i, v in enumerate(数据)]
    pts = " ".join(f"{p[0]},{p[1]}" for p in 点s)
    s.append(f'<polygon points="{pts}" fill="rgba(212,175,55,0.25)" stroke="{龙金}" stroke-width="3"/>')
    for i, (p, v) in enumerate(zip(点s, 数据)):
        s.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="8" fill="{五行色[五行名[i]]}"/>')
        lp = 五边形点((cx, cy), r + 48, i)
        vp = 五边形点((cx, cy), r + 88, i)
        s.append(f'<text x="{lp[0]}" y="{lp[1]}" text-anchor="middle" fill="{五行色[五行名[i]]}" font-size="28">{五行名[i]}</text>')
        s.append(f'<text x="{vp[0]}" y="{vp[1]}" text-anchor="middle" fill="#E8E8E8" font-size="18">{int(v)}</text>')
    s.append("</svg>")
    return "".join(s)


def 生成SVG_审计仪表盘(数据: dict, W=1000, H=800) -> str:
    cx, cy, r = W / 2, H / 2 + 60, min(W, H) / 2 - 100
    综合 = int(100.0 * 数据["green"] / max(数据["total"], 1))
    s = [_svg_head(W, H), f'<text x="{W/2}" y="46" text-anchor="middle" fill="{龙金}" font-size="40">龍魂·三色审计仪表盘</text>']
    # 半圆弧：用描边虚线近似三色（每 2° 一段）
    for 百分比 in range(0, 101, 2):
        ang = 仪表盘角度(百分比)
        a1, a2 = ang, 仪表盘角度(min(100, 百分比 + 2))
        x1, y1 = cx + r * math.cos(a1), cy - r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy - r * math.sin(a2)
        col = "#E8402E" if 百分比 < 34 else ("#E8B23A" if 百分比 < 67 else "#2E8B57")
        s.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="12" stroke-linecap="round"/>')
    ptr = 仪表盘角度(综合)
    px, py = cx + (r - 40) * math.cos(ptr), cy - (r - 40) * math.sin(ptr)
    s.append(f'<line x1="{cx}" y1="{cy}" x2="{px}" y2="{py}" stroke="#fff" stroke-width="6"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="14" fill="#fff"/>')
    s.append(f'<text x="{W/2}" y="{cy+60}" text-anchor="middle" fill="#E8E8E8" font-size="34">{数据["verdict"]} {综合}%</text>')
    三色计数 = [(数据["green"], "🟢 通过", 三色["green"]),
              (数据["yellow"], "🟡 注意", 三色["yellow"]),
              (数据["red"], "🔴 严重", 三色["red"])]
    for i, (cnt, label, col) in enumerate(三色计数):
        bx = cx - 340 + i * 240
        s.append(f'<rect x="{bx}" y="{cy+150}" width="180" height="60" fill="none" stroke="{col}" stroke-width="3" rx="8"/>')
        s.append(f'<text x="{bx+90}" y="{cy+190}" text-anchor="middle" fill="{col}" font-size="24">{label} {cnt}</text>')
    s.append("</svg>")
    return "".join(s)


def 生成SVG_流场(数据: dict, W=1000, H=800) -> str:
    节点, 边s = 数据["nodes"], 数据["edges"]
    by_id = {nd.get("id"): nd for nd in 节点}
    s = [_svg_head(W, H), f'<text x="{W/2}" y="46" text-anchor="middle" fill="{龙金}" font-size="40">龍魂·流场节点可视化</text>']
    for a, b in 边s:
        if a in by_id and b in by_id:
            pa, pb = by_id[a], by_id[b]
            s.append(f'<line x1="{pa["x"]*W}" y1="{pa["y"]*H}" x2="{pb["x"]*W}" y2="{pb["y"]*H}" stroke="#3A5A8A" stroke-width="2"/>')
    for nd in 节点:
        x, y = nd["x"] * W, nd["y"] * H
        col = nd.get("color", 龙金)
        s.append(f'<circle cx="{x}" cy="{y}" r="24" fill="{col}" stroke="#fff" stroke-width="3"/>')
        label = nd.get("label") or nd.get("id", "")
        s.append(f'<text x="{x}" y="{y-44}" text-anchor="middle" fill="#E8E8E8" font-size="20">{label}</text>')
    s.append("</svg>")
    return "".join(s)


def 生成SVG_健康看板(数据: dict, W=1000, H=800) -> str:
    checks = 数据.get("checks", []) or [{"name": "无检查项", "ok": False}]
    pas = sum(1 for c in checks if c.get("ok"))
    fail = len(checks) - pas
    总分 = int(100.0 * pas / max(len(checks), 1))
    s = [_svg_head(W, H), f'<text x="{W/2}" y="46" text-anchor="middle" fill="{龙金}" font-size="40">龍魂·健康看板</text>',
         f'<text x="{W/2}" y="110" text-anchor="middle" fill="#2E8B57" font-size="28">健康度 {总分}%  (🟢{pas} / 🔴{fail})</text>']
    y = 170
    for c in checks[:12]:
        ok = c.get("ok")
        col = "#2E8B57" if ok else "#E8402E"
        mark = "✅" if ok else "❌"
        name = str(c.get("name", ""))[:36]
        detail = str(c.get("detail", ""))[:40]
        s.append(f'<text x="40" y="{y}" fill="{col}" font-size="20">{mark} {name} {detail}</text>')
        y += 42
    s.append("</svg>")
    return "".join(s)


# ============================================================
# 分发 + 输出
# ============================================================
def 渲染(类型: str, 数据: str = None, 格式: str = "png", 输出: str = None, 路径目录: Path = None):
    """统一入口：返回输出文件路径"""
    raw = 解析数据(数据)
    if 类型 == "health" and not raw:
        raw = _拉健康数据()
    if 类型 == "wuxing":
        data = 取五行数据(raw)
        svg = 生成SVG_雷达图(data)
        png_fn = lambda: 绘制_雷达图_png(data)  # noqa: E731
    elif 类型 == "audit":
        data = 取审计数据(raw)
        svg = 生成SVG_审计仪表盘(data)
        png_fn = lambda: 绘制_审计仪表盘_png(data)  # noqa: E731
    elif 类型 == "flow":
        data = 取流场数据(raw)
        svg = 生成SVG_流场(data)
        png_fn = lambda: 绘制_流场_png(data)  # noqa: E731
    elif 类型 == "health":
        data = raw
        svg = 生成SVG_健康看板(data)
        png_fn = lambda: 绘制_健康看板_png(data)  # noqa: E731
    else:
        raise SystemExit(f"❌ 未知类型: {类型}（支持: wuxing/audit/flow/health）")

    dir = 路径目录 or 输出默认目录
    dir.mkdir(parents=True, exist_ok=True)
    if not 输出:
        h = hashlib.md5(f"{类型}{json.dumps(data, ensure_ascii=False)}".encode()).hexdigest()[:12]
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        输出 = f"wuwu_{类型}_{ts}_{h}"
    out = Path(输出)
    if not out.suffix:
        out = dir / f"{out}.{格式}"
    elif out.parent == Path("."):
        out = dir / out.name

    格式 = 格式.lower()
    if 格式 == "svg":
        out.write_text(svg, encoding="utf-8")
    elif 格式 == "html":
        b64 = base64.b64encode(svg.encode("utf-8")).decode()
        html = (f'<!DOCTYPE html><html lang="zh-CN"><meta charset="utf-8">'
                f'<title>龍魂 · {类型}</title><body style="margin:0;background:#0E1420">'
                f'<img src="data:image/svg+xml;base64,{b64}" style="width:100%">'
                f'<p style="color:#555;text-align:center;font-size:12px">'
                f'🐉 女娲五彩石渲染引擎 · 诸葛鑫 | UID9622 · 龍芯北辰</p></body></html>')
        out.write_text(html, encoding="utf-8")
    else:
        try:
            img = png_fn()
            img.save(str(out))
        except ImportError:
            out = Path(str(out).replace(".png", ".svg"))
            out.write_text(svg, encoding="utf-8")
    return str(out)


def _拉健康数据() -> dict:
    """自动联动 lh health --json"""
    try:
        r = subprocess.run(["python3", str(ROOT / "bin" / "lh_health.py"), "--json"],
                           capture_output=True, text=True, timeout=60)
        return json.loads(r.stdout)
    except Exception:
        return {"checks": [{"name": "lh health 不可达", "ok": False, "detail": str(e)} for e in [""]]}


def 自测() -> int:
    dir = ROOT / "data" / "renders" / "selftest"
    print("🐉 女娲五彩石引擎自测…")
    for 类型, 数据 in [("wuxing", '{"金":88,"木":66,"水":72,"火":91,"土":58}'),
                     ("audit", '{"red":1,"yellow":132,"green":1}'),
                     ("flow", '{"nodes":[{"id":"a","label":"网关"},{"id":"b","label":"审计"},{"id":"c","label":"记忆"}],"edges":[["a","b"],["b","c"]]}'),
                     ("health", None)]:
        p = 渲染(类型, 数据, "png", 路径目录=dir)
        print(f"  ✅ {类型:6s} → {p}")
        p = 渲染(类型, 数据, "svg", 路径目录=dir)
        print(f"  ✅ {类型:6s} → {p}")
    print("🟢 自测通过")
    return 0


def main():
    ap = argparse.ArgumentParser(prog="wuwu-renderer", description="🐉 女娲五彩石渲染引擎")
    ap.add_argument("类型", nargs="?", help="wuxing/audit/flow/health")
    ap.add_argument("数据", nargs="?", default=None, help="JSON 或文件路径（health 可省略→自动联动 lh health --json）")
    ap.add_argument("--format", default="png", choices=["png", "svg", "html"], help="输出格式")
    ap.add_argument("--output", default=None, help="输出路径（默认 data/renders/）")
    ap.add_argument("--self-test", action="store_true", help="自测")
    args = ap.parse_args()

    if args.self_test:
        sys.exit(自测())
    if not args.类型:
        ap.print_help()
        sys.exit(1)
    try:
        p = 渲染(args.类型, args.数据, args.format, args.output)
        print(f"✅ 已生成: {p}")
    except Exception as e:
        print(f"❌ 渲染失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
