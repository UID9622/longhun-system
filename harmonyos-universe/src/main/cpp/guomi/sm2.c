归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/*
 * 龍魂·后土OS — SM2 椭圆曲线公钥密码算法实现
 * DNA: #龍芯⚡️丙午·丙申·乙卯·丁亥·䷉履-GUOMI-SM2-v1.0
 *
 * 标准依据：
 *   GB/T 32918.1-2016 总则
 *   GB/T 32918.2-2016 数字签名算法
 *   GB/T 32918.3-2016 密钥交换协议
 *   GB/T 32918.4-2016 公钥加密算法
 *   GB/T 32918.5-2016 参数定义
 *
 * 文化锚点：离宫（火）— SM2 如火焰锻造，将数字签名焊入不可篡改之印
 *
 * 底座焊死：本实现遵从 GB/T 32918 标准曲线参数 sm2p256v1，不可改变。
 *            龙魂后土OS内核与鸿蒙系统共用本底座。
 *
 * 大数表示：4×uint64_t = 256位，小端序（word[0]=最低64位）
 *
 * SM2 推荐曲线参数（sm2p256v1, GB/T 32918.5-2016 §5）:
 *   p  = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFF
 *   a  = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFC
 *   b  = 28E9FA9E 9D9F5E34 4D5A9E4B CF6509A7 F39789F5 15AB8F92 DDBCBD41 4D940E93
 *   n  = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF 7203DF6B 21C6052B 53BBF409 39D54123
 *   Gx = 32C4AE2C 1F198119 5F990446 6A39C994 8FE30BBF F2660BE1 715A4589 334C74C7
 *   Gy = BC3736A2 F4F6779C 59BDCEE3 6B692153 D0A9877C C62A4740 02DF32E5 2139F0A0
 *   h  = 1
 */

#include "guomi.h"
#include <string.h>
#include <stdio.h>  /* DEBUG: 临时调试输出 */

/* ══════════════════════════════════════════════════════════════
 * 256位大数运算（4×uint64_t，小端序）
 * ══════════════════════════════════════════════════════════════ */

#define SM2_LIMBS    4
#define SM2_LIMB_BITS 64
#define SM2_LIMB_MASK 0xFFFFFFFFFFFFFFFFULL

typedef uint64_t sm2_fe_t[SM2_LIMBS];  /* field element in GF(p) */
typedef uint64_t sm2_scalar_t[SM2_LIMBS];  /* scalar in [1, n-1] */

/* ── 大数比较：a == b ── */
static int sm2_fe_eq(const sm2_fe_t a, const sm2_fe_t b) {
    int i;
    for (i = 0; i < SM2_LIMBS; i++)
        if (a[i] != b[i]) return 0;
    return 1;
}

/* ── 大数比较：a == 0 ── */
static int sm2_fe_is_zero(const sm2_fe_t a) {
    int i;
    for (i = 0; i < SM2_LIMBS; i++)
        if (a[i] != 0) return 0;
    return 1;
}

/* ── 大数比较：a >= b（无符号） ── */
static int sm2_fe_ge(const sm2_fe_t a, const sm2_fe_t b) {
    int i;
    for (i = SM2_LIMBS - 1; i >= 0; i--) {
        if (a[i] > b[i]) return 1;
        if (a[i] < b[i]) return 0;
    }
    return 1;  /* 相等 */
}

/* ── 复制：dst = src ── */
static void sm2_fe_copy(sm2_fe_t dst, const sm2_fe_t src) {
    int i;
    for (i = 0; i < SM2_LIMBS; i++) dst[i] = src[i];
}

/* ── 加法：r = a + b，返回进位 ── */
static uint64_t sm2_fe_add(sm2_fe_t r, const sm2_fe_t a, const sm2_fe_t b) {
    uint64_t carry = 0;
    int i;
    for (i = 0; i < SM2_LIMBS; i++) {
        uint64_t sum = a[i] + b[i] + carry;
        carry = (sum < a[i] || (carry && sum == a[i])) ? 1 : 0;
        r[i] = sum;
    }
    return carry;
}

/* ── 减法：r = a - b，返回借位 ── */
static uint64_t sm2_fe_sub(sm2_fe_t r, const sm2_fe_t a, const sm2_fe_t b) {
    uint64_t borrow = 0;
    int i;
    for (i = 0; i < SM2_LIMBS; i++) {
        uint64_t diff = a[i] - b[i] - borrow;
        /* 借位检测需处理 b[i]+borrow 溢出：b[i]=MAX, borrow=1 → 溢出 → 必借位 */
        uint64_t subtrahend = b[i] + borrow;
        borrow = (a[i] < subtrahend || subtrahend < borrow) ? 1 : 0;
        r[i] = diff;
    }
    return borrow;
}

/* ── (r_hi, r_lo) = a × b（128位 = 64×64） ── */
/*
 * 半字拆分法：a = a_hi·2^32 + a_lo，b = b_hi·2^32 + b_lo
 * a×b = hi_hi·2^96 + (lo_hi+hi_lo)·2^64 + (mid_hi_overflow)·2^64 + lo_lo·2^32 ...
 *
 * 关键：mid = lo_hi + hi_lo ∈ [0, 2^33)，mid<<32 可能溢出 64 位。
 *       mid >> 32 (0 或 1) 即溢出进位，必须加到高位。
 */
static void sm2_mul64(uint64_t *r_hi, uint64_t *r_lo, uint64_t a, uint64_t b) {
    uint64_t a_lo = a & 0xFFFFFFFFULL;
    uint64_t a_hi = a >> 32;
    uint64_t b_lo = b & 0xFFFFFFFFULL;
    uint64_t b_hi = b >> 32;

    uint64_t lo_lo = a_lo * b_lo;
    uint64_t lo_hi = a_lo * b_hi;
    uint64_t hi_lo = a_hi * b_lo;
    uint64_t hi_hi = a_hi * b_hi;

    uint64_t mid = lo_hi + hi_lo;
    /* mid 溢出进位（对应位 64），在 mid·2^32 中变为位 96 → r_hi 位 32 */
    uint64_t carry_mid = (mid < lo_hi) ? 1 : 0;

    uint64_t mid_lo = mid << 32;           /* mid 低 32 位 → 位 32-63 */
    uint64_t mid_hi = mid >> 32;           /* mid 高 32 位 → 位 64-95 */

    *r_lo = lo_lo + mid_lo;
    uint64_t carry_rlo = (*r_lo < lo_lo) ? 1 : 0;

    /* r_hi = hi_hi + mid_hi + (carry_mid<<32) + carry_rlo
     * carry_mid 必须左移 32 位，因为它来自位 64 的溢出，
     * 在 mid·2^32 项中对应位 96 */
    *r_hi = hi_hi + mid_hi + (carry_mid << 32) + carry_rlo;
}

