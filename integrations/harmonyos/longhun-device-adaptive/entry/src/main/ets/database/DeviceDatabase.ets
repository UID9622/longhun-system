// entry/src/main/ets/database/DeviceDatabase.ets
// 龍魂 · 设备配置数据库 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { relationalStore } from '@kit.ArkData';
import { BusinessError } from '@kit.BasicServicesKit';

const STORE_CONFIG: relationalStore.StoreConfig = {
  name: 'LonghunDevice.db',
  securityLevel: relationalStore.SecurityLevel.S3
};

const SQL_CREATE_DEVICES = `
  CREATE TABLE IF NOT EXISTS devices (
    id TEXT PRIMARY KEY,
    device_type TEXT NOT NULL DEFAULT 'phone',
    breakpoint TEXT DEFAULT 'sm',
    screen_width REAL DEFAULT 360,
    screen_height REAL DEFAULT 780,
    screen_density REAL DEFAULT 3,
    orientation TEXT DEFAULT 'portrait',
    interaction_mode TEXT DEFAULT 'touch',
    color_mode TEXT DEFAULT 'auto',
    is_round INTEGER DEFAULT 0,
    has_notch INTEGER DEFAULT 0,
    safe_area_top REAL DEFAULT 0,
    safe_area_bottom REAL DEFAULT 0,
    safe_area_left REAL DEFAULT 0,
    safe_area_right REAL DEFAULT 0,
    dna_signature TEXT,
    last_seen INTEGER,
    created_at INTEGER
  )
`;

const SQL_CREATE_LAYOUTS = `
  CREATE TABLE IF NOT EXISTS layout_strategies (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    device_type TEXT NOT NULL,
    breakpoint TEXT NOT NULL,
    content_padding REAL DEFAULT 16,
    card_columns INTEGER DEFAULT 1,
    list_item_height REAL DEFAULT 56,
    header_height REAL DEFAULT 56,
    footer_height REAL DEFAULT 56,
    sidebar_width REAL DEFAULT 0,
    tab_bar_height REAL DEFAULT 56,
    button_height REAL DEFAULT 44,
    button_min_width REAL DEFAULT 80,
    input_height REAL DEFAULT 44,
    avatar_size REAL DEFAULT 40,
    icon_size REAL DEFAULT 24,
    animation_duration INTEGER DEFAULT 300,
    page_transition TEXT DEFAULT 'slide',
    dna_signature TEXT,
    created_at INTEGER
  )
`;

const SQL_CREATE_WINDOW_HISTORY = `
  CREATE TABLE IF NOT EXISTS window_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    width REAL NOT NULL,
    height REAL NOT NULL,
    device_type TEXT,
    breakpoint TEXT,
    orientation TEXT,
    timestamp INTEGER NOT NULL
  )
`;

const SQL_CREATE_PREFERENCES = `
  CREATE TABLE IF NOT EXISTS device_preferences (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at INTEGER
  )
`;

// 索引
const SQL_INDEXES = [
  'CREATE INDEX IF NOT EXISTS idx_devices_type ON devices(device_type)',
  'CREATE INDEX IF NOT EXISTS idx_devices_last_seen ON devices(last_seen DESC)',
  'CREATE INDEX IF NOT EXISTS idx_window_history_ts ON window_history(timestamp DESC)',
  'CREATE INDEX IF NOT EXISTS idx_layout_device ON layout_strategies(device_type, breakpoint)'
];

// 默认布局数据
const DEFAULT_LAYOUTS = [
  {
    id: 'layout-watch-xs',
    name: '手表精简',
    device_type: 'watch', breakpoint: 'xs',
    content_padding: 4, card_columns: 1, list_item_height: 36,
    header_height: 0, footer_height: 0, sidebar_width: 0, tab_bar_height: 0,
    button_height: 36, button_min_width: 60, input_height: 36,
    avatar_size: 28, icon_size: 20, animation_duration: 200, page_transition: 'fade'
  },
  {
    id: 'layout-phone-sm',
    name: '手机标准',
    device_type: 'phone', breakpoint: 'sm',
    content_padding: 16, card_columns: 1, list_item_height: 56,
    header_height: 56, footer_height: 56, sidebar_width: 0, tab_bar_height: 56,
    button_height: 44, button_min_width: 80, input_height: 44,
    avatar_size: 40, icon_size: 24, animation_duration: 300, page_transition: 'slide'
  },
  {
    id: 'layout-tablet-lg',
    name: '平板宽屏',
    device_type: 'tablet', breakpoint: 'lg',
    content_padding: 24, card_columns: 3, list_item_height: 64,
    header_height: 64, footer_height: 64, sidebar_width: 240, tab_bar_height: 0,
    button_height: 48, button_min_width: 96, input_height: 48,
    avatar_size: 48, icon_size: 28, animation_duration: 300, page_transition: 'slide'
  },
  {
    id: 'layout-car-xl',
    name: '车机放大',
    device_type: 'car', breakpoint: 'xl',
    content_padding: 32, card_columns: 4, list_item_height: 80,
    header_height: 80, footer_height: 0, sidebar_width: 320, tab_bar_height: 0,
    button_height: 64, button_min_width: 120, input_height: 56,
    avatar_size: 56, icon_size: 32, animation_duration: 400, page_transition: 'scale'
  },
  {
    id: 'layout-tv-xl',
    name: '电视巨幕',
    device_type: 'tv', breakpoint: 'xl',
    content_padding: 48, card_columns: 6, list_item_height: 96,
    header_height: 96, footer_height: 0, sidebar_width: 400, tab_bar_height: 0,
    button_height: 72, button_min_width: 160, input_height: 64,
    avatar_size: 64, icon_size: 40, animation_duration: 500, page_transition: 'fade'
  }
];

