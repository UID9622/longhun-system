/**
 * 龙魂·记忆存储层 — 鸿蒙分布式KV + RDB双写
 * License: MulanPSL v2
 */
import { MemoryEntry } from './models/MemoryModels';
import distributedKVStore from '@ohos.data.distributedKVStore';
import relationalStore from '@ohos.data.relationalStore';

export class MemoryStorage {
  private kvStore: any;
  private rdbStore: any;
  private initialized: boolean = false;

  async init(): Promise<void> {
    if (this.initialized) return;

    const kvMgr = distributedKVStore.createKVManager({ bundleName: 'com.longhun.harmony', context: getContext() });
    this.kvStore = await kvMgr.getKVStore('longhun_memory_store', {
      createIfMissing: true, encrypt: true, backup: true, autoSync: true,
      kvStoreType: distributedKVStore.KVStoreType.DEVICE_COLLABORATION
    });

    this.rdbStore = await relationalStore.getRdbStore({
      name: 'LonghunMemory.db', securityLevel: relationalStore.SecurityLevel.S2
    });
    await this.rdbStore.executeSql(`
      CREATE TABLE IF NOT EXISTS memories (
        dna TEXT PRIMARY KEY, raw_text TEXT, compressed_text TEXT,
        semantic_hash TEXT, decay_weight REAL, timestamp TEXT,
        sovereignty_tag TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
      )
    `);
    this.initialized = true;
  }

  async save(entry: MemoryEntry): Promise<void> {
    if (!this.initialized) await this.init();
    await this.kvStore.put(entry.dna, JSON.stringify({
      semanticHash: entry.semanticHash, decayWeight: entry.decayWeight, timestamp: entry.timestamp
    }));
    await this.rdbStore.executeSql(
      `INSERT OR REPLACE INTO memories VALUES (?,?,?,?,?,?,?,?)`,
      [entry.dna, entry.raw, entry.compressed, entry.semanticHash, entry.decayWeight,
       entry.timestamp, entry.sovereigntyTag, new Date().toISOString()]
    );
  }

  async query(dna: string): Promise<MemoryEntry | null> {
    if (!this.initialized) await this.init();
    const r = await this.rdbStore.query(`SELECT * FROM memories WHERE dna = ?`, [dna]);
    return r.goToFirstRow() ? this.rowToEntry(r) : null;
  }

  async list(): Promise<MemoryEntry[]> {
    if (!this.initialized) await this.init();
    const entries: MemoryEntry[] = [];
    const r = await this.rdbStore.query(`SELECT * FROM memories ORDER BY created_at DESC`);
    while (r.goToNextRow()) entries.push(this.rowToEntry(r));
    return entries;
  }

  async update(entry: MemoryEntry): Promise<void> { await this.save(entry); }

  async getStats(): Promise<Record<string, number>> {
    if (!this.initialized) await this.init();
    const r = await this.rdbStore.query('SELECT COUNT(*) as t FROM memories');
    r.goToFirstRow();
    return { total: r.getLong(r.getColumnIndex('t')) };
  }

  private rowToEntry(r: any): MemoryEntry {
    return {
      dna: r.getString(r.getColumnIndex('dna')),
      raw: r.getString(r.getColumnIndex('raw_text')),
      compressed: r.getString(r.getColumnIndex('compressed_text')),
      semanticHash: r.getString(r.getColumnIndex('semantic_hash')),
      decayWeight: r.getDouble(r.getColumnIndex('decay_weight')),
      timestamp: r.getString(r.getColumnIndex('timestamp')),
      sovereigntyTag: r.getString(r.getColumnIndex('sovereignty_tag')),
      metadata: {}
    };
  }
}