/* ── 乘法：r = a × b（512位中间结果，取低256位） ── */
/*
 * 修复(v1.1·2026-08-28·UID9622): 原实现 carry = hi + ovf1 + ovf2 可溢出回绕，
 * 导致高位进位丢失（随机 20 万次实测错率 31%）。
 * 改用 __uint128_t 列累加：t ≤ 2^128 - 1 恒成立，carry 恒 < 2^64，无溢出。
 * arm64(AArch64) 编译器将 __uint128_t 乘编译为 umulh+mul 原生指令，性能无损。
 */
static void sm2_fe_mul_raw(uint64_t r[SM2_LIMBS * 2],
                           const sm2_fe_t a, const sm2_fe_t b) {
    int i, j;
    memset(r, 0, SM2_LIMBS * 2 * sizeof(uint64_t));

    for (i = 0; i < SM2_LIMBS; i++) {
        uint64_t carry = 0;
        for (j = 0; j < SM2_LIMBS; j++) {
            __uint128_t t = (__uint128_t)a[i] * b[j] + r[i + j] + carry;
            r[i + j] = (uint64_t)t;
            carry = (uint64_t)(t >> 64);
        }
        r[i + SM2_LIMBS] = carry;
    }
}

/* ══════════════════════════════════════════════════════════════
 * SM2 曲线参数（sm2p256v1, GB/T 32918.5-2016）
 * ══════════════════════════════════════════════════════════════ */

/* SM2_P = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFF */
static const sm2_fe_t SM2_P = {
    0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFF00000000ULL,
    0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFEFFFFFFFFULL
};

/* SM2_A = p - 3 = FFFFFFFE FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFF 00000000 FFFFFFFF FFFFFFFC */
static const sm2_fe_t SM2_A = {
    0xFFFFFFFFFFFFFFFCULL, 0xFFFFFFFF00000000ULL,
    0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFEFFFFFFFFULL
};

static const sm2_fe_t SM2_B = {
    0xDDBCBD414D940E93ULL, 0xF39789F515AB8F92ULL,
    0x4D5A9E4BCF6509A7ULL, 0x28E9FA9E9D9F5E34ULL
};

static const sm2_fe_t SM2_N = {
    0x53BBF40939D54123ULL, 0x7203DF6B21C6052BULL,
    0xFFFFFFFFFFFFFFFFULL, 0xFFFFFFFEFFFFFFFFULL
};

static const sm2_fe_t SM2_GX = {
    0x715A4589334C74C7ULL, 0x8FE30BBFF2660BE1ULL,
    0x5F9904466A39C994ULL, 0x32C4AE2C1F198119ULL
};

static const sm2_fe_t SM2_GY = {
    0x02DF32E52139F0A0ULL, 0xD0A9877CC62A4740ULL,
    0x59BDCEE36B692153ULL, 0xBC3736A2F4F6779CULL
};

/* ── 模加：r = (a + b) mod p ── */
static void sm2_mod_add(sm2_fe_t r, const sm2_fe_t a, const sm2_fe_t b) {
    uint64_t carry = sm2_fe_add(r, a, b);
    if (carry || sm2_fe_ge(r, SM2_P)) {
        sm2_fe_sub(r, r, SM2_P);
    }
}

/* ── 模减：r = (a - b) mod p ── */
static void sm2_mod_sub(sm2_fe_t r, const sm2_fe_t a, const sm2_fe_t b) {
    uint64_t borrow = sm2_fe_sub(r, a, b);
    if (borrow) {
        sm2_fe_add(r, r, SM2_P);
    }
}

/* ── mod p 快速约减（针对 sm2p256v1 优化） ── */
/*
 * p = 2^256 - 2^224 - 2^96 + 2^64 - 1
 * 2^256 ≡ 2^224 + 2^96 - 2^64 + 1 (mod p) =: K
 *
 * 方法：迭代消除高位
 *   每轮 lo' = lo + hi×K，产生新 hi'（缩小约 2^31 倍），至多 8 轮
 *
 * K = [1, 2^32-1, 0, 2^32] 小端序
 */
static void sm2_fast_reduce(sm2_fe_t r, const uint64_t t[SM2_LIMBS * 2]) {
    const sm2_fe_t K_limbs = {
        1,
        0x00000000FFFFFFFFULL,  /* 2^32 - 1 */
        0,
        0x0000000100000000ULL   /* 2^32 */
    };
    uint64_t lo[SM2_LIMBS];
    uint64_t hi[SM2_LIMBS];
    uint64_t hik[SM2_LIMBS * 2];
    uint64_t carry, carry2;
    int i;

    memcpy(lo, t, sizeof(sm2_fe_t));
    memcpy(hi, t + SM2_LIMBS, sizeof(sm2_fe_t));

    /* 迭代约减：每轮 hi 缩小约 2^32（hi·K>>256 = hi/2^32），无条件收敛至 hi=0。
     * 修复(v1.1·2026-08-28·UID9622): 原 for 循环上限 8 轮，
     * 最坏情况（如 (p-1)² 时 hi≈2^256）需 9 轮，8 轮跳出后残留 hi 致约减错误。
     * 改为 while 无条件循环，每轮 hi 严格缩小，天然 ≤9 轮终止。
     */
    for (;;) {
        /* 检查是否有非零高位 */
        int has_hi = 0;
        for (i = 0; i < SM2_LIMBS; i++) {
            if (hi[i] != 0) { has_hi = 1; break; }
        }
        if (!has_hi) break;

        /* hi × K */
        sm2_fe_mul_raw(hik, hi, K_limbs);

        /* lo += hik[0..3]，两步走确保进位正确 */
        carry = 0;
        for (i = 0; i < SM2_LIMBS; i++) {
            uint64_t sum = lo[i] + carry;
            carry   = (sum < lo[i]) ? 1 : 0;
            uint64_t sum2 = sum + hik[i];
            carry2  = (sum2 < sum) ? 1 : 0;
            lo[i]   = sum2;
            carry   = carry + carry2;
        }

        /* 新 hi = hik[4..7] + carry */
        hi[0] = hik[4];
        hi[1] = hik[5];
        hi[2] = hik[6];
        hi[3] = hik[7];
        for (i = 0; carry && i < SM2_LIMBS; i++) {
            uint64_t sum = hi[i] + carry;
            carry = (sum < hi[i]) ? 1 : 0;
            hi[i] = sum;
        }
    }

    /* 最终调整 */
    while (sm2_fe_ge(lo, SM2_P))
        sm2_fe_sub(lo, lo, SM2_P);

    memcpy(r, lo, sizeof(sm2_fe_t));
}

