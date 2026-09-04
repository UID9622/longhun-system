/**
 * 龙魂·审计数据模型
 * DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-AUDIT-MODELS
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 */

export type AuditColor = '🟢' | '🟡' | '🔴';

export interface AuditInput {
  description: string;
  auditTarget: string;
  department?: string;
  tags?: string[];
  gates?: string[];
  metadata?: Record<string, string>;
}

export interface DimensionScore {
  name: string;
  score: number;
  weight: number;
  weightedScore: number;
}

export interface GateResult {
  name: string;
  passed: boolean;
  detail: string;
  score: number;
}

export interface SovereignSeal {
  sovereign: string;
  creatorDNA: string;
  deviceFingerprint: string;
  timestamp: string;
  signature: string;
  gpgFingerprint: string;
}

export interface AuditResult {
  dna: string;
  color: AuditColor;
  rValue: number;
  scores: DimensionScore[];
  gateResults: GateResult[];
  sovereignSeal: SovereignSeal;
  timestamp: string;
  elapsedMs: number;
  summary: string;
}

export interface AuditRecord {
  id: number;
  dna: string;
  color: AuditColor;
  rValue: number;
  description: string;
  target: string;
  timestamp: string;
  sealed: boolean;
}
