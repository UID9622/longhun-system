// entry/src/main/ets/database/PCDatabase.ets
// 龍魂 · PC状态持久化数据库 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { relationalStore } from '@kit.ArkData';
import { BusinessError } from '@kit.BasicServicesKit';

const DB_NAME = 'LonghunPC.db';
const DB_VERSION = 1;

// === 表结构SQL ===
const SQL_CREATE_TABLE_WINDOWS = `
  CREATE TABLE IF NOT EXISTS pc_windows (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    state TEXT NOT NULL DEFAULT 'normal',
    x INTEGER DEFAULT 100,
    y INTEGER DEFAULT 100,
    width INTEGER DEFAULT 1280,
    height INTEGER DEFAULT 720,
    display_id INTEGER DEFAULT 0,
    is_primary INTEGER DEFAULT 1,
    is_always_on_top INTEGER DEFAULT 0,
    is_transparent INTEGER DEFAULT 0,
    opacity REAL DEFAULT 1.0,
    dna_signature TEXT,
    created_at TEXT DEFAULT (datetime('now','localtime')),
    updated_at TEXT DEFAULT (datetime('now','localtime'))
  )
`;

const SQL_CREATE_TABLE_NOTIFICATIONS = `
  CREATE TABLE IF NOT EXISTS pc_notifications (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT DEFAULT '',
    level TEXT NOT NULL DEFAULT 'normal',
    source TEXT DEFAULT '龍魂系统',
    source_icon TEXT DEFAULT '🐉',
    timestamp TEXT NOT NULL,
    expire_at TEXT,
    is_read INTEGER DEFAULT 0,
    is_pinned INTEGER DEFAULT 0,
    dna_signature TEXT,
    created_at TEXT DEFAULT (datetime('now','localtime'))
  )
`;

const SQL_CREATE_TABLE_HOTKEYS = `
  CREATE TABLE IF NOT EXISTS pc_hotkeys (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    modifiers TEXT NOT NULL DEFAULT '[]',
    key_code TEXT NOT NULL,
    description TEXT DEFAULT '',
    scope TEXT NOT NULL DEFAULT 'global',
    is_enabled INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now','localtime'))
  )
`;

const SQL_CREATE_TABLE_CLIPBOARD = `
  CREATE TABLE IF NOT EXISTS pc_clipboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    recorded_at TEXT DEFAULT (datetime('now','localtime'))
  )
`;

const SQL_CREATE_TABLE_SETTINGS = `
  CREATE TABLE IF NOT EXISTS pc_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT DEFAULT (datetime('now','localtime'))
  )
`;

// === 索引SQL ===
const SQL_INDEX_NOTIFICATIONS_LEVEL = `
  CREATE INDEX IF NOT EXISTS idx_notifications_level ON pc_notifications(level)
`;
const SQL_INDEX_NOTIFICATIONS_READ = `
  CREATE INDEX IF NOT EXISTS idx_notifications_read ON pc_notifications(is_read)
`;
const SQL_INDEX_NOTIFICATIONS_TIME = `
  CREATE INDEX IF NOT EXISTS idx_notifications_time ON pc_notifications(timestamp DESC)
`;
const SQL_INDEX_CLIPBOARD_TIME = `
  CREATE INDEX IF NOT EXISTS idx_clipboard_time ON pc_clipboard(recorded_at DESC)
`;
const SQL_INDEX_HOTKEYS_ENABLED = `
  CREATE INDEX IF NOT EXISTS idx_hotkeys_enabled ON pc_hotkeys(is_enabled)
`;

export class PCDatabase {
  private static instance: PCDatabase;
  private store: relationalStore.RdbStore | null = null;

  static getInstance(): PCDatabase {
    if (!PCDatabase.instance) {
      PCDatabase.instance = new PCDatabase();
    }
    return PCDatabase.instance;
  }

  // 初始化数据库
  async init(context: Context): Promise<void> {
    const config: relationalStore.StoreConfig = {
      name: DB_NAME,
      securityLevel: relationalStore.SecurityLevel.S3
    };

    try {
      this.store = await relationalStore.getRdbStore(context, config);
      await this.createTables();
      await this.insertSeedData();
      console.info('[龍魂] PC数据库初始化完成');
    } catch (err) {
      const error = err as BusinessError;
      console.error(`[龍魂] PC数据库初始化失败: ${error.message}`);
    }
  }

