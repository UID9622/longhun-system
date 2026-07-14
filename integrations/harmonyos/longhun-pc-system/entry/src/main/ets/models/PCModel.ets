// entry/src/main/ets/models/PCModel.ets
// 龍魂 · PC应用模型层 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

// === DNA常量 ===
export const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
export const MASTER_UID = "9622";
export const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 窗口状态 ===
export enum WindowState {
  NORMAL = 'normal',
  MINIMIZED = 'minimized',
  MAXIMIZED = 'maximized',
  FULLSCREEN = 'fullscreen',
  HIDDEN = 'hidden'
}

// === 通知级别 ===
export enum NotificationLevel {
  SILENT = 'silent',
  NORMAL = 'normal',
  URGENT = 'urgent',
  CRITICAL = 'critical'
}

// === 托盘菜单类型 ===
export enum TrayMenuType {
  ITEM = 'item',
  SEPARATOR = 'separator',
  SUBMENU = 'submenu',
  CHECKBOX = 'checkbox',
  RADIO = 'radio'
}

// === 热键修饰键 ===
export enum ModifierKey {
  CTRL = 'Ctrl',
  ALT = 'Alt',
  SHIFT = 'Shift',
  META = 'Meta',
  FN = 'Fn'
}

// === 窗口档案 ===
export class WindowProfile {
  id: string;
  title: string;
  state: WindowState;
  x: number;
  y: number;
  width: number;
  height: number;
  displayId: number;
  isPrimary: boolean;
  isAlwaysOnTop: boolean;
  isTransparent: boolean;
  opacity: number;
  dnaSignature: string;

  constructor(data: Partial<WindowProfile> = {}) {
    this.id = data.id || `WIN-${Date.now()}`;
    this.title = data.title || '龍魂PC应用';
    this.state = data.state || WindowState.NORMAL;
    this.x = data.x || 100;
    this.y = data.y || 100;
    this.width = data.width || 1280;
    this.height = data.height || 720;
    this.displayId = data.displayId || 0;
    this.isPrimary = data.isPrimary || true;
    this.isAlwaysOnTop = data.isAlwaysOnTop || false;
    this.isTransparent = data.isTransparent || false;
    this.opacity = data.opacity || 1.0;
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.title}-${this.state}-${this.x}-${this.y}`;
    let hash = 0;
    for (let i = 0; i < payload.length; i++) {
      hash = ((hash << 5) - hash) + payload.charCodeAt(i);
      hash |= 0;
    }
    return `SM3-${Math.abs(hash).toString(16).substring(0, 16)}`;
  }

  minimizeToTray(): void {
    this.state = WindowState.HIDDEN;
  }

  restoreFromTray(): void {
    this.state = WindowState.NORMAL;
  }

  maximize(): void {
    this.state = WindowState.MAXIMIZED;
  }

  fullscreen(): void {
    this.state = WindowState.FULLSCREEN;
  }

  setAlwaysOnTop(value: boolean): void {
    this.isAlwaysOnTop = value;
  }

  setOpacity(value: number): void {
    this.opacity = Math.max(0.1, Math.min(1.0, value));
  }

  moveToDisplay(displayId: number): void {
    this.displayId = displayId;
  }

  toBounds(): { x: number; y: number; width: number; height: number } {
    return { x: this.x, y: this.y, width: this.width, height: this.height };
  }
}

// === 通知操作 ===
export interface NotificationAction {
  id: string;
  label: string;
  icon?: string;
  type: 'primary' | 'secondary' | 'danger';
  callback: () => void;
}

// === 通知消息 ===
export class NotificationMessage {
  id: string;
  title: string;
  content: string;
  level: NotificationLevel;
  source: string;
  sourceIcon: string;
  timestamp: Date;
  expireAt?: Date;
  actions: NotificationAction[];
  isRead: boolean;
  isPinned: boolean;
  dnaSignature: string;

  constructor(data: Partial<NotificationMessage> = {}) {
    this.id = data.id || `NOTIFY-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;
    this.title = data.title || '通知';
    this.content = data.content || '';
    this.level = data.level || NotificationLevel.NORMAL;
    this.source = data.source || '龍魂系统';
    this.sourceIcon = data.sourceIcon || '🐉';
    this.timestamp = data.timestamp || new Date();
    this.expireAt = data.expireAt;
    this.actions = data.actions || [];
    this.isRead = data.isRead || false;
    this.isPinned = data.isPinned || false;
    this.dnaSignature = this.signData();
  }

  private signData(): string {
    const payload = `${this.id}-${this.title}-${this.level}-${this.timestamp.getTime()}`;
    let hash = 0;
    for (let i = 0; i < payload.length; i++) {
      hash = ((hash << 5) - hash) + payload.charCodeAt(i);
      hash |= 0;
    }
    return `SM3-${Math.abs(hash).toString(16).substring(0, 16)}`;
  }

  markAsRead(): void {
    this.isRead = true;
  }

  togglePin(): void {
    this.isPinned = !this.isPinned;
  }

  isExpired(): boolean {
    if (!this.expireAt) return false;
    return new Date() > this.expireAt;
  }

  getLevelColor(): string {
    switch (this.level) {
      case NotificationLevel.SILENT: return '#666666';
      case NotificationLevel.NORMAL: return '#0066cc';
      case NotificationLevel.URGENT: return '#ff6600';
      case NotificationLevel.CRITICAL: return '#c41e3a';
      default: return '#666666';
    }
  }

  getLevelIcon(): string {
    switch (this.level) {
      case NotificationLevel.SILENT: return '🔕';
      case NotificationLevel.NORMAL: return '🔔';
      case NotificationLevel.URGENT: return '⚠️';
      case NotificationLevel.CRITICAL: return '🚨';
      default: return '🔔';
    }
  }
}

