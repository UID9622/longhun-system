// DNA: #龍芯⚡️丙午·丙申·乙卯·申时·䷐随-HARMONY-GUOMI-NAPI-v1.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 用途: 鸿蒙 NAPI 桥接 · 将国密 C 底座暴露给 ArkTS
//       与 iOS LonghunKit/CGuomi 同源 · 三端同一加密内核
// 约定: 所有输入输出均为 hex 字符串（避免二进制边界问题）

#include "napi/native_api.h"
#include "guomi/guomi.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

// ── 工具函数 ──

static int hex_char_val(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return -1;
}

static int hex_to_bytes(const char *hex, uint8_t *out, size_t out_cap) {
    size_t len = strlen(hex);
    if (len % 2 != 0) return -1;
    size_t n = len / 2;
    if (n > out_cap) return -1;
    for (size_t i = 0; i < n; i++) {
        int hi = hex_char_val(hex[i * 2]);
        int lo = hex_char_val(hex[i * 2 + 1]);
        if (hi < 0 || lo < 0) return -1;
        out[i] = (uint8_t)((hi << 4) | lo);
    }
    return (int)n;
}

static void bytes_to_hex(const uint8_t *data, size_t len, char *hex) {
    static const char *T = "0123456789abcdef";
    for (size_t i = 0; i < len; i++) {
        hex[i * 2] = T[data[i] >> 4];
        hex[i * 2 + 1] = T[data[i] & 0x0f];
    }
    hex[len * 2] = '\0';
}

static napi_value make_js_string(napi_env env, const char *str) {
    napi_value v;
    napi_create_string_utf8(env, str, NAPI_AUTO_LENGTH, &v);
    return v;
}

static napi_value throw_js_error(napi_env env, const char *msg) {
    napi_throw_error(env, nullptr, msg);
    return nullptr;
}

// ── SM3 ──

// sm3Hex(data: string): string
static napi_value Sm3Hex(napi_env env, napi_callback_info info) {
    size_t argc = 1;
    napi_value args[1];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (argc < 1) return throw_js_error(env, "sm3Hex: 需要 1 个参数 (data)");

    char buf[65536];
    size_t len = 0;
    if (napi_get_value_string_utf8(env, args[0], buf, sizeof(buf), &len) != napi_ok)
        return throw_js_error(env, "sm3Hex: 参数必须是字符串");

    uint8_t digest[SM3_DIGEST_SIZE];
    guomi_sm3_hash((const uint8_t *)buf, len, digest);

    char hex[SM3_DIGEST_SIZE * 2 + 1];
    bytes_to_hex(digest, SM3_DIGEST_SIZE, hex);
    return make_js_string(env, hex);
}

// sm3Hmac(keyHex: string, dataHex: string): string
static napi_value Sm3Hmac(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (argc < 2) return throw_js_error(env, "sm3Hmac: 需要 2 个参数 (keyHex, dataHex)");

    char key_hex[8192], data_hex[65536];
    size_t klen = 0, dlen = 0;
    napi_get_value_string_utf8(env, args[0], key_hex, sizeof(key_hex), &klen);
    napi_get_value_string_utf8(env, args[1], data_hex, sizeof(data_hex), &dlen);

    uint8_t key[4096], data[32768], mac[SM3_HMAC_SIZE];
    int kn = hex_to_bytes(key_hex, key, sizeof(key));
    int dn = hex_to_bytes(data_hex, data, sizeof(data));
    if (kn < 0 || dn < 0) return throw_js_error(env, "sm3Hmac: 参数必须是合法 hex");

    guomi_sm3_hmac(key, (size_t)kn, data, (size_t)dn, mac);
    char hex[SM3_HMAC_SIZE * 2 + 1];
    bytes_to_hex(mac, SM3_HMAC_SIZE, hex);
    return make_js_string(env, hex);
}

// ── SM2 ──

