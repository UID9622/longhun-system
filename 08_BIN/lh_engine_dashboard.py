#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 引擎管理仪表盘 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-ENGINE-DASHBOARD-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  - 统一查看所有引擎状态（存在/GPG/大小/可导入）
  - 分类展示（核心/审计/知识/运维/其他）
  - Web 仪表盘（FastAPI + 暗色HTML）
  - 终端彩色输出

用法:
  lh 引擎仪表盘                    # 终端分类展示
  lh 引擎仪表盘 --web              # 启动Web服务
  lh 引擎仪表盘 --web --port 9000
  lh 引擎仪表盘 --json             # JSON输出
"""

import json
import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import OrderedDict

PROJECT_ROOT = Path.home() / "longhun-system"
BIN_DIR = PROJECT_ROOT / "bin"

# 引擎分类规则（按文件名前缀/关键词）
CATEGORY_RULES = {
    "🧠 核心意图": ["intent", "dag", "task", "asi", "brain", "quantum", "seven", "cnsh_runtime", "uid9622_central"],
    "🔍 审计治理": ["audit", "掀", "君子", "purify", "sovereignty", "compliance", "mirror", "regulatory", "energy", "反虚伪", "governance", "three_layer", "three_color", "dna_validate"],
    "📚 知识管理": ["knowledge", "消化", "semantic", "crawler", "content_classifier", "memory", "harvester", "compiler", "migrate"],
    "🛡️ 安全防线": ["security", "firewall", "browser", "anti", "guard", "black", "安全"],
    "⚙️ 系统运维": ["health", "monitor", "lifecycle", "anomaly", "clean", "backup", "performance", "event"],
    "💻 代码能力": ["codegen", "test", "code_review", "review", "translate", "cnsh_translator", "tongxinyi"],
    "📡 模型服务": ["model", "feed", "agent_trainer", "prompt", "predict", "router", "train"],
    "📊 其他": [],  # 兜底
}

CATEGORY_COLORS = {
    "🧠 核心意图": "\033[94m",      # 蓝
    "🔍 审计治理": "\033[91m",      # 红
    "📚 知识管理": "\033[93m",      # 黄
    "🛡️ 安全防线": "\033[95m",      # 紫
    "⚙️ 系统运维": "\033[92m",      # 绿
    "💻 代码能力": "\033[96m",      # 青
    "📡 模型服务": "\033[97m",      # 白
    "📊 其他": "\033[90m",          # 灰
}
RESET = "\033[0m"


class EngineDashboard:
    def __init__(self):
        self.engines = []

    def _classify(self, name: str) -> str:
        for cat, keywords in CATEGORY_RULES.items():
            if cat == "📊 其他":
                continue
            for kw in keywords:
                if kw in name:
                    return cat
        return "📊 其他"

    def scan(self) -> List[Dict]:
        """扫描并分类所有引擎"""
        engines = []
        for file_path in sorted(BIN_DIR.glob("lh_*.py")):
            name = file_path.stem
            asc_path = BIN_DIR / f"{name}.py.asc"
            try:
                stat = file_path.stat()
                size_kb = round(stat.st_size / 1024, 1)
            except Exception:
                size_kb = 0

            # 导入检查
            importable = False
            try:
                spec = importlib.util.spec_from_file_location(name, file_path)
                if spec:
                    importable = True
            except Exception:
                pass

            engines.append({
                "name": name,
                "category": self._classify(name),
                "exists": True,
                "size_kb": size_kb,
                "gpg_signed": asc_path.exists(),
                "importable": importable,
                "modified": stat.st_mtime if size_kb > 0 else None,
            })

        self.engines = engines
        return engines

    def _group_by_category(self) -> Dict[str, List[Dict]]:
        groups = OrderedDict()
        for cat in CATEGORY_RULES:
            groups[cat] = []
        for eng in self.engines:
            cat = eng["category"]
            if cat not in groups:
                groups["📊 其他"].append(eng)
            else:
                groups[cat].append(eng)
        # 去除空组
        return {k: v for k, v in groups.items() if v}

    def terminal_output(self):
        self.scan()
        groups = self._group_by_category()

        total = len(self.engines)
        gpg_ok = sum(1 for e in self.engines if e["gpg_signed"])
        import_ok = sum(1 for e in self.engines if e["importable"])

        print(f"\n🐉 龍魂 · 引擎管理仪表盘")
        print("=" * 68)
        print(f"  总计: {total} 引擎 | GPG: {gpg_ok}/{total} | 可导入: {import_ok}/{total}")
        print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 68)

        for cat, engines in groups.items():
            color = CATEGORY_COLORS.get(cat, "")
            print(f"\n  {color}{cat} ({len(engines)}){RESET}")
            print(f"  {'─' * 50}")
            for eng in engines:
                status_icon = "✅" if eng["importable"] else "⚠️"
                gpg_icon = "🔑" if eng["gpg_signed"] else "  "
                name = eng["name"]
                size = f"{eng['size_kb']}KB"
                print(f"    {status_icon} {gpg_icon} {name:<40} {size:>8}")

        print(f"\n{'=' * 68}")
        # 健康评分
        health = int((gpg_ok / max(1, total) * 0.5 + import_ok / max(1, total) * 0.5) * 100)
        grade = "🟢" if health >= 80 else ("🟡" if health >= 60 else "🔴")
        print(f"  健康评分: {health}/100 {grade}")
        print(f"{'=' * 68}")

    def json_output(self) -> str:
        self.scan()
        groups = self._group_by_category()
        total = len(self.engines)
        return json.dumps({
            "total": total,
            "gpg_signed": sum(1 for e in self.engines if e["gpg_signed"]),
            "importable": sum(1 for e in self.engines if e["importable"]),
            "categories": {cat: len(engs) for cat, engs in groups.items()},
            "engines": {cat: [e["name"] for e in engs] for cat, engs in groups.items()},
            "timestamp": datetime.now().isoformat(),
        }, ensure_ascii=False, indent=2)

    def web_server(self, port: int = 8080):
        """启动 Web 仪表盘"""
        try:
            from fastapi import FastAPI
            from fastapi.responses import HTMLResponse
            import uvicorn
        except ImportError:
            print("⚠️ 请安装: pip install fastapi uvicorn")
            return

        dashboard = self
        app = FastAPI(title="龍魂·引擎仪表盘", docs_url=None, redoc_url=None)

        CATEGORY_EMOJI = {
            "🧠 核心意图": "🧠", "🔍 审计治理": "🔍", "📚 知识管理": "📚",
            "🛡️ 安全防线": "🛡️", "⚙️ 系统运维": "⚙️", "💻 代码能力": "💻",
            "📡 模型服务": "📡", "📊 其他": "📊"
        }

        @app.get("/")
        async def index():
            engines = dashboard.scan()
            groups = dashboard._group_by_category()
            total = len(engines)
            gpg_ok = sum(1 for e in engines if e["gpg_signed"])
            import_ok = sum(1 for e in engines if e["importable"])
            health = int((gpg_ok / max(1, total) * 0.5 + import_ok / max(1, total) * 0.5) * 100)

            html = """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>龍魂 · 引擎仪表盘</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,sans-serif;background:#0d1117;color:#c9d1d9;padding:24px}
