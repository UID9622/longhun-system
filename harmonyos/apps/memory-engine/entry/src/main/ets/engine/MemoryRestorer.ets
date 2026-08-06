/**
 * 龙魂·记忆恢复器
 * License: MulanPSL v2
 */
import { MemoryEntry } from './models/MemoryModels';

export class MemoryRestorer {
  async restore(entry: MemoryEntry): Promise<MemoryEntry> {
    if (!entry.compressed) return entry;
    return {
      ...entry,
      raw: this.decompress(entry.compressed),
      compressed: null,
      restoredAt: new Date().toISOString()
    };
  }
  private decompress(c: string): string {
    return c.startsWith('[压缩]') ? c.replace('[压缩] ', '').replace(/\[KW:.*\]/, '') : c;
  }
}
