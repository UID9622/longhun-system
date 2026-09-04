/**
 * 🐉 龍魂 · 审计模型
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-AUDIT-MODEL-v2.0-UID9622
 */
export interface Audit {
  id: string;
  vehicleId: string;
  type: string;
  result: '🟢' | '🟡' | '🔴';
  dna: string;
  timestamp: string;
  details: object;
}
