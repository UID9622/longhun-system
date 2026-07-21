// entry/src/main/ets/database/InventoryDatabase.ets
// 龍魂 · 库存数据库 · 关系型存储

import { relationalStore } from '@kit.ArkData';

const STORE_NAME = 'LongHunInventory.db';
const TABLE_ITEMS = 'supply_items';
const TABLE_RECORDS = 'inventory_records';
const TABLE_REQUESTS = 'purchase_requests';
const TABLE_REQUEST_ITEMS = 'purchase_request_items';

export class InventoryDatabase {
  private static store: relationalStore.RdbStore | null = null;

  static async init(context: Context): Promise<void> {
    const config: relationalStore.StoreConfig = {
      name: STORE_NAME,
      securityLevel: relationalStore.SecurityLevel.S1,
      encrypt: true
    };

    this.store = await relationalStore.getRdbStore(context, config);

    // 创建物资表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_ITEMS} (
        id TEXT PRIMARY KEY,
        sku TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        category TEXT,
        specification TEXT,
        brand TEXT,
        unit TEXT DEFAULT '个',
        location TEXT DEFAULT '未指定',
        status TEXT DEFAULT '在库',
        quantity INTEGER DEFAULT 0,
        min_quantity INTEGER DEFAULT 10,
        max_quantity INTEGER DEFAULT 100,
        reorder_point INTEGER DEFAULT 20,
        batch_no TEXT,
        supplier TEXT,
        purchase_date INTEGER,
        expiry_date INTEGER,
        purchase_price REAL DEFAULT 0,
        total_value REAL DEFAULT 0,
        custodian TEXT,
        department TEXT,
        last_used_by TEXT,
        last_used_date INTEGER,
        barcode TEXT,
        qr_code TEXT,
        photo_path TEXT,
        rfid_tag TEXT,
        created_at INTEGER,
        updated_at INTEGER,
        dna_signature TEXT
      )
    `);

    // 创建索引
    await this.store.executeSql(`
      CREATE INDEX IF NOT EXISTS idx_items_sku ON ${TABLE_ITEMS}(sku)
    `);
    await this.store.executeSql(`
      CREATE INDEX IF NOT EXISTS idx_items_category ON ${TABLE_ITEMS}(category)
    `);
    await this.store.executeSql(`
      CREATE INDEX IF NOT EXISTS idx_items_status ON ${TABLE_ITEMS}(status)
    `);

    // 创建流水表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_RECORDS} (
        id TEXT PRIMARY KEY,
        item_id TEXT NOT NULL,
        type TEXT NOT NULL,
        quantity INTEGER DEFAULT 0,
        old_quantity INTEGER DEFAULT 0,
        new_quantity INTEGER DEFAULT 0,
        operator TEXT,
        approver TEXT,
        reason TEXT,
        document_no TEXT,
        photo_path TEXT,
        timestamp INTEGER,
        dna_signature TEXT,
        FOREIGN KEY (item_id) REFERENCES ${TABLE_ITEMS}(id)
      )
    `);

    await this.store.executeSql(`
      CREATE INDEX IF NOT EXISTS idx_records_item ON ${TABLE_RECORDS}(item_id)
    `);
    await this.store.executeSql(`
      CREATE INDEX IF NOT EXISTS idx_records_time ON ${TABLE_RECORDS}(timestamp DESC)
    `);

    // 创建采购申请表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_REQUESTS} (
        id TEXT PRIMARY KEY,
        request_no TEXT UNIQUE NOT NULL,
        requester TEXT,
        department TEXT,
        request_date INTEGER,
        required_date INTEGER,
        total_amount REAL DEFAULT 0,
        status TEXT DEFAULT '草稿',
        level1_approver TEXT,
        level1_approved INTEGER,
        level1_comment TEXT,
        level2_approver TEXT,
        level2_approved INTEGER,
        level2_comment TEXT,
        level3_approver TEXT,
        level3_approved INTEGER,
        level3_comment TEXT,
        purchase_order_no TEXT,
        supplier TEXT,
        actual_amount REAL,
        received_date INTEGER,
        created_at INTEGER,
        dna_signature TEXT
      )
    `);

    // 创建采购物项表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_REQUEST_ITEMS} (
        id TEXT PRIMARY KEY,
        request_id TEXT NOT NULL,
        item_name TEXT NOT NULL,
        specification TEXT,
        quantity INTEGER DEFAULT 1,
        unit TEXT DEFAULT '个',
        estimated_price REAL DEFAULT 0,
        total_price REAL DEFAULT 0,
        supplier TEXT,
        remark TEXT,
        FOREIGN KEY (request_id) REFERENCES ${TABLE_REQUESTS}(id)
      )
    `);

    console.log('🐉 龍魂库存数据库初始化完成');
  }

  static getStore(): relationalStore.RdbStore | null {
    return this.store;
  }

  // === 物资 CRUD ===
  static async insertItem(item: Record<string, Object>): Promise<void> {
    if (!this.store) {
      return;
    }
    const keys = Object.keys(item);
    const values = Object.values(item);
    const placeholders = values.map(() => '?').join(',');
    await this.store.executeSql(
      `INSERT OR REPLACE INTO ${TABLE_ITEMS} (${keys.join(',')}) VALUES (${placeholders})`,
      values
    );
  }

  static async queryAllItems(): Promise<Record<string, Object>[]> {
    if (!this.store) {
      return [];
    }
    const result = await this.store.querySql(
      `SELECT * FROM ${TABLE_ITEMS} ORDER BY updated_at DESC`
    );
    return result.rowCount > 0 ? result.getRows() : [];
  }

  static async queryItemBySKU(sku: string): Promise<Record<string, Object> | null> {
    if (!this.store) {
      return null;
    }
    const result = await this.store.querySql(
      `SELECT * FROM ${TABLE_ITEMS} WHERE sku = ?`,
      [sku]
    );
    return result.rowCount > 0 ? result.getRows()[0] : null;
  }

  static async deleteItem(id: string): Promise<void> {
    if (!this.store) {
      return;
    }
    await this.store.executeSql(`DELETE FROM ${TABLE_ITEMS} WHERE id = ?`, [id]);
    await this.store.executeSql(`DELETE FROM ${TABLE_RECORDS} WHERE item_id = ?`, [id]);
  }

  // === 流水记录 ===
  static async insertRecord(record: Record<string, Object>): Promise<void> {
    if (!this.store) {
      return;
    }
    const keys = Object.keys(record);
    const values = Object.values(record);
    const placeholders = values.map(() => '?').join(',');
    await this.store.executeSql(
      `INSERT INTO ${TABLE_RECORDS} (${keys.join(',')}) VALUES (${placeholders})`,
      values
    );
  }

  static async queryRecordsByItem(itemId: string): Promise<Record<string, Object>[]> {
    if (!this.store) {
      return [];
    }
    const result = await this.store.querySql(
      `SELECT * FROM ${TABLE_RECORDS} WHERE item_id = ? ORDER BY timestamp DESC`,
      [itemId]
    );
    return result.rowCount > 0 ? result.getRows() : [];
  }

  // === 采购申请 ===
  static async insertRequest(request: Record<string, Object>, items: Record<string, Object>[]): Promise<void> {
    if (!this.store) {
      return;
    }
    const rKeys = Object.keys(request);
    const rValues = Object.values(request);
    const rPlaceholders = rValues.map(() => '?').join(',');
    await this.store.executeSql(
      `INSERT OR REPLACE INTO ${TABLE_REQUESTS} (${rKeys.join(',')}) VALUES (${rPlaceholders})`,
      rValues
    );

    for (const item of items) {
      const iKeys = Object.keys(item);
      const iValues = Object.values(item);
      const iPlaceholders = iValues.map(() => '?').join(',');
      await this.store.executeSql(
        `INSERT OR REPLACE INTO ${TABLE_REQUEST_ITEMS} (${iKeys.join(',')}) VALUES (${iPlaceholders})`,
        iValues
      );
    }
  }

  static async updateRequestStatus(id: string, status: string, updates: Record<string, Object>): Promise<void> {
    if (!this.store) {
      return;
    }
    const setClauses = Object.keys(updates).map(k => `${k} = ?`).join(', ');
    const values = [...Object.values(updates), id];
    await this.store.executeSql(
      `UPDATE ${TABLE_REQUESTS} SET status = ?, ${setClauses} WHERE id = ?`,
      [status, ...values]
    );
  }

  // === 统计查询 ===
  static async getStats(): Promise<Record<string, number>> {
    if (!this.store) {
      return { total: 0, inStock: 0, lowStock: 0, outOfStock: 0, totalValue: 0 };
    }

    const total = await this.store.querySql(`SELECT COUNT(*) as cnt FROM ${TABLE_ITEMS}`);
    const inStock = await this.store.querySql(
      `SELECT COUNT(*) as cnt FROM ${TABLE_ITEMS} WHERE status = '在库'`
    );
    const lowStock = await this.store.querySql(
      `SELECT COUNT(*) as cnt FROM ${TABLE_ITEMS} WHERE status = '低库存'`
    );
    const outOfStock = await this.store.querySql(
      `SELECT COUNT(*) as cnt FROM ${TABLE_ITEMS} WHERE status = '缺货'`
    );
    const totalValue = await this.store.querySql(
      `SELECT SUM(total_value) as val FROM ${TABLE_ITEMS}`
    );

    return {
      total: total.rowCount > 0 ? (total.getRows()[0]['cnt'] as number) : 0,
      inStock: inStock.rowCount > 0 ? (inStock.getRows()[0]['cnt'] as number) : 0,
      lowStock: lowStock.rowCount > 0 ? (lowStock.getRows()[0]['cnt'] as number) : 0,
      outOfStock: outOfStock.rowCount > 0 ? (outOfStock.getRows()[0]['cnt'] as number) : 0,
      totalValue: totalValue.rowCount > 0 ? ((totalValue.getRows()[0]['val'] as number) || 0) : 0
    };
  }
}
