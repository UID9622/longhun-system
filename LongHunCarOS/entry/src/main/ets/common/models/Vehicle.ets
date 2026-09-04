/**
 * 🐉 龍魂 · 车辆模型
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-VEHICLE-MODEL-v2.0-UID9622
 */
export interface Vehicle {
  id: string;
  model: string;
  vin: string;
  brand: string;
  platform: string;
  adsVersion: string;
  coordinates: { lat: number; lng: number; };
  speed: number;
  heading: number;
  dna: string;
}
