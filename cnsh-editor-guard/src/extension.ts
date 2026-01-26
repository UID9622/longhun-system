/*
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龙魂系统 | UID9622                                        ║
╠═══════════════════════════════════════════════════════════════╣
║  📦 模块：CNSH编辑器智能避坑插件入口                           ║
║  📌 版本：v1.0                                                ║
║  🧬 DNA：#UID9622⚡️2026-01-26-EXTENSION-v1.0                 ║
║  🔐 GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F            ║
║  👤 创建者：Lucky·UID9622（诸葛鑫）                          ║
║  📅 创建时间：北京时间 2026-01-26                             ║
║  🌐 项目：AI Truth Protocol                                   ║
╚═══════════════════════════════════════════════════════════════╝
*/

import * as vscode from 'vscode';
import { DNAHeaderGenerator } from './generators/dnaHeader';
import { AIAnnotationGenerator } from './generators/aiAnnotation';
import {
    NotionWatermarkBlockGenerator,
    WatermarkValidator,
    WatermarkType,
    WatermarkConfig
} from './generators/notionWatermarkBlocks';
import { CodeAnalyzer } from './analyzers/codeAnalyzer';
import { WorkspaceScanner } from './scanners/workspaceScanner';

// 全局实例
let dnaHeaderGenerator: DNAHeaderGenerator;
let aiAnnotationGenerator: AIAnnotationGenerator;
let watermarkGenerator: NotionWatermarkBlockGenerator;
let codeAnalyzer: CodeAnalyzer;
let workspaceScanner: WorkspaceScanner;

/**
 * 插件激活入口
 */