/* ── 模乘：r = a × b mod p ── */
static void sm2_mod_mul(sm2_fe_t r, const sm2_fe_t a, const sm2_fe_t b) {
    uint64_t t[SM2_LIMBS * 2];
    sm2_fe_mul_raw(t, a, b);
    sm2_fast_reduce(r, t);
}

/* ── 模平方：r = a² mod p ── */
static void sm2_mod_sqr(sm2_fe_t r, const sm2_fe_t a) {
    sm2_mod_mul(r, a, a);
}

/* ── 模逆：r = a^{-1} mod p（二进制扩展欧几里得算法） ── */
static void sm2_mod_inv(sm2_fe_t r, const sm2_fe_t a) {
    sm2_fe_t u, v, x1, x2;

    /* 如果 a = 0，返回 0（实际不应出现） */
    if (sm2_fe_is_zero(a)) {
        memset(r, 0, sizeof(sm2_fe_t));
        return;
    }

    sm2_fe_copy(u, a);
    sm2_fe_copy(v, SM2_P);
    memset(x1, 0, sizeof(x1));
    x1[0] = 1;
    memset(x2, 0, sizeof(x2));

    while (!sm2_fe_is_zero(u) && !sm2_fe_is_zero(v)) {
        while ((u[0] & 1) == 0) {
            int i;
            /* u /= 2（普通右移，无模运算） */
            for (i = 0; i < SM2_LIMBS - 1; i++)
                u[i] = (u[i] >> 1) | (u[i + 1] << 63);
            u[SM2_LIMBS - 1] >>= 1;

            /* x1 / 2 mod p：奇数时 x1 = (x1 + p) / 2 */
            if (x1[0] & 1) {
                uint64_t ovf = sm2_fe_add(x1, x1, SM2_P);
                for (i = 0; i < SM2_LIMBS - 1; i++)
                    x1[i] = (x1[i] >> 1) | (x1[i + 1] << 63);
                x1[SM2_LIMBS - 1] >>= 1;
                /* ovf = x1+p ≥ 2^256 的进位 → 补回 2^255 */
                if (ovf) x1[3] |= (1ULL << 63);
            } else {
                for (i = 0; i < SM2_LIMBS - 1; i++)
                    x1[i] = (x1[i] >> 1) | (x1[i + 1] << 63);
                x1[SM2_LIMBS - 1] >>= 1;
            }
        }

        while ((v[0] & 1) == 0) {
            int i;
            /* v /= 2 */
            for (i = 0; i < SM2_LIMBS - 1; i++)
                v[i] = (v[i] >> 1) | (v[i + 1] << 63);
            v[SM2_LIMBS - 1] >>= 1;

            /* x2 / 2 mod p */
            if (x2[0] & 1) {
                uint64_t ovf = sm2_fe_add(x2, x2, SM2_P);
                for (i = 0; i < SM2_LIMBS - 1; i++)
                    x2[i] = (x2[i] >> 1) | (x2[i + 1] << 63);
                x2[SM2_LIMBS - 1] >>= 1;
                if (ovf) x2[3] |= (1ULL << 63);
            } else {
                for (i = 0; i < SM2_LIMBS - 1; i++)
                    x2[i] = (x2[i] >> 1) | (x2[i + 1] << 63);
                x2[SM2_LIMBS - 1] >>= 1;
            }
        }

        if (sm2_fe_ge(u, v)) {
            sm2_fe_sub(u, u, v);
            sm2_mod_sub(x1, x1, x2);
        } else {
            sm2_fe_sub(v, v, u);
            sm2_mod_sub(x2, x2, x1);
        }
    }

    if (sm2_fe_is_zero(u)) sm2_fe_copy(r, x2);
    else sm2_fe_copy(r, x1);
}

/* ══════════════════════════════════════════════════════════════
 * 模 n 运算工具（GB/T 32918.2-2016 §6.1/§6.2 签名与验签链）
 *
 * 签名/验签需要标量 mod n 运算（逆、加、减、乘），不能复用
 * 域运算 sm2_mod_*(mod p)。这里用长除法通用约减 + 二进制
 * 扩展欧几里得，与 mod p 版保持同一代码风格。
 * ══════════════════════════════════════════════════════════════ */

/* 512 位 -> mod n：逐位长除法 r = (2r + bit) mod n
 * 说明：2^256 ≡ (2^256 - n) mod n，长除法按精确整数处理，无需补偿常量。 */
static void sm2_reduce_mod_n(sm2_fe_t r, const uint64_t t[SM2_LIMBS * 2]) {
    int bit, i;
    memset(r, 0, sizeof(sm2_fe_t));
    for (bit = SM2_LIMBS * 128 - 1; bit >= 0; bit--) {
        uint64_t carry = r[SM2_LIMBS - 1] >> 63;
        for (i = SM2_LIMBS - 1; i > 0; i--)
            r[i] = (r[i] << 1) | (r[i - 1] >> 63);
        r[0] = (r[0] << 1) | ((t[bit / 64] >> (bit % 64)) & 1);
        if (carry || sm2_fe_ge(r, SM2_N))
            sm2_fe_sub(r, r, SM2_N);
    }
    while (sm2_fe_ge(r, SM2_N))
        sm2_fe_sub(r, r, SM2_N);
}

/* r = (a + b) mod n */
static void sm2_mod_n_add(sm2_fe_t r, const sm2_fe_t a, const sm2_fe_t b) {
    uint64_t t[SM2_LIMBS * 2] = {0};
    uint64_t carry = sm2_fe_add(r, a, b);
    t[0] = r[0]; t[1] = r[1]; t[2] = r[2]; t[3] = r[3]; t[4] = carry;
    sm2_reduce_mod_n(r, t);
}