  // 创建表结构
  private async createTables(): Promise<void> {
    if (!this.store) return;

    const tables = [
      SQL_CREATE_TABLE_WINDOWS,
      SQL_CREATE_TABLE_NOTIFICATIONS,
      SQL_CREATE_TABLE_HOTKEYS,
      SQL_CREATE_TABLE_CLIPBOARD,
      SQL_CREATE_TABLE_SETTINGS,
      SQL_INDEX_NOTIFICATIONS_LEVEL,
      SQL_INDEX_NOTIFICATIONS_READ,
      SQL_INDEX_NOTIFICATIONS_TIME,
      SQL_INDEX_CLIPBOARD_TIME,
      SQL_INDEX_HOTKEYS_ENABLED
    ];

    for (const sql of tables) {
      await this.store.executeSql(sql);
    }
    console.info('[龍魂] 数据库表结构已创建 · 5表 · 5索引');
  }

  // 插入种子数据
  private async insertSeedData(): Promise<void> {
    if (!this.store) return;

    // 默认设置
    const defaultSettings: Array<[string, string]> = [
      ['tray_icon', '🐉'],
      ['tray_tooltip', '龍魂系统'],
      ['theme', 'dark'],
      ['language', 'zh-CN'],
      ['max_notifications', '100'],
      ['max_clipboard', '50'],
      ['auto_start', 'true'],
      ['minimize_to_tray', 'true']
    ];

    for (const [key, value] of defaultSettings) {
      await this.store.executeSql(
        'INSERT OR IGNORE INTO pc_settings (key, value) VALUES (?, ?)',
        [key, value]
      );
    }

    console.info('[龍魂] 种子数据已插入 · 8条设置');
  }

