// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-0a6188f6
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/* 龍魂 SM2 100 轮随机密钥回归 · lh_sm2_stress.c
 * 每轮: 随机 sk -> pubkey_from_sk -> sign -> verify(ok)=1
 *       -> 篡改消息 verify=0 -> 篡改签名 verify=0
 * 外加 SM3 标准向量回归(每轮开头)
 */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include "guomi/guomi.h"

int main(void) {
    int rounds = 100;
    int fails = 0;
    const uint8_t id[] = "1234567812345678";
    const uint8_t msg[] = "longhun stress test sm2 round";
    uint64_t ctr = 0;

    /* SM3 标准向量: sm3("abc") = 66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0 */
    {
        uint8_t d[32];
        guomi_sm3_hash((const uint8_t*)"abc", 3, d);
        const uint8_t exp[32] = {0x66,0xc7,0xf0,0xf4,0x62,0xee,0xed,0xd9,0xd1,0xf2,0xd4,0x6b,0xdc,0x10,0xe4,0xe2,
                                  0x41,0x67,0xc4,0x87,0x5c,0xf2,0xf7,0xa2,0x29,0x7d,0xa0,0x2b,0x8f,0x4b,0xa8,0xe0};
        if (memcmp(d, exp, 32) != 0) { printf("SM3 vector FAIL\n"); fails++; }
        else printf("SM3 vector PASS\n");
    }

    for (int r = 0; r < rounds; r++) {
        uint8_t sk[SM2_KEY_SIZE], pk[SM2_PUBKEY_SIZE];
        uint8_t sig[SM2_SIGN_SIZE];
        uint8_t seed[32];

        /* 随机 sk: SM3(time || ctr || counter) */
        {
            guomi_sm3_ctx_t c;
            char hdr[64];
            snprintf(hdr, sizeof(hdr), "lh-stress-%llu-%d", (unsigned long long)time(NULL), r);
            guomi_sm3_init(&c);
            guomi_sm3_update(&c, (uint8_t*)hdr, strlen(hdr));
            guomi_sm3_update(&c, (uint8_t*)&ctr, sizeof(ctr));
            guomi_sm3_final(&c, seed);
            ctr++;
            memcpy(sk, seed, 32);
            if (r % 7 == 0) sk[0] ^= (uint8_t)(r * 13);
        }

        guomi_sm2_pubkey_from_sk(sk, pk);
        guomi_sm2_sign(sk, msg, sizeof(msg)-1, id, sizeof(id)-1, sig);

        if (guomi_sm2_verify(pk, msg, sizeof(msg)-1, id, sizeof(id)-1, sig) != 1) {
            printf("round %d: verify(ok) FAIL\n", r); fails++;
            continue;
        }

        uint8_t bm[sizeof(msg)];
        memcpy(bm, msg, sizeof(msg));
        bm[3] ^= 0x80;
        if (guomi_sm2_verify(pk, bm, sizeof(msg)-1, id, sizeof(id)-1, sig) != 0) {
            printf("round %d: verify(tampered msg) FAIL\n", r); fails++;
        }

        uint8_t bs[SM2_SIGN_SIZE];
        memcpy(bs, sig, SM2_SIGN_SIZE);
        bs[10] ^= 0x01;
        if (guomi_sm2_verify(pk, msg, sizeof(msg)-1, id, sizeof(id)-1, bs) != 0) {
            printf("round %d: verify(tampered sig) FAIL\n", r); fails++;
        }
    }

    printf("=== stress %d rounds: %s (%d fails) ===\n", rounds, fails ? "FAIL" : "ALL PASS", fails);
    return fails;
}
