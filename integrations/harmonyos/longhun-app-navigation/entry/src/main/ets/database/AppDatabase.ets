// entry/src/main/ets/database/AppDatabase.ets
// 龍魂 · 应用数据持久化

import { relationalStore } from '@kit.ArkData';
import { BusinessError } from '@kit.BasicServicesKit';

const DATABASE_NAME = 'LonghunApp.db';
const DATABASE_VERSION = 1;

// === 数据库表定义 ===
const SQL_CREATE_USER_TABLE = `
  CREATE TABLE IF NOT EXISTS t_user (
    id TEXT PRIMARY KEY,
    uid TEXT NOT NULL,
    name TEXT NOT NULL,
    avatar TEXT,
    role TEXT DEFAULT 'user',
    department TEXT DEFAULT '龍魂系统',
    permissions TEXT DEFAULT '["read"]',
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    dna_signature TEXT NOT NULL
  )
`;

const SQL_CREATE_PAGE_STATE_TABLE = `
  CREATE TABLE IF NOT EXISTS t_page_state (
    id TEXT PRIMARY KEY,
    page_name TEXT NOT NULL,
    route TEXT NOT NULL UNIQUE,
    params TEXT DEFAULT '{}',
    scroll_position REAL DEFAULT 0,
    form_data TEXT DEFAULT '{}',
    is_dirty INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    dna_signature TEXT NOT NULL
  )
`;

const SQL_CREATE_NAV_HISTORY_TABLE = `
  CREATE TABLE IF NOT EXISTS t_nav_history (
    id TEXT PRIMARY KEY,
    stack TEXT DEFAULT '[]',
    current_index INTEGER DEFAULT -1,
    max_depth INTEGER DEFAULT 50,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    dna_signature TEXT NOT NULL
  )
`;

const SQL_CREATE_ROUTE_GUARD_TABLE = `
  CREATE TABLE IF NOT EXISTS t_route_guard (
    id TEXT PRIMARY KEY,
    route TEXT NOT NULL UNIQUE,
    guards TEXT DEFAULT '[]',
    fallback_route TEXT DEFAULT '/login',
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    dna_signature TEXT NOT NULL
  )
`;

const SQL_CREATE_APP_SETTINGS_TABLE = `
  CREATE TABLE IF NOT EXISTS t_app_settings (
    id TEXT PRIMARY KEY,
    theme TEXT DEFAULT 'dark',
    language TEXT DEFAULT 'zh-CN',
    font_scale REAL DEFAULT 1.0,
    animations INTEGER DEFAULT 1,
    auto_save INTEGER DEFAULT 1,
    sync_interval INTEGER DEFAULT 30000,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
  )
`;

// === 索引 ===
const SQL_CREATE_INDEXES = [
  'CREATE INDEX IF NOT EXISTS idx_user_uid ON t_user(uid)',
  'CREATE INDEX IF NOT EXISTS idx_page_route ON t_page_state(route)',
  'CREATE INDEX IF NOT EXISTS idx_nav_history_id ON t_nav_history(id)',
  'CREATE INDEX IF NOT EXISTS idx_route_guard_route ON t_route_guard(route)',
  'CREATE INDEX IF NOT EXISTS idx_settings_id ON t_app_settings(id)'
];

// === 数据库管理器 ===
export class AppDatabase {
  private static instance: AppDatabase;
  private store: relationalStore.RdbStore | null = null;

  private constructor() {}

  static getInstance(): AppDatabase {
    if (!AppDatabase.instance) {
      AppDatabase.instance = new AppDatabase();
    }
    return AppDatabase.instance;
  }

  // 初始化数据库
  async init(context: Context): Promise<void> {
    const config: relationalStore.StoreConfig = {
      name: DATABASE_NAME,
      securityLevel: relationalStore.SecurityLevel.S1
    };

    try {
      this.store = await relationalStore.getRdbStore(context, config);
      await this.createTables();
      await this.createIndexes();
      await this.seedDefaults();
      console.info('[龍魂] 数据库初始化完成');
    } catch (err) {
      const error = err as BusinessError;
      console.error(`[龍魂] 数据库初始化失败: ${error.message}`);
    }
  }

