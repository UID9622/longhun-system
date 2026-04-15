/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║  龍魂万年历 · 农历引擎实现                                ║
 * ║  DNA: #龍芯⚡️2026-04-12-LUNAR-ENGINE-v1.0               ║
 * ║  创始人: 诸葛鑫（UID9622）                                ║
 * ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
 * ║  理论指导: 曾仕强老师（永恒显示）                          ║
 * ║  协议: CC BY-NC-ND                                       ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * 纯C++17 · 不依赖任何平台 · 老大的内核不属于任何生态
 *
 * 献给每一个相信技术应该有温度的人。
 */

#include "lunar_engine.h"
#include <cmath>
#include <sstream>

namespace longhun {
namespace calendar {

// ═══════════════════════════════════════════
// 常量表
// ═══════════════════════════════════════════

static const char* STEMS[] = {
    "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"
};

static const char* BRANCHES[] = {
    "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"
};

static const char* ZODIACS[] = {
    "鼠", "牛", "虎", "兔", "龍", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"
};

static const char* MONTHS[] = {
    "正月", "二月", "三月", "四月", "五月", "六月",
    "七月", "八月", "九月", "十月", "冬月", "腊月"
};

static const char* DAYS[] = {
    "初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
    "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
    "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"
};

// ═══════════════════════════════════════════
// 农历数据表 1900-2100
// 编码方式（从低位到高位）：
//   bit[0-3]:  闰月月份（0=无闰月，1-12=闰几月）
//   bit[4]:    闰月天数（0=小月29天，1=大月30天）
//   bit[5-16]: 正月到腊月每月天数（0=29天，1=30天）
// ═══════════════════════════════════════════

const uint32_t LunarEngine::LUNAR_DATA[] = {
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
    0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x05ac0, 0x0ab60, 0x096d5, 0x092e0,
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
    0x14b63, 0x09370, 0x049f8, 0x04970, 0x064b0, 0x168a6, 0x0ea50, 0x06aa0, 0x1a6c4, 0x0aae0,
    // 2060-2069
    0x092e0, 0x0d2e3, 0x0c960, 0x0d557, 0x0d4a0, 0x0da50, 0x05d55, 0x056a0, 0x0a6d0, 0x055d4,
    // 2070-2079
    0x052d0, 0x0a9b8, 0x0a950, 0x0b4a0, 0x0b6a6, 0x0ad50, 0x055a0, 0x0aba4, 0x0a5b0, 0x052b0,
    // 2080-2089
    0x0b273, 0x06930, 0x07337, 0x06aa0, 0x0ad50, 0x14b55, 0x04b60, 0x0a570, 0x054e4, 0x0d160,
    // 2090-2099
    0x0e968, 0x0d520, 0x0daa0, 0x16aa6, 0x056d0, 0x04ae0, 0x0a9d4, 0x0a2d0, 0x0d150, 0x0f252,
    // 2100
    0x0d520,
};

// ═══════════════════════════════════════════
// 工具函数
// ═══════════════════════════════════════════

int LunarEngine::to_julian_day(const SolarDate& s) {
    int a = (14 - s.month) / 12;
    int y = s.year + 4800 - a;
    int m = s.month + 12 * a - 3;
    return s.day + (153 * m + 2) / 5 + 365 * y + y / 4 - y / 100 + y / 400 - 32045;
}

SolarDate LunarEngine::from_julian_day(int jd) {
    int a = jd + 32044;
    int b = (4 * a + 3) / 146097;
    int c = a - (146097 * b) / 4;
    int d = (4 * c + 3) / 1461;
    int e = c - (1461 * d) / 4;
    int m = (5 * e + 2) / 153;
    SolarDate s;
    s.day = e - (153 * m + 2) / 5 + 1;
    s.month = m + 3 - 12 * (m / 10);
    s.year = 100 * b + d - 4800 + m / 10;
    return s;
}

int LunarEngine::leap_month(int year) {
    if (year < 1900 || year > 2100) return 0;
    return LUNAR_DATA[year - 1900] & 0xf;
}

int LunarEngine::days_in_lunar_month(int year, int month, bool is_leap) {
    if (year < 1900 || year > 2100) return 29;
    uint32_t data = LUNAR_DATA[year - 1900];

    if (is_leap) {
        // 闰月天数
        if ((data & 0xf) != static_cast<uint32_t>(month)) return 0;  // 不是闰月
        return (data & 0x10) ? 30 : 29;
    }

    // 正常月份天数
    return (data & (0x10000 >> (month - 1))) ? 30 : 29;
}

int LunarEngine::days_in_lunar_year(int year) {
    if (year < 1900 || year > 2100) return 354;
    int total = 0;
    uint32_t data = LUNAR_DATA[year - 1900];

    // 12个月
    for (int m = 1; m <= 12; m++) {
        total += (data & (0x10000 >> (m - 1))) ? 30 : 29;
    }

    // 闰月
    int lm = data & 0xf;
    if (lm > 0) {
        total += (data & 0x10) ? 30 : 29;
    }

    return total;
}

int LunarEngine::days_to_lunar_year(int year) {
    int total = 0;
    for (int y = 1900; y < year; y++) {
        total += days_in_lunar_year(y);
    }
    return total;
}

// ═══════════════════════════════════════════
// 核心转换
// ═══════════════════════════════════════════

LunarDate LunarEngine::solar_to_lunar(const SolarDate& solar) {
    // 1900年1月31日 = 农历1900年正月初一
    SolarDate base = {1900, 1, 31};
    int offset = to_julian_day(solar) - to_julian_day(base);

    LunarDate result = {};

    // 逐年累减
    int year = 1900;
    int year_days;
    for (; year <= 2100; year++) {
        year_days = days_in_lunar_year(year);
        if (offset < year_days) break;
        offset -= year_days;
    }
    result.year = year;

    int lm = leap_month(year);
    bool is_leap = false;

    // 逐月累减
    int month = 1;
    int month_days;
    for (; month <= 12; month++) {
        // 正常月
        month_days = days_in_lunar_month(year, month, false);
        if (offset < month_days) {
            break;
        }
        offset -= month_days;

        // 闰月（紧跟在正常月之后）
        if (lm == month) {
            month_days = days_in_lunar_month(year, month, true);
            if (offset < month_days) {
                is_leap = true;
                break;
            }
            offset -= month_days;
        }
    }

    result.month = month;
    result.day = offset + 1;
    result.is_leap = is_leap;

    // 天干地支
    result.stem_index = ((year - 4) % 10 + 10) % 10;
    result.branch_index = ((year - 4) % 12 + 12) % 12;
    result.zodiac_index = result.branch_index;

    return result;
}

SolarDate LunarEngine::lunar_to_solar(const LunarDate& lunar) {
    SolarDate base = {1900, 1, 31};
    int offset = days_to_lunar_year(lunar.year);

    int lm = leap_month(lunar.year);

    // 加上到目标月之前的天数
    for (int m = 1; m < lunar.month; m++) {
        offset += days_in_lunar_month(lunar.year, m, false);
        if (lm == m) {
            offset += days_in_lunar_month(lunar.year, m, true);
        }
    }

    // 如果目标是闰月，加上正常月天数
    if (lunar.is_leap) {
        offset += days_in_lunar_month(lunar.year, lunar.month, false);
    }

    offset += lunar.day - 1;

    int jd = to_julian_day(base) + offset;
    return from_julian_day(jd);
}

// ═══════════════════════════════════════════
// 名称查询
// ═══════════════════════════════════════════

const char* LunarEngine::stem_name(int index) {
    return STEMS[(index % 10 + 10) % 10];
}

const char* LunarEngine::branch_name(int index) {
    return BRANCHES[(index % 12 + 12) % 12];
}

const char* LunarEngine::zodiac_name(int index) {
    return ZODIACS[(index % 12 + 12) % 12];
}

const char* LunarEngine::month_name(int month, bool is_leap) {
    static thread_local char buf[32];
    int idx = (month - 1) % 12;
    if (is_leap) {
        snprintf(buf, sizeof(buf), "闰%s", MONTHS[idx]);
        return buf;
    }
    return MONTHS[idx];
}

const char* LunarEngine::day_name(int day) {
    int idx = (day - 1) % 30;
    return DAYS[idx];
}

std::string LunarEngine::ganzhi_year(int lunar_year) {
    int si = ((lunar_year - 4) % 10 + 10) % 10;
    int bi = ((lunar_year - 4) % 12 + 12) % 12;
    return std::string(STEMS[si]) + BRANCHES[bi] + "年";
}

std::string LunarEngine::full_display(const LunarDate& lunar) {
    std::ostringstream oss;
    oss << stem_name(lunar.stem_index)
        << branch_name(lunar.branch_index)
        << "年【" << zodiac_name(lunar.zodiac_index) << "】"
        << month_name(lunar.month, lunar.is_leap)
        << day_name(lunar.day);
    return oss.str();
}

std::string LunarEngine::short_display(const LunarDate& lunar) {
    return std::string(month_name(lunar.month, lunar.is_leap)) + day_name(lunar.day);
}

}  // namespace calendar
}  // namespace longhun
