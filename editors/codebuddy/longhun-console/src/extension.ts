/**
 * 龍魂控制台 · CodeBuddy 侧边栏插件 v1.1.0
 * DNA: #龍芯⚡️丙午·辛未·CODEBUDDY-LONGHUN-CONSOLE-v1.1
 *
 * 功能:
 *   1. 侧边栏显示系统状态（DNA锚定、引擎数、人格状态、三色审计）
 *   2. 审计日志实时摘要
 *   3. 一键跳转终端执行 lh 命令
 *   4. 与本地服务联动（:9677 蚁群 / :9627 神经网络 / :8766 控制面板）
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { exec } from 'child_process';

interface SkillRegistry {
    _meta: any;
    public: SkillDef[];
    restricted: SkillDef[];
    internal: SkillDef[];
}

interface SkillDef {
    id: string;
    name: string;
    title: string;
    emoji: string;
    description: string;
    entry: string;
    command: string;
    category: string;
    license: string;
    reason?: string;
}

// ─── 技能注册表 ───────────────────────────────────────────

let SKILL_REGISTRY: SkillRegistry | null = null;

function loadSkillRegistry(): SkillRegistry | null {
    if (SKILL_REGISTRY) { return SKILL_REGISTRY; }
    const regPath = path.join(WORKSPACE_ROOT, 'editors/codebuddy/longhun-console/skills/public-skills.json');
    try {
        const raw = fs.readFileSync(regPath, 'utf-8');
        SKILL_REGISTRY = JSON.parse(raw) as SkillRegistry;
        return SKILL_REGISTRY;
    } catch (e) {
        console.log('[龍魂控制台] 无法加载技能注册表:', e);
        return null;
    }
}

function getSkillByCommand(command: string): SkillDef | undefined {
    const reg = loadSkillRegistry();
    if (!reg) { return undefined; }
    return reg.public.find(s => s.command === command)
        || reg.restricted.find(s => s.command === command)
        || reg.internal.find(s => s.command === command);
}

function getAllPublicSkills(): SkillDef[] {
    const reg = loadSkillRegistry();
    return reg ? reg.public : [];
}

function runSkill(skill: SkillDef) {
    const terminal = vscode.window.createTerminal(`龍魂 ${skill.name}`);
    terminal.show();
    // 展开 home 目录
    const entry = skill.entry.replace('~/', process.env.HOME + '/');
    terminal.sendText(`cd "${WORKSPACE_ROOT}" && ${entry}`);
}

function runSkillWithInput(skill: SkillDef) {
    if (skill.entry.includes('$1') || skill.entry.includes('{}')) {
        vscode.window.showInputBox({ prompt: `输入 ${skill.name} 的参数` }).then(input => {
            if (input === undefined) { return; }
            const cmd = skill.entry.replace('~/', process.env.HOME + '/').replace('$1', input).replace('{}', input);
            const terminal = vscode.window.createTerminal(`龍魂 ${skill.name}`);
            terminal.show();
            terminal.sendText(`cd "${WORKSPACE_ROOT}" && ${cmd}`);
        });
    } else {
        runSkill(skill);
    }
}


interface SystemStatus {
    dna: string;
    timestamp: string;
    personas: { total: number; active: number; red: number };
    engines: { total: number; online: number };
    audit: { green: number; yellow: number; red: number };
    antColony: { port: number; alive: boolean; tick?: number; E?: number };
    neuralNet: { port: number; alive: boolean };
    dashboard: { port: number; alive: boolean };
    services: { name: string; port: number; alive: boolean }[];
}

interface AuditLogEntry {
    timestamp: string;
    action: string;
    level: 'green' | 'yellow' | 'red';
    source: string;
    dna: string;
    hash: string;
}

// ─── 常量 ───────────────────────────────────────────────

const WORKSPACE_ROOT = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || process.env.HOME + '/longhun-system';
const NEURAL_NET_PATH = path.join(WORKSPACE_ROOT, '.codebuddy', 'longhun_neural_net.json');
const AUDIT_LOG_PATH = path.join(WORKSPACE_ROOT, 'logs', 'action_log.jsonl');
const LH_BIN = path.join(WORKSPACE_ROOT, 'bin', 'lh.py');

const SERVICE_PORTS: Record<string, number> = {
    'ant_colony': 9677,
    'neural_net': 9627,
    'dashboard': 8766,
    'symbiote': 9627,
};

// ─── 激活入口 ────────────────────────────────────────────

export function activate(context: vscode.ExtensionContext) {
    console.log('[龍魂控制台] 激活');

    // 注册 WebView Provider
    const provider = new LongHunViewProvider(context.extensionUri);
    context.subscriptions.push(
        vscode.window.registerWebviewViewProvider('longhun-console.mainView', provider)
    );

    // 注册命令
    context.subscriptions.push(
        vscode.commands.registerCommand('longhun-console.runLhCommand', runLhCommand),
        vscode.commands.registerCommand('longhun-console.openDashboard', () => openUrl(`http://127.0.0.1:${SERVICE_PORTS.dashboard}`)),
        vscode.commands.registerCommand('longhun-console.openAntColony', () => openUrl(`http://127.0.0.1:${SERVICE_PORTS.ant_colony}/dashboard`)),
        vscode.commands.registerCommand('longhun-console.quickAudit', quickAudit),
        vscode.commands.registerCommand('longhun-console.toggleDevPanel', () => {
            vscode.commands.executeCommand('workbench.action.toggleDevTools');
        }),
        vscode.commands.registerCommand('longhun-console.openSkillMatrix', () => {
            provider.openSkillPanel();
        }),
        vscode.commands.registerCommand('longhun-console.checkUpdate', () => {
            checkForUpdate(provider);
        })
    );

    // 动态注册公开技能命令
    const registry = loadSkillRegistry();
    if (registry) {
        const all = [
            ...registry.public,
            ...registry.restricted,
            ...registry.internal
        ];
        for (const skill of all) {
            const cmdId = `longhun-console.skill.${skill.command}`;
            context.subscriptions.push(
                vscode.commands.registerCommand(cmdId, () => {
                    if (registry.restricted.some(s => s.command === skill.command)) {
                        vscode.window.showWarningMessage(
                            `${skill.title} 为受限技能：${skill.reason}`,
                            '仍要执行', '取消'
                        ).then(choice => {
                            if (choice === '仍要执行') { runSkillWithInput(skill); }
                        });
                    } else if (registry.internal.some(s => s.command === skill.command)) {
                        vscode.window.showInformationMessage(`${skill.title} 为内部技能，不对外暴露`);
                    } else {
                        runSkillWithInput(skill);
                    }
                })
            );
        }
    }

    // 启动时自动探测服务状态
    probeServices().then(status => {
        provider.updateStatus(status);
    });

    // 每 30 秒自动刷新
    const interval = setInterval(async () => {
        const status = await probeServices();
        provider.updateStatus(status);
    }, 30000);
    context.subscriptions.push({ dispose: () => clearInterval(interval) });
}

export function deactivate() {
    console.log('[龍魂控制台] 停用');
}

// ─── WebView Provider ────────────────────────────────────

class LongHunViewProvider implements vscode.WebviewViewProvider {
    private _view?: vscode.WebviewView;

    constructor(private readonly _extensionUri: vscode.Uri) {}

    resolveWebviewView(webviewView: vscode.WebviewView) {
        this._view = webviewView;
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this._extensionUri],
        };
        webviewView.webview.html = this._getHtml();
        webviewView.webview.onDidReceiveMessage(async (msg) => {
            await this._handleMessage(msg);
        });
    }

    updateStatus(status: SystemStatus) {
        if (this._view) {
            this._view.webview.postMessage({ type: 'status', data: status });
        }
    }

    openSkillPanel() {
        if (this._view) {
            const skills = getAllPublicSkills();
            this._view.webview.postMessage({ type: 'skillPanel', data: skills });
        } else {
            vscode.window.showInformationMessage('请先打开龍魂控制台侧边栏');
        }
    }

    showUpdateResult(data: any) {
        if (this._view) {
            this._view.webview.postMessage({ type: 'updateStatus', data });
        }
    }

    private async _handleMessage(msg: any) {
        switch (msg.type) {
            case 'refresh':
                const status = await probeServices();
                this.updateStatus(status);
                break;
            case 'runLh':
                runLhCommand();
                break;
            case 'openUrl':
                openUrl(msg.url);
                break;
            case 'getAuditLogs':
                const logs = await readAuditLogs(20);
                this._view?.webview.postMessage({ type: 'auditLogs', data: logs });
                break;
            case 'runSkill':
                const s = getSkillByCommand(msg.command);
                if (s) { runSkillWithInput(s); }
                break;
            case 'loadSkills':
                const pubSkills = getAllPublicSkills();
                this._view?.webview.postMessage({ type: 'skillPanel', data: pubSkills });
                break;
            case 'checkUpdate':
                checkForUpdate(this);
                break;
        }
    }

    private _getHtml(): string {
        return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>龍魂控制台</title>
<style>
:root {
    --bg: #0a0e17;
    --bg-card: #111827;
    --gold: #d4a843;
    --gold-dim: #8b6914;
    --green: #22c55e;
    --yellow: #eab308;
    --red: #ef4444;
    --text: #e2e8f0;
    --text-dim: #94a3b8;
    --border: #1e293b;
    --font: 'SF Mono', 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', monospace;
    --blue: #3b82f6;
    --purple: #a855f7;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    font-size: 12px;
    line-height: 1.5;
    padding: 12px;
    overflow-y: auto;
}
.header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border);
}
.header .logo {
    font-size: 18px;
}
.header .title {
    font-size: 14px;
    font-weight: 700;
    color: var(--gold);
}
.header .dna {
    font-size: 10px;
    color: var(--text-dim);
    word-break: break-all;
}
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px;
    margin-bottom: 8px;
}
.card-title {
    font-size: 11px;
    font-weight: 600;
    color: var(--gold-dim);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 3px 0;
}
.label { color: var(--text-dim); }
.value { font-weight: 600; }
.value.green { color: var(--green); }
.value.yellow { color: var(--yellow); }
.value.red { color: var(--red); }
.value.gold { color: var(--gold); }

.btn-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 8px;
}
.btn {
    background: var(--bg-card);
    border: 1px solid var(--border);
    color: var(--text);
    padding: 4px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 11px;
    font-family: var(--font);
    transition: all 0.2s;
}
.btn:hover { border-color: var(--gold); color: var(--gold); }
.btn.primary { background: var(--gold); color: #000; border-color: var(--gold); font-weight: 600; }
.btn.primary:hover { background: #c49a3c; }
.btn.blue { border-color: var(--blue); color: var(--blue); }
.btn.blue:hover { background: rgba(59, 130, 246, 0.1); color: #60a5fa; }
.btn.purple { border-color: var(--purple); color: var(--purple); }
.btn.purple:hover { background: rgba(168, 85, 247, 0.1); color: #c084fc; }

.skill-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 6px;
}
.skill-item {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 6px 8px;
    cursor: pointer;
    transition: all 0.2s;
}
.skill-item:hover {
    border-color: var(--gold);
}
.skill-icon {
    font-size: 14px;
    width: 22px;
    text-align: center;
}
.skill-info {
    flex: 1;
    min-width: 0;
}
.skill-name {
    font-weight: 600;
    font-size: 11px;
    color: var(--text);
}
.skill-desc {
    font-size: 10px;
    color: var(--text-dim);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.skill-cat {
    font-size: 9px;
    padding: 2px 5px;
    border-radius: 3px;
    background: rgba(212, 168, 67, 0.1);
    color: var(--gold-dim);
    border: 1px solid var(--gold-dim);
}
.skill-empty {
    color: var(--text-dim);
    font-size: 11px;
    text-align: center;
    padding: 12px 0;
}
.skill-section {
    display: none;
}
.skill-section.visible {
    display: block;
}
.category-row {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-bottom: 8px;
}
.cat-filter {
    font-size: 9px;
    padding: 2px 6px;
    border-radius: 3px;
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--text-dim);
    cursor: pointer;
}
.cat-filter:hover, .cat-filter.active {
    border-color: var(--gold);
    color: var(--gold);
}
.audit-item {
    padding: 4px 0;
    border-bottom: 1px solid var(--border);
    font-size: 11px;
}
.audit-item:last-child { border-bottom: none; }
.audit-level {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 6px;
}
.audit-level.green { background: var(--green); }
.audit-level.yellow { background: var(--yellow); }
.audit-level.red { background: var(--red); }
.audit-ts { color: var(--text-dim); font-size: 10px; }

.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 4px;
}
.status-dot.alive { background: var(--green); box-shadow: 0 0 6px var(--green); }
.status-dot.dead { background: var(--red); }

.footer {
    text-align: center;
    color: var(--text-dim);
    font-size: 10px;
    margin-top: 12px;
    padding-top: 8px;
    border-top: 1px solid var(--border);
}
</style>
</head>
<body>

<div class="header">
    <span class="logo">🐉</span>
    <div>
        <div class="title">龍魂控制台</div>
        <div class="dna" id="dnaDisplay">加载中...</div>
    </div>
</div>

<div class="card">
    <div class="card-title">📡 服务状态</div>
    <div id="servicesStatus">探测中...</div>
</div>

<div class="card">
    <div class="card-title">🧠 系统快照</div>
    <div id="systemSnapshot">加载中...</div>
</div>

<div class="card">
    <div class="card-title">🛡️ 三色审计</div>
    <div id="auditSummary">加载中...</div>
</div>

<div class="card">
    <div class="card-title">📋 最近审计日志</div>
    <div id="auditLogs" style="max-height: 200px; overflow-y: auto;">点击刷新...</div>
</div>

<div class="card">
    <div class="card-title">🧰 技能矩阵</div>
    <div class="category-row" id="skillFilters">
        <span class="cat-filter active" data-cat="all">全部</span>
    </div>
    <div class="skill-grid" id="skillGrid" style="display: none;">
        <div class="skill-empty">点击展开技能矩阵</div>
    </div>
    <div class="skill-empty" id="skillHint" style="display: block;">点击「技能矩阵」展开龍魂公开技能</div>
</div>

<div class="btn-row">
    <button class="btn primary" onclick="runLh()">🖥️ lh 命令</button>
    <button class="btn" onclick="openDashboard()">📊 总控面板</button>
    <button class="btn" onclick="openAntColony()">🐜 蚁群控制台</button>
    <button class="btn blue" onclick="toggleSkills()">🧰 技能矩阵</button>
    <button class="btn purple" onclick="checkUpdate()">🔄 自动更新</button>
    <button class="btn" onclick="refresh()">🔄 刷新</button>
    <button class="btn" onclick="loadAuditLogs()">📋 加载日志</button>
</div>

<div class="footer">
    #龍芯⚡️丙午·辛未 · UID9622 · v1.1.0
</div>

<script>
const vscode = acquireVsCodeApi();

// 接收来自扩展的消息
window.addEventListener('message', (e) => {
    const msg = e.data;
    switch (msg.type) {
        case 'status':
            renderStatus(msg.data);
            break;
        case 'auditLogs':
            renderAuditLogs(msg.data);
            break;
        case 'skillPanel':
            renderSkills(msg.data);
            break;
        case 'updateStatus':
            showUpdateStatus(msg.data);
            break;
    }
});

function post(msg) { vscode.postMessage(msg); }

function refresh() { post({ type: 'refresh' }); }
function runLh() { post({ type: 'runLh' }); }
function openDashboard() { post({ type: 'openUrl', url: 'http://127.0.0.1:8766' }); }
function openAntColony() { post({ type: 'openUrl', url: 'http://127.0.0.1:9677/dashboard' }); }
function loadAuditLogs() { post({ type: 'getAuditLogs' }); }

function renderStatus(s) {
    document.getElementById('dnaDisplay').textContent = s.dna || '未锚定';

    // 服务状态
    let svcHtml = '';
    if (s.services) {
        for (const svc of s.services) {
            const dot = svc.alive ? 'alive' : 'dead';
            const text = svc.alive ? '在线' : '离线';
            svcHtml += '<div class="row"><span class="label"><span class="status-dot ' + dot + '"></span>' + svc.name + '</span><span class="value ' + (svc.alive ? 'green' : 'red') + '">' + text + ' :' + svc.port + '</span></div>';
        }
    }
    document.getElementById('servicesStatus').innerHTML = svcHtml || '无服务数据';

    // 系统快照
    const ant = s.antColony || {};
    let snapHtml = '';
    snapHtml += '<div class="row"><span class="label">人格矩阵</span><span class="value green">' + (s.personas?.active || 0) + '/' + (s.personas?.total || 0) + ' 满编</span></div>';
    snapHtml += '<div class="row"><span class="label">引擎</span><span class="value">' + (s.engines?.total || 0) + '</span></div>';
    snapHtml += '<div class="row"><span class="label">蚁群 tick</span><span class="value gold">' + (ant.tick || '-') + '</span></div>';
    snapHtml += '<div class="row"><span class="label">涌现 E</span><span class="value gold">' + (ant.E != null ? ant.E.toFixed(4) : '-') + '</span></div>';
    snapHtml += '<div class="row"><span class="label">红色人格</span><span class="value ' + ((s.personas?.red || 0) > 0 ? 'red' : 'green') + '">' + (s.personas?.red || 0) + '</span></div>';
    document.getElementById('systemSnapshot').innerHTML = snapHtml;

    // 审计摘要
    const a = s.audit || {};
    let auditHtml = '';
    auditHtml += '<div class="row"><span class="label">🟢 绿</span><span class="value green">' + (a.green || 0) + '</span></div>';
    auditHtml += '<div class="row"><span class="label">🟡 黄</span><span class="value yellow">' + (a.yellow || 0) + '</span></div>';
    auditHtml += '<div class="row"><span class="label">🔴 红</span><span class="value red">' + (a.red || 0) + '</span></div>';
    document.getElementById('auditSummary').innerHTML = auditHtml;
}

function renderAuditLogs(logs) {
    if (!logs || logs.length === 0) {
        document.getElementById('auditLogs').innerHTML = '<div style="color:var(--text-dim)">暂无日志</div>';
        return;
    }
    let html = '';
    for (const l of logs) {
        const levelClass = l.level === 'green' ? 'green' : l.level === 'yellow' ? 'yellow' : 'red';
        html += '<div class="audit-item">';
        html += '<span class="audit-level ' + levelClass + '"></span>';
        html += '<span>' + esc(l.action) + '</span>';
        html += '<span class="audit-ts" style="float:right">' + esc(l.timestamp) + '</span>';
        html += '</div>';
    }
    document.getElementById('auditLogs').innerHTML = html;
}

function esc(s) { return (s || '').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function escJs(s) { return (s || '').replace(/'/g, "\\'").replace(/"/g, '&quot;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

// 首次加载
refresh();
setTimeout(() => loadAuditLogs(), 1000);
setTimeout(() => loadSkills(), 500);

let allSkills = [];

function toggleSkills() {
    const grid = document.getElementById('skillGrid');
    const hint = document.getElementById('skillHint');
    if (grid.style.display === 'none') {
        grid.style.display = 'grid';
        hint.style.display = 'none';
        loadSkills();
    } else {
        grid.style.display = 'none';
        hint.style.display = 'block';
    }
}

function loadSkills() { post({ type: 'loadSkills' }); }

function renderSkills(skills) {
    allSkills = skills || [];
    const grid = document.getElementById('skillGrid');
    const filters = document.getElementById('skillFilters');
    if (!grid) { return; }
    if (!allSkills.length) {
        grid.innerHTML = '<div class="skill-empty">未加载技能注册表</div>';
        return;
    }

    // 分类过滤器
    const cats = ['all', ...new Set(allSkills.map(s => s.category))];
    filters.innerHTML = cats.map(c => '<span class="cat-filter ' + (c === 'all' ? 'active' : '') + '" data-cat="' + c + '" onclick="filterSkills(\'' + escJs(c) + '\')">' + (c === 'all' ? '全部' : esc(c)) + '</span>').join('');

    renderSkillGrid(allSkills);
}

function filterSkills(cat) {
    document.querySelectorAll('.cat-filter').forEach(el => el.classList.remove('active'));
    var active = document.querySelector('.cat-filter[data-cat="' + cat + '"]');
    if (active) { active.classList.add('active'); }
    const list = cat === 'all' ? allSkills : allSkills.filter(s => s.category === cat);
    renderSkillGrid(list);
}

function renderSkillGrid(skills) {
    const grid = document.getElementById('skillGrid');
    grid.innerHTML = skills.map(function(s) {
        return '<div class="skill-item" onclick="runSkill(\'' + escJs(s.command) + '\')">' +
            '<span class="skill-icon">' + esc(s.emoji) + '</span>' +
            '<div class="skill-info">' +
            '<div class="skill-name">' + esc(s.name) + '</div>' +
            '<div class="skill-desc">' + esc(s.description) + '</div>' +
            '</div>' +
            '<span class="skill-cat">' + esc(s.category) + '</span>' +
            '</div>';
    }).join('');
}

function runSkill(command) { post({ type: 'runSkill', command }); }
function checkUpdate() { post({ type: 'checkUpdate' }); }

function showUpdateStatus(data) {
    var msg = '';
    if (data.hasUpdate) {
        msg = '[龍魂] 发现新版本 v' + data.latest + ' (当前 v' + data.current + ')\\n' + data.changelog + '\\n下载地址: ' + data.url;
        vscode.postMessage({ type: 'openUrl', url: data.url });
    } else {
        msg = '[龍魂] 已是最新版本 v' + data.current;
    }
    // show a simple notification
    var el = document.createElement('div');
    el.style.cssText = 'position:fixed;top:10px;right:10px;background:var(--bg-card);border:1px solid var(--gold);color:var(--gold);padding:8px 12px;border-radius:4px;z-index:9999;font-size:11px;';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(function() { el.remove(); }, 5000);
}
</script>
</body>
</html>`;
    }
}

// ─── 命令实现 ────────────────────────────────────────────

async function runLhCommand() {
    const cmd = await vscode.window.showInputBox({
        prompt: '输入 lh 命令参数（如: status / health / audit / ant status）',
        placeHolder: 'status'
    });
    if (!cmd) { return; }

    const terminal = vscode.window.createTerminal('龍魂 lh');
    terminal.show();
    terminal.sendText(`cd "${WORKSPACE_ROOT}" && python3 bin/lh.py ${cmd}`);
}

async function quickAudit() {
    const terminal = vscode.window.createTerminal('龍魂审计');
    terminal.show();
    terminal.sendText(`cd "${WORKSPACE_ROOT}" && python3 bin/lh.py audit`);
}

function openUrl(url: string) {
    vscode.env.openExternal(vscode.Uri.parse(url));
}

// ─── 自动更新检查 ──────────────────────────────────────────

const UPDATE_URL = 'https://raw.githubusercontent.com/uid9622/longhun-system/main/editors/codebuddy/longhun-console/update.json';
const CURRENT_VERSION = '1.1.0';

async function checkForUpdate(provider: LongHunViewProvider) {
    try {
        const https = require('https') as typeof import('https');
        const result = await new Promise<{ version: string; url: string; changelog: string }>((resolve, reject) => {
            https.get(UPDATE_URL, { timeout: 5000 }, (res: any) => {
                let data = '';
                res.on('data', (chunk: string) => { data += chunk; });
                res.on('end', () => {
                    try { resolve(JSON.parse(data)); }
                    catch (e) { reject(e); }
                });
                res.on('error', reject);
            }).on('error', reject);
        });

        const hasUpdate = compareVersions(result.version, CURRENT_VERSION) > 0;
        provider.showUpdateResult({
            hasUpdate,
            current: CURRENT_VERSION,
            latest: result.version,
            url: result.url,
            changelog: result.changelog || ''
        });

        if (hasUpdate) {
            const choice = await vscode.window.showInformationMessage(
                `龍魂控制台新版本 v${result.version} 可用 (当前 v${CURRENT_VERSION})`,
                '下载更新', '稍后再说'
            );
            if (choice === '下载更新') {
                vscode.env.openExternal(vscode.Uri.parse(result.url));
            }
        } else {
            vscode.window.showInformationMessage(`龍魂控制台已是最新版本 v${CURRENT_VERSION}`);
        }
    } catch (e: any) {
        vscode.window.showWarningMessage(`龍魂更新检查失败: ${e.message || '网络不可达'}`);
        provider.showUpdateResult({
            hasUpdate: false, current: CURRENT_VERSION, latest: '', url: '', changelog: '', error: e.message
        });
    }
}

function compareVersions(a: string, b: string): number {
    const pa = a.split('.').map(Number);
    const pb = b.split('.').map(Number);
    for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
        const diff = (pa[i] || 0) - (pb[i] || 0);
        if (diff !== 0) { return diff; }
    }
    return 0;
}

// ─── 服务探测 ────────────────────────────────────────────

async function probeServices(): Promise<SystemStatus> {
    const status: SystemStatus = {
        dna: '',
        timestamp: new Date().toISOString(),
        personas: { total: 16, active: 16, red: 0 },
        engines: { total: 122, online: 0 },
        audit: { green: 0, yellow: 0, red: 0 },
        antColony: { port: SERVICE_PORTS.ant_colony, alive: false },
        neuralNet: { port: SERVICE_PORTS.neural_net, alive: false },
        dashboard: { port: SERVICE_PORTS.dashboard, alive: false },
        services: [],
    };

    // 1. 读取神经网络拓扑获取 DNA
    try {
        const nnRaw = fs.readFileSync(NEURAL_NET_PATH, 'utf-8');
        const nn = JSON.parse(nnRaw);
        status.dna = nn._meta?.dna || '';
        status.personas.total = nn.persona_matrix?.total || 16;
        status.personas.active = nn.persona_matrix?.active || 16;
        status.personas.red = nn.persona_matrix?.red || 0;
        status.engines.total = nn.engine_index?.total || 122;
    } catch {
        status.dna = '#龍芯⚡️拓扑加载失败';
    }

    // 2. 并行探测所有服务端口
    const probes = Object.entries(SERVICE_PORTS).map(async ([name, port]) => {
        const alive = await httpProbe(port);
        return { name, port, alive };
    });

    const results = await Promise.all(probes);
    status.services = results;

    for (const r of results) {
        switch (r.name) {
            case 'ant_colony':
                status.antColony.alive = r.alive;
                if (r.alive) {
                    try {
                        const resp = await httpGet(`http://127.0.0.1:${r.port}/config`);
                        if (resp) {
                            const config = JSON.parse(resp);
                            status.antColony.tick = config.tick_count;
                            status.antColony.E = config.emergence_E;
                        }
                    } catch { /* 忽略配置读取错误 */ }
                }
                break;
            case 'neural_net':
                status.neuralNet.alive = r.alive;
                break;
            case 'dashboard':
                status.dashboard.alive = r.alive;
                break;
        }
    }

    // 3. 读取审计日志摘要
    try {
        const logs = await readAuditLogs(100);
        for (const log of logs) {
            if (log.level === 'green') status.audit.green++;
            else if (log.level === 'yellow') status.audit.yellow++;
            else status.audit.red++;
        }
    } catch { /* 忽略 */ }

    return status;
}

