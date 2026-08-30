归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/*
 * 龍魂·后土OS — SM4 分组密码算法实现
 * DNA: #龍芯⚡️丙午·丙申·乙卯·丁亥·䷉履-GUOMI-SM4-v1.0
 *
 * 标准依据：GB/T 32907-2016 信息安全技术 SM4分组密码算法
 * 文化锚点：兑宫（金）— SM4 加密如金盾，将明文锻造成密文
 *
 * 算法结构：
 *   密钥长度：128位，分组大小：128位，迭代轮数：32轮
 *   非平衡 Feistel 结构，S盒层 + 线性变换层
 *
 * 底座焊死：本实现遵从 GB/T 32907-2016 标准原文，不可改变。
 *            龙魂后土OS内核与鸿蒙系统共用本底座。
 *
 * 测试向量（GB/T 32907-2016 附录A）：
 *   密钥: 0123456789ABCDEFFEDCBA9876543210
 *   明文: 0123456789ABCDEFFEDCBA9876543210
 *   加密(1000000次): 595298C7 C6FD271F 0402F804 C33D3F66
 */

#include "guomi.h"
#include <string.h>

/* ══════════════════════════════════════════════════════════════
 * SM4 S 盒（GB/T 32907-2016 §6.4 表2）
 *
 * 8位输入 → 8位非线性输出
 * 例如 S(0xEF) = 0x18（查表：行 E，列 F）
 * ══════════════════════════════════════════════════════════════ */

static const uint8_t SM4_SBOX[256] = {
    0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7,
    0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05,
    0x2B, 0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3,
    0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
    0x9C, 0x42, 0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A,
    0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62,
    0xE4, 0xB3, 0x1C, 0xA9, 0xC9, 0x08, 0xE8, 0x95,
    0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6,
    0x47, 0x07, 0xA7, 0xFC, 0xF3, 0x73, 0x17, 0xBA,
    0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8,
    0x68, 0x6B, 0x81, 0xB2, 0x71, 0x64, 0xDA, 0x8B,
    0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35,
    0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58, 0xD1, 0xA2,
    0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 0x78, 0x87,
    0xD4, 0x00, 0x46, 0x57, 0x9F, 0xD3, 0x27, 0x52,
    0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E,
    0xEA, 0xBF, 0x8A, 0xD2, 0x40, 0xC7, 0x38, 0xB5,
    0xA3, 0xF7, 0xF2, 0xCE, 0xF9, 0x61, 0x15, 0xA1,
    0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 0x1A, 0x55,
    0xAD, 0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3,
    0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60,
    0xC0, 0x29, 0x23, 0xAB, 0x0D, 0x53, 0x4E, 0x6F,
    0xD5, 0xDB, 0x37, 0x45, 0xDE, 0xFD, 0x8E, 0x2F,
    0x03, 0xFF, 0x6A, 0x72, 0x6D, 0x6C, 0x5B, 0x51,
    0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F,
    0x11, 0xD9, 0x5C, 0x41, 0x1F, 0x10, 0x5A, 0xD8,
    0x0A, 0xC1, 0x31, 0x88, 0xA5, 0xCD, 0x7B, 0xBD,
    0x2D, 0x74, 0xD0, 0x12, 0xB8, 0xE5, 0xB4, 0xB0,
    0x89, 0x69, 0x97, 0x4A, 0x0C, 0x96, 0x77, 0x7E,
    0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E, 0xC6, 0x84,
    0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC, 0x4D, 0x20,
    0x79, 0xEE, 0x5F, 0x3E, 0xD7, 0xCB, 0x39, 0x48
};

/* ── 系统参数 FK（GB/T 32907-2016 §7.2）── */
static const uint32_t SM4_FK[4] = {
    0xA3B1BAC6U, 0x56AA3350U, 0x677D9197U, 0xB27022DCU
};