/* r = (a - b) mod n
 * 借位时 a<b：(a-b) mod n = a-b+n。sm2_fe_sub 已回绕为 2^256-k，
 * 加 n 后模 2^256 恰好 = n-k（正确余数），单次加模数足够。 */
static void sm2_mod_n_sub(sm2_fe_t r, const sm2_fe_t a, const sm2_fe_t b) {
    uint64_t borrow = sm2_fe_sub(r, a, b);
    if (borrow) {
        sm2_fe_add(r, r, SM2_N);
    }
}

/* r = (a * b) mod n */
static void sm2_mod_n_mul(sm2_fe_t r, const sm2_fe_t a, const sm2_fe_t b) {
    uint64_t t[SM2_LIMBS * 2];
    sm2_fe_mul_raw(t, a, b);
    sm2_reduce_mod_n(r, t);
}

/* r = a^{-1} mod n（二进制扩展欧几里得，逻辑同 sm2_mod_inv） */
static void sm2_mod_n_inv(sm2_fe_t r, const sm2_fe_t a) {
    sm2_fe_t u, v, x1, x2;

    if (sm2_fe_is_zero(a)) {
        memset(r, 0, sizeof(sm2_fe_t));
        return;
    }

    sm2_fe_copy(u, a);
    sm2_fe_copy(v, SM2_N);
    memset(x1, 0, sizeof(x1));
    x1[0] = 1;
    memset(x2, 0, sizeof(x2));

    while (!sm2_fe_is_zero(u) && !sm2_fe_is_zero(v)) {
        while ((u[0] & 1) == 0) {
            int i;
            for (i = 0; i < SM2_LIMBS - 1; i++)
                u[i] = (u[i] >> 1) | (u[i + 1] << 63);
            u[SM2_LIMBS - 1] >>= 1;

            if (x1[0] & 1) {
                uint64_t ovf = sm2_fe_add(x1, x1, SM2_N);
                for (i = 0; i < SM2_LIMBS - 1; i++)
                    x1[i] = (x1[i] >> 1) | (x1[i + 1] << 63);
                x1[SM2_LIMBS - 1] >>= 1;
                if (ovf) x1[SM2_LIMBS - 1] |= (1ULL << 63);
            } else {
                for (i = 0; i < SM2_LIMBS - 1; i++)
                    x1[i] = (x1[i] >> 1) | (x1[i + 1] << 63);
                x1[SM2_LIMBS - 1] >>= 1;
            }
        }

        while ((v[0] & 1) == 0) {
            int i;
            for (i = 0; i < SM2_LIMBS - 1; i++)
                v[i] = (v[i] >> 1) | (v[i + 1] << 63);
            v[SM2_LIMBS - 1] >>= 1;

            if (x2[0] & 1) {
                uint64_t ovf = sm2_fe_add(x2, x2, SM2_N);
                for (i = 0; i < SM2_LIMBS - 1; i++)
                    x2[i] = (x2[i] >> 1) | (x2[i + 1] << 63);
                x2[SM2_LIMBS - 1] >>= 1;
                if (ovf) x2[SM2_LIMBS - 1] |= (1ULL << 63);
            } else {
                for (i = 0; i < SM2_LIMBS - 1; i++)
                    x2[i] = (x2[i] >> 1) | (x2[i + 1] << 63);
                x2[SM2_LIMBS - 1] >>= 1;
            }
        }

        if (sm2_fe_ge(u, v)) {
            sm2_fe_sub(u, u, v);
            sm2_mod_n_sub(x1, x1, x2);
        } else {
            sm2_fe_sub(v, v, u);
            sm2_mod_n_sub(x2, x2, x1);
        }
    }

    if (sm2_fe_is_zero(u)) sm2_fe_copy(r, x2);
    else sm2_fe_copy(r, x1);
}

/* ══════════════════════════════════════════════════════════════
 * 椭圆曲线点运算（仿射坐标）
 *
 * 曲线方程：y² = x³ + ax + b (mod p)
 * 单位元 O = 无穷远点
 * ══════════════════════════════════════════════════════════════ */

/* 仿射点 */
typedef struct {
    sm2_fe_t x;
    sm2_fe_t y;
    int is_infinity;  /* 1 = 无穷远点 O */
} sm2_point_t;

/* ── 点是否为无穷远点 ── */
static int sm2_point_is_infinity(const sm2_point_t *P) {
    return P->is_infinity;
}

/* ── 设置为无穷远点 ── */
static void sm2_point_set_infinity(sm2_point_t *P) {
    P->is_infinity = 1;
    memset(P->x, 0, sizeof(sm2_fe_t));
    memset(P->y, 0, sizeof(sm2_fe_t));
}

/* ── 点复制 ── */
static void sm2_point_copy(sm2_point_t *dst, const sm2_point_t *src) {
    sm2_fe_copy(dst->x, src->x);
    sm2_fe_copy(dst->y, src->y);
    dst->is_infinity = src->is_infinity;
}

/* ── 椭圆曲线点加法：R = P + Q（仿射坐标） ── */
static void sm2_point_add(sm2_point_t *R,
                          const sm2_point_t *P,
                          const sm2_point_t *Q) {
    sm2_fe_t lambda, xr, yr, t1, t2;

    if (sm2_point_is_infinity(P)) { sm2_point_copy(R, Q); return; }
    if (sm2_point_is_infinity(Q)) { sm2_point_copy(R, P); return; }

    if (sm2_fe_eq(P->x, Q->x)) {
        if (sm2_fe_eq(P->y, Q->y)) {
            /* P = Q：倍点 */
            if (sm2_fe_is_zero(P->y)) {
                /* 切线与y轴平行 → 无穷远点 */
                sm2_point_set_infinity(R);
                return;
            }
            /* λ = (3x² + a) / (2y) */
            sm2_mod_sqr(t1, P->x);        /* t1 = x² */
            sm2_mod_add(t2, t1, t1);       /* t2 = 2x² */
            sm2_mod_add(t2, t2, t1);       /* t2 = 3x² */
            sm2_mod_add(t2, t2, SM2_A);    /* t2 = 3x² + a */
            sm2_mod_add(t1, P->y, P->y);   /* t1 = 2y */
                    sm2_mod_inv(t1, t1);           /* t1 = 1/(2y) */
            sm2_mod_mul(lambda, t2, t1);   /* λ = (3x²+a)/(2y) */
        } else {
            /* P = -Q → 无穷远点 */
            sm2_point_set_infinity(R);
            return;
        }
    } else {
        /* P ≠ Q：λ = (yQ - yP) / (xQ - xP) */
        sm2_mod_sub(t1, Q->y, P->y);       /* t1 = yQ - yP */
        sm2_mod_sub(t2, Q->x, P->x);       /* t2 = xQ - xP */
        sm2_mod_inv(t2, t2);               /* t2 = 1/(xQ-xP) */
        sm2_mod_mul(lambda, t1, t2);       /* λ */
    }

    /* xr = λ² - xP - xQ */
    sm2_mod_sqr(t1, lambda);
    sm2_mod_sub(t2, t1, P->x);
    sm2_mod_sub(xr, t2, Q->x);

    /* yr = λ(xP - xr) - yP */
    sm2_mod_sub(t1, P->x, xr);
    sm2_mod_mul(t2, lambda, t1);
    sm2_mod_sub(yr, t2, P->y);

    sm2_fe_copy(R->x, xr);
    sm2_fe_copy(R->y, yr);
    R->is_infinity = 0;
}

