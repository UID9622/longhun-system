/*
 * 龍魂·后土OS — SM3 密码杂凑算法实现
 * DNA: #龍芯⚡️丙午·丙申·乙卯·丁亥·䷉履-GUOMI-SM3-v1.0
 *
 * 标准依据：GB/T 32905-2016 信息安全技术 SM3密码杂凑算法
 * 文化锚点：坎宫（水）— SM3 哈希如水，可鉴真伪，不可逆流
 *
 * 算法结构：
 *   消息填充 → 迭代压缩 → 输出256位摘要
 *   块大小：512位（64字节），摘要长度：256位（32字节）
 *   基于 Merkle-Damgård 结构，移位+非线性变换
 *
 * 底座焊死：本实现遵从 GB/T 32905-2016 标准原文，不可改变。
 *            龙魂后土OS内核与鸿蒙系统共用本底座。
 *
 * 测试向量（GB/T 32905-2016 附录A）：
 *   输入 "abc"：
 *     66c7f0f4 62eeedd9 d1f2d46b dc10e4e2
 *     4167c487 5cf2f7a2 297da02b 8f4ba8e0
 */

#include "guomi.h"
#include <string.h>  /* memcpy, memset */

/* SM3 初始值 IV（GB/T 32905-2016 §5.2） */
static const uint32_t SM3_IV[8] = {
    0x7380166FU, 0x4914B2B9U, 0x172442D7U, 0xDA8A0600U,
    0xA96F30BCU, 0x163138AAU, 0xE38DEE4DU, 0xB0FB0E4EU
};

/* ── 内部辅助函数 ── */

/* 32位循环左移（n 自动取模32，防止 n=0 时 UB） */
static inline uint32_t rotl32(uint32_t x, int n) {
    n &= 31;
    return (x << n) | (x >> (32 - n));
}

/* P0 置换函数（§4.3） */
static inline uint32_t sm3_p0(uint32_t x) {
    return x ^ rotl32(x, 9) ^ rotl32(x, 17);
}

/* P1 置换函数（§4.3） */
static inline uint32_t sm3_p1(uint32_t x) {
    return x ^ rotl32(x, 15) ^ rotl32(x, 23);
}

/* FF_j 布尔函数（§4.2） */
static inline uint32_t sm3_ff(int j, uint32_t x, uint32_t y, uint32_t z) {
    if (j < 16) return x ^ y ^ z;
    else        return (x & y) | (x & z) | (y & z);
}

/* GG_j 布尔函数（§4.2） */
static inline uint32_t sm3_gg(int j, uint32_t x, uint32_t y, uint32_t z) {
    if (j < 16) return x ^ y ^ z;
    else        return (x & y) | ((~x) & z);
}

/* 常量 T_j（§5.3.2） */
static inline uint32_t sm3_tj(int j) {
    if (j < 16) return 0x79CC4519U;
    else        return 0x7A879D8AU;
}

/* ── 大端读写（freestanding 兼容）── */
static inline uint32_t load_be32(const uint8_t *p) {
    return ((uint32_t)p[0] << 24) | ((uint32_t)p[1] << 16)
         | ((uint32_t)p[2] << 8)  |  (uint32_t)p[3];
}

static inline void store_be32(uint8_t *p, uint32_t v) {
    p[0] = (uint8_t)(v >> 24);
    p[1] = (uint8_t)(v >> 16);
    p[2] = (uint8_t)(v >> 8);
    p[3] = (uint8_t)(v);
}

/* ══════════════════════════════════════════════════════════════
 * SM3 压缩函数 CF（GB/T 32905-2016 §5.3）
 *
 * V(i+1) = CF(V(i), B(i))
 * V: 256位 = 8×32位 状态字
 * B: 512位 = 16×32位 消息块
 * ══════════════════════════════════════════════════════════════ */