/* ── 固定参数 CK（GB/T 32907-2016 §7.2）── */
static const uint32_t SM4_CK[32] = {
    0x00070E15U, 0x1C232A31U, 0x383F464DU, 0x545B6269U,
    0x70777E85U, 0x8C939AA1U, 0xA8AFB6BDU, 0xC4CBD2D9U,
    0xE0E7EEF5U, 0xFC030A11U, 0x181F262DU, 0x343B4249U,
    0x50575E65U, 0x6C737A81U, 0x888F969DU, 0xA4ABB2B9U,
    0xC0C7CED5U, 0xDCE3EAF1U, 0xF8FF060DU, 0x141B2229U,
    0x30373E45U, 0x4C535A61U, 0x686F767DU, 0x848B9299U,
    0xA0A7AEB5U, 0xBCC3CAD1U, 0xD8DFE6EDU, 0xF4FB0209U,
    0x10171E25U, 0x2C333A41U, 0x484F565DU, 0x646B7279U
};

/* ── 内部辅助 ── */
static inline uint32_t rotl32(uint32_t x, int n) {
    n &= 31;
    return (x << n) | (x >> (32 - n));
}

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

/* ── S 盒变换 τ（§6.4）── */
static inline uint32_t sm4_tau(uint32_t x) {
    return ((uint32_t)SM4_SBOX[(x >> 24) & 0xFF] << 24)
         | ((uint32_t)SM4_SBOX[(x >> 16) & 0xFF] << 16)
         | ((uint32_t)SM4_SBOX[(x >> 8)  & 0xFF] << 8)
         | ((uint32_t)SM4_SBOX[ x        & 0xFF]);
}

/* ── 线性变换 L（§6.3，加密轮函数用）── */
static inline uint32_t sm4_L(uint32_t B) {
    return B ^ rotl32(B, 2) ^ rotl32(B, 10) ^ rotl32(B, 18) ^ rotl32(B, 24);
}

/* ── 线性变换 L'（§7.2，密钥扩展用）── */
static inline uint32_t sm4_Lp(uint32_t B) {
    return B ^ rotl32(B, 13) ^ rotl32(B, 23);
}

/* ── 轮函数 F（§6.1）── */
static inline uint32_t sm4_F(uint32_t X0, uint32_t X1, uint32_t X2, uint32_t X3, uint32_t rk) {
    return X0 ^ sm4_L(sm4_tau(X1 ^ X2 ^ X3 ^ rk));
}

/* ══════════════════════════════════════════════════════════════
 * 密钥扩展（GB/T 32907-2016 §7.2）
 *
 * (K0, K1, K2, K3) = (MK0^FK0, MK1^FK1, MK2^FK2, MK3^FK3)
 * rk_i = K_{i+4} = K_i ^ L'(τ(K_{i+1} ^ K_{i+2} ^ K_{i+3} ^ CK_i))
 * ══════════════════════════════════════════════════════════════ */

static void sm4_key_expansion(uint32_t rk[SM4_ROUNDS], const uint8_t key[SM4_KEY_SIZE]) {
    uint32_t K[36];  /* K[0..35] */
    uint32_t MK[4];
    int i;

    /* 加载主密钥 */
    MK[0] = load_be32(key);
    MK[1] = load_be32(key + 4);
    MK[2] = load_be32(key + 8);
    MK[3] = load_be32(key + 12);

    /* (K0, K1, K2, K3) = (MK0^FK0, MK1^FK1, MK2^FK2, MK3^FK3) */
    for (i = 0; i < 4; i++)
        K[i] = MK[i] ^ SM4_FK[i];

    /* rk_i = K_{i+4} = K_i ^ L'(τ(K_{i+1} ^ K_{i+2} ^ K_{i+3} ^ CK_i)) */
    for (i = 0; i < SM4_ROUNDS; i++) {
        K[i + 4] = K[i] ^ sm4_Lp(sm4_tau(K[i + 1] ^ K[i + 2] ^ K[i + 3] ^ SM4_CK[i]));
        rk[i] = K[i + 4];
    }
}

/* ══════════════════════════════════════════════════════════════
 * SM4 加解密核心（GB/T 32907-2016 §6.3）
 *
 * 输入: X[0..3] = 4个32位明文/密文字
 * 轮密钥: rk[0..31]
 * 输出: X[0..3]（原地修改）
 * ══════════════════════════════════════════════════════════════ */

