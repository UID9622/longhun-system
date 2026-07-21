// entry/src/main/ets/database/VoiceDatabase.ets
// 龍魂 · 语音数据库

import { relationalStore } from '@kit.ArkData';
import { VoiceModel, VoiceEngineType, LanguageType, DialectType } from '../models/VoiceModel';

const DB_NAME = 'longhun_voice.db';
const DB_VERSION = 1;

export class VoiceDatabase {
  private static instance: VoiceDatabase;
  private rdbStore: relationalStore.RdbStore | null = null;

  static getInstance(): VoiceDatabase {
    if (!VoiceDatabase.instance) VoiceDatabase.instance = new VoiceDatabase();
    return VoiceDatabase.instance;
  }

  static async init(): Promise<void> {
    const db = VoiceDatabase.getInstance();
    await db.initialize();
  }

  private async initialize(): Promise<void> {
    if (this.rdbStore) return;

    const storeConfig: relationalStore.StoreConfig = {
      name: DB_NAME,
      securityLevel: relationalStore.SecurityLevel.S3
    };

    try {
      this.rdbStore = await relationalStore.getRdbStore(this.context, storeConfig);
      await this.createTables();
      await this.seedData();
      console.info('[龍魂] 语音数据库初始化完成');
    } catch (err) {
      console.error(`[龍魂] 数据库初始化失败: ${JSON.stringify(err)}`);
    }
  }

  private async createTables(): Promise<void> {
    if (!this.rdbStore) return;

    // 模型表
    await this.rdbStore.executeSql(`
      CREATE TABLE IF NOT EXISTS voice_models (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        engine_type TEXT NOT NULL,
        language TEXT NOT NULL,
        dialect TEXT,
        version TEXT NOT NULL,
        size REAL DEFAULT 0,
        path TEXT DEFAULT '',
        accuracy REAL DEFAULT 0.95,
        latency INTEGER DEFAULT 200,
        memory_usage INTEGER DEFAULT 100,
        is_downloaded INTEGER DEFAULT 0,
        is_loaded INTEGER DEFAULT 0,
        is_enabled INTEGER DEFAULT 1,
        downloaded_at TEXT,
        loaded_at TEXT,
        dna_signature TEXT NOT NULL
      )
    `);

    // 识别结果表
    await this.rdbStore.executeSql(`
      CREATE TABLE IF NOT EXISTS asr_results (
        id TEXT PRIMARY KEY,
        text TEXT NOT NULL,
        confidence REAL DEFAULT 0,
        is_final INTEGER DEFAULT 0,
        start_time INTEGER DEFAULT 0,
        end_time INTEGER DEFAULT 0,
        detected_language TEXT DEFAULT 'zh-CN',
        detected_dialect TEXT,
        created_at TEXT NOT NULL
      )
    `);

    // 字幕表
    await this.rdbStore.executeSql(`
      CREATE TABLE IF NOT EXISTS captions (
        id TEXT PRIMARY KEY,
        text TEXT NOT NULL,
        speaker_id TEXT,
        start_time INTEGER DEFAULT 0,
        end_time INTEGER DEFAULT 0,
        confidence REAL DEFAULT 0,
        is_final INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
      )
    `);

    // 对话表
    await this.rdbStore.executeSql(`
      CREATE TABLE IF NOT EXISTS dialogs (
        id TEXT PRIMARY KEY,
        role TEXT NOT NULL,
        text TEXT NOT NULL,
        audio_url TEXT,
        intent TEXT,
        slots TEXT,
        is_playing INTEGER DEFAULT 0,
        is_error INTEGER DEFAULT 0,
        timestamp TEXT NOT NULL
      )
    `);

    // 声纹表
    await this.rdbStore.executeSql(`
      CREATE TABLE IF NOT EXISTS voice_prints (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        name TEXT NOT NULL,
        features TEXT NOT NULL,
        sample_count INTEGER DEFAULT 0,
        samples TEXT,
        threshold REAL DEFAULT 0.85,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        dna_signature TEXT NOT NULL
      )
    `);

    // 索引
    await this.rdbStore.executeSql(`CREATE INDEX IF NOT EXISTS idx_models_engine ON voice_models(engine_type, language)`);
    await this.rdbStore.executeSql(`CREATE INDEX IF NOT EXISTS idx_asr_created ON asr_results(created_at DESC)`);
    await this.rdbStore.executeSql(`CREATE INDEX IF NOT EXISTS idx_captions_created ON captions(created_at DESC)`);
    await this.rdbStore.executeSql(`CREATE INDEX IF NOT EXISTS idx_dialogs_timestamp ON dialogs(timestamp DESC)`);
    await this.rdbStore.executeSql(`CREATE INDEX IF NOT EXISTS idx_voice_prints_user ON voice_prints(user_id)`);
  }

