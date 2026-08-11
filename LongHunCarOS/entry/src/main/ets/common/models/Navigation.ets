/**
 * 🐉 龍魂 · 导航模型
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-NAV-MODEL-v2.0-UID9622
 */
export interface Navigation {
  id: string;
  vehicleId: string;
  sancaiDecision: string;
  hexagram: string;
  hexagramColor: string;
  route: object[];
  dna: string;
  timestamp: string;
}
