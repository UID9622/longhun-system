/**
 * 🐉 龍魂 · CNSH编辑器预加载脚本
 * 安全桥接: contextIsolation=true 下暴露最小 API 给渲染进程
 * DNA: #龍芯⚡️丙午·丙申·辛酉·丑时-CNSH-EDITOR-PRELOAD-UID9622
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

const { contextBridge, ipcRenderer } = require('electron');

// 只暴露白名单 API · 不开放 ipcRenderer 本体（安全铁律）
contextBridge.exposeInMainWorld('cnshAPI', {
  saveFile: (payload) => ipcRenderer.invoke('save-file', payload),
  openFile: () => ipcRenderer.invoke('open-file'),
  generateDna: (payload) => ipcRenderer.invoke('generate-dna', payload),
  auditContent: (payload) => ipcRenderer.invoke('audit-content', payload),
  compileToC: (payload) => ipcRenderer.invoke('compile-to-c', payload),
  syncKunpeng: (payload) => ipcRenderer.invoke('sync-kunpeng', payload),
  // 菜单事件订阅
  onMenu: (callback) => {
    const handlers = {
      'menu-new': () => callback('new'),
      'menu-open': () => callback('open'),
      'menu-save': () => callback('save'),
      'menu-save-as': () => callback('save-as'),
      'menu-export-c': () => callback('export-c'),
      'menu-generate-dna': () => callback('generate-dna'),
      'menu-audit': () => callback('audit'),
      'menu-sync-kunpeng': () => callback('sync-kunpeng'),
      'menu-sync-notion': () => callback('sync-notion')
    };
    Object.keys(handlers).forEach((channel) => {
      ipcRenderer.on(channel, handlers[channel]);
    });
  },
  // 龍魂环境信息
  getEnv: () => ({
    LONGHUN_HOME: process.env.HOME + '/.longhun',
    CONFIRM: '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z',
    GPG: 'A2D0092CEE2E5BA87035600924C3704A8CC26D5F'
  })
});
