/**
 * 🐉 龙魂·DNA生成器
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-DNAC-GENERATOR-v1.0
 * License: MulanPSL v2
 * 创建者: 诸葛鑫（UID9622）
 */
export class DNAGenerator {
  private static readonly HEX = '0123456789abcdef';

  static generate(module: string): string {
    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2, '0');
    const d = String(now.getDate()).padStart(2, '0');
    const rand = this.generateRandom(8);
    return `#龍芯⚡️${y}-${m}-${d}-${module}-HM-v1.0-${rand}`;
  }

  static generateRandom(length: number): string {
    let result = '';
    for (let i = 0; i < length; i++) {
      result += this.HEX[Math.floor(Math.random() * 16)];
    }
    return result;
  }
}
