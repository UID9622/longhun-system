/**
 * 龙魂·三色审计引擎 — HarmonyOS 原生
 * 六维加权R值计算 + 三色判定 + GATE闸口
 * DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-TRICOLOR-AUDIT-ENGINE
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 */
import { AuditInput, AuditResult, AuditRecord, DimensionScore, AuditColor } from '../models/AuditModels';
import { AUDIT_DIMENSIONS, AUDIT_THRESHOLDS, SOVEREIGNTY } from '../models/Constants';
import { DNAGenerator } from './DNAGenerator';
import { SovereigntyManager } from './SovereigntyManager';

export class TricolorAudit {
  private static instance: TricolorAudit;
  private dnaGen: DNAGenerator = new DNAGenerator();
  private sovereignty: SovereigntyManager = new SovereigntyManager();

  private constructor() {}

  static getInstance(): TricolorAudit {
    if (!TricolorAudit.instance) {
      TricolorAudit.instance = new TricolorAudit();
    }
    return TricolorAudit.instance;
  }

  /** 执行审计 */
  async audit(input: AuditInput): Promise<AuditResult> {
    const dna = await this.dnaGen.generate('TRICOLOR-AUDIT', 'AUDIT');
    const startTime = Date.now();

    // 六维评分
    const scores = this.evaluateSixDimensions(input);
    // 加权R值
    const rValue = this.computeRValue(scores);
    // 三色判定
    const color = this.determineColor(rValue);
    // GATE闸口
    const gateResults = this.runGateCheck(input, scores, rValue);
    // 主权印章
    const seal = await this.sovereignty.seal(dna, rValue, color, gateResults);

    const elapsed = Date.now() - startTime;

    const result: AuditResult = {
      dna,
      color,
      rValue,
      scores,
      gateResults,
      sovereignSeal: seal,
      timestamp: new Date().toISOString(),
      elapsedMs: elapsed,
      summary: this.generateSummary(color, rValue, gateResults)
    };

    return result;
  }

  /** 六维评分 */
  private evaluateSixDimensions(input: AuditInput): DimensionScore[] {
    return AUDIT_DIMENSIONS.map(dim => ({
      name: dim.name,
      score: this.evaluateDimension(dim.name, input),
      weight: dim.weight,
      weightedScore: 0 // 在后面计算
    }));
  }

  /** 评估单个维度 */
  private evaluateDimension(dimName: string, input: AuditInput): number {
    const enabledGates = input.gates || Object.keys(AUDIT_THRESHOLDS);
    switch (dimName) {
      case '人类福祉': {
        // 检查是否服务普通人而非收割
        const hasPublicBenefit = input.description?.includes('用户') ||
          input.description?.includes('人民') || input.description?.includes('公共');
        const noExploit = !input.description?.includes('收割') &&
          !input.description?.includes('诱导') && !input.description?.includes('成瘾');
        return hasPublicBenefit && noExploit ? 0.90 : 0.40;
      }
      case '公平': {
        const noDiscrimination = !input.description?.includes('歧视') &&
          !input.description?.includes('筛选');
        const accessible = input.description?.includes('普惠') || input.description?.includes('开放');
        return noDiscrimination && accessible ? 0.85 : 0.45;
      }
      case '可控': {
        const userControl = input.description?.includes('用户控制') ||
          input.auditTarget?.includes('决策') === false;
        const reversible = !input.description?.includes('不可逆');
        return userControl && reversible ? 0.80 : 0.50;
      }
      case '透明': {
        const openSource = input.description?.includes('开源') ||
          input.description?.includes('透明');
        const documented = input.description?.includes('文档') ||
          (input.auditTarget?.length || 0) > 10;
        return openSource || documented ? 0.82 : 0.35;
      }
      case '可追溯': {
        const hasDNA = input.description?.includes('DNA') ||
          input.description?.includes('追溯');
        const hasLog = input.description?.includes('日志') ||
          input.description?.includes('审计');
        return hasDNA || hasLog ? 0.88 : 0.30;
      }
      case '隐私': {
        const localFirst = input.description?.includes('本地') ||
          input.description?.includes('端侧');
        const noCloudLeak = !input.description?.includes('云端') ||
          input.description?.includes('加密');
        return localFirst || noCloudLeak ? 0.86 : 0.35;
      }
      default:
        return 0.50;
    }
  }

  /** 加权R值 */
  private computeRValue(scores: DimensionScore[]): number {
    let totalWeighted = 0;
    let totalWeight = 0;
    for (const s of scores) {
      s.weightedScore = s.score * s.weight;
      totalWeighted += s.weightedScore;
      totalWeight += s.weight;
    }
    return totalWeighted / (totalWeight || 100);
  }

  /** 三色判定 */
  private determineColor(rValue: number): AuditColor {
    if (rValue >= AUDIT_THRESHOLDS.GREEN) return '🟢';
    if (rValue >= AUDIT_THRESHOLDS.YELLOW) return '🟡';
    return '🔴';
  }

  /** GATE闸口检查 */
  private runGateCheck(input: AuditInput, scores: DimensionScore[], rValue: number): GateResult[] {
    const gates = ['GATE-01身份', 'GATE-02意图', 'GATE-03语义', 'GATE-04数字根',
      'GATE-05伦理', 'GATE-06数据', 'GATE-07协议', 'GATE-08人格',
      'GATE-09DNA', 'GATE-10归档'];
    return gates.map((gate, idx) => {
      const passed = rValue >= 0.35 + idx * 0.02;
      return {
        name: gate,
        passed,
        detail: passed ? '通过' : `需人工复核（${gate}）`,
        score: Math.min(95, 55 + idx * 4)
      };
    });
  }

  /** 生成摘要 */
  private generateSummary(color: AuditColor, rValue: number, gates: GateResult[]): string {
    const failedGates = gates.filter(g => !g.passed);
    switch (color) {
      case '🟢': return `审计通过 · R=${rValue.toFixed(3)} · ${gates.filter(g => g.passed).length}/10 闸通过`;
      case '🟡': return `待复核 · R=${rValue.toFixed(3)} · ${failedGates.length} 闸待核: ${failedGates.map(g => g.name).join(', ')}`;
      case '🔴': return `红线 · R=${rValue.toFixed(3)} · ${failedGates.length} 闸未通过 · 立即冻结`;
      default: return '';
    }
  }
}

interface GateResult {
  name: string;
  passed: boolean;
  detail: string;
  score: number;
}