function httpProbe(port: number): Promise<boolean> {
    return new Promise((resolve) => {
        const timeout = setTimeout(() => resolve(false), 2000);
        httpGet(`http://127.0.0.1:${port}/health`)
            .then(() => { clearTimeout(timeout); resolve(true); })
            .catch(() => { clearTimeout(timeout); resolve(false); });
    });
}

function httpGet(url: string): Promise<string> {
    return new Promise((resolve, reject) => {
        const http = url.startsWith('https') ? require('https') : require('http');
        http.get(url, { timeout: 2000 }, (res: any) => {
            let data = '';
            res.on('data', (chunk: string) => { data += chunk; });
            res.on('end', () => resolve(data));
            res.on('error', reject);
        }).on('error', reject);
    });
}

// ─── 审计日志读取 ────────────────────────────────────────

async function readAuditLogs(limit: number): Promise<AuditLogEntry[]> {
    const entries: AuditLogEntry[] = [];
    try {
        if (!fs.existsSync(AUDIT_LOG_PATH)) return entries;
        const content = fs.readFileSync(AUDIT_LOG_PATH, 'utf-8');
        const lines = content.trim().split('\n');
        // 取最后 limit 条
        const recent = lines.slice(-limit);
        for (const line of recent) {
            try {
                const entry = JSON.parse(line);
                entries.push({
                    timestamp: entry.timestamp || entry.ts || '',
                    action: entry.action || entry.operation || entry.cmd || '',
                    level: entry.level || entry.audit_level || 'green',
                    source: entry.source || entry.engine || '',
                    dna: entry.dna || '',
                    hash: entry.hash || entry.chain_hash || '',
                });
            } catch { /* 跳过无效行 */ }
        }
    } catch { /* 忽略 */ }
    return entries.reverse();
}
