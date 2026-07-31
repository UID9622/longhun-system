#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# 龍魂系统 · 统一采集服务 v3.0
# 两线汇入：浏览器扩展实时采集 + 数据中台本地直读
# DNA: #龍芯⚡️丙午·乙申·COLLECTOR-v3.0-SERVER
# UID9622 | 龍芯北辰
# ============================================================

import json
import os
import sys
import time
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HOME = Path.home()
PROJECT = HOME / "longhun-system"
DATA_DIR = PROJECT / "data" / "collector" / "raw"
HUB_DIR = PROJECT / "data-hub" / "raw"
LOG_DIR = PROJECT / "logs"
DATA_DIR.mkdir(parents=True, exist_ok=True)

VALID_DNA = [
    "#龍芯⚡️丙午·乙申·COLLECTOR-v2.0",
    "ZHUGEXIN-2025-CHINA-LONGHUN",
]

TIANGAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DIZHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
BASE_YEAR = 1984

def get_ganzhi():
    offset = datetime.now().year - BASE_YEAR
    return f"{TIANGAN[offset % 10]}{DIZHI[offset % 12]}"

def compute_hash(data_str):
    return hashlib.sha256(data_str.encode()).hexdigest()[:16]

# ---- 采集统计内存缓存 ----
_stats_cache = {"time": 0, "data": {}}
_collection_log = []  # 最近采集记录

def get_all_stats():
    """获取完整统计，5秒缓存"""
    global _stats_cache
    now = time.time()
    if now - _stats_cache["time"] < 5:
        return _stats_cache["data"]
    
    total_files = 0
    total_size = 0
    sites = {}
    dates = {}
    recent = []
    
    try:
        for root, dirs, files in os.walk(DATA_DIR):
            for f in sorted(files, reverse=True):
                if f.endswith(".json"):
                    fp = os.path.join(root, f)
                    total_files += 1
                    sz = os.path.getsize(fp)
                    total_size += sz
                    
                    # 解析站点
                    parts = f.split("_")
                    if len(parts) >= 2:
                        site = parts[1]
                        sites[site] = sites.get(site, 0) + 1
                    
                    # 按日期统计
                    rel = os.path.relpath(root, DATA_DIR)
                    date_part = rel.split("/")[0] if "/" in rel else rel
                    if len(date_part) == 10:  # YYYY-MM-DD
                        dates[date_part] = dates.get(date_part, 0) + 1
                    
                    # 最近10条
                    if len(recent) < 10:
                        try:
                            with open(fp, "r", encoding="utf-8") as rf:
                                d = json.load(rf)
                                recent.append({
                                    "site": d.get("site", "?"),
                                    "title": d.get("title", "")[:60],
                                    "url": d.get("url", ""),
                                    "time": d.get("_saved_at", ""),
                                })
                        except:
                            pass
    except:
        pass
    
    data = {
        "total_files": total_files,
        "total_size_mb": round(total_size / 1024 / 1024, 2),
        "sites": sites,
        "dates": dict(sorted(dates.items(), reverse=True)[:7]),
        "recent": recent,
        "ganzhi": get_ganzhi(),
    }
    _stats_cache = {"time": now, "data": data}
    return data

def save_data(data):
    site = data.get("site", "unknown").replace(" ", "_")
    ts = data.get("timestamp", int(time.time() * 1000))
    ganzhi = get_ganzhi()
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    site_dir = DATA_DIR / date_str / site
    site_dir.mkdir(parents=True, exist_ok=True)
    
    session_id = str(data.get("title", data.get("url", "unknown")))[:30]
    session_id = "".join(c if c.isalnum() or c in "_-" else "_" for c in session_id)
    filename = f"{ts}_{site}_{session_id}.json"
    filepath = site_dir / filename
    
    data["_ganzhi"] = ganzhi
    data["_hash"] = compute_hash(json.dumps(data, sort_keys=True, ensure_ascii=False))
    data["_saved_at"] = datetime.now().isoformat()
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    # 记录到采集日志
    _collection_log.append({
        "site": site,
        "title": data.get("title", "")[:50],
        "time": datetime.now().strftime("%H:%M:%S"),
    })
    if len(_collection_log) > 100:
        _collection_log.pop(0)
    
    return str(filepath)


# ==================== API ====================

@app.route("/", methods=["GET"])
@app.route("/dashboard", methods=["GET"])
def dashboard():
    """统一采集看板"""
    return render_template_string(DASHBOARD_HTML, ganzhi=get_ganzhi())

@app.route("/collect", methods=["POST"])
def collect():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"code": 400, "message": "无有效数据"}), 400
    
    dna = data.get("dna", "")
    if dna not in VALID_DNA:
        return jsonify({"code": 403, "message": "DNA不匹配"}), 403
    
    filepath = save_data(data)
    return jsonify({"code": 200, "status": "SAVED", "filepath": filepath, "ganzhi": get_ganzhi()})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"code": 200, "status": "UP", "service": "longhun-collector", "version": "3.0.0", "ganzhi": get_ganzhi()})

