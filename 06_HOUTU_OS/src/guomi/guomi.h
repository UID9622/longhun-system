/*
 * 龍魂·后土OS — 国密算法底座 · 统一头文件
 * DNA: #龍芯⚡️丙午·丙申·乙卯·丁亥·䷉履-GUOMI-BASE-v1.0
 *
 * 文化锚点：中宫（太极）— 国密算法为系统安全之根基
 *
 * 本底座焊死不可变：
 *   - SM3 密码杂凑算法   GB/T 32905-2016
 *   - SM4 分组密码算法   GB/T 32907-2016
 *   - SM2 椭圆曲线公钥密码算法 GB/T 32918.1~5-2016
 *
 * 设计原则：
 *   - 纯 C99，零外部依赖（freestanding 兼容）
 *   - 所有内存由调用者分配，算法层不分配
 *   - 龙魂后土OS内核与鸿蒙系统共用同一套C底座
 *   - 算法参数直接引用 GB/T 标准原文
 *
 * 使用层级：
 *   L0·底座层 — 本文件及 sm2/sm3/sm4（焊死不可变）
 *   L1·协议层 — 上层封装（加解密、签名、密钥交换）
 *   L2·应用层 — 文件加密、DNA签名、审计验证
 */

#ifndef HOUTU_GUOMI_H
#define HOUTU_GUOMI_H

#include <stddef.h>
#include <stdint.h>

/* ── 算法常量 ── */
#define SM3_BLOCK_SIZE   64   /* SM3 消息块：512位 = 64字节 */
#define SM3_DIGEST_SIZE  32   /* SM3 摘要：256位 = 32字节 */
#define SM3_HMAC_SIZE    32   /* SM3-HMAC 输出 */

#define SM4_BLOCK_SIZE   16   /* SM4 分组：128位 = 16字节 */
#define SM4_KEY_SIZE     16   /* SM4 密钥：128位 = 16字节 */
#define SM4_ROUNDS       32   /* SM4 迭代轮数 */

#define SM2_KEY_SIZE     32   /* SM2 私钥：256位 = 32字节 */
#define SM2_PUBKEY_SIZE  64   /* SM2 公钥（未压缩）：512位 = 64字节 */
#define SM2_SIGN_SIZE    64   /* SM2 签名(r,s)：各256位 */
#define SM2_CIPHER_OVERHEAD 97 /* SM2 加密额外开销：C1(65)+C3(32) */

/* ── 三色审计返回码 ── */
#define GUOMI_AUDIT_GREEN  0  /* 🟢 通过 */
#define GUOMI_AUDIT_YELLOW 1  /* 🟡 待审 */
#define GUOMI_AUDIT_RED    2  /* 🔴 熔断 */

/* ══════════════════════════════════════════════════════════════
 * SM3 密码杂凑算法  GB/T 32905-2016
 * ══════════════════════════════════════════════════════════════ */

/* SM3 上下文（调用者分配） */
typedef struct {
    uint8_t  block[SM3_BLOCK_SIZE];  /* 当前消息块 */
    uint32_t state[8];               /* 中间状态 V */
    uint64_t total_bits;             /* 已处理消息总位数 */
    size_t   block_len;              /* 当前块已用字节数 */
} guomi_sm3_ctx_t;

/* 初始化 SM3 上下文 */
void guomi_sm3_init(guomi_sm3_ctx_t *ctx);

/* 追加消息数据 */
void guomi_sm3_update(guomi_sm3_ctx_t *ctx, const uint8_t *data, size_t len);

/* 完成哈希计算，输出 32 字节摘要到 digest */
void guomi_sm3_final(guomi_sm3_ctx_t *ctx, uint8_t digest[SM3_DIGEST_SIZE]);

/* 便捷函数：一步完成 SM3 哈希 */
void guomi_sm3_hash(const uint8_t *data, size_t len,
                    uint8_t digest[SM3_DIGEST_SIZE]);

/* SM3-HMAC */
void guomi_sm3_hmac(const uint8_t *key, size_t key_len,
                    const uint8_t *data, size_t data_len,
                    uint8_t mac[SM3_HMAC_SIZE]);

/* ══════════════════════════════════════════════════════════════
 * SM4 分组密码算法  GB/T 32907-2016
 * ══════════════════════════════════════════════════════════════ */

/* SM4 上下文 */
typedef struct {
    uint32_t round_keys[SM4_ROUNDS];  /* 轮密钥 */
} guomi_sm4_ctx_t;