  // === 窗口操作 ===
  async saveWindow(window: {
    id: string; title: string; state: string; x: number; y: number;
    width: number; height: number; displayId: number; isPrimary: number;
    isAlwaysOnTop: number; isTransparent: number; opacity: number; dnaSignature: string;
  }): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql(
      `INSERT OR REPLACE INTO pc_windows
       (id, title, state, x, y, width, height, display_id, is_primary,
        is_always_on_top, is_transparent, opacity, dna_signature, updated_at)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now','localtime'))`,
      [window.id, window.title, window.state, window.x, window.y, window.width, window.height,
       window.displayId, window.isPrimary, window.isAlwaysOnTop, window.isTransparent,
       window.opacity, window.dnaSignature]
    );
  }

  async loadWindows(): Promise<relationalStore.ResultSet> {
    if (!this.store) throw new Error('数据库未初始化');
    return this.store.querySql('SELECT * FROM pc_windows ORDER BY is_primary DESC');
  }

  async deleteWindow(id: string): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql('DELETE FROM pc_windows WHERE id = ?', [id]);
  }

  // === 通知操作 ===
  async saveNotification(notification: {
    id: string; title: string; content: string; level: string;
    source: string; sourceIcon: string; timestamp: string; expireAt: string | null;
    isRead: number; isPinned: number; dnaSignature: string;
  }): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql(
      `INSERT OR REPLACE INTO pc_notifications
       (id, title, content, level, source, source_icon, timestamp, expire_at,
        is_read, is_pinned, dna_signature)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [notification.id, notification.title, notification.content, notification.level,
       notification.source, notification.sourceIcon, notification.timestamp, notification.expireAt,
       notification.isRead, notification.isPinned, notification.dnaSignature]
    );
  }

  async loadNotifications(limit: number = 100): Promise<relationalStore.ResultSet> {
    if (!this.store) throw new Error('数据库未初始化');
    return this.store.querySql(
      'SELECT * FROM pc_notifications ORDER BY timestamp DESC LIMIT ?',
      [limit.toString()]
    );
  }

  async markNotificationRead(id: string): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql(
      'UPDATE pc_notifications SET is_read = 1 WHERE id = ?', [id]
    );
  }

  async markAllNotificationsRead(): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql('UPDATE pc_notifications SET is_read = 1 WHERE is_read = 0');
  }

  async deleteNotification(id: string): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql('DELETE FROM pc_notifications WHERE id = ?', [id]);
  }

  async clearOldNotifications(keepPinned: boolean = true): Promise<void> {
    if (!this.store) return;
    if (keepPinned) {
      await this.store.executeSql('DELETE FROM pc_notifications WHERE is_pinned = 0');
    } else {
      await this.store.executeSql('DELETE FROM pc_notifications');
    }
  }

  async cleanupExpiredNotifications(): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql(
      `DELETE FROM pc_notifications
       WHERE expire_at IS NOT NULL AND datetime(expire_at) < datetime('now','localtime')
         AND is_pinned = 0`
    );
  }

  // === 热键操作 ===
  async saveHotkey(hotkey: {
    id: string; name: string; modifiers: string; keyCode: string;
    description: string; scope: string; isEnabled: number;
  }): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql(
      `INSERT OR REPLACE INTO pc_hotkeys
       (id, name, modifiers, key_code, description, scope, is_enabled)
       VALUES (?, ?, ?, ?, ?, ?, ?)`,
      [hotkey.id, hotkey.name, hotkey.modifiers, hotkey.keyCode,
       hotkey.description, hotkey.scope, hotkey.isEnabled]
    );
  }

  async loadHotkeys(): Promise<relationalStore.ResultSet> {
    if (!this.store) throw new Error('数据库未初始化');
    return this.store.querySql('SELECT * FROM pc_hotkeys ORDER BY scope, name');
  }

  async deleteHotkey(id: string): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql('DELETE FROM pc_hotkeys WHERE id = ?', [id]);
  }

  // === 剪贴板操作 ===
  async saveClipboardItem(content: string): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql(
      'INSERT INTO pc_clipboard (content) VALUES (?)', [content]
    );
    // 保持最大条目数
    await this.store.executeSql(
      `DELETE FROM pc_clipboard WHERE id NOT IN (
        SELECT id FROM pc_clipboard ORDER BY recorded_at DESC LIMIT 50
      )`
    );
  }

  async loadClipboardHistory(limit: number = 20): Promise<relationalStore.ResultSet> {
    if (!this.store) throw new Error('数据库未初始化');
    return this.store.querySql(
      'SELECT * FROM pc_clipboard ORDER BY recorded_at DESC LIMIT ?',
      [limit.toString()]
    );
  }

  async clearClipboardHistory(): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql('DELETE FROM pc_clipboard');
  }

  // === 设置操作 ===
  async getSetting(key: string): Promise<string | null> {
    if (!this.store) return null;
    const result = await this.store.querySql(
      'SELECT value FROM pc_settings WHERE key = ?', [key]
    );
    if (result.goToFirstRow()) {
      return result.getString(0);
    }
    return null;
  }

  async setSetting(key: string, value: string): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql(
      `INSERT OR REPLACE INTO pc_settings (key, value, updated_at)
       VALUES (?, ?, datetime('now','localtime'))`,
      [key, value]
    );
  }

  async loadAllSettings(): Promise<relationalStore.ResultSet> {
    if (!this.store) throw new Error('数据库未初始化');
    return this.store.querySql('SELECT * FROM pc_settings ORDER BY key');
  }

  // === 统计查询 ===
  async getStats(): Promise<{
    totalWindows: number;
    totalNotifications: number;
    unreadNotifications: number;
    totalHotkeys: number;
    clipboardItems: number;
  }> {
    if (!this.store) return { totalWindows: 0, totalNotifications: 0, unreadNotifications: 0, totalHotkeys: 0, clipboardItems: 0 };

    const stats = { totalWindows: 0, totalNotifications: 0, unreadNotifications: 0, totalHotkeys: 0, clipboardItems: 0 };

    let result = await this.store.querySql('SELECT COUNT(*) FROM pc_windows');
    if (result.goToFirstRow()) stats.totalWindows = result.getLong(0);

    result = await this.store.querySql('SELECT COUNT(*) FROM pc_notifications');
    if (result.goToFirstRow()) stats.totalNotifications = result.getLong(0);

    result = await this.store.querySql('SELECT COUNT(*) FROM pc_notifications WHERE is_read = 0');
    if (result.goToFirstRow()) stats.unreadNotifications = result.getLong(0);

    result = await this.store.querySql('SELECT COUNT(*) FROM pc_hotkeys');
    if (result.goToFirstRow()) stats.totalHotkeys = result.getLong(0);

    result = await this.store.querySql('SELECT COUNT(*) FROM pc_clipboard');
    if (result.goToFirstRow()) stats.clipboardItems = result.getLong(0);

    return stats;
  }

  // === 维护操作 ===
  async vacuum(): Promise<void> {
    if (!this.store) return;
    await this.store.executeSql('VACUUM');
    console.info('[龍魂] 数据库已压缩');
  }

  async close(): Promise<void> {
    if (this.store) {
      this.store.close();
      this.store = null;
      console.info('[龍魂] 数据库已关闭');
    }
  }
}

// 全局单例
export const pcDatabase = PCDatabase.getInstance();
