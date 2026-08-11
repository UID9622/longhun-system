/**
 * 🐉 龍魂 · 耻辱墙
 * 错误操作公开记账，不可删除
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-WALL-OF-SHAME-v2.0-UID9622
 */
import { DNAEngine } from './DNAEngine';

export interface ShameRecord {
  id: string;
  timestamp: string;
  vehicleId: string;
  errorType: 'navigation_error' | 'collection_failure' | 'ads_mistake' | 'tampering' | 'other';
  errorDetail: string;
  severity: 1 | 2 | 3 | 4 | 5;
  dna: string;
  status: 'pending' | 'fixing' | 'resolved';
  resolution?: string;
  resolvedAt?: string;
}

export class WallOfShame {
  private static records: ShameRecord[] = [];

  /**
   * 登记错误
   */
  static register(
    vehicleId: string,
    errorType: ShameRecord['errorType'],
    errorDetail: string,
    severity: 1 | 2 | 3 | 4 | 5
  ): ShameRecord {
    const timestamp = new Date().toISOString();
    const id = `SHAME-${Date.now().toString(36)}-${Math.random().toString(36).substring(2, 6)}`;
    const dna = DNAEngine.generateDNA(vehicleId, 'SHAME', `${errorType}:${errorDetail}`);

    const record: ShameRecord = {
      id, timestamp, vehicleId, errorType, errorDetail,
      severity, dna, status: 'pending'
    };

    this.records.push(record);
    return record;
  }

  /**
   * 标记已修复
   */
  static resolve(id: string, resolution: string): boolean {
    const record = this.records.find(r => r.id === id);
    if (!record) return false;
    record.status = 'resolved';
    record.resolution = resolution;
    record.resolvedAt = new Date().toISOString();
    return true;
  }

  /**
   * 获取耻辱墙列表（公开可查）
   */
  static getShameWall(): ShameRecord[] {
    return [...this.records];
  }

  /**
   * 按车辆查询
   */
  static getByVehicle(vehicleId: string): ShameRecord[] {
    return this.records.filter(r => r.vehicleId === vehicleId);
  }

  /**
   * 统计
   */
  static getStats(): {
    total: number; pending: number; resolved: number;
    bySeverity: Record<number, number>;
  } {
    const bySeverity: Record<number, number> = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 };
    let pending = 0, resolved = 0;
    this.records.forEach(r => {
      bySeverity[r.severity] = (bySeverity[r.severity] || 0) + 1;
      if (r.status === 'pending') pending++;
      if (r.status === 'resolved') resolved++;
    });
    return { total: this.records.length, pending, resolved, bySeverity };
  }

  /**
   * 导出耻辱墙JSON
   */
  static export(): string {
    return JSON.stringify(this.records, null, 2);
  }
}

/**
 * 道德经注释
 * 第41章: "大器晚成" → 错误要公开记录，才能成就大器
 * 第63章: "图难于其易" → 从错误中学习
 */