static void sm4_crypt_core(uint32_t X[4], const uint32_t rk[SM4_ROUNDS]) {
    int i;
    for (i = 0; i < SM4_ROUNDS; i++) {
        X[0] = sm4_F(X[0], X[1], X[2], X[3], rk[i]);
        /* 不借助临时变量的循环移位：X[0],X[1],X[2],X[3] → X[1],X[2],X[3],X[0] */
        uint32_t t = X[1]; X[1] = X[2]; X[2] = X[3]; X[3] = X[0]; X[0] = t;
    }
    /* 最后反序输出：(X[35],X[34],X[33],X[32]) = (X[3],X[2],X[1],X[0]) → 已在位 */
    /* 经过32轮后 X 已经循环移位了32次，当前排列为 (X35, X34, X33, X32) */
    /* 即 X[35]=X[3], X[34]=X[2], X[33]=X[1], X[32]=X[0] */
}

/* ══════════════════════════════════════════════════════════════
 * 公开 API
 * ══════════════════════════════════════════════════════════════ */

void guomi_sm4_set_encrypt_key(guomi_sm4_ctx_t *ctx,
                               const uint8_t key[SM4_KEY_SIZE]) {
    sm4_key_expansion(ctx->round_keys, key);
}

void guomi_sm4_set_decrypt_key(guomi_sm4_ctx_t *ctx,
                               const uint8_t key[SM4_KEY_SIZE]) {
    uint32_t rk[SM4_ROUNDS];
    int i;
    sm4_key_expansion(rk, key);
    /* 解密轮密钥 = 加密轮密钥逆序 */
    for (i = 0; i < SM4_ROUNDS; i++)
        ctx->round_keys[i] = rk[SM4_ROUNDS - 1 - i];
}

void guomi_sm4_encrypt_block(const guomi_sm4_ctx_t *ctx,
                             const uint8_t input[SM4_BLOCK_SIZE],
                             uint8_t output[SM4_BLOCK_SIZE]) {
    uint32_t X[4];
    int i;

    for (i = 0; i < 4; i++)
        X[i] = load_be32(input + i * 4);

    sm4_crypt_core(X, ctx->round_keys);

    /* SM4 标准输出: (X35, X34, X33, X32) = 逆序 */
    for (i = 0; i < 4; i++)
        store_be32(output + i * 4, X[3 - i]);
}

void guomi_sm4_decrypt_block(const guomi_sm4_ctx_t *ctx,
                             const uint8_t input[SM4_BLOCK_SIZE],
                             uint8_t output[SM4_BLOCK_SIZE]) {
    /* 解密与加密使用相同核心，仅轮密钥顺序不同 */
    guomi_sm4_encrypt_block(ctx, input, output);
}

/* ══════════════════════════════════════════════════════════════
 * SM4-CBC 模式（PKCS7 填充）
 * ══════════════════════════════════════════════════════════════ */

size_t guomi_sm4_cbc_encrypt(const guomi_sm4_ctx_t *ctx,
                             const uint8_t iv[SM4_BLOCK_SIZE],
                             const uint8_t *input, size_t input_len,
                             uint8_t *output) {
    uint8_t chain[SM4_BLOCK_SIZE];
    uint8_t block[SM4_BLOCK_SIZE];
    size_t j, out_pos = 0, in_pos = 0;

    /* PKCS7 填充 */
    uint8_t pad_val = (uint8_t)(SM4_BLOCK_SIZE - (input_len % SM4_BLOCK_SIZE));
    if (pad_val == 0) pad_val = SM4_BLOCK_SIZE;

    /* 复制 IV */
    memcpy(chain, iv, SM4_BLOCK_SIZE);

    /* 完整分组 */
    while (in_pos + SM4_BLOCK_SIZE <= input_len) {
        for (j = 0; j < SM4_BLOCK_SIZE; j++)
            block[j] = input[in_pos + j] ^ chain[j];
        guomi_sm4_encrypt_block(ctx, block, output + out_pos);
        memcpy(chain, output + out_pos, SM4_BLOCK_SIZE);
        out_pos += SM4_BLOCK_SIZE;
        in_pos += SM4_BLOCK_SIZE;
    }

    /* 最后一个分组（含填充） */
    for (j = 0; j < SM4_BLOCK_SIZE; j++) {
        if (in_pos + j < input_len)
            block[j] = input[in_pos + j];
        else
            block[j] = pad_val;
        block[j] ^= chain[j];
    }
    guomi_sm4_encrypt_block(ctx, block, output + out_pos);
    out_pos += SM4_BLOCK_SIZE;

    return out_pos;
}

