/**
 * 🐉 龍魂 · 天干地支工具 v3.0（Kimi审阅修正版 · 万年历口径）
 * DNA: #龍芯⚡️2026-08-10-GANZHI-UTIL-v3.0-UID9622（生成器回填）
 *
 * v2.0 → v3.0 修正：
 *   ① 弃用"蔡勒公式变体"（经实测：JDN拼装错误、连自身锚点1900甲戌都复现不了，
 *      2026-08-10算出己丑，与任何口径都对不上）
 *   ② 统一为 rizhu v3.0 锚点口径：1900-01-01 = 甲戌日（六十甲子索引10）顺推
 *      验证锚点：1949-10-01=甲子 · 2000-01-01=戊午 · 2026-08-10=丙辰
 *      任何人打开万年历App即可核对——信任闭环的前提是可外部验证
 *   ③ 月柱按节气月（每月7日近似分界），年柱公元年-4对60取模
 *
 * 与 core/rizhu.py v3.0 同一口径，两端输出必须一致（CI须跑交叉验证）。
 */

export class GanzhiUtil {
  private static readonly TIAN_GAN: string[] =
    ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
  private static readonly DI_ZHI: string[] =
    ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
  private static readonly HEXAGRAMS: string[] = [
    '乾卦', '坤卦', '屯卦', '蒙卦', '需卦', '讼卦', '师卦', '比卦',
    '小畜', '履卦', '泰卦', '否卦', '同人', '大有', '谦卦', '豫卦',
    '随卦', '蛊卦', '临卦', '观卦', '噬嗑', '贲卦', '剥卦', '复卦',
    '无妄', '大畜', '颐卦', '大过', '坎卦', '离卦', '咸卦', '恒卦',
    '遁卦', '大壮', '晋卦', '明夷', '家人', '睽卦', '蹇卦', '解卦',
    '损卦', '益卦', '夬卦', '姤卦', '萃卦', '升卦', '困卦', '井卦',
    '革卦', '鼎卦', '震卦', '艮卦', '渐卦', '归妹', '丰卦', '旅卦',
    '巽卦', '兑卦', '涣卦', '节卦', '中孚', '小过', '既济', '未济'
  ];
  private static readonly MS_PER_DAY: number = 86400000;
  private static readonly ANCHOR: number = Date.UTC(1900, 0, 1); // 1900-01-01

  /** 日柱干支：1900甲戌锚点顺推六十甲子（与公开万年历一致） */
  static getRiZhu(date: Date): string {
    const days = Math.floor((Date.UTC(date.getFullYear(), date.getMonth(), date.getDate())
      - this.ANCHOR) / this.MS_PER_DAY);
    const idx = ((10 + days) % 60 + 60) % 60;
    return this.TIAN_GAN[idx % 10] + this.DI_ZHI[idx % 12];
  }

  /** 年柱：公元年-4 对60取模（简化口径，与既有引擎一致） */
  static getNianZhu(date: Date): string {
    const idx = ((date.getFullYear() - 4) % 60 + 60) % 60;
    return this.TIAN_GAN[idx % 10] + this.DI_ZHI[idx % 12];
  }

  /** 月柱：五虎遁，寅月起正月，按节气月（每月7日近似分界） */
  static getYueZhu(date: Date): string {
    const YIN_MONTH_GAN: number[] = [2, 4, 6, 8, 0, 2, 4, 6, 8, 0];
    const yearGanIdx = ((date.getFullYear() - 4) % 10 + 10) % 10;
    const m = date.getMonth() + 1; // 1-12
    let sm = date.getDate() >= 7 ? m - 1 : m - 2; // 节气月：寅月≈公历2月
    if (sm < 1) sm += 12;
    const gan = this.TIAN_GAN[(YIN_MONTH_GAN[yearGanIdx] + sm - 1) % 10];
    const zhi = this.DI_ZHI[(2 + sm - 1) % 12];
    return gan + zhi;
  }

  /** 时柱：日干起时 */
  static getShiZhu(date: Date): string {
    const riGanIdx = this.TIAN_GAN.indexOf(this.getRiZhu(date).charAt(0));
    const hourZhiIdx = Math.floor(((date.getHours() + 1) % 24) / 2);
    const hourGanIdx = (riGanIdx % 5 * 2 + hourZhiIdx) % 10;
    return this.TIAN_GAN[hourGanIdx] + this.DI_ZHI[hourZhiIdx];
  }

  /** 四柱干支：年·月·日·时（唯一对外口径） */
  static getSiZhu(date: Date): string {
    return `${this.getNianZhu(date)}·${this.getYueZhu(date)}·${this.getRiZhu(date)}·${this.getShiZhu(date)}`;
  }

  /** 当前四柱 */
  static getCurrentGanzhi(): string {
    return this.getSiZhu(new Date());
  }

  /** 当前卦象（日序对64取模） */
  static getCurrentHexagram(): string {
    const now = new Date();
    const dayOfYear = Math.floor(
      (now.getTime() - new Date(now.getFullYear(), 0, 0).getTime()) / this.MS_PER_DAY);
    return this.HEXAGRAMS[dayOfYear % 64];
  }

  static getFullGanzhiHexagram(): string {
    return `${this.getCurrentGanzhi()}·${this.getCurrentHexagram()}`;
  }

  /** 自检：入库/构建前必跑，全绿才准合并 */
  static selfTest(): boolean {
    const d = (y: number, m: number, day: number, h: number = 12) => new Date(y, m - 1, day, h);
    console.assert(this.getRiZhu(d(1900, 1, 1)) === '甲戌', '锚点1失败');
    console.assert(this.getRiZhu(d(1949, 10, 1)) === '甲子', '锚点2失败(开国大典)');
    console.assert(this.getRiZhu(d(2000, 1, 1)) === '戊午', '锚点3失败');
    console.assert(this.getRiZhu(d(2026, 8, 10)) === '丙辰', '锚点4失败');
    console.assert(this.getSiZhu(d(2026, 8, 10, 12)) === '丙午·丙申·丙辰·甲午', '四柱锚点失败');
    return this.getRiZhu(d(2026, 8, 10)) === '丙辰'
      && this.getSiZhu(d(2026, 8, 10, 12)) === '丙午·丙申·丙辰·甲午';
  }
}
