/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║  龍魂万年历 · 八卦引擎                                    ║
 * ║  DNA: #龍芯⚡️2026-04-12-BAGUA-ENGINE-v1.0               ║
 * ║  创始人: 诸葛鑫（UID9622）                                ║
 * ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
 * ║  理论指导: 曾仕强老师（永恒显示）                          ║
 * ║  协议: CC BY-NC-ND                                       ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * ☰乾☷坤 · 八卦六十四卦算法 · 纯C++17
 * 日卦：从日期推算每天的本卦+变卦
 * 时卦：时辰叠加当日卦象
 *
 * 献给每一个相信技术应该有温度的人。
 */

#ifndef LONGHUN_BAGUA_ENGINE_H
#define LONGHUN_BAGUA_ENGINE_H

#include "../include/longhun_types.h"
#include <string>
#include <array>

namespace longhun {
namespace bagua {

// 八卦索引：乾0 兑1 离2 震3 巽4 坎5 艮6 坤7
// 对应先天八卦序

class BaGuaEngine {
public:
    /**
     * 从农历日期推算日卦
     * 方法：(农历年+月+日) 取上卦，(年+月+日+时辰) 取下卦
     */
    static Gua day_gua(const LunarDate& lunar, int shichen_index = 0);

    /**
     * 从数字推算卦象（梅花易数）
     * 上卦 = num1 % 8, 下卦 = num2 % 8
     */
    static Gua from_numbers(int num1, int num2, int dong_yao = 0);

    /**
     * 获取八卦名称（单卦）
     */
    static const char* trigram_name(uint8_t index);

    /**
     * 获取八卦符号
     */
    static const char* trigram_symbol(uint8_t index);

    /**
     * 获取六十四卦名称
     */
    static const char* hexagram_name(uint8_t upper, uint8_t lower);

    /**
     * 获取六十四卦序号（按先天排列）
     */
    static uint8_t hexagram_index(uint8_t upper, uint8_t lower);

    /**
     * 卦象完整显示
     * 例："☰天 over ☷地 = 天地否"
     */
    static std::string display(const Gua& gua);

    /**
     * 简短显示
     * 例："天地否"
     */
    static std::string short_display(const Gua& gua);

    /**
     * 获取卦辞（简要）
     */
    static const char* hexagram_text(uint8_t upper, uint8_t lower);

private:
    // 六十四卦名称表 [上卦][下卦]
    static const char* const HEXAGRAM_NAMES[8][8];

    // 六十四卦卦辞（简要）
    static const char* const HEXAGRAM_TEXTS[8][8];
};

}  // namespace bagua
}  // namespace longhun

#endif  // LONGHUN_BAGUA_ENGINE_H
