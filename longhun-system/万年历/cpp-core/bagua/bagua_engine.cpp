/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║  龍魂万年历 · 八卦引擎实现                                ║
 * ║  DNA: #龍芯⚡️2026-04-12-BAGUA-ENGINE-v1.0               ║
 * ║  创始人: 诸葛鑫（UID9622）                                ║
 * ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
 * ║  理论指导: 曾仕强老师（永恒显示）                          ║
 * ║  协议: CC BY-NC-ND                                       ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * ☰乾☷坤 · 梅花易数核心算法
 * 纯C++17 · 零依赖 · 站着打开市场
 *
 * 献给每一个相信技术应该有温度的人。
 */

#include "bagua_engine.h"
#include <sstream>

namespace longhun {
namespace bagua {

// ═══════════════════════════════════════════
// 八卦基础常量
// ═══════════════════════════════════════════

static const char* TRIGRAM_NAMES[] = {
    "乾", "兑", "离", "震", "巽", "坎", "艮", "坤"
};

static const char* TRIGRAM_SYMBOLS[] = {
    "☰", "☱", "☲", "☳", "☴", "☵", "☶", "☷"
};

static const char* TRIGRAM_NATURE[] = {
    "天", "泽", "火", "雷", "风", "水", "山", "地"
};

// 六十四卦名 [上卦][下卦]
// 索引: 乾0 兑1 离2 震3 巽4 坎5 艮6 坤7
const char* const BaGuaEngine::HEXAGRAM_NAMES[8][8] = {
    // 上乾
    {"乾为天", "天泽履", "天火同人", "天雷无妄", "天风姤",   "天水讼", "天山遁", "天地否"},
    // 上兑
    {"泽天夬", "兑为泽", "泽火革",   "泽雷随",   "泽风大过", "泽水困", "泽山咸", "泽地萃"},
    // 上离
    {"火天大有", "火泽睽", "离为火", "火雷噬嗑", "火风鼎",   "火水未济", "火山旅", "火地晋"},
    // 上震
    {"雷天大壮", "雷泽归妹", "雷火丰", "震为雷", "雷风恒",   "雷水解", "雷山小过", "雷地豫"},
    // 上巽
    {"风天小畜", "风泽中孚", "风火家人", "风雷益", "巽为风", "风水涣", "风山渐", "风地观"},
    // 上坎
    {"水天需", "水泽节", "水火既济", "水雷屯", "水风井",     "坎为水", "水山蹇", "水地比"},
    // 上艮
    {"山天大畜", "山泽损", "山火贲",   "山雷颐", "山风蛊",   "山水蒙", "艮为山", "山地剥"},
    // 上坤
    {"地天泰", "地泽临", "地火明夷", "地雷复",   "地风升",   "地水师", "地山谦", "坤为地"},
};

// 六十四卦卦辞（精要版）
const char* const BaGuaEngine::HEXAGRAM_TEXTS[8][8] = {
    // 上乾
    {"元亨利贞·自强不息", "上天下泽·礼之用也", "同人于野·亨", "无妄·元亨利贞", "天下有风·后以施命", "天与水违行·讼", "天下有山·遁", "天地不交·否"},
    // 上兑
    {"泽上于天·夬", "丽泽兑·朋友讲习", "泽中有火·革", "泽中有雷·随", "泽灭木·大过", "泽无水·困", "山上有泽·咸", "泽上于地·萃"},
    // 上离
    {"火在天上·大有", "上火下泽·睽", "明两作离·继明照四方", "雷电噬嗑", "木上有火·鼎", "火水未济·慎始", "火在山上·旅", "明出地上·晋"},
    // 上震
    {"雷在天上·大壮", "泽上有雷·归妹", "雷电皆至·丰", "洊雷震·恐致福", "雷风相与·恒", "雷雨作·解", "山上有雷·小过", "雷出地奋·豫"},
    // 上巽
    {"风行天上·小畜", "风泽中孚·信及豚鱼", "风自火出·家人", "风雷益·损上益下", "随风巽·申命行事", "风行水上·涣", "山上有木·渐", "风行地上·观"},
    // 上坎
    {"云上于天·需", "泽上有水·节", "水在火上·既济", "云雷屯·经纶", "木上有水·井", "水洊至·习坎", "山上有水·蹇", "地上有水·比"},
    // 上艮
    {"天在山中·大畜", "山下有泽·损", "山下有火·贲", "山下有雷·颐", "山下有风·蛊", "山下出泉·蒙", "兼山艮·止", "山附于地·剥"},
    // 上坤
    {"天地交·泰", "泽上有地·临", "明入地中·明夷", "雷在地中·复", "地中生木·升", "地中有水·师", "地中有山·谦", "地势坤·厚德载物"},
};

// ═══════════════════════════════════════════
// 核心算法
// ═══════════════════════════════════════════

Gua BaGuaEngine::day_gua(const LunarDate& lunar, int shichen_index) {
    // 梅花易数·时间起卦法
    // 上卦 = (年数 + 月 + 日) ÷ 8 取余
    // 下卦 = (年数 + 月 + 日 + 时辰) ÷ 8 取余
    // 动爻 = (年数 + 月 + 日 + 时辰) ÷ 6 取余

    int year_num = lunar.year % 100;  // 取年份后两位
    if (year_num == 0) year_num = 100;

    int sum_upper = year_num + lunar.month + lunar.day;
    int sum_lower = sum_upper + shichen_index + 1;  // 时辰从1开始

    Gua gua = {};
    gua.upper = static_cast<uint8_t>((sum_upper % 8 + 8) % 8);
    gua.lower = static_cast<uint8_t>((sum_lower % 8 + 8) % 8);
    gua.index_64 = hexagram_index(gua.upper, gua.lower);

    // 动爻
    int dong_yao = ((sum_lower % 6) + 6) % 6;

    // 构造六爻（上卦3爻 + 下卦3爻）
    // 乾=111, 兑=110, 离=101, 震=100, 巽=011, 坎=010, 艮=001, 坤=000
    static const uint8_t TRIGRAM_BITS[8] = {
        0b111, 0b110, 0b101, 0b100, 0b011, 0b010, 0b001, 0b000
    };

    uint8_t lower_bits = TRIGRAM_BITS[gua.lower];
    uint8_t upper_bits = TRIGRAM_BITS[gua.upper];

    gua.yao[0] = (lower_bits >> 0) & 1;  // 初爻
    gua.yao[1] = (lower_bits >> 1) & 1;  // 二爻
    gua.yao[2] = (lower_bits >> 2) & 1;  // 三爻
    gua.yao[3] = (upper_bits >> 0) & 1;  // 四爻
    gua.yao[4] = (upper_bits >> 1) & 1;  // 五爻
    gua.yao[5] = (upper_bits >> 2) & 1;  // 上爻

    // 动爻翻转
    gua.yao[dong_yao] ^= 1;

    return gua;
}

Gua BaGuaEngine::from_numbers(int num1, int num2, int dong_yao) {
    Gua gua = {};
    gua.upper = static_cast<uint8_t>((num1 % 8 + 8) % 8);
    gua.lower = static_cast<uint8_t>((num2 % 8 + 8) % 8);
    gua.index_64 = hexagram_index(gua.upper, gua.lower);

    static const uint8_t TRIGRAM_BITS[8] = {
        0b111, 0b110, 0b101, 0b100, 0b011, 0b010, 0b001, 0b000
    };

    uint8_t lower_bits = TRIGRAM_BITS[gua.lower];
    uint8_t upper_bits = TRIGRAM_BITS[gua.upper];

    gua.yao[0] = (lower_bits >> 0) & 1;
    gua.yao[1] = (lower_bits >> 1) & 1;
    gua.yao[2] = (lower_bits >> 2) & 1;
    gua.yao[3] = (upper_bits >> 0) & 1;
    gua.yao[4] = (upper_bits >> 1) & 1;
    gua.yao[5] = (upper_bits >> 2) & 1;

    if (dong_yao >= 0 && dong_yao < 6) {
        gua.yao[dong_yao] ^= 1;
    }

    return gua;
}

const char* BaGuaEngine::trigram_name(uint8_t index) {
    return TRIGRAM_NAMES[index % 8];
}

const char* BaGuaEngine::trigram_symbol(uint8_t index) {
    return TRIGRAM_SYMBOLS[index % 8];
}

const char* BaGuaEngine::hexagram_name(uint8_t upper, uint8_t lower) {
    return HEXAGRAM_NAMES[upper % 8][lower % 8];
}

uint8_t BaGuaEngine::hexagram_index(uint8_t upper, uint8_t lower) {
    return (upper % 8) * 8 + (lower % 8);
}

const char* BaGuaEngine::hexagram_text(uint8_t upper, uint8_t lower) {
    return HEXAGRAM_TEXTS[upper % 8][lower % 8];
}

std::string BaGuaEngine::display(const Gua& gua) {
    std::ostringstream oss;
    oss << trigram_symbol(gua.upper) << TRIGRAM_NATURE[gua.upper]
        << " over "
        << trigram_symbol(gua.lower) << TRIGRAM_NATURE[gua.lower]
        << " = " << hexagram_name(gua.upper, gua.lower)
        << "\n卦辞: " << hexagram_text(gua.upper, gua.lower)
        << "\n六爻: ";
    for (int i = 5; i >= 0; i--) {
        oss << (gua.yao[i] ? "⚊" : "⚋");
    }
    return oss.str();
}

std::string BaGuaEngine::short_display(const Gua& gua) {
    return hexagram_name(gua.upper, gua.lower);
}

}  // namespace bagua
}  // namespace longhun
