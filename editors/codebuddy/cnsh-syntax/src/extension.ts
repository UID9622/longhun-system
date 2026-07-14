/**
 * CNSH 语法高亮 v2.0 · 龍魂协议校验插件
 * DNA: #龍芯⚡️丙午·辛未·CNSH-SYNTAX-v2.0
 *
 * 功能:
 *   1. CNSH 语法高亮（中文变量/关键字/DNA锚定/安全标记/内置函数 分层着色）
 *   2. 中文变量名自动补全建议
 *   3. 保存时自动审计变量命名（纯英文→建议改中文）
 *   4. 保存时自动龍魂协议校验（DNA锚定/老祖宗规则/敏感信息泄露）
 *   5. 违规弹窗警告 + 一键修复
 *   6. 审计日志写入本地
 */

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { LanguageClient, LanguageClientOptions, ServerOptions, TransportKind } from 'vscode-languageclient/node';

// ─── 常量 ───────────────────────────────────────────────

const CNSH_KEYWORDS = [
    '定义', '函数', '返回', '如果', '否则', '否则如果',
    '循环', '当', '对于', '遍历', '中断', '继续',
    '打印', '输入', '真', '假', '空', '并且', '或者', '非',
    '导入', '导出', '模块', '变量', '常量', '结构体',
    '类型', '实现', '接口', '继承', '枚举',
    '整数', '浮点', '文本', '布尔', '列表', '字典', '集合', '元组',
];

const CNSH_BUILTINS = [
    '长度', '类型', '范围', '排序', '映射', '过滤', '归约',
    '连接', '分割', '替换', '格式化',
    '读取文件', '写入文件', '发送请求',
    '解析JSON', '生成JSON',
    '哈希计算', '签名验证',
    'DNA检测', '伦理审计', '熔断检查', '日志记录',
    '三色审计', '伦理检查', '闸门通行',
];

const DNA_PATTERN = /#龍芯⚡️[\u4e00-\u9fa5·䷀-䷿\-A-Za-z0-9._]+/;
const SENSITIVE_PATTERNS: { pattern: RegExp; message: string }[] = [
    { pattern: /(api[_-]?key|apikey|secret[_-]?key|access[_-]?token|private[_-]?key)\s*[:=]\s*['"][^'"]{8,}['"]/gi, message: '疑似硬编码 API 密钥' },
    { pattern: /(password|passwd|pwd)\s*[:=]\s*['"][^'"]+['"]/gi, message: '疑似硬编码密码' },
    { pattern: /(sk-[a-zA-Z0-9]{20,})/g, message: '疑似 OpenAI/云端 API 密钥格式' },
    { pattern: /(AKID[a-zA-Z0-9]{32,})/g, message: '疑似腾讯云 SecretId' },
    { pattern: /-----BEGIN\s+(RSA|EC|DSA|OPENSSH)?\s*PRIVATE KEY-----/g, message: '私钥明文存储' },
];

// ─── 激活入口 ────────────────────────────────────────────

let client: LanguageClient | undefined;
let outputChannel: vscode.OutputChannel;
let diagCollection: vscode.DiagnosticCollection;

export function activate(context: vscode.ExtensionContext) {
    console.log('[CNSH v2.0] 激活');

    outputChannel = vscode.window.createOutputChannel('CNSH');
    diagCollection = vscode.languages.createDiagnosticCollection('cnsh');

    // 尝试启动 LSP 客户端（可选，CNSh 编译服务可用时启动）
    tryStartLSP(context);

    // 注册补全提供器
    context.subscriptions.push(
        vscode.languages.registerCompletionItemProvider(
            'cnsh',
            new CnshCompletionProvider(),
            '.' // 触发字符
        )
    );

    // 注册保存时审计
    context.subscriptions.push(
        vscode.workspace.onDidSaveTextDocument(onSave)
    );

    // 注册命令
    context.subscriptions.push(
        vscode.commands.registerCommand('cnsh-syntax.runFile', runFile),
        vscode.commands.registerCommand('cnsh-syntax.compileFile', compileFile),
        vscode.commands.registerCommand('cnsh-syntax.auditVariables', auditCurrentFile),
        vscode.commands.registerCommand('cnsh-syntax.showDNA', showDNA),
        vscode.commands.registerCommand('cnsh-syntax.checkProtocol', checkProtocol),
        vscode.commands.registerCommand('cnsh-syntax.fixProtocol', fixProtocol),
        diagCollection,
        outputChannel
    );

    // 激活时对已打开的 CNSH 文件做一次检查
    vscode.window.visibleTextEditors.forEach(editor => {
        if (editor.document.languageId === 'cnsh') {
            auditDocument(editor.document);
        }
    });

    vscode.window.showInformationMessage('🐉 CNSH v2.0 语法引擎已激活');
}