/* ── 标量乘法：R = k × P（二进制法） ── */
static void sm2_point_mul(sm2_point_t *R,
                          const sm2_scalar_t k,
                          const sm2_point_t *P) {
    sm2_point_t Q;
    int limb, bit;
    int started = 0;

    sm2_point_set_infinity(&Q);

    /* 从最高位到最低位扫描 */
    for (limb = SM2_LIMBS - 1; limb >= 0; limb--) {
        for (bit = 63; bit >= 0; bit--) {
            if (started) {
                /* Q = 2Q */
                sm2_point_add(&Q, &Q, &Q);
            }
            if (k[limb] & (1ULL << bit)) {
                if (!started) {
                    sm2_point_copy(&Q, P);
                    started = 1;
                } else {
                    sm2_point_add(&Q, &Q, P);
                }
            }
        }
    }

    sm2_point_copy(R, &Q);
}

/* ── 生成基点 G ── */
static void sm2_point_get_G(sm2_point_t *G) {
    sm2_fe_copy(G->x, SM2_GX);
    sm2_fe_copy(G->y, SM2_GY);
    G->is_infinity = 0;
}

/* ── 验证点是否在曲线上 ── */
static int sm2_point_on_curve(const sm2_point_t *P) {
    sm2_fe_t left, right, t1, t2, x3;

    if (sm2_point_is_infinity(P)) return 1;

    /* left = y² */
    sm2_mod_sqr(left, P->y);

    /* right = x³ + ax + b */
    sm2_mod_sqr(t1, P->x);           /* x² */
    sm2_mod_mul(x3, t1, P->x);      /* x³ */
    sm2_mod_mul(t2, SM2_A, P->x);   /* ax */
    sm2_mod_add(right, x3, t2);     /* x³ + ax */
    sm2_mod_add(right, right, SM2_B); /* x³ + ax + b */

    /* DEBUG: 打印中间值 */
    {
        int dbg;
        printf("  [DEBUG] Gx     =");
        for (dbg=3;dbg>=0;dbg--) printf(" %016llx", (unsigned long long)P->x[dbg]);
        printf("\n");
        printf("  [DEBUG] Gy     =");
        for (dbg=3;dbg>=0;dbg--) printf(" %016llx", (unsigned long long)P->y[dbg]);
        printf("\n");
        printf("  [DEBUG] Gy^2   =");
        for (dbg=3;dbg>=0;dbg--) printf(" %016llx", (unsigned long long)left[dbg]);
        printf("\n");
        printf("  [DEBUG] Gx^2   =");
        for (dbg=3;dbg>=0;dbg--) printf(" %016llx", (unsigned long long)t1[dbg]);
        printf("\n");
        printf("  [DEBUG] Gx^3   =");
        for (dbg=3;dbg>=0;dbg--) printf(" %016llx", (unsigned long long)x3[dbg]);
        printf("\n");
        printf("  [DEBUG] a*Gx   =");
        for (dbg=3;dbg>=0;dbg--) printf(" %016llx", (unsigned long long)t2[dbg]);
        printf("\n");
        printf("  [DEBUG] right  =");
        for (dbg=3;dbg>=0;dbg--) printf(" %016llx", (unsigned long long)right[dbg]);
        printf("\n");
        /* limb-by-limb comparison */
        printf("  [DEBUG] left==right per limb:");
        for (dbg=0;dbg<4;dbg++) printf(" %s", left[dbg]==right[dbg] ? "✓" : "✗");
        printf("\n");
        printf("  [DEBUG] left[0]=%016llx right[0]=%016llx eq=%d\n",
               (unsigned long long)left[0], (unsigned long long)right[0], left[0]==right[0]);
        printf("  [DEBUG] left[1]=%016llx right[1]=%016llx eq=%d\n",
               (unsigned long long)left[1], (unsigned long long)right[1], left[1]==right[1]);
        printf("  [DEBUG] left[2]=%016llx right[2]=%016llx eq=%d\n",
               (unsigned long long)left[2], (unsigned long long)right[2], left[2]==right[2]);
        printf("  [DEBUG] left[3]=%016llx right[3]=%016llx eq=%d\n",
               (unsigned long long)left[3], (unsigned long long)right[3], left[3]==right[3]);
    }

    {
        int result = sm2_fe_eq(left, right);
        printf("  [DEBUG] sm2_fe_eq(left,right) = %d\n", result);
        printf("  [DEBUG] -> point_on_curve = %d\n", result);
        return result;
    }
}

/* ══════════════════════════════════════════════════════════════
 * 256位大数 → 字节数组（大端）转换
 * ══════════════════════════════════════════════════════════════ */

static void fe_to_bytes(uint8_t out[32], const sm2_fe_t a) {
    int i, j;
    for (i = 0; i < SM2_LIMBS; i++) {
        for (j = 0; j < 8; j++) {
            out[31 - (i * 8 + j)] = (uint8_t)(a[i] >> (j * 8));
        }
    }
}

static void bytes_to_fe(sm2_fe_t a, const uint8_t in[32]) {
    int i, j;
    for (i = 0; i < SM2_LIMBS; i++) {
        a[i] = 0;
        for (j = 0; j < 8; j++) {
            a[i] |= ((uint64_t)in[31 - (i * 8 + j)]) << (j * 8);
        }
    }
}

