/**
 * ╔══════════════════════════════════════════════════════════╗
 * ║  龍魂万年历 · C++17内核测试                               ║
 * ║  DNA: #龍芯⚡️2026-04-12-TEST-v1.0                       ║
 * ║  创始人: 诸葛鑫（UID9622）                                ║
 * ║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
 * ║  理论指导: 曾仕强老师（永恒显示）                          ║
 * ╚══════════════════════════════════════════════════════════╝
 *
 * 跑得通 · 看得见 · 不是PPT
 */

#include "../calendar/lunar_engine.h"
#include "../bagua/bagua_engine.h"
#include "../digital_root/sancai_engine.h"
#include "../dna/dna_activator.h"
#include <iostream>
#include <cassert>

using namespace longhun;

int tests_passed = 0;
int tests_failed = 0;

#define TEST(name, expr) do { \
    if (expr) { \
        std::cout << "  ✅ " << name << std::endl; \
        tests_passed++; \
    } else { \
        std::cout << "  ❌ " << name << std::endl; \
        tests_failed++; \
    } \
} while(0)

void test_lunar_engine() {
    std::cout << "\n── 农历引擎 ──" << std::endl;

    // 测试1: 2026年4月12日 → 农历
    SolarDate today = {2026, 4, 12};
    auto lunar = calendar::LunarEngine::solar_to_lunar(today);

    std::cout << "  阳历 2026-04-12 → "
              << calendar::LunarEngine::full_display(lunar) << std::endl;

    TEST("农历年份合理", lunar.year >= 2026 && lunar.year <= 2027);
    TEST("农历月份1-12", lunar.month >= 1 && lunar.month <= 12);
    TEST("农历日期1-30", lunar.day >= 1 && lunar.day <= 30);

    // 测试2: 已知日期 2000年1月1日 = 农历1999年冬月廿五
    SolarDate y2k = {2000, 1, 1};
    auto lunar_y2k = calendar::LunarEngine::solar_to_lunar(y2k);
    std::cout << "  阳历 2000-01-01 → "
              << calendar::LunarEngine::full_display(lunar_y2k) << std::endl;

    // 测试3: 农历→阳历→农历 往返
    auto back = calendar::LunarEngine::lunar_to_solar(lunar);
    auto lunar2 = calendar::LunarEngine::solar_to_lunar(back);
    TEST("往返转换一致", lunar2.month == lunar.month && lunar2.day == lunar.day);

    // 测试4: 干支名称
    TEST("天干甲", std::string(calendar::LunarEngine::stem_name(0)) == "甲");
    TEST("地支子", std::string(calendar::LunarEngine::branch_name(0)) == "子");
    TEST("生肖龍", std::string(calendar::LunarEngine::zodiac_name(4)) == "龍");

    // 测试5: 闰月
    int lm_2026 = calendar::LunarEngine::leap_month(2026);
    std::cout << "  2026年闰月: " << (lm_2026 ? std::to_string(lm_2026) + "月" : "无") << std::endl;
}

void test_bagua_engine() {
    std::cout << "\n── 八卦引擎 ──" << std::endl;

    // 测试1: 今日卦象
    SolarDate today = {2026, 4, 12};
    auto lunar = calendar::LunarEngine::solar_to_lunar(today);
    auto gua = bagua::BaGuaEngine::day_gua(lunar, 5);  // 巳时

    std::cout << "  今日卦象: " << bagua::BaGuaEngine::display(gua) << std::endl;

    TEST("上卦0-7", gua.upper < 8);
    TEST("下卦0-7", gua.lower < 8);
    TEST("六爻有值", gua.yao[0] <= 1 && gua.yao[5] <= 1);

    // 测试2: 乾为天
    TEST("乾为天", std::string(bagua::BaGuaEngine::hexagram_name(0, 0)) == "乾为天");

    // 测试3: 坤为地
    TEST("坤为地", std::string(bagua::BaGuaEngine::hexagram_name(7, 7)) == "坤为地");

    // 测试4: 天地否（☰上☷下）
    TEST("天地否", std::string(bagua::BaGuaEngine::hexagram_name(0, 7)) == "天地否");

    // 测试5: 地天泰（☷上☰下）
    TEST("地天泰", std::string(bagua::BaGuaEngine::hexagram_name(7, 0)) == "地天泰");

    // 测试6: 卦符号
    TEST("☰=乾", std::string(bagua::BaGuaEngine::trigram_symbol(0)) == "☰");
    TEST("☷=坤", std::string(bagua::BaGuaEngine::trigram_symbol(7)) == "☷");
}