// sm2Keygen(): { sk: string, pk: string }
static napi_value Sm2Keygen(napi_env env, napi_callback_info info) {
    uint8_t sk[SM2_KEY_SIZE], pk[SM2_PUBKEY_SIZE];
    guomi_sm2_keygen(sk, pk);

    char sk_hex[SM2_KEY_SIZE * 2 + 1], pk_hex[SM2_PUBKEY_SIZE * 2 + 1];
    bytes_to_hex(sk, SM2_KEY_SIZE, sk_hex);
    bytes_to_hex(pk, SM2_PUBKEY_SIZE, pk_hex);

    napi_value obj, v;
    napi_create_object(env, &obj);
    napi_create_string_utf8(env, sk_hex, NAPI_AUTO_LENGTH, &v);
    napi_set_named_property(env, obj, "sk", v);
    napi_create_string_utf8(env, pk_hex, NAPI_AUTO_LENGTH, &v);
    napi_set_named_property(env, obj, "pk", v);
    return obj;
}

// sm2Sign(skHex, msgHex, idHex?): string (r||s)
static napi_value Sm2Sign(napi_env env, napi_callback_info info) {
    size_t argc = 3;
    napi_value args[3];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (argc < 2) return throw_js_error(env, "sm2Sign: 需要 2~3 个参数 (skHex, msgHex, idHex?)");

    char sk_hex[SM2_KEY_SIZE * 2 + 1], msg_hex[65536], id_hex[1024];
    size_t sl = 0, ml = 0, il = 0;
    napi_get_value_string_utf8(env, args[0], sk_hex, sizeof(sk_hex), &sl);
    napi_get_value_string_utf8(env, args[1], msg_hex, sizeof(msg_hex), &ml);
    if (argc >= 3)
        napi_get_value_string_utf8(env, args[2], id_hex, sizeof(id_hex), &il);

    uint8_t sk[SM2_KEY_SIZE], msg[32768], id[512], sig[SM2_SIGN_SIZE];
    int sn = hex_to_bytes(sk_hex, sk, sizeof(sk));
    int mn = hex_to_bytes(msg_hex, msg, sizeof(msg));
    int in = (argc >= 3 && il > 0) ? hex_to_bytes(id_hex, id, sizeof(id)) : 0;
    if (sn != SM2_KEY_SIZE) return throw_js_error(env, "sm2Sign: sk 必须为 32 字节 hex");
    if (mn < 0 || in < 0) return throw_js_error(env, "sm2Sign: 参数必须是合法 hex");

    guomi_sm2_sign(sk, msg, (size_t)mn, in > 0 ? id : nullptr, (size_t)in, sig);

    char hex[SM2_SIGN_SIZE * 2 + 1];
    bytes_to_hex(sig, SM2_SIGN_SIZE, hex);
    return make_js_string(env, hex);
}

// sm2Verify(pkHex, msgHex, sigHex, idHex?): boolean
static napi_value Sm2Verify(napi_env env, napi_callback_info info) {
    size_t argc = 4;
    napi_value args[4];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (argc < 3) return throw_js_error(env, "sm2Verify: 需要 3~4 个参数 (pkHex, msgHex, sigHex, idHex?)");

    char pk_hex[SM2_PUBKEY_SIZE * 2 + 1], msg_hex[65536], sig_hex[SM2_SIGN_SIZE * 2 + 1], id_hex[1024];
    size_t pl = 0, ml = 0, sl = 0, il = 0;
    napi_get_value_string_utf8(env, args[0], pk_hex, sizeof(pk_hex), &pl);
    napi_get_value_string_utf8(env, args[1], msg_hex, sizeof(msg_hex), &ml);
    napi_get_value_string_utf8(env, args[2], sig_hex, sizeof(sig_hex), &sl);
    if (argc >= 4)
        napi_get_value_string_utf8(env, args[3], id_hex, sizeof(id_hex), &il);

    uint8_t pk[SM2_PUBKEY_SIZE], msg[32768], sig[SM2_SIGN_SIZE], id[512];
    int pn = hex_to_bytes(pk_hex, pk, sizeof(pk));
    int mn = hex_to_bytes(msg_hex, msg, sizeof(msg));
    int sn = hex_to_bytes(sig_hex, sig, sizeof(sig));
    int in = (argc >= 4 && il > 0) ? hex_to_bytes(id_hex, id, sizeof(id)) : 0;
    if (pn != SM2_PUBKEY_SIZE || sn != SM2_SIGN_SIZE)
        return throw_js_error(env, "sm2Verify: pk/sig 长度不正确");
    if (mn < 0 || in < 0) return throw_js_error(env, "sm2Verify: 参数必须是合法 hex");

    int ok = guomi_sm2_verify(pk, msg, (size_t)mn, in > 0 ? id : nullptr, (size_t)in, sig);
    napi_value result;
    napi_get_boolean(env, ok == 1, &result);
    return result;
}

