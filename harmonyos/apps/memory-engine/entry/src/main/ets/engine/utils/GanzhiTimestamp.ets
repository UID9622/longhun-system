/**
 * 龙魂·干支时间戳
 * License: MulanPSL v2
 */
export class GanzhiTimestamp {
  private static TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
  private static DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
  private static SHI_CHEN = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

  static now(): string { return this.format(new Date()); }
  static format(d: Date): string {
    const y = d.getFullYear(), m = d.getMonth() + 1, day = d.getDate(), h = d.getHours();
    const yG = GanzhiTimestamp.TIAN_GAN[(y - 4) % 10];
    const yZ = GanzhiTimestamp.DI_ZHI[(y - 4) % 12];
    const mG = GanzhiTimestamp.TIAN_GAN[((y - 4) % 10 * 2 + m) % 10];
    const mZ = GanzhiTimestamp.DI_ZHI[(m + 1) % 12];
    return `${yG}${yZ}·${mG}${mZ}·${(y - 1900) % 10}·${h.toString().padStart(2, '0')}时`;
  }
}
