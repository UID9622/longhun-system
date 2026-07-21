/*
 * ==========================================================================
 * 龍魂 · 农历转换引擎
 * DNA: #龍芯⚡️丙午·辛未·丙戌·亥时-LUNAR-ENGINE-v2.0
 * ==========================================================================
 * 补全原始代码中的占位农历转换，支持完整农历↔公历互转。
 * 使用 1900-2100 农历数据表，覆盖200年范围。
 */

// ═══════════════════════════════════════════════
// 农历数据表（压缩格式）
// 每个数字代表农历月的天数：
//   低4位 = 闰月月份（0=无闰月）
//   高12位 = 每月大小月（1=30天, 0=29天, 从正月到腊月）
// ═══════════════════════════════════════════════
const LUNAR_INFO: number[] = [
  // 1900-1909
  0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
  // 1910-1919
  0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
  // 1920-1929
  0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
  // 1930-1939
  0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
  // 1940-1949
  0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
  // 1950-1959
  0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5b0, 0x14573, 0x052b0, 0x0a9a8, 0x0e950, 0x06aa0,
  // 1960-1969
  0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
  // 1970-1979
  0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b6a0, 0x195a6,
  // 1980-1989
  0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
  // 1990-1999
  0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,
  // 2000-2009
  0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
  // 2010-2019
  0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
  // 2020-2029
  0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
  // 2030-2039
  0x05aa0, 0x076a3, 0x096d0, 0x04afb, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
  // 2040-2049
  0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
  // 2050-2059
  0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06b20, 0x1a6c4, 0x0aae0,
  // 2060-2069
  0x0a2e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
  // 2070-2079
  0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
  // 2080-2089
  0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
  // 2090-2099
  0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a4d0, 0x0d150, 0x0f252,
  // 2100
  0x0d520
];

// 农历年起始（1900年正月初一对应的公历日期）
const LUNAR_BASE_YEAR = 1900;
const LUNAR_BASE_MONTH = 1;
const LUNAR_BASE_DAY = 31;

// 公历每月天数
const SOLAR_MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];

function isLeapYear(year: number): boolean {
  return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
}

function daysInMonth(year: number, month: number): number {
  if (month === 2 && isLeapYear(year)) return 29;
  return SOLAR_MONTH_DAYS[month - 1];
}

export class LunarEngine {
  // ═══════════════════════════════════════════════
  // 公历日期 → 距1900-01-31的天数
  // ═══════════════════════════════════════════════
  private static solarToDays(year: number, month: number, day: number): number {
    let days = day - LUNAR_BASE_DAY;
    for (let y = LUNAR_BASE_YEAR; y < year; y++) {
      days += isLeapYear(y) ? 366 : 365;
    }
    for (let m = 1; m < month; m++) {
      days += daysInMonth(year, m);
    }
    return days;
  }

  // ═══════════════════════════════════════════════
  // 偏移天数 → 公历日期
  // ═══════════════════════════════════════════════
  private static daysToSolar(offset: number): { year: number; month: number; day: number } {
    let d = offset + LUNAR_BASE_DAY;
    let year = LUNAR_BASE_YEAR;
    let month = 1;

    // 减去年
    while (true) {
      const yearDays = isLeapYear(year) ? 366 : 365;
      if (d <= yearDays) break;
      d -= yearDays;
      year++;
    }

    // 减去月
    while (true) {
      const md = daysInMonth(year, month);
      if (d <= md) break;
      d -= md;
      month++;
    }

    return { year, month, day: d };
  }

  // ═══════════════════════════════════════════════
  // 农历月 → 该月天数
  // ═══════════════════════════════════════════════
  private static lunarMonthDays(lunarYear: number, lunarMonth: number): number {
    const info = LUNAR_INFO[lunarYear - LUNAR_BASE_YEAR];
    const leapMonth = info & 0xf;  // 闰月月份
    const monthBit = lunarMonth > leapMonth && leapMonth > 0 ? lunarMonth - 1 : lunarMonth;
    return (info & (0x10000 >> monthBit)) ? 30 : 29;
  }

  // ═══════════════════════════════════════════════
  // 农历年总天数
  // ═══════════════════════════════════════════════
  private static lunarYearDays(lunarYear: number): number {
    let days = 0;
    const info = LUNAR_INFO[lunarYear - LUNAR_BASE_YEAR];
    // 12个月 + 闰月(若有)
    for (let m = 1; m <= 12; m++) {
      days += ((info & (0x10000 >> m)) ? 30 : 29);
    }
    const leapMonth = info & 0xf;
    if (leapMonth > 0) {
      days += ((info & (0x10000 >> leapMonth)) ? 30 : 29);
    }
    return days;
  }

