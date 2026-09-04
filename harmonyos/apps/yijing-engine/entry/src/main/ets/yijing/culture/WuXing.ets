/**
 * 🐉 龙魂·五行生克
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-WUXING-v1.0
 * License: MulanPSL v2
 * 创建者: 诸葛鑫（UID9622）
 */
export class WuXing {
  private static readonly SHENG: Record<string, string> = {
    '金': '水', '水': '木', '木': '火', '火': '土', '土': '金',
  };
  private static readonly KE: Record<string, string> = {
    '金': '木', '木': '土', '土': '水', '水': '火', '火': '金',
  };

  /** 获取生克关系（六亲）— 以 palaceWuXing 为"我" */
  static getRelation(palaceWuXing: string, yaoWuXing: string): string {
    if (palaceWuXing === yaoWuXing) return '兄弟';
    if (this.SHENG[palaceWuXing] === yaoWuXing) return '子孙';  // 我生
    if (this.SHENG[yaoWuXing] === palaceWuXing) return '父母';  // 生我
    if (this.KE[palaceWuXing] === yaoWuXing) return '妻财';    // 我克
    if (this.KE[yaoWuXing] === palaceWuXing) return '官鬼';    // 克我
    return '';
  }

  /** 是否相生 */
  static isSheng(a: string, b: string): boolean {
    return this.SHENG[a] === b;
  }

  /** 是否相克 */
  static isKe(a: string, b: string): boolean {
    return this.KE[a] === b;
  }
}
