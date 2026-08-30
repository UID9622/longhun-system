// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-82f09d4f
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/*
 * 龍魂 SM2 全链路自测 · lh_sm2_full.c
 * 修复验证: fe_mul_raw(__uint128_t) + fast_reduce(while) 后回归
 * 测试项:
 *   [1] validate_params == 1
 *   [2] keygen -> sign -> verify(ok) == 1
 *   [3] 篡改消息 -> verify == 0
 *   [4] 篡改签名 -> verify == 0
 *   [5] encrypt -> decrypt match == 1
 *   [6] 非法公钥验签拒绝
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "guomi/guomi.h"

static int fails = 0;

static void check(const char *name, int cond) {
    printf("[%s] %s\n", cond ? "PASS" : "FAIL", name);
    if (!cond) fails++;
}

int main(void) {
    uint8_t sk[SM2_KEY_SIZE], pk[SM2_PUBKEY_SIZE];
    uint8_t pk2[SM2_PUBKEY_SIZE];
    uint8_t sig[SM2_SIGN_SIZE];
    const uint8_t msg[] = "longhun houtuo OS guomi test";
    const uint8_t id[] = "1234567812345678";

    check("validate_params (0=ok)", guomi_sm2_validate_params() == 0);

    guomi_sm2_keygen(sk, pk);
    guomi_sm2_pubkey_from_sk(sk, pk2);
    check("pubkey_from_sk == keygen pk", memcmp(pk, pk2, SM2_PUBKEY_SIZE) == 0);

    guomi_sm2_sign(sk, msg, sizeof(msg)-1, id, sizeof(id)-1, sig);
    check("verify(ok) == 1", guomi_sm2_verify(pk, msg, sizeof(msg)-1, id, sizeof(id)-1, sig) == 1);

    {
        uint8_t bad_msg[sizeof(msg)];
        memcpy(bad_msg, msg, sizeof(msg));
        bad_msg[2] ^= 0x01;
        check("verify(tampered msg) == 0",
              guomi_sm2_verify(pk, bad_msg, sizeof(msg)-1, id, sizeof(id)-1, sig) == 0);
    }

    {
        uint8_t bad_sig[SM2_SIGN_SIZE];
        memcpy(bad_sig, sig, SM2_SIGN_SIZE);
        bad_sig[3] ^= 0x40;
        check("verify(tampered sig) == 0",
              guomi_sm2_verify(pk, msg, sizeof(msg)-1, id, sizeof(id)-1, bad_sig) == 0);
    }

    {
        const uint8_t plain[] = "hongmeng native guomi three-end same-source";
        size_t plen = sizeof(plain) - 1;
        uint8_t ct[sizeof(plain) + SM2_CIPHER_OVERHEAD];
        uint8_t pt[sizeof(plain) + SM2_CIPHER_OVERHEAD];
        size_t ctlen = guomi_sm2_encrypt(pk, plain, plen, ct);
        size_t ptlen = guomi_sm2_decrypt(sk, ct, ctlen, pt);
        check("encrypt len == plain + 97", ctlen == plen + SM2_CIPHER_OVERHEAD);
        check("decrypt len == plain len", ptlen == plen);
        check("decrypt == plain", ptlen == plen && memcmp(pt, plain, plen) == 0);
    }

    {
        uint8_t zero_pk[SM2_PUBKEY_SIZE] = {0};
        check("verify(zero pk) == 0",
              guomi_sm2_verify(zero_pk, msg, sizeof(msg)-1, id, sizeof(id)-1, sig) == 0);
    }

    printf("\n=== summary: %s (%d fails) ===\n", fails == 0 ? "ALL PASS" : "FAIL", fails);
    return fails;
}
