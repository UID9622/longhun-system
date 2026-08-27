# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 龍魂一键部署 v1.0
 * DNA: #龍芯⚡️丙午·辛未·ONE-CLICK-DEPLOY-v1.0
 *
 * 功能:
 *   1. 一键 git add + commit + push (GPG签名)
 *   2. 多远程推送：GitHub / Gitee / 华为云
 *   3. 状态栏显示当前分支和待推送数
 *   4. 自动拉取→合并→推送 安全流水线
 */

import * as vscode from 'vscode';
import { exec, ExecException } from 'child_process';
import * as path from 'path';

// ─── 类型 ────────────────────────────────────────────────

interface GitStatus {
    branch: string;
    ahead: number;
    behind: number;
    staged: number;
    modified: number;
    untracked: number;
    clean: boolean;
}

// ─── 状态栏 ──────────────────────────────────────────────

let statusBarItem: vscode.StatusBarItem;
let deployOutput: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    console.log('[龍魂一键部署] 激活');

    deployOutput = vscode.window.createOutputChannel('龍魂部署');

    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 97);
    statusBarItem.command = 'longhun-deploy.quickPush';
    context.subscriptions.push(statusBarItem, deployOutput);
    refreshStatusBar();

    // 定时刷新（每 60 秒）
    const interval = setInterval(refreshStatusBar, 60000);
    context.subscriptions.push({ dispose: () => clearInterval(interval) });

    // 注册命令
    context.subscriptions.push(
        vscode.commands.registerCommand('longhun-deploy.quickPush', () => quickPush()),
        vscode.commands.registerCommand('longhun-deploy.pushToGitHub', () => pushTo('github')),
        vscode.commands.registerCommand('longhun-deploy.pushToGitee', () => pushTo('gitee')),
        vscode.commands.registerCommand('longhun-deploy.pushToHuawei', () => pushTo('huawei')),
        vscode.commands.registerCommand('longhun-deploy.gpgSignAndPush', () => gpgSignAndPush()),
        vscode.commands.registerCommand('longhun-deploy.showGitStatus', () => showGitStatus()),
    );
}

export function deactivate() {
    statusBarItem?.dispose();
    deployOutput?.dispose();
}

// ─── 命令：一键推送 ──────────────────────────────────────

async function quickPush() {
    const config = vscode.workspace.getConfiguration('longhun-deploy');
    const enableGPG = config.get<boolean>('enableGPG', true);

    // 1. 获取提交信息
    const commitMsg = await vscode.window.showInputBox({
        prompt: '输入提交信息',
        placeHolder: 'fix: 修复xxx问题',
        validateInput: (value) => value.trim() ? null : '提交信息不能为空',
    });
    if (!commitMsg) return;

    // 2. 选择提交类型
    const commitType = await vscode.window.showQuickPick(
        ['feat: 新功能', 'fix: 修复', 'docs: 文档', 'refactor: 重构', 'style: 格式', 'test: 测试', 'chore: 杂项', 'perf: 性能'],
        { placeHolder: '选择提交类型' }
    );
    if (!commitType) return;

    const type = commitType.split(':')[0];
    const fullMessage = `${type}: ${commitMsg}`;

    // 3. 显示确认
    const confirmed = await vscode.window.showQuickPick(
        ['确认推送', '取消'],
        { placeHolder: `即将提交: "${fullMessage}" → origin/main` }
    );
    if (confirmed !== '确认推送') return;

    // 4. 执行
    deployOutput.clear();
    deployOutput.show(true);

    const workspaceRoot = getWorkspaceRoot();
    const cmds: string[] = [];

    // git add
    cmds.push(`git add -A`);

    // git commit (with GPG if enabled)
    if (enableGPG) {
        cmds.push(`git commit -S -m "${fullMessage}"`);
    } else {
        cmds.push(`git commit -m "${fullMessage}"`);
    }

    // git pull (auto-pull before push)
    if (config.get<boolean>('autoPullBeforePush', true)) {
        cmds.push(`git pull --rebase origin main`);
    }

    // git push
    cmds.push(`git push origin main`);

    // 同时推送到其他远程
    const remotes = config.get<string[]>('extraRemotes', []);
    for (const remote of remotes) {
        cmds.push(`git push ${remote} main`);
    }

    await executeChain(workspaceRoot, cmds);
    refreshStatusBar();
}

// ─── 命令：推送到指定远程 ─────────────────────────────────

async function pushTo(target: 'github' | 'gitee' | 'huawei') {
    const config = vscode.workspace.getConfiguration('longhun-deploy');
    const remoteMap: Record<string, string> = {
        github: config.get<string>('githubRemote', 'github'),
        gitee: config.get<string>('giteeRemote', 'gitee'),
        huawei: config.get<string>('huaweiRemote', 'huawei'),
    };

    const remote = remoteMap[target];
    const workspaceRoot = getWorkspaceRoot();

    deployOutput.clear();
    deployOutput.show(true);
    deployOutput.appendLine(`🐉 推送到 ${target} (${remote})...`);

    await executeChain(workspaceRoot, [
        `git push ${remote} main`,
    ]);

    vscode.window.showInformationMessage(`🐉 已推送到 ${target}`);
}

// ─── 命令：GPG 签名推送 ──────────────────────────────────

