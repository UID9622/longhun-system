/**
 * 龍魂协议校验 v1.0
 * DNA: #龍芯⚡️丙午·辛未·PROTOCOL-CHECKER-v1.0
 *
 * 保存文件时自动扫描:
 *   1. DNA 锚定码检查 — 文件是否包含 #龍芯⚡️ 追溯码
 *   2. 老祖宗规则检查 — 境外API导入/云端上传/敏感库引用
 *   3. 敏感信息泄露 — 密钥/Token/密码/私钥
 *   4. 违规弹窗 + 一键修复
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { Minimatch } from 'minimatch';

// ─── 类型 ────────────────────────────────────────────────

interface ProtocolIssue {
    rule: string;
    severity: 'error' | 'warning' | 'info';
    message: string;
    line?: number;
    column?: number;
    autoFixable: boolean;
}

interface CheckResult {
    file: string;
    passed: boolean;
    issues: ProtocolIssue[];
    checkedAt: string;
}

// ─── 协议规则 ────────────────────────────────────────────

const DNA_PATTERN = /#龍芯⚡️[\u4e00-\u9fa5·䷀-䷿\-A-Za-z0-9._]+/;

const ANCESTOR_RULES: { name: string; pattern: RegExp; message: string; severity: 'error' | 'warning'; autoFixable: boolean }[] = [
    {
        name: '境外AI-OpenAI',
        pattern: /(import\s+openai|from\s+openai)/g,
        message: '直接导入 openai 可能泄露数据到境外，建议改用国内模型或本地模型',
        severity: 'error',
        autoFixable: true,
    },
    {
        name: '境外AI-Anthropic',
        pattern: /(import\s+anthropic|from\s+anthropic)/g,
        message: '直接导入 anthropic 可能泄露数据到境外',
        severity: 'error',
        autoFixable: true,
    },
    {
        name: '境外AI-Google',
        pattern: /(import\s+google\.generativeai|from\s+google\.generativeai)/g,
        message: '直接导入 Google AI 可能泄露数据到境外',
        severity: 'warning',
        autoFixable: true,
    },
    {
        name: '云端上传-requests',
        pattern: /requests\.(post|put)\s*\(\s*['"](?!https?:\/\/(127\.0\.0\.1|localhost))/g,
        message: '检测到向非本地地址发送数据，请确认数据主权',
        severity: 'warning',
        autoFixable: false,
    },
    {
        name: '云端上传-boto3',
        pattern: /(import\s+boto3|from\s+boto3|boto3\.client\s*\(\s*['"]s3['"]\s*\))/g,
        message: '检测到 AWS S3 上传，数据可能出境',
        severity: 'error',
        autoFixable: true,
    },
    {
        name: '敏感库-telemetry',
        pattern: /(sentry|datadog|newrelic|logrocket|fullstory|mixpanel)/gi,
        message: '检测到遥测/监控库，可能上传用户数据',
        severity: 'warning',
        autoFixable: true,
    },
];

const SENSITIVE_PATTERNS: { name: string; pattern: RegExp; message: string }[] = [
    { name: 'API Key', pattern: /(api[_-]?key|apikey)\s*[:=]\s*['"][^'"]{8,}['"]/gi, message: '硬编码 API 密钥' },
    { name: 'Secret', pattern: /(secret[_-]?key|access[_-]?token)\s*[:=]\s*['"][^'"]{8,}['"]/gi, message: '硬编码密钥/Token' },
    { name: 'Password', pattern: /(password|passwd|pwd)\s*[:=]\s*['"][^'"]+['"]/gi, message: '硬编码密码' },
    { name: 'OpenAI Key', pattern: /sk-[a-zA-Z0-9]{20,}/g, message: 'OpenAI API Key 格式' },
    { name: 'Tencent Key', pattern: /AKID[a-zA-Z0-9]{32,}/g, message: '腾讯云 SecretId' },
    { name: 'Private Key', pattern: /-----BEGIN\s+(RSA|EC|DSA|OPENSSH)?\s*PRIVATE KEY-----/g, message: '私钥明文存储' },
    { name: 'JWT Secret', pattern: /(jwt[_-]?secret|jwt[_-]?key)\s*[:=]\s*['"][^'"]+['"]/gi, message: 'JWT 密钥硬编码' },
    { name: 'Database URL', pattern: /(mongodb|mysql|postgresql|redis):\/\/[^'"\s]+@/gi, message: '数据库连接串含密码' },
];

// ─── 状态栏 ──────────────────────────────────────────────

let statusBarItem: vscode.StatusBarItem;
let lastCheckStats = { passed: 0, warning: 0, error: 0 };

export function activate(context: vscode.ExtensionContext) {
    console.log('[龍魂协议校验] 激活');

    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 98);
    statusBarItem.command = 'longhun-protocol.checkWorkspace';
    context.subscriptions.push(statusBarItem);
    updateStatusBar();

    // 保存时自动检查
    context.subscriptions.push(
        vscode.workspace.onDidSaveTextDocument(onSave)
    );

    // 注册命令
    context.subscriptions.push(
        vscode.commands.registerCommand('longhun-protocol.checkFile', checkCurrentFile),
        vscode.commands.registerCommand('longhun-protocol.checkWorkspace', checkWorkspace),
        vscode.commands.registerCommand('longhun-protocol.fixFile', fixCurrentFile),
    );

    // 对已打开的文件做一次检查
    checkAllOpenFiles();
}

export function deactivate() {
    statusBarItem?.dispose();
}

// ─── 保存时检查 ──────────────────────────────────────────

function onSave(doc: vscode.TextDocument) {
    if (shouldIgnore(doc.uri.fsPath)) return;

    const result = checkDocument(doc);
    if (result.issues.length > 0) {
        const errors = result.issues.filter(i => i.severity === 'error');
        const warnings = result.issues.filter(i => i.severity === 'warning');

        if (errors.length > 0) {
            const config = vscode.workspace.getConfiguration('longhun-protocol');
            if (config.get<boolean>('autoFixOnSave', false)) {
                autoFixDocument(doc, result.issues);
            } else {
                vscode.window.showErrorMessage(
                    `🐉 协议违规(${errors.length}错误): ${errors[0].message}`,
                    '查看详情', '一键修复'
                ).then(choice => {
                    if (choice === '查看详情') showCheckResult(result);
                    if (choice === '一键修复') autoFixDocument(doc, result.issues);
                });
            }
        } else if (warnings.length > 0) {
            vscode.window.showWarningMessage(
                `🐉 协议提醒(${warnings.length}): ${warnings[0].message}`,
                '查看详情'
            ).then(choice => {
                if (choice === '查看详情') showCheckResult(result);
            });
        }
    }
}

// ─── 文档检查 ────────────────────────────────────────────

function checkDocument(doc: vscode.TextDocument): CheckResult {
    const config = vscode.workspace.getConfiguration('longhun-protocol');
    const text = doc.getText();
    const issues: ProtocolIssue[] = [];

    // 1. DNA 锚定检查
    if (config.get<boolean>('enableDNA', true)) {
        if (!DNA_PATTERN.test(text)) {
            issues.push({
                rule: 'DNA锚定',
                severity: 'warning',
                message: '文件缺少 DNA 锚定码。建议添加 #龍芯⚡️... 格式的追溯码',
                autoFixable: true,
            });
        }
    }

    // 2. 老祖宗规则检查
    if (config.get<boolean>('enableAncestors', true)) {
        for (const rule of ANCESTOR_RULES) {
            rule.pattern.lastIndex = 0;
            const match = rule.pattern.exec(text);
            if (match) {
                const pos = doc.positionAt(match.index);
                issues.push({
                    rule: rule.name,
                    severity: rule.severity,
                    message: rule.message,
                    line: pos.line + 1,
                    column: pos.character + 1,
                    autoFixable: rule.autoFixable,
                });
            }
        }
    }

    // 3. 敏感信息检查
    if (config.get<boolean>('enableSensitive', true)) {
        for (const sp of SENSITIVE_PATTERNS) {
            sp.pattern.lastIndex = 0;
            const match = sp.pattern.exec(text);
            if (match) {
                const pos = doc.positionAt(match.index);
                issues.push({
                    rule: sp.name,
                    severity: 'error',
                    message: `敏感信息泄露: ${sp.message}`,
                    line: pos.line + 1,
                    column: pos.character + 1,
                    autoFixable: false, // 敏感信息不能自动修复，需要人工处理
                });
            }
        }
    }

    return {
        file: doc.uri.fsPath,
        passed: issues.length === 0,
        issues,
        checkedAt: new Date().toISOString(),
    };
}

// ─── 自动修复 ────────────────────────────────────────────

function autoFixDocument(doc: vscode.TextDocument, issues: ProtocolIssue[]) {
    const edit = new vscode.WorkspaceEdit();
    let text = doc.getText();
    let modified = false;

    const fixableIssues = issues.filter(i => i.autoFixable);

    for (const issue of fixableIssues) {
        switch (issue.rule) {
            case 'DNA锚定':
                if (!DNA_PATTERN.test(text)) {
                    const now = new Date();
                    text = `#龍芯⚡️丙午·辛未·AUTO-FIX-${now.getHours()}${now.getMinutes()}\n` + text;
                    modified = true;
                }
                break;

            case '境外AI-OpenAI':
                text = text.replace(/(import\s+openai|from\s+openai)/g, '// 🔴 已禁用(数据主权): $1');
                modified = true;
                break;

            case '境外AI-Anthropic':
                text = text.replace(/(import\s+anthropic|from\s+anthropic)/g, '// 🔴 已禁用(数据主权): $1');
                modified = true;
                break;

            case '境外AI-Google':
                text = text.replace(/(import\s+google\.generativeai|from\s+google\.generativeai)/g, '// 🟡 已禁用(数据主权): $1');
                modified = true;
                break;

            case '云端上传-boto3':
                text = text.replace(/(import\s+boto3|from\s+boto3)/g, '// 🔴 已禁用(AWS S3): $1');
                modified = true;
                break;

            case '敏感库-telemetry':
                // 注释掉遥测库导入
                text = text.replace(
                    new RegExp(`(import\\s+${issue.rule}|from\\s+${issue.rule})`, 'gi'),
                    '// 🔴 已禁用(遥测): $1'
                );
                modified = true;
                break;
        }
    }

    if (modified) {
        const fullRange = new vscode.Range(
            doc.positionAt(0),
            doc.positionAt(doc.getText().length)
        );
        edit.replace(doc.uri, fullRange, text);
        vscode.workspace.applyEdit(edit);
        vscode.window.showInformationMessage(`🐉 已自动修复 ${fixableIssues.length} 项协议违规`);
    }
}

// ─── 命令：检查当前文件 ──────────────────────────────────

function checkCurrentFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const result = checkDocument(editor.document);
    showCheckResult(result);
}

// ─── 命令：检查工作区 ────────────────────────────────────

async function checkWorkspace() {
    const files = await vscode.workspace.findFiles('**/*.{py,js,ts,jsx,tsx,cnsh,sh,json,yaml,yml,toml,md}', '**/node_modules/**');
    const config = vscode.workspace.getConfiguration('longhun-protocol');
    const ignoredPatterns = config.get<string[]>('ignoredFiles', []);

    const filtered = files.filter(f => !shouldIgnore(f.fsPath, ignoredPatterns));

    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: '龍魂协议校验中...',
        cancellable: true,
    }, async (progress, token) => {
        const results: CheckResult[] = [];
        let checked = 0;

        for (const file of filtered) {
            if (token.isCancellationRequested) break;
            try {
                const doc = await vscode.workspace.openTextDocument(file);
                const result = checkDocument(doc);
                if (!result.passed) results.push(result);
                checked++;
                progress.report({ increment: 100 / filtered.length, message: `${checked}/${filtered.length}` });
            } catch { /* skip */ }
        }

        // 汇总
        const totalIssues = results.reduce((sum, r) => sum + r.issues.length, 0);
        const errors = results.reduce((sum, r) => sum + r.issues.filter(i => i.severity === 'error').length, 0);
        const warnings = results.reduce((sum, r) => sum + r.issues.filter(i => i.severity === 'warning').length, 0);

        lastCheckStats = { passed: filtered.length - results.length, warning: warnings, error: errors };
        updateStatusBar();

        if (results.length === 0) {
            vscode.window.showInformationMessage(`🐉 协议校验通过 · ${filtered.length} 文件全部合规`);
        } else {
            showWorkspaceResult(results, filtered.length);
        }
    });
}