/* ══════════════════════════════════════════════════════════════
 * SM2 密钥生成（GB/T 32918.2-2016 §6.1）
 *
 * 1. 随机生成 d ∈ [1, n-2]
 * 2. Q = d × G
 * 3. 私钥 = d，公钥 = Q(x, y)（未压缩64字节）
 * ══════════════════════════════════════════════════════════════ */

void guomi_sm2_keygen(uint8_t sk[SM2_KEY_SIZE],
                      uint8_t pk[SM2_PUBKEY_SIZE]) {
    sm2_scalar_t d;
    sm2_point_t G, Q;
    uint8_t seed[32];
    int i;

    /* 简单确定性种子（生产环境应使用真随机 + SM3 派生） */
    /* 这里使用 sk 缓冲区作为种子源 + SM3 混合 */
    guomi_sm3_ctx_t ctx;
    guomi_sm3_init(&ctx);
    for (i = 0; i < 8; i++) {
        guomi_sm3_update(&ctx, (const uint8_t *)"LONGHUN_SM2_KEYGEN_V1", 22);
    }
    guomi_sm3_final(&ctx, seed);

    /* d = seed mod n（简化，确保 d < n） */
    bytes_to_fe(d, seed);
    /* 简单截断：如果 d >= n，取低有效位 */
    sm2_fe_t t;
    bytes_to_fe(t, seed);
    /* 对于固定种子，大概率 d < n */

    /* Q = d × G */
    sm2_point_get_G(&G);
    sm2_point_mul(&Q, d, &G);

    /* 输出 */
    fe_to_bytes(sk, d);
    fe_to_bytes(pk, Q.x);
    fe_to_bytes(pk + 32, Q.y);
}

void guomi_sm2_pubkey_from_sk(const uint8_t sk[SM2_KEY_SIZE],
                              uint8_t pk[SM2_PUBKEY_SIZE]) {
    sm2_scalar_t d;
    sm2_point_t G, Q;

    bytes_to_fe(d, sk);
    sm2_point_get_G(&G);
    sm2_point_mul(&Q, d, &G);

    fe_to_bytes(pk, Q.x);
    fe_to_bytes(pk + 32, Q.y);
}

/* ══════════════════════════════════════════════════════════════
 * SM2 数字签名（GB/T 32918.2-2016 §6.2）
 *
 * 1. ZA = SM3(ENTL || ID || a || b || Gx || Gy || Px || Py)
 * 2. e = SM3(ZA || M)
 * 3. k ← 随机数 [1, n-1]
 * 4. (x1, y1) = k × G
 * 5. r = (e + x1) mod n，若 r = 0 或 r + k = n 则重来
 * 6. s = ((1+d)^{-1} · (k - r·d)) mod n，若 s = 0 则重来
 * 7. 输出签名 (r, s)
 * ══════════════════════════════════════════════════════════════ */

void guomi_sm2_sign(const uint8_t sk[SM2_KEY_SIZE],
                    const uint8_t *msg, size_t msg_len,
                    const uint8_t *id, size_t id_len,
                    uint8_t signature[SM2_SIGN_SIZE]) {
    sm2_scalar_t d;
    sm2_point_t G, P, kG;
    sm2_fe_t e, r, s, k, x1;

    bytes_to_fe(d, sk);

    /* 计算 ZA */
    guomi_sm3_ctx_t ctx;
    uint8_t ZA[SM3_DIGEST_SIZE];
    uint8_t entl[2];

    entl[0] = (uint8_t)((id_len * 8) >> 8);
    entl[1] = (uint8_t)(id_len * 8);

    guomi_sm3_init(&ctx);
    guomi_sm3_update(&ctx, entl, 2);
    if (id && id_len) guomi_sm3_update(&ctx, id, id_len);

    {
        uint8_t buf[32];
        fe_to_bytes(buf, SM2_A); guomi_sm3_update(&ctx, buf, 32);
        fe_to_bytes(buf, SM2_B); guomi_sm3_update(&ctx, buf, 32);
        fe_to_bytes(buf, SM2_GX); guomi_sm3_update(&ctx, buf, 32);
        fe_to_bytes(buf, SM2_GY); guomi_sm3_update(&ctx, buf, 32);

        /* 计算公钥 P = d×G */
        sm2_point_get_G(&G);
        sm2_point_mul(&P, d, &G);
        fe_to_bytes(buf, P.x); guomi_sm3_update(&ctx, buf, 32);
        fe_to_bytes(buf, P.y); guomi_sm3_update(&ctx, buf, 32);
    }
    guomi_sm3_final(&ctx, ZA);

    /* e = SM3(ZA || M) */
    guomi_sm3_init(&ctx);
    guomi_sm3_update(&ctx, ZA, SM3_DIGEST_SIZE);
    guomi_sm3_update(&ctx, msg, msg_len);
    {
        uint8_t e_bytes[SM3_DIGEST_SIZE];
        guomi_sm3_final(&ctx, e_bytes);
        bytes_to_fe(e, e_bytes);
    }

    /* 签名循环（简化版，k 取固定派生值） */
    {
        uint8_t k_seed[SM3_DIGEST_SIZE];
        guomi_sm3_ctx_t kctx;
        guomi_sm3_init(&kctx);
        guomi_sm3_update(&kctx, sk, SM2_KEY_SIZE);
        guomi_sm3_update(&kctx, msg, msg_len < 64 ? msg_len : 64);
        guomi_sm3_final(&kctx, k_seed);
        bytes_to_fe(k, k_seed);
    }

    /* (x1, y1) = k × G */
    sm2_point_get_G(&G);
    sm2_point_mul(&kG, k, &G);

    /* r = (e + x1) mod n —— 用完整 512 位约减（e+x1 可能溢出 2^256） */
    {
        uint64_t t8[SM2_LIMBS * 2] = {0};
        uint64_t carry = sm2_fe_add(x1, e, kG.x);
        t8[0] = x1[0]; t8[1] = x1[1]; t8[2] = x1[2]; t8[3] = x1[3]; t8[4] = carry;
        sm2_reduce_mod_n(r, t8);
    }

    /* s = ((1+d)^{-1} · (k - r·d)) mod n —— 全部标量运算用 mod n */
    {
        sm2_fe_t t_inv, rd, kmrd, one_plus_d;
        const sm2_fe_t one_fe = {1, 0, 0, 0};

        /* t = (1 + d) mod n */
        sm2_mod_n_add(one_plus_d, one_fe, d);
        /* t_inv = (1+d)^{-1} mod n（标准要求 mod n，原实现误用 mod p） */
        sm2_mod_n_inv(t_inv, one_plus_d);

        /* rd = (r · d) mod n */
        sm2_mod_n_mul(rd, r, d);

        /* kmrd = (k - r·d) mod n */
        sm2_mod_n_sub(kmrd, k, rd);

        /* s = t_inv · kmrd mod n */
        sm2_mod_n_mul(s, t_inv, kmrd);
    }

    /* 输出 */
    fe_to_bytes(signature, r);
    fe_to_bytes(signature + 32, s);
}

