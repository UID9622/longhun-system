# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// #龍芯⚡️丙午·丙申·乙卯·丙戌·䷷旅-CNSH-VSCODE-EXTENSION-v1.0
// CNSH 编辑器避坑插件 · VS Code Extension
// 提供：语法高亮、关键字补全、变量命名审计、编译入口

const vscode = require('vscode');
const fs = require('fs');
const path = require('path');

const CNSH_KEYWORDS = [
  '定义', '函数', '返回', '如果', '否则', '循环', '遍历', '中断', '继续',
  '打印', '输入', '真', '假', '空', '并且', '或者', '非', '导入', '导出'
];

const CNSH_BUILTINS = [
  'DNA检测', '伦理审计', '熔断检查', '日志记录', '哈希', '签名', '验证'
];

function activate(context) {
  const disposables = [];

  // 关键字补全
  disposables.push(
    vscode.languages.registerCompletionItemProvider(
      'cnsh',
      {
        provideCompletionItems(document, position) {
          return [...CNSH_KEYWORDS, ...CNSH_BUILTINS].map(kw => {
            const item = new vscode.CompletionItem(kw, vscode.CompletionItemKind.Keyword);
            item.insertText = kw;
            return item;
          });
        }
      },
      '.'
    )
  );

  // 变量命名审计：检查是否使用中文语义命名
  function auditVariables(document) {
    const text = document.getText();
    const lines = text.split('\n');
    const diagnostics = [];
    const diagCollection = vscode.languages.createDiagnosticCollection('cnsh');
    context.subscriptions.push(diagCollection);

    lines.forEach((line, idx) => {
      const match = line.match(/定义\s+([a-zA-Z_][a-zA-Z0-9_]*)/);
      if (match) {
        const varName = match[1];
        if (/^[a-zA-Z]+$/.test(varName)) {
          const range = new vscode.Range(idx, line.indexOf(varName), idx, line.indexOf(varName) + varName.length);
          const diag = new vscode.Diagnostic(
            range,
            `CNSH 建议：变量「${varName}」使用纯英文缩写，建议改用中文语义命名（如 用户列表、计数器）`,
            vscode.DiagnosticSeverity.Warning
          );
          diag.code = 'CNSH-中文命名';
          diagnostics.push(diag);
        }
      }
    });

    diagCollection.set(document.uri, diagnostics);
  }

  // 保存时自动审计
  disposables.push(
    vscode.workspace.onDidSaveTextDocument(doc => {
      if (doc.languageId === 'cnsh' && vscode.workspace.getConfiguration('cnsh').get('enableAuditOnSave')) {
        auditVariables(doc);
      }
    })
  );

  // 命令：审计变量
  disposables.push(
    vscode.commands.registerCommand('cnsh.auditVariables', () => {
      const editor = vscode.window.activeTextEditor;
      if (editor && editor.document.languageId === 'cnsh') {
        auditVariables(editor.document);
        vscode.window.showInformationMessage('CNSH 变量审计完成');
      }
    })
  );

  // 命令：编译为 C（调用本地 CNSH 编译器）
  disposables.push(
    vscode.commands.registerCommand('cnsh.compileToC', async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor || editor.document.languageId !== 'cnsh') return;
      const filePath = editor.document.fileName;
      const compiler = vscode.workspace.getConfiguration('cnsh').get('compilerPath') || './CNSH编译器/cnsh-compiler.js';
      const terminal = vscode.window.createTerminal('CNSH 编译');
      terminal.sendText(`node "${compiler}" "${filePath}"`);
      terminal.show();
    })
  );

  // 命令：显示 DNA
  disposables.push(
    vscode.commands.registerCommand('cnsh.showDNA', () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) return;
      const text = editor.document.getText();
      const match = text.match(/#龍芯⚡️[\u4e00-\u9fa5·䷀-䷿\-A-Za-z0-9]+/);
      vscode.window.showInformationMessage(match ? `DNA: ${match[0]}` : '当前文件未找到 DNA 追溯码');
    })
  );

  disposables.forEach(d => context.subscriptions.push(d));
}

function deactivate() {}

module.exports = { activate, deactivate };