// sm2Encrypt(pkHex, msgHex): string
static napi_value Sm2Encrypt(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (argc < 2) return throw_js_error(env, "sm2Encrypt: 需要 2 个参数 (pkHex, msgHex)");

    char pk_hex[SM2_PUBKEY_SIZE * 2 + 1], msg_hex[65536];
    size_t pl = 0, ml = 0;
    napi_get_value_string_utf8(env, args[0], pk_hex, sizeof(pk_hex), &pl);
    napi_get_value_string_utf8(env, args[1], msg_hex, sizeof(msg_hex), &ml);

    uint8_t pk[SM2_PUBKEY_SIZE], msg[32768], out[32768 + SM2_CIPHER_OVERHEAD];
    int pn = hex_to_bytes(pk_hex, pk, sizeof(pk));
    int mn = hex_to_bytes(msg_hex, msg, sizeof(msg));
    if (pn != SM2_PUBKEY_SIZE) return throw_js_error(env, "sm2Encrypt: pk 必须为 64 字节 hex");
    if (mn < 0) return throw_js_error(env, "sm2Encrypt: msg 必须是合法 hex");

    size_t out_len = guomi_sm2_encrypt(pk, msg, (size_t)mn, out);
    char hex[65536 * 2 + 256];
    bytes_to_hex(out, out_len, hex);
    return make_js_string(env, hex);
}

// sm2Decrypt(skHex, cipherHex): string
static napi_value Sm2Decrypt(napi_env env, napi_callback_info info) {
    size_t argc = 2;
    napi_value args[2];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (argc < 2) return throw_js_error(env, "sm2Decrypt: 需要 2 个参数 (skHex, cipherHex)");

    char sk_hex[SM2_KEY_SIZE * 2 + 1], ct_hex[65536];
    size_t sl = 0, cl = 0;
    napi_get_value_string_utf8(env, args[0], sk_hex, sizeof(sk_hex), &sl);
    napi_get_value_string_utf8(env, args[1], ct_hex, sizeof(ct_hex), &cl);

    uint8_t sk[SM2_KEY_SIZE], ct[65536], out[65536];
    int sn = hex_to_bytes(sk_hex, sk, sizeof(sk));
    int cn = hex_to_bytes(ct_hex, ct, sizeof(ct));
    if (sn != SM2_KEY_SIZE) return throw_js_error(env, "sm2Decrypt: sk 必须为 32 字节 hex");
    if (cn < 0) return throw_js_error(env, "sm2Decrypt: 密文必须是合法 hex");

    size_t out_len = guomi_sm2_decrypt(sk, ct, (size_t)cn, out);
    if (out_len == 0) return throw_js_error(env, "sm2Decrypt: 解密失败（密钥不匹配或密文损坏）");
    char hex[65536 * 2 + 1];
    bytes_to_hex(out, out_len, hex);
    return make_js_string(env, hex);
}

// ── SM4 ──

// sm4CbcEncrypt(keyHex, ivHex, plainHex): string
static napi_value Sm4CbcEncrypt(napi_env env, napi_callback_info info) {
    size_t argc = 3;
    napi_value args[3];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (argc < 3) return throw_js_error(env, "sm4CbcEncrypt: 需要 3 个参数 (keyHex, ivHex, plainHex)");

    char key_hex[SM4_KEY_SIZE * 2 + 1], iv_hex[SM4_BLOCK_SIZE * 2 + 1], pt_hex[65536];
    size_t kl = 0, il = 0, pl = 0;
    napi_get_value_string_utf8(env, args[0], key_hex, sizeof(key_hex), &kl);
    napi_get_value_string_utf8(env, args[1], iv_hex, sizeof(iv_hex), &il);
    napi_get_value_string_utf8(env, args[2], pt_hex, sizeof(pt_hex), &pl);

    uint8_t key[SM4_KEY_SIZE], iv[SM4_BLOCK_SIZE], pt[32768], out[32768 + SM4_BLOCK_SIZE];
    int kn = hex_to_bytes(key_hex, key, sizeof(key));
    int in = hex_to_bytes(iv_hex, iv, sizeof(iv));
    int pn = hex_to_bytes(pt_hex, pt, sizeof(pt));
    if (kn != SM4_KEY_SIZE || in != SM4_BLOCK_SIZE)
        return throw_js_error(env, "sm4CbcEncrypt: key/iv 长度不正确");
    if (pn < 0) return throw_js_error(env, "sm4CbcEncrypt: 明文必须是合法 hex");

    guomi_sm4_ctx_t ctx;
    guomi_sm4_set_encrypt_key(&ctx, key);
    size_t out_len = guomi_sm4_cbc_encrypt(&ctx, iv, pt, (size_t)pn, out);
    char hex[65536 * 2 + 1];
    bytes_to_hex(out, out_len, hex);
    return make_js_string(env, hex);
}

