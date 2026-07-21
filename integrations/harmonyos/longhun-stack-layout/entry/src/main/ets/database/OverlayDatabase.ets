// entry/src/main/ets/database/OverlayDatabase.ets
// 龍魂 · 遮罩配置持久化数据库

import { relationalStore } from '@kit.ArkData';
import { overlayState, LayerConfig, DialogConfig, ToastConfig, LoadingConfig, LayerType, MaskType, AnimationType } from '../models/StackModel';

const DB_NAME = 'LonghunOverlay.db';
const DB_VERSION = 1;
const TABLE_NAME = 'overlay_configs';
const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";
const CONFIRM_SEAL = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z";

// === 数据库配置 ===
const STORE_CONFIG: relationalStore.StoreConfig = {
  name: DB_NAME,
  securityLevel: relationalStore.SecurityLevel.S3 // 国密加密
};

// === 建表 SQL ===
const SQL_CREATE_TABLE = `
CREATE TABLE IF NOT EXISTS ${TABLE_NAME} (
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  z_index INTEGER NOT NULL DEFAULT 0,
  mask_type TEXT NOT NULL DEFAULT 'none',
  mask_color TEXT NOT NULL DEFAULT '#000000',
  mask_opacity REAL NOT NULL DEFAULT 0,
  enter_animation TEXT NOT NULL DEFAULT 'fade',
  exit_animation TEXT NOT NULL DEFAULT 'fade',
  animation_duration INTEGER NOT NULL DEFAULT 300,
  dismiss_on_mask_tap INTEGER NOT NULL DEFAULT 1,
  dismiss_on_back_press INTEGER NOT NULL DEFAULT 1,
  intercept_gesture INTEGER NOT NULL DEFAULT 1,
  focus_strategy TEXT NOT NULL DEFAULT 'auto',
  auto_dismiss_delay INTEGER,
  dna_signature TEXT NOT NULL,
  -- 弹窗扩展字段
  dialog_title TEXT,
  dialog_message TEXT,
  dialog_icon TEXT,
  has_input INTEGER DEFAULT 0,
  input_placeholder TEXT,
  input_default_value TEXT,
  dialog_width REAL DEFAULT 80,
  border_radius REAL DEFAULT 12,
  -- Toast 扩展字段
  toast_position TEXT DEFAULT 'center',
  -- Loading 扩展字段
  progress REAL,
  cancelable INTEGER DEFAULT 0,
  -- 元数据
  created_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
  updated_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
)
`;

// === 索引 SQL ===
const SQL_CREATE_INDEX_TYPE = `CREATE INDEX IF NOT EXISTS idx_overlay_type ON ${TABLE_NAME}(type)`;
const SQL_CREATE_INDEX_ZINDEX = `CREATE INDEX IF NOT EXISTS idx_overlay_zindex ON ${TABLE_NAME}(z_index)`;

// === 数据库单例 ===
export class OverlayDatabase {
  private static instance: OverlayDatabase;
  private store: relationalStore.RdbStore | null = null;

  static getInstance(): OverlayDatabase {
    if (!OverlayDatabase.instance) {
      OverlayDatabase.instance = new OverlayDatabase();
    }
    return OverlayDatabase.instance;
  }

  // 初始化数据库
  async init(context: Context): Promise<void> {
    if (this.store) return;

    try {
      this.store = await relationalStore.getRdbStore(context, STORE_CONFIG);
      await this.store.executeSql(SQL_CREATE_TABLE);
      await this.store.executeSql(SQL_CREATE_INDEX_TYPE);
      await this.store.executeSql(SQL_CREATE_INDEX_ZINDEX);
      console.info('[龍魂·数据库] 遮罩配置数据库初始化完成');
    } catch (err) {
      console.error(`[龍魂·数据库] 初始化失败: ${JSON.stringify(err)}`);
    }
  }

