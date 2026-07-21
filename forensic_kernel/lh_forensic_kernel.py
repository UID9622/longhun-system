#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · Claude 留证取证内核 v1.0

功能：
  1. 自动扫描 /Users/zuimeidedeyihan/Downloads/Claude的留证 目录
  2. 对每份证据生成 DNA、SM3 哈希、时间戳、来源、模块标签
  3. 提取 Claude 承诺/实现过的功能模块，形成注册表
  4. 输出渲染变量（JSON / Markdown / HTML）
  5. 一键启动本地 API 服务，浏览器访问即可查看

标准语法：CNSH + 龍魂 DNA 追溯 + 三色审计
DNA: #龍芯⚡️2026-07-01-LONGHUN-FORENSIC-KERNEL-v1.0
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 加载国密工具
_HOME = Path.home()
if str(_HOME) not in sys.path:
    sys.path.insert(0, str(_HOME))
from CNSH_国密工具 import SM3

# 复用技能收集器
sys.path.insert(0, str(_HOME / "longhun-system" / "龍魂取证内核"))
from 龍魂技能收集器 import 收集技能 as _收集技能


# ============ 0. 常量与配置 ============
EVIDENCE_DIR = _HOME / "Downloads" / "Claude的留证"
OUTPUT_DIR = _HOME / "longhun-system" / "data" / "forensic_kernel"
DEFAULT_PORT = 8843

# 模块关键词表：模块名 -> 搜索关键词
MODULE_KEYWORDS: Dict[str, List[str]] = {
    "跨窗口持久化记忆": ["跨窗口记忆", "SESSION_MEMORY", "持久化记忆", "铁律 13"],
    "凭证管理系统": ["凭证管理", "CREDIBILITY-SYSTEM", "凭证", "确认码"],
    "文字即权重可视化": ["文字即权重", "权重可视化", "term_translator"],
    "单一真实源头": ["单一真实源头", "官方版本源", "版本源"],
    "DNA签章系统": ["DNA", "DNA签章", "dna_validator"],
    "三色审计": ["三色审计", "batch_auditor"],
    "五色审计": ["五色审计"],
    "十五人格API": ["15 人格", "persona_api", "P00", "P72"],
    "宝宝菜单系统": ["宝宝菜单", "宝宝_菜单系统"],
    "决策流场主控页": ["决策流场", "Notion 同步", "v2.7.36"],
    "新焊点验收": ["焊点", "validate_new_welding_point"],
    "Phase3 Web UI": ["Phase 3", "React 18", "FastAPI", "longhun-phase3"],
    "龍魂Skills集成": ["Skills", "longhun-skills"],
    "仓库治理": ["BFG", "M270", "大文件清理"],
    "安全修复": ["SECURITY-HOTFIX", "安全修复"],
    "longhun888.com部署": ["longhun888.com", "Cloudflare", "Let's Encrypt"],
}