// === 托盘菜单项 ===
export class TrayMenuItem {
  id: string;
  type: TrayMenuType;
  label: string;
  icon?: string;
  shortcut?: string;
  isChecked?: boolean;
  isEnabled: boolean;
  children?: TrayMenuItem[];
  action?: () => void;

  constructor(data: Partial<TrayMenuItem> = {}) {
    this.id = data.id || `MENU-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;
    this.type = data.type || TrayMenuType.ITEM;
    this.label = data.label || '';
    this.icon = data.icon;
    this.shortcut = data.shortcut;
    this.isChecked = data.isChecked;
    this.isEnabled = data.isEnabled !== false;
    this.children = data.children;
    this.action = data.action;
  }

  static separator(): TrayMenuItem {
    return new TrayMenuItem({ type: TrayMenuType.SEPARATOR });
  }

  static submenu(label: string, children: TrayMenuItem[]): TrayMenuItem {
    return new TrayMenuItem({ type: TrayMenuType.SUBMENU, label, children });
  }
}

// === 热键定义 ===
export class HotkeyDefinition {
  id: string;
  name: string;
  modifiers: ModifierKey[];
  key: string;
  description: string;
  scope: 'global' | 'window' | 'app';
  action: () => void;
  isEnabled: boolean;

  constructor(data: Partial<HotkeyDefinition> = {}) {
    this.id = data.id || `HOTKEY-${Date.now()}`;
    this.name = data.name || '';
    this.modifiers = data.modifiers || [];
    this.key = data.key || '';
    this.description = data.description || '';
    this.scope = data.scope || 'global';
    this.action = data.action || (() => {});
    this.isEnabled = data.isEnabled !== false;
  }

  getDisplayText(): string {
    const mods = this.modifiers.map(m => {
      switch (m) {
        case ModifierKey.CTRL: return 'Ctrl';
        case ModifierKey.ALT: return 'Alt';
        case ModifierKey.SHIFT: return 'Shift';
        case ModifierKey.META: return 'Win';
        case ModifierKey.FN: return 'Fn';
      }
    }).join('+');
    return mods ? `${mods}+${this.key}` : this.key;
  }

  isValid(): boolean {
    return this.key.length > 0 && (this.modifiers.length > 0 || this.key.length === 1);
  }
}

// === 显示器信息 ===
export interface DisplayInfo {
  id: number;
  name: string;
  width: number;
  height: number;
  x: number;
  y: number;
  isPrimary: boolean;
  scaleFactor: number;
}

// === PC统计 ===
export interface PCStats {
  totalWindows: number;
  visibleWindows: number;
  totalNotifications: number;
  unreadNotifications: number;
  pinnedNotifications: number;
  totalHotkeys: number;
  activeHotkeys: number;
  clipboardItems: number;
  displayCount: number;
}

// === PC全局状态 ===
@Observed
export class PCState {
  windows: Map<string, WindowProfile> = new Map();
  activeWindowId: string = '';
  notifications: NotificationMessage[] = [];
  unreadCount: number = 0;
  trayIcon: string = '🐉';
  trayTooltip: string = '龍魂系统';
  trayMenu: TrayMenuItem[] = [];
  isTrayVisible: boolean = true;
  hotkeys: Map<string, HotkeyDefinition> = new Map();
  clipboardHistory: string[] = [];
  maxClipboardHistory: number = 50;
  displays: DisplayInfo[] = [];
  primaryDisplayId: number = 0;

  get statistics(): PCStats {
    return {
      totalWindows: this.windows.size,
      visibleWindows: Array.from(this.windows.values()).filter(w => w.state !== WindowState.HIDDEN).length,
      totalNotifications: this.notifications.length,
      unreadNotifications: this.notifications.filter(n => !n.isRead).length,
      pinnedNotifications: this.notifications.filter(n => n.isPinned).length,
      totalHotkeys: this.hotkeys.size,
      activeHotkeys: Array.from(this.hotkeys.values()).filter(h => h.isEnabled).length,
      clipboardItems: this.clipboardHistory.length,
      displayCount: this.displays.length
    };
  }

  createWindow(profile: WindowProfile): void {
    this.windows.set(profile.id, profile);
    this.activeWindowId = profile.id;
  }

  closeWindow(id: string): void {
    this.windows.delete(id);
    if (this.activeWindowId === id) {
      const keys = Array.from(this.windows.keys());
      this.activeWindowId = keys.length > 0 ? keys[0] : '';
    }
  }

  minimizeToTray(id: string): void {
    const win = this.windows.get(id);
    if (win) {
      win.minimizeToTray();
    }
  }

  sendNotification(notification: NotificationMessage): void {
    this.notifications.unshift(notification);
    if (this.notifications.length > 100) {
      this.notifications = this.notifications.slice(0, 100);
    }
    this.updateUnreadCount();
  }

  markAsRead(id: string): void {
    const notification = this.notifications.find(n => n.id === id);
    if (notification) {
      notification.markAsRead();
      this.updateUnreadCount();
    }
  }

  markAllAsRead(): void {
    this.notifications.forEach(n => n.markAsRead());
    this.updateUnreadCount();
  }

  clearNotifications(): void {
    this.notifications = this.notifications.filter(n => n.isPinned);
    this.updateUnreadCount();
  }

  private updateUnreadCount(): void {
    this.unreadCount = this.notifications.filter(n => !n.isRead).length;
  }

  registerHotkey(hotkey: HotkeyDefinition): boolean {
    if (!hotkey.isValid()) return false;
    this.hotkeys.set(hotkey.id, hotkey);
    return true;
  }

  unregisterHotkey(id: string): void {
    this.hotkeys.delete(id);
  }

  recordClipboard(text: string): void {
    if (this.clipboardHistory.includes(text)) {
      this.clipboardHistory = this.clipboardHistory.filter(t => t !== text);
    }
    this.clipboardHistory.unshift(text);
    if (this.clipboardHistory.length > this.maxClipboardHistory) {
      this.clipboardHistory = this.clipboardHistory.slice(0, this.maxClipboardHistory);
    }
  }

  getClipboardHistory(): string[] {
    return [...this.clipboardHistory];
  }

  persist(): void {
    AppStorage.setOrCreate('pc_windows', JSON.stringify(Array.from(this.windows.entries())));
    AppStorage.setOrCreate('pc_notifications', JSON.stringify(this.notifications.slice(0, 50)));
    AppStorage.setOrCreate('pc_hotkeys', JSON.stringify(Array.from(this.hotkeys.entries())));
    AppStorage.setOrCreate('pc_clipboard', JSON.stringify(this.clipboardHistory.slice(0, 20)));
  }

  load(): void {
    // 从 AppStorage 加载持久化数据
    try {
      const windowsData = AppStorage.get<string>('pc_windows');
      if (windowsData) {
        const entries = JSON.parse(windowsData);
        this.windows = new Map(entries);
      }
      const notificationsData = AppStorage.get<string>('pc_notifications');
      if (notificationsData) {
        this.notifications = JSON.parse(notificationsData);
      }
      const hotkeysData = AppStorage.get<string>('pc_hotkeys');
      if (hotkeysData) {
        this.hotkeys = new Map(JSON.parse(hotkeysData));
      }
      const clipboardData = AppStorage.get<string>('pc_clipboard');
      if (clipboardData) {
        this.clipboardHistory = JSON.parse(clipboardData);
      }
    } catch (e) {
      console.error('[龍魂] 加载PC状态失败', e);
    }
    this.updateUnreadCount();
  }
}

// 全局单例
export const pcState = new PCState();
AppStorage.setOrCreate('pcState', pcState);
