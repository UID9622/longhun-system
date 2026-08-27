// 🐉 DNA追溯码生成器
// DNA: #龍芯⚡️2026-08-06-DNA-GENERATOR-V2.0-UID9622
// License: MulanPSL v2

import hilog from '@ohos.hilog';

const TAG: string = 'DNAGenerator';
const DOMAIN: number = 0xFF04;

/**
 * DNA追溯码生成器
 * 格式: #前缀⚡️YYYY-MM-DD-类型-随机码-UID9622
 */
export class DNAGenerator {
  private static readonly UID: string = '9622';
  private static readonly CHARS: string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';

  /**
   * 生成DNA追溯码
   */
  static generate(prefix: string = '龍芯⚡️', type: string = 'GEN'): string {
    const now = new Date();
    const pad = (n: number): string => String(n).padStart(2, '0');
    const dateStr = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
    const random = this.generateRandom(8);
    return `#${prefix}${dateStr}-${type}-${random}-${this.UID}`;
  }

  private static generateRandom(length: number): string {
    let result = '';
    for (let i = 0; i < length; i++) {
      result += this.CHARS.charAt(Math.floor(Math.random() * this.CHARS.length));
    }
    return result;
  }

  /**
   * 验证DNA格式
   */
  static validate(dna: string): boolean {
    if (!dna || dna.length < 20) return false;
    if (!dna.includes('⚡️')) return false;
    if (!dna.includes(this.UID)) return false;

    const parts = dna.replace('#', '').split('⚡️');
    if (parts.length !== 2) return false;

    const segments = parts[1].split('-');
    if (segments.length < 4) return false;

    const datePattern = /^\d{4}-\d{2}-\d{2}$/;
    return datePattern.test(segments[0]);
  }

  static extractType(dna: string): string {
    if (!this.validate(dna)) return '';
    const parts = dna.replace('#', '').split('⚡️');
    return parts[1].split('-')[1] || '';
  }

  static extractDate(dna: string): string {
    if (!this.validate(dna)) return '';
    const parts = dna.replace('#', '').split('⚡️');
    return parts[1].split('-')[0] || '';
  }
}
