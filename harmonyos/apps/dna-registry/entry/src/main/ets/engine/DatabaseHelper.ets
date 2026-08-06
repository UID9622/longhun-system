/**
 * 龙魂·DNA数据库适配层 — RDB 持久化
 * License: MulanPSL v2
 */
import { DnaRecord } from '../models/DnaModels';
import relationalStore from '@ohos.data.relationalStore';

export class DatabaseHelper {
  private store: any;
  private static readonly DB = 'LonghunDnaRegistry.db';
  private static readonly TBL = 'dna_records';

  async initialize(): Promise<void> {
    const cfg = { name: DatabaseHelper.DB, securityLevel: relationalStore.SecurityLevel.S2 };
    this.store = await relationalStore.getRdbStore(cfg);
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${DatabaseHelper.TBL} (
        dna TEXT PRIMARY KEY, module TEXT NOT NULL, action TEXT NOT NULL,
        creator TEXT DEFAULT 'UID9622', ganzhi TEXT, gua TEXT, hash TEXT,
        timestamp TEXT, metadata TEXT, sovereignty_proof TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
      )
    `);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_dna_module ON ${DatabaseHelper.TBL}(module)`);
  }
  async insertDna(r: DnaRecord): Promise<void> {
    await this.store.executeSql(
      `INSERT OR REPLACE INTO ${DatabaseHelper.TBL} VALUES (?,?,?,?,?,?,?,?,?,?,?)`,
      [r.dna, r.module, r.action, r.creator, r.ganzhi, r.gua, r.hash, r.timestamp,
       JSON.stringify(r.metadata || {}), JSON.stringify(r.sovereigntyProof || {}), new Date().toISOString()]
    );
  }
  async queryDna(dna: string): Promise<DnaRecord | null> {
    const r = await this.store.query(`SELECT * FROM ${DatabaseHelper.TBL} WHERE dna = ?`, [dna]);
    return r.goToFirstRow() ? this.row(r) : null;
  }
  async queryByModule(m: string): Promise<DnaRecord[]> {
    const recs: DnaRecord[] = [];
    const r = await this.store.query(`SELECT * FROM ${DatabaseHelper.TBL} WHERE module = ? ORDER BY created_at DESC`, [m]);
    while (r.goToNextRow()) recs.push(this.row(r));
    return recs;
  }
  async listAll(): Promise<DnaRecord[]> {
    const recs: DnaRecord[] = [];
    const r = await this.store.query(`SELECT * FROM ${DatabaseHelper.TBL} ORDER BY created_at DESC LIMIT 100`);
    while (r.goToNextRow()) recs.push(this.row(r));
    return recs;
  }
  private row(r: any): DnaRecord {
    return {
      dna: r.getString(r.getColumnIndex('dna')),
      module: r.getString(r.getColumnIndex('module')),
      action: r.getString(r.getColumnIndex('action')),
      creator: r.getString(r.getColumnIndex('creator')),
      ganzhi: r.getString(r.getColumnIndex('ganzhi')),
      gua: r.getString(r.getColumnIndex('gua')),
      hash: r.getString(r.getColumnIndex('hash')),
      timestamp: r.getString(r.getColumnIndex('timestamp')),
      metadata: JSON.parse(r.getString(r.getColumnIndex('metadata')) || '{}'),
      sovereigntyProof: JSON.parse(r.getString(r.getColumnIndex('sovereignty_proof')) || '{}')
    };
  }
}
