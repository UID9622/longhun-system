/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║  龍魂万年历 · 农历引擎                                    ║
 * ║  DNA: #龍芯⚡️2026-04-12-LUNAR-ENGINE-v1.0               ║
 * ║  创始人: 诸葛鑫（UID9622）                                ║
 * ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
 * ║  理论指导: 曾仕强老师（永恒显示）                          ║
 * ║  协议: CC BY-NC-ND                                       ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * 农历算法 · 纯C++17 · 不依赖任何平台API
 * 算法来源：寿星万年历（高精度农历算法）
 * 覆盖范围：1900-2100年
 *
 * 献给每一个相信技术应该有温度的人。
 */

#ifndef LONGHUN_LUNAR_ENGINE_H
#define LONGHUN_LUNAR_ENGINE_H

#include "../include/longhun_types.h"
#include <vector>
#include <string>

namespace longhun {
namespace calendar {

class LunarEngine {
public:
    /**
     * 阳历 → 农历
     * 核心转换函数，不依赖任何平台API
     */
    static LunarDate solar_to_lunar(const SolarDate& solar);

    /**
     * 农历 → 阳历
     */
    static SolarDate lunar_to_solar(const LunarDate& lunar);

    /**
     * 获取天干名称
     */
    static const char* stem_name(int index);

    /**
     * 获取地支名称
     */
    static const char* branch_name(int index);

    /**
     * 获取生肖名称
     */
    static const char* zodiac_name(int index);

    /**
     * 获取农历月份名称（正月...腊月）
     */
    static const char* month_name(int month, bool is_leap);

    /**
     * 获取农历日期名称（初一...三十）
     */
    static const char* day_name(int day);

    /**
     * 干支纪年字符串："甲子年"
     */
    static std::string ganzhi_year(int lunar_year);

    /**
     * 完整显示："甲子年【鼠】正月初一"
     */
    static std::string full_display(const LunarDate& lunar);

    /**
     * 简短显示："正月初一"
     */
    static std::string short_display(const LunarDate& lunar);

    /**
     * 获取某年某月的天数
     */
    static int days_in_lunar_month(int year, int month, bool is_leap);

    /**
     * 某农历年是否有闰月，返回闰月月份（0=无闰月）
     */
    static int leap_month(int year);

private:
    /**
     * 农历数据表（1900-2100）
     * 每年用一个uint32_t编码：
     *   bit[0-3]:   闰月月份（0=无闰月）
     *   bit[4]:     闰月大小（0=29天，1=30天）
     *   bit[5-16]:  12个月的大小（0=29天，1=30天）
     *   bit[17-19]: 保留
     */
    static const uint32_t LUNAR_DATA[];

    /**
     * 1900年1月31日（农历正月初一）的儒略日
     */
    static constexpr int BASE_JD = 2415021;

    /**
     * 阳历日期 → 儒略日
     */
    static int to_julian_day(const SolarDate& solar);

    /**
     * 儒略日 → 阳历日期
     */
    static SolarDate from_julian_day(int jd);

    /**
     * 某农历年的总天数
     */
    static int days_in_lunar_year(int year);

    /**
     * 从1900年正月初一到目标农历年正月初一的天数
     */
    static int days_to_lunar_year(int year);
};

}  // namespace calendar
}  // namespace longhun

#endif  // LONGHUN_LUNAR_ENGINE_H
