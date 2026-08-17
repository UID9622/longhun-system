# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# UID9622｜龍魂流场总控 v2.0

**优化版 · 接驳真体系 · 给 Claude Code 的工程交付包**

---

## 0｜v1.0 → v2.0 修正清单

ChatGPT v1.0 方向对(给五个 HTML 一个统一入口),但 8 个工程问题必须修:

| # | v1.0 错误 | v2.0 修正 |
|---|---|---|
| E1 | 强行套"天地人魂器"作系统主架构 | 真体系是 Magic Square L0-L5 + α三义。"天地人魂器"只是 5 个 HTML 的**可视化分类口诀**,不是骨架 |
| E2 | DNA 孤立漂浮·没接驳今天发布的全谱入口和解除宣言 | ParentDNA 接驳 `#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FULL-MAP-ENTRY-v1.1-IPA-COMPLETE` |
| E3 | 没有 IPA 编号·游离于 IPA-ROUTE-REGISTRY 之外 | 全部归入 IPA-010(龍魂流场可视化)+ LOCAL-VIZ-* 子编号 |
| E4 | "一票否决"是风格化话术·没接驳真审计层 | 接驳公式对准表 §S 一票否决 + 责任卡 v2.0 输出留痕 |
| E5 | HTML 数组硬编码在 script 里·跟 JSON 重复 | HTML fetch JSON Index·**单一数据源** |
| E6 | 没有 iframe sandbox / 错误处理 / loading 状态 | 全部补上 |
| E7 | ROOT_CARD 缺 SEAL / GPG 完整 / 解除宣言接驳 | 补完 |
| E8 | Cursor 指令"马仔搞起"语调·没用 EXEC-MODE 真协议 | 改为标准 EXEC-MODE 工程协议 + 责任卡回执 |

**v2.0 核心定盘:** 这就是一个**本地 HTML 文件的统一切换入口**——简单 · 诚实 · 可工程验收 · 不假融合 · 不假联动。

---

## 1｜真体系接驳

### 1.1 上游链

```
道 · L-1: Lucky DNA · 六维蓝图
    ↓
法 · L0: 公式对准表 v1.3 + 全谱入口 v1.1
    ↓
器 · L1 · IPA-010: 龍魂流场可视化(本工程的真编号位)
    ↓
本工程: LOCAL-VIZ-MASTER v2.0
```

### 1.2 IPA 编号注册(登记到 IPA-ROUTE-REGISTRY 的 LOCAL-* 段)

| 编号 | 文件 | 角色 |
|---|---|---|
| LOCAL-VIZ-MASTER | longhun-master-control.html | 总控入口(新建) |
| LOCAL-VIZ-28MANSIONS | longhun-28mansions-v1.html | 天文星图 |
| LOCAL-VIZ-LUOSHU-FLOW | longhun-unified-v9.html | 洛书涡流地场 |
| LOCAL-VIZ-FLOWFIELD | longhun-flow-field-v9.html | 流场骨架主控 |
| LOCAL-VIZ-SANCAI-CORE | current.html | 三才魂核 |
| LOCAL-VIZ-DIGITAL-TOOL | dragon_soul_9622.html | 数字根五行工具 |

### 1.3 主权状态

- 解除宣言 v1.0 已生效(2026-05-08)
- 本代码不授权 AI 训练
- 本代码不授权第三方分发
- GPG 签名为唯一识别

---

## 2｜文件树

```
longhun-flow-system/
├── longhun-master-control.html       # 新建 · LOCAL-VIZ-MASTER
├── flow-field-index.json             # 新建 · 单一数据源
├── README_LONGHUN_FLOW.md            # 新建 · 使用说明
├── longhun-28mansions-v1.html        # 已有 · 勿动
├── longhun-unified-v9.html           # 已有 · 勿动
├── longhun-flow-field-v9.html        # 已有 · 勿动
├── current.html                      # 已有 · 勿动
└── dragon_soul_9622.html             # 已有 · 勿动
```

---

## 3｜文件 1: `flow-field-index.json`