h1{color:#ffd700;margin-bottom:4px}
.subtitle{color:#8b949e;font-size:14px;margin-bottom:16px}
.stats{display:flex;gap:16px;margin-bottom:24px}
.stat{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 20px;text-align:center}
.stat .num{font-size:36px;font-weight:bold;color:#58a6ff}
.stat .label{font-size:12px;color:#8b949e;margin-top:4px}
.category{margin-bottom:24px}
.cat-title{font-size:18px;color:#ffd700;border-bottom:1px solid #30363d;padding-bottom:6px;margin-bottom:8px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:8px}
.card{background:#161b22;border:1px solid #30363d;border-radius:6px;padding:10px 14px;display:flex;align-items:center;gap:10px}
.card.good{border-left:3px solid #3fb950}
.card.warn{border-left:3px solid #d29922}
.card .icon{font-size:18px}
.card .name{font-family:monospace;color:#e6edf3}
.card .meta{font-size:12px;color:#8b949e;margin-left:auto}
.health-bar{width:100%;height:8px;background:#21262d;border-radius:4px}
.health-bar .fill{height:100%;border-radius:4px;transition:width 0.3s}
.timestamp{color:#8b949e;font-size:12px;text-align:center;margin-top:24px}
</style></head>
<body>
<h1>🐉 龍魂 · 引擎管理仪表盘</h1>
<div class="subtitle">""" + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """</div>
<div class="stats">
<div class="stat"><div class="num">""" + str(total) + """</div><div class="label">引擎总数</div></div>
<div class="stat"><div class="num">""" + str(gpg_ok) + """</div><div class="label">GPG签名</div></div>
<div class="stat"><div class="num">""" + str(import_ok) + """</div><div class="label">可导入</div></div>
<div class="stat"><div class="num">""" + str(health) + """</div><div class="label">健康评分</div></div>
</div>
<div class="health-bar" style="margin-bottom:24px"><div class="fill" style="width:""" + str(health) + """%;background:""" + ("#3fb950" if health >= 80 else "#d29922" if health >= 60 else "#f85149") + """"></div></div>
"""
            for cat, engs in groups.items():
                emoji = CATEGORY_EMOJI.get(cat, "📊")
                html += f'<div class="category"><div class="cat-title">{emoji} {cat} ({len(engs)})</div><div class="grid">'
                for e in engs:
                    cls = "good" if e["importable"] else "warn"
                    gpg = "🔑" if e["gpg_signed"] else ""
                    html += f'<div class="card {cls}"><span class="icon">{gpg}</span><span class="name">{e["name"]}</span><span class="meta">{e["size_kb"]}KB</span></div>'
                html += '</div></div>'

            html += '<div class="timestamp">DNA: #龍芯⚡️' + datetime.now().strftime('%Y%m%d%H%M%S') + '-DASHBOARD-UID9622</div></body></html>'
            return HTMLResponse(html)

        print(f"🚀 仪表盘启动: http://localhost:{port}")
        print(f"   按 Ctrl+C 停止")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·引擎管理仪表盘")
    parser.add_argument("--web", action="store_true", help="启动Web界面")
    parser.add_argument("--port", type=int, default=8080, help="Web端口")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    dashboard = EngineDashboard()

    if args.web:
        dashboard.web_server(args.port)
    elif args.json:
        print(dashboard.json_output())
    else:
        dashboard.terminal_output()


if __name__ == "__main__":
    main()