size_t guomi_sm4_cbc_decrypt(const guomi_sm4_ctx_t *ctx,
                             const uint8_t iv[SM4_BLOCK_SIZE],
                             const uint8_t *input, size_t input_len,
                             uint8_t *output) {
    uint8_t chain[SM4_BLOCK_SIZE];
    uint8_t block[SM4_BLOCK_SIZE];
    size_t i, j, out_pos = 0, in_pos = 0;
    uint8_t pad_val;

    if (input_len < SM4_BLOCK_SIZE || input_len % SM4_BLOCK_SIZE != 0)
        return 0;  /* 无效长度 */

    memcpy(chain, iv, SM4_BLOCK_SIZE);

    while (in_pos < input_len - SM4_BLOCK_SIZE) {
        guomi_sm4_decrypt_block(ctx, input + in_pos, block);
        for (j = 0; j < SM4_BLOCK_SIZE; j++)
            output[out_pos + j] = block[j] ^ chain[j];
        memcpy(chain, input + in_pos, SM4_BLOCK_SIZE);
        out_pos += SM4_BLOCK_SIZE;
        in_pos += SM4_BLOCK_SIZE;
    }

    /* 最后一个分组（去 PKCS7 填充） */
    guomi_sm4_decrypt_block(ctx, input + in_pos, block);
    for (j = 0; j < SM4_BLOCK_SIZE; j++)
        output[out_pos + j] = block[j] ^ chain[j];

    /* 验证并去除填充 */
    pad_val = output[out_pos + SM4_BLOCK_SIZE - 1];
    if (pad_val == 0 || pad_val > SM4_BLOCK_SIZE) return 0;  /* 填充错误 */

    for (i = 1; i < pad_val; i++) {
        if (output[out_pos + SM4_BLOCK_SIZE - 1 - i] != pad_val)
            return 0;  /* 填充不一致 */
    }

    return out_pos + SM4_BLOCK_SIZE - pad_val;
}

/* ══════════════════════════════════════════════════════════════
 * SM4 自检：使用 GB/T 32907-2016 附录A 测试向量
 * ══════════════════════════════════════════════════════════════ */

int guomi_sm4_selftest(void) {
    /* 测试向量（GB/T 32907-2016 A.1） */
    static const uint8_t test_key[SM4_KEY_SIZE] = {
        0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF,
        0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10
    };
    static const uint8_t test_plain[SM4_BLOCK_SIZE] = {
        0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF,
        0xFE, 0xDC, 0xBA, 0x98, 0x76, 0x54, 0x32, 0x10
    };
    /* 加密一次 */
    static const uint8_t expected[SM4_BLOCK_SIZE] = {
        0x68, 0x1E, 0xDF, 0x34, 0xD2, 0x06, 0x96, 0x5E,
        0x86, 0xB3, 0xE9, 0x4F, 0x53, 0x6E, 0x42, 0x46
    };

    guomi_sm4_ctx_t ctx;
    uint8_t output[SM4_BLOCK_SIZE];
    uint8_t decrypted[SM4_BLOCK_SIZE];
    size_t i;

    /* 加密测试 */
    guomi_sm4_set_encrypt_key(&ctx, test_key);
    guomi_sm4_encrypt_block(&ctx, test_plain, output);
    for (i = 0; i < SM4_BLOCK_SIZE; i++) {
        if (output[i] != expected[i]) return 1;
    }

    /* 解密测试 */
    guomi_sm4_set_decrypt_key(&ctx, test_key);
    guomi_sm4_decrypt_block(&ctx, output, decrypted);
    for (i = 0; i < SM4_BLOCK_SIZE; i++) {
        if (decrypted[i] != test_plain[i]) return 2;
    }

    return 0;  /* 全部通过 */
}
