/**
 * 🐉 龍魂 · 史官机制
 * 全程记录、不可篡改、哈希链验证
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-HISTORIAN-v2.0-UID9622
 */
import { HashUtil } from '../common/utils/HashUtil';
import { DNAEngine } from './DNAEngine';

export interface HistoryRecord {
  index: number;
  timestamp: string;
  vehicleId: string;
  operation: string;
  detail: string;
  dna: string;
  prevHash: string;
  hash: string;
  sancaiScore?: number;
  digitalRoot?: number;
}

export class HistorianEngine {
  private static records: HistoryRecord[] = [];
  private static chain: string[] = [];
  private static lastHash: string = '0';

  /**
   * 记录事件
   */
  static record(
    vehicleId: string,
    operation: string,
    detail: string,
    sancaiScore?: number,
    digitalRoot?: number
  ): HistoryRecord {
    const timestamp = new Date().toISOString();
    const dna = DNAEngine.generateDNA(vehicleId, operation, detail);
    const index = this.records.length;
    const prevHash = this.lastHash;
    const content = `${index}${timestamp}${vehicleId}${operation}${detail}${dna}${prevHash}`;
    const hash = HashUtil.sha256(content);

    const record: HistoryRecord = {
      index, timestamp, vehicleId, operation, detail,
      dna, prevHash, hash, sancaiScore, digitalRoot
    };

    this.records.push(record);
    this.chain.push(hash);
    this.lastHash = hash;

    return record;
  }

  /**
   * 验证链完整性
   */
  static verifyChain(): { valid: boolean; brokenAt?: number } {
    for (let i = 0; i < this.records.length; i++) {
      const record = this.records[i];
      const content = `${i}${record.timestamp}${record.vehicleId}${record.operation}${record.detail}${record.dna}${i === 0 ? '0' : this.records[i - 1].hash}`;
      const computedHash = HashUtil.sha256(content);
      if (computedHash !== record.hash) {
        return { valid: false, brokenAt: i };
      }
    }
    return { valid: true };
  }

  /**
   * 获取完整历史
   */
  static getHistory(): HistoryRecord[] {
    return [...this.records];
  }

  /**
   * 按车辆查询
   */
  static getByVehicle(vehicleId: string): HistoryRecord[] {
    return this.records.filter(r => r.vehicleId === vehicleId);
  }

  /**
   * 按DNA查询
   */
  static getByDNA(dna: string): HistoryRecord | undefined {
    return this.records.find(r => r.dna === dna);
  }
}

/**
 * 道德经注释
 * 第63章: "图难于其易，为大于其细" → 史官记录每一件小事
 * 第64章: "慎终如始，则无败事" → 史官验证确保链条完整
 */
