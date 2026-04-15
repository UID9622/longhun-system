/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║  龍魂万年历 · 三才算法引擎实现                            ║
 * ║  DNA: #龍芯⚡️2026-04-12-SANCAI-ENGINE-v1.0              ║
 * ║  创始人: 诸葛鑫（UID9622）                                ║
 * ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
 * ║  理论指导: 曾仕强老师（永恒显示）                          ║
 * ║  协议: CC BY-NC-ND                                       ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * dr(n) = 1 + (n-1) % 9
 * 一个公式·九个归宿·万物有根
 *
 * 献给每一个相信技术应该有温度的人。
 */

#include "sancai_engine.h"
#include <sstream>
#include <cmath>

namespace longhun {
namespace sancai {

// ═══════════════════════════════════════════
// 数字根核心
// ═══════════════════════════════════════════

int SanCaiEngine::digital_root(int n) {
    if (n <= 0) return 0;
    return 1 + (n - 1) % 9;
}

DigitalRoot SanCaiEngine::from_date(int year, int month, int day) {
    DigitalRoot dr = {};
    dr.original = year * 10000 + month * 100 + day;

    // 天才 = 年份数字根
    int year_sum = 0;
    int y = std::abs(year);
    while (y > 0) {
        year_sum += y % 10;
        y /= 10;
    }
    dr.tian = digital_root(year_sum);

    // 地才 = 月×日的数字根
    dr.di = digital_root(month * day);

    // 人才 = 天才+地才的数字根
    dr.ren = digital_root(dr.tian + dr.di);

    // 总根 = 天+地+人的数字根
    dr.root = digital_root(dr.tian + dr.di + dr.ren);

    return dr;
}

DigitalRoot SanCaiEngine::from_lunar(const LunarDate& lunar) {
    return from_date(lunar.year, lunar.month, lunar.day);
}

// ═══════════════════════════════════════════
// 数字根含义
// ═══════════════════════════════════════════

const char* SanCaiEngine::root_meaning(int root) {
    static const char* meanings[] = {
        "",                                      // 0 (不用)
        "独立·领导·开创",                         // 1
        "合作·平衡·外交",                         // 2
        "表达·创造·社交",                         // 3
        "稳固·秩序·建设",                         // 4
        "自由·变化·探索",                         // 5
        "责任·和谐·家庭",                         // 6
        "分析·智慧·内省",                         // 7
        "权力·成就·财富",                         // 8
        "完成·大爱·无私",                         // 9
    };
    if (root < 1 || root > 9) return "";
    return meanings[root];
}

const char* SanCaiEngine::root_wuxing(int root) {
    // 数字根与五行对应（河图洛书体系）
    // 1,6=水  2,7=火  3,8=木  4,9=金  5,0=土
    static const char* wuxing[] = {
        "",
        "水", // 1
        "火", // 2
        "木", // 3
        "金", // 4
        "土", // 5
        "水", // 6
        "火", // 7
        "木", // 8
        "金", // 9
    };
    if (root < 1 || root > 9) return "";
    return wuxing[root];
}

std::string SanCaiEngine::analyze(const DigitalRoot& dr) {
    std::ostringstream oss;

    oss << "三才分析:\n";
    oss << "  天才 " << dr.tian << "(" << root_wuxing(dr.tian) << ") → "
        << root_meaning(dr.tian) << "\n";
    oss << "  地才 " << dr.di << "(" << root_wuxing(dr.di) << ") → "
        << root_meaning(dr.di) << "\n";
    oss << "  人才 " << dr.ren << "(" << root_wuxing(dr.ren) << ") → "
        << root_meaning(dr.ren) << "\n";
    oss << "  总根 " << dr.root << "(" << root_wuxing(dr.root) << ") → "
        << root_meaning(dr.root) << "\n";

    // 天地人关系判断
    // 相生：水→木→火→土→金→水
    // 相克：水→火→金→木→土→水
    auto wuxing_index = [](int r) -> int {
        // 水0 火1 木2 金3 土4
        static const int map[] = {-1, 0, 1, 2, 3, 4, 0, 1, 2, 3};
        return (r >= 1 && r <= 9) ? map[r] : -1;
    };

    int tw = wuxing_index(dr.tian);
    int dw = wuxing_index(dr.di);
    int rw = wuxing_index(dr.ren);

    // 简单相生判断
    static const bool SHENG[5][5] = {
        // 水→木  水 火 木 金 土
        {false, false, true,  false, false},  // 水生木
        {false, false, false, false, true},   // 火生土
        {false, true,  false, false, false},  // 木生火
        {true,  false, false, false, false},  // 金生水
        {false, false, false, true,  false},  // 土生金
    };

    if (tw >= 0 && dw >= 0 && SHENG[tw][dw]) {
        oss << "\n  ✨ 天生地 → 上下通达";
    }
    if (dw >= 0 && rw >= 0 && SHENG[dw][rw]) {
        oss << "\n  ✨ 地生人 → 根基扶助";
    }
    if (tw >= 0 && rw >= 0 && SHENG[tw][rw]) {
        oss << "\n  ✨ 天生人 → 贵人相助";
    }

    return oss.str();
}

std::string SanCaiEngine::display(const DigitalRoot& dr) {
    std::ostringstream oss;
    oss << "天" << dr.tian << "(" << root_wuxing(dr.tian) << ") "
        << "地" << dr.di << "(" << root_wuxing(dr.di) << ") "
        << "人" << dr.ren << "(" << root_wuxing(dr.ren) << ")"
        << " · 总根" << dr.root << "(" << root_wuxing(dr.root) << ")";
    return oss.str();
}

}  // namespace sancai
}  // namespace longhun