// ─── 命令：一键修复当前文件 ──────────────────────────────

function fixCurrentFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;

    const result = checkDocument(editor.document);
    if (result.issues.length === 0) {
        vscode.window.showInformationMessage('当前文件无协议违规');
        return;
    }
    autoFixDocument(editor.document, result.issues);
}

// ─── 显示结果 ────────────────────────────────────────────

function showCheckResult(result: CheckResult) {
    const panel = vscode.window.createWebviewPanel(
        'protocolCheck',
        `协议校验: ${path.basename(result.file)}`,
        vscode.ViewColumn.Two,
        { enableScripts: false }
    );

    const issueRows = result.issues.map(i => {
        const icon = i.severity === 'error' ? '🔴' : i.severity === 'warning' ? '🟡' : 'ℹ️';
        const loc = i.line ? `:${i.line}` : '';
        const fixable = i.autoFixable ? ' [可自动修复]' : '';
        return `<tr><td>${icon}</td><td>${i.rule}</td><td>${i.message}${fixable}</td><td>${loc}</td></tr>`;
    }).join('');

    panel.webview.html = `<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
:root { --bg: #0a0e17; --bg-card: #111827; --gold: #d4a843; --green: #22c55e; --red: #ef4444; --text: #e2e8f0; --text-dim: #94a3b8; --border: #1e293b; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--bg); color: var(--text); font-family: monospace; font-size: 13px; padding: 16px; }
h1 { color: ${result.passed ? 'var(--green)' : 'var(--red)'}; margin-bottom: 8px; font-size: 16px; }
.file { color: var(--text-dim); margin-bottom: 12px; font-size: 12px; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 8px; border-bottom: 2px solid var(--gold); color: var(--gold); }
td { padding: 6px 8px; border-bottom: 1px solid var(--border); }
.summary { padding: 12px; margin-bottom: 16px; border-radius: 6px; background: var(--bg-card); border: 1px solid var(--border); }
</style></head>
<body>
<h1>${result.passed ? '✅ 协议通过' : `⚠️ ${result.issues.length} 项问题`}</h1>
<div class="file">${result.file}</div>
<div class="summary">
    错误: ${result.issues.filter(i => i.severity === 'error').length} ·
    警告: ${result.issues.filter(i => i.severity === 'warning').length} ·
    提示: ${result.issues.filter(i => i.severity === 'info').length}
</div>
${result.issues.length > 0 ? `<table><tr><th></th><th>规则</th><th>说明</th><th>位置</th></tr>${issueRows}</table>` : '<p style="color:var(--green)">无协议违规</p>'}
</body></html>`;
}

