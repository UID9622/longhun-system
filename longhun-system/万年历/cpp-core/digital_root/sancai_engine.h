/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║  龍魂万年历 · 三才算法引擎                                ║
 * ║  DNA: #龍芯⚡️2026-04-12-SANCAI-ENGINE-v1.0              ║
 * ║  创始人: 诸葛鑫（UID9622）                                ║
 * ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
 * ║  理论指导: 曾仕强老师（永恒显示）                          ║
 * ║  协议: CC BY-NC-ND                                       ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * 三才 = 天·地·人
 * 数字根 = dr(n) = 1 + (n-1) % 9
 * 曾老师说：天地人三才贯穿一切
 *
 * 献给每一个相信技术应该有温度的人。
 */

#ifndef LONGHUN_SANCAI_ENGINE_H
#define LONGHUN_SANCAI_ENGINE_H

#include "../include/longhun_types.h"
#include <string>

namespace longhun {
namespace sancai {

class SanCaiEngine {
public:
    /**
     * 数字根: dr(n) = 1 + (n-1) % 9
     * 任何正整数最终归结为1-9
     */
    static int digital_root(int n);

    /**
     * 从日期计算三才数
     * 天才 = dr(年)
     * 地才 = dr(月×日)
     * 人才 = dr(天才+地才)
     */
    static DigitalRoot from_date(int year, int month, int day);

    /**
     * 从农历日期计算三才
     */
    static DigitalRoot from_lunar(const LunarDate& lunar);

    /**
     * 数字根含义
     */
    static const char* root_meaning(int root);

    /**
     * 数字根五行属性
     */
    static const char* root_wuxing(int root);

    /**
     * 三才组合分析
     */
    static std::string analyze(const DigitalRoot& dr);

    /**
     * 完整显示
     * 例："天3(火) 地7(金) 人1(水) · 总根5(土)"
     */
    static std::string display(const DigitalRoot& dr);
};

}  // namespace sancai
}  // namespace longhun

#endif  // LONGHUN_SANCAI_ENGINE_H