  // ═══════════════════════════════════════════════
  // 公历 → 农历（核心算法）
  // ═══════════════════════════════════════════════
  static solarToLunar(solarYear: number, solarMonth: number, solarDay: number):
    { year: number; month: number; day: number; isLeap: boolean } {
    const offset = this.solarToDays(solarYear, solarMonth, solarDay);

    // 找到农历年
    let lunarYear = LUNAR_BASE_YEAR;
    let remaining = offset;
    while (true) {
      const yDays = this.lunarYearDays(lunarYear);
      if (remaining < yDays) break;
      remaining -= yDays;
      lunarYear++;
    }

    // 找到农历月和日
    const info = LUNAR_INFO[lunarYear - LUNAR_BASE_YEAR];
    const leapMonth = info & 0xf;
    let isLeap = false;
    let lunarMonth = 1;

    for (let m = 1; m <= 12; m++) {
      const md = (info & (0x10000 >> m)) ? 30 : 29;
      if (remaining < md) {
        lunarMonth = m;
        break;
      }
      remaining -= md;

      // 检查闰月
      if (leapMonth === m) {
        const lmd = (info & (0x10000 >> m)) ? 30 : 29;
        if (remaining < lmd) {
          lunarMonth = m;
          isLeap = true;
          break;
        }
        remaining -= lmd;
      }
    }

    return { year: lunarYear, month: lunarMonth, day: remaining + 1, isLeap };
  }

  // ═══════════════════════════════════════════════
  // 农历 → 公历（下一个生日）
  // ═══════════════════════════════════════════════
  static lunarToSolarNext(currentSolarYear: number, lunarMonth: number, lunarDay: number): Date {
    const now = new Date();

    // 尝试今年
    let thisYearSolar = this.lunarToSolar(currentSolarYear, lunarMonth, lunarDay);
    let result = new Date(thisYearSolar.year, thisYearSolar.month - 1, thisYearSolar.day);
    if (result > now) return result;

    // 尝试明年
    let nextYearSolar = this.lunarToSolar(currentSolarYear + 1, lunarMonth, lunarDay);
    return new Date(nextYearSolar.year, nextYearSolar.month - 1, nextYearSolar.day);
  }

  // ═══════════════════════════════════════════════
  // 农历指定日期 → 公历（精确查找）
  // ═══════════════════════════════════════════════
  private static lunarToSolar(lunarYear: number, lunarMonth: number, lunarDay: number):
    { year: number; month: number; day: number } {

    // 计算农历年起点的偏移天数
    let offset = 0;
    for (let y = LUNAR_BASE_YEAR; y < lunarYear; y++) {
      offset += this.lunarYearDays(y);
    }

    const info = LUNAR_INFO[lunarYear - LUNAR_BASE_YEAR];
    const leapMonth = info & 0xf;

    // 加到目标月
    let targetMonth = lunarMonth;
    for (let m = 1; m < targetMonth; m++) {
      offset += (info & (0x10000 >> m)) ? 30 : 29;
      // 处理闰月
      if (leapMonth === m) {
        offset += (info & (0x10000 >> m)) ? 30 : 29;
      }
    }

    // 加上日期
    offset += lunarDay - 1;

    return this.daysToSolar(offset);
  }

  // ═══════════════════════════════════════════════
  // 判断今天是否是某农历生日
  // ═══════════════════════════════════════════════
  static isLunarBirthdayToday(lunarMonth: number, lunarDay: number): boolean {
    const now = new Date();
    const lunar = this.solarToLunar(now.getFullYear(), now.getMonth() + 1, now.getDate());
    return lunar.month === lunarMonth && lunar.day === lunarDay && !lunar.isLeap;
  }

  // ═══════════════════════════════════════════════
  // 获取当前农历日期字符串
  // ═══════════════════════════════════════════════
  static getCurrentLunarString(): string {
    const now = new Date();
    const lunar = this.solarToLunar(now.getFullYear(), now.getMonth() + 1, now.getDate());
    const leapStr = lunar.isLeap ? '闰' : '';
    const monthNames = ['', '正月', '二月', '三月', '四月', '五月', '六月',
      '七月', '八月', '九月', '十月', '冬月', '腊月'];
    const dayNames = ['', '初一', '初二', '初三', '初四', '初五', '初六', '初七', '初八', '初九', '初十',
      '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十',
      '廿一', '廿二', '廿三', '廿四', '廿五', '廿六', '廿七', '廿八', '廿九', '三十'];
    return `${leapStr}${monthNames[lunar.month]}${dayNames[lunar.day]}`;
  }

  // ═══════════════════════════════════════════════
  // 计算农历生肖
  // ═══════════════════════════════════════════════
  static getZodiacByYear(year: number): string {
    const SHENG_XIAO_FULL = ['鼠', '牛', '虎', '兔', '龙', '蛇', '马', '羊', '猴', '鸡', '狗', '猪'];
    return SHENG_XIAO_FULL[(year - 4) % 12];
  }

  // ═══════════════════════════════════════════════
  // 计算天干地支
  // ═══════════════════════════════════════════════
  static getTianganDizhiByYear(year: number): string {
    const TG = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];
    const DZ = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];
    return `${TG[(year - 4) % 10]}${DZ[(year - 4) % 12]}`;
  }
}
