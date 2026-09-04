/**
 * 龙魂·干支时间戳引擎 — HarmonyOS 原生
 * 天干地支·梅花易数64卦起卦
 * DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-TIMESTAMP
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 * 创建者: 诸葛鑫（UID9622）
 */
export class TimeStampEngine {
  private static TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
  private static DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
  private static SHI_CHEN = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
  private static GUA_64: string[] = [
    '䷀乾', '䷁坤', '䷂屯', '䷃蒙', '䷄需', '䷅讼', '䷆师', '䷇比',
    '䷈小畜', '䷉履', '䷊泰', '䷋否', '䷌同人', '䷍大有', '䷎谦', '䷏豫',
    '䷐随', '䷑蛊', '䷒临', '䷓观', '䷔噬嗑', '䷕贲', '䷖剥', '䷗复',
    '䷘无妄', '䷙大畜', '䷚颐', '䷛大过', '䷜坎', '䷝离', '䷞咸', '䷟恒',
    '䷠遁', '䷡大壮', '䷢晋', '䷣明夷', '䷤家人', '䷥睽', '䷦蹇', '䷧解',
    '䷨损', '䷩益', '䷪夬', '䷫姤', '䷬萃', '䷭升', '䷮困', '䷯井',
    '䷰革', '䷱鼎', '䷲震', '䷳艮', '䷴渐', '䷵归妹', '䷶丰', '䷷旅',
    '䷸巽', '䷹兑', '䷺涣', '䷻节', '䷼中孚', '䷽小过', '䷾既济', '䷿未济'
  ];

  now(): string { return this.format(new Date()); }
  getCurrentGua(): string {
    const n = new Date();
    const up = (n.getFullYear() + n.getMonth() + 1) % 8 || 8;
    const lo = (n.getMonth() + 1 + n.getDate()) % 8 || 8;
    return TimeStampEngine.GUA_64[((up - 1) * 8 + (lo - 1)) % 64];
  }

  format(d: Date): string {
    const y = d.getFullYear(), m = d.getMonth() + 1, day = d.getDate(), h = d.getHours();
    const yG = TimeStampEngine.TIAN_GAN[(y - 4) % 10];
    const yZ = TimeStampEngine.DI_ZHI[(y - 4) % 12];
    const mG = TimeStampEngine.TIAN_GAN[((y - 4) % 10 * 2 + m) % 10];
    const mZ = TimeStampEngine.DI_ZHI[(m + 1) % 12];
    const dBase = Math.floor((y - 1900) * 365.25) + (m - 1) * 30 + day;
    const dG = TimeStampEngine.TIAN_GAN[(dBase + 9) % 10];
    const dZ = TimeStampEngine.DI_ZHI[(dBase + 5) % 12];
    const sc = TimeStampEngine.SHI_CHEN[Math.floor((h + 1) / 2) % 12];
    return `${yG}${yZ}·${mG}${mZ}·${dG}${dZ}·${sc}时`;
  }
}
