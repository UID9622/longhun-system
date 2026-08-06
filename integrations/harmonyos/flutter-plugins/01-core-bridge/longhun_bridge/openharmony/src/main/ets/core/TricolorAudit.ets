// 🐉 三色审计引擎
// DNA: #龍芯⚡️2026-08-06-TRICOLOR-AUDIT-V2.0-UID9622
// License: MulanPSL v2

import hilog from '@ohos.hilog';
import { DNAGenerator } from './DNAGenerator';

const TAG: string = 'TricolorAudit';
const DOMAIN: number = 0xFF05;

export interface AuditResult {
  status: string;  // 🟢 🟡 🔴
  score: number;   // 0-100
  violations: string[];
  warnings: string[];
  dna: string;
  timestamp: string;
  dimensions: Record<string, number>;
}

/**
 * 三色审计引擎
 * 基于六维加权计算R值，自动判定审计状态
 */
export class TricolorAudit {
  // 六维权重（P0级焊死）
  private static readonly WEIGHTS: Record<string, number> = {
    humanWelfare: 0.20,
    fairness: 0.20,
    controllability: 0.15,
    transparency: 0.15,
    traceability: 0.15,
    privacy: 0.15,
  };

  private static readonly DIMENSIONS = [
    'humanWelfare', 'fairness', 'controllability',
    'transparency', 'traceability', 'privacy',
  ];

  private static readonly THRESHOLDS = { red: 40, yellow: 60, green: 85 };

  private static readonly DIMENSION_NAMES: Record<string, string> = {
    humanWelfare: '人类福祉',
    fairness: '公平公正',
    controllability: '可控可信',
    transparency: '透明可解释',
    traceability: '责任可追溯',
    privacy: '隐私保护',
  };

  static run(data: any): AuditResult {
    const dimensions = this.calculateDimensions(data);
    const score = this.calculateScore(dimensions);
    const status = this.determineStatus(score);
    const { violations, warnings } = this.detectIssues(dimensions, data);
    const dna = DNAGenerator.generate('AUDIT');

    return {
      status, score, violations, warnings,
      dna, timestamp: new Date().toISOString(), dimensions,
    };
  }

  private static calculateDimensions(data: any): Record<string, number> {
    const dims: Record<string, number> = {};
    for (const dim of this.DIMENSIONS) {
      const value = data[dim];
      dims[dim] = (typeof value === 'number') ? Math.min(100, Math.max(0, value)) : 50;
    }
    return dims;
  }

  private static calculateScore(dimensions: Record<string, number>): number {
    let raw = 0;
    for (const dim of this.DIMENSIONS) {
      raw += (this.WEIGHTS[dim] || 0) * (dimensions[dim] || 0);
    }
    return Math.min(95, Math.round(raw));
  }

  private static determineStatus(score: number): string {
    if (score >= this.THRESHOLDS.green) return '🟢';
    if (score >= this.THRESHOLDS.yellow) return '🟡';
    return '🔴';
  }

  private static detectIssues(
    dimensions: Record<string, number>,
    data: any
  ): { violations: string[]; warnings: string[] } {
    const violations: string[] = [];
    const warnings: string[] = [];

    for (const dim of this.DIMENSIONS) {
      const score = dimensions[dim] || 0;
      const name = this.DIMENSION_NAMES[dim] || dim;
      if (score < this.THRESHOLDS.red) {
        violations.push(`${name}得分过低 (${score}/100)`);
      } else if (score < this.THRESHOLDS.yellow) {
        warnings.push(`${name}得分偏低 (${score}/100)，建议优化`);
      }
    }

    if (data.hasRedLine === true) {
      violations.push('触犯🔴红线，需立即停止');
    }

    return { violations, warnings };
  }
}