export function deactivate(): Thenable<void> | undefined {
    diagCollection?.clear();
    diagCollection?.dispose();
    return client ? client.stop() : undefined;
}

// ─── LSP 客户端 ──────────────────────────────────────────

function tryStartLSP(context: vscode.ExtensionContext) {
    try {
        const serverOptions: ServerOptions = {
            command: 'cnsh',
            args: ['lsp', '--stdio'],
            transport: TransportKind.stdio,
        };
        const clientOptions: LanguageClientOptions = {
            documentSelector: [{ scheme: 'file', language: 'cnsh' }],
            outputChannel,
        };
        client = new LanguageClient('cnsh-v2', 'CNSH Language Server v2', serverOptions, clientOptions);
        client.start();
    } catch {
        outputChannel.appendLine('[CNSH] LSP 服务未找到，仅使用本地语法检查');
    }
}

// ─── 保存时审计 ──────────────────────────────────────────

function onSave(doc: vscode.TextDocument) {
    if (doc.languageId !== 'cnsh') return;

    const config = vscode.workspace.getConfiguration('cnsh');

    if (config.get<boolean>('enableAuditOnSave', true)) {
        auditDocument(doc);
    }

    if (config.get<boolean>('enableProtocolCheckOnSave', true)) {
        checkProtocolOnDocument(doc);
    }
}

// ─── 变量审计 ────────────────────────────────────────────

function auditDocument(doc: vscode.TextDocument) {
    const text = doc.getText();
    const lines = text.split('\n');
    const diagnostics: vscode.Diagnostic[] = [];

    // 检查 DNA 锚定
    if (vscode.workspace.getConfiguration('cnsh').get<boolean>('enableDNAHighlight', true)) {
        if (!DNA_PATTERN.test(text)) {
            const range = new vscode.Range(0, 0, 0, 1);
            const diag = new vscode.Diagnostic(
                range,
                'CNSH 协议要求：文件缺少 DNA 锚定码。请在文件开头添加 #龍芯⚡️... 格式的追溯码',
                vscode.DiagnosticSeverity.Warning
            );
            diag.code = 'CNSH-MISSING-DNA';
            diagnostics.push(diag);
        }
    }

    // 检查纯英文变量名
    lines.forEach((line, idx) => {
        const varMatch = line.match(/定义\s+([a-zA-Z_][a-zA-Z0-9_]*)/);
        if (varMatch) {
            const varName = varMatch[1];
            // 允许 snake_case 但给出提示
            if (/^[a-z]+(_[a-z]+)*$/.test(varName) && varName.length <= 8) {
                const startIdx = line.indexOf(varName);
                const range = new vscode.Range(idx, startIdx, idx, startIdx + varName.length);
                const diag = new vscode.Diagnostic(
                    range,
                    `CNSH 建议：变量「${varName}」使用英文缩写，建议改为中文语义命名`,
                    vscode.DiagnosticSeverity.Information
                );
                diag.code = 'CNSH-ENGLISH-VAR';
                diagnostics.push(diag);
            }
        }
    });

    // 检查敏感信息泄露
    if (vscode.workspace.getConfiguration('cnsh').get<boolean>('enableSensitiveLeakCheck', true)) {
        for (const sp of SENSITIVE_PATTERNS) {
            let match;
            sp.pattern.lastIndex = 0;
            while ((match = sp.pattern.exec(text)) !== null) {
                const pos = doc.positionAt(match.index);
                const range = new vscode.Range(pos, pos.translate(0, match[0].length));
                const diag = new vscode.Diagnostic(
                    range,
                    `🔴 敏感信息泄露: ${sp.message}`,
                    vscode.DiagnosticSeverity.Error
                );
                diag.code = 'CNSH-SENSITIVE-LEAK';
                diagnostics.push(diag);
            }
        }
    }

    diagCollection.set(doc.uri, diagnostics);

    // 写入审计日志
    writeAuditLog(doc.fileName, diagnostics);
}

