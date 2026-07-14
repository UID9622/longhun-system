/*
 * ==========================================================================
 * 通心译 — 文化适配器
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-CULTURAL-v1.0
 * ==========================================================================
 * 职能: 主权字保护 / CNSH命名规范检查 / 文化敏感度筛查 / 龍魂标记保护
 * 主权字保护规则:
 *   1. "龍"为繁体主权字·用于正式/神圣语境
 *   2. "龍"为简体常用字·用于日常语境
 *   3. 龍魂体系标记中的"龍"不可替换
 *   4. 用户可自定义主权字偏好
 * ==========================================================================
 */

import { DRAGON_SOUL_MARKS } from '../common/types';

export class CulturalAdapter {
  private sovereignChars: Record<string, { variant: string; protectionLevel: string; context: string }> = {
    '龍': { variant: '龍', protectionLevel: 'maximum', context: 'formal/sacred' },
    '国': { variant: '国', protectionLevel: 'high', context: 'formal/sacred' },
    '华': { variant: '华', protectionLevel: 'high', context: 'formal/sacred' }
  };

  private userPreference: 'auto' | 'traditional' | 'simplified' = 'auto';

  /** 适配为中文语境 */
  adaptToChinese(text: string): string {
    text = this.protectSovereignChars(text);
    text = this.applyChineseCulturalNuances(text);
    return text;
  }

  /** 适配为英文语境 */
  adaptToEnglish(text: string): string {
    return this.protectSovereignChars(text);
  }

  /** 主权字保护 */
  private protectSovereignChars(text: string): string {
    // 龍魂DNA标记中的主权字不可动
    if (text.includes(DRAGON_SOUL_MARKS.DNA) ||
        text.includes(DRAGON_SOUL_MARKS.SEAL)) {
      return text;
    }

    if (this.userPreference === 'traditional') {
      for (const [sacred, info] of Object.entries(this.sovereignChars)) {
        text = text.split(info.variant).join(sacred);
      }
    } else if (this.userPreference === 'simplified') {
      for (const [sacred, info] of Object.entries(this.sovereignChars)) {
        text = text.split(sacred).join(info.variant);
      }
    }
    return text;
  }

  /** 应用中文文化细节 */
  private applyChineseCulturalNuances(text: string): string {
    const replacements: [string, string][] = [
      [', ', '，'],
      ['. ', '。'],
      ['! ', '！'],
      ['? ', '？'],
      [': ', '：'],
      ['; ', '；']
    ];
    for (const [en, cn] of replacements) {
      text = text.split(en).join(cn);
    }
    return text;
  }

  /** 检查CNSH命名规范 */
  checkCNSHNaming(name: string): string {
    const rules: [RegExp, string][] = [
      [/^[a-z][a-zA-Z0-9_]*$/, 'CNSH小驼峰: 变量/函数命名'],
      [/^[A-Z][a-zA-Z0-9_]*$/, 'CNSH大驼峰: 类名命名'],
      [/^[A-Z][A-Z0-9_]*$/, 'CNSH全大写: 常量命名'],
      [/^[a-z][a-z0-9-]*$/, 'CNSH烤串式: 模块/包命名']
    ];

    for (const [pattern, desc] of rules) {
      if (pattern.test(name)) {
        return `✅ 符合${desc}`;
      }
    }
    return '⚠️ 不符合CNSH命名规范，建议使用: 小驼峰/大驼峰/全大写/烤串式';
  }

  /** 筛查敏感内容 */
  screenSensitiveContent(text: string): { passed: boolean; issues: string[] } {
    const issues: string[] = [];
    const patterns: [RegExp, string][] = [];

    for (const [pattern, desc] of patterns) {
      if (pattern.test(text)) {
        issues.push(`发现敏感内容: ${desc}`);
      }
    }
    return { passed: issues.length === 0, issues };
  }

  /** 设置主权字偏好 */
  setSovereignPreference(preference: 'auto' | 'traditional' | 'simplified'): void {
    this.userPreference = preference;
  }

  /** 生成主权字保护报告 */
  getSovereignReport(): string {
    let report = '【主权字保护状态】\n';
    for (const [char, info] of Object.entries(this.sovereignChars)) {
      report += `  ${char} ↔ ${info.variant} (保护级别: ${info.protectionLevel})\n`;
    }
    report += `  当前模式: ${this.userPreference}\n`;
    return report;
  }
}
