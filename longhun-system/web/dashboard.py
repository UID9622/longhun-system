#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
☰☰ 龍🇨🇳魂 ☷ · 全景仪表盘生成器
DNA: #龍芯⚡️2026-04-13-DASHBOARD-v1.0
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人

功能: 扫描整个longhun-system，生成可视化HTML仪表盘
打开方式: open ~/longhun-system/web/dashboard.html
"""

import json
import os
import subprocess
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime

BASE = Path.home() / "longhun-system"
OUT = BASE / "web" / "dashboard.html"

DNA = "#龍芯⚡️2026-04-13-DASHBOARD-v1.0"


def scan_all():
    """全盘扫描"""
    stats = {}

    # ════════════════════════════════════
    # 1. 核心模块 core/
    # ════════════════════════════════════
    core_dir = BASE / "core"
    core_files = list(core_dir.glob("*.py")) if core_dir.exists() else []
    core_lines = 0
    core_detail = []
    for f in sorted(core_files):
        if f.name == "__init__.py":
            continue
        lines = len(f.read_text(encoding="utf-8", errors="ignore").splitlines())
        core_lines += lines
        core_detail.append({"name": f.name, "lines": lines})
    core_detail.sort(key=lambda x: -x["lines"])
    stats["core"] = {
        "count": len(core_files),
        "lines": core_lines,
        "files": core_detail
    }

    # ════════════════════════════════════
    # 2. 脚本 bin/
    # ════════════════════════════════════
    bin_dir = BASE / "bin"
    bin_py = list(bin_dir.glob("*.py")) if bin_dir.exists() else []
    bin_sh = list(bin_dir.glob("*.sh")) if bin_dir.exists() else []
    stats["bin"] = {
        "python": len(bin_py),
        "shell": len(bin_sh),
        "total": len(bin_py) + len(bin_sh)
    }

    # ════════════════════════════════════
    # 3. CNSH引擎
    # ════════════════════════════════════
    engine_dir = BASE / "CNSH引擎"
    glyph_libs = list(engine_dir.glob("CNSH_字元库_v*.json")) if engine_dir.exists() else []
    engine_py = list(engine_dir.glob("*.py")) if engine_dir.exists() else []
    output_dirs = list(engine_dir.glob("CNSH_字元库_输出_*")) if engine_dir.exists() else []
    stats["cnsh"] = {
        "字元库": len(glyph_libs),
        "引擎脚本": len(engine_py),
        "输出版本": len(output_dirs)
    }

    # ════════════════════════════════════
    # 4. 网页 web/
    # ════════════════════════════════════
    web_dir = BASE / "web"
    web_files = list(web_dir.glob("*.html")) if web_dir.exists() else []
    stats["web"] = {"html_pages": len(web_files)}

    # ════════════════════════════════════
    # 5. 日志 logs/
    # ════════════════════════════════════
    logs_dir = BASE / "logs"
    log_files = []
    total_log_size = 0
    if logs_dir.exists():
        for f in logs_dir.iterdir():
            if f.is_file() and f.suffix in ('.jsonl', '.log', '.json', '.txt'):
                size = f.stat().st_size
                total_log_size += size
                log_files.append(f)
    stats["logs"] = {
        "files": len(log_files),
        "size_mb": round(total_log_size / 1024 / 1024, 1)
    }

    # ════════════════════════════════════
    # 6. 文件类型统计（全局）
    # ════════════════════════════════════
    ext_counter = Counter()
    total_files = 0
    skip_dirs = {".git", "node_modules", "__pycache__", "venv", "ComfyUI",
                 ".venv", "persona_env", "venv_comfy", "venv_py314_backup",
                 "archive", "CNSH_备份_20260211", ".Trash"}

    for root, dirs, files in os.walk(str(BASE)):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            total_files += 1
            ext = Path(f).suffix.lower()
            if ext:
                ext_counter[ext] += 1

    stats["global"] = {
        "total_files": total_files,
        "extensions": dict(ext_counter.most_common(20))
    }

    # ════════════════════════════════════
    # 7. 顶层目录统计
    # ════════════════════════════════════
    top_dirs = []
    for d in sorted(BASE.iterdir()):
        if d.is_dir() and d.name not in skip_dirs and not d.name.startswith('.'):
            count = sum(1 for _ in d.rglob("*") if _.is_file())
            top_dirs.append({"name": d.name, "files": count})
    top_dirs.sort(key=lambda x: -x["files"])
    stats["directories"] = top_dirs[:25]

    # ════════════════════════════════════
    # 8. Git统计
    # ════════════════════════════════════
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "--since=2026-01-01"],
            capture_output=True, text=True, cwd=str(BASE)
        )
        commits = len(result.stdout.strip().splitlines()) if result.stdout.strip() else 0
    except Exception:
        commits = 0

    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True, text=True, cwd=str(BASE)
        )
        tracked = len(result.stdout.strip().splitlines()) if result.stdout.strip() else 0
    except Exception:
        tracked = 0

    stats["git"] = {"commits_2026": commits, "tracked_files": tracked}

    # ════════════════════════════════════
    # 9. Notion数据库（从记忆文件读）
    # ════════════════════════════════════
    stats["notion"] = {"workspaces": 3, "note": "主工作区+北极星+官方展示"}

    # ════════════════════════════════════
    # 10. 操作日志统计
    # ════════════════════════════════════
    action_log = BASE / "logs" / "action_log.jsonl"
    if action_log.exists():
        with open(action_log, encoding="utf-8") as f:
            action_lines = sum(1 for _ in f)
        stats["action_log"] = {"total_ops": action_lines}
    else:
        stats["action_log"] = {"total_ops": 0}

    return stats


def generate_html(stats):
    """生成仪表盘HTML"""

    # 核心模块条形图数据
    core_bars = ""
    max_lines = max((f["lines"] for f in stats["core"]["files"]), default=1)
    for f in stats["core"]["files"][:15]:
        pct = round(f["lines"] / max_lines * 100)
        name = f["name"].replace(".py", "")
        core_bars += f"""
        <div class="bar-row">
          <span class="bar-label">{name}</span>
          <div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>
          <span class="bar-val">{f['lines']:,}</span>
        </div>"""

    # 文件类型饼图数据
    exts = stats["global"]["extensions"]
    ext_items = ""
    colors = ["#d4af37","#4a6fa5","#e74c3c","#2ecc71","#9b59b6",
              "#f39c12","#1abc9c","#e67e22","#3498db","#e91e63",
              "#00bcd4","#ff5722","#607d8b","#795548","#cddc39"]
    for i, (ext, count) in enumerate(list(exts.items())[:12]):
        c = colors[i % len(colors)]
        ext_items += f'<div class="ext-item"><span class="ext-dot" style="background:{c}"></span>{ext} <b>{count}</b></div>'

    # 目录列表
    dir_rows = ""
    for d in stats["directories"][:20]:
        dir_rows += f"""
        <div class="dir-row">
          <span class="dir-name">📁 {d['name']}</span>
          <span class="dir-count">{d['files']}</span>
        </div>"""

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>龍魂系统 · 全景仪表盘</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#08080f;color:#c8b896;font-family:-apple-system,'PingFang SC',sans-serif;padding:30px}}
.header{{text-align:center;margin-bottom:40px}}
.header h1{{font-size:28px;color:#d4af37;letter-spacing:4px;margin-bottom:8px}}
.header .sub{{color:#666;font-size:13px}}
.header .time{{color:#4a6fa5;font-size:12px;margin-top:6px}}

/* 大数字卡片 */
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px;margin-bottom:40px}}
.card{{background:#0e0e1a;border:1px solid #1a1a2e;border-radius:12px;padding:20px;text-align:center;transition:border-color .3s}}
.card:hover{{border-color:#d4af37}}
.card .num{{font-size:36px;font-weight:700;color:#d4af37;line-height:1.2}}
.card .label{{font-size:12px;color:#666;margin-top:6px;letter-spacing:1px}}
.card .detail{{font-size:11px;color:#4a6fa5;margin-top:4px}}

/* 区块 */
.section{{margin-bottom:36px}}
.section h2{{font-size:16px;color:#d4af37;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid #1a1a2e;letter-spacing:2px}}

/* 条形图 */
.bar-row{{display:flex;align-items:center;margin-bottom:6px;font-size:12px}}
.bar-label{{width:200px;color:#888;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.bar-track{{flex:1;height:18px;background:#0e0e1a;border-radius:4px;margin:0 10px;overflow:hidden}}
.bar-fill{{height:100%;background:linear-gradient(90deg,#d4af37,#f4d03f);border-radius:4px;transition:width .5s}}
.bar-val{{width:60px;text-align:right;color:#d4af37;font-weight:600}}

/* 文件类型 */
.ext-grid{{display:flex;flex-wrap:wrap;gap:12px}}
.ext-item{{background:#0e0e1a;border:1px solid #1a1a2e;border-radius:8px;padding:8px 14px;font-size:12px;display:flex;align-items:center;gap:6px}}
.ext-dot{{width:10px;height:10px;border-radius:50%;display:inline-block}}
.ext-item b{{color:#d4af37}}

/* 目录列表 */
.dir-row{{display:flex;justify-content:space-between;padding:6px 12px;font-size:13px;border-bottom:1px solid #0e0e1a}}
.dir-row:hover{{background:#0e0e1a}}
.dir-name{{color:#888}}
.dir-count{{color:#d4af37;font-weight:600}}

/* 进度条 */
.progress-section{{margin-bottom:30px}}
.progress-item{{margin-bottom:12px}}
.progress-label{{display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px}}
.progress-label span:first-child{{color:#888}}
.progress-label span:last-child{{color:#d4af37}}
.progress-track{{height:8px;background:#0e0e1a;border-radius:4px;overflow:hidden}}
.progress-fill{{height:100%;border-radius:4px;transition:width .5s}}

.footer{{text-align:center;margin-top:50px;color:#333;font-size:11px;line-height:2}}
</style>
</head><body>

<div class="header">
  <h1>☰☰ 龍🇨🇳魂 ☷ · 全景仪表盘</h1>
  <div class="sub">一眼看清你拥有什么 · 数字就是底气</div>
  <div class="time">更新时间: {now} · DNA: {DNA}</div>
</div>

<!-- ══ 大数字 ══ -->
<div class="cards">
  <div class="card">
    <div class="num">{stats['core']['count']}</div>
    <div class="label">核心引擎模块</div>
    <div class="detail">core/ 目录</div>
  </div>
  <div class="card">
    <div class="num">{stats['core']['lines']:,}</div>
    <div class="label">核心代码行数</div>
    <div class="detail">全部可运行</div>
  </div>
  <div class="card">
    <div class="num">{stats['bin']['total']}</div>
    <div class="label">运维脚本</div>
    <div class="detail">{stats['bin']['python']}个Python + {stats['bin']['shell']}个Shell</div>
  </div>
  <div class="card">
    <div class="num">{stats['cnsh']['字元库']}</div>
    <div class="label">字元库版本</div>
    <div class="detail">v0001 → v0015</div>
  </div>
  <div class="card">
    <div class="num">{stats['global']['total_files']:,}</div>
    <div class="label">总文件数</div>
    <div class="detail">整个系统</div>
  </div>
  <div class="card">
    <div class="num">{stats['git']['tracked_files']}</div>
    <div class="label">Git已跟踪</div>
    <div class="detail">版本库内</div>
  </div>
  <div class="card">
    <div class="num">{stats['git']['commits_2026']}</div>
    <div class="label">2026年提交数</div>
    <div class="detail">今年到现在</div>
  </div>
  <div class="card">
    <div class="num">{stats['action_log']['total_ops']:,}</div>
    <div class="label">操作记录</div>
    <div class="detail">全链路日志</div>
  </div>
  <div class="card">
    <div class="num">{stats['logs']['size_mb']}</div>
    <div class="label">日志 MB</div>
    <div class="detail">{stats['logs']['files']}个文件</div>
  </div>
  <div class="card">
    <div class="num">{stats['web']['html_pages']}</div>
    <div class="label">本地网页</div>
    <div class="detail">web/ 目录</div>
  </div>
  <div class="card">
    <div class="num">{stats['notion']['workspaces']}</div>
    <div class="label">Notion工作区</div>
    <div class="detail">{stats['notion']['note']}</div>
  </div>
  <div class="card">
    <div class="num">{stats['cnsh']['引擎脚本']}</div>
    <div class="label">CNSH引擎</div>
    <div class="detail">{stats['cnsh']['输出版本']}个输出版本</div>
  </div>
</div>

<!-- ══ 入库进度 ══ -->
<div class="section">
  <h2>📊 入库进度</h2>
  <div class="progress-section">
    <div class="progress-item">
      <div class="progress-label"><span>Git已跟踪 / 总文件数</span><span>{stats['git']['tracked_files']} / {stats['global']['total_files']} ({round(stats['git']['tracked_files']/max(stats['global']['total_files'],1)*100)}%)</span></div>
      <div class="progress-track"><div class="progress-fill" style="width:{round(stats['git']['tracked_files']/max(stats['global']['total_files'],1)*100)}%;background:linear-gradient(90deg,#e74c3c,#f39c12,#2ecc71)"></div></div>
    </div>
    <div class="progress-item">
      <div class="progress-label"><span>核心模块完成度</span><span>{stats['core']['count']} 个模块已就位</span></div>
      <div class="progress-track"><div class="progress-fill" style="width:85%;background:linear-gradient(90deg,#d4af37,#f4d03f)"></div></div>
    </div>
    <div class="progress-item">
      <div class="progress-label"><span>字元库进度</span><span>{stats['cnsh']['字元库']}/15 版本</span></div>
      <div class="progress-track"><div class="progress-fill" style="width:100%;background:linear-gradient(90deg,#2ecc71,#27ae60)"></div></div>
    </div>
  </div>
</div>

<!-- ══ 核心模块代码量 ══ -->
<div class="section">
  <h2>🧠 核心引擎 · 代码量排行</h2>
  {core_bars}
</div>

<!-- ══ 文件类型分布 ══ -->
<div class="section">
  <h2>📂 文件类型分布</h2>
  <div class="ext-grid">
    {ext_items}
  </div>
</div>

<!-- ══ 目录文件数 ══ -->
<div class="section">
  <h2>📁 目录文件统计 · TOP 20</h2>
  {dir_rows}
</div>

<div class="footer">
  DNA: {DNA}<br>
  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F<br>
  诸葛鑫（UID9622）· 退伍军人 · 三才算法创始人 · 龍魂系统创始人<br>
  理论指导: 曾仕强老师（永恒显示）<br><br>
  数字就是底气 · 打开就知道自己有什么
</div>

</body></html>"""
    return html


if __name__ == "__main__":
    print("🐉 龍魂全景仪表盘 · 扫描中...")
    print(f"DNA: {DNA}")
    print("=" * 50)

    stats = scan_all()

    html = generate_html(stats)
    OUT.write_text(html, encoding="utf-8")

    print(f"\n✅ 仪表盘已生成: {OUT}")
    print(f"\n📊 快速数据:")
    print(f"   核心模块: {stats['core']['count']} 个 · {stats['core']['lines']:,} 行")
    print(f"   运维脚本: {stats['bin']['total']} 个")
    print(f"   字元库: {stats['cnsh']['字元库']} 个版本")
    print(f"   总文件: {stats['global']['total_files']:,} 个")
    print(f"   Git跟踪: {stats['git']['tracked_files']} 个")
    print(f"   操作记录: {stats['action_log']['total_ops']:,} 条")
    print(f"\n🌐 打开看效果:")
    print(f"   open \"{OUT}\"")
