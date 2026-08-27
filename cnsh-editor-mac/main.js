#!/usr/bin/env node
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 🐉 龍魂 · Mac中文代码编辑器 v1.0
 * DNA: #龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-CNSH-EDITOR-UID9622
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 * GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

const { app, BrowserWindow, Menu, ipcMain, dialog } = require('electron');
const path = require('path');
const fs = require('fs-extra');
const { exec } = require('child_process');
const crypto = require('crypto');

// 龍魂环境变量
const LONGHUN_HOME = process.env.HOME + '/.longhun';
const CONFIRM = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z';
const GPG = 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F';

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    titleBarStyle: 'hiddenInset',
    backgroundColor: '#0a0a14',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, 'assets', 'icon.icns')
  });

  mainWindow.loadFile(path.join(__dirname, 'src', 'editor', 'index.html'));

  // 创建菜单
  const template = [
    {
      label: '龍魂编辑器',
      submenu: [
        { label: '关于龍魂编辑器', role: 'about' },
        { type: 'separator' },
        { label: '偏好设置', accelerator: 'CmdOrCtrl+,', click: () => {} },
        { type: 'separator' },
        { label: '退出', accelerator: 'CmdOrCtrl+Q', role: 'quit' }
      ]
    },
    {
      label: '文件',
      submenu: [
        { label: '新建', accelerator: 'CmdOrCtrl+N', click: () => mainWindow.webContents.send('menu-new') },
        { label: '打开', accelerator: 'CmdOrCtrl+O', click: () => mainWindow.webContents.send('menu-open') },
        { label: '保存', accelerator: 'CmdOrCtrl+S', click: () => mainWindow.webContents.send('menu-save') },
        { label: '另存为', accelerator: 'CmdOrCtrl+Shift+S', click: () => mainWindow.webContents.send('menu-save-as') },
        { type: 'separator' },
        { label: '导出为C代码', click: () => mainWindow.webContents.send('menu-export-c') }
      ]
    },
    {
      label: '编辑',
      submenu: [
        { label: '撤销', accelerator: 'CmdOrCtrl+Z', role: 'undo' },
        { label: '重做', accelerator: 'CmdOrCtrl+Shift+Z', role: 'redo' },
        { type: 'separator' },
        { label: '剪切', accelerator: 'CmdOrCtrl+X', role: 'cut' },
        { label: '复制', accelerator: 'CmdOrCtrl+C', role: 'copy' },
        { label: '粘贴', accelerator: 'CmdOrCtrl+V', role: 'paste' },
        { type: 'separator' },
        { label: '全选', accelerator: 'CmdOrCtrl+A', role: 'selectAll' }
      ]
    },
    {
      label: '视图',
      submenu: [
        { label: '开发者工具', accelerator: 'CmdOrCtrl+Shift+I', click: () => mainWindow.webContents.openDevTools() },
        { label: '重新加载', accelerator: 'CmdOrCtrl+R', click: () => mainWindow.reload() }
      ]
    },
    {
      label: '龍魂',
      submenu: [
        { label: '生成DNA追溯码', click: () => mainWindow.webContents.send('menu-generate-dna') },
        { label: '三色审计', click: () => mainWindow.webContents.send('menu-audit') },
        { type: 'separator' },
        { label: '同步到鲲鹏', click: () => mainWindow.webContents.send('menu-sync-kunpeng') },
        { label: '同步到Notion', click: () => mainWindow.webContents.send('menu-sync-notion') }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  // 确保龍魂环境存在
  ensureLonghunEnvironment();
  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});

// ============================================================
// IPC 通信处理
// ============================================================

ipcMain.handle('save-file', async (event, { content, path: filePath }) => {
  try {
    if (filePath) {
      await fs.writeFile(filePath, content, 'utf-8');
      return { success: true, path: filePath };
    } else {
      // 打开保存对话框
      const result = await dialog.showSaveDialog(mainWindow, {
        title: '保存CNSH文件',
        filters: [{ name: 'CNSH文件', extensions: ['cnsh'] }],
        defaultExtension: 'cnsh'
      });
      if (result.canceled) return { success: false };
      await fs.writeFile(result.filePath, content, 'utf-8');
      return { success: true, path: result.filePath };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('open-file', async () => {
  const result = await dialog.showOpenDialog(mainWindow, {
    title: '打开CNSH文件',
    filters: [
      { name: 'CNSH文件', extensions: ['cnsh'] },
      { name: '所有文件', extensions: ['*'] }
    ],
    properties: ['openFile']
  });
  if (result.canceled) return null;
  const content = await fs.readFile(result.filePaths[0], 'utf-8');
  return { path: result.filePaths[0], content };
});

ipcMain.handle('generate-dna', async (event, { content, module }) => {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const h = crypto.createHash('sha256').update(content + Date.now().toString()).digest('hex').substring(0, 8).toUpperCase();
  const dna = `#龍芯⚡️${year}-${month}-${day}-${module || 'EDITOR'}-${h}-UID9622`;
  return dna;
});

ipcMain.handle('audit-content', async (event, { content }) => {
  // 三色审计逻辑
  let score = 0;
  const issues = [];

  // 检查DNA
  if (!content.includes('#龍芯⚡️')) {
    issues.push('缺少DNA追溯码');
    score -= 20;
  }
  // 检查确认码
  if (!content.includes('#CONFIRM🌌')) {
    issues.push('缺少确认码');
    score -= 15;
  }
  // 检查关键字
  const keywords = ['函数', '类', '如果', '循环', '返回'];
  let hasKeyword = false;
  for (const kw of keywords) {
    if (content.includes(kw)) { hasKeyword = true; break; }
  }
  if (!hasKeyword) {
    issues.push('未检测到CNSH关键字');
    score -= 10;
  }

  let color, status;
  if (score >= 70) { color = '🟢'; status = '通过'; }
  else if (score >= 40) { color = '🟡'; status = '警告'; }
  else { color = '🔴'; status = '失败'; }

  return { color, status, score: Math.max(0, score), issues };
});

ipcMain.handle('compile-to-c', async (event, { content }) => {
  // CNSH → C 语言转译
  const mapping = {
    '函数': 'void',
    '类': 'struct',
    '如果': 'if',
    '否则': 'else',
    '循环': 'for',
    '当': 'while',
    '返回': 'return',
    '整数': 'int',
    '文本': 'char*',
    '列表': 'array'
  };

  let c_code = '// 由龍魂CNSH编译器生成\n// DNA: 自动注入\n\n#include <stdio.h>\n\n';
  let lines = content.split('\n');
  for (const line of lines) {
    let c_line = line;
    for (const [cnsh, c] of Object.entries(mapping)) {
      c_line = c_line.replace(new RegExp(cnsh, 'g'), c);
    }
    c_code += c_line + '\n';
  }
  return c_code;
});

ipcMain.handle('sync-kunpeng', async (event, { content, filename }) => {
  // 同步到鲲鹏（仅在龍魂环境已配置 SSH 时可用）
  return new Promise((resolve) => {
    const name = filename || 'untitled.cnsh';
    const localPath = path.join(app.getPath('temp'), name);
    fs.writeFileSync(localPath, content, 'utf-8');
    exec(`scp ${JSON.stringify(localPath)} root@119.13.90.27:/opt/longhun/shared/editor/ 2>&1`, (err, stdout, stderr) => {
      if (err) resolve({ success: false, error: stderr || err.message });
      else resolve({ success: true, message: stdout });
    });
  });
});

// ============================================================
// 龍魂环境初始化
// ============================================================

function ensureLonghunEnvironment() {
  const dirs = [
    `${LONGHUN_HOME}`,
    `${LONGHUN_HOME}/env`,
    `${LONGHUN_HOME}/memory`,
    `${LONGHUN_HOME}/state`,
    `${LONGHUN_HOME}/apps/cnsh-editor`
  ];
  for (const dir of dirs) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }

  // 创建环境变量文件
  const envFile = `${LONGHUN_HOME}/env.sh`;
  if (!fs.existsSync(envFile)) {
    fs.writeFileSync(envFile, `#!/bin/bash
# 🐉 龍魂统一环境
export LONGHUN_HOME="${LONGHUN_HOME}"
export CNSH_EDITOR_HOME="${LONGHUN_HOME}/apps/cnsh-editor"
export DNA_PREFIX="#龍芯⚡️"
export CONFIRM="${CONFIRM}"
export GPG="${GPG}"
`);
  }
}