async function gpgSignAndPush() {
    const config = vscode.workspace.getConfiguration('longhun-deploy');
    const gpgKey = config.get<string>('gpgKeyId', '');

    const commitMsg = await vscode.window.showInputBox({
        prompt: '输入 GPG 签名提交信息',
        placeHolder: 'feat: 重要更新',
    });
    if (!commitMsg) return;

    const workspaceRoot = getWorkspaceRoot();
    deployOutput.clear();
    deployOutput.show(true);

    const cmds = [
        'git add -A',
        `git commit -S${gpgKey} -m "${commitMsg}"`,
        'git push origin main',
    ];

    await executeChain(workspaceRoot, cmds);
    refreshStatusBar();
}

// ─── 命令：查看 Git 状态 ──────────────────────────────────

async function showGitStatus() {
    const status = await getGitStatus();

    const panel = vscode.window.createWebviewPanel(
        'gitStatus',
        '龍魂 Git 状态',
        vscode.ViewColumn.One,
        { enableScripts: false }
    );

    panel.webview.html = `<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8">
<style>
:root { --bg: #0a0e17; --bg-card: #111827; --gold: #d4a843; --green: #22c55e; --yellow: #eab308; --red: #ef4444; --text: #e2e8f0; --text-dim: #94a3b8; --border: #1e293b; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--bg); color: var(--text); font-family: monospace; font-size: 13px; padding: 20px; }
h1 { color: var(--gold); margin-bottom: 12px; }
.card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 8px; padding: 16px; margin-bottom: 12px; }
.row { display: flex; justify-content: space-between; padding: 4px 0; }
.label { color: var(--text-dim); }
.value { font-weight: 600; }
.status-clean { color: var(--green); }
.status-dirty { color: var(--yellow); }
</style></head>
<body>
<h1>🐉 Git 状态</h1>
<div class="card">
    <div class="row"><span class="label">分支</span><span class="value" style="color:var(--gold)">${status.branch}</span></div>
    <div class="row"><span class="label">状态</span><span class="value ${status.clean ? 'status-clean' : 'status-dirty'}">${status.clean ? '✅ 干净' : '⚠️ 有变更'}</span></div>
</div>
<div class="card">
    <div class="row"><span class="label">已暂存</span><span class="value">${status.staged}</span></div>
    <div class="row"><span class="label">已修改</span><span class="value">${status.modified}</span></div>
    <div class="row"><span class="label">未跟踪</span><span class="value">${status.untracked}</span></div>
    <div class="row"><span class="label">领先远程</span><span class="value" style="color:var(--yellow)">${status.ahead}</span></div>
    <div class="row"><span class="label">落后远程</span><span class="value" style="color:var(--red)">${status.behind}</span></div>
</div>
</body></html>`;
}

// ─── Git 状态查询 ────────────────────────────────────────

function getGitStatus(): Promise<GitStatus> {
    return new Promise((resolve) => {
        const root = getWorkspaceRoot();
        const defaultStatus: GitStatus = {
            branch: 'unknown', ahead: 0, behind: 0,
            staged: 0, modified: 0, untracked: 0, clean: true,
        };

        exec('git status --porcelain && git rev-parse --abbrev-ref HEAD', { cwd: root }, (err, stdout) => {
            if (err) { resolve(defaultStatus); return; }

            const lines = stdout.trim().split('\n');
            const branch = lines[lines.length - 1] || 'unknown';
            const statusLines = lines.slice(0, -1);

            let staged = 0, modified = 0, untracked = 0;
            for (const line of statusLines) {
                const idx = line.substring(0, 2);
                if (idx.includes('M') || idx.includes('A') || idx.includes('D') || idx.includes('R')) staged++;
                if (idx.includes(' M') || idx.includes(' D')) modified++;
                if (idx.includes('??')) untracked++;
            }

            resolve({
                branch,
                ahead: 0, behind: 0,
                staged, modified, untracked,
                clean: statusLines.length === 0,
            });
        });
    });
}

function refreshStatusBar() {
    getGitStatus().then(status => {
        if (status.clean) {
            statusBarItem.text = `$(git-branch) ${status.branch} ✓`;
            statusBarItem.color = '#22c55e';
        } else {
            const changes = status.staged + status.modified + status.untracked;
            statusBarItem.text = `$(git-branch) ${status.branch} · ${changes}`;
            statusBarItem.color = '#eab308';
        }
        statusBarItem.tooltip = `分支: ${status.branch} · 暂存${status.staged} · 修改${status.modified} · 未跟踪${status.untracked}`;
        statusBarItem.show();
    });
}

// ─── 工具函数 ────────────────────────────────────────────

function getWorkspaceRoot(): string {
    return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || process.cwd();
}

async function executeChain(cwd: string, commands: string[]): Promise<void> {
    for (const cmd of commands) {
        deployOutput.appendLine(`\n> ${cmd}`);
        await new Promise<void>((resolve, reject) => {
            exec(cmd, { cwd, encoding: 'utf-8' }, (error: ExecException | null, stdout: string, stderr: string) => {
                if (stdout) deployOutput.append(stdout);
                if (stderr) deployOutput.append(stderr);
                if (error) {
                    deployOutput.appendLine(`[FAILED] ${error.message}`);
                    vscode.window.showErrorMessage(`🐉 部署失败: ${error.message}`);
                    reject(error);
                } else {
                    deployOutput.appendLine('[OK]');
                    resolve();
                }
            });
        });
    }
    deployOutput.appendLine('\n🎉 部署完成');
    vscode.window.showInformationMessage('🐉 部署完成');
}