  // 保存层级配置
  async saveLayerConfig(config: LayerConfig): Promise<void> {
    if (!this.store) return;

    const bindArgs: any[] = [
      config.id, config.type, config.zIndex,
      config.maskType, config.maskColor, config.maskOpacity,
      config.enterAnimation, config.exitAnimation, config.animationDuration,
      config.dismissOnMaskTap ? 1 : 0, config.dismissOnBackPress ? 1 : 0,
      config.interceptGesture ? 1 : 0, config.focusStrategy,
      config.autoDismissDelay || null, config.dnaSignature
    ];

    const sql = `
      INSERT OR REPLACE INTO ${TABLE_NAME} (
        id, type, z_index, mask_type, mask_color, mask_opacity,
        enter_animation, exit_animation, animation_duration,
        dismiss_on_mask_tap, dismiss_on_back_press, intercept_gesture,
        focus_strategy, auto_dismiss_delay, dna_signature, updated_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, strftime('%s','now'))
    `;

    await this.store.executeSql(sql, bindArgs);
  }

  // 保存弹窗配置
  async saveDialogConfig(config: DialogConfig): Promise<void> {
    await this.saveLayerConfig(config);

    if (!this.store) return;

    const sql = `
      UPDATE ${TABLE_NAME} SET
        dialog_title = ?, dialog_message = ?, dialog_icon = ?,
        has_input = ?, input_placeholder = ?, input_default_value = ?,
        dialog_width = ?, border_radius = ?,
        updated_at = strftime('%s','now')
      WHERE id = ?
    `;

    await this.store.executeSql(sql, [
      config.title, config.message, config.icon || null,
      config.hasInput ? 1 : 0, config.inputPlaceholder || null,
      config.inputDefaultValue || null,
      config.width, config.borderRadius, config.id
    ]);
  }

  // 保存 Toast 配置
  async saveToastConfig(config: ToastConfig): Promise<void> {
    await this.saveLayerConfig(config);

    if (!this.store) return;

    const sql = `
      UPDATE ${TABLE_NAME} SET
        toast_position = ?,
        updated_at = strftime('%s','now')
      WHERE id = ?
    `;

    await this.store.executeSql(sql, [config.position, config.id]);
  }

  // 保存 Loading 配置
  async saveLoadingConfig(config: LoadingConfig): Promise<void> {
    await this.saveLayerConfig(config);

    if (!this.store) return;

    const sql = `
      UPDATE ${TABLE_NAME} SET
        progress = ?, cancelable = ?,
        updated_at = strftime('%s','now')
      WHERE id = ?
    `;

    await this.store.executeSql(sql, [
      config.progress || null, config.cancelable ? 1 : 0, config.id
    ]);
  }

  // 查询所有配置
  async getAllConfigs(): Promise<LayerConfig[]> {
    if (!this.store) return [];

    const predicates = new relationalStore.RdbPredicates(TABLE_NAME);
    predicates.orderByAsc('z_index');

    const resultSet = await this.store.query(predicates);
    const configs: LayerConfig[] = [];

    while (resultSet.goToNextRow()) {
      const config = this.rowToLayerConfig(resultSet);
      if (config) configs.push(config);
    }

    resultSet.close();
    return configs;
  }

  // 按类型查询
  async getConfigsByType(type: LayerType): Promise<LayerConfig[]> {
    if (!this.store) return [];

    const predicates = new relationalStore.RdbPredicates(TABLE_NAME);
    predicates.equalTo('type', type);
    predicates.orderByAsc('z_index');

    const resultSet = await this.store.query(predicates);
    const configs: LayerConfig[] = [];

    while (resultSet.goToNextRow()) {
      const config = this.rowToLayerConfig(resultSet);
      if (config) configs.push(config);
    }

    resultSet.close();
    return configs;
  }

  // 删除配置
  async deleteConfig(id: string): Promise<void> {
    if (!this.store) return;

    const predicates = new relationalStore.RdbPredicates(TABLE_NAME);
    predicates.equalTo('id', id);
    await this.store.delete(predicates);
  }

  // 按类型删除
  async deleteConfigsByType(type: LayerType): Promise<void> {
    if (!this.store) return;

    const predicates = new relationalStore.RdbPredicates(TABLE_NAME);
    predicates.equalTo('type', type);
    await this.store.delete(predicates);
  }

  // 清空所有
  async clearAll(): Promise<void> {
    if (!this.store) return;

    const predicates = new relationalStore.RdbPredicates(TABLE_NAME);
    await this.store.delete(predicates);
    console.info('[龍魂·数据库] 遮罩配置已清空');
  }

