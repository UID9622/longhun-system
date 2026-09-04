/*
 * 测试 SM2 基点 G 曲线验证
 * DNA: #龍芯⚡️丙午·丙申·乙卯·亥时·需-GUOMI-TEST_G-v1.0
 *
 * 编译: cd 03_后土OS/src/guomi && clang -Wall -std=c99 test_g.c -o /tmp/test_g
 *
 * 采用单翻译单元方式直接 #include sm2.c，可访问内部 static 函数。
 */
#include <stdio.h>
#include <stdint.h>
#include "sm3.c"  /* sm2.c 依赖 sm3 哈希函数 */
#include "sm2.c"  /* 单TU include，同目录下 sm3.c/sm2.c + guomi.h 均可解析 */
#undef main
int main(void) {
    printf("SM2 G 点曲线验证\n==================\n");

    sm2_point_t G;
    sm2_point_get_G(&G);

    printf("G.x = ");
    for (int i = 3; i >= 0; i--) printf("%016llX", (unsigned long long)G.x[i]);
    printf("\nG.y = ");
    for (int i = 3; i >= 0; i--) printf("%016llX", (unsigned long long)G.y[i]);
    printf("\nG.is_infinity = %d\n", G.is_infinity);

    printf("\n验证 SM2 参数...\n");
    int ret = guomi_sm2_validate_params();
    printf("validate_params() = %d\n", ret);

    int on_curve = sm2_point_on_curve(&G);
    printf("point_on_curve(G) = %d\n", on_curve);

    /* 手动验证 y² ≡ x³ + ax + b (mod p) */
    sm2_fe_t y2, x3, ax, rhs, t1;
    uint64_t raw[8];

    sm2_fe_mul_raw(raw, G.y, G.y);
    sm2_fast_reduce(y2, raw);

    sm2_fe_mul_raw(raw, G.x, G.x);
    sm2_fast_reduce(t1, raw);
    sm2_fe_mul_raw(raw, t1, G.x);
    sm2_fast_reduce(x3, raw);

    sm2_fe_mul_raw(raw, SM2_A, G.x);
    sm2_fast_reduce(ax, raw);

    sm2_fe_add(rhs, x3, ax);
    while (sm2_fe_ge(rhs, SM2_P)) sm2_fe_sub(rhs, rhs, SM2_P);
    sm2_fe_add(rhs, rhs, SM2_B);
    while (sm2_fe_ge(rhs, SM2_P)) sm2_fe_sub(rhs, rhs, SM2_P);

    printf("\ny²      = "); for (int i = 3; i >= 0; i--) printf("%016llX", (unsigned long long)y2[i]);
    printf("\nx³+ax+b = "); for (int i = 3; i >= 0; i--) printf("%016llX", (unsigned long long)rhs[i]);
    printf("\nExpected y² = FBF2EDDD128CDEF06491287E877DA3674FBB9591CE6200A6B09D6E1D38D4C1E5\n");
    printf("Match: %s\n", sm2_fe_eq(y2, rhs) ? "YES" : "NO");

    return 0;
}