export function activate(context: vscode.ExtensionContext) {
    console.log('🐉 CNSH编辑器智能避坑插件已激活');

    // 初始化生成器
    dnaHeaderGenerator = new DNAHeaderGenerator();
    aiAnnotationGenerator = new AIAnnotationGenerator();
    watermarkGenerator = new NotionWatermarkBlockGenerator(getWatermarkConfig());
    codeAnalyzer = new CodeAnalyzer();
    workspaceScanner = new WorkspaceScanner();

    // 注册DNA头部命令
    const addDnaHeaderCommand = vscode.commands.registerCommand('cnsh.addDnaHeader', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('请先打开一个文件');
            return;
        }

        const header = dnaHeaderGenerator.generateHeader(editor.document);
        await editor.edit(editBuilder => {
            editBuilder.insert(new vscode.Position(0, 0), header);
        });

        vscode.window.showInformationMessage('🧬 DNA追溯头部已添加');
    });

    // 注册AI类型标注命令
    const aiTypeAnnotationCommand = vscode.commands.registerCommand('cnsh.aiTypeAnnotation', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('请先打开一个文件');
            return;
        }

        const annotation = aiAnnotationGenerator.generateAnnotation(editor.document);
        await editor.edit(editBuilder => {
            editBuilder.insert(new vscode.Position(0, 0), annotation);
        });

        vscode.window.showInformationMessage('🏷️ AI输出类型标注已添加');
    });

    // 注册水印块命令 - 快速选择
    const insertWatermarkCommand = vscode.commands.registerCommand('cnsh.insertWatermark', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('请先打开一个文件');
            return;
        }

        // 显示快速选择菜单
        const options = [
            { label: '📋 标准版', description: '完整信息，适用于核心技术文档', type: WatermarkType.STANDARD },
            { label: '📝 精简版', description: '日常使用，简洁清晰', type: WatermarkType.COMPACT },
            { label: '⚡ 极简版', description: '快速标注，一行搞定', type: WatermarkType.MINIMAL },
            { label: '🎨 美化版', description: '对外展示，专业美观', type: WatermarkType.BEAUTIFIED },
            { label: '💻 代码仓库版', description: '适用于代码文件', type: WatermarkType.CODE_REPO },
            { label: '📰 文章版', description: '适用于博客、公众号', type: WatermarkType.ARTICLE },
            { label: '🤝 协作版', description: '多人协作文档', type: WatermarkType.COLLABORATION },
            { label: '🌐 CSDN版', description: 'HTML格式，适用于CSDN', type: WatermarkType.CSDN },
            { label: '📄 Markdown版', description: '通用Markdown格式', type: WatermarkType.MARKDOWN }
        ];

        const selected = await vscode.window.showQuickPick(options, {
            placeHolder: '选择水印块类型',
            title: '📜 插入版权水印块'
        });

        if (!selected) {
            return;
        }

        // 更新配置
        watermarkGenerator.updateConfig(getWatermarkConfig());
        const watermark = watermarkGenerator.generate(selected.type);

        await editor.edit(editBuilder => {
            const position = editor.selection.active;
            editBuilder.insert(position, '\n' + watermark + '\n');
        });

        vscode.window.showInformationMessage(`📜 ${selected.label} 水印块已插入`);
    });

    // 注册各种水印块快捷命令
    const watermarkCommands = [
        { command: 'cnsh.insertWatermarkStandard', type: WatermarkType.STANDARD, name: '标准版' },
        { command: 'cnsh.insertWatermarkCompact', type: WatermarkType.COMPACT, name: '精简版' },
        { command: 'cnsh.insertWatermarkMinimal', type: WatermarkType.MINIMAL, name: '极简版' },
        { command: 'cnsh.insertWatermarkBeautified', type: WatermarkType.BEAUTIFIED, name: '美化版' },
        { command: 'cnsh.insertWatermarkCode', type: WatermarkType.CODE_REPO, name: '代码仓库版' },
        { command: 'cnsh.insertWatermarkMarkdown', type: WatermarkType.MARKDOWN, name: 'Markdown版' }
    ];

    for (const cmd of watermarkCommands) {
        const disposable = vscode.commands.registerCommand(cmd.command, async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('请先打开一个文件');
                return;
            }

            watermarkGenerator.updateConfig(getWatermarkConfig());
            const watermark = watermarkGenerator.generate(cmd.type);

            await editor.edit(editBuilder => {
                const position = editor.selection.active;
                editBuilder.insert(position, '\n' + watermark + '\n');
            });

            vscode.window.showInformationMessage(`📜 ${cmd.name}水印块已插入`);
        });

        context.subscriptions.push(disposable);
    }

    // 注册水印块验证命令
    const validateWatermarkCommand = vscode.commands.registerCommand('cnsh.validateWatermark', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('请先打开一个文件');
            return;
        }

        const content = editor.document.getText();
        const result = WatermarkValidator.checkIntegrity(content);

        if (result.isValid) {
            vscode.window.showInformationMessage('✅ 水印块验证通过！');
        } else {
            const issueList = result.issues.join('\n• ');
            vscode.window.showWarningMessage(`⚠️ 水印块验证发现问题：\n• ${issueList}`, '查看详情').then(selection => {
                if (selection === '查看详情') {
                    showValidationDetails(result);
                }
            });
        }
    });

    // 注册扫描命令
    const scanFileCommand = vscode.commands.registerCommand('cnsh.scanFile', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('请先打开一个文件');
            return;
        }

        const diagnostics = codeAnalyzer.analyzeDocument(editor.document);
        vscode.window.showInformationMessage(`🔍 扫描完成，发现 ${diagnostics.length} 个问题`);
    });

    const scanWorkspaceCommand = vscode.commands.registerCommand('cnsh.scanWorkspace', async () => {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: '🌐 正在扫描工作区...',
            cancellable: true
        }, async (progress, token) => {
            const results = await workspaceScanner.scanWorkspace(progress, token);
            const totalIssues = results.reduce((sum, r) => sum + r.issues.length, 0);
            vscode.window.showInformationMessage(`🌐 工作区扫描完成，共扫描 ${results.length} 个文件，发现 ${totalIssues} 个问题`);
        });
    });

    // 注册快速修正命令
    const quickFixCommand = vscode.commands.registerCommand('cnsh.quickFix', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('请先打开一个文件');
            return;
        }

        const diagnostics = codeAnalyzer.analyzeDocument(editor.document);
        if (diagnostics.length === 0) {
            vscode.window.showInformationMessage('✅ 没有发现需要修正的问题');
            return;
        }

        // 显示问题列表并提供修正选项
        const options = diagnostics.map((d, i) => ({
            label: `${i + 1}. ${d.message}`,
            description: `行 ${d.range.start.line + 1}`,
            diagnostic: d
        }));

        const selected = await vscode.window.showQuickPick(options, {
            placeHolder: '选择要修正的问题',
            title: '🔧 智能修正'
        });

        if (selected) {
            // 执行修正逻辑
            vscode.window.showInformationMessage(`🔧 正在修正: ${selected.label}`);
        }
    });

    // 添加所有命令到订阅列表
    context.subscriptions.push(
        addDnaHeaderCommand,
        aiTypeAnnotationCommand,
        insertWatermarkCommand,
        validateWatermarkCommand,
        scanFileCommand,
        scanWorkspaceCommand,
        quickFixCommand
    );

    // 注册配置变更监听
    vscode.workspace.onDidChangeConfiguration(e => {
        if (e.affectsConfiguration('cnsh.watermark')) {
            watermarkGenerator.updateConfig(getWatermarkConfig());
            console.log('🔄 水印配置已更新');
        }
    });

    console.log('✅ CNSH编辑器插件初始化完成');
}

