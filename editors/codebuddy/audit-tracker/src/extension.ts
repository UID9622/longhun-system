/**
 * 龍魂审计追踪插件 v1.0
 * DNA: #龍芯⚡️丙午·辛未·AUDIT-TRACKER-v1.0
 *
 * 功能:
 *   1. AI 生成代码自动审计 — 粘贴/保存时检测并记录
 *   2. 记录模型来源、提示词哈希、生成时间、审核结果
 *   3. 写入本地审计日志（JSONL），不上传云端
 *   4. 状态栏显示审计计数
 *   5. 一键生成审计报告
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import * as crypto from 'crypto';

// ─── 类型 ────────────────────────────────────────────────

interface AuditEntry {
    id: string;
    timestamp: string;
    model_source: string;
    prompt_hash: string;
    code_hash: string;
    file_path: string;
    line_start: number;
    line_end: number;
    code_snippet_preview: string;
    review_status: 'pending' | 'reviewed' | 'rejected';
    review_timestamp?: string;
    reviewer?: string;
    notes?: string;
    dna: string;
}

interface AuditStats {
    total: number;
    pending: number;
    reviewed: number;
    rejected: number;
    today: number;
}

// ─── 常量 ────────────────────────────────────────────────

const DNA = '#龍芯⚡️丙午·辛未·AUDIT-TRACKER-v1.0';
const WORKSPACE_ROOT = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '';
const DEFAULT_AUDIT_LOG = path.join(WORKSPACE_ROOT, 'logs', 'ai_audit.jsonl');

// AI 代码特征标记（常见的 AI 生成代码特征）
const AI_MARKERS = [
    /\/\/\s*(AI|ai|生成|generated|by copilot|by claude|by gpt|by deepseek|by kimi)/i,
    /\/\*\s*(AI|ai|生成|generated|by copilot|by claude|by gpt)/i,
    /#\s*(AI|ai|生成|generated|by copilot)/i,
];

// ─── 状态栏 ──────────────────────────────────────────────

let statusBarItem: vscode.StatusBarItem;
let stats: AuditStats = { total: 0, pending: 0, reviewed: 0, rejected: 0, today: 0 };

export function activate(context: vscode.ExtensionContext) {
    console.log('[龍魂审计追踪] 激活');

    // 状态栏
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'longhun-audit.showAuditLog';
    context.subscriptions.push(statusBarItem);

    // 加载已有统计
    loadStats();
    updateStatusBar();

    // 监听粘贴事件（检测 AI 生成代码粘贴）
    context.subscriptions.push(
        vscode.workspace.onDidChangeTextDocument(onDocumentChange)
    );

    // 监听保存事件
    context.subscriptions.push(
        vscode.workspace.onDidSaveTextDocument(onDocumentSave)
    );

    // 注册命令
    context.subscriptions.push(
        vscode.commands.registerCommand('longhun-audit.showAuditLog', showAuditLog),
        vscode.commands.registerCommand('longhun-audit.auditSelection', auditSelection),
        vscode.commands.registerCommand('longhun-audit.generateReport', generateReport),
        vscode.commands.registerCommand('longhun-audit.markAsReviewed', markAsReviewed)
    );

    // 显示激活提示
    updateStatusBar();
}

export function deactivate() {
    statusBarItem?.dispose();
}

// ─── 文档变更监听（检测粘贴的 AI 代码）────────────────────

function onDocumentChange(e: vscode.TextDocumentChangeEvent) {
    const config = vscode.workspace.getConfiguration('longhun-audit');
    if (!config.get<boolean>('autoAuditOnPaste', true)) return;

    for (const change of e.contentChanges) {
        // 检测大量代码粘贴（超过 3 行或 200 字符）
        const text = change.text;
        if (text.split('\n').length < 3 && text.length < 200) continue;

        // 检测 AI 标记
        if (!hasAIMarker(text)) continue;

        // 记录审计
        recordAudit({
            filePath: e.document.uri.fsPath,
            codeSnippet: text,
            lineStart: change.range.start.line + 1,
            lineEnd: change.range.end.line + 1,
            modelSource: detectModelSource(text),
        });
    }
}

// ─── 文档保存监听 ────────────────────────────────────────

function onDocumentSave(doc: vscode.TextDocument) {
    const config = vscode.workspace.getConfiguration('longhun-audit');
    if (!config.get<boolean>('autoAuditOnSave', true)) return;

    const text = doc.getText();
    if (!hasAIMarker(text)) return;

    // 全文件扫描 AI 标记行
    const lines = text.split('\n');
    let currentBlock: string[] = [];
    let blockStart = 0;

    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const isAIMarked = AI_MARKERS.some(m => m.test(line));

        if (isAIMarked || line.trim() === '') {
            if (currentBlock.length >= 3) {
                recordAudit({
                    filePath: doc.uri.fsPath,
                    codeSnippet: currentBlock.join('\n'),
                    lineStart: blockStart + 1,
                    lineEnd: i,
                    modelSource: detectModelSource(currentBlock.join('\n')),
                });
            }
            currentBlock = [];
            blockStart = i + 1;
        } else if (line.trim().length > 0) {
            currentBlock.push(line);
        }
    }

    // 最后一块
    if (currentBlock.length >= 3) {
        recordAudit({
            filePath: doc.uri.fsPath,
            codeSnippet: currentBlock.join('\n'),
            lineStart: blockStart + 1,
            lineEnd: lines.length,
            modelSource: detectModelSource(currentBlock.join('\n')),
        });
    }
}

// ─── 审计记录 ────────────────────────────────────────────

function recordAudit(params: {
    filePath: string;
    codeSnippet: string;
    lineStart: number;
    lineEnd: number;
    modelSource: string;
}) {
    const entry: AuditEntry = {
        id: crypto.randomBytes(8).toString('hex'),
        timestamp: new Date().toISOString(),
        model_source: params.modelSource,
        prompt_hash: hashString(params.codeSnippet.substring(0, 200)),
        code_hash: hashString(params.codeSnippet),
        file_path: params.filePath,
        line_start: params.lineStart,
        line_end: params.lineEnd,
        code_snippet_preview: params.codeSnippet.substring(0, 100).replace(/\n/g, ' '),
        review_status: 'pending',
        dna: DNA,
    };

    writeAuditEntry(entry);
    stats.total++;
    stats.pending++;
    stats.today++;
    updateStatusBar();
}

// ─── 命令：查看审计日志 ──────────────────────────────────

async function showAuditLog() {
    const entries = readAllAuditEntries();
    if (entries.length === 0) {
        vscode.window.showInformationMessage('🐉 暂无 AI 代码审计记录');
        return;
    }

    // 创建 WebView 面板
    const panel = vscode.window.createWebviewPanel(
        'longhunAuditLog',
        '龍魂 AI 代码审计日志',
        vscode.ViewColumn.One,
        { enableScripts: true }
    );

    panel.webview.html = buildAuditLogHtml(entries);
}

// ─── 命令：审计选中代码 ──────────────────────────────────

async function auditSelection() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const selection = editor.selection;
    if (selection.isEmpty) {
        vscode.window.showWarningMessage('请先选中要审计的代码');
        return;
    }

    const text = editor.document.getText(selection);
    const modelSource = await vscode.window.showInputBox({
        prompt: '输入 AI 模型来源（如: DeepSeek / Kimi / Claude / 手动）',
        placeHolder: 'DeepSeek',
    });

    recordAudit({
        filePath: editor.document.uri.fsPath,
        codeSnippet: text,
        lineStart: selection.start.line + 1,
        lineEnd: selection.end.line + 1,
        modelSource: modelSource || '手动标记',
    });

    vscode.window.showInformationMessage(`🐉 已审计 ${text.split('\n').length} 行代码 → ${modelSource || '手动标记'}`);
}

// ─── 命令：生成审计报告 ──────────────────────────────────

async function generateReport() {
    const entries = readAllAuditEntries();
    if (entries.length === 0) {
        vscode.window.showInformationMessage('🐉 无审计数据可生成报告');
        return;
    }

    // 统计
    const modelStats: Record<string, number> = {};
    const fileStats: Record<string, number> = {};
    for (const e of entries) {
        modelStats[e.model_source] = (modelStats[e.model_source] || 0) + 1;
        fileStats[e.file_path] = (fileStats[e.file_path] || 0) + 1;
    }

    const reportPath = path.join(
        WORKSPACE_ROOT,
        'logs',
        `audit_report_${new Date().toISOString().replace(/[:.]/g, '-')}.md`
    );

    const report = `# 龍魂 AI 代码审计报告

> DNA: ${DNA}
> 生成时间: ${new Date().toISOString()}
> 总记录数: ${entries.length}
> 待审核: ${entries.filter(e => e.review_status === 'pending').length}
> 已审核: ${entries.filter(e => e.review_status === 'reviewed').length}
> 已拒绝: ${entries.filter(e => e.review_status === 'rejected').length}

## 模型来源分布

| 模型 | 次数 |
|------|:---:|
${Object.entries(modelStats).map(([k, v]) => `| ${k} | ${v} |`).join('\n')}

## 文件分布

| 文件 | 次数 |
|------|:---:|
${Object.entries(fileStats).map(([k, v]) => `| ${path.basename(k)} | ${v} |`).join('\n')}

## 最近 50 条记录

| 时间 | 模型 | 文件 | 状态 | 预览 |
|------|------|------|:---:|------|
${entries.slice(-50).reverse().map(e =>
    `| ${e.timestamp.substring(0, 19)} | ${e.model_source} | ${path.basename(e.file_path)}:${e.line_start}-${e.line_end} | ${statusEmoji(e.review_status)} | ${e.code_snippet_preview} |`
).join('\n')}

---
*本报告由龍魂审计追踪插件自动生成，数据仅存本地*
`;

    fs.writeFileSync(reportPath, report, 'utf-8');
    const doc = await vscode.workspace.openTextDocument(reportPath);
    await vscode.window.showTextDocument(doc);
    vscode.window.showInformationMessage(`🐉 审计报告已生成: ${path.basename(reportPath)}`);
}

// ─── 命令：标记为已审核 ──────────────────────────────────

async function markAsReviewed() {
    const entries = readAllAuditEntries();
    const pending = entries.filter(e => e.review_status === 'pending');
    if (pending.length === 0) {
        vscode.window.showInformationMessage('没有待审核的记录');
        return;
    }

    const items = pending.slice(-20).map(e => ({
        label: `$(circle-outline) ${path.basename(e.file_path)}:${e.line_start}-${e.line_end}`,
        description: `${e.model_source} · ${e.timestamp.substring(0, 19)}`,
        detail: e.code_snippet_preview,
        entry: e,
    }));

    const selected = await vscode.window.showQuickPick(items, {
        placeHolder: '选择要标记为已审核的记录',
        canPickMany: true,
    });

    if (!selected || selected.length === 0) return;

    // 更新记录
    const auditPath = getAuditLogPath();
    const allLines = fs.readFileSync(auditPath, 'utf-8').trim().split('\n');
    const selectedIds = new Set(selected.map(s => s.entry.id));

    const updated = allLines.map(line => {
        const e = JSON.parse(line) as AuditEntry;
        if (selectedIds.has(e.id)) {
            e.review_status = 'reviewed';
            e.review_timestamp = new Date().toISOString();
            e.reviewer = 'UID9622';
        }
        return JSON.stringify(e);
    });

    fs.writeFileSync(auditPath, updated.join('\n') + '\n', 'utf-8');
    loadStats();
    updateStatusBar();
    vscode.window.showInformationMessage(`🐉 已审核 ${selected.length} 条记录`);
}

// ─── 辅助函数 ────────────────────────────────────────────

function hasAIMarker(text: string): boolean {
    return AI_MARKERS.some(m => m.test(text));
}

function detectModelSource(text: string): string {
    if (/claude|anthropic/i.test(text)) return 'Claude';
    if (/deepseek/i.test(text)) return 'DeepSeek';
    if (/kimi|moonshot/i.test(text)) return 'Kimi';
    if (/gpt|openai/i.test(text)) return 'GPT';
    if (/copilot/i.test(text)) return 'GitHub Copilot';
    if (/gemini/i.test(text)) return 'Gemini';
    if (/codebuddy/i.test(text)) return 'CodeBuddy';
    return '未知AI';
}

function hashString(s: string): string {
    return crypto.createHash('sha256').update(s, 'utf-8').digest('hex').substring(0, 16);
}

function getAuditLogPath(): string {
    const config = vscode.workspace.getConfiguration('longhun-audit');
    return config.get<string>('auditLogPath') || DEFAULT_AUDIT_LOG;
}

function writeAuditEntry(entry: AuditEntry) {
    const auditPath = getAuditLogPath();
    const dir = path.dirname(auditPath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.appendFileSync(auditPath, JSON.stringify(entry) + '\n', 'utf-8');
}

function readAllAuditEntries(): AuditEntry[] {
    const auditPath = getAuditLogPath();
    if (!fs.existsSync(auditPath)) return [];
    const content = fs.readFileSync(auditPath, 'utf-8').trim();
    if (!content) return [];
    return content.split('\n').map(line => {
        try { return JSON.parse(line) as AuditEntry; }
        catch { return null; }
    }).filter(Boolean) as AuditEntry[];
}

function loadStats() {
    const entries = readAllAuditEntries();
    const today = new Date().toISOString().substring(0, 10);
    stats = {
        total: entries.length,
        pending: entries.filter(e => e.review_status === 'pending').length,
        reviewed: entries.filter(e => e.review_status === 'reviewed').length,
        rejected: entries.filter(e => e.review_status === 'rejected').length,
        today: entries.filter(e => e.timestamp.startsWith(today)).length,
    };
}

function updateStatusBar() {
    const config = vscode.workspace.getConfiguration('longhun-audit');
    if (!config.get<boolean>('showStatusBar', true)) {
        statusBarItem.hide();
        return;
    }
    statusBarItem.text = `$(shield) 审计 ${stats.today} | $(circle-outline) ${stats.pending}`;
    statusBarItem.tooltip = `龍魂AI审计: 总计${stats.total} · 待审${stats.pending} · 已审${stats.reviewed} · 今日${stats.today}`;
    statusBarItem.show();
}

function statusEmoji(status: string): string {
    switch (status) {
        case 'reviewed': return '✅';
        case 'rejected': return '🔴';
        default: return '🟡';
    }
}

function buildAuditLogHtml(entries: AuditEntry[]): string {
    const rows = entries.slice(-100).reverse().map(e => `
        <tr class="status-${e.review_status}">
            <td>${statusEmoji(e.review_status)}</td>
            <td>${e.timestamp.substring(0, 19)}</td>
            <td>${e.model_source}</td>
            <td>${path.basename(e.file_path)}:${e.line_start}</td>
            <td title="${e.code_hash}">${e.code_snippet_preview}</td>
            <td>${e.prompt_hash}</td>
        </tr>
    `).join('');

    return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
:root { --bg: #0a0e17; --bg-card: #111827; --gold: #d4a843; --text: #e2e8f0; --text-dim: #94a3b8; --border: #1e293b; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--bg); color: var(--text); font-family: monospace; font-size: 13px; padding: 16px; }
h1 { color: var(--gold); margin-bottom: 12px; font-size: 18px; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 8px; border-bottom: 2px solid var(--gold); color: var(--gold); font-size: 12px; }
td { padding: 6px 8px; border-bottom: 1px solid var(--border); font-size: 12px; }
tr.status-pending { background: rgba(234,179,8,0.05); }
tr.status-rejected { background: rgba(239,68,68,0.05); }
.summary { background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; padding: 12px; margin-bottom: 16px; display: flex; gap: 24px; }
.stat { text-align: center; }
.stat-value { font-size: 24px; font-weight: 700; color: var(--gold); }
.stat-label { font-size: 11px; color: var(--text-dim); }
</style>
</head>
<body>
<h1>🐉 龍魂 AI 代码审计日志</h1>
<div class="summary">
    <div class="stat"><div class="stat-value">${entries.length}</div><div class="stat-label">总记录</div></div>
    <div class="stat"><div class="stat-value" style="color:#eab308">${entries.filter(e => e.review_status === 'pending').length}</div><div class="stat-label">待审核</div></div>
    <div class="stat"><div class="stat-value" style="color:#22c55e">${entries.filter(e => e.review_status === 'reviewed').length}</div><div class="stat-label">已审核</div></div>
    <div class="stat"><div class="stat-value" style="color:#ef4444">${entries.filter(e => e.review_status === 'rejected').length}</div><div class="stat-label">已拒绝</div></div>
</div>
<table>
<tr><th></th><th>时间</th><th>模型</th><th>位置</th><th>代码预览</th><th>哈希</th></tr>
${rows}
</table>
</body>
</html>`;
}
