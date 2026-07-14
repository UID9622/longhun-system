// entry/src/main/ets/hotkey/HotkeyManager.ets
// 龍魂 · 全局热键管理器 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { pcState, HotkeyDefinition, ModifierKey } from '../models/PCModel';

export class HotkeyManager {
  private static instance: HotkeyManager;
  private registeredHotkeys: Map<string, HotkeyDefinition> = new Map();

  static getInstance(): HotkeyManager {
    if (!HotkeyManager.instance) {
      HotkeyManager.instance = new HotkeyManager();
    }
    return HotkeyManager.instance;
  }

  // 初始化默认热键
  initDefaultHotkeys(): void {
    // 显示/隐藏主窗口
    this.registerHotkey(new HotkeyDefinition({
      id: 'hotkey_toggle_window',
      name: '显示/隐藏窗口',
      modifiers: [ModifierKey.CTRL, ModifierKey.SHIFT],
      key: 'S',
      description: '切换主窗口显示状态',
      scope: 'global',
      action: () => { this.toggleWindow(); }
    }));

    // 快速搜索
    this.registerHotkey(new HotkeyDefinition({
      id: 'hotkey_quick_search',
      name: '快速搜索',
      modifiers: [ModifierKey.CTRL, ModifierKey.SHIFT],
      key: 'F',
      description: '打开快速搜索',
      scope: 'global',
      action: () => { this.openQuickSearch(); }
    }));

    // 新建项目
    this.registerHotkey(new HotkeyDefinition({
      id: 'hotkey_new_project',
      name: '新建项目',
      modifiers: [ModifierKey.CTRL],
      key: 'N',
      description: '新建项目',
      scope: 'app',
      action: () => { console.info('[龍魂] 热键 → 新建项目'); }
    }));

    // 打开里程碑
    this.registerHotkey(new HotkeyDefinition({
      id: 'hotkey_open_milestone',
      name: '打开里程碑',
      modifiers: [ModifierKey.CTRL, ModifierKey.SHIFT],
      key: 'M',
      description: '打开里程碑时间线',
      scope: 'app',
      action: () => { console.info('[龍魂] 热键 → 里程碑'); }
    }));

    // 打开周报
    this.registerHotkey(new HotkeyDefinition({
      id: 'hotkey_open_weekly',
      name: '打开周报',
      modifiers: [ModifierKey.CTRL, ModifierKey.SHIFT],
      key: 'W',
      description: '打开周报管理',
      scope: 'app',
      action: () => { console.info('[龍魂] 热键 → 周报'); }
    }));

    // 截图
    this.registerHotkey(new HotkeyDefinition({
      id: 'hotkey_screenshot',
      name: '截图',
      modifiers: [ModifierKey.CTRL, ModifierKey.SHIFT],
      key: 'P',
      description: '截取屏幕',
      scope: 'global',
      action: () => { this.takeScreenshot(); }
    }));

    // 锁定
    this.registerHotkey(new HotkeyDefinition({
      id: 'hotkey_lock_app',
      name: '锁定应用',
      modifiers: [ModifierKey.CTRL, ModifierKey.ALT],
      key: 'L',
      description: '锁定应用',
      scope: 'global',
      action: () => { this.lockApp(); }
    }));

    // 退出
    this.registerHotkey(new HotkeyDefinition({
      id: 'hotkey_exit_app',
      name: '退出应用',
      modifiers: [ModifierKey.CTRL],
      key: 'Q',
      description: '退出应用',
      scope: 'global',
      action: () => { this.exitApp(); }
    }));

    console.info('[龍魂] 默认热键已初始化 · 8个热键');
  }

  // 注册热键
  registerHotkey(hotkey: HotkeyDefinition): boolean {
    if (!hotkey.isValid()) {
      console.error(`[龍魂] 热键无效: ${hotkey.name}`);
      return false;
    }

    // 检查冲突
    const conflict = this.findConflict(hotkey);
    if (conflict) {
      console.warn(`[龍魂] 热键冲突: ${hotkey.name} 与 ${conflict.name}`);
      return false;
    }

    this.registeredHotkeys.set(hotkey.id, hotkey);
    pcState.registerHotkey(hotkey);

    console.info(`[龍魂] 热键注册: ${hotkey.name} (${hotkey.getDisplayText()})`);
    return true;
  }

  // 注销热键
  unregisterHotkey(id: string): void {
    const hotkey = this.registeredHotkeys.get(id);
    if (hotkey) {
      this.registeredHotkeys.delete(id);
      pcState.unregisterHotkey(id);
      console.info(`[龍魂] 热键注销: ${hotkey.name}`);
    }
  }

  // 查找冲突
  findConflict(hotkey: HotkeyDefinition): HotkeyDefinition | undefined {
    for (const [id, existing] of this.registeredHotkeys) {
      if (existing.key === hotkey.key &&
        existing.modifiers.length === hotkey.modifiers.length &&
        existing.modifiers.every(m => hotkey.modifiers.includes(m))) {
        return existing;
      }
    }
    return undefined;
  }

  // 获取所有热键
  getAllHotkeys(): HotkeyDefinition[] {
    return Array.from(this.registeredHotkeys.values());
  }

  // 切换窗口
  private toggleWindow(): void {
    const win = pcState.windows.get(pcState.activeWindowId);
    if (win) {
      if (win.state === 'hidden') {
        win.restoreFromTray();
        console.info('[龍魂] 热键 → 恢复窗口');
      } else {
        win.minimizeToTray();
        console.info('[龍魂] 热键 → 最小化到托盘');
      }
    }
  }

  // 快速搜索
  private openQuickSearch(): void {
    console.info('[龍魂] 热键 → 快速搜索');
    AppStorage.setOrCreate('show_quick_search', true);
  }

  // 截图
  private takeScreenshot(): void {
    console.info('[龍魂] 热键 → 截图');
  }

  // 锁定应用
  private lockApp(): void {
    console.info('[龍魂] 热键 → 锁定应用');
    AppStorage.setOrCreate('app_locked', true);
  }

  // 退出应用
  private exitApp(): void {
    console.info('[龍魂] 热键 → 退出应用');
    pcState.persist();
  }
}

// 全局单例
export const hotkeyManager = HotkeyManager.getInstance();
