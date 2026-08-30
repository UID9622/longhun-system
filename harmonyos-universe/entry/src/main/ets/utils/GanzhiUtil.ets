归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 🐉 龍魂 · 天干地支工具
 * 60甲子万年历·梅花易数起卦·完整四柱
 * License: MulanPSL v2
 * DNA: #龍芯⚡️2026-08-11-CAR-GANZHI-UTIL-v2.0-UID9622
 */
export class GanzhiUtil {
  private static TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
  private static DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
  private static HEXAGRAMS = ['乾卦', '坤卦', '震卦', '巽卦', '坎卦', '离卦', '艮卦', '兑卦'];
  private static SHI_CHEN = ['子时', '丑时', '寅时', '卯时', '辰时', '巳时', '午时', '未时', '申时', '酉时', '戌时', '亥时'];

  static getCurrentGanzhi(): string {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth() + 1;
    const day = now.getDate();
    const hour = now.getHours();

    const nian = this.getYearPillar(year);
    const yue = this.getMonthPillar(year, month);
    const ri = this.getDayPillar(year, month, day);
    const shi = this.getHourPillar(hour);

    return `${nian}·${yue}·${ri}·${shi}`;
  }

  static getYearPillar(year: number): string {
    const base = year - 4;
    return this.TIAN_GAN[base % 10] + this.DI_ZHI[base % 12];
  }

  static getMonthPillar(year: number, month: number): string {
    const monthZhiIdx = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0];
    const mz = monthZhiIdx[month - 1];
    const nianGan = this.TIAN_GAN.indexOf(this.getYearPillar(year)[0]);
    const yinYueGan = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0];
    const offset = (mz - 2 + 12) % 12;
    return this.TIAN_GAN[(yinYueGan[nianGan] + offset) % 10] + this.DI_ZHI[mz];
  }

  static getDayPillar(year: number, month: number, day: number): string {
    const yy = year % 100;
    let base = (yy + 7) * 5 + 15 + (yy + 19) / 4;
    base = Math.floor(base) % 60;
    const isLeap = (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
    const monthDays = [31, isLeap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
    let dayOfYear = day;
    for (let i = 0; i < month - 1; i++) { dayOfYear += monthDays[i]; }
    const seq = (base + dayOfYear) % 60;
    return this.TIAN_GAN[(seq - 1) % 10] + this.DI_ZHI[(seq - 1) % 12];
  }

  static getHourPillar(hour: number): string {
    return this.SHI_CHEN[Math.floor(((hour + 1) / 2) % 12)];
  }

  static getCurrentHexagram(): string {
    const now = new Date();
    const seed = (now.getFullYear() * 10000 + (now.getMonth() + 1) * 100 + now.getDate()) * now.getHours();
    return this.HEXAGRAMS[seed % 8];
  }

  static getHexagramSymbol(hexagram: string): string {
    const symbols: Record<string, string> = {
      '乾卦': '☰', '坤卦': '☷', '震卦': '☳', '巽卦': '☴',
      '坎卦': '☵', '离卦': '☲', '艮卦': '☶', '兑卦': '☱'
    };
    return symbols[hexagram] || '☰';
  }

  static getFullStamp(): string {
    const ganzhi = this.getCurrentGanzhi();
    const hexagram = this.getCurrentHexagram();
    const symbol = this.getHexagramSymbol(hexagram);
    return `🐉${ganzhi}·${symbol}${hexagram}`;
  }
}