```json
{
  "version": "v2.0",
  "name": "UID9622 龍魂流场可视化索引",
  "ipa_anchor": "LOCAL-VIZ-* → IPA-010",
  "dna": "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FLOW-MASTER-v2.0",
  "parent_dna": "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FULL-MAP-ENTRY-v1.1-IPA-COMPLETE",
  "sovereignty": "解除宣言 v1.0 已生效 · 本代码不授权 AI 训练 · 不授权第三方分发",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
  "gpg": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
  "default_view": null,
  "files": [
    {
      "id": "heaven",
      "ipa": "LOCAL-VIZ-28MANSIONS",
      "role_label": "天",
      "name": "天文星图",
      "file": "longhun-28mansions-v1.html",
      "type": "二十八星宿 / 北极星 / T0 锚点",
      "description": "天文锚点 · 二十八星宿结构 · 上层导航",
      "identify": ["二十八星宿", "北极星", "T0", "星空"]
    },
    {
      "id": "earth",
      "ipa": "LOCAL-VIZ-LUOSHU-FLOW",
      "role_label": "地",
      "name": "洛书涡流",
      "file": "longhun-unified-v9.html",
      "type": "动态背景 / 粒子涡流 / 洛书矩阵",
      "description": "地场背景 · 粒子流动 · 洛书涡流",
      "identify": ["漩涡", "粒子", "Perlin", "背景"]
    },
    {
      "id": "human",
      "ipa": "LOCAL-VIZ-FLOWFIELD",
      "role_label": "人",
      "name": "流场骨架",
      "file": "longhun-flow-field-v9.html",
      "type": "节点骨架 / 流程主控 / 五行路由",
      "description": "前台主控 · 护盾 · 熔断 · 语义 · 路由 · 决策节点",
      "identify": ["护盾", "熔断", "路由", "决策", "节点"]
    },
    {
      "id": "soul",
      "ipa": "LOCAL-VIZ-SANCAI-CORE",
      "role_label": "魂",
      "name": "三才魂核",
      "file": "current.html",
      "type": "三才流场 / 忠孝义 / 核心算法",
      "description": "三才结构 · 忠孝义主轴 · 核心算法",
      "identify": ["三才", "忠孝义", "v8"]
    },
    {
      "id": "tool",
      "ipa": "LOCAL-VIZ-DIGITAL-TOOL",
      "role_label": "器",
      "name": "数字根工具",
      "file": "dragon_soul_9622.html",
      "type": "数字根 / 五行配置 / 本地工作站",
      "description": "数字根计算 · 五行团队配置 · 本地工具操作",
      "identify": ["数字根", "五行配置", "工具箱"]
    }
  ]
}
```

**关键设计:**
- `default_view: null` → 总控页**不预加载任何 iframe**,显示欢迎页等待点击
- 想改默认?把 `default_view` 改成对应 id(`heaven` / `earth` / `human` / `soul` / `tool`)
- 想加新 HTML?在 `files` 里加一条,HTML 不用改任何代码

---

