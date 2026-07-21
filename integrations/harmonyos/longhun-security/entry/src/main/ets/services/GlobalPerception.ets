// entry/src/main/ets/services/GlobalPerception.ets
// 龍魂 · 全域感知引擎 · 传感器融合+异常检测
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️ | UID: 9622

import { PerceptionData, PerceptionType, ThreatLevel } from '../models/SecurityModel';

export class GlobalPerception {
  private static instance: GlobalPerception;
  private sensors: Map<PerceptionType, boolean> = new Map();
  private perceptionHistory: PerceptionData[] = [];
  private threatThresholds: Map<PerceptionType, number> = new Map();
  private readonly HISTORY_SIZE: number = 1000;

  static getInstance(): GlobalPerception {
    if (!GlobalPerception.instance) {
      GlobalPerception.instance = new GlobalPerception();
    }
    return GlobalPerception.instance;
  }

  private constructor() {
    this.initThresholds();
  }

  private initThresholds(): void {
    this.threatThresholds.set(PerceptionType.MOTION, 50);
    this.threatThresholds.set(PerceptionType.SOUND, 80);
    this.threatThresholds.set(PerceptionType.TEMPERATURE, 60);
    this.threatThresholds.set(PerceptionType.HUMIDITY, 90);
    this.threatThresholds.set(PerceptionType.LIGHT, 10);
    this.threatThresholds.set(PerceptionType.PRESSURE, 1000);
    this.threatThresholds.set(PerceptionType.PROXIMITY, 0.5);
    this.threatThresholds.set(PerceptionType.ACCELERATION, 5);
  }

  enableSensor(type: PerceptionType): void {
    this.sensors.set(type, true);
    console.info(`[龍魂·全域感知] 启用传感器: ${type}`);
  }

  disableSensor(type: PerceptionType): void {
    this.sensors.set(type, false);
    console.info(`[龍魂·全域感知] 禁用传感器: ${type}`);
  }

  receiveData(data: PerceptionData): void {
    if (!this.sensors.get(data.type)) return;

    this.perceptionHistory.push(data);
    if (this.perceptionHistory.length > this.HISTORY_SIZE) {
      this.perceptionHistory = this.perceptionHistory.slice(-this.HISTORY_SIZE);
    }

    const threat = this.assessThreat(data);
    data.threatLevel = threat.level;
    data.description = threat.description;

    if (threat.level >= ThreatLevel.MEDIUM) {
      this.triggerAlert(data);
    }

    console.info(`[龍魂·全域感知] ${data.type}=${data.value}${data.unit} 威胁:${threat.level}`);
  }

  private assessThreat(data: PerceptionData): { level: ThreatLevel, description: string } {
    const threshold = this.threatThresholds.get(data.type);
    if (!threshold) {
      return { level: ThreatLevel.NONE, description: '无阈值配置' };
    }

    const ratio = data.value / threshold;

    if (ratio >= 3.0) return { level: ThreatLevel.CRITICAL, description: `${data.type}严重异常: ${data.value}` };
    if (ratio >= 2.0) return { level: ThreatLevel.HIGH, description: `${data.type}高度异常: ${data.value}` };
    if (ratio >= 1.5) return { level: ThreatLevel.MEDIUM, description: `${data.type}中度异常: ${data.value}` };
    if (ratio >= 1.0) return { level: ThreatLevel.LOW, description: `${data.type}轻度异常: ${data.value}` };
    return { level: ThreatLevel.NONE, description: '正常' };
  }

  private triggerAlert(data: PerceptionData): void {
    console.warn(`[龍魂·全域感知] 告警: ${data.type} [${data.threatLevel}] ${data.description}`);
    this.coordinatedResponse(data);
  }

  private coordinatedResponse(data: PerceptionData): void {
    switch (data.threatLevel) {
      case ThreatLevel.LOW: break;
      case ThreatLevel.MEDIUM: break;
      case ThreatLevel.HIGH: break;
      case ThreatLevel.CRITICAL: break;
    }
  }

  analyzeBehavior(trajectoryId: string, timeWindow: number): object {
    const recentData = this.perceptionHistory.filter(
      p => p.timestamp > Date.now() - timeWindow
    );
    const stats: Map<PerceptionType, { count: number, avg: number, max: number }> = new Map();
    for (const data of recentData) {
      const current = stats.get(data.type) || { count: 0, avg: 0, max: 0 };
      current.count++;
      current.avg = (current.avg * (current.count - 1) + data.value) / current.count;
      current.max = Math.max(current.max, data.value);
      stats.set(data.type, current);
    }
    return Object.fromEntries(stats);
  }

  getHistory(type?: PerceptionType, limit: number = 100): PerceptionData[] {
    let filtered = this.perceptionHistory;
    if (type) {
      filtered = filtered.filter(p => p.type === type);
    }
    return filtered.slice(-limit);
  }

  getActiveSensors(): PerceptionType[] {
    return Array.from(this.sensors.entries())
      .filter(([_, enabled]) => enabled)
      .map(([type, _]) => type);
  }
}

export const globalPerception = GlobalPerception.getInstance();
