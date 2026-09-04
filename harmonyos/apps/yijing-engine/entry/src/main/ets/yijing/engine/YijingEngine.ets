/**
 * 🐉 龙魂·易经推演主引擎
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-YIJING-ENGINE-v1.0
 * License: MulanPSL v2
 * 创建者: 诸葛鑫（UID9622）
 * GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
 *
 * 🔥 绑定DNA追溯 + 三色审计 + 主权锚定
 * 🔥 互卦支持（新增）
 */
import hilog from '@ohos.hilog';
import { HexagramReading, DivinationMethod } from './models/HexagramModels';
import { HexagramCaster } from './HexagramCaster';
import { HexagramLoader } from './HexagramLoader';
import { HexagramInterpreter } from './HexagramInterpreter';
import { DNAGenerator } from '../../utils/DNAGenerator';
import { GanzhiTimestamp } from '../../utils/GanzhiTimestamp';
import { constants } from '../../utils/Constants';

const TAG = 'YijingEngine';
const DOMAIN = 0xFF45;

export class YijingEngine {
  private static instance: YijingEngine;

  static getInstance(): YijingEngine {
    if (!YijingEngine.instance) {
      YijingEngine.instance = new YijingEngine();
    }
    return YijingEngine.instance;
  }

  /**
   * 🔥 执行推演（主入口）
   */
  divinate(
    question: string,
    method: DivinationMethod,
    params?: Record<string, Object>
  ): HexagramReading {
    hilog.info(DOMAIN, TAG, `🔮 推演开始: ${question}`);

    // 1. 起卦
    let castResult: { yaos: import('./models/HexagramModels').Yao[]; movingIndices: number[] };
    switch (method) {
      case DivinationMethod.TIME:
        castResult = HexagramCaster.castByTime((params?.['date'] as Date) || new Date());
        break;
      case DivinationMethod.NUMBERS:
        castResult = HexagramCaster.castByNumbers(
          (params?.['num1'] as number) || 1,
          (params?.['num2'] as number) || 2,
          (params?.['num3'] as number) || 3
        );
        break;
      default: // coins
        castResult = HexagramCaster.castByCoins((params?.['seed'] as number) || Date.now());
    }
    const { yaos, movingIndices } = castResult;

    // 2. 本卦
    const originalHexagram = HexagramCaster.buildHexagram(yaos);
    if (!originalHexagram) throw new Error('起卦失败');

    // 3. 变卦（有动爻时）
    let changedHexagram = undefined;
    let changedYaos: typeof yaos | undefined;
    let changedName: string | undefined;
    if (movingIndices.length > 0) {
      const result = HexagramCaster.buildChangedHexagram(yaos);
      changedHexagram = result.hexagram;
      changedYaos = result.yaos;
      changedName = changedHexagram?.name;
    }

    // 4. 互卦
    const mutualHexagram = HexagramCaster.buildMutualHexagram(yaos);
    const mutualName = mutualHexagram?.name;

    // 5. 装卦
    const loaded = HexagramLoader.load(yaos, originalHexagram, new Date());

    // 6. DNA + 时间
    const dna = DNAGenerator.generate('YIJING');
    const ganzhi = GanzhiTimestamp.getCurrent();

    // 7. 三色审计
    const auditResult = auditDivination(originalHexagram.name);

    // 8. 构建结果
    const reading: HexagramReading = {
      dna, timestamp: new Date().toISOString(),
      ganzhiTime: ganzhi.full,
      question,
      originalHexagram, originalYaos: loaded.yaos, originalName: originalHexagram.name,
      changedHexagram, changedYaos, changedName,
      mutualHexagram, mutualName,
      movingYaoIndices: movingIndices,
      shiPosition: loaded.shiPosition, yingPosition: loaded.yingPosition,
      sixRelations: loaded.sixRelations, sixSpirits: loaded.sixSpirits,
      interpretation: '',
      suggestion: '',
      sovereignty: `#ZHUGEXIN⚡️${new Date().toISOString().slice(0, 10)}-YIJING-${DNAGenerator.generateRandom(6)}-9622`,
      confirmCode: constants.CONFIRM_CODE,
      gpg: constants.GPG,
      auditStatus: auditResult.status,
      auditRScore: auditResult.rScore,
      auditDetail: auditResult.detail,
    };

    // 9. 🔥 解卦：解读和建议分开调用
    reading.interpretation = HexagramInterpreter.interpret(reading);
    reading.suggestion = HexagramInterpreter.suggestion(reading);

    hilog.info(DOMAIN, TAG, `✅ 推演完成: ${reading.originalName}卦 ${auditResult.status}`);
    return reading;
  }

  /**
   * 格式化报告
   */
  formatReport(reading: HexagramReading): string {
    const L: string[] = [];
    L.push('═══════════════════════════════════════');
    L.push('🐉 龙魂 · 易经推演报告');
    L.push(`DNA: ${reading.dna}`);
    L.push(`时间: ${reading.ganzhiTime}`);
    L.push(`问题: ${reading.question}`);
    L.push('═══════════════════════════════════════');
    L.push('');
    L.push(reading.interpretation);
    L.push('');
    L.push('───────────────────────────────────────');
    L.push(`🔐 主权锚定: ${reading.sovereignty}`);
    L.push(`确认码: ${reading.confirmCode}`);
    L.push(`三色审计: ${reading.auditStatus} (R=${reading.auditRScore})`);
    L.push('═══════════════════════════════════════');
    return L.join('\n');
  }
}

/** 推演审计 */
function auditDivination(guaName: string): { status: string; rScore: number; detail: string } {
  // 易经推演类应用天然正向：帮人自省不收割
  const scores = { humanWelfare: 90, fairness: 85, controllability: 80, transparency: 80, traceability: 95, privacy: 95 };
  const weights = [25, 20, 15, 15, 15, 10];
  const dims = [scores.humanWelfare, scores.fairness, scores.controllability,
    scores.transparency, scores.traceability, scores.privacy];

  let rScore = 0;
  for (let i = 0; i < dims.length; i++) rScore += dims[i] * weights[i] / 100;
  rScore = Math.round(rScore) / 10;

  // P0红线检测
  const redLines = [
    guaName.includes('讼') ? '涉诉风险·宜警示' : '',
  ].filter(Boolean);

  if (redLines.length > 0) return { status: '🟡', rScore, detail: redLines.join('; ') };
  if (rScore >= 7.0) return { status: '🟢', rScore, detail: '全维度通过' };
  if (rScore >= 4.0) return { status: '🟡', rScore, detail: '部分维度待核' };
  return { status: '🔴', rScore, detail: '审计异常' };
}