export class DeviceDatabase {
  static store: relationalStore.RdbStore | null = null;

  static async init(): Promise<void> {
    try {
      const context = getContext();
      this.store = await relationalStore.getRdbStore(context, STORE_CONFIG);

      await this.store.executeSql(SQL_CREATE_DEVICES);
      await this.store.executeSql(SQL_CREATE_LAYOUTS);
      await this.store.executeSql(SQL_CREATE_WINDOW_HISTORY);
      await this.store.executeSql(SQL_CREATE_PREFERENCES);

      for (const idxSql of SQL_INDEXES) {
        await this.store.executeSql(idxSql);
      }

      await this.seedDefaultLayouts();
      console.info('[龍魂] 设备数据库初始化完成');
    } catch (err) {
      const error = err as BusinessError;
      console.error(`[龍魂] 设备数据库初始化失败: ${error.message}`);
    }
  }

  static async seedDefaultLayouts(): Promise<void> {
    if (!this.store) return;
    for (const layout of DEFAULT_LAYOUTS) {
      const predicates = new relationalStore.RdbPredicates('layout_strategies');
      predicates.equalTo('id', layout.id);
      const resultSet = await this.store.query(predicates);
      if (resultSet.rowCount === 0) {
        const vb: relationalStore.ValuesBucket = {
          id: layout.id, name: layout.name,
          device_type: layout.device_type, breakpoint: layout.breakpoint,
          content_padding: layout.content_padding, card_columns: layout.card_columns,
          list_item_height: layout.list_item_height, header_height: layout.header_height,
          footer_height: layout.footer_height, sidebar_width: layout.sidebar_width,
          tab_bar_height: layout.tab_bar_height, button_height: layout.button_height,
          button_min_width: layout.button_min_width, input_height: layout.input_height,
          avatar_size: layout.avatar_size, icon_size: layout.icon_size,
          animation_duration: layout.animation_duration, page_transition: layout.page_transition,
          dna_signature: `SM3-${layout.id}-${Date.now()}`, created_at: Date.now()
        };
        await this.store.insert('layout_strategies', vb);
      }
      resultSet.close();
    }
  }

  static async recordWindowChange(width: number, height: number, deviceType: string, breakpoint: string, orientation: string): Promise<void> {
    if (!this.store) return;
    const vb: relationalStore.ValuesBucket = {
      width, height, device_type: deviceType, breakpoint, orientation,
      timestamp: Date.now()
    };
    await this.store.insert('window_history', vb);

    // 清理超过7天的历史
    const threshold = Date.now() - 7 * 24 * 60 * 60 * 1000;
    const predicates = new relationalStore.RdbPredicates('window_history');
    predicates.lessThan('timestamp', threshold);
    await this.store.delete(predicates);
  }

  static async getWindowHistory(limit: number = 50): Promise<any[]> {
    if (!this.store) return [];
    const predicates = new relationalStore.RdbPredicates('window_history');
    predicates.orderByDesc('timestamp');
    predicates.limit(limit);
    const resultSet = await this.store.query(predicates);
    const results: any[] = [];
    while (resultSet.goToNextRow()) {
      results.push({
        width: resultSet.getDouble(resultSet.getColumnIndex('width')),
        height: resultSet.getDouble(resultSet.getColumnIndex('height')),
        deviceType: resultSet.getString(resultSet.getColumnIndex('device_type')),
        breakpoint: resultSet.getString(resultSet.getColumnIndex('breakpoint')),
        orientation: resultSet.getString(resultSet.getColumnIndex('orientation')),
        timestamp: resultSet.getLong(resultSet.getColumnIndex('timestamp'))
      });
    }
    resultSet.close();
    return results;
  }

  static async getLayoutStrategy(deviceType: string, breakpoint: string): Promise<any> {
    if (!this.store) return null;
    const predicates = new relationalStore.RdbPredicates('layout_strategies');
    predicates.equalTo('device_type', deviceType);
    predicates.equalTo('breakpoint', breakpoint);
    const resultSet = await this.store.query(predicates);
    if (resultSet.goToFirstRow()) {
      const layout: any = {};
      for (const col of [
        'id', 'name', 'device_type', 'breakpoint', 'content_padding', 'card_columns',
        'list_item_height', 'header_height', 'footer_height', 'sidebar_width',
        'tab_bar_height', 'button_height', 'button_min_width', 'input_height',
        'avatar_size', 'icon_size', 'animation_duration', 'page_transition'
      ]) {
        layout[col] = resultSet.getValue(resultSet.getColumnIndex(col));
      }
      resultSet.close();
      return layout;
    }
    resultSet.close();
    return null;
  }

  static async savePreference(key: string, value: string): Promise<void> {
    if (!this.store) return;
    const vb: relationalStore.ValuesBucket = { key, value, updated_at: Date.now() };

    const predicates = new relationalStore.RdbPredicates('device_preferences');
    predicates.equalTo('key', key);
    const resultSet = await this.store.query(predicates);
    if (resultSet.rowCount > 0) {
      await this.store.update(vb, predicates);
    } else {
      await this.store.insert('device_preferences', vb);
    }
    resultSet.close();
  }

  static async getPreference(key: string): Promise<string | null> {
    if (!this.store) return null;
    const predicates = new relationalStore.RdbPredicates('device_preferences');
    predicates.equalTo('key', key);
    const resultSet = await this.store.query(predicates);
    if (resultSet.goToFirstRow()) {
      const value = resultSet.getString(resultSet.getColumnIndex('value'));
      resultSet.close();
      return value;
    }
    resultSet.close();
    return null;
  }

  static destroy(): void {
    if (this.store) {
      this.store.close();
      this.store = null;
    }
  }
}
