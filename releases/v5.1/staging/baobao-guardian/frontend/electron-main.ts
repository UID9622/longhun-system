// ╔══════════════════════════════════════════════════════════════════╗
// ║     宝宝守护助手 · Electron主进程                                ║
// ║     UID9622 · 龍魂系统核心                                       ║
// ╚══════════════════════════════════════════════════════════════════╝
// DNA:#龍芯⚡️2026-06-04-BAOBAO-ELECTRON-FILE1-v1.0

import { app, BrowserWindow, Menu, ipcMain } from 'electron';
import isDev from 'electron-is-dev';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow: BrowserWindow | null = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      preload: path.join(__dirname, 'preload.ts'),
      nodeIntegration: false,
      contextIsolation: true,
    },
    icon: path.join(__dirname, 'assets/icon.png'),
    show: false,
  });

  const startUrl = isDev
    ? 'http://localhost:5173'
    : `file://${path.join(__dirname, '../dist/index.html')}`;

  mainWindow.loadURL(startUrl);

  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.once('ready-to-show', () => {
    mainWindow?.show();
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// IPC处理
ipcMain.handle('get-version', () => {
  return app.getVersion();
});

ipcMain.handle('get-app-path', () => {
  return app.getAppPath();
});

// 创建菜单
const template: any[] = [
  {
    label: '宝宝守护助手',
    submenu: [
      { role: 'about', label: '关于' },
      { type: 'separator' },
      { role: 'quit', label: '退出' },
    ],
  },
  {
    label: '编辑',
    submenu: [
      { role: 'undo', label: '撤销' },
      { role: 'redo', label: '重做' },
      { type: 'separator' },
      { role: 'cut', label: '剪切' },
      { role: 'copy', label: '复制' },
      { role: 'paste', label: '粘贴' },
    ],
  },
  {
    label: '开发',
    submenu: [
      { role: 'toggleDevTools', label: '开发者工具' },
      { role: 'reload', label: '重新加载' },
      { role: 'forceReload', label: '强制重新加载' },
    ],
  },
];

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);