@app.route("/api/stats", methods=["GET"])
def api_stats():
    return jsonify({"code": 200, **get_all_stats()})

@app.route("/api/log", methods=["GET"])
def api_log():
    return jsonify({"code": 200, "log": _collection_log[-50:]})

@app.route("/api/hub/run", methods=["POST"])
def run_hub():
    """触发数据中台采集"""
    script = PROJECT / "scripts" / "龍魂数据中台采集器.py"
    if not script.exists():
        return jsonify({"code": 404, "message": "数据中台脚本不存在"}), 404
    
    try:
        result = subprocess.run(
            [sys.executable, str(script), "--sync"],
            capture_output=True, text=True, timeout=120
        )
        return jsonify({
            "code": 200,
            "stdout": result.stdout[-2000:],
            "stderr": result.stderr[-500:],
            "returncode": result.returncode,
        })
    except subprocess.TimeoutExpired:
        return jsonify({"code": 408, "message": "采集超时"}), 408
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)}), 500

@app.route("/api/hub/status", methods=["GET"])
def hub_status():
    """数据中台状态"""
    exists = (PROJECT / "scripts" / "龍魂数据中台采集器.py").exists()
    hub_files = 0
    hub_size = 0
    if HUB_DIR.exists():
        for f in HUB_DIR.rglob("*"):
            if f.is_file():
                hub_files += 1
                hub_size += f.stat().st_size
    return jsonify({
        "code": 200,
        "exists": exists,
        "hub_files": hub_files,
        "hub_size_mb": round(hub_size / 1024 / 1024, 2),
    })

