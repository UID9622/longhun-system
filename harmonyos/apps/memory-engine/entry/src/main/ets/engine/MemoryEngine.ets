/**
 * 龙魂·记忆压缩与恢复引擎 — MemoryEngine
 * DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-MEMORY-ENGINE
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 */
import { MemoryCompressor } from './MemoryCompressor';
import { MemoryRestorer } from './MemoryRestorer';
import { MemoryStorage } from './MemoryStorage';
import { MemoryScheduler } from './MemoryScheduler';
import { MemoryEntry, CompressResult } from './models/MemoryModels';
import { DNAGenerator } from './utils/DNAGenerator';
import { GanzhiTimestamp } from './utils/GanzhiTimestamp';

export class MemoryEngine {
  private static instance: MemoryEngine;
  private compressor = new MemoryCompressor();
  private restorer = new MemoryRestorer();
  private storage = new MemoryStorage();
  private scheduler = new MemoryScheduler(this);
  private dnaGen = new DNAGenerator();

  private constructor() { this.initSovereignty(); }
  static getInstance(): MemoryEngine {
    if (!MemoryEngine.instance) MemoryEngine.instance = new MemoryEngine();
    return MemoryEngine.instance;
  }
  private initSovereignty(): void {
    const dna = this.dnaGen.generate({ module: 'MEMORY-ENGINE', action: 'INIT', timestamp: GanzhiTimestamp.now() });
    console.info(`[龍魂记忆] 主权锚定: ${dna}`);
  }

  async ingest(raw: string, metadata?: Record<string, string>): Promise<MemoryEntry> {
    const dna = this.dnaGen.generate({ module: 'MEMORY', action: 'INGEST', timestamp: GanzhiTimestamp.now() });
    const entry: MemoryEntry = {
      dna, raw, compressed: null,
      semanticHash: await this.compressor.computeSemanticHash(raw),
      decayWeight: this.compressor.computeDecay(metadata?.timestamp),
      timestamp: GanzhiTimestamp.now(), metadata: metadata || {},
      sovereigntyTag: 'UID9622-ZHUGEXIN-🇨🇳🐉'
    };
    await this.storage.save(entry);
    this.scheduler.scheduleCompress(entry.dna);
    return entry;
  }

  async recall(dna: string): Promise<MemoryEntry | null> {
    let entry = await this.storage.query(dna);
    return (entry?.compressed) ? await this.restorer.restore(entry) : entry;
  }

  async search(query: string, limit: number = 10): Promise<MemoryEntry[]> {
    return this.compressor.semanticSearch(query, await this.storage.list(), limit);
  }

  async compressAll(olderThanDays: number = 7): Promise<CompressResult> {
    return this.compressor.batchCompress(olderThanDays);
  }

  startScheduler(intervalHours: number = 1): void { this.scheduler.start(intervalHours); }
  async stats(): Promise<Record<string, number>> { return this.storage.getStats(); }
}
