# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 龍魂多模型路由 v1.0
 * DNA: #龍芯⚡️丙午·辛未·MODEL-ROUTER-v1.0
 *
 * 功能:
 *   1. DeepSeek / Kimi / 本地模型 一键切换
 *   2. 根据任务类型自动选择模型
 *   3. 状态栏显示当前激活模型
 *   4. 敏感操作强制路由到本地模型
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

// ─── 类型 ────────────────────────────────────────────────

type ModelName = 'deepseek' | 'kimi' | 'local' | 'auto';
type TaskType = 'code_gen' | 'code_review' | 'sensitive' | 'general';

interface ModelConfig {
    name: ModelName;
    displayName: string;
    icon: string;
    color: string;
    description: string;
}

// ─── 常量 ────────────────────────────────────────────────

const MODELS: Record<string, ModelConfig> = {
    deepseek: {
        name: 'deepseek',
        displayName: 'DeepSeek',
        icon: '$(circuit-board)',
        color: '#4f9cf5',
        description: 'DeepSeek — 代码生成主力',
    },
    kimi: {
        name: 'kimi',
        displayName: 'Kimi',
        icon: '$(eye)',
        color: '#a855f7',
        description: 'Kimi — 代码审查与分析',
    },
    local: {
        name: 'local',
        displayName: '本地模型',
        icon: '$(server)',
        color: '#22c55e',
        description: '本地模型 — 敏感操作安全区',
    },
    auto: {
        name: 'auto',
        displayName: '自动路由',
        icon: '$(sync)',
        color: '#d4a843',
        description: '按任务类型自动选择模型',
    },
};

// 任务类型 → 默认模型映射
const DEFAULT_TASK_ROUTING: Record<TaskType, ModelName> = {
    code_gen: 'deepseek',
    code_review: 'kimi',
    sensitive: 'local',
    general: 'deepseek',
};

// ─── 状态栏 ──────────────────────────────────────────────

let statusBarItem: vscode.StatusBarItem;
let currentModel: ModelName = 'auto';

export function activate(context: vscode.ExtensionContext) {
    console.log('[龍魂多模型路由] 激活');

    // 读取当前配置
    const config = vscode.workspace.getConfiguration('longhun-model');
    const defaultModel = config.get<string>('defaultModel', 'auto') as ModelName;
    currentModel = defaultModel;

    // 状态栏
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 99);
    statusBarItem.command = 'longhun-model.showStatus';
    context.subscriptions.push(statusBarItem);
    updateStatusBar();

    // 注册命令
    context.subscriptions.push(
        vscode.commands.registerCommand('longhun-model.switchToDeepSeek', () => switchModel('deepseek')),
        vscode.commands.registerCommand('longhun-model.switchToKimi', () => switchModel('kimi')),
        vscode.commands.registerCommand('longhun-model.switchToLocal', () => switchModel('local')),
        vscode.commands.registerCommand('longhun-model.switchAuto', () => switchModel('auto')),
        vscode.commands.registerCommand('longhun-model.showStatus', showStatus),
    );
}

export function deactivate() {
    statusBarItem?.dispose();
}

// ─── 模型切换 ────────────────────────────────────────────

function switchModel(model: ModelName) {
    currentModel = model;
    updateStatusBar();

    const mc = MODELS[model];
    vscode.window.showInformationMessage(`${mc.icon} 已切换到 ${mc.displayName}`);

    // 写入本地路由配置文件
    writeRouteConfig(model);
}

function updateStatusBar() {
    const mc = MODELS[currentModel];
    statusBarItem.text = `${mc.icon} ${mc.displayName}`;
    statusBarItem.tooltip = `龍魂模型路由: ${mc.description}`;
    statusBarItem.color = mc.color;
    statusBarItem.show();
}

// ─── 任务路由 ────────────────────────────────────────────

function routeTask(taskType: TaskType): ModelName {
    if (currentModel !== 'auto') {
        return currentModel; // 手动指定，直接返回
    }

    const config = vscode.workspace.getConfiguration('longhun-model');
    switch (taskType) {
        case 'code_gen':
            return config.get<ModelName>('codeGenModel', 'deepseek');
        case 'code_review':
            return config.get<ModelName>('codeReviewModel', 'kimi');
        case 'sensitive':
            // 敏感操作强制本地
            const sensitiveModel = config.get<ModelName>('sensitiveModel', 'local');
            if (sensitiveModel !== 'local') {
                vscode.window.showWarningMessage('⚠️ 敏感操作建议使用本地模型，已自动切换');
            }
            return 'local';
        default:
            return DEFAULT_TASK_ROUTING[taskType] || 'deepseek';
    }
}

