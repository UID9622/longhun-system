/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║  龍魂万年历 · 核心类型定义                                ║
 * ║  DNA: #龍芯⚡️2026-04-12-CALENDAR-TYPES-v1.0             ║
 * ║  创始人: 诸葛鑫（UID9622）                                ║
 * ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
 * ║  理论指导: 曾仕强老师（永恒显示）                          ║
 * ║  协议: CC BY-NC-ND                                       ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * C++17 纯内核 · 不属于任何平台 · 站着打开市场
 * iOS用Secure Enclave · 鸿蒙用华为TEE · 换个桥接层就完事
 *
 * 献给每一个相信技术应该有温度的人。
 */

#ifndef LONGHUN_TYPES_H
#define LONGHUN_TYPES_H

#include <cstdint>
#include <string>
#include <array>

namespace longhun {

// ═══════════════════════════════════════════
// 农历日期
// ═══════════════════════════════════════════

struct LunarDate {
    int year;       // 农历年
    int month;      // 1-12
    int day;        // 1-30
    bool is_leap;   // 是否闰月

    // 天干地支
    int stem_index;     // 天干索引 0-9
    int branch_index;   // 地支索引 0-11
    int zodiac_index;   // 生肖索引 0-11
};

// ═══════════════════════════════════════════
// 阳历日期
// ═══════════════════════════════════════════

struct SolarDate {
    int year;
    int month;
    int day;
};

// ═══════════════════════════════════════════
// 时辰
// ═══════════════════════════════════════════

struct ShiChen {
    int index;          // 0-11 (子丑寅卯辰巳午未申酉戌亥)
    int hour_start;     // 起始小时
    int hour_end;       // 结束小时
};

// ═══════════════════════════════════════════
// 卦象
// ═══════════════════════════════════════════

struct Gua {
    uint8_t upper;      // 上卦 0-7 (乾兑离震巽坎艮坤)
    uint8_t lower;      // 下卦 0-7
    uint8_t index_64;   // 六十四卦序号 0-63
    uint8_t yao[6];     // 六爻 (0=阴, 1=阳)
};

// ═══════════════════════════════════════════
// 数字根（三才算法核心）
// ═══════════════════════════════════════════

struct DigitalRoot {
    int original;       // 原始数
    int root;           // 数字根 1-9
    int tian;           // 天才数
    int di;             // 地才数
    int ren;            // 人才数
};

// ═══════════════════════════════════════════
// DNA激活凭证
// ═══════════════════════════════════════════

struct DNAToken {
    std::array<uint8_t, 32> hash;   // SHA-256哈希
    uint64_t timestamp;              // 激活时间戳
    uint32_t uid;                    // 用户ID
    bool activated;                  // 是否已激活
};

// ═══════════════════════════════════════════
// 黄历宜忌
// ═══════════════════════════════════════════

enum class HuangLiAction : uint8_t {
    YI,     // 宜
    JI,     // 忌
    ZHONG   // 中性
};

struct HuangLiItem {
    std::string action;         // 行为名称
    HuangLiAction suitability;  // 宜/忌/中
};

// ═══════════════════════════════════════════
// 万年历一天的完整数据
// ═══════════════════════════════════════════

struct DayInfo {
    SolarDate solar;
    LunarDate lunar;
    ShiChen current_shichen;
    Gua day_gua;
    DigitalRoot day_root;
    // 黄历条目由上层填充
};

}  // namespace longhun

#endif  // LONGHUN_TYPES_H