function showWorkspaceResult(results: CheckResult[], totalFiles: number) {
    const totalIssues = results.reduce((sum, r) => sum + r.issues.length, 0);
    const filesWithIssues = results.length;

    vscode.window.showWarningMessage(
        `🐉 协议校验: ${filesWithIssues}/${totalFiles} 文件有 ${totalIssues} 项问题`,
        '查看详情', '一键修复全部'
    ).then(async choice => {
        if (choice === '查看详情') {
            // 显示摘要面板
            const panel = vscode.window.createWebviewPanel(
                'workspaceProtocol',
                '龍魂工作区协议校验',
                vscode.ViewColumn.One,
                { enableScripts: false }
            );

            const rows = results.map(r => {
                const errors = r.issues.filter(i => i.severity === 'error').length;
                const warnings = r.issues.filter(i => i.severity === 'warning').length;
                return `<tr>
                    <td>${errors > 0 ? '🔴' : '🟡'}</td>
                    <td>${path.basename(r.file)}</td>
                    <td>${errors} 错误 · ${warnings} 警告</td>
                    <td>${r.issues[0]?.message || ''}</td>
                </tr>`;
            }).join('');

            panel.webview.html = `<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
:root { --bg: #0a0e17; --bg-card: #111827; --gold: #d4a843; --text: #e2e8f0; --text-dim: #94a3b8; --border: #1e293b; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--bg); color: var(--text); font-family: monospace; font-size: 13px; padding: 16px; }
h1 { color: var(--gold); margin-bottom: 8px; }
table { width: 100%; border-collapse: collapse; }
th { text-align: left; padding: 8px; border-bottom: 2px solid var(--gold); color: var(--gold); }
td { padding: 6px 8px; border-bottom: 1px solid var(--border); }
</style></head>
<body>
<h1>🐉 工作区协议校验结果</h1>
<p style="color:var(--text-dim);margin-bottom:12px">${totalFiles} 文件 · ${filesWithIssues} 有问题 · ${totalIssues} 项问题</p>
<table><tr><th></th><th>文件</th><th>问题</th><th>首项</th></tr>${rows}</table>
</body></html>`;
        }

        if (choice === '一键修复全部') {
            for (const r of results) {
                try {
                    const doc = await vscode.workspace.openTextDocument(vscode.Uri.file(r.file));
                    autoFixDocument(doc, r.issues);
                } catch { /* skip */ }
            }
            vscode.window.showInformationMessage(`🐉 已尝试修复 ${results.length} 个文件`);
        }
    });
}

