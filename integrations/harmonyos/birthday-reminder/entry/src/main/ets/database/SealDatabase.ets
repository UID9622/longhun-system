// 龍魂 · 印章数据库 · 关系型存储
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { relationalStore } from '@kit.ArkData';

const STORE_NAME = 'LongHunSeal.db';
const TABLE_SEALS = 'seals';
const TABLE_APPLICATIONS = 'applications';
const TABLE_APPROVALS = 'approvals';
const TABLE_OUT_RECORDS = 'out_records';
const TABLE_GPS_TRACKS = 'gps_tracks';
const TABLE_CHECK_INS = 'check_ins';

export class SealDatabase {
  private static store: relationalStore.RdbStore | null = null;

  static async init(context: Context): Promise<void> {
    const config: relationalStore.StoreConfig = {
      name: STORE_NAME,
      securityLevel: relationalStore.SecurityLevel.S3,
      encrypt: true
    };

    this.store = await relationalStore.getRdbStore(context, config);

    // 印章表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_SEALS} (
        id TEXT PRIMARY KEY,
        seal_no TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        type TEXT,
        material TEXT,
        status TEXT,
        diameter INTEGER,
        shape TEXT,
        pattern TEXT,
        font TEXT,
        custodian TEXT,
        deputy_custodian TEXT,
        department TEXT,
        vault_location TEXT,
        safe_no TEXT,
        rfid_tag TEXT,
        fingerprint_lock INTEGER,
        face_lock INTEGER,
        gps_tracker INTEGER,
        engrave_date INTEGER,
        record_date INTEGER,
        expiry_date INTEGER,
        last_used_date INTEGER,
        use_count INTEGER DEFAULT 0,
        destroy_date INTEGER,
        created_at INTEGER,
        updated_at INTEGER,
        dna_signature TEXT
      )
    `);

    // 申请表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_APPLICATIONS} (
        id TEXT PRIMARY KEY,
        app_no TEXT NOT NULL UNIQUE,
        seal_id TEXT,
        seal_name TEXT,
        seal_type TEXT,
        applicant TEXT,
        department TEXT,
        apply_date INTEGER,
        usage_type TEXT,
        usage_desc TEXT,
        document_name TEXT,
        document_count INTEGER DEFAULT 1,
        document_pages INTEGER DEFAULT 1,
        urgency TEXT DEFAULT '普通',
        document_path TEXT,
        attachment_paths TEXT,
        approval_level TEXT,
        executor TEXT,
        execute_time INTEGER,
        execute_location TEXT,
        witness TEXT,
        photos TEXT,
        gps_lat REAL,
        gps_lng REAL,
        fingerprint_verify INTEGER DEFAULT 0,
        face_verify INTEGER DEFAULT 0,
        result TEXT DEFAULT 'pending',
        actual_count INTEGER,
        remarks TEXT,
        created_at INTEGER,
        updated_at INTEGER,
        dna_signature TEXT
      )
    `);

    // 审批记录表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_APPROVALS} (
        id TEXT PRIMARY KEY,
        application_id TEXT NOT NULL,
        level INTEGER,
        approver TEXT,
        comment TEXT,
        signature TEXT,
        timestamp INTEGER,
        dna_signature TEXT,
        FOREIGN KEY (application_id) REFERENCES ${TABLE_APPLICATIONS}(id)
      )
    `);

    // 外带记录表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_OUT_RECORDS} (
        id TEXT PRIMARY KEY,
        seal_id TEXT,
        seal_name TEXT,
        borrower TEXT,
        borrower_dept TEXT,
        borrow_date INTEGER,
        expected_return INTEGER,
        actual_return INTEGER,
        purpose TEXT,
        destination TEXT,
        escort TEXT,
        status TEXT DEFAULT 'out',
        created_at INTEGER,
        dna_signature TEXT
      )
    `);

    // GPS轨迹表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_GPS_TRACKS} (
        id TEXT PRIMARY KEY,
        record_id TEXT NOT NULL,
        lat REAL,
        lng REAL,
        accuracy REAL,
        timestamp INTEGER,
        dna_signature TEXT,
        FOREIGN KEY (record_id) REFERENCES ${TABLE_OUT_RECORDS}(id)
      )
    `);

    // 回传记录表
    await this.store.executeSql(`
      CREATE TABLE IF NOT EXISTS ${TABLE_CHECK_INS} (
        id TEXT PRIMARY KEY,
        record_id TEXT NOT NULL,
        timestamp INTEGER,
        location TEXT,
        photo_path TEXT,
        operator TEXT,
        dna_signature TEXT,
        FOREIGN KEY (record_id) REFERENCES ${TABLE_OUT_RECORDS}(id)
      )
    `);

    // 索引
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_seal_status ON ${TABLE_SEALS}(status)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_seal_type ON ${TABLE_SEALS}(type)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_app_result ON ${TABLE_APPLICATIONS}(result)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_app_applicant ON ${TABLE_APPLICATIONS}(applicant)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_out_status ON ${TABLE_OUT_RECORDS}(status)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_approval_app ON ${TABLE_APPROVALS}(application_id)`);
    await this.store.executeSql(`CREATE INDEX IF NOT EXISTS idx_gps_record ON ${TABLE_GPS_TRACKS}(record_id)`);
  }

  static getStore(): relationalStore.RdbStore | null {
    return this.store;
  }

  // === 印章 CRUD ===
  static async insertSeal(values: relationalStore.ValuesBucket): Promise<number> {
    if (!this.store) return -1;
    return await this.store.insert(TABLE_SEALS, values);
  }

  static async updateSeal(values: relationalStore.ValuesBucket, predicates: relationalStore.RdbPredicates): Promise<number> {
    if (!this.store) return -1;
    return await this.store.update(values, predicates);
  }

  static async deleteSeal(predicates: relationalStore.RdbPredicates): Promise<number> {
    if (!this.store) return -1;
    return await this.store.delete(predicates);
  }

  static async querySeals(predicates: relationalStore.RdbPredicates): Promise<relationalStore.ResultSet> {
    if (!this.store) throw new Error('Database not initialized');
    return await this.store.query(predicates);
  }

  // === 统计查询 ===
  static async getSealCountByStatus(): Promise<Map<string, number>> {
    if (!this.store) return new Map();
    const sql = `SELECT status, COUNT(*) as cnt FROM ${TABLE_SEALS} GROUP BY status`;
    const resultSet = await this.store.querySql(sql);
    const map = new Map<string, number>();
    while (resultSet.goToNextRow()) {
      map.set(resultSet.getString(0), resultSet.getLong(1));
    }
    resultSet.close();
    return map;
  }

  static async getTodayExecutionCount(): Promise<number> {
    if (!this.store) return 0;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const startOfDay = today.getTime();
    const sql = `SELECT COUNT(*) FROM ${TABLE_APPLICATIONS} WHERE result='executed' AND execute_time >= ?`;
    const resultSet = await this.store.querySql(sql, [startOfDay.toString()]);
    let count = 0;
    if (resultSet.goToFirstRow()) {
      count = resultSet.getLong(0);
    }
    resultSet.close();
    return count;
  }

  static async getPendingApprovalCount(): Promise<number> {
    if (!this.store) return 0;
    const sql = `SELECT COUNT(*) FROM ${TABLE_APPLICATIONS} WHERE result='pending'`;
    const resultSet = await this.store.querySql(sql);
    let count = 0;
    if (resultSet.goToFirstRow()) {
      count = resultSet.getLong(0);
    }
    resultSet.close();
    return count;
  }
}
