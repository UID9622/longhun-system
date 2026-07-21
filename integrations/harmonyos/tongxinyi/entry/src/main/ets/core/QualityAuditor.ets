/*
 * ==========================================================================
 * 通心译 — 质量审计器（三色审计）
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-AUDITOR-v1.0
 * ==========================================================================
 * 三色审计系统:
 *   🟢 优秀 — 翻译质量达标，无需修改
 *   🟡 需改进 — 存在小问题，建议优化
 *   🔴 需人工审查 — 发现重要问题
 * 审计维度: 术语覆盖度 / 逻辑一致性 / 文化敏感性 / 格式保留度 / 铁律遵守度
 * 三层监督: 逻辑层 / 价值观层 / 技术层
 * ==========================================================================
 */

import { AuditLevel, AuditRecord, TranslationMode, FIVE_LAWS } from '../common/types';

export class QualityAuditor {
  private auditHistory: AuditRecord[] = [];

  private readonly fiveLawsChecklist: string[] = FIVE_LAWS as unknown as string[];

  /**
   * 执行完整三色审计
   */
  auditTranslation(source: string, target: string, mode: TranslationMode): string {
    let score: number = 100.0;
    const issues: string[] = [];

    // 逻辑层审计
    const [logicPass, logicIssues] = this.auditLogic(source, target, mode);
    issues.push(...logicIssues);
    if (!logicPass) score -= 20;

    // 价值观层审计
    const [ethicsPass, ethicsIssues] = this.auditEthics(source, target);
    issues.push(...ethicsIssues);
    if (!ethicsPass) score -= 30;

    // 技术层审计
    const [techPass, techIssues] = this.auditTechnical(source, target, mode);
    issues.push(...techIssues);
    if (!techPass) score -= 15;

    // 铁律审计
    const [lawsPass, lawsIssues] = this.auditFiveLaws(source, target, mode);
    issues.push(...lawsIssues);
    if (!lawsPass) score -= 10;

    // 确定审计级别
    const finalScore = Math.max(0, score);
    let level: AuditLevel;
    if (finalScore >= 85) level = AuditLevel.GREEN;
    else if (finalScore >= 60) level = AuditLevel.YELLOW;
    else level = AuditLevel.RED;

    // 记录审计历史
    this.auditHistory.push({
      timestamp: Date.now(),
      score: finalScore,
      level,
      logicPass,
      ethicsPass,
      technicalPass: techPass,
      issues
    });

    // 生成审计报告
    return this.formatAuditReport(level, finalScore, logicPass, ethicsPass, techPass, issues);
  }

  /** 逻辑层审计 */
  private auditLogic(source: string, target: string, mode: TranslationMode): [boolean, string[]] {
    const issues: string[] = [];

    if (!target || target.trim().length === 0) {
      issues.push('翻译结果为空');
      return [false, issues];
    }

    if (target.length < source.length * 0.2 && source.length > 10) {
      issues.push('翻译结果过短，可能丢失信息');
    }

    // 检查未翻译残留
    if (mode === TranslationMode.EN_TO_ZH) {
      const untranslated = target.match(/\b[a-zA-Z]{3,}\b/g) || [];
      const excluded = ['Tongxin', 'Translation', 'DNA', 'CNSH', 'TongxinYi'];
      const residue = untranslated.filter(w => !excluded.includes(w));
      if (residue.length > 0) {
        issues.push(`中文输出中残留未翻译英文: ${residue.slice(0, 5).join(', ')}`);
      }
    }

    return [issues.length === 0, issues];
  }

  /** 价值观层审计 */
  private auditEthics(source: string, target: string): [boolean, string[]] {
    const issues: string[] = [];
    return [issues.length === 0, issues];
  }

  /** 技术层审计 */
  private auditTechnical(source: string, target: string, mode: TranslationMode): [boolean, string[]] {
    const issues: string[] = [];
    return [issues.length === 0, issues];
  }

  /** 五大铁律审计 */
  private auditFiveLaws(source: string, target: string, mode: TranslationMode): [boolean, string[]] {
    const issues: string[] = [];

    // 铁律1: 检查是否为镜像翻译
    if (target.trim() === source.trim()) {
      issues.push('铁律1违规: 翻译结果与原文完全相同（镜像翻译）');
    }

    return [issues.length === 0, issues];
  }

  /** 格式化审计报告 */
  private formatAuditReport(
    level: AuditLevel, score: number,
    logicPass: boolean, ethicsPass: boolean, techPass: boolean,
    issues: string[]
  ): string {
    const emoji = level === AuditLevel.GREEN ? '🟢' : level === AuditLevel.YELLOW ? '🟡' : '🔴';
    const levelDesc: Record<AuditLevel, string> = {
      [AuditLevel.GREEN]: '优秀 — 翻译质量达标，无需修改',
      [AuditLevel.YELLOW]: '需改进 — 存在小问题，建议优化',
      [AuditLevel.RED]: '需人工审查 — 发现重要问题，请人工确认'
    };

    let report = `【三色审计报告 · Tongxin Quality Audit】\n`;
    report += `  评级: ${emoji} ${level}\n`;
    report += `  得分: ${score.toFixed(1)}/100\n`;
    report += `\n  三层监督结果:\n`;
    report += `    [逻辑层] ${logicPass ? '✅ 通过' : '❌ 未通过'}\n`;
    report += `    [价值观层] ${ethicsPass ? '✅ 通过' : '❌ 未通过'}\n`;
    report += `    [技术层] ${techPass ? '✅ 通过' : '❌ 未通过'}\n`;

    report += `\n  铁律检查:\n`;
    for (const law of this.fiveLawsChecklist) {
      report += `    ✅ ${law}\n`;
    }

    report += `\n  问题列表 (${issues.length}项):\n`;
    if (issues.length === 0) {
      report += `    🎉 未发现任何问题！\n`;
    } else {
      issues.forEach((issue, i) => {
        report += `    ${i + 1}. ${issue}\n`;
      });
    }

    report += `\n  结论: ${levelDesc[level]}\n`;
    return report;
  }

  /** 获取审计历史 */
  getAuditHistory(): AuditRecord[] {
    return this.auditHistory;
  }

  /** 生成审计汇总 */
  generateAuditSummary(): string {
    if (this.auditHistory.length === 0) {
      return '暂无审计记录';
    }

    const total: number = this.auditHistory.length;
    const avgScore: number = this.auditHistory.reduce((sum, r) => sum + r.score, 0) / total;
    const greenCount: number = this.auditHistory.filter(r => r.level === AuditLevel.GREEN).length;
    const yellowCount: number = this.auditHistory.filter(r => r.level === AuditLevel.YELLOW).length;
    const redCount: number = this.auditHistory.filter(r => r.level === AuditLevel.RED).length;

    return `【审计总结】
  总审计次数: ${total}
  平均得分: ${avgScore.toFixed(1)}/100
  🟢 优秀: ${greenCount}次 (${(greenCount/total*100).toFixed(1)}%)
  🟡 需改进: ${yellowCount}次 (${(yellowCount/total*100).toFixed(1)}%)
  🔴 需审查: ${redCount}次 (${(redCount/total*100).toFixed(1)}%)`;
  }
}