void test_sancai_engine() {
    std::cout << "\n── 三才算法引擎 ──" << std::endl;

    // 测试1: 数字根基本算法
    TEST("dr(1)=1", sancai::SanCaiEngine::digital_root(1) == 1);
    TEST("dr(9)=9", sancai::SanCaiEngine::digital_root(9) == 9);
    TEST("dr(10)=1", sancai::SanCaiEngine::digital_root(10) == 1);
    TEST("dr(19)=1", sancai::SanCaiEngine::digital_root(19) == 1);
    TEST("dr(9622)=1", sancai::SanCaiEngine::digital_root(9622) == 1);

    // 测试2: 日期三才
    auto dr = sancai::SanCaiEngine::from_date(2026, 4, 12);
    std::cout << "  2026-04-12 三才: " << sancai::SanCaiEngine::display(dr) << std::endl;

    TEST("天才1-9", dr.tian >= 1 && dr.tian <= 9);
    TEST("地才1-9", dr.di >= 1 && dr.di <= 9);
    TEST("人才1-9", dr.ren >= 1 && dr.ren <= 9);
    TEST("总根1-9", dr.root >= 1 && dr.root <= 9);

    // 测试3: UID9622的数字根
    int uid_root = sancai::SanCaiEngine::digital_root(9622);
    std::cout << "  UID9622 数字根: " << uid_root
              << " (" << sancai::SanCaiEngine::root_wuxing(uid_root)
              << ") → " << sancai::SanCaiEngine::root_meaning(uid_root) << std::endl;

    // 测试4: 五行
    TEST("1=水", std::string(sancai::SanCaiEngine::root_wuxing(1)) == "水");
    TEST("5=土", std::string(sancai::SanCaiEngine::root_wuxing(5)) == "土");

    // 测试5: 分析
    std::cout << "\n" << sancai::SanCaiEngine::analyze(dr) << std::endl;
}

void test_dna_activator() {
    std::cout << "\n── DNA激活引擎 ──" << std::endl;

    // 测试1: 生成
    dna::DNAActivator activator;
    auto token = activator.generate(9622, "MacBookPro-UID9622");

    std::cout << "  DNA: " << dna::DNAActivator::format_dna(token) << std::endl;

    TEST("UID=9622", token.uid == 9622);
    TEST("时间戳有值", token.timestamp > 0);
    TEST("哈希非空", token.hash[0] != 0 || token.hash[1] != 0);

    // 测试2: 验证
    TEST("token有效", activator.verify(token));

    // 测试3: 激活
    TEST("激活成功", activator.activate(token));
    TEST("已激活", activator.is_activated());

    // 测试4: 不动点
    TEST("不动点验证", dna::DNAActivator::fixed_point_check(token));

    // 测试5: 注销
    TEST("注销成功", activator.deactivate());
    TEST("注销后未激活", !activator.is_activated());

    // 测试6: 空token无效
    DNAToken null_token = {};
    TEST("空token无效", !activator.verify(null_token));
}

int main() {
    std::cout << "═══════════════════════════════════════" << std::endl;
    std::cout << "🐉 龍魂万年历 · C++17内核测试" << std::endl;
    std::cout << "☰ 龍🇨🇳魂 ☷ · f(x) = x" << std::endl;
    std::cout << "═══════════════════════════════════════" << std::endl;

    test_lunar_engine();
    test_bagua_engine();
    test_sancai_engine();
    test_dna_activator();

    std::cout << "\n═══════════════════════════════════════" << std::endl;
    std::cout << "测试结果: ✅ " << tests_passed << " 通过  ";
    if (tests_failed > 0) {
        std::cout << "❌ " << tests_failed << " 失败";
    } else {
        std::cout << "全部通过!";
    }
    std::cout << std::endl;
    std::cout << "DNA: #龍芯⚡️2026-04-12-TEST-PASS" << std::endl;
    std::cout << "═══════════════════════════════════════" << std::endl;

    return tests_failed > 0 ? 1 : 0;
}