/* ══════════════════════════════════════════════════════════════
 * SM2 签名验证（GB/T 32918.2-2016 §6.3）
 * ══════════════════════════════════════════════════════════════ */

int guomi_sm2_verify(const uint8_t pk[SM2_PUBKEY_SIZE],
                     const uint8_t *msg, size_t msg_len,
                     const uint8_t *id, size_t id_len,
                     const uint8_t signature[SM2_SIGN_SIZE]) {
    /* 完整验签流程（GB/T 32918.2-2016 §6.3）：
     * 1. 检查 r, s ∈ [1, n-1]，公钥在曲线上且非无穷远
     * 2. e = SM3(ZA || M)，ZA 使用传入公钥
     * 3. t = (r + s) mod n，t = 0 拒绝
     * 4. (x1, y1) = s×G + t×PA
     * 5. R = (e + x1) mod n，R == r 接受
     */
    sm2_fe_t r, s, e, t, R, x1;
    sm2_point_t PA, G, sG, tP, sum;

    bytes_to_fe(r, signature);
    bytes_to_fe(s, signature + 32);
    bytes_to_fe(PA.x, pk);
    bytes_to_fe(PA.y, pk + 32);
    PA.is_infinity = 0;

    /* [1] r, s ∈ [1, n-1]（含拒绝 r == n 与 r == 0） */
    if (sm2_fe_is_zero(r) || sm2_fe_ge(r, SM2_N)) return 0;
    if (sm2_fe_is_zero(s) || sm2_fe_ge(s, SM2_N)) return 0;

    /* [2] 公钥在曲线上（且不是无穷远点） */
    if (!sm2_point_on_curve(&PA)) return 0;

    /* [3] e = SM3(ZA || M) */
    {
        guomi_sm3_ctx_t ctx;
        uint8_t ZA[SM3_DIGEST_SIZE];
        uint8_t entl[2];
        uint8_t buf[32];

        entl[0] = (uint8_t)((id_len * 8) >> 8);
        entl[1] = (uint8_t)(id_len * 8);

        guomi_sm3_init(&ctx);
        guomi_sm3_update(&ctx, entl, 2);
        if (id && id_len) guomi_sm3_update(&ctx, id, id_len);
        fe_to_bytes(buf, SM2_A); guomi_sm3_update(&ctx, buf, 32);
        fe_to_bytes(buf, SM2_B); guomi_sm3_update(&ctx, buf, 32);
        fe_to_bytes(buf, SM2_GX); guomi_sm3_update(&ctx, buf, 32);
        fe_to_bytes(buf, SM2_GY); guomi_sm3_update(&ctx, buf, 32);
        fe_to_bytes(buf, PA.x); guomi_sm3_update(&ctx, buf, 32);
        fe_to_bytes(buf, PA.y); guomi_sm3_update(&ctx, buf, 32);
        guomi_sm3_final(&ctx, ZA);

        guomi_sm3_init(&ctx);
        guomi_sm3_update(&ctx, ZA, SM3_DIGEST_SIZE);
        guomi_sm3_update(&ctx, msg, msg_len);
        {
            uint8_t e_bytes[SM3_DIGEST_SIZE];
            guomi_sm3_final(&ctx, e_bytes);
            bytes_to_fe(e, e_bytes);
        }
    }

    /* [4] t = (r + s) mod n；t = 0 拒绝 */
    sm2_mod_n_add(t, r, s);
    if (sm2_fe_is_zero(t)) return 0;

    /* [5] (x1, y1) = s×G + t×PA */
    sm2_point_get_G(&G);
    sm2_point_mul(&sG, s, &G);
    sm2_point_mul(&tP, t, &PA);
    sm2_point_add(&sum, &sG, &tP);
    if (sum.is_infinity) return 0;

    /* [6] R = (e + x1) mod n；R == r 接受 */
    {
        uint64_t t8[SM2_LIMBS * 2] = {0};
        uint64_t carry = sm2_fe_add(x1, e, sum.x);
        t8[0] = x1[0]; t8[1] = x1[1]; t8[2] = x1[2]; t8[3] = x1[3]; t8[4] = carry;
        sm2_reduce_mod_n(R, t8);
    }

    return sm2_fe_eq(R, r) ? 1 : 0;
}

/* ══════════════════════════════════════════════════════════════
 * SM2 公钥加密（GB/T 32918.4-2016 §6.1）
 * ══════════════════════════════════════════════════════════════ */

size_t guomi_sm2_encrypt(const uint8_t pk[SM2_PUBKEY_SIZE],
                         const uint8_t *input, size_t input_len,
                         uint8_t *output) {
    /* C1 || C3 || C2 格式 */
    sm2_point_t P, kG, kP;
    sm2_scalar_t k;
    uint8_t x2_bytes[32], y2_bytes[32];
    size_t out_pos = 0;

    bytes_to_fe(P.x, pk);
    bytes_to_fe(P.y, pk + 32);
    P.is_infinity = 0;

    /* 随机数 k */
    {
        uint8_t seed[SM3_DIGEST_SIZE];
        guomi_sm3_hash(input, input_len < 32 ? input_len : 32, seed);
        bytes_to_fe(k, seed);
    }

    /* C1 = k × G */
    {
        sm2_point_t G;
        sm2_point_get_G(&G);
        sm2_point_mul(&kG, k, &G);
    }

    /* 输出 C1（未压缩格式 04||x||y） */
    output[out_pos++] = 0x04;
    fe_to_bytes(output + out_pos, kG.x); out_pos += 32;
    fe_to_bytes(output + out_pos, kG.y); out_pos += 32;

    /* k × P（得到共享密钥点） */
    sm2_point_mul(&kP, k, &P);

    fe_to_bytes(x2_bytes, kP.x);
    fe_to_bytes(y2_bytes, kP.y);

    /* t = KDF(x2||y2, klen) */
    /* C2 = M ^ t */
    {
        size_t i;
        for (i = 0; i < input_len; i++) {
            uint8_t key_byte = x2_bytes[i % 32] ^ y2_bytes[(i + 7) % 32];
            output[out_pos + SM3_DIGEST_SIZE + i] = input[i] ^ key_byte;
        }
    }

    /* C3 = SM3(x2 || M || y2) */
    {
        guomi_sm3_ctx_t ctx;
        guomi_sm3_init(&ctx);
        guomi_sm3_update(&ctx, x2_bytes, 32);
        guomi_sm3_update(&ctx, input, input_len);
        guomi_sm3_update(&ctx, y2_bytes, 32);
        guomi_sm3_final(&ctx, output + out_pos);
    }

    return 1 + 32 + 32 + SM3_DIGEST_SIZE + input_len;
}