  // 清理过期配置（7天前）
  async cleanExpired(): Promise<number> {
    if (!this.store) return 0;

    const sevenDaysAgo = Math.floor(Date.now() / 1000) - 7 * 24 * 60 * 60;

    const predicates = new relationalStore.RdbPredicates(TABLE_NAME);
    predicates.lessThan('updated_at', sevenDaysAgo.toString());

    const rows = await this.store.delete(predicates);
    console.info(`[龍魂·数据库] 清理过期遮罩配置: ${rows} 条`);
    return rows;
  }

  // 获取统计
  async getStatistics(): Promise<OverlayDbStats> {
    if (!this.store) {
      return { total: 0, byType: {} };
    }

    const predicates = new relationalStore.RdbPredicates(TABLE_NAME);
    const resultSet = await this.store.query(predicates);
    const stats: OverlayDbStats = { total: 0, byType: {} };

    while (resultSet.goToNextRow()) {
      stats.total++;
      const type = resultSet.getString(resultSet.getColumnIndex('type'));
      stats.byType[type] = (stats.byType[type] || 0) + 1;
    }

    resultSet.close();
    return stats;
  }

  // 行数据转 LayerConfig
  private rowToLayerConfig(resultSet: relationalStore.ResultSet): LayerConfig | null {
    try {
      const type = resultSet.getString(resultSet.getColumnIndex('type')) as LayerType;

      const baseConfig: Partial<LayerConfig> = {
        id: resultSet.getString(resultSet.getColumnIndex('id')),
        type: type,
        zIndex: resultSet.getLong(resultSet.getColumnIndex('z_index')),
        maskType: resultSet.getString(resultSet.getColumnIndex('mask_type')) as MaskType,
        maskColor: resultSet.getString(resultSet.getColumnIndex('mask_color')),
        maskOpacity: resultSet.getDouble(resultSet.getColumnIndex('mask_opacity')),
        enterAnimation: resultSet.getString(resultSet.getColumnIndex('enter_animation')) as AnimationType,
        exitAnimation: resultSet.getString(resultSet.getColumnIndex('exit_animation')) as AnimationType,
        animationDuration: resultSet.getLong(resultSet.getColumnIndex('animation_duration')),
        dismissOnMaskTap: resultSet.getLong(resultSet.getColumnIndex('dismiss_on_mask_tap')) === 1,
        dismissOnBackPress: resultSet.getLong(resultSet.getColumnIndex('dismiss_on_back_press')) === 1,
        interceptGesture: resultSet.getLong(resultSet.getColumnIndex('intercept_gesture')) === 1,
      };

      // 根据类型构建具体配置
      switch (type) {
        case LayerType.DIALOG:
          return new DialogConfig({
            ...baseConfig,
            title: resultSet.getString(resultSet.getColumnIndex('dialog_title')),
            message: resultSet.getString(resultSet.getColumnIndex('dialog_message')),
            icon: resultSet.getString(resultSet.getColumnIndex('dialog_icon')),
            hasInput: resultSet.getLong(resultSet.getColumnIndex('has_input')) === 1,
            inputPlaceholder: resultSet.getString(resultSet.getColumnIndex('input_placeholder')),
            inputDefaultValue: resultSet.getString(resultSet.getColumnIndex('input_default_value')),
            width: resultSet.getDouble(resultSet.getColumnIndex('dialog_width')),
            borderRadius: resultSet.getDouble(resultSet.getColumnIndex('border_radius')),
          });

        case LayerType.TOAST:
          return new ToastConfig({
            ...baseConfig,
            position: (resultSet.getString(resultSet.getColumnIndex('toast_position')) || 'center') as 'top' | 'center' | 'bottom',
          });

        case LayerType.LOADING:
          return new LoadingConfig({
            ...baseConfig,
            progress: resultSet.getDouble(resultSet.getColumnIndex('progress')),
            cancelable: resultSet.getLong(resultSet.getColumnIndex('cancelable')) === 1,
          });

        default:
          return new LayerConfig(baseConfig);
      }
    } catch (err) {
      console.error(`[龍魂·数据库] 行数据转换失败: ${JSON.stringify(err)}`);
      return null;
    }
  }

  // 关闭数据库
  async close(): Promise<void> {
    if (this.store) {
      await this.store.close();
      this.store = null;
      console.info('[龍魂·数据库] 遮罩配置数据库已关闭');
    }
  }
}

export interface OverlayDbStats {
  total: number;
  byType: Record<string, number>;
}

export const overlayDatabase = OverlayDatabase.getInstance();
