"use strict";
// CNSH v2.1 VS Code / Cursor 插件
// DNA: #龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-CNSH-VSCODE-v0.1.0
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const node_1 = require("vscode-languageclient/node");
const child_process_1 = require("child_process");
const path = __importStar(require("path"));
let client;
let outputChannel;
function activate(context) {
    outputChannel = vscode.window.createOutputChannel('CNSH');
    // 启动 LSP 客户端
    const serverOptions = {
        command: 'cnsh',
        args: ['lsp', '--stdio'],
        transport: node_1.TransportKind.stdio,
    };
    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'cnsh' }],
        outputChannel,
    };
    client = new node_1.LanguageClient('cnsh', 'CNSH Language Server', serverOptions, clientOptions);
    client.start();
    // 注册命令
    context.subscriptions.push(vscode.commands.registerCommand('cnsh.runFile', runFile), vscode.commands.registerCommand('cnsh.compileFile', compileFile), outputChannel);
}
function deactivate() {
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
    const target = await vscode.window.showQuickPick(['python', 'javascript', 'rust', 'c'], { placeHolder: '选择编译目标' });
    if (!target) {
        return;
    }
    const ext = target === 'javascript' ? 'js' : target;
    const out = path.join(path.dirname(file), `${path.basename(file, '.cnsh')}.${ext}`);
    execCmd(`cnsh compile "${file}" --target ${target} -o "${out}"`);
}
function execCmd(command) {
    outputChannel.clear();
    outputChannel.show(true);
    outputChannel.appendLine(`> ${command}`);
    (0, child_process_1.exec)(command, { encoding: 'utf-8' }, (error, stdout, stderr) => {
        if (stdout) {
            outputChannel.append(stdout);
        }
        if (stderr) {
            outputChannel.append(stderr);
        }
        if (error) {
            outputChannel.appendLine(`[exit ${error.code}]`);
        }
        else {
            outputChannel.appendLine('[done]');
        }
    });
}
//# sourceMappingURL=extension.js.map