/* 设置加密密钥（128位/16字节） */
void guomi_sm4_set_encrypt_key(guomi_sm4_ctx_t *ctx,
                               const uint8_t key[SM4_KEY_SIZE]);

/* 设置解密密钥（与加密密钥相同，轮密钥反转） */
void guomi_sm4_set_decrypt_key(guomi_sm4_ctx_t *ctx,
                               const uint8_t key[SM4_KEY_SIZE]);

/* 加密单个 16 字节分组 */
void guomi_sm4_encrypt_block(const guomi_sm4_ctx_t *ctx,
                             const uint8_t input[SM4_BLOCK_SIZE],
                             uint8_t output[SM4_BLOCK_SIZE]);

/* 解密单个 16 字节分组 */
void guomi_sm4_decrypt_block(const guomi_sm4_ctx_t *ctx,
                             const uint8_t input[SM4_BLOCK_SIZE],
                             uint8_t output[SM4_BLOCK_SIZE]);

/* SM4-CBC 加密（PKCS7 填充） */
/* 返回填充后的加密长度，output 需预留 len+16 字节 */
size_t guomi_sm4_cbc_encrypt(const guomi_sm4_ctx_t *ctx,
                             const uint8_t iv[SM4_BLOCK_SIZE],
                             const uint8_t *input, size_t input_len,
                             uint8_t *output);

/* SM4-CBC 解密（自动去除 PKCS7 填充） */
/* 返回去填充后的明文长度 */
size_t guomi_sm4_cbc_decrypt(const guomi_sm4_ctx_t *ctx,
                             const uint8_t iv[SM4_BLOCK_SIZE],
                             const uint8_t *input, size_t input_len,
                             uint8_t *output);

/* ══════════════════════════════════════════════════════════════
 * SM2 椭圆曲线公钥密码算法  GB/T 32918.1~5-2016
 * ══════════════════════════════════════════════════════════════ */

/*
 * SM2 公钥格式（未压缩）：
 *   pubkey[0..31] = x 坐标（大端）
 *   pubkey[32..63] = y 坐标（大端）
 *
 * SM2 签名格式：
 *   sign[0..31] = r（大端）
 *   sign[32..63] = s（大端）
 *
 * SM2 密文格式（C1||C3||C2）：
 *   output[0] = 0x04（未压缩标志）
 *   output[1..32] = C1_x
 *   output[33..64] = C1_y
 *   output[65..96] = C3（SM3 哈希）
 *   output[97..] = C2（密文，与明文等长）
 */

/* 生成 SM2 密钥对 */
/* sk: 32字节私钥输出，pk: 64字节公钥输出 */
void guomi_sm2_keygen(uint8_t sk[SM2_KEY_SIZE],
                      uint8_t pk[SM2_PUBKEY_SIZE]);

/* SM2 数字签名 */
/* 对消息 msg(长度 msg_len) 签名，使用私钥 sk 和标识 id(可为空) */
void guomi_sm2_sign(const uint8_t sk[SM2_KEY_SIZE],
                    const uint8_t *msg, size_t msg_len,
                    const uint8_t *id, size_t id_len,
                    uint8_t signature[SM2_SIGN_SIZE]);

/* SM2 签名验证 */
/* 返回 1=有效, 0=无效 */
int guomi_sm2_verify(const uint8_t pk[SM2_PUBKEY_SIZE],
                     const uint8_t *msg, size_t msg_len,
                     const uint8_t *id, size_t id_len,
                     const uint8_t signature[SM2_SIGN_SIZE]);

/* SM2 公钥加密 */
/* output 需预留 input_len + SM2_CIPHER_OVERHEAD 字节 */
size_t guomi_sm2_encrypt(const uint8_t pk[SM2_PUBKEY_SIZE],
                         const uint8_t *input, size_t input_len,
                         uint8_t *output);

/* SM2 私钥解密 */
/* output 需预留 input_len - SM2_CIPHER_OVERHEAD 字节 */
size_t guomi_sm2_decrypt(const uint8_t sk[SM2_KEY_SIZE],
                         const uint8_t *input, size_t input_len,
                         uint8_t *output);

/* ── SM2 曲线参数校验（三色审计用）── */
int guomi_sm2_validate_params(void);

/* ── 便捷函数：导出公钥 ── */
void guomi_sm2_pubkey_from_sk(const uint8_t sk[SM2_KEY_SIZE],
                              uint8_t pk[SM2_PUBKEY_SIZE]);

#endif /* HOUTU_GUOMI_H */