  private async seedData(): Promise<void> {
    if (!this.rdbStore) return;

    const result = await this.rdbStore.querySql('SELECT COUNT(*) as count FROM voice_models');
    if (result.rowCount > 0) {
      result.goToFirstRow();
      const count = result.getLong(result.getColumnIndex('count'));
      if (count > 0) return;
    }

    const seedModels = [
      { id: 'ASR-ZH-v1', name: '中文语音识别模型', engineType: VoiceEngineType.ASR, language: LanguageType.ZH_CN, size: 120, accuracy: 0.96, latency: 180 },
      { id: 'ASR-EN-v1', name: '英文语音识别模型', engineType: VoiceEngineType.ASR, language: LanguageType.EN_US, size: 95, accuracy: 0.94, latency: 160 },
      { id: 'TTS-ZH-v1', name: '中文语音合成模型', engineType: VoiceEngineType.TTS, language: LanguageType.ZH_CN, size: 80, accuracy: 0.95, latency: 150 },
      { id: 'TTS-EN-v1', name: '英文语音合成模型', engineType: VoiceEngineType.TTS, language: LanguageType.EN_US, size: 70, accuracy: 0.93, latency: 130 },
      { id: 'WAKE-ZH-v1', name: '中文唤醒词模型', engineType: VoiceEngineType.WAKE, language: LanguageType.ZH_CN, size: 15, accuracy: 0.97, latency: 50 },
      { id: 'VPR-v1', name: '声纹识别模型', engineType: VoiceEngineType.VPR, language: LanguageType.ZH_CN, size: 25, accuracy: 0.92, latency: 100 },
      { id: 'NSE-v1', name: '噪声抑制模型', engineType: VoiceEngineType.NSE, language: LanguageType.ZH_CN, size: 30, accuracy: 0.90, latency: 60 }
    ];

    for (const model of seedModels) {
      const dna = `SM3-${model.id}-${model.name}-${model.engineType}-v1`;
      await this.rdbStore.executeSql(
        `INSERT INTO voice_models (id, name, engine_type, language, version, size, accuracy, latency, is_downloaded, is_loaded, dna_signature)
         VALUES (?, ?, ?, ?, '1.0.0', ?, ?, ?, 0, 0, ?)`,
        [model.id, model.name, model.engineType, model.language, model.size, model.accuracy, model.latency, dna]
      );
    }

    console.info('[龍魂] 种子数据已写入');
  }

  // === CRUD: 模型 ===
  async getModels(): Promise<VoiceModel[]> {
    if (!this.rdbStore) return [];
    const result = await this.rdbStore.querySql('SELECT * FROM voice_models ORDER BY engine_type, language');
    const models: VoiceModel[] = [];
    while (result.goToNextRow()) {
      models.push(new VoiceModel({
        id: result.getString(result.getColumnIndex('id')),
        name: result.getString(result.getColumnIndex('name')),
        engineType: result.getString(result.getColumnIndex('engine_type')) as VoiceEngineType,
        language: result.getString(result.getColumnIndex('language')) as LanguageType,
        version: result.getString(result.getColumnIndex('version')),
        size: result.getDouble(result.getColumnIndex('size')),
        accuracy: result.getDouble(result.getColumnIndex('accuracy')),
        latency: result.getLong(result.getColumnIndex('latency')),
        isDownloaded: result.getLong(result.getColumnIndex('is_downloaded')) === 1,
        isLoaded: result.getLong(result.getColumnIndex('is_loaded')) === 1
      }));
    }
    return models;
  }

  async updateModelStatus(id: string, isDownloaded: boolean, isLoaded: boolean): Promise<void> {
    if (!this.rdbStore) return;
    const now = new Date().toISOString();
    await this.rdbStore.executeSql(
      `UPDATE voice_models SET is_downloaded = ?, is_loaded = ?, ${isDownloaded ? 'downloaded_at' : ''} = ? WHERE id = ?`,
      [isDownloaded ? 1 : 0, isLoaded ? 1 : 0, now, id]
    );
  }

  // === CRUD: 识别结果 ===
  async insertASRResult(id: string, text: string, confidence: number, isFinal: boolean): Promise<void> {
    if (!this.rdbStore) return;
    await this.rdbStore.executeSql(
      `INSERT INTO asr_results (id, text, confidence, is_final, start_time, end_time, created_at)
       VALUES (?, ?, ?, ?, 0, 0, ?)`,
      [id, text, confidence, isFinal ? 1 : 0, new Date().toISOString()]
    );
  }