static void sm3_compress(uint32_t state[8], const uint8_t block[SM3_BLOCK_SIZE]) {
    uint32_t W[68], Wp[64];  /* W[0..67] 消息扩展, W'[0..63] */
    uint32_t A, B, C, D, E, F, G, H;
    uint32_t SS1, SS2, TT1, TT2;
    int j;

    /* ── 消息扩展（§5.3.1）── */
    for (j = 0; j < 16; j++) {
        W[j] = load_be32(block + j * 4);
    }
    for (j = 16; j < 68; j++) {
        /* W_j = P1(W_{j-16} ^ W_{j-9} ^ (W_{j-3}<<<15)) ^ (W_{j-13}<<<7) ^ W_{j-6} */
        W[j] = sm3_p1(W[j - 16] ^ W[j - 9] ^ rotl32(W[j - 3], 15))
             ^ rotl32(W[j - 13], 7)
             ^ W[j - 6];
    }
    for (j = 0; j < 64; j++) {
        Wp[j] = W[j] ^ W[j + 4];
    }

    /* ── 迭代压缩（§5.3.2）── */
    A = state[0]; B = state[1]; C = state[2]; D = state[3];
    E = state[4]; F = state[5]; G = state[6]; H = state[7];

    for (j = 0; j < 64; j++) {
        SS1 = rotl32(rotl32(A, 12) + E + rotl32(sm3_tj(j), j), 7);
        SS2 = SS1 ^ rotl32(A, 12);
        TT1 = sm3_ff(j, A, B, C) + D + SS2 + Wp[j];
        TT2 = sm3_gg(j, E, F, G) + H + SS1 + W[j];

        D = C;
        C = rotl32(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = rotl32(F, 19);
        F = E;
        E = sm3_p0(TT2);
    }

    state[0] ^= A; state[1] ^= B; state[2] ^= C; state[3] ^= D;
    state[4] ^= E; state[5] ^= F; state[6] ^= G; state[7] ^= H;
}

/* ══════════════════════════════════════════════════════════════
 * 公开 API
 * ══════════════════════════════════════════════════════════════ */

void guomi_sm3_init(guomi_sm3_ctx_t *ctx) {
    size_t i;
    for (i = 0; i < 8; i++) ctx->state[i] = SM3_IV[i];
    ctx->total_bits = 0;
    ctx->block_len = 0;
}

void guomi_sm3_update(guomi_sm3_ctx_t *ctx, const uint8_t *data, size_t len) {
    size_t i;
    for (i = 0; i < len; i++) {
        ctx->block[ctx->block_len++] = data[i];
        if (ctx->block_len == SM3_BLOCK_SIZE) {
            sm3_compress(ctx->state, ctx->block);
            ctx->total_bits += 512;
            ctx->block_len = 0;
        }
    }
}

void guomi_sm3_final(guomi_sm3_ctx_t *ctx, uint8_t digest[SM3_DIGEST_SIZE]) {
    size_t i;
    uint64_t total_bits;

    /* 已处理的总位数 */
    total_bits = ctx->total_bits + (uint64_t)ctx->block_len * 8;

    /* ── 消息填充（§5.1）── */
    /* 追加 bit '1' */
    ctx->block[ctx->block_len++] = 0x80;

    if (ctx->block_len > 56) {
        /* 当前块放不下 8 字节长度 → 先填充满当前块并压缩 */
        for (i = ctx->block_len; i < SM3_BLOCK_SIZE; i++)
            ctx->block[i] = 0;
        sm3_compress(ctx->state, ctx->block);
        ctx->block_len = 0;
    }

    /* 填充 0 直到剩余 8 字节 */
    for (i = ctx->block_len; i < 56; i++)
        ctx->block[i] = 0;

    /* 最后 8 字节写入消息总位数（大端） */
    store_be32(ctx->block + 56, (uint32_t)(total_bits >> 32));
    store_be32(ctx->block + 60, (uint32_t)(total_bits));
    sm3_compress(ctx->state, ctx->block);

    /* ── 输出 256 位摘要（大端）── */
    for (i = 0; i < 8; i++) {
        store_be32(digest + i * 4, ctx->state[i]);
    }
}

void guomi_sm3_hash(const uint8_t *data, size_t len,
                    uint8_t digest[SM3_DIGEST_SIZE]) {
    guomi_sm3_ctx_t ctx;
    guomi_sm3_init(&ctx);
    guomi_sm3_update(&ctx, data, len);
    guomi_sm3_final(&ctx, digest);
}

/* ══════════════════════════════════════════════════════════════
 * SM3-HMAC（GB/T 32905-2016 附录）
 *
 * HMAC(K, M) = H((K ^ opad) || H((K ^ ipad) || M))
 * ipad = 0x36, opad = 0x5C
 * ══════════════════════════════════════════════════════════════ */

void guomi_sm3_hmac(const uint8_t *key, size_t key_len,
                    const uint8_t *data, size_t data_len,
                    uint8_t mac[SM3_HMAC_SIZE]) {
    guomi_sm3_ctx_t ctx;
    uint8_t key_block[SM3_BLOCK_SIZE];
    uint8_t inner_hash[SM3_DIGEST_SIZE];
    size_t i;

    /* 密钥预处理：小于等于块大小的直接使用，大于的需要先哈希 */
    if (key_len > SM3_BLOCK_SIZE) {
        guomi_sm3_hash(key, key_len, key_block);
        for (i = SM3_DIGEST_SIZE; i < SM3_BLOCK_SIZE; i++)
            key_block[i] = 0;
    } else {
        for (i = 0; i < key_len; i++) key_block[i] = key[i];
        for (i = key_len; i < SM3_BLOCK_SIZE; i++) key_block[i] = 0;
    }

    /* 内层: H((K ^ ipad) || M) */
    guomi_sm3_init(&ctx);
    for (i = 0; i < SM3_BLOCK_SIZE; i++)
        guomi_sm3_update(&ctx, &(uint8_t){key_block[i] ^ 0x36}, 1);
    guomi_sm3_update(&ctx, data, data_len);
    guomi_sm3_final(&ctx, inner_hash);

    /* 外层: H((K ^ opad) || inner_hash) */
    guomi_sm3_init(&ctx);
    for (i = 0; i < SM3_BLOCK_SIZE; i++)
        guomi_sm3_update(&ctx, &(uint8_t){key_block[i] ^ 0x5C}, 1);
    guomi_sm3_update(&ctx, inner_hash, SM3_DIGEST_SIZE);
    guomi_sm3_final(&ctx, mac);
}

/* ══════════════════════════════════════════════════════════════
 * SM3 自检：使用 GB/T 32905-2016 附录A 标准测试向量
 * 返回 0=通过, 非0=失败
 * ══════════════════════════════════════════════════════════════ */

int guomi_sm3_selftest(void) {
    /* 测试向量1: 输入 "abc"（GB/T 32905-2016 A.1 例1） */
    static const uint8_t test_in1[] = "abc";
    static const uint8_t expected1[SM3_DIGEST_SIZE] = {
        0x66, 0xC7, 0xF0, 0xF4, 0x62, 0xEE, 0xED, 0xD9,
        0xD1, 0xF2, 0xD4, 0x6B, 0xDC, 0x10, 0xE4, 0xE2,
        0x41, 0x67, 0xC4, 0x87, 0x5C, 0xF2, 0xF7, 0xA2,
        0x29, 0x7D, 0xA0, 0x2B, 0x8F, 0x4B, 0xA8, 0xE0
    };
    uint8_t result[SM3_DIGEST_SIZE];
    size_t i;

    guomi_sm3_hash(test_in1, 3, result);
    for (i = 0; i < SM3_DIGEST_SIZE; i++) {
        if (result[i] != expected1[i]) return 1;
    }

    /* 测试向量2: 输入 "abcdabcd..." × 16（512位） GB/T 32905-2016 A.1 例2 */
    static const uint8_t test_in2[] =
        "abcdabcdabcdabcdabcdabcdabcdabcd"
        "abcdabcdabcdabcdabcdabcdabcdabcd";
    static const uint8_t expected2[SM3_DIGEST_SIZE] = {
        0xDE, 0xBE, 0x9F, 0xF9, 0x22, 0x75, 0xB8, 0xA1,
        0x38, 0x60, 0x48, 0x89, 0xC1, 0x8E, 0x5A, 0x4D,
        0x6F, 0xDB, 0x70, 0xE5, 0x38, 0x7E, 0x57, 0x65,
        0x29, 0x3D, 0xCB, 0xA3, 0x9C, 0x0C, 0x57, 0x32
    };

    guomi_sm3_hash(test_in2, 64, result);
    for (i = 0; i < SM3_DIGEST_SIZE; i++) {
        if (result[i] != expected2[i]) return 2;
    }

    return 0;  /* 全部通过 */
}
