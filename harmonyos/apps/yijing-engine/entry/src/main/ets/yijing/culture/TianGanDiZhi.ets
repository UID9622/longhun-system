/**
 * 🐉 龙魂·天干地支计算器
 * DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-TIANGAN-DIZHI-v1.0
 * License: MulanPSL v2
 * 创建者: 诸葛鑫（UID9622）
 */
export class TianGanDiZhi {
  static readonly GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
  static readonly ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
  static readonly SHICHEN = ['子时', '丑时', '寅时', '卯时', '辰时', '巳时',
    '午时', '未时', '申时', '酉时', '戌时', '亥时'];

  /** 获取日天干 */
  static getDayGan(date: Date): string {
    const base = new Date(1984, 1, 2); // 甲子日
    const diff = Math.floor((date.getTime() - base.getTime()) / 86400000);
    return this.GAN[((diff % 10) + 10) % 10];
  }

  /** 获取日地支 */
  static getDayZhi(date: Date): string {
    const base = new Date(1984, 1, 2);
    const diff = Math.floor((date.getTime() - base.getTime()) / 86400000);
    return this.ZHI[((diff % 12) + 12) % 12];
  }

  /** 时辰地支 */
  static getShichenZhi(hour: number): string {
    return this.ZHI[Math.floor(((hour + 1) % 24) / 2) % 12];
  }

  /** 获取完整四柱 */
  static getFourPillars(date: Date): { nian: string; yue: string; ri: string; shi: string } {
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const hour = date.getHours();

    // 年柱（简化：公元年份-4后取模）
    const yearGanIdx = ((year - 4) % 10 + 10) % 10;
    const yearZhiIdx = ((year - 4) % 12 + 12) % 12;
    const nian = this.GAN[yearGanIdx] + this.ZHI[yearZhiIdx];

    // 月柱（年天干决定月干起始）
    const monthGanBase = (yearGanIdx % 5) * 2;
    const monthGanIdx = (monthGanBase + month - 1) % 10;
    const monthZhiIdx = (month + 1) % 12;
    const yue = this.GAN[monthGanIdx] + this.ZHI[monthZhiIdx];

    // 日柱
    const ri = this.getDayGan(date) + this.getDayZhi(date);

    // 时柱
    const hourZhiIdx = Math.floor(((hour + 1) % 24) / 2) % 12;
    const dayGanIdx = this.GAN.indexOf(this.getDayGan(date));
    const hourGanBase = (dayGanIdx % 5) * 2;
    const hourGanIdx = (hourGanBase + hourZhiIdx) % 10;
    const shi = this.GAN[hourGanIdx] + this.ZHI[hourZhiIdx];

    return { nian, yue, ri, shi };
  }

  /** 获取当前干支四柱字符串 */
  static getFullGanzhi(date: Date = new Date()): string {
    const p = this.getFourPillars(date);
    return `${p.nian}·${p.yue}·${p.ri}·${p.shi}`;
  }
}
