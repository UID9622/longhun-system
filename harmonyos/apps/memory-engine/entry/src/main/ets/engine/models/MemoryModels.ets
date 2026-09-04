/**
 * 龙魂·记忆数据模型
 * License: MulanPSL v2
 */
export interface MemoryEntry {
  dna: string;
  raw: string;
  compressed: string | null;
  semanticHash: string;
  decayWeight: number;
  timestamp: string;
  sovereigntyTag: string;
  metadata: Record<string, string>;
  compressedAt?: string;
  restoredAt?: string;
}

export interface CompressResult {
  totalCount: number;
  compressedCount: number;
  cutoffDate: string;
}

export interface RestoreResult {
  dna: string;
  success: boolean;
  integrity: 'FULL' | 'PARTIAL' | 'FAILED';
  error?: string;
}

export interface SemanticScore {
  dna: string;
  score: number;
  entry: MemoryEntry;
}