// ─── 辅助 ────────────────────────────────────────────────

function shouldIgnore(filePath: string, extraPatterns?: string[]): boolean {
    const patterns = extraPatterns || vscode.workspace.getConfiguration('longhun-protocol').get<string[]>('ignoredFiles', []);
    const relativePath = path.relative(
        vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || '',
        filePath
    );
    return patterns.some(p => {
        try {
            return new Minimatch(p, { matchBase: true }).match(relativePath || filePath);
        } catch { return false; }
    });
}

function checkAllOpenFiles() {
    vscode.window.visibleTextEditors.forEach(editor => {
        if (!shouldIgnore(editor.document.uri.fsPath)) {
            checkDocument(editor.document);
        }
    });
}

function updateStatusBar() {
    if (lastCheckStats.error > 0) {
        statusBarItem.text = `$(error) 协议 ${lastCheckStats.error}`;
        statusBarItem.color = '#ef4444';
    } else if (lastCheckStats.warning > 0) {
        statusBarItem.text = `$(warning) 协议 ${lastCheckStats.warning}`;
        statusBarItem.color = '#eab308';
    } else {
        statusBarItem.text = '$(pass) 协议';
        statusBarItem.color = '#22c55e';
    }
    statusBarItem.tooltip = `龍魂协议校验 · 通过${lastCheckStats.passed} · 警告${lastCheckStats.warning} · 错误${lastCheckStats.error}`;
    statusBarItem.show();
}