  // 创建表
  private async createTables(): Promise<void> {
    if (!this.store) return;

    const sqls = [
      SQL_CREATE_USER_TABLE,
      SQL_CREATE_PAGE_STATE_TABLE,
      SQL_CREATE_NAV_HISTORY_TABLE,
      SQL_CREATE_ROUTE_GUARD_TABLE,
      SQL_CREATE_APP_SETTINGS_TABLE
    ];

    for (const sql of sqls) {
      await this.store.executeSql(sql);
    }

    console.info('[龍魂] 数据库表创建完成 (5表)');
  }

  // 创建索引
  private async createIndexes(): Promise<void> {
    if (!this.store) return;

    for (const sql of SQL_CREATE_INDEXES) {
      await this.store.executeSql(sql);
    }

    console.info('[龍魂] 数据库索引创建完成 (5索引)');
  }

  // 种子数据
  private async seedDefaults(): Promise<void> {
    if (!this.store) return;

    const now = Date.now();

    // 检查是否已有设置
    const predicates = new relationalStore.RdbPredicates('t_app_settings');
    const resultSet = await this.store.query(predicates);

    if (resultSet.rowCount === 0) {
      const settingsSql = `
        INSERT INTO t_app_settings (id, theme, language, font_scale, animations, auto_save, sync_interval, created_at, updated_at)
        VALUES ('SETTINGS-9622-default', 'dark', 'zh-CN', 1.0, 1, 1, 30000, ${now}, ${now})
      `;
      await this.store.executeSql(settingsSql);
      console.info('[龍魂] 默认设置已种子化');
    }

    resultSet.close();
  }

  // 获取数据库实例
  getStore(): relationalStore.RdbStore | null {
    return this.store;
  }

  // === 用户数据操作 ===

  // 保存用户
  async saveUser(userData: Record<string, Object>): Promise<void> {
    if (!this.store) return;

    const now = Date.now();
    const valueBucket: relationalStore.ValuesBucket = {
      'id': userData['id'] as string,
      'uid': userData['uid'] as string,
      'name': userData['name'] as string,
      'avatar': userData['avatar'] as string || '',
      'role': userData['role'] as string || 'user',
      'department': userData['department'] as string || '龍魂系统',
      'permissions': JSON.stringify(userData['permissions'] || ['read']),
      'created_at': userData['createdAt'] ? (userData['createdAt'] as Date).getTime() : now,
      'updated_at': now,
      'dna_signature': userData['dnaSignature'] as string || ''
    };

    await this.store.insert('t_user', valueBucket, relationalStore.ConflictMode.REPLACE);
  }

  // 查询用户
  async getUser(uid: string): Promise<Record<string, Object> | null> {
    if (!this.store) return null;

    const predicates = new relationalStore.RdbPredicates('t_user');
    predicates.equalTo('uid', uid);

    const resultSet = await this.store.query(predicates);
    if (resultSet.goToFirstRow()) {
      const user: Record<string, Object> = {
        id: resultSet.getString(resultSet.getColumnIndex('id')),
        uid: resultSet.getString(resultSet.getColumnIndex('uid')),
        name: resultSet.getString(resultSet.getColumnIndex('name')),
        avatar: resultSet.getString(resultSet.getColumnIndex('avatar')),
        role: resultSet.getString(resultSet.getColumnIndex('role')),
        department: resultSet.getString(resultSet.getColumnIndex('department')),
        permissions: JSON.parse(resultSet.getString(resultSet.getColumnIndex('permissions'))),
        createdAt: new Date(resultSet.getLong(resultSet.getColumnIndex('created_at'))),
        updatedAt: new Date(resultSet.getLong(resultSet.getColumnIndex('updated_at'))),
        dnaSignature: resultSet.getString(resultSet.getColumnIndex('dna_signature'))
      };
      resultSet.close();
      return user;
    }
    resultSet.close();
    return null;
  }

  // === 页面状态操作 ===

  // 保存页面状态
  async savePageState(route: string, state: Record<string, Object>): Promise<void> {
    if (!this.store) return;

    const now = Date.now();
    const valueBucket: relationalStore.ValuesBucket = {
      'id': state['id'] as string || `PAGE-${route}-${now}`,
      'page_name': state['pageName'] as string || route,
      'route': route,
      'params': JSON.stringify(state['params'] || {}),
      'scroll_position': state['scrollPosition'] as number || 0,
      'form_data': JSON.stringify(state['formData'] || {}),
      'is_dirty': (state['isDirty'] as boolean) ? 1 : 0,
      'created_at': now,
      'updated_at': now,
      'dna_signature': state['dnaSignature'] as string || ''
    };

    await this.store.insert('t_page_state', valueBucket, relationalStore.ConflictMode.REPLACE);
  }

