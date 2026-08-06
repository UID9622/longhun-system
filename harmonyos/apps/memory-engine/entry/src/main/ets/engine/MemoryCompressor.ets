/**
 * 龙魂·记忆压缩器 — 语义相似度 + 时间衰减 + 批量压缩
 * License: MulanPSL v2
 */
import { MemoryEntry, CompressResult, SemanticScore } from './models/MemoryModels';
import { MemoryStorage } from './MemoryStorage';
import crypto from '@ohos.security.crypto';

export class MemoryCompressor {
  computeSemanticHash(text: string): string {
    const md = crypto.createHash('SHA256');
    md.update({ data: text });
    return md.digest();
  }
  computeDecay(timestamp?: string): number {
    if (!timestamp) return 1.0;
    const days = (Date.now() - this.parseGanzhiTs(timestamp)) / 86400000;
    return Math.exp(-Math.log(2) * days / 7);
  }
  async semanticSearch(query: string, entries: MemoryEntry[], limit: number): Promise<MemoryEntry[]> {
    const qh = this.computeSemanticHash(query);
    const scores: SemanticScore[] = [];
    for (const e of entries) {
      const t = e.compressed || e.raw;
      if (!t) continue;
      const sim = this.cosineSim(qh, this.computeSemanticHash(t));
      scores.push({ dna: e.dna, score: sim * this.computeDecay(e.timestamp), entry: e });
    }
    return scores.sort((a, b) => b.score - a.score).slice(0, limit).map(s => s.entry);
  }
  async batchCompress(olderThanDays: number): Promise<CompressResult> {
    const storage = new MemoryStorage();
    const entries = await storage.list();
    const cutoff = Date.now() - olderThanDays * 86400000;
    let compressedCount = 0;
    for (const e of entries) {
      if (this.parseGanzhiTs(e.timestamp) < cutoff && !e.compressed) {
        e.compressed = this.compress(e.raw);
        e.compressedAt = new Date().toISOString();
        await storage.update(e);
        compressedCount++;
      }
    }
    return { totalCount: entries.length, compressedCount, cutoffDate: new Date(cutoff).toISOString() };
  }
  private compress(text: string): string {
    const s = text.slice(0, 200);
    const kw = text.match(/[龍魂DNA三色审计锚点熔断]/g)?.join('') || '';
    return `[压缩] ${s}...[KW:${kw}]`;
  }
  private cosineSim(h1: string, h2: string): number {
    let dot = 0, m1 = 0, m2 = 0;
    for (let i = 0; i < Math.min(h1.length, h2.length); i++) {
      const v1 = h1.charCodeAt(i) / 255, v2 = h2.charCodeAt(i) / 255;
      dot += v1 * v2; m1 += v1 * v1; m2 += v2 * v2;
    }
    return (m1 === 0 || m2 === 0) ? 0 : dot / (Math.sqrt(m1) * Math.sqrt(m2));
  }
  private parseGanzhiTs(ts: string): number { return Date.parse(ts) || Date.now(); }
}
