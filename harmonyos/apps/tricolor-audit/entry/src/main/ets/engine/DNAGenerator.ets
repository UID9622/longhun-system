/**
 * 龙魂·DNA生成器 — HarmonyOS 原生
 * v∞格式: #龍芯⚡️干支四柱·卦-模块-动作-哈希8
 * DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-DNA-GENERATOR
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 */
import { GANZHI, SOVEREIGNTY } from '../models/Constants';

export class DNAGenerator {
  private static readonly TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
  private static readonly DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
  private static readonly SHI_CHEN = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
  private static readonly GUA_64: string[] = [
    '䷀乾', '䷁坤', '䷂屯', '䷃蒙', '䷄需', '䷅讼', '䷆师', '䷇比',
    '䷈小畜', '䷉履', '䷊泰', '䷋否', '䷌同人', '䷍大有', '䷎谦', '䷏豫',
    '䷐随', '䷑蛊', '䷒临', '䷓观', '䷔噬嗑', '䷕贲', '䷖剥', '䷗复',
    '䷘无妄', '䷙大畜', '䷚颐', '䷛大过', '䷜坎', '䷝离', '䷞咸', '䷟恒',
    '䷠遁', '䷡大壮', '䷢晋', '䷣明夷', '䷤家人', '䷥睽', '䷦蹇', '䷧解',
    '䷨损', '䷩益', '䷪夬', '䷫姤', '䷬萃', '䷭升', '䷮困', '䷯井',
    '䷰革', '䷱鼎', '䷲震', '䷳艮', '䷴渐', '䷵归妹', '䷶丰', '䷷旅',
    '䷸巽', '䷹兑', '䷺涣', '䷻节', '䷼中孚', '䷽小过', '䷾既济', '䷿未济'
  ];

  /** 生成DNA */
  generate(module: string, action: string): string {
    const now = new Date();
    const ganzhi = this.formatGanzhi(now);
    const gua = this.getCurrentGua(now);
    const hash = this.generateHash(8);
    return `#龍芯⚡️${ganzhi}·${gua}-${module}-${action}-${hash}`;
  }

  /** 验证DNA格式 */
  validate(dna: string): boolean {
    if (!dna || !dna.startsWith('#龍芯⚡️')) return false;
    const parts = dna.replace('#龍芯⚡️', '').split('-');
    return parts.length >= 4 && parts[parts.length - 1].length === 8;
  }

  /** 从DNA提取模块名 */
  extractModule(dna: string): string | null {
    if (!this.validate(dna)) return null;
    const parts = dna.replace('#龍芯⚡️', '').split('-');
    return parts[parts.length - 3] || null;
  }

  /** 从DNA提取动作 */
  extractAction(dna: string): string | null {
    if (!this.validate(dna)) return null;
    const parts = dna.replace('#龍芯⚡️', '').split('-');
    return parts[parts.length - 2] || null;
  }

  /** 干支四柱格式化 */
  private formatGanzhi(date: Date): string {
    const y = date.getFullYear();
    const m = date.getMonth() + 1;
    const d = date.getDate();
    const h = date.getHours();

    const yG = DNAGenerator.TIAN_GAN[(y - 4) % 10];
    const yZ = DNAGenerator.DI_ZHI[(y - 4) % 12];
    const mG = DNAGenerator.TIAN_GAN[((y - 4) % 10 * 2 + m) % 10];
    const mZ = DNAGenerator.DI_ZHI[(m + 1) % 12];
    const dG = DNAGenerator.TIAN_GAN[(Math.floor((y - 1900) * 365.25) + (m - 1) * 30 + d + 9) % 10];
    const dZ = DNAGenerator.DI_ZHI[(Math.floor((y - 1900) * 365.25) + (m - 1) * 30 + d + 5) % 12];
    const scIdx = Math.floor((h + 1) / 2) % 12;
    const sc = DNAGenerator.SHI_CHEN[scIdx];

    return `${yG}${yZ}·${mG}${mZ}·${dG}${dZ}·${sc}时`;
  }

  /** 梅花易数起卦 */
  private getCurrentGua(date: Date): string {
    const y = date.getFullYear();
    const m = date.getMonth() + 1;
    const d = date.getDate();
    const upper = (y + m) % 8 || 8;
    const lower = (m + d) % 8 || 8;
    const idx = (upper - 1) * 8 + (lower - 1);
    return DNAGenerator.GUA_64[idx % 64];
  }

  /** 生成随机哈希 */
  private generateHash(length: number): string {
    const chars = '0123456789abcdef';
    let result = '';
    for (let i = 0; i < length; i++) {
      result += chars[Math.floor(Math.random() * chars.length)];
    }
    return result;
  }
}
