# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// CNSH v2.1 VS Code / Cursor 插件
// DNA:#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-CNSH-VSCODE-FILE1-v0.1.0

import * as vscode from 'vscode';
import { LanguageClient, LanguageClientOptions, ServerOptions, TransportKind } from 'vscode-languageclient/node';
import { exec, ExecException } from 'child_process';
import * as path from 'path';

let client: LanguageClient | undefined;
let outputChannel: vscode.OutputChannel;

export function activate(context: vscode.ExtensionContext) {
    outputChannel = vscode.window.createOutputChannel('CNSH');

    // 启动 LSP 客户端
    const serverOptions: ServerOptions = {
        command: 'cnsh',
        args: ['lsp', '--stdio'],
        transport: TransportKind.stdio,
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'cnsh' }],
        outputChannel,
    };

    client = new LanguageClient('cnsh', 'CNSH Language Server', serverOptions, clientOptions);
    client.start();

    // 注册命令
    context.subscriptions.push(
        vscode.commands.registerCommand('cnsh.runFile', runFile),
        vscode.commands.registerCommand('cnsh.compileFile', compileFile),
        outputChannel
    );
}

export function deactivate(): Thenable<void> | undefined {
    return client ? client.stop() : undefined;
}

function runFile() {
    const editor = vscode.window.activeTextEditor;
    if (!editor || editor.document.languageId !== 'cnsh') {
        vscode.window.showWarningMessage('请先打开一个 .cnsh 文件');
        return;
    }
    const file = editor.document.uri.fsPath;
    execCmd(`cnsh run "${file}"`);
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
    if (!target) { return; }
    const ext = target === 'javascript' ? 'js' : target;
    const out = path.join(path.dirname(file), `${path.basename(file, '.cnsh')}.${ext}`);
    execCmd(`cnsh compile "${file}" --target ${target} -o "${out}"`);
}

function execCmd(command: string) {
    outputChannel.clear();
    outputChannel.show(true);
    outputChannel.appendLine(`> ${command}`);
    exec(command, { encoding: 'utf-8' }, (error: ExecException | null, stdout: string, stderr: string) => {
        if (stdout) { outputChannel.append(stdout); }
        if (stderr) { outputChannel.append(stderr); }
        if (error) {
            outputChannel.appendLine(`[exit ${error.code}]`);
        } else {
            outputChannel.appendLine('[done]');
        }
    });
}