  // 查询页面状态
  async getPageState(route: string): Promise<Record<string, Object> | null> {
    if (!this.store) return null;

    const predicates = new relationalStore.RdbPredicates('t_page_state');
    predicates.equalTo('route', route);

    const resultSet = await this.store.query(predicates);
    if (resultSet.goToFirstRow()) {
      const state: Record<string, Object> = {
        id: resultSet.getString(resultSet.getColumnIndex('id')),
        pageName: resultSet.getString(resultSet.getColumnIndex('page_name')),
        route: resultSet.getString(resultSet.getColumnIndex('route')),
        params: JSON.parse(resultSet.getString(resultSet.getColumnIndex('params'))),
        scrollPosition: resultSet.getDouble(resultSet.getColumnIndex('scroll_position')),
        formData: JSON.parse(resultSet.getString(resultSet.getColumnIndex('form_data'))),
        isDirty: resultSet.getLong(resultSet.getColumnIndex('is_dirty')) === 1,
        createdAt: new Date(resultSet.getLong(resultSet.getColumnIndex('created_at'))),
        updatedAt: new Date(resultSet.getLong(resultSet.getColumnIndex('updated_at'))),
        dnaSignature: resultSet.getString(resultSet.getColumnIndex('dna_signature'))
      };
      resultSet.close();
      return state;
    }
    resultSet.close();
    return null;
  }

  // === 设置操作 ===

  // 保存设置
  async saveSettings(settings: Record<string, Object>): Promise<void> {
    if (!this.store) return;

    const now = Date.now();
    const valueBucket: relationalStore.ValuesBucket = {
      'id': 'SETTINGS-9622-default',
      'theme': settings['theme'] as string || 'dark',
      'language': settings['language'] as string || 'zh-CN',
      'font_scale': settings['fontScale'] as number || 1.0,
      'animations': (settings['animations'] as boolean) ? 1 : 0,
      'auto_save': (settings['autoSave'] as boolean) ? 1 : 0,
      'sync_interval': settings['syncInterval'] as number || 30000,
      'updated_at': now
    };

    await this.store.insert('t_app_settings', valueBucket, relationalStore.ConflictMode.REPLACE);
  }

  // 查询设置
  async getSettings(): Promise<Record<string, Object> | null> {
    if (!this.store) return null;

    const predicates = new relationalStore.RdbPredicates('t_app_settings');
    predicates.equalTo('id', 'SETTINGS-9622-default');

    const resultSet = await this.store.query(predicates);
    if (resultSet.goToFirstRow()) {
      const settings: Record<string, Object> = {
        id: resultSet.getString(resultSet.getColumnIndex('id')),
        theme: resultSet.getString(resultSet.getColumnIndex('theme')),
        language: resultSet.getString(resultSet.getColumnIndex('language')),
        fontScale: resultSet.getDouble(resultSet.getColumnIndex('font_scale')),
        animations: resultSet.getLong(resultSet.getColumnIndex('animations')) === 1,
        autoSave: resultSet.getLong(resultSet.getColumnIndex('auto_save')) === 1,
        syncInterval: resultSet.getLong(resultSet.getColumnIndex('sync_interval')),
        createdAt: new Date(resultSet.getLong(resultSet.getColumnIndex('created_at'))),
        updatedAt: new Date(resultSet.getLong(resultSet.getColumnIndex('updated_at')))
      };
      resultSet.close();
      return settings;
    }
    resultSet.close();
    return null;
  }

  // === 维护操作 ===

  // 清理30天前的历史记录
  async cleanOldHistory(daysOld: number = 30): Promise<void> {
    if (!this.store) return;

    const cutoff = Date.now() - daysOld * 24 * 60 * 60 * 1000;
    const sql = `DELETE FROM t_nav_history WHERE updated_at < ${cutoff}`;
    await this.store.executeSql(sql);
    console.info(`[龍魂] 清理 ${daysOld} 天前的导航历史`);
  }

  // 关闭数据库
  async close(): Promise<void> {
    if (this.store) {
      await this.store.close();
      this.store = null;
      console.info('[龍魂] 数据库已关闭');
    }
  }
}

// 全局数据库实例
export const appDatabase = AppDatabase.getInstance();