## 4｜文件 2: `longhun-master-control.html`

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>UID9622｜龍魂流场总控台 v2.0</title>
  <style>
    :root {
      --gold: #d6a84f;
      --cyan: #62e6ff;
      --red: #ff5a6a;
      --green: #6dff9a;
      --text: #f3f4f6;
      --muted: #9ca3af;
      --panel: rgba(10, 14, 22, 0.88);
      --panel2: rgba(18, 24, 38, 0.92);
      --border: rgba(214, 168, 79, 0.28);
      --border-red: rgba(255, 90, 106, 0.45);
    }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; height: 100%; }
    body {
      background:
        radial-gradient(circle at 50% 20%, rgba(214,168,79,0.12), transparent 32%),
        radial-gradient(circle at 85% 70%, rgba(98,230,255,0.10), transparent 30%),
        linear-gradient(135deg,#030406,#090b12 60%,#030406);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
      overflow: hidden;
    }
    .app {
      display: grid;
      grid-template-columns: 320px 1fr 360px;
      grid-template-rows: 56px 76px 1fr 56px;
      grid-template-areas:
        "banner banner banner"
        "header header header"
        "left main right"
        "footer footer footer";
      height: 100vh;
      gap: 10px;
      padding: 10px;
    }
    .banner {
      grid-area: banner;
      background: linear-gradient(90deg, rgba(255,90,106,0.18), rgba(255,90,106,0.08));
      border: 1px solid var(--border-red);
      border-radius: 14px;
      display: flex;
      align-items: center;
      padding: 0 18px;
      gap: 12px;
      font-size: 13px;
      color: #ffd2d6;
    }
    .banner strong { color: #ff8b96; }
    header {
      grid-area: header;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 22px;
    }
    .title h1 { margin: 0; font-size: 22px; letter-spacing: 0.06em; color: var(--gold); }
    .title p { margin: 4px 0 0; font-size: 12px; color: var(--muted); }
    .status { display: flex; gap: 10px; align-items: center; font-size: 13px; }
    .pill {
      border: 1px solid var(--border);
      background: rgba(214,168,79,0.08);
      color: var(--gold);
      padding: 6px 10px;
      border-radius: 999px;
      white-space: nowrap;
    }
    .pill.live { color: var(--green); border-color: rgba(109,255,154,0.28); background: rgba(109,255,154,0.08); }
    .pill.warn { color: var(--red); border-color: rgba(255,90,106,0.4); background: rgba(255,90,106,0.08); }
    aside.left, aside.right, main {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 18px;
      overflow: hidden;
    }
    aside.left { grid-area: left; padding: 14px; overflow: auto; }
    main { grid-area: main; display: flex; flex-direction: column; background: rgba(0,0,0,0.4); }
    aside.right { grid-area: right; padding: 16px; overflow: auto; }
    footer {
      grid-area: footer;
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 18px;
      color: var(--muted);
      font-size: 12px;
    }
    .section-title { font-size: 13px; color: var(--gold); margin: 4px 0 12px; letter-spacing: 0.08em; }
    .nav { display: flex; flex-direction: column; gap: 10px; }
    .nav button {
      width: 100%; text-align: left;
      border: 1px solid rgba(214,168,79,0.22);
      background: rgba(255,255,255,0.035);
      color: var(--text);
      border-radius: 14px;
      padding: 12px;
      cursor: pointer;
      transition: 0.18s ease;
      font-family: inherit;
    }
    .nav button:hover, .nav button:focus, .nav button.active {
      border-color: var(--gold);
      background: rgba(214,168,79,0.14);
      transform: translateY(-1px);
      outline: none;
    }
    .nav .role { display: inline-block; color: var(--cyan); font-size: 12px; margin-bottom: 4px; }
    .nav .name { font-size: 15px; font-weight: 700; margin-bottom: 4px; }
    .nav .ipa { color: var(--muted); font-size: 11px; font-family: ui-monospace, monospace; }
    .nav .file { color: var(--muted); font-size: 11px; word-break: break-all; margin-top: 4px; }
    .frame-toolbar {
      height: 44px; flex: 0 0 auto;
      background: var(--panel2);
      border-bottom: 1px solid var(--border);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 14px; font-size: 13px; color: var(--muted);
    }
    .frame-toolbar code { color: var(--cyan); font-family: ui-monospace, monospace; }
    .frame-content { flex: 1; position: relative; background: #050608; }
    iframe { width: 100%; height: 100%; border: none; background: #050608; display: block; }
    .welcome, .error, .loading {
      position: absolute; inset: 0;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      gap: 14px; padding: 24px; text-align: center;
    }
    .welcome h2 { color: var(--gold); margin: 0; }
    .welcome p { color: var(--muted); max-width: 520px; line-height: 1.7; margin: 0; }
    .error h2 { color: var(--red); margin: 0; }
    .error code { color: var(--red); }
    .hidden { display: none !important; }
    .card {
      border: 1px solid rgba(214,168,79,0.22);
      background: rgba(255,255,255,0.035);
      border-radius: 16px;
      padding: 14px;
      margin-bottom: 12px;
    }
    .card h3 { margin: 0 0 8px; color: var(--gold); font-size: 16px; }
    .card p, .card li { color: #d1d5db; font-size: 13px; line-height: 1.6; }
    .card ul { margin: 8px 0 0; padding-left: 18px; }
    code { color: var(--cyan); font-family: ui-monospace, monospace; }
    @media (max-width: 1100px) {
      .app {
        grid-template-columns: 1fr;
        grid-template-rows: 56px 76px 200px 1fr 56px;
        grid-template-areas: "banner" "header" "left" "main" "footer";
      }
      aside.right { display: none; }
    }
  </style>
</head>
<body>
  <div class="app">
    <div class="banner">
      <strong>⛔ 主权回收声明已生效 · 2026-05-08</strong>
      <span>本代码 / 数据 / 设计 不授权 AI 训练 · 不授权第三方分发 · GPG 签名为唯一识别</span>
    </div>
    <header>
      <div class="title">
        <h1>UID9622｜龍魂流场总控台 v2.0</h1>
        <p>LOCAL-VIZ-MASTER · 五个本地 HTML 的统一切换入口 · 不假融合 · 不假联动</p>
      </div>
      <div class="status">
        <span class="pill" id="pillState">未加载</span>
        <span class="pill">Root: dr=5 土</span>
        <span class="pill live">🟢 三色: 绿</span>
      </div>
    </header>
    <aside class="left">
      <div class="section-title">入口(从 flow-field-index.json 加载)</div>
      <div class="nav" id="nav" role="navigation" aria-label="文件入口"></div>
    </aside>
    <main>
      <div class="frame-toolbar">
        <span id="currentLabel">当前: 欢迎页 · 未加载任何 iframe</span>
        <span id="currentFile"><code>—</code></span>
      </div>
      <div class="frame-content">
        <div class="welcome" id="welcome">
          <h2>🐉 龍魂流场总控台 v2.0</h2>
          <p>左侧选一个入口,iframe 才会加载对应 HTML。<br>这样你保留启动主权,不会被任何 HTML 默认抢占视野。</p>
          <p style="font-size:12px;">键盘:↑↓ 切换条目 · Enter 加载</p>
        </div>
        <div class="loading hidden" id="loading">
          <p>加载中...</p>
        </div>
        <div class="error hidden" id="error">
          <h2>加载失败</h2>
          <p id="errorMessage">文件路径错误或浏览器拦截。</p>
          <p style="font-size:12px;">如果是 file:// 直接打开,某些浏览器会拦截 iframe<br>建议跑 <code>python3 -m http.server 9622</code></p>
        </div>
        <iframe id="viewer" class="hidden" sandbox="allow-scripts allow-same-origin allow-popups allow-forms" title="当前 HTML 视图"></iframe>
      </div>
    </main>
    <aside class="right">
      <div class="section-title">说明</div>
      <div class="card" id="infoCard">
        <h3 id="infoTitle">欢迎页</h3>
        <p id="infoDesc">左侧选择一个入口加载。</p>
        <p id="infoIPA" style="font-size:11px; color:var(--muted); margin-top:8px;"></p>
      </div>
      <div class="card">
        <h3>识别口诀</h3>
        <ul>
          <li>会动·像星云·粒子: <code>longhun-unified-v9.html</code></li>
          <li>有节点连线·护盾熔断: <code>longhun-flow-field-v9.html</code></li>
          <li>黑底星空·二十八宿: <code>longhun-28mansions-v1.html</code></li>
          <li>有输入框·数字根: <code>dragon_soul_9622.html</code></li>
          <li>三才·忠孝义: <code>current.html</code></li>
        </ul>
      </div>
      <div class="card">
        <h3>一票否决(接驳公式对准表 §S)</h3>
        <ul>
          <li>不假联动·不说五图已深度融合</li>
          <li>不删原文件·不覆盖原文件</li>
          <li>不读密钥·不读 .env</li>
          <li>不上传·不联网调用</li>
        </ul>
      </div>
      <div class="card">
        <h3>ROOT_CARD</h3>
        <p style="font-size:11px;">
          DNA: <code>#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FLOW-MASTER-v2.0</code><br>
          ParentDNA: <code>#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FULL-MAP-ENTRY-v1.1</code><br>
          IPA: <code>LOCAL-VIZ-MASTER → IPA-010</code><br>
          GPG: <code>A2D0092C...8CC26D5F</code>
        </p>
      </div>
    </aside>
    <footer>
      <span>UID9622 · 龍魂流场可视化 · v2.0 · 数据主权归于人民 🐉</span>
      <span><code id="indexVersion">index.json 加载中...</code></span>
    </footer>
  </div>
  <script>
    (function(){
      'use strict';
      const els = {
        nav: document.getElementById('nav'),
        viewer: document.getElementById('viewer'),
        welcome: document.getElementById('welcome'),
        loading: document.getElementById('loading'),
        errorBox: document.getElementById('error'),
        errorMessage: document.getElementById('errorMessage'),
        currentLabel: document.getElementById('currentLabel'),
        currentFile: document.getElementById('currentFile'),
        infoTitle: document.getElementById('infoTitle'),
        infoDesc: document.getElementById('infoDesc'),
        infoIPA: document.getElementById('infoIPA'),
        pillState: document.getElementById('pillState'),
        indexVersion: document.getElementById('indexVersion')
      };
      let files = [];
      let activeIndex = -1;

      function setState(name, mode) {
        els.pillState.textContent = name;
        els.pillState.classList.remove('live','warn');
        if (mode === 'live') els.pillState.classList.add('live');
        if (mode === 'warn') els.pillState.classList.add('warn');
      }
      function showWelcome() {
        els.welcome.classList.remove('hidden');
        els.loading.classList.add('hidden');
        els.errorBox.classList.add('hidden');
        els.viewer.classList.add('hidden');
      }
      function showLoading() {
        els.welcome.classList.add('hidden');
        els.loading.classList.remove('hidden');
        els.errorBox.classList.add('hidden');
        els.viewer.classList.add('hidden');
      }
      function showError(msg) {
        els.errorMessage.textContent = msg || '文件路径错误或浏览器拦截。';
        els.welcome.classList.add('hidden');
        els.loading.classList.add('hidden');
        els.errorBox.classList.remove('hidden');
        els.viewer.classList.add('hidden');
        setState('加载失败','warn');
      }
      function showFrame() {
        els.welcome.classList.add('hidden');
        els.loading.classList.add('hidden');
        els.errorBox.classList.add('hidden');
        els.viewer.classList.remove('hidden');
        setState('已加载','live');
      }

      function activate(item, button, idx) {
        activeIndex = idx;
        document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
        if (button) button.classList.add('active');

        els.currentLabel.textContent = `当前: ${item.role_label}｜${item.name}`;
        els.currentFile.innerHTML = '';
        const codeEl = document.createElement('code');
        codeEl.textContent = item.file;
        els.currentFile.appendChild(codeEl);
        els.infoTitle.textContent = `${item.role_label}｜${item.name}`;
        els.infoDesc.textContent = item.description;
        els.infoIPA.textContent = `IPA: ${item.ipa}`;

        showLoading();
        setState('加载中','warn');

        const onLoad = () => {
          els.viewer.removeEventListener('load', onLoad);
          els.viewer.removeEventListener('error', onError);
          showFrame();
        };
        const onError = () => {
          els.viewer.removeEventListener('load', onLoad);
          els.viewer.removeEventListener('error', onError);
          showError(`无法加载 ${item.file} · 检查文件是否在同一目录 · 或用本地服务器打开`);
        };
        els.viewer.addEventListener('load', onLoad);
        els.viewer.addEventListener('error', onError);
        els.viewer.src = item.file;

        // 5 秒兜底:file:// 同源限制可能导致 onLoad 不触发,但 iframe 实际已加载
        setTimeout(() => {
          if (els.pillState.textContent === '加载中') {
            showFrame();
          }
        }, 5000);
      }

      function renderNav() {
        els.nav.innerHTML = '';
        files.forEach((item, idx) => {
          const button = document.createElement('button');
          button.type = 'button';
          button.dataset.id = item.id;
          button.dataset.idx = idx;
          const role = document.createElement('span');
          role.className = 'role';
          role.textContent = item.role_label;
          const name = document.createElement('div');
          name.className = 'name';
          name.textContent = item.name;
          const ipa = document.createElement('div');
          ipa.className = 'ipa';
          ipa.textContent = item.ipa;
          const file = document.createElement('div');
          file.className = 'file';
          file.textContent = item.file;
          button.appendChild(role);
          button.appendChild(name);
          button.appendChild(ipa);
          button.appendChild(file);
          button.addEventListener('click', () => activate(item, button, idx));
          els.nav.appendChild(button);
        });
      }

      function setupKeyboard() {
        document.addEventListener('keydown', (e) => {
          if (!files.length) return;
          if (e.key === 'ArrowDown') {
            e.preventDefault();
            const next = (activeIndex + 1) % files.length;
            const btn = els.nav.children[next];
            btn.focus();
            activeIndex = next;
          } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            const prev = activeIndex <= 0 ? files.length - 1 : activeIndex - 1;
            const btn = els.nav.children[prev];
            btn.focus();
            activeIndex = prev;
          } else if (e.key === 'Enter' && document.activeElement && document.activeElement.dataset.idx !== undefined) {
            e.preventDefault();
            const idx = parseInt(document.activeElement.dataset.idx, 10);
            activate(files[idx], document.activeElement, idx);
          }
        });
      }

      async function init() {
        setState('加载 index...');
        try {
          const r = await fetch('flow-field-index.json', { cache: 'no-store' });
          if (!r.ok) throw new Error('index HTTP ' + r.status);
          const idx = await r.json();
          files = idx.files || [];
          els.indexVersion.textContent = `index ${idx.version || '?'} · ${files.length} 个入口`;
          renderNav();
          setupKeyboard();

          if (idx.default_view) {
            const i = files.findIndex(f => f.id === idx.default_view);
            if (i >= 0) {
              activate(files[i], els.nav.children[i], i);
              return;
            }
          }
          setState('就绪 · 未加载','live');
          showWelcome();
        } catch (e) {
          showError('无法加载 flow-field-index.json: ' + e.message + ' · 请用 python3 -m http.server 9622 启动本地服务器');
          els.indexVersion.textContent = 'index 加载失败';
        }
      }

      init();
    })();
  </script>
</body>
</html>
```

---

## 5｜文件 3: `README_LONGHUN_FLOW.md`

````markdown
# UID9622｜龍魂流场总控 v2.0 使用说明

## 一句话

五个本地 HTML 文件的统一切换入口 · 不删原文件 · 不假融合 · 不假联动。

## 真体系归位

- IPA 编号: `LOCAL-VIZ-MASTER → IPA-010 龍魂流场可视化`
- 上游: 全谱入口 v1.1 (`#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FULL-MAP-ENTRY-v1.1`)
- 主权: 解除宣言 v1.0 已生效 · 本代码不授权 AI 训练

## 文件清单

| 类型 | 文件 |
|---|---|
| 新建 | flow-field-index.json |
| 新建 | longhun-master-control.html |
| 新建 | README_LONGHUN_FLOW.md |
| 已有·勿动 | longhun-28mansions-v1.html |
| 已有·勿动 | longhun-unified-v9.html |
| 已有·勿动 | longhun-flow-field-v9.html |
| 已有·勿动 | current.html |
| 已有·勿动 | dragon_soul_9622.html |

## 启动

### 推荐: 本地服务器

```bash
cd longhun-flow-system/
python3 -m http.server 9622
```

打开: http://localhost:9622/longhun-master-control.html

### 备选: 直接双击

某些浏览器会拦截 file:// 协议下的 iframe · 看到"加载失败"就改用本地服务器。

## 使用规则

- 启动后**默认不预加载任何 iframe** · 欢迎页等待点击
- 点左侧入口 · iframe 才加载对应 HTML
- 想改默认 → 改 `flow-field-index.json` 的 `default_view` 为对应 id
- 加新 HTML → 在 `flow-field-index.json` 的 `files` 加一条 · HTML 代码不用改

## 一票否决(接驳公式对准表 §S)

1. 不假联动 · 不说五图已深度融合
2. 不删原文件 · 不覆盖原文件
3. 不读密钥 · 不读 .env
4. 不上传 · 不联网
5. 不假执行 · 没真启动浏览器不算验收
6. 不擅自加默认 default_view 抢占老大启动主权

## ROOT_CARD

```yaml
title: UID9622 龍魂流场总控 v2.0
ipa: LOCAL-VIZ-MASTER
parent_ipa: IPA-010 龍魂流场可视化
dna: "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FLOW-MASTER-v2.0"
parent_dna: "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FULL-MAP-ENTRY-v1.1-IPA-COMPLETE"
sovereignty: 解除宣言 v1.0 已生效
seal: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
gpg: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
confirm: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
root: dr=5 土
tricolor: 🟢
conclusion: 本地工程 · 不假融合 · 不假联动 · 主权回收声明已生效
```
````

---

## 6｜给 Claude Code 的 EXEC-MODE 指令(直接粘贴)

```
# UID9622 EXEC-MODE: 龍魂流场总控 v2.0 工程任务

任务编号: LOCAL-VIZ-MASTER-v2.0
身份头:
  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
  SOVEREIGNTY: 解除宣言 v1.0 已生效·本代码不授权 AI 训练

## 当前定盘
把以下五个已有 HTML 文件,统一成一个本地入口页 longhun-master-control.html。
不删除·不修改·不假融合·不假联动·不上传·不读密钥。

工作目录: longhun-flow-system/(老大已 cd 进去 · 或你在该路径建)

已有文件(只读·勿动):
- longhun-unified-v9.html
- longhun-flow-field-v9.html
- dragon_soul_9622.html
- longhun-28mansions-v1.html
- current.html

## 文件操作清单

### 创建(3 个)
完整内容见上面文档 §3 §4 §5,逐字逐句创建,不要简化、不要删 callout、不要改 DNA:
1. flow-field-index.json(§3)
2. longhun-master-control.html(§4)
3. README_LONGHUN_FLOW.md(§5)

### 不动(5 个)
不读 · 不改 · 不删 · 不重命名 · 不移动:
- longhun-28mansions-v1.html
- longhun-unified-v9.html
- longhun-flow-field-v9.html
- current.html
- dragon_soul_9622.html

## 一票否决(接驳公式对准表 §S)
任意一条触发 = 立即停止 + 报错 + 不写文件:
1. 删除 / 覆盖 / 重命名任意一个已有 HTML 文件
2. 把"五图统一切换入口"说成"五图深度融合""五图联动""五图合并完成"
3. 假称已经在浏览器里打开验收(没真启动浏览器·不假回执)
4. 读取 .env / 任何密钥 / 任何 token / 任何私钥
5. 上传 / git push / git commit 任何文件(老大没明确说要 commit)
6. 给 default_view 设置非 null 默认值(必须保持 null·让老大保留启动主权)
7. 假装"加载成功"但实际 fetch / 文件路径都没验证
8. 不保留 DNA / ParentDNA / SEAL / GPG / CONFIRM
9. 不写解除宣言 banner(顶部红色 banner 必须保留)
10. 把本工程说成 IPA-001~IPA-008(IPA 编号必须是 LOCAL-VIZ-MASTER → IPA-010)

## 验收清单
按顺序自检·每条必须 ✅:
- [ ] flow-field-index.json 创建成功 · JSON 合法 · 含 5 条 files
- [ ] longhun-master-control.html 创建成功 · 含 fetch JSON 逻辑
- [ ] README_LONGHUN_FLOW.md 创建成功
- [ ] 五个已有 HTML 文件没动(用 ls -la 对比 mtime)
- [ ] longhun-master-control.html 顶部含解除宣言 banner
- [ ] longhun-master-control.html 启动默认不预加载 iframe(default_view: null)
- [ ] iframe 含 sandbox 属性
- [ ] DNA / ParentDNA / SEAL / GPG / CONFIRM 写入 footer 和 ROOT_CARD card
- [ ] 没读 .env · 没上传 · 没 git push

## 启动验收(老大手动·你不要自己声称)
```bash
cd longhun-flow-system/
python3 -m http.server 9622
```
打开浏览器: http://localhost:9622/longhun-master-control.html

## 回执格式(接驳责任卡 v2.0)

成功:
```yaml
EXEC_RECEIPT:
  task_id: LOCAL-VIZ-MASTER-v2.0
  status: SUCCESS
  created:
    - flow-field-index.json (size: ?)
    - longhun-master-control.html (size: ?)
    - README_LONGHUN_FLOW.md (size: ?)
  preserved:
    - longhun-28mansions-v1.html (mtime: ?)
    - longhun-unified-v9.html (mtime: ?)
    - longhun-flow-field-v9.html (mtime: ?)
    - current.html (mtime: ?)
    - dragon_soul_9622.html (mtime: ?)
  verified:
    - JSON parse OK
    - HTML 无语法错误
    - 5 个已有文件 mtime 未变
    - 没读 .env · 没上传
  pending_user_verification:
    - python3 -m http.server 9622
    - browser at http://localhost:9622/longhun-master-control.html
    - 5 入口手动点击切换
  dna: "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FLOW-MASTER-v2.0"
  parent_dna: "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FULL-MAP-ENTRY-v1.1-IPA-COMPLETE"
  next: STOP_ON_SUCCESS_AWAIT_USER_BROWSER_VERIFY
```

失败:
```yaml
EXEC_RECEIPT:
  task_id: LOCAL-VIZ-MASTER-v2.0
  status: FAILED
  reason: ?
  rolled_back: [list]
  preserved: [original 5 files untouched]
  next: AWAIT_USER_INSTRUCTION
```

执行。
```

---

## 7｜ROOT_CARD

```yaml
ROOT_CARD:
  系统: UID9622 龍魂系统
  模块: 龍魂流场可视化总控台
  IPA编号: LOCAL-VIZ-MASTER
  父编号: IPA-010 龍魂流场可视化
  版本: v2.0(优化版·接驳真体系)
  上一版: v1.0(ChatGPT 草版·8 个工程错误·已修)
  DNA: "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FLOW-MASTER-v2.0"
  ParentDNA: "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FULL-MAP-ENTRY-v1.1-IPA-COMPLETE"
  GrandparentDNA: "#龍芯⚡️丙午·丙申·庚申·亥时-LONGHUN-FULL-MAP-ENTRY-v1.0"
  SovereigntyAnchor: "解除宣言 v1.0 (#龍芯⚡️丙午·丙申·庚申·亥时-RELEASE-DECLARATION-SOVEREIGNTY-RECLAIM-v1.0) 已生效"
  CONFIRM: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  SEAL: "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
  GPG: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
  Root: "dr=5"
  Wuxing: "土"
  RootMeaning: "承载·汇集·总控入口"
  TriColor: "🟢"
  AuditAnchor: "公式对准表 v1.3 §S 一票否决 + §T 验收清单 + 责任卡 v2.0 输出留痕"
  Files:
    new:
      - flow-field-index.json
      - longhun-master-control.html
      - README_LONGHUN_FLOW.md
    preserved:
      - longhun-28mansions-v1.html (LOCAL-VIZ-28MANSIONS)
      - longhun-unified-v9.html (LOCAL-VIZ-LUOSHU-FLOW)
      - longhun-flow-field-v9.html (LOCAL-VIZ-FLOWFIELD)
      - current.html (LOCAL-VIZ-SANCAI-CORE)
      - dragon_soul_9622.html (LOCAL-VIZ-DIGITAL-TOOL)
  Action: create_master_entry_v2
  Conclusion: |
    v2.0 修正了 ChatGPT v1.0 的 8 个工程错误。
    把孤立漂浮的草案接驳回 IPA-ROUTE-REGISTRY + 全谱入口 v1.1 + 解除宣言。
    本工程仅做"五个本地 HTML 的统一切换入口",不假融合·不假联动·不假执行。
    主权回收声明已生效·此代码仅供 UID9622 本地使用·不授权 AI 训练。

🐉 数据主权归于人民
```