# ============ 1. DNA 与哈希工具 ============
def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _生成DNA(主题: str, 版本: str = "v1.0") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S%f")
    short = hashlib.sha256(f"{主题}:{ts}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{ts[:8]}-{ts[9:]}-{主题}-{版本}-{short}"


def _sm3_hex(数据: bytes) -> str:
    return SM3.hash(数据).hex()


def _三色审计(内容: str) -> Tuple[str, str]:
    """
    简单主权审查：
      - 包含明显贬损/极端词汇 → 熔断
      - 包含情绪词 → 警告
      - 其他 → 通过
    """
    熔断词 = ["诈骗", "骗子", "他妈的", "洗脑", "操纵", "虚伪"]
    警告词 = ["愤怒", "失望", "对抗", "崩溃", "免責", "忽悠"]
    if any(w in 内容 for w in 熔断词):
        return "熔断", "内容包含极端/贬损词汇，已触发熔断"
    if any(w in 内容 for w in 警告词):
        return "警告", "内容包含情绪词，需复核"
    return "通过", "内容通过三色审计"


# ============ 2. 证据解析器 ============
class 证据记录:
    def __init__(self, 路径: Path):
        self.路径 = 路径
        self.文件名 = 路径.name
        self.类型 = self._判断类型()
        self.大小 = 路径.stat().st_size
        self.修改时间 = datetime.fromtimestamp(路径.stat().st_mtime, tz=timezone.utc).isoformat()
        self.原始内容 = self._读取()
        self.哈希 = _sm3_hex(self.原始内容.encode("utf-8"))
        self.DNA = self._生成记录DNA()
        self.摘要 = self._生成摘要()
        self.模块命中 = self._提取模块()
        self.情绪标签 = self._提取情绪()
        self.审计状态, self.审计说明 = _三色审计(self.原始内容[:20000])

    def _判断类型(self) -> str:
        suffix = self.路径.suffix.lower()
        if suffix == ".md":
            return "markdown"
        if suffix == ".txt":
            return "terminal_text"
        return "unknown"

    def _读取(self) -> str:
        try:
            return self.路径.read_text(encoding="utf-8")
        except Exception:
            return ""

    def _生成记录DNA(self) -> str:
        base = self.路径.stem.replace(" ", "_").replace(".", "_")[:40]
        return _生成DNA(base)

    def _生成摘要(self) -> str:
        lines = self.原始内容.splitlines()
        if not lines:
            return ""
        # 取前 5 行非空行
        non_empty = [l.strip() for l in lines if l.strip()][:5]
        return " | ".join(non_empty)[:300]

    def _提取模块(self) -> List[str]:
        hit = []
        lower = self.原始内容.lower()
        for 模块名, 关键词列表 in MODULE_KEYWORDS.items():
            if any(kw.lower() in lower for kw in 关键词列表):
                hit.append(模块名)
        return hit

    def _提取情绪(self) -> List[str]:
        tags = []
        lower = self.原始内容.lower()
        if any(w in lower for w in ["愤怒", "妈的", "滚", "失望", "崩溃"]):
            tags.append("愤怒")
        if any(w in lower for w in ["承诺", "保证", "一定"]):
            tags.append("承诺")
        if any(w in lower for w in ["完成", "验收", "部署", "发布"]):
            tags.append("落地")
        if any(w in lower for w in ["不懂", "小白", "我不会"]):
            tags.append("求助")
        return tags

    def to_dict(self) -> Dict[str, Any]:
        return {
            "文件名": self.文件名,
            "类型": self.类型,
            "大小": self.大小,
            "修改时间": self.修改时间,
            "DNA": self.DNA,
            "SM3哈希": self.哈希,
            "摘要": self.摘要,
            "模块命中": self.模块命中,
            "情绪标签": self.情绪标签,
            "审计状态": self.审计状态,
            "审计说明": self.审计说明,
        }


# ============ 3. 取证内核 ============
class 龍魂取证内核:
    def __init__(self, 证据目录: Optional[Path] = None, 输出目录: Optional[Path] = None):
        self.证据目录 = 证据目录 or EVIDENCE_DIR
        self.输出目录 = 输出目录 or OUTPUT_DIR
        self.输出目录.mkdir(parents=True, exist_ok=True)
        self.证据列表: List[证据记录] = []
        self.模块注册表: Dict[str, Dict[str, Any]] = {}
        self.渲染变量: Dict[str, Any] = {}
        self.DNA = "#龍芯⚡️2026-07-01-LONGHUN-FORENSIC-KERNEL-v1.0"

    def 加载证据(self) -> "龍魂取证内核":
        if not self.证据目录.exists():
            raise FileNotFoundError(f"证据目录不存在: {self.证据目录}")
        files = [f for f in self.证据目录.iterdir() if f.is_file() and f.suffix.lower() in (".md", ".txt")]
        self.证据列表 = [证据记录(f) for f in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)]
        return self

    def 构建模块注册表(self) -> "龍魂取证内核":
        registry: Dict[str, Dict[str, Any]] = {}
        for 模块名 in MODULE_KEYWORDS:
            registry[模块名] = {
                "模块名": 模块名,
                "证据来源": [],
                "提及次数": 0,
                "DNA": _生成DNA(模块名.replace(" ", "_")),
                "状态": "候选",
            }
        for ev in self.证据列表:
            for m in ev.模块命中:
                registry[m]["证据来源"].append(ev.文件名)
                registry[m]["提及次数"] += 1
        # 过滤掉完全没命中的模块
        self.模块注册表 = {k: v for k, v in registry.items() if v["提及次数"] > 0}
        for v in self.模块注册表.values():
            if v["提及次数"] >= 3:
                v["状态"] = "核心"
            elif v["提及次数"] >= 1:
                v["状态"] = "已识别"
        return self

    def 生成渲染变量(self) -> Dict[str, Any]:
        审计统计 = {"通过": 0, "警告": 0, "熔断": 0}
        for ev in self.证据列表:
            审计统计[ev.审计状态] = 审计统计.get(ev.审计状态, 0) + 1
        try:
            技能清单 = _收集技能()
        except Exception:
            技能清单 = {"技能总数": 0, "技能清单": [], "按状态分组": {}}
        self.渲染变量 = {
            "系统DNA": self.DNA,
            "生成时间": _now_iso(),
            "证据总数": len(self.证据列表),
            "模块总数": len(self.模块注册表),
            "技能总数": 技能清单.get("技能总数", 0),
            "审计统计": 审计统计,
            "证据列表": [ev.to_dict() for ev in self.证据列表],
            "模块注册表": list(self.模块注册表.values()),
            "技能清单": 技能清单.get("技能清单", []),
            "技能分组": 技能清单.get("按状态分组", {}),
            "情绪分布": self._情绪分布(),
            "总字节数": sum(ev.大小 for ev in self.证据列表),
        }
        return self.渲染变量

    def _情绪分布(self) -> Dict[str, int]:
        dist: Dict[str, int] = {}
        for ev in self.证据列表:
            for tag in ev.情绪标签:
                dist[tag] = dist.get(tag, 0) + 1
        return dist

    def 保存JSON(self) -> Path:
        path = self.输出目录 / "forensic_kernel_manifest.json"
        path.write_text(json.dumps(self.渲染变量, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def 生成Markdown报告(self) -> str:
        v = self.渲染变量
        lines = [
            "# 🐉 龍魂 · Claude 留证取证报告",
            f"**系统 DNA**: `{v['系统DNA']}`",
            f"**生成时间**: {v['生成时间']}",
            f"**证据总数**: {v['证据总数']} 份",
            f"**模块总数**: {v['模块总数']} 个",
            f"**总字节数**: {v['总字节数']:,}",
            "",
            "## 三色审计统计",
            f"- 🟢 通过: {v['审计统计'].get('通过', 0)}",
            f"- 🟡 警告: {v['审计统计'].get('警告', 0)}",
            f"- 🔴 熔断: {v['审计统计'].get('熔断', 0)}",
            "",
            "## 功能模块注册表",
        ]
        for m in v["模块注册表"]:
            lines.append(f"### {m['模块名']}")
            lines.append(f"- 状态: {m['状态']}")
            lines.append(f"- 提及次数: {m['提及次数']}")
            lines.append(f"- 证据来源: {', '.join(m['证据来源'])}")
            lines.append(f"- 模块 DNA: `{m['DNA']}`")
            lines.append("")
        lines.append("## 证据清单")
        for ev in v["证据列表"]:
            lines.append(f"### {ev['文件名']}")
            lines.append(f"- 类型: {ev['类型']} | 大小: {ev['大小']:,} bytes")
            lines.append(f"- 审计: {ev['审计状态']}")
            lines.append(f"- 模块: {', '.join(ev['模块命中']) or '无'}")
            lines.append(f"- DNA: `{ev['DNA']}`")
            lines.append(f"> 摘要: {ev['摘要']}")
            lines.append("")
        return "\n".join(lines)

    def 生成HTML面板(self) -> str:
        v = self.渲染变量
        rows = ""
        for ev in v["证据列表"]:
            badge = {"通过": "green", "警告": "orange", "熔断": "red"}.get(ev["审计状态"], "gray")
            rows += f"""
            <tr>
              <td>{ev['文件名']}</td>
              <td>{ev['类型']}</td>
              <td>{ev['大小']:,}</td>
              <td><span style="color:{badge}">{ev['审计状态']}</span></td>
              <td>{', '.join(ev['模块命中']) or '-'}</td>
              <td><code>{ev['DNA']}</code></td>
            </tr>
            """
        module_cards = ""
        for m in v["模块注册表"]:
            module_cards += f"""
            <div style="border:1px solid #ccc;padding:10px;margin:10px 0;border-radius:6px;">
              <h3>{m['模块名']}</h3>
              <p>状态: <strong>{m['状态']}</strong> | 提及: {m['提及次数']} 次</p>
              <p>来源: {', '.join(m['证据来源'])}</p>
              <p><code>{m['DNA']}</code></p>
            </div>
            """
        skill_rows = ""
        for s in sorted(v.get("技能清单", []), key=lambda x: x.get("提及次数", 0), reverse=True):
            status_color = {"已实现/已部署": "green", "已识别": "orange", "候选": "gray"}.get(s["状态"], "black")
            skill_rows += f"""
            <tr>
              <td><strong>{s['技能名']}</strong></td>
              <td><span style="color:{status_color}">{s['状态']}</span></td>
              <td>{s['提及次数']}</td>
              <td>{', '.join(s['来源文件'][:3])}{'...' if len(s['来源文件']) > 3 else ''}</td>
              <td><code>{', '.join(s['关键词'][:3])}</code></td>
            </tr>
            """
        return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>龍魂取证内核面板</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 40px; background: #f7f7f7; }}
  .container {{ max-width: 1200px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
  h1 {{ color: #b91c1c; }}
  .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin: 20px 0; }}
  .card {{ background: #fafafa; border-left: 4px solid #b91c1c; padding: 16px; border-radius: 6px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
  th, td {{ text-align: left; padding: 10px; border-bottom: 1px solid #eee; font-size: 14px; }}
  th {{ background: #f0f0f0; }}
  code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 4px; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">
  <h1>🐉 龍魂 · Claude 留证取证内核</h1>
  <p><strong>系统 DNA:</strong> <code>{v['系统DNA']}</code></p>
  <p><strong>生成时间:</strong> {v['生成时间']}</p>
  <div class="summary">
    <div class="card"><strong>证据总数</strong><br>{v['证据总数']}</div>
    <div class="card"><strong>模块总数</strong><br>{v['模块总数']}</div>
    <div class="card"><strong>技能总数</strong><br>{v.get('技能总数', 0)}</div>
    <div class="card"><strong>🟢 通过</strong><br>{v['审计统计'].get('通过', 0)}</div>
    <div class="card"><strong>🟡 警告</strong><br>{v['审计统计'].get('警告', 0)}</div>
    <div class="card"><strong>🔴 熔断</strong><br>{v['审计统计'].get('熔断', 0)}</div>
  </div>
  <h2>技能清单（统一注册）</h2>
  <table>
    <tr><th>技能名</th><th>状态</th><th>提及次数</th><th>来源文件</th><th>关键词</th></tr>
    {skill_rows}
  </table>
  <h2>功能模块注册表</h2>
  {module_cards}
  <h2>证据清单</h2>
  <table>
    <tr><th>文件名</th><th>类型</th><th>大小</th><th>审计</th><th>命中模块</th><th>DNA</th></tr>
    {rows}
  </table>
</div>
</body>
</html>"""


# ============ 4. API 服务 ============
def _构建Flask应用(内核: 龍魂取证内核):
    from flask import Flask, jsonify, Response
    app = Flask(__name__)

    @app.route("/")
    def 首页():
        return Response(内核.生成HTML面板(), mimetype="text/html")

    @app.route("/api/manifest")
    def API清单():
        return jsonify(内核.渲染变量)

    @app.route("/api/modules")
    def API模块():
        return jsonify(list(内核.模块注册表.values()))

    @app.route("/api/evidence")
    def API证据():
        return jsonify([ev.to_dict() for ev in 内核.证据列表])

    @app.route("/report.md")
    def Markdown报告():
        return Response(内核.生成Markdown报告(), mimetype="text/markdown; charset=utf-8")

    return app


# ============ 5. 一键启动脚本 ============
def _生成启动脚本():
    script = _HOME / "longhun-system" / "龍魂取证内核" / "start_kernel.sh"
    script.write_text(
        "#!/bin/bash\n"
        "# 龍魂取证内核一键启动\n"
        "cd \"$(dirname \"$0\")\"\n"
        "python3 龍魂取证内核.py --start\n",
        encoding="utf-8",
    )
    script.chmod(0o755)
    return script


# ============ 6. CLI 入口 ============
def main():
    parser = argparse.ArgumentParser(description="龍魂 · Claude 留证取证内核")
    parser.add_argument("--start", action="store_true", help="一键启动 API 服务")
    parser.add_argument("--report", action="store_true", help="生成 Markdown 报告")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"服务端口（默认 {DEFAULT_PORT}）")
    args = parser.parse_args()

    内核 = 龍魂取证内核().加载证据().构建模块注册表()
    内核.生成渲染变量()
    manifest_path = 内核.保存JSON()
    _生成启动脚本()

    if args.report:
        report = 内核.生成Markdown报告()
        report_path = OUTPUT_DIR / "forensic_kernel_report.md"
        report_path.write_text(report, encoding="utf-8")
        print(report)
        print(f"\n报告已保存: {report_path}")
        return

    if args.start:
        app = _构建Flask应用(内核)
        print(f"🐉 龍魂取证内核已启动")
        print(f"   系统 DNA: {内核.DNA}")
        print(f"   证据目录: {内核.证据目录}")
        print(f"   清单文件: {manifest_path}")
        print(f"   访问面板: http://127.0.0.1:{args.port}/")
        print(f"   API 清单: http://127.0.0.1:{args.port}/api/manifest")
        print(f"   Markdown: http://127.0.0.1:{args.port}/report.md")
        app.run(host="127.0.0.1", port=args.port, threaded=True)
        return

    # 默认：生成清单 + 打印摘要
    print("🐉 龍魂取证内核处理完成")
    print(f"   系统 DNA: {内核.DNA}")
    print(f"   证据总数: {内核.渲染变量['证据总数']}")
    print(f"   模块总数: {内核.渲染变量['模块总数']}")
    print(f"   审计统计: {内核.渲染变量['审计统计']}")
    print(f"   清单文件: {manifest_path}")
    print(f"\n一键启动: python3 {__file__} --start")


if __name__ == "__main__":
    main()