// sm4CbcDecrypt(keyHex, ivHex, cipherHex): string
static napi_value Sm4CbcDecrypt(napi_env env, napi_callback_info info) {
    size_t argc = 3;
    napi_value args[3];
    napi_get_cb_info(env, info, &argc, args, nullptr, nullptr);
    if (argc < 3) return throw_js_error(env, "sm4CbcDecrypt: 需要 3 个参数 (keyHex, ivHex, cipherHex)");

    char key_hex[SM4_KEY_SIZE * 2 + 1], iv_hex[SM4_BLOCK_SIZE * 2 + 1], ct_hex[65536];
    size_t kl = 0, il = 0, cl = 0;
    napi_get_value_string_utf8(env, args[0], key_hex, sizeof(key_hex), &kl);
    napi_get_value_string_utf8(env, args[1], iv_hex, sizeof(iv_hex), &il);
    napi_get_value_string_utf8(env, args[2], ct_hex, sizeof(ct_hex), &cl);

    uint8_t key[SM4_KEY_SIZE], iv[SM4_BLOCK_SIZE], ct[32768], out[32768];
    int kn = hex_to_bytes(key_hex, key, sizeof(key));
    int in = hex_to_bytes(iv_hex, iv, sizeof(iv));
    int cn = hex_to_bytes(ct_hex, ct, sizeof(ct));
    if (kn != SM4_KEY_SIZE || in != SM4_BLOCK_SIZE)
        return throw_js_error(env, "sm4CbcDecrypt: key/iv 长度不正确");
    if (cn < 0) return throw_js_error(env, "sm4CbcDecrypt: 密文必须是合法 hex");

    guomi_sm4_ctx_t ctx;
    guomi_sm4_set_decrypt_key(&ctx, key);
    size_t out_len = guomi_sm4_cbc_decrypt(&ctx, iv, ct, (size_t)cn, out);
    char hex[65536 * 2 + 1];
    bytes_to_hex(out, out_len, hex);
    return make_js_string(env, hex);
}

// ── SM2 曲线参数三色审计 ──

// auditParams(): boolean
static napi_value AuditParams(napi_env env, napi_callback_info info) {
    int ok = guomi_sm2_validate_params();
    napi_value result;
    napi_get_boolean(env, ok == GUOMI_AUDIT_GREEN, &result);
    return result;
}

// ── 模块注册 ──

static napi_value Init(napi_env env, napi_value exports) {
    napi_property_descriptor desc[] = {
        {"sm3Hex", nullptr, Sm3Hex, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"sm3Hmac", nullptr, Sm3Hmac, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"sm2Keygen", nullptr, Sm2Keygen, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"sm2Sign", nullptr, Sm2Sign, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"sm2Verify", nullptr, Sm2Verify, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"sm2Encrypt", nullptr, Sm2Encrypt, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"sm2Decrypt", nullptr, Sm2Decrypt, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"sm4CbcEncrypt", nullptr, Sm4CbcEncrypt, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"sm4CbcDecrypt", nullptr, Sm4CbcDecrypt, nullptr, nullptr, nullptr, napi_default, nullptr},
        {"auditParams", nullptr, AuditParams, nullptr, nullptr, nullptr, napi_default, nullptr},
    };
    napi_define_properties(env, exports, sizeof(desc) / sizeof(desc[0]), desc);
    return exports;
}

static napi_module longhuncoreModule = {
    .nm_version = 1,
    .nm_flags = 0,
    .nm_filename = nullptr,
    .nm_register_func = Init,
    .nm_modname = "longhuncore",
    .nm_priv = ((void *)0),
    .reserved = {0},
};

extern "C" __attribute__((constructor)) void RegisterLonghuncoreModule(void) {
    napi_module_register(&longhuncoreModule);
}