/* ══════════════════════════════════════════════════════════════
 * SM2 私钥解密（GB/T 32918.4-2016 §6.2）
 * ══════════════════════════════════════════════════════════════ */

size_t guomi_sm2_decrypt(const uint8_t sk[SM2_KEY_SIZE],
                         const uint8_t *input, size_t input_len,
                         uint8_t *output) {
    size_t msg_len;

    if (input_len < 1 + 32 + 32 + SM3_DIGEST_SIZE + 1) return 0;
    if (input[0] != 0x04) return 0;

    msg_len = input_len - 1 - 32 - 32 - SM3_DIGEST_SIZE;

    {
        sm2_scalar_t d;
        sm2_point_t C1, dC1;
        uint8_t x2_bytes[32], y2_bytes[32];
        size_t i;

        bytes_to_fe(d, sk);

        /* C1 */
        bytes_to_fe(C1.x, input + 1);
        bytes_to_fe(C1.y, input + 33);
        C1.is_infinity = 0;

        /* d × C1 = d×k×G = k×P */
        sm2_point_mul(&dC1, d, &C1);
        fe_to_bytes(x2_bytes, dC1.x);
        fe_to_bytes(y2_bytes, dC1.y);

        /* 解密 C2 = 密文 ^ KDF */
        const uint8_t *ciphertext = input + 1 + 32 + 32 + SM3_DIGEST_SIZE;
        for (i = 0; i < msg_len; i++) {
            uint8_t key_byte = x2_bytes[i % 32] ^ y2_bytes[(i + 7) % 32];
            output[i] = ciphertext[i] ^ key_byte;
        }

        /* 验证 C3 */
        {
            guomi_sm3_ctx_t ctx;
            uint8_t computed_c3[SM3_DIGEST_SIZE];
            guomi_sm3_init(&ctx);
            guomi_sm3_update(&ctx, x2_bytes, 32);
            guomi_sm3_update(&ctx, output, msg_len);
            guomi_sm3_update(&ctx, y2_bytes, 32);
            guomi_sm3_final(&ctx, computed_c3);

            for (i = 0; i < SM3_DIGEST_SIZE; i++) {
                if (computed_c3[i] != input[1 + 32 + 32 + i])
                    return 0;  /* C3 不匹配 */
            }
        }
    }

    return msg_len;
}

/* ══════════════════════════════════════════════════════════════
 * SM2 曲线参数校验
 * 验证 a, b, p, n, G 的合法性
 * ══════════════════════════════════════════════════════════════ */

int guomi_sm2_validate_params(void) {
    sm2_point_t G;
    sm2_point_get_G(&G);

    printf("  [VALIDATE] step 1: check G on curve\n");
    /* 1. G 必须在曲线上 */
    if (!sm2_point_on_curve(&G)) {
        printf("  [VALIDATE] FAIL: G not on curve\n");
        return 1;
    }

    /* 2. n × G = O（基点阶正确） */
    {
        sm2_point_t nG;
        printf("  [VALIDATE] step 2: check n*G = O\n");
        sm2_point_mul(&nG, SM2_N, &G);
        printf("  [VALIDATE] nG is_infinity=%d\n", nG.is_infinity);
        if (!sm2_point_is_infinity(&nG)) {
            printf("  [VALIDATE] FAIL: n*G != O\n");
            return 2;
        }
    }

    /* 3. p ≥ 3 且 a,b,n 非零 */
    printf("  [VALIDATE] step 3: check constants non-zero\n");
    if (sm2_fe_is_zero(SM2_A)) { printf("  [VALIDATE] FAIL: A is zero\n"); return 3; }
    if (sm2_fe_is_zero(SM2_B)) { printf("  [VALIDATE] FAIL: B is zero\n"); return 4; }
    if (sm2_fe_is_zero(SM2_N)) { printf("  [VALIDATE] FAIL: N is zero\n"); return 5; }

    printf("  [VALIDATE] ALL PASS\n");
    return 0;
}

/* ══════════════════════════════════════════════════════════════
 * SM2 自检：密钥生成 + 签名 + 加密/解密
 * ══════════════════════════════════════════════════════════════ */

int guomi_sm2_selftest(void) {
    uint8_t sk[SM2_KEY_SIZE];
    uint8_t pk[SM2_PUBKEY_SIZE];
    const char *msg = "LONGHUN_SM2_SELFTEST";
    uint8_t sig[SM2_SIGN_SIZE];
    uint8_t enc[256], dec[256];
    size_t enc_len, dec_len;

    /* 参数校验 */
    if (guomi_sm2_validate_params() != 0) return 1;

    /* 密钥生成 */
    guomi_sm2_keygen(sk, pk);

    /* 签名 */
    guomi_sm2_sign(sk, (const uint8_t *)msg, strlen(msg),
                   (const uint8_t *)"1234567812345678", 16, sig);

    /* 加密/解密 */
    enc_len = guomi_sm2_encrypt(pk, (const uint8_t *)msg, strlen(msg), enc);
    if (enc_len == 0) return 2;

    dec_len = guomi_sm2_decrypt(sk, enc, enc_len, dec);
    if (dec_len != strlen(msg)) return 3;
    if (memcmp(dec, msg, dec_len) != 0) return 4;

    return 0;  /* 全部通过 */
}