// ─── 协议校验 ────────────────────────────────────────────

function checkProtocolOnDocument(doc: vscode.TextDocument) {
    const text = doc.getText();
    const issues: string[] = [];

    // 1. DNA 锚定
    if (!DNA_PATTERN.test(text)) {
        issues.push('缺少 DNA 锚定码');
    }

    // 2. 老祖宗规则检查：是否含违规导入
    if (text.includes('import openai') || text.includes('from openai')) {
        issues.push('直接导入 openai 可能泄露数据到境外');
    }
    if (text.includes('import anthropic') || text.includes('from anthropic')) {
        issues.push('直接导入 anthropic 可能泄露数据到境外');
    }

    // 3. 云端上传检查
    const cloudUploadPatterns = [
        /\.upload\(/g,
        /\.push\(/g,
        /requests\.(post|put)\s*\(\s*['"]https?:\/\/(?!127\.0\.0\.1|localhost)/g,
    ];
    for (const p of cloudUploadPatterns) {
        if (p.test(text)) {
            issues.push('检测到可能的云端上传操作，请确认数据主权');
            break;
        }
    }

    // 4. 敏感信息泄露（复用上面的检查）
    for (const sp of SENSITIVE_PATTERNS) {
        sp.pattern.lastIndex = 0;
        if (sp.pattern.test(text)) {
            issues.push(sp.message);
            break;
        }
    }

    if (issues.length > 0) {
        const msg = issues.join('；');
        vscode.window.showWarningMessage(`🐉 龍魂协议校验: ${msg}`, '一键修复', '忽略').then(choice => {
            if (choice === '一键修复') {
                fixProtocolOnDocument(doc, issues);
            }
        });
    }
}

// ─── 一键修复 ────────────────────────────────────────────

function fixProtocolOnDocument(doc: vscode.TextDocument, issues: string[]) {
    const edit = new vscode.WorkspaceEdit();
    let text = doc.getText();
    let modified = false;

    // 修复 DNA 锚定
    if (!DNA_PATTERN.test(text)) {
        const now = new Date();
        const dna = `#龍芯⚡️丙午·辛未·AUTO-FIX-${now.getHours()}${now.getMinutes()}\n`;
        text = dna + text;
        modified = true;
    }

    // 注释掉敏感导入
    const sensitiveImports = ['import openai', 'from openai', 'import anthropic', 'from anthropic'];
    for (const imp of sensitiveImports) {
        if (text.includes(imp)) {
            text = text.replace(new RegExp(`^${imp}.*$`, 'gm'), (match) => `// 🔴 已禁用: ${match}`);
            modified = true;
        }
    }

    if (modified) {
        const fullRange = new vscode.Range(
            doc.positionAt(0),
            doc.positionAt(doc.getText().length)
        );
        edit.replace(doc.uri, fullRange, text);
        vscode.workspace.applyEdit(edit);
        vscode.window.showInformationMessage('🐉 协议违规已自动修复');
    }
}

// ─── 命令实现 ────────────────────────────────────────────

function runFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'cnsh') {
        vscode.window.showWarningMessage('请先打开一个 .cnsh 文件');
        return;
    }
    const file = editor.document.uri.fsPath;
    execInChannel(`cnsh run "${file}"`);
}

async function compileFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'cnsh') {
        vscode.window.showWarningMessage('请先打开一个 .cnsh 文件');
        return;
    }
    const file = editor.document.uri.fsPath;
    const target = await vscode.window.showQuickPick(
        ['python', 'javascript', 'rust', 'c'],
        { placeHolder: '选择编译目标' }
    );
    if (!target) return;
    const ext = target === 'javascript' ? 'js' : target;
    const out = path.join(path.dirname(file), `${path.basename(file, '.cnsh')}.${ext}`);
    execInChannel(`cnsh compile "${file}" --target ${target} -o "${out}"`);
}