/**
 * 从VSCode配置获取水印配置
 */
function getWatermarkConfig(): Partial<WatermarkConfig> {
    const config = vscode.workspace.getConfiguration('cnsh.watermark');
    return {
        uid: config.get<string>('uid', '9622'),
        creatorName: config.get<string>('creatorName', '诸葛鑫'),
        creatorEnglishName: config.get<string>('creatorEnglishName', 'Lucky'),
        dnaPrefix: config.get<string>('dnaPrefix', '#ZHUGEXIN⚡️2026'),
        whitepaperVersion: config.get<string>('whitepaperVersion', 'WP-v1.0.0'),
        licenseType: config.get<string>('licenseType', '木兰宽松许可证 v2')
    };
}

/**
 * 显示验证详情
 */
function showValidationDetails(result: ReturnType<typeof WatermarkValidator.checkIntegrity>): void {
    const panel = vscode.window.createWebviewPanel(
        'watermarkValidation',
        '水印块验证结果',
        vscode.ViewColumn.One,
        {}
    );

    panel.webview.html = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>水印块验证结果</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            padding: 20px;
            background: #1e1e1e;
            color: #d4d4d4;
        }
        h1 { color: #569cd6; }
        .status { font-size: 24px; margin: 20px 0; }
        .valid { color: #4ec9b0; }
        .invalid { color: #f14c4c; }
        .checklist { list-style: none; padding: 0; }
        .checklist li { padding: 8px 0; }
        .check { color: #4ec9b0; }
        .cross { color: #f14c4c; }
        .issues { background: #2d2d2d; padding: 15px; border-radius: 8px; margin-top: 20px; }
        .issues h3 { color: #ce9178; }
        .issues ul { color: #f14c4c; }
    </style>
</head>
<body>
    <h1>📜 水印块验证结果</h1>

    <div class="status ${result.isValid ? 'valid' : 'invalid'}">
        ${result.isValid ? '✅ 验证通过' : '⚠️ 验证失败'}
    </div>

    <h2>检查清单</h2>
    <ul class="checklist">
        <li>${result.hasDNACode ? '<span class="check">✅</span>' : '<span class="cross">❌</span>'} DNA追溯码</li>
        <li>${result.hasCreator ? '<span class="check">✅</span>' : '<span class="cross">❌</span>'} 创作者信息</li>
        <li>${result.hasWhitepaperVersion ? '<span class="check">✅</span>' : '<span class="cross">❌</span>'} 白皮书版本</li>
        <li>${result.hasProhibitions ? '<span class="check">✅</span>' : '<span class="cross">❌</span>'} 禁止条款</li>
        <li>${result.hasSovereigntyStatement ? '<span class="check">✅</span>' : '<span class="cross">❌</span>'} 数据主权声明</li>
    </ul>

    ${result.issues.length > 0 ? `
    <div class="issues">
        <h3>发现的问题</h3>
        <ul>
            ${result.issues.map(issue => `<li>${issue}</li>`).join('')}
        </ul>
    </div>
    ` : ''}
</body>
</html>
    `;
}

/**
 * 插件停用
 */
export function deactivate() {
    console.log('🐉 CNSH编辑器智能避坑插件已停用');
}
