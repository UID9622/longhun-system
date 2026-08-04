/*
 * 龍魂·后土OS — 国密底座自检程序（宿主环境运行）
 * DNA: #龍芯⚡️丙午·丙申·乙卯·丁亥·䷉履-GUOMI-SELFTEST-v1.0
 *
 * 用宿主编译器编译运行，验证 SM2/SM3/SM4 实现在标准测试向量下正确。
 * 不依赖 QEMU，直接在 macOS/Linux 上跑。
 *
 * 构建: cc -std=c99 -O2 -Wall -I src/guomi \
 *        src/guomi/sm3.c src/guomi/sm4.c src/guomi/sm2.c \
 *        src/guomi/selftest_main.c -o build/guomi_selftest
 * 或: make selftest
 */

#include <stdio.h>
#include "guomi.h"  /* SM2/SM3/SM4 类型声明与自检声明 */// IWYU pragma: keep

/* 通过 sm3.c/sm4.c/sm2.c 的内部自检函数声明 */
extern int guomi_sm3_selftest(void);
extern int guomi_sm4_selftest(void);
extern int guomi_sm2_selftest(void);

int main(void) {
    int failures = 0;
    int result;

    printf("╔══════════════════════════════════════════════════╗\n");
    printf("║  龍魂·后土OS — 国密底座自检                      ║\n");
    printf("║  DNA: #龍芯⚡️丙午·丙申·乙卯·丁亥·䷉履          ║\n");
    printf("║  SM2/SM3/SM4 · GB/T 32905~32918-2016           ║\n");
    printf("╚══════════════════════════════════════════════════╝\n\n");

    /* SM3 自检 */
    printf("📦 SM3 密码杂凑算法 (GB/T 32905-2016)\n");
    result = guomi_sm3_selftest();
    if (result == 0) {
        printf("  ✅ SM3 自检通过\n");
    } else {
        printf("  🔴 SM3 自检失败 (code=%d)\n", result);
        failures++;
    }

    /* SM4 自检 */
    printf("\n📦 SM4 分组密码算法 (GB/T 32907-2016)\n");
    result = guomi_sm4_selftest();
    if (result == 0) {
        printf("  ✅ SM4 自检通过\n");
    } else {
        printf("  🔴 SM4 自检失败 (code=%d)\n", result);
        failures++;
    }

    /* SM2 自检 */
    printf("\n📦 SM2 椭圆曲线公钥密码算法 (GB/T 32918-2016)\n");
    result = guomi_sm2_selftest();
    if (result == 0) {
        printf("  ✅ SM2 自检通过\n");
    } else {
        printf("  🔴 SM2 自检失败 (code=%d)\n", result);
        failures++;
    }

    printf("\n═══════════════════════════════════════════════════\n");
    if (failures == 0) {
        printf("  🟢 国密底座自检: ALL PASS (3/3)\n");
        printf("  底座状态: 焊死·不可变·龙魂与鸿蒙共用\n");
    } else {
        printf("  🔴 国密底座自检: FAILED (%d/3)\n", failures);
    }
    printf("═══════════════════════════════════════════════════\n");

    return failures;
}
