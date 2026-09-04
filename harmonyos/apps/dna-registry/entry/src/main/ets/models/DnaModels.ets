/**
 * 龙魂·DNA数据模型
 * License: MulanPSL v2
 */
export interface DnaRecord {
  dna: string;
  module: string;
  action: string;
  creator: string;
  ganzhi: string;
  gua: string;
  hash: string;
  timestamp: string;
  metadata: Record<string, string>;
  sovereigntyProof: SovereigntyProof;
}
export interface DnaGenerateRequest {
  module: string;
  action: string;
  metadata?: Record<string, string>;
}
export interface SovereigntyProof {
  creatorDNA: string;
  deviceFingerprint: string;
  timestamp: string;
  signature: string;
  auditMark: string;
}
