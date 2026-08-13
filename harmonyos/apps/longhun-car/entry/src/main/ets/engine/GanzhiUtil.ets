/**
 * 🐉 龍魂 · 干支工具 GanzhiUtil.ets v3.0（ArkTS 移植）
 * ====================================================
 * DNA: #龍芯⚡️丙午·丙申·丁巳·恒卦-GANZHI-UTIL-v3.0-UID9622
 * License: MulanPSL v2
 *
 * 算法来源: bin/rizhu_core.py v3.0（Python 锚点顺推）
 * 锚点: 1900-01-01 = 甲戌日（六十甲子索引10）
 * 交叉验证: 1949-10-01 = 甲子日（开国大典）
 *
 * CI 中与 rizhu_core.py 交叉验证，两端输出必须一致。
 */

const TIAN_GAN: string[] = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
const DI_ZHI: string[] = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
const YIN_MONTH_GAN: number[] = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0];  // 五虎遁
const ANCHOR_TS = Date.UTC(1900, 0, 1);  // 1900-01-01 UTC 毫秒
const ANCHOR_IDX = 10;                    // 1900-01-01 = 甲戌(索引10)
const MS_PER_DAY = 86400000;

export class GanzhiUtil {
  /** 日柱 v3.0 —— 锚点顺推，与公开万年历一致 */
  static getRizhu(date: Date): string {
    const days = Math.floor((date.getTime() - ANCHOR_TS) / MS_PER_DAY);
    const idx = ((ANCHOR_IDX + days) % 60 + 60) % 60;  // 处理负值
    return TIAN_GAN[idx % 10] + DI_ZHI[idx % 12];
  }

  /** 年柱：公元年-4 对60取模 */
  static getNianzhu(date: Date): string {
    const idx = ((date.getFullYear() - 4) % 60 + 60) % 60;
    return TIAN_GAN[idx % 10] + DI_ZHI[idx % 12];
  }

  /** 节气月近似（每月7日分界，±1天） */
  private static solarTermMonth(date: Date): number {
    const m = date.getMonth();     // 0-11
    const d = date.getDate();      // 1-31
    const sm = d >= 7 ? m : m - 1;
    return sm >= 0 ? sm + 1 : sm + 13;  // 返回 1-12
  }

  /** 月柱：五虎遁，寅月起正月 */
  static getYuezhu(date: Date): string {
    const yinGan = YIN_MONTH_GAN[(date.getFullYear() - 4) % 10];
    const sm = GanzhiUtil.solarTermMonth(date);
    return TIAN_GAN[(yinGan + sm - 1) % 10] + DI_ZHI[(2 + sm - 1) % 12];
  }

  /** 时柱：日干起时（甲己还加甲） */
  static getShizhu(date: Date): string {
    const riGan = TIAN_GAN.indexOf(GanzhiUtil.getRizhu(date)[0]);
    const hz = ((date.getHours() + 1) >> 1) % 12;
    return TIAN_GAN[(riGan % 5 * 2 + hz) % 10] + DI_ZHI[hz];
  }

  /** 四柱：年·月·日·时，唯一对外口径 */
  static sizhuGanzhi(date: Date): string {
    return `${GanzhiUtil.getNianzhu(date)}·${GanzhiUtil.getYuezhu(date)}·${GanzhiUtil.getRizhu(date)}·${GanzhiUtil.getShizhu(date)}`;
  }

  /** DNA 戳生成 */
  static dnaStamp(date: Date, module: string = '', action: string = ''): string {
    const sz = GanzhiUtil.sizhuGanzhi(date);
    const tail = module ? `-${module}-${action}` : '';
    return `#龍芯⚡️${sz}${tail}`;
  }

  // ===== 自检（CI 中跑交叉验证） =====
  static selfTest(): boolean {
    // 锚点1: 1900-01-01 = 甲戌
    if (GanzhiUtil.getRizhu(new Date('1900-01-01')) !== '甲戌') return false;
    // 锚点2: 1949-10-01 = 甲子
    if (GanzhiUtil.getRizhu(new Date('1949-10-01')) !== '甲子') return false;
    // 锚点3: 2026-08-10 = 丙辰
    if (GanzhiUtil.getRizhu(new Date('2026-08-10')) !== '丙辰') return false;
    // 月柱: 2026-08-10 = 丙申
    if (GanzhiUtil.getYuezhu(new Date('2026-08-10')) !== '丙申') return false;
    return true;
  }
}