function auditCurrentFile() {
    const editor = vscode.window.activeTextEditor;
    if (editor && editor.document.languageId === 'cnsh') {
        auditDocument(editor.document);
        vscode.window.showInformationMessage('CNSH 变量审计完成');
    }
}

function showDNA() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) return;
    const text = editor.document.getText();
    const match = text.match(DNA_PATTERN);
    if (match) {
        vscode.window.showInformationMessage(`DNA: ${match[0]}`);
    } else {
        vscode.window.showWarningMessage('当前文件未找到 DNA 追溯码。建议添加 #龍芯⚡️... 格式的锚定码');
    }
}

function checkProtocol() {
    const editor = vscode.window.activeTextEditor;
    if (editor && editor.document.languageId === 'cnsh') {
        checkProtocolOnDocument(editor.document);
    }
}

async function fixProtocol() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'cnsh') return;
    const text = editor.document.getText();
    const issues: string[] = [];
    if (!DNA_PATTERN.test(text)) issues.push('缺少 DNA 锚定码');
    fixProtocolOnDocument(editor.document, issues);
}

// ─── 自动补全 ────────────────────────────────────────────

class CnshCompletionProvider implements vscode.CompletionItemProvider {
    provideCompletionItems(
        _document: vscode.TextDocument,
        _position: vscode.Position,
        _token: vscode.CancellationToken,
        _context: vscode.CompletionContext
    ): vscode.CompletionItem[] {
        const items: vscode.CompletionItem[] = [];

        for (const kw of CNSH_KEYWORDS) {
            const item = new vscode.CompletionItem(kw, vscode.CompletionItemKind.Keyword);
            item.insertText = kw;
            item.detail = 'CNSH 关键字';
            items.push(item);
        }

        for (const bi of CNSH_BUILTINS) {
            const item = new vscode.CompletionItem(bi, vscode.CompletionItemKind.Function);
            item.insertText = bi;
            item.detail = 'CNSH 内置函数';
            items.push(item);
        }

        return items;
    }
}

// ─── 工具函数 ────────────────────────────────────────────

function execInChannel(command: string) {
    outputChannel.clear();
    outputChannel.show(true);
    outputChannel.appendLine(`> ${command}`);
    const { exec } = require('child_process');
    exec(command, { encoding: 'utf-8' }, (error: any, stdout: string, stderr: string) => {
        if (stdout) outputChannel.append(stdout);
        if (stderr) outputChannel.append(stderr);
        if (error) {
            outputChannel.appendLine(`[exit ${error.code}]`);
        } else {
            outputChannel.appendLine('[done]');
        }
    });
}

function writeAuditLog(fileName: string, diagnostics: vscode.Diagnostic[]) {
    try {
        const config = vscode.workspace.getConfiguration('cnsh');
        const auditPath = config.get<string>('auditOutputPath') ||
            path.join(
                vscode.workspace.workspaceFolders?.[0]?.uri.fsPath || process.env.HOME || '.',
                'logs', 'cnsh_audit.jsonl'
            );

        const dir = path.dirname(auditPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }

        const entry = {
            timestamp: new Date().toISOString(),
            file: fileName,
            issue_count: diagnostics.length,
            issues: diagnostics.map(d => ({
                severity: d.severity === vscode.DiagnosticSeverity.Error ? 'error' :
                          d.severity === vscode.DiagnosticSeverity.Warning ? 'warning' : 'info',
                message: d.message,
                code: d.code,
            })),
        };

        fs.appendFileSync(auditPath, JSON.stringify(entry) + '\n', 'utf-8');
    } catch {
        // 静默失败，不影响编辑器
    }
}
