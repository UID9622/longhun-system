/**
 * 龙魂·存储适配层 — RDB 持久化
 * License: MulanPSL v2
 */
import { AuditResult, AuditRecord } from '../models/AuditModels';
import relationalStore from '@ohos.data.relationalStore';

export class StorageHelper {
  private store: any;
  private static readonly DB_NAME = 'LonghunAudit.db';
  private static readonly TABLE = 'audit_records';
  private initialized: boolean = false;

  async init(): Promise<void> {
    if (this.initialized) return;
    const config = {
      name: StorageHelper.DB_NAME,
      securityLevel: relationalStore.SecurityLevel.S2
    };
    this.store = await relationalStore.getRdbStore(config);
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${StorageHelper.TABLE} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dna TEXT NOT NULL UNIQUE,
        color TEXT NOT NULL,
        r_value REAL NOT NULL,
        description TEXT,
        target TEXT,
        scores_json TEXT,
        seal_json TEXT,
        timestamp TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
      )
    `);
    this.initialized = true;
  }

  async saveAuditRecord(result: AuditResult): Promise<void> {
    if (!this.initialized) await this.init();
    await this.store.executeSql(
      `INSERT OR REPLACE INTO ${StorageHelper.TABLE}
       (dna, color, r_value, description, target, scores_json, seal_json, timestamp)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        result.dna,
        result.color,
        result.rValue,
        result.summary,
        '', // target from input
        JSON.stringify(result.scores),
        JSON.stringify(result.sovereignSeal),
        result.timestamp
      ]
    );
  }

  async getAuditRecords(): Promise<AuditRecord[]> {
    if (!this.initialized) await this.init();
    const records: AuditRecord[] = [];
    try {
      const result = await this.store.query(
        `SELECT * FROM ${StorageHelper.TABLE} ORDER BY created_at DESC LIMIT 50`
      );
      while (result.goToNextRow()) {
        records.push({
          id: result.getLong(result.getColumnIndex('id')),
          dna: result.getString(result.getColumnIndex('dna')),
          color: result.getString(result.getColumnIndex('color')),
          rValue: result.getDouble(result.getColumnIndex('r_value')),
          description: result.getString(result.getColumnIndex('description')),
          target: result.getString(result.getColumnIndex('target')),
          timestamp: result.getString(result.getColumnIndex('timestamp')),
          sealed: true
        });
      }
    } catch (e) {
      console.error(`[龙魂存储] 查询失败: ${e}`);
    }
    return records;
  }

  async getRecordCount(): Promise<number> {
    if (!this.initialized) await this.init();
    const result = await this.store.query(
      `SELECT COUNT(*) as total FROM ${StorageHelper.TABLE}`
    );
    result.goToFirstRow();
    return result.getLong(result.getColumnIndex('total'));
  }
}