  async getRecentASRResults(limit: number = 50): Promise<any[]> {
    if (!this.rdbStore) return [];
    const result = await this.rdbStore.querySql(`SELECT * FROM asr_results ORDER BY created_at DESC LIMIT ${limit}`);
    const results: any[] = [];
    while (result.goToNextRow()) {
      results.push({
        id: result.getString(result.getColumnIndex('id')),
        text: result.getString(result.getColumnIndex('text')),
        confidence: result.getDouble(result.getColumnIndex('confidence')),
        isFinal: result.getLong(result.getColumnIndex('is_final')) === 1
      });
    }
    return results;
  }

  async clearASRResults(): Promise<void> {
    if (!this.rdbStore) return;
    await this.rdbStore.executeSql('DELETE FROM asr_results');
  }

  // === CRUD: 字幕 ===
  async insertCaption(id: string, text: string, speakerId?: string): Promise<void> {
    if (!this.rdbStore) return;
    await this.rdbStore.executeSql(
      `INSERT INTO captions (id, text, speaker_id, created_at) VALUES (?, ?, ?, ?)`,
      [id, text, speakerId || '', new Date().toISOString()]
    );
  }

  async getRecentCaptions(limit: number = 50): Promise<any[]> {
    if (!this.rdbStore) return [];
    const result = await this.rdbStore.querySql(`SELECT * FROM captions ORDER BY created_at DESC LIMIT ${limit}`);
    const captions: any[] = [];
    while (result.goToNextRow()) {
      captions.push({
        id: result.getString(result.getColumnIndex('id')),
        text: result.getString(result.getColumnIndex('text')),
        speakerId: result.getString(result.getColumnIndex('speaker_id'))
      });
    }
    return captions;
  }

  async clearCaptions(): Promise<void> {
    if (!this.rdbStore) return;
    await this.rdbStore.executeSql('DELETE FROM captions');
  }

  // === CRUD: 对话 ===
  async insertDialog(id: string, role: string, text: string, intent?: string): Promise<void> {
    if (!this.rdbStore) return;
    await this.rdbStore.executeSql(
      `INSERT INTO dialogs (id, role, text, intent, timestamp) VALUES (?, ?, ?, ?, ?)`,
      [id, role, text, intent || '', new Date().toISOString()]
    );
  }

  async getRecentDialogs(limit: number = 50): Promise<any[]> {
    if (!this.rdbStore) return [];
    const result = await this.rdbStore.querySql(`SELECT * FROM dialogs ORDER BY timestamp DESC LIMIT ${limit}`);
    const dialogs: any[] = [];
    while (result.goToNextRow()) {
      dialogs.push({
        id: result.getString(result.getColumnIndex('id')),
        role: result.getString(result.getColumnIndex('role')),
        text: result.getString(result.getColumnIndex('text')),
        intent: result.getString(result.getColumnIndex('intent'))
      });
    }
    return dialogs;
  }

  async clearDialogs(): Promise<void> {
    if (!this.rdbStore) return;
    await this.rdbStore.executeSql('DELETE FROM dialogs');
  }

  // === 过期清理 ===
  async cleanExpiredData(retentionDays: number = 30): Promise<void> {
    if (!this.rdbStore) return;
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - retentionDays);
    const cutoffStr = cutoff.toISOString();

    await this.rdbStore.executeSql(`DELETE FROM asr_results WHERE created_at < ?`, [cutoffStr]);
    await this.rdbStore.executeSql(`DELETE FROM captions WHERE created_at < ?`, [cutoffStr]);
    await this.rdbStore.executeSql(`DELETE FROM dialogs WHERE timestamp < ?`, [cutoffStr]);
    console.info(`[龍魂] 已清理 ${retentionDays} 天前的过期数据`);
  }

  // === 统计 ===
  async getStats(): Promise<{ asrCount: number; captionCount: number; dialogCount: number; modelCount: number }> {
    if (!this.rdbStore) return { asrCount: 0, captionCount: 0, dialogCount: 0, modelCount: 0 };

    const asrResult = await this.rdbStore.querySql('SELECT COUNT(*) as count FROM asr_results');
    const captionResult = await this.rdbStore.querySql('SELECT COUNT(*) as count FROM captions');
    const dialogResult = await this.rdbStore.querySql('SELECT COUNT(*) as count FROM dialogs');
    const modelResult = await this.rdbStore.querySql('SELECT COUNT(*) as count FROM voice_models');

    asrResult.goToFirstRow(); captionResult.goToFirstRow();
    dialogResult.goToFirstRow(); modelResult.goToFirstRow();

    return {
      asrCount: asrResult.getLong(asrResult.getColumnIndex('count')),
      captionCount: captionResult.getLong(captionResult.getColumnIndex('count')),
      dialogCount: dialogResult.getLong(dialogResult.getColumnIndex('count')),
      modelCount: modelResult.getLong(modelResult.getColumnIndex('count'))
    };
  }
}
