#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙酉·癸亥·巳时·䷫姤-CNSH-WEB-IDE-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
🐉 CNSH Web IDE v1.0

基于 FastAPI + Ace Editor 的浏览器端 CNSH 集成开发环境。

功能：
  - 项目文件浏览器
  - 多标签代码编辑
  - CNSH 语法高亮
  - 一键纠错 / 编译 / 运行
  - 输出/日志面板

用法：
  python3 08_BIN/cnsh_web_ide.py
  python3 08_BIN/cnsh_web_ide.py --project /path/to/project
  python3 08_BIN/cnsh_web_ide.py --host 0.0.0.0 --port 8080
"""

import os
import sys
import json
import time
import argparse
import traceback
from collections import deque
from pathlib import Path
from typing import List, Dict, Optional

from fastapi import FastAPI, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# 让导入能找到同目录模块
sys.path.insert(0, str(Path(__file__).resolve().parent))

# 引擎分批导入，避免一个失败导致全部不可用
try:
    from cnsh_editor import CNSHEditor
    from cnsh_compiler import CNSHCompiler
    from cnsh_ui import CNSHInterpreterV2, CNSHAI
    HAS_ENGINES = True
except Exception as e:
    print(f"⚠️ 核心引擎导入失败: {e}", file=sys.stderr)
    HAS_ENGINES = False

try:
    from cnsh_ai_providers import get_router, make_cnsh_ai_callback
    from cnsh_bagua_router import BaguaRouter
    HAS_AI_ROUTER = True
except Exception as e:
    print(f"⚠️ AI 路由导入失败: {e}", file=sys.stderr)
    HAS_AI_ROUTER = False

try:
    from lh_agent_cosmos import Cosmos
    HAS_COSMOS = True
except Exception as e:
    print(f"⚠️ 智能体宇宙导入失败: {e}", file=sys.stderr)
    HAS_COSMOS = False

try:
    from cnsh_knowledge_hub import KnowledgeHub
    HAS_KNOWLEDGE_HUB = True
except Exception as e:
    print(f"⚠️ 知识库中枢导入失败: {e}", file=sys.stderr)
    HAS_KNOWLEDGE_HUB = False

try:
    from compliance_sandbox import ComplianceSandbox
    HAS_COMPLIANCE = True
except Exception as e:
    print(f"⚠️ 合规沙盒导入失败: {e}", file=sys.stderr)
    HAS_COMPLIANCE = False

try:
    from civilization_archive import CivilizationArchive
    HAS_CIV_ARCHIVE = True
except Exception as e:
    print(f"⚠️ 文明档案馆导入失败: {e}", file=sys.stderr)
    HAS_CIV_ARCHIVE = False


# ═══════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════
APP_NAME = "CNSH Web IDE"
APP_VERSION = "1.0.0"
DEFAULT_PROJECT = Path.home() / "longhun-system" / "cnsh_projects"

# ═══════════════════════════════════════════════════════
# AI 路由初始化
# ═══════════════════════════════════════════════════════
ai_router = None
bagua_router = None
if HAS_AI_ROUTER and HAS_ENGINES:
    try:
        ai_router = get_router()
        bagua_router = BaguaRouter(ai_router)
        CNSHAI.set_custom_ask(make_cnsh_ai_callback(ai_router))
        print(f"🧠 AI 路由已加载，默认厂商: {ai_router.get_default().get('name', '模拟')}")
        print(f"☯ 八卦/八门路由已加载")
    except Exception as e:
        print(f"⚠️ AI 路由初始化失败: {e}", file=sys.stderr)

# 知识库中枢初始化（独立，不依赖其他引擎）
knowledge_hub = None
if HAS_KNOWLEDGE_HUB:
    try:
        knowledge_hub = KnowledgeHub()
        print(f"🧠 知识库中枢已加载: {knowledge_hub.stats()['total_entries']} 条记忆")
    except Exception as e:
        print(f"⚠️ 知识库中枢初始化失败: {e}", file=sys.stderr)

# 国际合规沙盒初始化
compliance_sandbox = None
if HAS_COMPLIANCE:
    try:
        compliance_sandbox = ComplianceSandbox(mode="sandbox")
        print(f"🛡️ 国际合规沙盒已加载（{len(compliance_sandbox.check(''))} 个法域）")
    except Exception as e:
        print(f"⚠️ 合规沙盒初始化失败: {e}", file=sys.stderr)

# DNA 文明档案馆初始化
civ_archive = None
if HAS_CIV_ARCHIVE:
    try:
        civ_archive = CivilizationArchive()
        print(f"📜 DNA 文明档案馆已加载: {civ_archive.stats()['total']} 条记录")
    except Exception as e:
        print(f"⚠️ 文明档案馆初始化失败: {e}", file=sys.stderr)

DEMO_PROJECT = '''@任务 欢迎

# 设变量
设 名字 = "龍魂"
设 版本 = 1.0

打印 名字
打印 版本

# 条件
如果 版本 >= 1.0
    打印 "正式版"
结束

# AI 理解（模拟）
理解 "把 CNSH 编译成 Python"
记录 AI结果

打印 AI结果

@任务 结束
'''


# ═══════════════════════════════════════════════════════
# 应用
# ═══════════════════════════════════════════════════════
app = FastAPI(title=APP_NAME, version=APP_VERSION)

# ═══════════════════════════════════════════════════════
# API 限流中间件（Phase D：外网 API 加固）
# ═══════════════════════════════════════════════════════
class RateLimiter:
    """基于滑动窗口的内存限流器：按 client_ip + path 计数"""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        # key -> deque[timestamp]
        self.windows: Dict[str, deque] = {}

    def is_allowed(self, key: str) -> bool:
        now = time.time()
        window = self.windows.get(key)
        if window is None:
            window = deque()
            self.windows[key] = window

        # 清理过期时间戳
        cutoff = now - self.window_seconds
        while window and window[0] < cutoff:
            window.popleft()

        if len(window) >= self.max_requests:
            return False

        window.append(now)
        return True

    def get_remaining(self, key: str) -> int:
        now = time.time()
        window = self.windows.get(key, deque())
        cutoff = now - self.window_seconds
        while window and window[0] < cutoff:
            window.popleft()
        return max(0, self.max_requests - len(window))


rate_limiter: Optional[RateLimiter] = None


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """对 /api/* 路径应用限流"""
    if rate_limiter is None or not request.url.path.startswith("/api/"):
        return await call_next(request)

    # 优先取 X-Forwarded-For 第一个 IP（经过 nginx 反代时）
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else "unknown"

    key = f"{client_ip}:{request.url.path}"

    if not rate_limiter.is_allowed(key):
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "error": "请求过于频繁，请稍后再试",
                "retry_after": rate_limiter.window_seconds,
                "limit": rate_limiter.max_requests,
                "window": rate_limiter.window_seconds,
                "dna": "#龍芯⚡️RATE-LIMIT-UID9622"
            },
            headers={"Retry-After": str(rate_limiter.window_seconds)}
        )

    response = await call_next(request)
    # 在响应头中加上限流信息
    remaining = rate_limiter.get_remaining(key)
    response.headers["X-RateLimit-Limit"] = str(rate_limiter.max_requests)
    response.headers["X-RateLimit-Window"] = str(rate_limiter.window_seconds)
    response.headers["X-RateLimit-Remaining"] = str(remaining)
    return response


# 静态资源目录（Ace Editor 等本地资源）
# 开发时从项目根目录 static/ 加载；PyInstaller 打包后从 sys._MEIPASS/static/ 加载
def _resolve_static_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)) / "static"
    return Path(__file__).resolve().parent.parent / "static"

STATIC_DIR = _resolve_static_dir()
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
else:
    print(f"⚠️ 静态资源目录不存在: {STATIC_DIR}", file=sys.stderr)

project_dir: Path = DEFAULT_PROJECT


# ═══════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════
def ensure_demo_project(path: Path):
    demo_file = path / "demo" / "welcome.cnsh"
    if not demo_file.exists():
        demo_file.parent.mkdir(parents=True, exist_ok=True)
        demo_file.write_text(DEMO_PROJECT, encoding="utf-8")


def list_files(path: Path) -> List[Dict]:
    """递归列出项目文件"""
    items = []
    try:
        for child in sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name)):
            if child.name.startswith("."):
                continue
            if child.name in ("__pycache__", "venv", ".venv"):
                continue
            rel = child.relative_to(path)
            item = {
                "name": child.name,
                "path": str(rel),
                "type": "file" if child.is_file() else "dir",
            }
            if child.is_dir():
                item["children"] = list_files(child)
            items.append(item)
    except PermissionError:
        pass
    return items


def safe_path(rel_path: str) -> Optional[Path]:
    """把相对路径解析为项目内的绝对路径，防止目录遍历"""
    target = (project_dir / rel_path).resolve()
    try:
        target.relative_to(project_dir.resolve())
        return target
    except ValueError:
        return None


# ═══════════════════════════════════════════════════════
# HTML 前端
# ═══════════════════════════════════════════════════════
INDEX_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐉 CNSH Web IDE</title>
    <script src="static/ace/ace.min.js"></script>
    <script src="static/ace/mode-python.min.js"></script>
    <script src="static/ace/theme-monokai.min.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #1e1e1e;
            color: #d4d4d4;
            height: 100vh;
            overflow: hidden;
        }
        .container { display: flex; flex-direction: column; height: 100vh; }
        .toolbar {
            background: #333333;
            padding: 8px 12px;
            display: flex;
            gap: 8px;
            align-items: center;
            border-bottom: 1px solid #444;
        }
        .toolbar button {
            background: #0e639c;
            color: white;
            border: none;
            padding: 6px 14px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
        }
        .toolbar button:hover { background: #1177bb; }
        .toolbar button.secondary { background: #444444; }
        .toolbar button.secondary:hover { background: #555555; }
        .main { display: flex; flex: 1; overflow: hidden; }
        .sidebar {
            width: 240px;
            background: #252526;
            border-right: 1px solid #333;
            overflow-y: auto;
            padding: 10px;
        }
        .sidebar h3 { font-size: 12px; color: #bbbbbb; margin-bottom: 8px; text-transform: uppercase; }
        .file-tree ul { list-style: none; }
        .file-tree li {
            padding: 4px 6px;
            cursor: pointer;
            border-radius: 3px;
            font-size: 13px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .file-tree li:hover { background: #37373d; }
        .file-tree li.dir { color: #75beff; font-weight: bold; }
        .file-tree li.file { color: #cccccc; padding-left: 16px; }
        .editor-area { flex: 1; display: flex; flex-direction: column; min-width: 0; }
        .tabs {
            background: #2d2d30;
            display: flex;
            border-bottom: 1px solid #333;
            overflow-x: auto;
        }
        .tab {
            padding: 8px 16px;
            cursor: pointer;
            font-size: 13px;
            border-right: 1px solid #333;
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
        }
        .tab.active { background: #1e1e1e; border-bottom: 2px solid #0e639c; }
        .tab:hover { background: #3c3c3c; }
        .tab .close { font-size: 16px; color: #888; }
        .tab .close:hover { color: #fff; }
        #editor { flex: 1; }
        .panels {
            height: 200px;
            background: #1e1e1e;
            border-top: 1px solid #333;
            display: flex;
            flex-direction: column;
        }
        .panel-tabs {
            display: flex;
            background: #2d2d30;
        }
        .panel-tab {
            padding: 6px 14px;
            cursor: pointer;
            font-size: 12px;
            color: #969696;
        }
        .panel-tab.active { color: #fff; background: #1e1e1e; }
        .panel-content {
            flex: 1;
            overflow: auto;
            padding: 10px;
            font-family: "Courier New", monospace;
            font-size: 12px;
            white-space: pre-wrap;
        }
        .statusbar {
            background: #007acc;
            color: white;
            padding: 4px 12px;
            font-size: 12px;
        }
        .hidden { display: none !important; }
    </style>
</head>
<body>
    <div class="container">
        <div class="toolbar">
            <button onclick="newFile()">🆕 新建</button>
            <button onclick="saveFile()">💾 保存</button>
            <button onclick="correctCode()">✨ 纠错</button>
            <button onclick="compileCode()">🔨 编译</button>
            <button onclick="runCode()">▶ 运行</button>
            <button class="secondary" onclick="loadDemo()">📂 加载示例</button>
            <span style="margin-left:auto; color:#aaa; font-size:12px;">🐉 CNSH Web IDE v1.0</span>
        </div>
        <div class="main">
            <div class="sidebar">
                <h3>📁 项目文件</h3>
                <div class="file-tree" id="fileTree"></div>
            </div>
            <div class="editor-area">
                <div class="tabs" id="tabs"></div>
                <div id="editor"></div>
                <div class="panels">
                    <div class="panel-tabs">
                        <div class="panel-tab active" onclick="switchPanel('output')">输出</div>
                        <div class="panel-tab" onclick="switchPanel('compile')">编译结果</div>
                        <div class="panel-tab" onclick="switchPanel('log')">日志</div>
                    </div>
                    <div class="panel-content" id="outputPanel"></div>
                    <div class="panel-content hidden" id="compilePanel"></div>
                    <div class="panel-content hidden" id="logPanel"></div>
                </div>
            </div>
        </div>
        <div class="statusbar" id="statusbar">就绪</div>
    </div>

    <script>
        let editor;
        let tabs = [];
        let activeTab = null;
        let currentFiles = [];

        function init() {
            editor = ace.edit("editor");
            editor.setTheme("ace/theme/monokai");
            editor.session.setMode("ace/mode/python");
            editor.setOptions({
                fontSize: 14,
                showPrintMargin: false,
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true
            });
            editor.on("input", () => {
                if (activeTab) {
                    activeTab.content = editor.getValue();
                    activeTab.modified = true;
                    updateTabLabel(activeTab);
                }
            });
            loadFileTree();
            newFile("welcome.cnsh", `""" + DEMO_PROJECT.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + """`);
        }

        function loadFileTree() {
            fetch('api/files')
                .then(r => r.json())
                .then(data => {
                    currentFiles = data.files;
                    document.getElementById('fileTree').innerHTML = renderTree(data.files);
                });
        }

        function renderTree(items) {
            if (!items || items.length === 0) return '';
            let html = '<ul>';
            for (const item of items) {
                if (item.type === 'dir') {
                    html += `<li class="dir">📁 ${item.name}</li>`;
                    html += renderTree(item.children);
                } else {
                    html += `<li class="file" onclick="openFile('${item.path}')">📄 ${item.name}</li>`;
                }
            }
            html += '</ul>';
            return html;
        }

        function newFile(name, content) {
            name = name || 'untitled.cnsh';
            content = content || '';
            const tab = { id: Date.now(), name, path: null, content, modified: false };
            tabs.push(tab);
            setActiveTab(tab);
        }

        function setActiveTab(tab) {
            activeTab = tab;
            editor.setValue(tab.content, -1);
            renderTabs();
        }

        function renderTabs() {
            const container = document.getElementById('tabs');
            container.innerHTML = tabs.map(tab => `
                <div class="tab ${tab === activeTab ? 'active' : ''}" onclick="setActiveTab(tabs.find(t => t.id === ${tab.id}))">
                    ${tab.modified ? '● ' : ''}${tab.name}
                    <span class="close" onclick="closeTab(event, ${tab.id})">×</span>
                </div>
            `).join('');
        }

        function updateTabLabel(tab) {
            renderTabs();
        }

        function closeTab(event, id) {
            event.stopPropagation();
            const idx = tabs.findIndex(t => t.id === id);
            if (idx === -1) return;
            const tab = tabs[idx];
            if (tab.modified && !confirm('文件未保存，确认关闭？')) return;
            tabs.splice(idx, 1);
            if (activeTab.id === id) {
                activeTab = tabs.length > 0 ? tabs[Math.min(idx, tabs.length - 1)] : null;
            }
            if (activeTab) {
                editor.setValue(activeTab.content, -1);
            } else {
                editor.setValue('', -1);
            }
            renderTabs();
        }

        function openFile(path) {
            fetch('api/file?path=' + encodeURIComponent(path))
                .then(r => r.json())
                .then(data => {
                    const existing = tabs.find(t => t.path === path);
                    if (existing) {
                        setActiveTab(existing);
                        return;
                    }
                    const tab = { id: Date.now(), name: path.split('/').pop(), path, content: data.content, modified: false };
                    tabs.push(tab);
                    setActiveTab(tab);
                });
        }

        function saveFile() {
            if (!activeTab) return;
            const path = activeTab.path || prompt('保存路径 (相对项目根目录):', activeTab.name);
            if (!path) return;
            fetch('api/file', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path, content: editor.getValue() })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    activeTab.path = path;
                    activeTab.name = path.split('/').pop();
                    activeTab.modified = false;
                    updateTabLabel(activeTab);
                    loadFileTree();
                    setStatus('已保存: ' + path);
                } else {
                    setStatus('保存失败: ' + data.error);
                }
            });
        }

        function correctCode() {
            if (!activeTab) return;
            setStatus('纠错中...');
            fetch('api/correct', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: editor.getValue() })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    editor.setValue(data.corrected, -1);
                    activeTab.content = data.corrected;
                    activeTab.modified = true;
                    updateTabLabel(activeTab);
                    showOutput('output', `✅ 纠错完成\\n应用规则: ${data.rules_count} 条\\n警告: ${data.warnings_count} 条\\n\\n${data.warnings.join('\\n')}`);
                } else {
                    showOutput('output', '❌ 纠错失败: ' + data.error);
                }
                setStatus('纠错完成');
            });
        }

        function compileCode() {
            if (!activeTab) return;
            setStatus('编译中...');
            fetch('api/compile', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: editor.getValue(), filename: activeTab.name })
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    showOutput('compile', '✅ 编译成功\\n\\n' + data.python_code);
                } else {
                    showOutput('compile', '❌ 编译失败\\n\\n' + data.errors.join('\\n'));
                }
                setStatus(data.success ? '编译成功' : '编译失败');
            });
        }

        function runCode() {
            if (!activeTab) return;
            setStatus('运行中...');
            showOutput('output', '▶ 运行中...');
            fetch('api/run', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: editor.getValue() })
            })
            .then(r => r.json())
            .then(data => {
                showOutput('output', data.output);
                showOutput('log', data.logs.join('\\n'));
                setStatus('运行完成: ' + data.logs.length + ' 条日志');
            });
        }

        function loadDemo() {
            newFile('welcome.cnsh', `""" + DEMO_PROJECT.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n') + """`);
        }

        function switchPanel(name) {
            document.querySelectorAll('.panel-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.panel-tab').forEach(el => el.classList.remove('active'));
            document.getElementById(name + 'Panel').classList.remove('hidden');
            event.target.classList.add('active');
        }

        function showOutput(panel, text) {
            switchPanel(panel);
            document.getElementById(panel + 'Panel').textContent = text;
        }

        function setStatus(text) {
            document.getElementById('statusbar').textContent = text;
        }

        window.addEventListener('beforeunload', (e) => {
            if (tabs.some(t => t.modified)) {
                e.preventDefault();
                e.returnValue = '';
            }
        });

        init();
    </script>
</body>
</html>
"""


# ═══════════════════════════════════════════════════════
# API 路由
# ═══════════════════════════════════════════════════════
@app.get("/", response_class=HTMLResponse)
def index():
    return INDEX_HTML


@app.get("/api/files")
def api_files():
    return {"files": list_files(project_dir)}


@app.get("/api/file")
def api_get_file(path: str = Query(...)):
    target = safe_path(path)
    if not target or not target.is_file():
        return JSONResponse({"error": "文件不存在或路径非法"}, status_code=400)
    try:
        return {"content": target.read_text(encoding="utf-8")}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/file")
async def api_save_file(request: Request):
    data = await request.json()
    path = data.get("path", "")
    content = data.get("content", "")
    target = safe_path(path)
    if not target:
        return JSONResponse({"success": False, "error": "非法路径"}, status_code=400)
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"success": True}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/correct")
async def api_correct(request: Request):
    if not HAS_ENGINES:
        return JSONResponse({"success": False, "error": "纠错引擎未加载"}, status_code=500)
    data = await request.json()
    content = data.get("content", "")
    try:
        engine = CNSHEditor()
        corrected, rules, warnings = engine.correct(content)
        return {
            "success": True,
            "corrected": corrected,
            "rules_count": len(rules),
            "warnings_count": len(warnings),
            "warnings": warnings,
        }
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/compile")
async def api_compile(request: Request):
    if not HAS_ENGINES:
        return JSONResponse({"success": False, "error": "编译器未加载"}, status_code=500)
    data = await request.json()
    content = data.get("content", "")
    filename = data.get("filename", "untitled.cnsh")
    try:
        compiler = CNSHCompiler()
        result = compiler.compile(content, filename)
        return {
            "success": result.get("success", False),
            "python_code": result.get("python_code", ""),
            "errors": result.get("errors", []),
        }
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/run")
async def api_run(request: Request):
    if not HAS_ENGINES:
        return JSONResponse({"success": False, "error": "执行引擎未加载"}, status_code=500)
    data = await request.json()
    content = data.get("content", "")
    try:
        output, logs = CNSHInterpreterV2.run_script(content, use_real_ai=False)
        return {"success": True, "output": output, "logs": logs}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e), "output": "", "logs": []}, status_code=500)


# ═══════════════════════════════════════════════════════
# AI 厂商路由接口
# ═══════════════════════════════════════════════════════

@app.get("/api/ai/providers")
async def api_ai_providers():
    """列出已支持的 AI 厂商及本地配置状态（API Key 已脱敏）"""
    if ai_router is None:
        return JSONResponse({"success": False, "error": "AI 路由未加载"}, status_code=500)
    return {
        "success": True,
        "default": ai_router.get_default(),
        "providers": ai_router.list_providers(),
        "config_path": str(ai_router.config_path),
    }


@app.post("/api/ai/chat")
async def api_ai_chat(request: Request):
    """单轮 AI 对话测试接口（支持八卦/八门路由与热重载）"""
    if ai_router is None:
        return JSONResponse({"success": False, "error": "AI 路由未加载"}, status_code=500)
    data = await request.json()
    prompt = data.get("prompt", "")
    provider = data.get("provider", None)
    system = data.get("system", None)
    use_bagua = data.get("use_bagua", True)
    if not prompt:
        return JSONResponse({"success": False, "error": "prompt 不能为空"}, status_code=400)
    try:
        # 每次对话前热重载配置，实现零重启切换 key/厂商
        ai_router.reload()

        if use_bagua and bagua_router is not None:
            decision = bagua_router.decide(prompt, preferred_provider=provider)
            if decision.blocked:
                return {
                    "success": True,
                    "answer": f"{decision.gate_info['emoji']} {decision.gate}·熔断\n{decision.reason}\n建议：人工复核后再决定。",
                    "provider": "",
                    "route": decision.to_dict(),
                    "blocked": True,
                }
            answer = ai_router.ask(prompt, provider_key=decision.provider, system=system)
            return {
                "success": True,
                "answer": answer,
                "provider": decision.provider,
                "route": decision.to_dict(),
                "blocked": False,
            }

        answer = ai_router.ask(prompt, provider_key=provider, system=system)
        return {"success": True, "answer": answer, "provider": provider or ai_router.default_key}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/ai/route")
async def api_ai_route(request: Request):
    """八卦/八门路由决策接口（只决策，不调用 AI）"""
    if bagua_router is None:
        return JSONResponse({"success": False, "error": "八卦路由未加载"}, status_code=500)
    data = await request.json()
    prompt = data.get("prompt", "")
    provider = data.get("provider", None)
    if not prompt:
        return JSONResponse({"success": False, "error": "prompt 不能为空"}, status_code=400)
    try:
        decision = bagua_router.decide(prompt, preferred_provider=provider)
        return {"success": True, "route": decision.to_dict()}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.get("/api/bagua/status")
async def api_bagua_status():
    """当前八卦态势（用于前端展示）"""
    if bagua_router is None:
        return JSONResponse({"success": False, "error": "八卦路由未加载"}, status_code=500)
    try:
        decision = bagua_router.decide("查询当前八卦态势")
        return {
            "success": True,
            "score": decision.bagua_score,
            "gua": decision.bagua_gua,
            "default_provider": ai_router.get_default() if ai_router else {},
        }
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/cosmos/run")
async def api_cosmos_run(request: Request):
    """触发一次龍魂智能体宇宙自治运行（本地、零 API 费用）"""
    if not HAS_COSMOS:
        return JSONResponse({"success": False, "error": "智能体宇宙未加载"}, status_code=500)
    try:
        data = await request.json()
    except Exception:
        data = {}
    topic = data.get("topic", "CNSH IDE 任务")
    steps = min(int(data.get("steps", 3)), 10)
    try:
        cosmos = Cosmos(offline=True)
        report = cosmos.run(steps=steps, topic=topic, max_generation=2)
        return {"success": True, "report": report.to_dict()}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/memory/store")
async def api_memory_store(request: Request):
    """存储一条记忆到知识库中枢（带 DNA 追溯）"""
    if knowledge_hub is None:
        return JSONResponse({"success": False, "error": "知识库未加载"}, status_code=500)
    try:
        data = await request.json()
    except Exception:
        data = {}
    content = data.get("content", "")
    if not content:
        return JSONResponse({"success": False, "error": "content 不能为空"}, status_code=400)
    try:
        entry = knowledge_hub.store(
            content=content,
            category=data.get("category", "general"),
            tags=data.get("tags", []),
            source=data.get("source", "api"),
            dna=data.get("dna"),
            metadata=data.get("metadata", {}),
        )
        return {
            "success": True,
            "entry_id": entry.entry_id,
            "dna": entry.dna,
            "content_hash": entry.content_hash,
            "created_at": entry.created_at,
            "bcm_fingerprint": entry.bcm_fingerprint,
        }
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/memory/retrieve")
async def api_memory_retrieve(request: Request):
    """按 entry_id 或 dna 检索单条记忆"""
    if knowledge_hub is None:
        return JSONResponse({"success": False, "error": "知识库未加载"}, status_code=500)
    try:
        data = await request.json()
    except Exception:
        data = {}
    entry = knowledge_hub.retrieve(
        entry_id=data.get("entry_id"),
        dna=data.get("dna"),
    )
    if entry is None:
        return JSONResponse({"success": False, "error": "未找到记忆"}, status_code=404)
    return {
        "success": True,
        "entry": {
            "entry_id": entry.entry_id,
            "dna": entry.dna,
            "content": entry.content,
            "category": entry.category,
            "tags": entry.tags,
            "source": entry.source,
            "created_at": entry.created_at,
            "bcm_fingerprint": entry.bcm_fingerprint,
        },
    }


@app.post("/api/memory/search")
async def api_memory_search(request: Request):
    """全文 + 语义混合检索知识库"""
    if knowledge_hub is None:
        return JSONResponse({"success": False, "error": "知识库未加载"}, status_code=500)
    try:
        data = await request.json()
    except Exception:
        data = {}
    query = data.get("query", "")
    if not query:
        return JSONResponse({"success": False, "error": "query 不能为空"}, status_code=400)
    try:
        results = knowledge_hub.search(
            query=query,
            top_k=min(int(data.get("top_k", 5)), 20),
            category=data.get("category"),
        )
        return {"success": True, "query": query, "results": results}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.get("/api/memory/stats")
async def api_memory_stats():
    """知识库统计"""
    if knowledge_hub is None:
        return JSONResponse({"success": False, "error": "知识库未加载"}, status_code=500)
    try:
        return {"success": True, "stats": knowledge_hub.stats()}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.get("/api/ai/config")
async def api_ai_config_get():
    """读取当前 AI 配置文件内容（返回模板或已保存内容）"""
    if ai_router is None:
        return JSONResponse({"success": False, "error": "AI 路由未加载"}, status_code=500)
    path = ai_router.config_path
    if path.exists():
        try:
            content = path.read_text(encoding="utf-8")
            return {"success": True, "exists": True, "path": str(path), "content": content}
        except Exception as e:
            return JSONResponse({"success": False, "error": str(e)}, status_code=500)
    template = {
        "default": "local",
        "providers": {
            "local": {"api_key": "", "model": "longhun-v43:latest", "enabled": True},
            "kimi": {"api_key": "", "model": "moonshot-v1-8k", "enabled": False},
            "tongyi": {"api_key": "", "model": "qwen-turbo", "enabled": False},
            "deepseek": {"api_key": "", "model": "deepseek-chat", "enabled": False},
            "zhipu": {"api_key": "", "model": "glm-4", "enabled": False},
            "doubao": {"api_key": "", "model": "doubao-lite-4k", "enabled": False},
        },
    }
    return {"success": True, "exists": False, "path": str(path), "content": json.dumps(template, ensure_ascii=False, indent=2)}


@app.post("/api/ai/config")
async def api_ai_config_save(request: Request):
    """保存 AI 配置文件到用户本地目录"""
    if ai_router is None:
        return JSONResponse({"success": False, "error": "AI 路由未加载"}, status_code=500)
    data = await request.json()
    content = data.get("content", "")
    try:
        config_obj = json.loads(content)
    except json.JSONDecodeError as e:
        return JSONResponse({"success": False, "error": f"JSON 格式错误: {e}"}, status_code=400)
    if not isinstance(config_obj, dict):
        return JSONResponse({"success": False, "error": "配置必须是 JSON 对象"}, status_code=400)
    if ai_router.save_config(config_obj):
        return {"success": True, "path": str(ai_router.config_path)}
    else:
        return JSONResponse({"success": False, "error": "保存失败"}, status_code=500)


# ═══════════════════════════════════════════════════════════════════════
# 国际合规沙盒 API
# ═══════════════════════════════════════════════════════════════════════
@app.post("/api/compliance/check")
async def api_compliance_check(request: Request):
    """合规审查：{content, regions?, mode?}"""
    if compliance_sandbox is None:
        return JSONResponse({"success": False, "error": "合规沙盒未加载"}, status_code=500)
    try:
        data = await request.json()
        content = data.get("content", "")
        regions = data.get("regions")
        mode = data.get("mode", "sandbox")
        sb = ComplianceSandbox(mode=mode)
        return {"success": True, "report": sb.generate_report(content, regions)}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.get("/api/compliance/regions")
async def api_compliance_regions():
    """列出支持的法域"""
    if compliance_sandbox is None:
        return JSONResponse({"success": False, "error": "合规沙盒未加载"}, status_code=500)
    try:
        from compliance_sandbox import COMPLIANCE_RULES
        return {
            "success": True,
            "regions": [
                {"code": k, "name": v["name"], "laws": v["laws"], "severity": v["severity"]}
                for k, v in COMPLIANCE_RULES.items()
            ]
        }
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ═══════════════════════════════════════════════════════════════════════
# DNA 文明档案馆 API
# ═══════════════════════════════════════════════════════════════════════
@app.post("/api/civilization/store")
async def api_civ_store(request: Request):
    """存储文明记录"""
    if civ_archive is None:
        return JSONResponse({"success": False, "error": "文明档案馆未加载"}, status_code=500)
    try:
        data = await request.json()
        rec = civ_archive.store(
            title=data.get("title", ""),
            content=data.get("content", ""),
            civilization=data.get("civilization", "CN"),
            category=data.get("category", "text"),
            tags=data.get("tags", []),
            lang=data.get("lang", "zh"),
            source=data.get("source", "api"),
            media_hashes=data.get("media_hashes", {}),
            metadata=data.get("metadata", {})
        )
        return {"success": True, "record": rec.__dict__}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.post("/api/civilization/search")
async def api_civ_search(request: Request):
    """搜索文明记录"""
    if civ_archive is None:
        return JSONResponse({"success": False, "error": "文明档案馆未加载"}, status_code=500)
    try:
        data = await request.json()
        results = civ_archive.search(
            data.get("query", ""),
            data.get("civilization"),
            data.get("top_k", 10)
        )
        return {"success": True, "results": results}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.get("/api/civilization/verify")
async def api_civ_verify():
    """验证文明档案馆哈希链"""
    if civ_archive is None:
        return JSONResponse({"success": False, "error": "文明档案馆未加载"}, status_code=500)
    try:
        return {"success": True, "verify": civ_archive.verify_chain()}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


@app.get("/api/civilization/stats")
async def api_civ_stats():
    """文明档案馆统计"""
    if civ_archive is None:
        return JSONResponse({"success": False, "error": "文明档案馆未加载"}, status_code=500)
    try:
        return {"success": True, "stats": civ_archive.stats()}
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


# ═══════════════════════════════════════════════════════════════════════
# 启动
# ═══════════════════════════════════════════════════════════════════════
def main():
    global project_dir, rate_limiter

    parser = argparse.ArgumentParser(description="🐉 CNSH Web IDE")
    parser.add_argument("--project", default=str(DEFAULT_PROJECT),
                        help=f"项目目录 (默认: {DEFAULT_PROJECT})")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8848, help="监听端口")
    parser.add_argument("--rate-limit", type=int, default=100,
                        help="每窗口每个 IP 对单个 API 端点的最大请求数 (默认 100)")
    parser.add_argument("--rate-window", type=int, default=60,
                        help="限流窗口秒数 (默认 60)")
    parser.add_argument("--no-rate-limit", action="store_true", help="关闭 API 限流")
    args = parser.parse_args()

    # 初始化限流器
    if not args.no_rate_limit:
        rate_limiter = RateLimiter(max_requests=args.rate_limit, window_seconds=args.rate_window)
        print(f"🛡️ API 限流已启用: {args.rate_limit} 请求 / {args.rate_window} 秒 / IP / 端点")
    else:
        print("⚠️ API 限流已关闭")

    project_dir = Path(args.project).resolve()
    project_dir.mkdir(parents=True, exist_ok=True)
    ensure_demo_project(project_dir)

    print(f"🐉 CNSH Web IDE 启动")
    print(f"   项目: {project_dir}")
    print(f"   访问: http://{args.host}:{args.port}")
    print(f"   按 Ctrl+C 停止")

    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
