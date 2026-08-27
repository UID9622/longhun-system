// include/CNSH_TestSuite.h
// DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-CNSH-TEST-SUITE-v1.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)  ← 工程实现层
// 说明: CNSH C 语言测试宏套件（C 侧资产测试用），三色审计 + DNA 校验 + 计时。

#ifndef CNSH_TEST_SUITE_H
#define CNSH_TEST_SUITE_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// ─── 三色审计（ANSI 颜色）───
#define CNSH_TEST_GREEN   "\033[32m"   // 🟢 通过
#define CNSH_TEST_YELLOW  "\033[33m"   // 🟡 待审
#define CNSH_TEST_RED     "\033[31m"   // 🔴 失败
#define CNSH_TEST_RESET   "\033[0m"

// ─── 测试计数器 ───
static int cnsh_test_passed = 0;
static int cnsh_test_failed = 0;
static int cnsh_test_total  = 0;
static clock_t cnsh_test_start;

// ─── 断言宏 ───
#define CNSH_ASSERT(expr) \
    do { \
        cnsh_test_total++; \
        if (expr) { \
            cnsh_test_passed++; \
            printf(CNSH_TEST_GREEN "[PASS]" CNSH_TEST_RESET " %-40s line:%d\n", #expr, __LINE__); \
        } else { \
            cnsh_test_failed++; \
            printf(CNSH_TEST_RED "[FAIL]" CNSH_TEST_RESET " %-40s line:%d\n", #expr, __LINE__); \
        } \
    } while(0)

#define CNSH_ASSERT_EQ(a, b)      CNSH_ASSERT((a) == (b))
#define CNSH_ASSERT_NE(a, b)      CNSH_ASSERT((a) != (b))
#define CNSH_ASSERT_GT(a, b)      CNSH_ASSERT((a) > (b))
#define CNSH_ASSERT_LT(a, b)      CNSH_ASSERT((a) < (b))
#define CNSH_ASSERT_STR_EQ(a, b)  CNSH_ASSERT(strcmp((a), (b)) == 0)
#define CNSH_ASSERT_NOT_NULL(p)   CNSH_ASSERT((p) != NULL)
#define CNSH_ASSERT_NULL(p)       CNSH_ASSERT((p) == NULL)

// ─── 三色断言 ───
#define CNSH_TRI_COLOR(expr, label) \
    do { \
        cnsh_test_total++; \
        if (expr) { \
            cnsh_test_passed++; \
            printf(CNSH_TEST_GREEN "  🟢 " CNSH_TEST_RESET "%s\n", label); \
        } else { \
            cnsh_test_failed++; \
            printf(CNSH_TEST_RED   "  🔴 " CNSH_TEST_RESET "%s\n", label); \
        } \
    } while(0)

// ─── DNA 校验宏（宽松: 必须含 #龍芯⚡️）───
#define CNSH_DNA_CHECK(dna_str) \
    do { \
        cnsh_test_total++; \
        if (dna_str != NULL && strstr(dna_str, "#龍芯⚡️") != NULL) { \
            cnsh_test_passed++; \
            printf(CNSH_TEST_GREEN "[DNA 🟢]" CNSH_TEST_RESET " %s\n", dna_str); \
        } else { \
            cnsh_test_failed++; \
            printf(CNSH_TEST_RED "[DNA 🔴]" CNSH_TEST_RESET " 无效DNA: %s\n", \
                   dna_str ? dna_str : "NULL"); \
        } \
    } while(0)

// ─── 测试组标记 ───
#define CNSH_TEST_GROUP(name) \
    printf("\n  ─── %s ───\n", name);

// ─── 套件入口（带计时）───
#define CNSH_TEST_SUITE(name) \
    int main(void) { \
        cnsh_test_start = clock(); \
        printf("\n🐉 CNSH 测试套件: %s\n", name); \
        printf("DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-CNSH-TEST-SUITE-v1.0-UID9622\n"); \
        printf("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

#define CNSH_TEST_SUITE_END() \
        double elapsed = (double)(clock() - cnsh_test_start) / CLOCKS_PER_SEC; \
        printf("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"); \
        printf("总计: %d | ✅ 通过: %d | ❌ 失败: %d | 耗时: %.3fs\n", \
               cnsh_test_total, cnsh_test_passed, cnsh_test_failed, elapsed); \
        const char* tri = cnsh_test_failed == 0 ? "🟢" \
                        : (cnsh_test_failed <= cnsh_test_total/5) ? "🟡" : "🔴"; \
        printf("三色: %s\n", tri); \
        return cnsh_test_failed > 0 ? 1 : 0; \
    }

#endif /* CNSH_TEST_SUITE_H */
