/**
 * 龙魂·记忆调度器 — 定时压缩
 * License: MulanPSL v2
 */
import { MemoryEngine } from './MemoryEngine';

export class MemoryScheduler {
  private engine: MemoryEngine;
  private timer: number | null = null;

  constructor(engine: MemoryEngine) { this.engine = engine; }

  start(intervalHours: number): void {
    this.stop();
    const ms = intervalHours * 3600000;
    this.timer = setInterval(() => {
      this.engine.compressAll(7).then(r => {
        console.info(`[龍魂记忆] 定时压缩完成: ${r.compressedCount}/${r.totalCount}`);
      });
    }, ms);
    console.info(`[龍魂记忆] 调度器启动·间隔${intervalHours}h`);
  }

  stop(): void {
    if (this.timer) { clearInterval(this.timer); this.timer = null; }
  }

  async scheduleCompress(dna: string): Promise<void> {
    // 有非压缩条目时触发异步压缩
    const stats = await this.engine.stats();
    if (stats.total > 0 && (stats.total - (stats.compressed || 0)) > 10) {
      this.engine.compressAll(7);
    }
  }
}
