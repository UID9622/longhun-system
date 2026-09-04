// DNA: #龍芯⚡️丙午·丙申·乙卯·申时·䷐随-HARMONY-GUOMI-TYPES-v1.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 龍魂国密 Native 核心 · ArkTS 类型声明

/** SM3 哈希: 输入 UTF-8 字符串, 输出 64 位 hex 摘要 */
export const sm3Hex: (data: string) => string;

/** SM3-HMAC: keyHex/dataHex, 输出 64 位 hex */
export const sm3Hmac: (keyHex: string, dataHex: string) => string;

/** SM2 密钥对生成: 返回 { sk: 64位hex, pk: 128位hex } */
export const sm2Keygen: () => { sk: string; pk: string };

/** SM2 签名: skHex(64) + msgHex + idHex?, 输出 128 位 hex 签名(r||s) */
export const sm2Sign: (skHex: string, msgHex: string, idHex?: string) => string;

/** SM2 验签: pkHex(128) + msgHex + sigHex(128) + idHex?, 返回是否有效 */
export const sm2Verify: (pkHex: string, msgHex: string, sigHex: string, idHex?: string) => boolean;

/** SM2 公钥加密: pkHex(128) + msgHex, 输出 C1||C3||C2 hex */
export const sm2Encrypt: (pkHex: string, msgHex: string) => string;

/** SM2 私钥解密: skHex(64) + cipherHex, 输出明文 hex */
export const sm2Decrypt: (skHex: string, cipherHex: string) => string;

/** SM4-CBC 加密: keyHex(32) + ivHex(32) + plainHex, PKCS7 填充 */
export const sm4CbcEncrypt: (keyHex: string, ivHex: string, plainHex: string) => string;

/** SM4-CBC 解密: keyHex(32) + ivHex(32) + cipherHex, 自动去填充 */
export const sm4CbcDecrypt: (keyHex: string, ivHex: string, cipherHex: string) => string;

/** SM2 曲线参数三色审计: 返回参数是否合法 🟢 */
export const auditParams: () => boolean;
