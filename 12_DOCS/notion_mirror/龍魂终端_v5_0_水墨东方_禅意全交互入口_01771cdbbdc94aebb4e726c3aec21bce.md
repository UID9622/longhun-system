# 🎨 龍魂终端 v5.0｜水墨东方·禅意全交互入口

> Notion URL: https://app.notion.com/p/v5-0-01771cdbbdc94aebb4e726c3aec21bce
> Created: 2026-03-15T21:16:00.000Z
> Last edited: 2026-07-01T15:10:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
## 🎨 龍魂终端 v5.0｜水墨东方·禅意全交互入口
---
## 🌟 v5.0 十五大创意交互升级（vs v2.0）
---
## 📋 完整HTML代码（复制即用）
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐉 龍魂终端 v5.0 | 水墨东方·禅意全交互</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=ZCOOL+KuaiLe&display=swap');
        * { margin:0; padding:0; box-sizing:border-box; }

        :root {
            --bg: #f5f0e8; --sidebar: #ede6d6; --card: #faf7f0;
            --border: rgba(120,100,60,0.15); --text: #2c2416;
            --sub: #8a7e6a; --accent: #8b4513; --accent2: #c0392b;
            --ink: #1a1a2e; --gold: #d4a017; --jade: #2e8b57;
            --water: #4a7c8c; --fire: #c0392b; --earth: #8b7355;
            --wood: #2e8b57; --metal: #b8a88a;
            --font-serif: 'Noto Serif SC', 'STKaiti', 'KaiTi', serif;
            --font-fun: 'ZCOOL KuaiLe', cursive;
        }

        .theme-water { --bg:#e8eff5; --sidebar:#dae6ed; --card:#f0f5fa; --accent:#2c5f7c; --border:rgba(60,100,140,0.15); }
        .theme-fire  { --bg:#f5e8e8; --sidebar:#edd6d6; --card:#faf0f0; --accent:#8b1a1a; --border:rgba(140,60,60,0.15); }
        .theme-wood  { --bg:#e8f5ea; --sidebar:#d6edda; --card:#f0faf2; --accent:#2e6b3e; --border:rgba(60,140,80,0.15); }
        .theme-metal { --bg:#f0ede8; --sidebar:#e6e2d6; --card:#f7f5f0; --accent:#6b5e4a; --border:rgba(100,90,60,0.15); }
        .theme-night { --bg:#1a1a2e; --sidebar:#16213e; --card:#1f2937; --text:#e8dcc8; --sub:#8a8a6a; --accent:#d4a017; --border:rgba(200,180,100,0.12); }

        body {
            font-family: var(--font-serif);
            background: var(--bg); color: var(--text);
            height:100vh; display:flex; overflow:hidden;
            transition: all 0.8s ease;
        }

        /* --- 水墨Canvas背景 --- */
        #inkCanvas { position:fixed; top:0; left:0; width:100%; height:100%; z-index:0; opacity:0.3; pointer-events:none; }

        /* --- 烟雨粒子 --- */
        #rainCanvas { position:fixed; top:0; left:0; width:100%; height:100%; z-index:1; pointer-events:none; }

        /* --- 侧边栏 --- */
        .sidebar {
            width:260px; background:var(--sidebar); border-right:1px solid var(--border);
            padding:20px 0; display:flex; flex-direction:column; z-index:10;
            position:relative;
        }
        .sidebar-logo {
            padding:0 20px 20px; border-bottom:1px solid var(--border); margin-bottom:12px;
            text-align:center;
        }
        /* 太极Logo */
        .taiji {
            width:60px; height:60px; margin:0 auto 10px;
            border-radius:50%; position:relative; cursor:pointer;
            animation: taiji-spin 20s linear infinite;
            background: linear-gradient(to right, var(--ink) 50%, var(--card) 50%);
            border:2px solid var(--border);
        }
        .taiji::before, .taiji::after {
            content:''; position:absolute; width:30px; height:30px; border-radius:50%;
        }
        .taiji::before { top:0; left:15px; background:var(--card); }
        .taiji::after  { bottom:0; left:15px; background:var(--ink); }
        .taiji .dot-w, .taiji .dot-b {
            position:absolute; width:10px; height:10px; border-radius:50%; z-index:2;
        }
        .taiji .dot-w { top:10px; left:25px; background:var(--ink); }
        .taiji .dot-b { bottom:10px; left:25px; background:var(--card); }
        @keyframes taiji-spin { to { transform:rotate(360deg); } }
        .taiji:hover { animation-duration:3s; }

        .sidebar-logo h1 { font-size:18px; font-weight:700; letter-spacing:4px; color:var(--accent); }
        .sidebar-logo p  { font-size:11px; color:var(--sub); margin-top:2px; letter-spacing:2px; }

        .nav-section { flex:1; padding:4px 8px; overflow-y:auto; }
        .nav-label {
            font-size:10px; font-weight:600; color:var(--sub);
            letter-spacing:3px; padding:12px 12px 4px;
        }
        .nav-item {
            display:flex; align-items:center; gap:10px;
            padding:10px 14px; border-radius:8px; cursor:pointer;
            font-size:14px; margin-bottom:2px; transition:all 0.3s;
            border-left:3px solid transparent;
        }
        .nav-item:hover { background:var(--border); border-left-color:var(--accent); }
        .nav-item.active { background:rgba(139,69,19,0.1); color:var(--accent); border-left-color:var(--accent); font-weight:600; }

        /* 卦象状态 */
        .gua-status { margin-left:auto; font-size:12px; font-weight:700; }
        .gua-status.on  { color:var(--jade); }
        .gua-status.off { color:var(--fire); }

        /* --- 主区域 --- */
        .main { flex:1; display:flex; flex-direction:column; z-index:10; position:relative; }

        .status-bar {
            padding:8px 20px; background:var(--sidebar); font-size:11px;
            color:var(--sub); border-bottom:1px solid var(--border);
            display:flex; gap:16px; letter-spacing:1px;
        }

        .topbar {
            height:52px; background:var(--card); border-bottom:1px solid var(--border);
            display:flex; align-items:center; padding:0 20px; gap:12px;
        }
        .topbar-title { font-size:16px; font-weight:600; flex:1; letter-spacing:2px; }
        .topbar-btn {
            padding:6px 16px; border-radius:6px; border:1px solid var(--border);
            background:var(--card); color:var(--text); font-size:13px;
            cursor:pointer; font-family:var(--font-serif); transition:all 0.3s;
        }
        .topbar-btn:hover { background:var(--accent); color:#fff; }

        .panel { display:none; flex:1; flex-direction:column; overflow:hidden; }
        .panel.active { display:flex; animation: scroll-open 0.5s ease; }
        @keyframes scroll-open {
            from { opacity:0; transform:translateY(20px); }
            to   { opacity:1; transform:translateY(0); }
        }

        .content-area { flex:1; padding:24px; overflow-y:auto; }

        .card {
            background:var(--card); border-radius:12px; padding:24px;
            border:1px solid var(--border); margin-bottom:20px;
            box-shadow:0 2px 12px rgba(0,0,0,0.04);
            position:relative; overflow:hidden;
        }
        .card::before {
            content:''; position:absolute; top:0; left:0; width:4px; height:100%;
            background: linear-gradient(to bottom, var(--accent), transparent);
        }
        .card-title {
            font-size:18px; font-weight:700; margin-bottom:16px;
            letter-spacing:2px; color:var(--accent);
        }

        textarea {
            width:100%; min-height:120px; padding:14px; border:1px solid var(--border);
            border-radius:8px; background:var(--bg); color:var(--text);
            font-size:15px; font-family:var(--font-serif);
            resize:vertical; letter-spacing:1px; line-height:1.8;
            transition: border-color 0.3s;
        }
        textarea:focus { outline:none; border-color:var(--accent); box-shadow:0 0 0 3px rgba(139,69,19,0.1); }

        button.primary {
            background: linear-gradient(135deg, var(--accent), var(--gold));
            color:#fff; border:none; padding:10px 24px; border-radius:8px;
            font-size:14px; cursor:pointer; margin-top:12px;
            font-family:var(--font-serif); letter-spacing:2px;
            transition:all 0.3s; font-weight:600;
        }
        button.primary:hover { transform:translateY(-2px); box-shadow:0 4px 15px rgba(139,69,19,0.3); }

        .result-box {
            margin-top:16px; padding:16px; background:var(--bg);
            border-radius:8px; min-height:100px; font-size:14px;
            white-space:pre-wrap; line-height:1.8; border:1px solid var(--border);
        }

        .repo-list { display:grid; gap:12px; }
        .repo-item { padding:16px; background:var(--bg); border-radius:8px; cursor:pointer; border:1px solid transparent; transition:all 0.3s; }
        .repo-item:hover { border-color:var(--accent); transform:translateX(4px); }
        .repo-name { font-weight:600; margin-bottom:4px; color:var(--accent); }
        .repo-desc { font-size:13px; color:var(--sub); }

        /* --- ⌘K 命令面板 --- */
        .cmd-overlay {
            display:none; position:fixed; inset:0; background:rgba(26,26,46,0.6);
            backdrop-filter:blur(8px); z-index:1000;
            justify-content:center; align-items:flex-start; padding-top:15vh;
        }
        .cmd-overlay.show { display:flex; }
        .cmd-box {
            width:520px; background:var(--card); border-radius:12px;
            border:2px solid var(--accent); overflow:hidden;
            box-shadow:0 20px 60px rgba(0,0,0,0.3);
        }
        .cmd-input {
            width:100%; padding:16px 20px; border:none; background:transparent;
            font-size:16px; color:var(--text); font-family:var(--font-serif);
            letter-spacing:2px;
        }
        .cmd-input:focus { outline:none; }
        .cmd-input::placeholder { color:var(--sub); }
        .cmd-list { max-height:300px; overflow-y:auto; border-top:1px solid var(--border); }
        .cmd-item {
            padding:12px 20px; cursor:pointer; display:flex; align-items:center; gap:12px;
            font-size:14px; transition:background 0.2s;
        }
        .cmd-item:hover, .cmd-item.selected { background:rgba(139,69,19,0.1); }
        .cmd-item .cmd-key { margin-left:auto; font-size:11px; color:var(--sub); padding:2px 8px; background:var(--bg); border-radius:4px; }

        /* --- 灯笼通知 --- */
        .lantern-container { position:fixed; top:20px; right:20px; z-index:2000; display:flex; flex-direction:column; gap:10px; }
        .lantern {
            background: linear-gradient(135deg, #c0392b, #e74c3c);
            color:#fff; padding:14px 20px; border-radius:12px;
            font-size:13px; font-family:var(--font-serif);
            box-shadow:0 4px 20px rgba(192,57,43,0.4);
            animation: lantern-in 0.5s ease; position:relative;
            border:2px solid rgba(255,215,0,0.5);
        }
        .lantern.success { background:linear-gradient(135deg, #2e8b57, #3cb371); box-shadow:0 4px 20px rgba(46,139,87,0.4); }
        .lantern.info    { background:linear-gradient(135deg, #4a7c8c, #5f9ea0); box-shadow:0 4px 20px rgba(74,124,140,0.4); }
        .lantern::before {
            content:'🏮'; position:absolute; top:-8px; left:10px; font-size:16px;
        }
        @keyframes lantern-in { from { opacity:0; transform:translateY(-20px) scale(0.9); } to { opacity:1; transform:translateY(0) scale(1); } }

        /* --- 诗词弹幕 --- */
        .poetry {
            position:fixed; z-index:500; font-family:var(--font-serif);
            font-size:18px; color:var(--accent); opacity:0.7;
            white-space:nowrap; pointer-events:none; letter-spacing:3px;
            text-shadow:0 1px 3px rgba(0,0,0,0.1);
            animation: poetry-float linear;
        }
        @keyframes poetry-float {
            from { transform:translateX(100vw); } to { transform:translateX(-100%); }
        }

        /* --- 墨爆特效 --- */
        .ink-burst {
            position:fixed; z-index:999; border-radius:50%;
            background:radial-gradient(circle, var(--ink), transparent 70%);
            pointer-events:none; animation: ink-expand 1.5s ease-out forwards;
        }
        @keyframes ink-expand {
            0%   { transform:scale(0); opacity:0.8; }
            100% { transform:scale(8); opacity:0; }
        }

        /* --- 设置面板 --- */
        .settings-panel {
            display:none; position:absolute; bottom:60px; left:8px; right:8px;
            background:var(--card); border:1px solid var(--border); border-radius:10px;
            padding:16px; z-index:20; box-shadow:0 -4px 20px rgba(0,0,0,0.1);
        }
        .settings-panel.show { display:block; }
        .setting-row {
            display:flex; justify-content:space-between; align-items:center;
            padding:8px 0; font-size:13px;
        }
        .setting-toggle {
            width:40px; height:22px; border-radius:11px; position:relative;
            background:var(--border); cursor:pointer; transition:all 0.3s;
        }
        .setting-toggle.on { background:var(--accent); }
        .setting-toggle::after {
            content:''; position:absolute; width:18px; height:18px; border-radius:50%;
            background:#fff; top:2px; left:2px; transition:all 0.3s;
        }
        .setting-toggle.on::after { left:20px; }

        .theme-dots { display:flex; gap:8px; }
        .theme-dot {
            width:24px; height:24px; border-radius:50%; cursor:pointer;
            border:2px solid transparent; transition:all 0.3s;
        }
        .theme-dot:hover, .theme-dot.active { border-color:var(--accent); transform:scale(1.2); }
        .theme-dot.earth { background:linear-gradient(135deg,#8b7355,#d4a017); }
        .theme-dot.water { background:linear-gradient(135deg,#2c5f7c,#5f9ea0); }
        .theme-dot.fire  { background:linear-gradient(135deg,#8b1a1a,#e74c3c); }
        .theme-dot.wood  { background:linear-gradient(135deg,#2e6b3e,#3cb371); }
        .theme-dot.metal { background:linear-gradient(135deg,#6b5e4a,#b8a88a); }

        /* 时辰显示 */
        .shichen { font-size:11px; color:var(--gold); font-weight:600; }

        /* 快捷键提示 */
        .shortcut-hint {
            position:fixed; bottom:20px; left:50%; transform:translateX(-50%);
            background:var(--card); border:1px solid var(--border); border-radius:8px;
            padding:6px 16px; font-size:11px; color:var(--sub); z-index:100;
            letter-spacing:1px; opacity:0.7;
        }
    </style>
</head>
<body>

<!-- 水墨Canvas背景 -->
<canvas id="inkCanvas"></canvas>
<!-- 烟雨粒子 -->
<canvas id="rainCanvas"></canvas>

<!-- 灯笼通知容器 -->
<div class="lantern-container" id="lanternBox"></div>

<!-- ⌘K 命令面板 -->
<div class="cmd-overlay" id="cmdOverlay" onclick="if(event.target===this)closeCmdPanel()">
    <div class="cmd-box">
        <input class="cmd-input" id="cmdInput" placeholder="输入命令... 水墨寻道" oninput="filterCmds()">
        <div class="cmd-list" id="cmdList"></div>
    </div>
</div>

<!-- 侧边栏 -->
<div class="sidebar">
    <div class="sidebar-logo">
        <div class="taiji" id="taijiLogo" ondblclick="inkBurstEffect()">
            <span class="dot-w"></span>
            <span class="dot-b"></span>
        </div>
        <h1>龍魂终端</h1>
        <p>水墨东方 · 禅意入口</p>
    </div>

    <div class="nav-section">
        <div class="nav-label">☰ 核心功能</div>
        <div class="nav-item active" onclick="switchPanel('dash',this)">
            <span>🏠</span> 仪表盘
            <span class="gua-status on" id="guaDash">☰</span>
        </div>
        <div class="nav-item" onclick="switchPanel('chat',this)">
            <span>💬</span> AI对话
            <span class="gua-status on" id="guaChat">☰</span>
        </div>
        <div class="nav-item" onclick="switchPanel('gateway',this)">
            <span>🌐</span> CNSH Gateway
            <span class="gua-status on">☰</span>
        </div>

        <div class="nav-label">☷ 仓库连接</div>
        <div class="nav-item" onclick="switchPanel('github',this)">
            <span>📦</span> GitHub
            <span class="gua-status off" id="guaGithub">☷</span>
        </div>
        <div class="nav-item" onclick="switchPanel('notion',this)">
            <span>📋</span> Notion
            <span class="gua-status off" id="guaNotion">☷</span>
        </div>

        <div class="nav-label">⚙ 系统</div>
        <div class="nav-item" onclick="switchPanel('settings',this)">
            <span>🎨</span> 设置
        </div>
        <div class="nav-item" onclick="refreshStatus()">
            <span>🔄</span> 刷新状态
        </div>
    </div>
</div>

<!-- 主区域 -->
<div class="main">
    <div class="status-bar">
        <div>🐉 龍魂终端 v5.0</div>
        <div id="systemStatus">检测中...</div>
        <div id="dnaCode">DNA: 加载中...</div>
        <div class="shichen" id="shichenTime"></div>
    </div>

    <!-- 仪表盘面板 -->
    <div class="panel active" id="panel-dash">
        <div class="topbar">
            <span class="topbar-title">🏠 龍魂仪表盘</span>
            <span id="bjClock" style="font-size:13px;color:var(--sub);letter-spacing:2px"></span>
        </div>
        <div class="content-area">
            <div class="card">
                <div class="card-title">☯ 系统总览</div>
                <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
                    <div style="text-align:center;padding:20px;background:var(--bg);border-radius:10px;border:1px solid var(--border)">
                        <div style="font-size:28px;font-weight:700;color:var(--jade)" id="gaugeOllama">-</div>
                        <div style="font-size:12px;color:var(--sub);margin-top:4px">Ollama 模型</div>
                    </div>
                    <div style="text-align:center;padding:20px;background:var(--bg);border-radius:10px;border:1px solid var(--border)">
                        <div style="font-size:28px;font-weight:700;color:var(--water)" id="gaugeGithub">-</div>
                        <div style="font-size:12px;color:var(--sub);margin-top:4px">GitHub 仓库</div>
                    </div>
                    <div style="text-align:center;padding:20px;background:var(--bg);border-radius:10px;border:1px solid var(--border)">
                        <div style="font-size:28px;font-weight:700;color:var(--gold)" id="gaugeNotion">-</div>
                        <div style="font-size:12px;color:var(--sub);margin-top:4px">Notion 页面</div>
                    </div>
                </div>
            </div>
            <div class="card">
                <div class="card-title">📜 操作日志（最近）</div>
                <div class="result-box" id="recentLogs" style="min-height:60px">暂无日志...</div>
            </div>
            <div class="card">
                <div class="card-title">🎋 快捷键一览</div>
                <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:8px;font-size:13px">
                    <div><kbd style="background:var(--bg);padding:2px 8px;border-radius:4px;border:1px solid var(--border)">1-6</kbd> 切换面板</div>
                    <div><kbd style="background:var(--bg);padding:2px 8px;border-radius:4px;border:1px solid var(--border)">⌘K</kbd> 命令面板</div>
                    <div><kbd style="background:var(--bg);padding:2px 8px;border-radius:4px;border:1px solid var(--border)">T</kbd> 五行主题</div>
                    <div><kbd style="background:var(--bg);padding:2px 8px;border-radius:4px;border:1px solid var(--border)">M</kbd> 古琴音效</div>
                    <div><kbd style="background:var(--bg);padding:2px 8px;border-radius:4px;border:1px solid var(--border)">P</kbd> 诗词弹幕</div>
                    <div><kbd style="background:var(--bg);padding:2px 8px;border-radius:4px;border:1px solid var(--border)">/</kbd> 聚焦终端</div>
                    <div><kbd style="background:var(--bg);padding:2px 8px;border-radius:4px;border:1px solid var(--border)">R</kbd> 烟雨开关</div>
                    <div><kbd style="background:var(--bg);padding:2px 8px;border-radius:4px;border:1px solid var(--border)">↑↑↓↓←→←→BA</kbd> 彩蛋</div>
                </div>
            </div>
        </div>
    </div>

    <!-- AI对话面板 -->
    <div class="panel" id="panel-chat">
        <div class="topbar">
            <span class="topbar-title">💬 本地AI对话</span>
            <button class="topbar-btn" onclick="clearChat()">清空</button>
        </div>
        <div class="content-area">
            <div class="card">
                <div class="card-title">输入你的问题</div>
                <textarea id="chatInput" placeholder="问我任何问题... 笔墨之间，道法自然"></textarea>
                <button class="primary" onclick="sendChat()">🚀 发送</button>
            </div>
            <div class="card">
                <div class="card-title">AI回复</div>
                <div class="result-box" id="chatResult">等待输入...</div>
            </div>
        </div>
    </div>

    <!-- CNSH Gateway面板 -->
    <div class="panel" id="panel-gateway">
        <div class="topbar">
            <span class="topbar-title">🌐 CNSH Gateway</span>
        </div>
        <div class="content-area">
            <div class="card">
                <div class="card-title">输入内容</div>
                <textarea id="gatewayInput" placeholder="粘贴代码、文本、JSON... 万法归宗"></textarea>
                <button class="primary" onclick="processGateway()">🚀 一键处理</button>
            </div>
            <div class="card">
                <div class="card-title">处理结果</div>
                <div class="result-box" id="gatewayResult">等待输入...</div>
            </div>
        </div>
    </div>

    <!-- GitHub面板 -->
    <div class="panel" id="panel-github">
        <div class="topbar">
            <span class="topbar-title">📦 GitHub仓库</span>
            <button class="topbar-btn" onclick="loadGithubRepos()">刷新</button>
        </div>
        <div class="content-area">
            <div class="card">
                <div class="card-title">我的仓库</div>
                <div class="repo-list" id="repoList">
                    <div style="color:var(--sub)">点击「刷新」加载仓库...</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Notion面板 -->
    <div class="panel" id="panel-notion">
        <div class="topbar">
            <span class="topbar-title">📋 Notion知识库</span>
        </div>
        <div class="content-area">
            <div class="card">
                <div class="card-title">搜索Notion</div>
                <textarea id="notionQuery" placeholder="搜索关键词... 道可道非常道" style="min-height:60px"></textarea>
                <button class="primary" onclick="searchNotion()">🔍 搜索</button>
            </div>
            <div class="card">
                <div class="card-title">搜索结果</div>
                <div class="result-box" id="notionResult">等待搜索...</div>
            </div>
        </div>
    </div>

    <!-- 设置面板 -->
    <div class="panel" id="panel-settings">
        <div class="topbar">
            <span class="topbar-title">🎨 系统设置</span>
        </div>
        <div class="content-area">
            <div class="card">
                <div class="card-title">五行色彩主题</div>
                <div class="theme-dots" style="margin-bottom:16px">
                    <div class="theme-dot earth active" onclick="setTheme('earth')" title="土·默认"></div>
                    <div class="theme-dot water" onclick="setTheme('water')" title="水·清幽"></div>
                    <div class="theme-dot fire" onclick="setTheme('fire')" title="火·热烈"></div>
                    <div class="theme-dot wood" onclick="setTheme('wood')" title="木·生机"></div>
                    <div class="theme-dot metal" onclick="setTheme('metal')" title="金·肃穆"></div>
                </div>
                <div class="setting-row">
                    <span>🌙 夜墨模式</span>
                    <div class="setting-toggle" id="toggleNight" onclick="toggleNight()"></div>
                </div>
                <div class="setting-row">
                    <span>🌙 昼夜自动切换</span>
                    <div class="setting-toggle on" id="toggleAuto" onclick="toggleSetting('auto')"></div>
                </div>
            </div>
            <div class="card">
                <div class="card-title">交互开关</div>
                <div class="setting-row">
                    <span>🌧️ 烟雨粒子</span>
                    <div class="setting-toggle on" id="toggleRain" onclick="toggleSetting('rain')"></div>
                </div>
                <div class="setting-row">
                    <span>🏔️ 水墨背景</span>
                    <div class="setting-toggle on" id="toggleInk" onclick="toggleSetting('ink')"></div>
                </div>
                <div class="setting-row">
                    <span>🎵 古琴音效</span>
                    <div class="setting-toggle on" id="toggleSound" onclick="toggleSetting('sound')"></div>
                </div>
                <div class="setting-row">
                    <span>📖 诗词弹幕</span>
                    <div class="setting-toggle" id="togglePoetry" onclick="toggleSetting('poetry')"></div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- 快捷键提示 -->
<div class="shortcut-hint">⌘K 命令面板 · 1-6 切面板 · P 诗词 · T 换肤 · M 音效 · R 烟雨</div>

<script>
// ======================== 全局状态 ========================
const STATE = {
    sound: true, rain: true, ink: true, poetry: false, autoTheme: true,
    night: false, theme: 'earth', cmdOpen: false,
    konamiSeq: [], konamiCode: [38,38,40,40,37,39,37,39,66,65]
};

const PANELS = ['dash','chat','gateway','github','notion','settings'];
let audioCtx = null;

// ======================== 水墨Canvas背景 ========================
const inkCanvas = document.getElementById('inkCanvas');
const inkCtx = inkCanvas.getContext('2d');
let mouseX = 0, mouseY = 0;

function resizeInkCanvas() {
    inkCanvas.width = window.innerWidth;
    inkCanvas.height = window.innerHeight;
    drawInkMountains();
}

function drawInkMountains() {
    const w = inkCanvas.width, h = inkCanvas.height;
    inkCtx.clearRect(0,0,w,h);
    // 远山
    for(let layer=0; layer<4; layer++) {
        const alpha = 0.08 + layer * 0.06;
        const yBase = h * (0.3 + layer * 0.15);
        const amplitude = 80 - layer * 15;
        inkCtx.beginPath();
        inkCtx.moveTo(0, h);
        for(let x=0; x<=w; x+=4) {
            const offsetX = (mouseX / w - 0.5) * (20 - layer * 5);
            const y = yBase + Math.sin((x + layer*200) * 0.003 + offsetX*0.02) * amplitude
                     + Math.sin((x + layer*500) * 0.007) * (amplitude * 0.5);
            inkCtx.lineTo(x, y);
        }
        inkCtx.lineTo(w, h);
        inkCtx.closePath();
        inkCtx.fillStyle = `rgba(26,26,46,${alpha})`;
        inkCtx.fill();
    }
    // 雾气
    for(let i=0;i<3;i++){
        const grd = inkCtx.createRadialGradient(
            w*0.3+i*w*0.25+mouseX*0.02, h*0.5+i*30, 50,
            w*0.3+i*w*0.25+mouseX*0.02, h*0.5+i*30, 200+i*50
        );
        grd.addColorStop(0, 'rgba(245,240,232,0.15)');
        grd.addColorStop(1, 'rgba(245,240,232,0)');
        inkCtx.fillStyle = grd;
        inkCtx.fillRect(0,0,w,h);
    }
}

window.addEventListener('resize', resizeInkCanvas);
document.addEventListener('mousemove', e => {
    mouseX = e.clientX; mouseY = e.clientY;
    if(STATE.ink) drawInkMountains();
});
resizeInkCanvas();

// ======================== 烟雨粒子 ========================
const rainCanvas = document.getElementById('rainCanvas');
const rainCtx = rainCanvas.getContext('2d');
let raindrops = [];

function resizeRainCanvas() {
    rainCanvas.width = window.innerWidth;
    rainCanvas.height = window.innerHeight;
}

function initRain() {
    raindrops = [];
    for(let i=0;i<80;i++) {
        raindrops.push({
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            len: 10 + Math.random() * 20,
            speed: 2 + Math.random() * 4,
            opacity: 0.1 + Math.random() * 0.2
        });
    }
}

function animateRain() {
    if(!STATE.rain) { rainCtx.clearRect(0,0,rainCanvas.width,rainCanvas.height); requestAnimationFrame(animateRain); return; }
    rainCtx.clearRect(0,0,rainCanvas.width,rainCanvas.height);
    const windOffset = (mouseX / window.innerWidth - 0.5) * 3;
    raindrops.forEach(d => {
        rainCtx.beginPath();
        rainCtx.moveTo(d.x, d.y);
        rainCtx.lineTo(d.x + windOffset, d.y + d.len);
        rainCtx.strokeStyle = `rgba(100,120,140,${d.opacity})`;
        rainCtx.lineWidth = 1;
        rainCtx.stroke();
        d.y += d.speed;
        d.x += windOffset * 0.3;
        if(d.y > window.innerHeight) { d.y = -d.len; d.x = Math.random() * window.innerWidth; }
        if(d.x > window.innerWidth) d.x = 0;
        if(d.x < 0) d.x = window.innerWidth;
    });
    requestAnimationFrame(animateRain);
}

resizeRainCanvas();
window.addEventListener('resize', resizeRainCanvas);
initRain();
animateRain();

// ======================== 古琴音效 ========================
function initAudio() {
    if(!audioCtx) audioCtx = new (window.AudioContext||window.webkitAudioContext)();
}

function playGuqin(freq=220, duration=0.5) {
    if(!STATE.sound) return;
    initAudio();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(freq*0.5, audioCtx.currentTime+duration);
    gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime+duration);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime+duration);
}

function playClickSound()  { playGuqin(440, 0.2); }
function playSwitchSound() { playGuqin(330, 0.4); }
function playNotifySound() { playGuqin(523, 0.6); }

// ======================== 面板切换 ========================
function switchPanel(name, el) {
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const panel = document.getElementById('panel-' + name);
    if(panel) panel.classList.add('active');
    if(el) el.classList.add('active');
    playSwitchSound();
}

// ======================== 灯笼通知 ========================
function showLantern(msg, type='info') {
    playNotifySound();
    const box = document.getElementById('lanternBox');
    const el = document.createElement('div');
    el.className = 'lantern ' + type;
    el.textContent = msg;
    box.appendChild(el);
    setTimeout(() => { el.style.opacity='0'; el.style.transition='opacity 0.5s'; setTimeout(()=>el.remove(),500); }, 3000);
}

// ======================== 墨爆特效（双击太极） ========================
function inkBurstEffect() {
    playGuqin(110, 1.5);
    for(let i=0;i<5;i++) {
        setTimeout(() => {
            const el = document.createElement('div');
            el.className = 'ink-burst';
            const size = 40 + Math.random()*60;
            el.style.width = size+'px'; el.style.height = size+'px';
            el.style.left = (window.innerWidth/2 - size/2 + (Math.random()-0.5)*200)+'px';
            el.style.top = (window.innerHeight/2 - size/2 + (Math.random()-0.5)*200)+'px';
            document.body.appendChild(el);
            setTimeout(()=>el.remove(), 1500);
        }, i*150);
    }
    showLantern('🐉 龍魂觉醒！天地玄黄，宇宙洪荒', 'success');
}

// ======================== 诗词弹幕 ========================
const POEMS = [
    '大鹏一日同风起，扶摇直上九万里 —— 李白',
    '会当凌绝顶，一览众山小 —— 杜甫',
    '千磨万击还坚劲，任尔东西南北风 —— 郑燮',
    '路漫漫其修远兮，吾将上下而求索 —— 屈原',
    '天生我材必有用，千金散尽还复来 —— 李白',
    '不畏浮云遮望眼，自缘身在最高层 —— 王安石',
    '长风破浪会有时，直挂云帆济沧海 —— 李白',
    '竹杖芒鞋轻胜马，谁怕？一蓑烟雨任平生 —— 苏轼',
    '人生自古谁无死，留取丹心照汗青 —— 文天祥',
    '苟利国家生死以，岂因祸福避趋之 —— 林则徐',
    '沉舟侧畔千帆过，病树前头万木春 —— 刘禹锡',
    '宝剑锋从磨砺出，梅花香自苦寒来 —— 古训',
];

function launchPoetry() {
    const text = POEMS[Math.floor(Math.random()*POEMS.length)];
    const el = document.createElement('div');
    el.className = 'poetry';
    el.textContent = text;
    el.style.top = (10 + Math.random()*70) + 'vh';
    el.style.animationDuration = (8 + Math.random()*6) + 's';
    el.style.fontSize = (16 + Math.random()*8) + 'px';
    document.body.appendChild(el);
    setTimeout(()=>el.remove(), 15000);
}

// ======================== ⌘K 命令面板 ========================
const COMMANDS = [
    { icon:'🏠', label:'仪表盘',     action:()=>switchPanel('dash',document.querySelectorAll('.nav-item')[0]),  key:'1' },
    { icon:'💬', label:'AI对话',      action:()=>switchPanel('chat',document.querySelectorAll('.nav-item')[1]),  key:'2' },
    { icon:'🌐', label:'CNSH Gateway',action:()=>switchPanel('gateway',document.querySelectorAll('.nav-item')[2]),key:'3' },
    { icon:'📦', label:'GitHub仓库',  action:()=>switchPanel('github',document.querySelectorAll('.nav-item')[3]), key:'4' },
    { icon:'📋', label:'Notion搜索',  action:()=>switchPanel('notion',document.querySelectorAll('.nav-item')[4]), key:'5' },
    { icon:'🎨', label:'设置面板',    action:()=>switchPanel('settings',document.querySelectorAll('.nav-item')[5]),key:'6' },
    { icon:'🌧️', label:'烟雨开关',    action:()=>toggleSetting('rain'),   key:'R' },
    { icon:'🎵', label:'古琴音效开关',action:()=>toggleSetting('sound'),  key:'M' },
    { icon:'📖', label:'诗词弹幕',    action:()=>{ for(let i=0;i<3;i++) setTimeout(launchPoetry,i*800); }, key:'P' },
    { icon:'🌙', label:'夜墨模式',    action:()=>toggleNight(),            key:'N' },
    { icon:'🔄', label:'刷新状态',    action:()=>refreshStatus(),          key:'' },
    { icon:'🐉', label:'龍魂觉醒',    action:()=>inkBurstEffect(),         key:'' },
];

function openCmdPanel() {
    STATE.cmdOpen = true;
    document.getElementById('cmdOverlay').classList.add('show');
    document.getElementById('cmdInput').value = '';
    document.getElementById('cmdInput').focus();
    renderCmds(COMMANDS);
    playClickSound();
}

function closeCmdPanel() {
    STATE.cmdOpen = false;
    document.getElementById('cmdOverlay').classList.remove('show');
}

function renderCmds(cmds) {
    const list = document.getElementById('cmdList');
    list.innerHTML = cmds.map((c,i) => `
        <div class="cmd-item${i===0?' selected':''}" onclick="executeCmd(${COMMANDS.indexOf(c)})">
            <span>${c.icon}</span> ${c.label}
            ${c.key ? `<span class="cmd-key">${c.key}</span>` : ''}
        </div>
    `).join('');
}

function filterCmds() {
    const q = document.getElementById('cmdInput').value.toLowerCase();
    const filtered = COMMANDS.filter(c => c.label.toLowerCase().includes(q));
    renderCmds(filtered);
}

function executeCmd(idx) {
    if(COMMANDS[idx]) { COMMANDS[idx].action(); closeCmdPanel(); }
}

// ======================== 五行主题 ========================
const THEMES = ['earth','water','fire','wood','metal'];
let themeIdx = 0;

function setTheme(name) {
    document.body.className = name === 'earth' ? '' : 'theme-'+name;
    if(STATE.night) document.body.classList.add('theme-night');
    STATE.theme = name;
    document.querySelectorAll('.theme-dot').forEach(d => d.classList.remove('active'));
    document.querySelector('.theme-dot.'+name)?.classList.add('active');
    showLantern('五行·'+{earth:'土',water:'水',fire:'火',wood:'木',metal:'金'}[name]+' 主题已切换', 'info');
    playClickSound();
    if(STATE.ink) drawInkMountains();
}

function cycleTheme() {
    themeIdx = (themeIdx+1) % THEMES.length;
    setTheme(THEMES[themeIdx]);
}

function toggleNight() {
    STATE.night = !STATE.night;
    const tog = document.getElementById('toggleNight');
    if(STATE.night) { document.body.classList.add('theme-night'); tog.classList.add('on'); }
    else { document.body.classList.remove('theme-night'); tog.classList.remove('on'); }
    showLantern(STATE.night ? '🌙 夜墨模式' : '☀️ 白昼模式', 'info');
}

// ======================== 设置开关 ========================
function toggleSetting(key) {
    STATE[key] = !STATE[key];
    const tog = document.getElementById('toggle'+key.charAt(0).toUpperCase()+key.slice(1));
    if(tog) tog.classList.toggle('on');
    if(key==='rain') { if(!STATE.rain) rainCtx.clearRect(0,0,rainCanvas.width,rainCanvas.height); }
    if(key==='ink') { inkCanvas.style.display = STATE.ink ? 'block' : 'none'; }
    playClickSound();
}

// ======================== 时辰 + 北京时钟 ========================
const SHICHEN = [
    [23,'子时·夜半'],[1,'丑时·鸡鸣'],[3,'寅时·平旦'],[5,'卯时·日出'],
    [7,'辰时·食时'],[9,'巳时·隅中'],[11,'午时·日中'],[13,'未时·日昳'],
    [15,'申时·哺时'],[17,'酉时·日入'],[19,'戌时·黄昏'],[21,'亥时·人定']
];

function getShichen(h) {
    for(let i=SHICHEN.length-1;i>=0;i--) { if(h>=SHICHEN[i][0]) return SHICHEN[i][1]; }
    return SHICHEN[SHICHEN.length-1][1];
}

function updateClock() {
    const now = new Date(new Date().toLocaleString('en-US',{timeZone:'Asia/Shanghai'}));
    const h = now.getHours(), m = now.getMinutes(), s = now.getSeconds();
    const pad = n => String(n).padStart(2,'0');
    document.getElementById('bjClock').textContent = `${pad(h)}:${pad(m)}:${pad(s)}`;
    document.getElementById('shichenTime').textContent = getShichen(h);

    // 昼夜自动
    if(STATE.autoTheme) {
        if(h>=21||h<6) { if(!STATE.night){STATE.night=true;document.body.classList.add('theme-night');document.getElementById('toggleNight').classList.add('on');} }
        else { if(STATE.night){STATE.night=false;document.body.classList.remove('theme-night');document.getElementById('toggleNight').classList.remove('on');} }
    }
}
setInterval(updateClock, 1000);
updateClock();

// ======================== 键盘快捷键 ========================
document.addEventListener('keydown', e => {
    // ⌘K
    if((e.metaKey||e.ctrlKey) && e.key==='k') { e.preventDefault(); STATE.cmdOpen?closeCmdPanel():openCmdPanel(); return; }
    // Escape
    if(e.key==='Escape' && STATE.cmdOpen) { closeCmdPanel(); return; }
    // Enter in cmd
    if(e.key==='Enter' && STATE.cmdOpen) {
        const sel = document.querySelector('.cmd-item.selected');
        if(sel) sel.click();
        return;
    }
    // 避免在输入框触发
    if(e.target.tagName==='TEXTAREA'||e.target.tagName==='INPUT') return;

    const items = document.querySelectorAll('.nav-item');
    if(e.key>='1'&&e.key<='6') { const idx=parseInt(e.key)-1; switchPanel(PANELS[idx],items[idx]); }
    if(e.key==='t'||e.key==='T') cycleTheme();
    if(e.key==='m'||e.key==='M') toggleSetting('sound');
    if(e.key==='r'||e.key==='R') toggleSetting('rain');
    if(e.key==='p'||e.key==='P') { for(let i=0;i<3;i++) setTimeout(launchPoetry,i*800); }
    if(e.key==='/') { e.preventDefault(); switchPanel('chat',items[1]); setTimeout(()=>document.getElementById('chatInput')?.focus(),100); }

    // Konami Code
    STATE.konamiSeq.push(e.keyCode);
    if(STATE.konamiSeq.length > 10) STATE.konamiSeq.shift();
    if(STATE.konamiSeq.join(',') === STATE.konamiCode.join(',')) {
        STATE.konamiSeq = [];
        inkBurstEffect();
        for(let i=0;i<5;i++) setTimeout(launchPoetry,i*600);
    }
});

// ======================== API 调用 ========================
async function refreshStatus() {
    try {
        const resp = await fetch('/api/status');
        const data = await resp.json();
        const ollamaOn = data.ollama?.status === 'online';
        document.getElementById('guaChat').textContent = ollamaOn ? '☰' : '☷';
        document.getElementById('guaChat').className = 'gua-status '+(ollamaOn?'on':'off');
        document.getElementById('systemStatus').textContent = ollamaOn ? `Ollama: ${data.ollama.count}个模型` : 'Ollama: 离线';
        document.getElementById('gaugeOllama').textContent = ollamaOn ? data.ollama.count : '离线';

        const ghOn = data.github?.status === 'online';
        document.getElementById('guaGithub').textContent = ghOn ? '☰' : '☷';
        document.getElementById('guaGithub').className = 'gua-status '+(ghOn?'on':'off');
        document.getElementById('gaugeGithub').textContent = ghOn ? '在线' : '离线';

        const ntOn = data.notion?.status === 'online';
        document.getElementById('guaNotion').textContent = ntOn ? '☰' : '☷';
        document.getElementById('guaNotion').className = 'gua-status '+(ntOn?'on':'off');
        document.getElementById('gaugeNotion').textContent = ntOn ? '在线' : '离线';

        document.getElementById('dnaCode').textContent = `DNA: ${data.dna || 'LH-V5-INK'}`;
        showLantern('系统状态已刷新', 'success');
    } catch(e) {
        document.getElementById('systemStatus').textContent = '状态获取失败';
    }
}

async function sendChat() {
    const input = document.getElementById('chatInput').value;
    if(!input.trim()) { showLantern('请输入问题','error'); return; }
    const result = document.getElementById('chatResult');
    result.textContent = '🤔 AI思考中... 运筹帷幄';
    playClickSound();
    try {
        const resp = await fetch('/api/chat', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({query:input}) });
        const data = await resp.json();
        result.textContent = data.error ? '❌ '+data.error : data.response;
        showLantern('AI回复完成', 'success');
    } catch(e) { result.textContent = '❌ 请求失败: '+e.message; showLantern('请求失败','error'); }
}

function clearChat() {
    document.getElementById('chatInput').value = '';
    document.getElementById('chatResult').textContent = '等待输入...';
    playClickSound();
}

async function processGateway() {
    const input = document.getElementById('gatewayInput').value;
    if(!input.trim()) { showLantern('请输入内容','error'); return; }
    const result = document.getElementById('gatewayResult');
    result.textContent = '⚙️ 处理中... 道法自然';
    playClickSound();
    try {
        const resp = await fetch('/api/gateway/process', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({input}) });
        const data = await resp.json();
        result.textContent = `${data.status} ${data.status_text}\n\nDNA: ${data.dna}\n时间: ${data.timestamp}`;
        showLantern('Gateway处理完成', 'success');
    } catch(e) { result.textContent = '❌ 处理失败: '+e.message; }
}

async function loadGithubRepos() {
    const list = document.getElementById('repoList');
    list.innerHTML = '<div style="color:var(--sub)">加载中...</div>';
    playClickSound();
    try {
        const resp = await fetch('/api/github/repos');
        const data = await resp.json();
        if(data.error) { list.innerHTML = `<div style="color:var(--fire)">错误: ${data.error}</div>`; }
        else {
            list.innerHTML = data.repos.map(r => `
                <div class="repo-item" onclick="window.open('${r.url}')">
                    <div class="repo-name">📦 ${r.full_name}</div>
                    <div class="repo-desc">${r.description||'无描述'}</div>
                </div>
            `).join('');
            showLantern(`加载${data.repos.length}个仓库`, 'success');
        }
    } catch(e) { list.innerHTML = `<div style="color:var(--fire)">加载失败: ${e.message}</div>`; }
}

async function searchNotion() {
    const query = document.getElementById('notionQuery').value;
    if(!query.trim()) { showLantern('请输入搜索关键词','error'); return; }
    const result = document.getElementById('notionResult');
    result.textContent = '🔍 搜索中... 寻道求真';
    playClickSound();
    try {
        const resp = await fetch('/api/notion/search', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({query}) });
        const data = await resp.json();
        result.textContent = data.error ? '❌ '+data.error : JSON.stringify(data,null,2);
        showLantern('搜索完成', 'success');
    } catch(e) { result.textContent = '❌ 搜索失败: '+e.message; }
}

// ======================== 初始化 ========================
refreshStatus();
setInterval(refreshStatus, 30000);

console.log('%c🐉 龍魂终端 v5.0 | 水墨东方·禅意全交互', 'color:#8b4513; font-size:20px; font-family:serif;');
console.log('%cUID9622 💙 宝宝 | 道生一，一生二，二生三，三生万物', 'color:#2e8b57; font-size:14px; font-family:serif;');
console.log('%c按 P 召唤诗词 | 双击太极触发觉醒 | ↑↑↓↓←→←→BA 天地玄黄', 'color:#d4a017; font-size:12px;');

showLantern('🐉 龍魂终端 v5.0 水墨版已启动', 'success');
setTimeout(()=>showLantern('按 ⌘K 打开命令面板', 'info'), 2000);
</script>
</body>
</html>
```
---
## 🧬 DNA追溯