// ─── 命令：查看状态 ──────────────────────────────────────

function showStatus() {
    const config = vscode.workspace.getConfiguration('longhun-model');

    const panel = vscode.window.createWebviewPanel(
        'longhunModelStatus',
        '龍魂多模型路由状态',
        vscode.ViewColumn.One,
        { enableScripts: false }
    );

    const currentMc = MODELS[currentModel];
    const codeGenMc = MODELS[config.get<string>('codeGenModel', 'deepseek')];
    const reviewMc = MODELS[config.get<string>('codeReviewModel', 'kimi')];
    const sensitiveMc = MODELS[config.get<string>('sensitiveModel', 'local')];

    panel.webview.html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
:root { --bg: #0a0e17; --bg-card: #111827; --gold: #d4a843; --text: #e2e8f0; --text-dim: #94a3b8; --border: #1e293b; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--bg); color: var(--text); font-family: monospace; padding: 20px; }
h1 { color: var(--gold); margin-bottom: 16px; }
.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.card.active { border-color: var(--gold); }
.card-title { font-weight: 600; margin-bottom: 8px; font-size: 14px; }
.row { display: flex; justify-content: space-between; padding: 4px 0; font-size: 13px; }
.label { color: var(--text-dim); }
.value { font-weight: 600; }
.btn-row { display: flex; gap: 8px; margin-top: 16px; }
.btn { padding: 8px 16px; border-radius: 6px; border: 1px solid var(--border); background: var(--bg-card); color: var(--text); cursor: pointer; font-family: monospace; font-size: 13px; }
.btn:hover { border-color: var(--gold); }
.btn.primary { background: var(--gold); color: #000; border-color: var(--gold); }
</style>
</head>
<body>
<h1>🐉 龍魂多模型路由</h1>

<div class="card active">
    <div class="card-title">${currentMc.icon} 当前: ${currentMc.displayName}</div>
    <div class="row"><span class="label">模式</span><span class="value">${currentModel === 'auto' ? '自动路由（按任务类型）' : '手动指定'}</span></div>
    <div class="row"><span class="label">描述</span><span class="value">${currentMc.description}</span></div>
</div>

<div class="card">
    <div class="card-title">📋 任务路由表</div>
    <div class="row"><span class="label">代码生成</span><span class="value" style="color:${codeGenMc.color}">${codeGenMc.icon} ${codeGenMc.displayName}</span></div>
    <div class="row"><span class="label">代码审查</span><span class="value" style="color:${reviewMc.color}">${reviewMc.icon} ${reviewMc.displayName}</span></div>
    <div class="row"><span class="label">敏感操作</span><span class="value" style="color:${sensitiveMc.color}">${sensitiveMc.icon} ${sensitiveMc.displayName}</span></div>
</div>

<div class="card">
    <div class="card-title">🔑 API 密钥状态</div>
    <div class="row"><span class="label">DeepSeek</span><span class="value">${config.get<string>('deepseekApiKey') ? '✅ 已配置' : '⚠️ 未配置'}</span></div>
    <div class="row"><span class="label">Kimi</span><span class="value">${config.get<string>('kimiApiKey') ? '✅ 已配置' : '⚠️ 未配置'}</span></div>
    <div class="row"><span class="label">本地模型</span><span class="value">${config.get<string>('localModelPath') || '⚠️ 未配置'}</span></div>
</div>

<div class="btn-row">
    <button class="btn primary" onclick="switchModel('deepseek')">🔵 DeepSeek</button>
    <button class="btn primary" onclick="switchModel('kimi')">🟣 Kimi</button>
    <button class="btn primary" onclick="switchModel('local')">🟢 本地</button>
    <button class="btn primary" onclick="switchModel('auto')">🟡 自动</button>
</div>
</body>
</html>`;
}

// ─── 路由配置持久化 ──────────────────────────────────────

function writeRouteConfig(model: ModelName) {
    try {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';
        if (!workspaceRoot) return;

        const configDir = path.join(workspaceRoot, 'config');
        if (!fs.existsSync(configDir)) {
            fs.mkdirSync(configDir, { recursive: true });
        }

        const configPath = path.join(configDir, 'model_route.json');
        const config = {
            active_model: model,
            switched_at: new Date().toISOString(),
            routing_table: DEFAULT_TASK_ROUTING,
            dna: '#龍芯⚡️丙午·辛未·MODEL-ROUTE-CONFIG-v1.0',
        };

        fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf-8');
    } catch {
        // 静默
    }
}