@app.route("/export", methods=["GET"])
def export_data():
    site = request.args.get("site", "")
    limit = int(request.args.get("limit", 100))
    date_str = request.args.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    results = []
    search_dir = DATA_DIR / date_str
    if not search_dir.is_dir():
        return jsonify({"code": 404, "message": f"日期 {date_str} 无数据"}), 404
    
    for root, dirs, files in os.walk(search_dir):
        for f in sorted(files, reverse=True):
            if f.endswith(".json"):
                if site and site not in root:
                    continue
                try:
                    with open(os.path.join(root, f), "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                        data.pop("_hash", None)
                        data.pop("_saved_at", None)
                        results.append(data)
                except:
                    continue
                if len(results) >= limit:
                    break
        if len(results) >= limit:
            break
    
    return jsonify({"code": 200, "count": len(results), "data": results})


# ==================== 看板 HTML ====================

DASHBOARD_HTML = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>龍魂采集看板 v3.0</title>
<style>
:root {
  --bg: #080812; --card: #12122a; --gold: #ffd700; --gold-dim: #b8960f;
  --green: #4ade80; --red: #f87171; --blue: #60a5fa;
  --text: #e2e8f0; --muted: #64748b; --border: #1e2950;
  --radius: 12px;
}
* { margin:0; padding:0; box-sizing:border-box; }
body {
  font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: var(--bg); color: var(--text); min-height: 100vh;
  background-image: radial-gradient(ellipse at top, #1a1a3e22 0%, transparent 60%);
}
.header {
  background: linear-gradient(135deg, #0f0f2e 0%, #1a1a3e 100%);
  padding: 20px 32px; border-bottom: 2px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
}
.header-left { display: flex; align-items: center; gap: 14px; }
.logo { font-size: 36px; }
.header h1 { font-size: 22px; color: var(--gold); letter-spacing: 2px; }
.header-sub { font-size: 12px; color: var(--muted); }
.dna-badge {
  font-family: monospace; font-size: 10px;
  background: var(--card); color: var(--gold-dim);
  padding: 6px 14px; border-radius: 20px; border: 1px solid var(--border);
}
.container { max-width: 1100px; margin: 0 auto; padding: 24px; }

/* Status Bar */
.status-row {
  display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap;
}
.status-card {
  flex: 1; min-width: 140px; background: var(--card);
  border: 1px solid var(--border); border-radius: var(--radius);
  padding: 16px; text-align: center;
}
.status-card .val { font-size: 28px; font-weight: 700; }
.status-card .val.gold { color: var(--gold); }
.status-card .val.green { color: var(--green); }
.status-card .val.blue { color: var(--blue); }
.status-card .label { font-size: 11px; color: var(--muted); margin-top: 4px; }
.status-dot {
  display: inline-block; width: 8px; height: 8px; border-radius: 50%;
  margin-right: 6px; animation: pulse 2s infinite;
}
.status-dot.online { background: var(--green); box-shadow: 0 0 8px var(--green); }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }

/* Actions */
.actions { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
.btn {
  padding: 12px 24px; border: none; border-radius: var(--radius);
  font-size: 14px; font-weight: 600; cursor: pointer; transition: all .2s;
  display: flex; align-items: center; gap: 6px;
}
.btn-gold { background: var(--gold); color: #080812; }
.btn-gold:hover { background: #ffe44d; transform: translateY(-1px); }
.btn-outline { background: transparent; color: var(--text); border: 1px solid var(--border); }
.btn-outline:hover { border-color: var(--gold-dim); }
.btn-green { background: #14532d; color: var(--green); border: 1px solid #166534; }
.btn-green:hover { background: #166534; }

/* Grid */
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }
@media (max-width: 700px) { .grid-2 { grid-template-columns: 1fr; } }

.card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 20px;
}
.card-title {
  font-size: 13px; color: var(--gold); text-transform: uppercase;
  letter-spacing: 2px; margin-bottom: 14px; display: flex; align-items: center; gap: 8px;
}

/* Site Tags */
.site-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.site-tag {
  font-size: 12px; padding: 6px 14px; border-radius: 20px;
  background: #1a1a3e; border: 1px solid var(--border); color: var(--text);
  display: flex; align-items: center; gap: 6px;
}
.site-tag .count {
  background: var(--gold); color: #080812; font-weight: 700;
  font-size: 11px; padding: 1px 7px; border-radius: 10px;
}

/* Recent List */
.recent-item {
  padding: 10px 0; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 10px; font-size: 13px;
}
.recent-item:last-child { border-bottom: none; }
.recent-site {
  font-size: 11px; padding: 2px 8px; border-radius: 4px;
  background: #1a1a3e; color: var(--gold-dim); white-space: nowrap;
}
.recent-title { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--text); }
.recent-time { font-size: 11px; color: var(--muted); white-space: nowrap; }

/* Log Feed */
.log-feed { max-height: 300px; overflow-y: auto; font-family: monospace; font-size: 12px; }
.log-item {
  padding: 4px 0; color: var(--muted);
  border-bottom: 1px solid #1e295022;
}
.log-item .ts { color: var(--gold-dim); margin-right: 8px; }

/* Empty State */
.empty {
  text-align: center; padding: 30px; color: var(--muted);
  font-size: 14px;
}

/* Toast */
.toast {
  position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
  background: var(--card); border: 1px solid var(--gold);
  color: var(--gold); padding: 10px 24px; border-radius: 20px;
  font-size: 13px; z-index: 99; opacity: 0; transition: opacity .3s; pointer-events: none;
}
.toast.show { opacity: 1; }

.footer {
  text-align: center; padding: 20px; color: var(--muted); font-size: 11px;
  border-top: 1px solid var(--border); margin-top: 20px;
}
</style>
</head>
<body>

<div class="header">
  <div class="header-left">
    <div class="logo">🐉</div>
    <div>
      <h1>龍魂采集看板 v3.0</h1>
      <div class="header-sub">UID9622 · 两线汇一 · 主权归集</div>
    </div>
  </div>
  <div class="dna-badge">#龍芯⚡️{{ ganzhi }}·COLLECTOR-v3.0</div>
</div>

<div class="container">

  <!-- 状态行 -->
  <div class="status-row">
    <div class="status-card">
      <div><span class="status-dot online"></span><span style="font-size:12px;color:var(--green)">服务在线</span></div>
      <div class="label">采集服务 :9622</div>
    </div>
    <div class="status-card">
      <div class="val gold" id="totalFiles">0</div>
      <div class="label">已采集文件</div>
    </div>
    <div class="status-card">
      <div class="val blue" id="totalSize">0 MB</div>
      <div class="label">数据总量</div>
    </div>
    <div class="status-card">
      <div class="val green" id="hubFiles">-</div>
      <div class="label">数据中台文件</div>
    </div>
  </div>

  <!-- 操作按钮 -->
  <div class="actions">
    <button class="btn btn-gold" onclick="runHub()">📡 运行数据中台采集</button>
    <button class="btn btn-outline" onclick="refreshAll()">🔄 刷新数据</button>
    <button class="btn btn-green" onclick="window.open('/export?limit=50')">📤 导出最近50条</button>
  </div>

  <!-- 双列布局 -->
  <div class="grid-2">
    <!-- 站点分布 -->
    <div class="card">
      <div class="card-title">📡 站点分布</div>
      <div class="site-tags" id="siteTags">
        <div class="empty">暂无采集数据</div>
      </div>
    </div>

    <!-- 日期趋势 -->
    <div class="card">
      <div class="card-title">📅 近7日趋势</div>
      <div id="dateTrends" style="font-size:13px;">
        <div class="empty">暂无趋势数据</div>
      </div>
    </div>
  </div>

  <!-- 最近采集 -->
  <div class="card" style="margin-bottom:20px;">
    <div class="card-title">📋 最近采集 (实时刷新)</div>
    <div id="recentList">
      <div class="empty">等待采集数据...</div>
    </div>
  </div>

  <!-- 采集日志 -->
  <div class="card">
    <div class="card-title">📜 采集日志</div>
    <div class="log-feed" id="logFeed">
      <div class="empty">等待采集事件...</div>
    </div>
  </div>

</div>

<div class="footer">
  🐉 龍魂系统 · 统一采集看板 · 数据主权归集本地 · UID9622
</div>

<div class="toast" id="toast"></div>

<script>
let toastTimer;
function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2500);
}

async function refreshAll() {
  try {
    // 采集统计
    const r1 = await fetch('/api/stats');
    const stats = await r1.json();
    document.getElementById('totalFiles').textContent = stats.total_files || 0;
    document.getElementById('totalSize').textContent = (stats.total_size_mb || 0) + ' MB';

    // 站点标签
    const sites = stats.sites || {};
    const siteTags = document.getElementById('siteTags');
    if (Object.keys(sites).length === 0) {
      siteTags.innerHTML = '<div class="empty">暂无采集数据 — 打开浏览器访问支持站点试试</div>';
    } else {
      siteTags.innerHTML = Object.entries(sites)
        .sort((a,b) => b[1] - a[1])
        .map(([name, count]) => `<span class="site-tag">${name}<span class="count">${count}</span></span>`)
        .join('');
    }

    // 日期趋势
    const dates = stats.dates || {};
    const dtDiv = document.getElementById('dateTrends');
    if (Object.keys(dates).length === 0) {
      dtDiv.innerHTML = '<div class="empty">暂无趋势数据</div>';
    } else {
      const maxVal = Math.max(...Object.values(dates), 1);
      dtDiv.innerHTML = Object.entries(dates).map(([d, c]) => {
        const pct = Math.round(c / maxVal * 100);
        return `<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
          <span style="font-size:11px;color:var(--muted);width:80px;">${d.slice(5)}</span>
          <div style="flex:1;height:18px;background:#1a1a3e;border-radius:4px;overflow:hidden;">
            <div style="height:100%;width:${pct}%;background:linear-gradient(90deg,var(--gold-dim),var(--gold));border-radius:4px;transition:width .5s;"></div>
          </div>
          <span style="font-size:12px;font-weight:700;width:30px;text-align:right;">${c}</span>
        </div>`;
      }).join('');
    }

    // 最近采集
    const recent = stats.recent || [];
    const recentDiv = document.getElementById('recentList');
    if (recent.length === 0) {
      recentDiv.innerHTML = '<div class="empty">等待采集数据...</div>';
    } else {
      recentDiv.innerHTML = recent.map(r => `
        <div class="recent-item">
          <span class="recent-site">${r.site || '?'}</span>
          <span class="recent-title" title="${r.title || ''}">${r.title || '无标题'}</span>
          <span class="recent-time">${(r.time || '').slice(11,19)}</span>
        </div>
      `).join('');
    }

    // 数据中台
    try {
      const r2 = await fetch('/api/hub/status');
      const hub = await r2.json();
      document.getElementById('hubFiles').textContent = hub.hub_files || 0;
    } catch(e) {}

  } catch(e) {
    console.error('刷新失败:', e);
  }
}

async function runHub() {
  toast('🚀 正在运行数据中台采集...');
  try {
    const r = await fetch('/api/hub/run', { method: 'POST' });
    const data = await r.json();
    if (data.code === 200) {
      toast('✅ 数据中台采集完成！');
    } else {
      toast('⚠️ ' + (data.message || '采集异常'));
    }
  } catch(e) {
    toast('❌ 采集失败: ' + e.message);
  }
  setTimeout(refreshAll, 2000);
}

// 初始加载 + 自动刷新
refreshAll();
setInterval(refreshAll, 5000);

// 键盘快捷键
document.addEventListener('keydown', e => {
  if (e.key === 'r' && e.ctrlKey) { e.preventDefault(); refreshAll(); }
  if (e.key === 'h' && e.ctrlKey) { e.preventDefault(); runHub(); }
});
</script>
</body>
</html>'''

# ==================== 启动 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("🐉 龍魂系统 · 统一采集服务 v3.0")
    print("UID9622 | 龍芯北辰 | 两线汇一")
    print(f"📁 数据目录: {DATA_DIR}")
    print(f"📊 看板:     http://localhost:9622/dashboard")
    print(f"📈 统计:     http://localhost:9622/api/stats")
    print(f"📡 中台:     http://localhost:9622/api/hub/run")
    print(f"📤 导出:     http://localhost:9622/export")
    print("=" * 60)
    
    app.run(host="127.0.0.1", port=9622, debug=False)
