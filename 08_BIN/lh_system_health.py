#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 系统健康报告引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-HEALTH-REPORT-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能:
  - 汇总所有引擎状态（存在性/GPG签名/导入可用性）
  - 检查Python依赖版本
  - 生成健康评分(0-100)
  - 输出终端报告 / JSON / HTML仪表盘

用法:
  lh 系统健康                    # 终端报告
  lh 系统健康 --html             # 生成HTML报告
  lh 系统健康 --json             # JSON输出
  lh 系统健康 --watch            # 持续监控模式
"""

import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

PROJECT_ROOT = Path.home() / "longhun-system"
BIN_DIR = PROJECT_ROOT / "bin"
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


class SystemHealth:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "engines": {},
            "dependencies": {},
            "overall_score": 100,
            "issues": [],
            "warnings": [],
            "grade": "🟢 健康",
        }

    def discover_engines(self) -> List[str]:
        """自动发现所有 lh_*.py 引擎"""
        engines = set()
        for f in BIN_DIR.glob("lh_*.py"):
            engines.add(f.stem)
        for f in BIN_DIR.glob("*.py"):
            if f.stem.startswith("lh_"):
                engines.add(f.stem)
        return sorted(engines)

    def check_engines(self) -> Dict:
        """检查所有引擎"""
        engine_names = self.discover_engines()
        engine_status = {}
        missing_gpg = []
        missing_importable = []

        for name in engine_names:
            file_path = BIN_DIR / f"{name}.py"
            asc_path = BIN_DIR / f"{name}.py.asc"
            has_gpg = asc_path.exists()
            exists = file_path.exists()
            size_kb = file_path.stat().st_size / 1024 if exists else 0

            # 轻量导入检查
            importable = False
            if exists:
                try:
                    spec = importlib.util.spec_from_file_location(name, file_path)
                    if spec:
                        importable = True
                except Exception:
                    pass

            engine_status[name] = {
                "exists": exists,
                "gpg_signed": has_gpg,
                "importable": importable,
                "size_kb": round(size_kb, 1),
            }

            if not has_gpg:
                missing_gpg.append(name)
            if not importable:
                missing_importable.append(name)

        self.results["engines"] = engine_status
        total = len(engine_names)

        if missing_gpg:
            self.results["warnings"].append(f"{len(missing_gpg)}/{total} 引擎缺GPG签名")
            self.results["overall_score"] -= min(len(missing_gpg) * 2, 20)

        if missing_importable:
            self.results["issues"].append(f"{len(missing_importable)}/{total} 引擎导入失败")

        self.results["engine_count"] = total
        return engine_status

    def check_dependencies(self) -> Dict:
        """检查Python依赖"""
        deps = {
            "psutil": "系统监控",
            "requests": "HTTP请求",
            "fastapi": "API服务",
            "uvicorn": "ASGI服务器",
            "sqlite3": "嵌入式数据库",
            "json": "JSON处理",
            "hashlib": "哈希计算",
            "subprocess": "进程管理",
            "importlib": "动态导入",
            "networkx": "图/图谱",
            "redis": "消息队列",
        }

        dep_status = {}
        missing = []
        for dep_name, dep_desc in deps.items():
            try:
                mod = importlib.import_module(dep_name)
                ver = getattr(mod, "__version__", "内置")
                dep_status[dep_name] = {"installed": True, "version": str(ver), "description": dep_desc}
            except ImportError:
                dep_status[dep_name] = {"installed": False, "version": None, "description": dep_desc}
                missing.append(dep_name)

        self.results["dependencies"] = dep_status
        if missing:
            self.results["warnings"].append(f"缺失依赖: {', '.join(missing)}")
            self.results["overall_score"] -= min(len(missing) * 3, 15)

        self.results["dep_count"] = len(deps)
        self.results["dep_missing"] = len(missing)
        return dep_status

    def check_lh_command(self) -> Dict:
        """检查 lh 命令入口"""
        lh_path = BIN_DIR / "lh.py"
        if not lh_path.exists():
            return {"available": False, "message": "lh.py 不存在"}

        # 检查是否能语法解析
        try:
            with open(lh_path, 'r') as f:
                content = f.read()
            tree = __import__('ast').parse(content)
            func_names = [n.name for n in __import__('ast').walk(tree) if isinstance(n, __import__('ast').FunctionDef)]
            return {
                "available": True,
                "file": str(lh_path),
                "size_kb": round(lh_path.stat().st_size / 1024, 1),
                "functions": len(func_names),
            }
        except Exception as e:
            return {"available": False, "message": str(e)}

    def _compute_final_score(self):
        s = max(0, min(100, self.results["overall_score"]))
        self.results["overall_score"] = s
        if s >= 85:
            self.results["grade"] = "🟢 健康"
        elif s >= 65:
            self.results["grade"] = "🟡 一般"
        else:
            self.results["grade"] = "🔴 需关注"

    def generate_report(self) -> Dict:
        print("🔍 系统健康检查中...")
        self.check_engines()
        self.check_dependencies()
        self.results["lh_command"] = self.check_lh_command()
        self._compute_final_score()
        return self.results

    def terminal_output(self):
        r = self.generate_report()
        print(f"\n🐉 龍魂系统健康报告")
        print("=" * 60)
        print(f"  📊 评分: {r['overall_score']}/100 ({r['grade']})")
        print(f"  ⚙️  引擎: {r.get('engine_count', 0)} 个")
        print(f"  📦 依赖: {r.get('dep_count', 0)} 项 ({r.get('dep_missing', 0)} 缺失)")
        print(f"  ⚠️  警告: {len(r['warnings'])} 条")
        print(f"  🔴 问题: {len(r['issues'])} 条")
        print("-" * 60)

        # 引擎概览
        print("\n  【引擎状态】")
        for name, info in list(r["engines"].items())[:15]:
            s = "✅" if info["exists"] else "❌"
            g = "🔑" if info["gpg_signed"] else "  "
            print(f"    {s}{g} {name} ({info['size_kb']}KB)")
        if len(r["engines"]) > 15:
            print(f"    ... 共 {len(r['engines'])} 个引擎")

        # 依赖
        print("\n  【依赖状态】")
        for dep, info in r["dependencies"].items():
            s = "✅" if info["installed"] else "❌"
            print(f"    {s} {dep} ({info.get('description', '')})")
        print("=" * 60)

    def generate_html(self) -> Path:
        """生成 HTML 仪表盘"""
        self.generate_report()
        r = self.results

        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>龍魂 · 系统健康报告</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, sans-serif; background: #0d1117; color: #c9d1d9; padding: 24px; }}
h1 {{ color: #ffd700; margin-bottom: 8px; }}
.score {{ font-size: 48px; font-weight: bold; color: #58a6ff; }}
.grade {{ font-size: 24px; margin-left: 12px; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; margin-top: 16px; }}
.card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; }}
.card .name {{ font-family: monospace; color: #ffd700; }}
.card .meta {{ font-size: 12px; color: #8b949e; }}
.card.good {{ border-left: 3px solid #3fb950; }}
.card.warn {{ border-left: 3px solid #d29922; }}
.bar {{ height: 8px; border-radius: 4px; background: #21262d; margin-top: 8px; }}
.bar .fill {{ height: 100%; border-radius: 4px; background: #3fb950; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 16px; }}
td {{ padding: 6px 12px; border-bottom: 1px solid #21262d; }}
.warn-text {{ color: #d29922; }}
.issue-text {{ color: #f85149; }}
.info-text {{ color: #58a6ff; }}
.timestamp {{ color: #8b949e; font-size: 12px; margin-top: 24px; }}
</style>
</head>
<body>
<h1>🐉 龍魂 · 系统健康报告</h1>
<p class="timestamp">生成时间: {r['timestamp']}</p>

<div style="display:flex;align-items:center;margin:16px 0;">
  <span class="score">{r['overall_score']}</span>
  <span class="grade">{r['grade']}</span>
</div>

<div style="display:flex;gap:24px;margin:16px 0;">
  <span>⚙️ 引擎: {r.get('engine_count', 0)}</span>
  <span>📦 依赖: {r.get('dep_count', 0)}</span>
  <span>⚠️ 警告: {len(r['warnings'])}</span>
  <span>🔴 问题: {len(r['issues'])}</span>
</div>

<div class="bar"><div class="fill" style="width:{r['overall_score']}%"></div></div>

<h2 style="margin-top:24px;color:#ffd700;">引擎列表</h2>
<div class="grid">
"""

        for name, info in r["engines"].items():
            cls = "good" if info["exists"] else "warn"
            gpg_tag = "🔑 " if info["gpg_signed"] else ""
            html += f"""<div class="card {cls}">
  <div class="name">{gpg_tag}{name}</div>
  <div class="meta">{info['size_kb']}KB · {'可导入' if info['importable'] else '导入失败'}</div>
</div>
"""

        html += """</div>

<h2 style="margin-top:24px;color:#ffd700;">依赖检查</h2>
<table>
"""

        for dep, info in r["dependencies"].items():
            s = "✅" if info["installed"] else "❌"
            cls = "" if info["installed"] else "issue-text"
            html += f"<tr><td>{s}</td><td class=\"{cls}\">{dep}</td><td>{info.get('description', '')}</td><td>{info.get('version', '')}</td></tr>\n"

        html += "</table>"

        if r["warnings"]:
            html += '<h2 style="margin-top:24px;color:#d29922;">⚠️ 警告</h2><ul>'
            for w in r["warnings"]:
                html += f"<li class=\"warn-text\">{w}</li>"
            html += "</ul>"

        if r["issues"]:
            html += '<h2 style="margin-top:24px;color:#f85149;">🔴 问题</h2><ul>'
            for i in r["issues"]:
                html += f"<li class=\"issue-text\">{i}</li>"
            html += "</ul>"

        html += f"""
<p class="timestamp">
  DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-HEALTH-UID9622
</p>
</body></html>"""

        html_path = REPORTS_DIR / "health_report.html"
        html_path.write_text(html, encoding="utf-8")
        print(f"✅ HTML报告: {html_path}")
        return html_path

    def watch(self, interval: int = 60):
        """持续监控模式"""
        import time
        print(f"🔄 监控模式启动 (间隔 {interval}s)，Ctrl+C 停止")
        try:
            while True:
                self.results = {
                    "timestamp": datetime.now().isoformat(),
                    "engines": {},
                    "dependencies": {},
                    "overall_score": 100,
                    "issues": [],
                    "warnings": [],
                }
                self.check_engines()
                self.check_dependencies()
                self._compute_final_score()
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"[{ts}] 评分: {self.results['overall_score']}/100 ({self.results['grade']})")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n👋 监控停止")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·系统健康报告引擎")
    parser.add_argument("--html", action="store_true", help="生成HTML报告")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--watch", action="store_true", help="持续监控")
    parser.add_argument("--interval", type=int, default=60, help="监控间隔(秒)")
    args = parser.parse_args()

    health = SystemHealth()

    if args.watch:
        health.watch(args.interval)
    elif args.html:
        health.generate_html()
    elif args.json:
        print(json.dumps(health.generate_report(), ensure_ascii=False, indent=2))
    else:
        health.terminal_output()


if __name__ == "__main__":
    main()
