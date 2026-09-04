// DNA: #龍芯⚡️丙午·丙申·乙卯·申时·䷐随-IOS-CRYPTO-v1.0-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
//
// 龍魂·iOS 国密算法 Swift 封装
// 桥接 CGuomi（纯 C99 底座）· 与鸿蒙 harmonyos-universe 同源
// SM2(GB/T 32918) · SM3(GB/T 32905) · SM4(GB/T 32907)

import Foundation
import CGuomi

/// 龍魂国密算法入口（端侧加密 · 密钥永不离开设备）
public enum LonghunCrypto {

    // MARK: - SM3 密码杂凑 (GB/T 32905-2016)

    /// SM3 哈希，返回 32 字节摘要
    public static func sm3(_ data: Data) -> [UInt8] {
        var digest = [UInt8](repeating: 0, count: Int(SM3_DIGEST_SIZE))
        data.withUnsafeBytes { raw in
            guomi_sm3_hash(raw.bindMemory(to: UInt8.self).baseAddress, data.count, &digest)
        }
        return digest
    }

    /// SM3 哈希，返回 64 位 hex 字符串
    public static func sm3Hex(_ data: Data) -> String {
        sm3(data).map { String(format: "%02x", $0) }.joined()
    }

    /// SM3 哈希（UTF-8 字符串输入）
    public static func sm3Hex(_ text: String) -> String {
        sm3Hex(Data(text.utf8))
    }

    /// SM3-HMAC，返回 32 字节 MAC
    public static func sm3Hmac(key: Data, data: Data) -> [UInt8] {
        var mac = [UInt8](repeating: 0, count: Int(SM3_HMAC_SIZE))
        key.withUnsafeBytes { kr in
            data.withUnsafeBytes { dr in
                guomi_sm3_hmac(kr.bindMemory(to: UInt8.self).baseAddress, key.count,
                               dr.bindMemory(to: UInt8.self).baseAddress, data.count, &mac)
            }
        }
        return mac
    }

    // MARK: - SM2 椭圆曲线公钥密码 (GB/T 32918.1~5-2016)

    /// SM2 密钥对（私钥 32 字节 · 公钥 64 字节未压缩）
    public struct SM2KeyPair: Sendable {
        public let sk: [UInt8]
        public let pk: [UInt8]
        public init(sk: [UInt8], pk: [UInt8]) {
            self.sk = sk
            self.pk = pk
        }
        /// 私钥 hex（64 位）
        public var skHex: String { sk.map { String(format: "%02x", $0) }.joined() }
        /// 公钥 hex（128 位）
        public var pkHex: String { pk.map { String(format: "%02x", $0) }.joined() }
    }

    /// 生成 SM2 密钥对
    public static func sm2Keygen() -> SM2KeyPair {
        var sk = [UInt8](repeating: 0, count: Int(SM2_KEY_SIZE))
        var pk = [UInt8](repeating: 0, count: Int(SM2_PUBKEY_SIZE))
        guomi_sm2_keygen(&sk, &pk)
        return SM2KeyPair(sk: sk, pk: pk)
    }

    /// SM2 签名（id 为空时使用标准默认标识）
    public static func sm2Sign(sk: [UInt8], message: Data, id: Data = Data()) -> [UInt8] {
        var sig = [UInt8](repeating: 0, count: Int(SM2_SIGN_SIZE))
        message.withUnsafeBytes { mr in
            id.withUnsafeBytes { ir in
                guomi_sm2_sign(sk, mr.bindMemory(to: UInt8.self).baseAddress, message.count,
                               ir.bindMemory(to: UInt8.self).baseAddress, id.count, &sig)
            }
        }
        return sig
    }

    /// SM2 验签，返回是否有效
    public static func sm2Verify(pk: [UInt8], message: Data, signature: [UInt8], id: Data = Data()) -> Bool {
        var ok: Int32 = 0
        message.withUnsafeBytes { mr in
            signature.withUnsafeBytes { sr in
                id.withUnsafeBytes { ir in
                    ok = guomi_sm2_verify(pk, mr.bindMemory(to: UInt8.self).baseAddress, message.count,
                                          ir.bindMemory(to: UInt8.self).baseAddress, id.count,
                                          sr.bindMemory(to: UInt8.self).baseAddress)
                }
            }
        }
        return ok == 1
    }

    /// SM2 公钥加密（输出 C1||C3||C2）
    public static func sm2Encrypt(pk: [UInt8], message: Data) -> [UInt8] {
        var out = [UInt8](repeating: 0, count: message.count + Int(SM2_CIPHER_OVERHEAD))
        let len = message.withUnsafeBytes { mr -> Int in
            guomi_sm2_encrypt(pk, mr.bindMemory(to: UInt8.self).baseAddress, message.count, &out)
        }
        return Array(out.prefix(len))
    }

    /// SM2 私钥解密
    public static func sm2Decrypt(sk: [UInt8], cipher: Data) -> [UInt8]? {
        var out = [UInt8](repeating: 0, count: max(cipher.count - Int(SM2_CIPHER_OVERHEAD), 0))
        let len = cipher.withUnsafeBytes { cr -> Int in
            guomi_sm2_decrypt(sk, cr.bindMemory(to: UInt8.self).baseAddress, cipher.count, &out)
        }
        guard len > 0 else { return nil }
        return Array(out.prefix(len))
    }

    /// 从私钥导出公钥
    public static func sm2Pubkey(from sk: [UInt8]) -> [UInt8] {
        var pk = [UInt8](repeating: 0, count: Int(SM2_PUBKEY_SIZE))
        guomi_sm2_pubkey_from_sk(sk, &pk)
        return pk
    }

    // MARK: - SM4 分组密码 (GB/T 32907-2016)

    /// SM4-CBC 加密（PKCS7 填充）
    public static func sm4CbcEncrypt(key: [UInt8], iv: [UInt8], plain: Data) -> [UInt8] {
        var ctx = guomi_sm4_ctx_t()
        guomi_sm4_set_encrypt_key(&ctx, key)
        var out = [UInt8](repeating: 0, count: plain.count + Int(SM4_BLOCK_SIZE))
        let len = plain.withUnsafeBytes { pr -> Int in
            guomi_sm4_cbc_encrypt(&ctx, iv, pr.bindMemory(to: UInt8.self).baseAddress, plain.count, &out)
        }
        return Array(out.prefix(len))
    }

    /// SM4-CBC 解密（自动去 PKCS7 填充）
    public static func sm4CbcDecrypt(key: [UInt8], iv: [UInt8], cipher: Data) -> [UInt8] {
        var ctx = guomi_sm4_ctx_t()
        guomi_sm4_set_decrypt_key(&ctx, key)
        var out = [UInt8](repeating: 0, count: max(cipher.count, 0))
        let len = cipher.withUnsafeBytes { cr -> Int in
            guomi_sm4_cbc_decrypt(&ctx, iv, cr.bindMemory(to: UInt8.self).baseAddress, cipher.count, &out)
        }
        return Array(out.prefix(max(len, 0)))
    }

    // MARK: - 三色审计

    /// SM2 曲线参数三色审计（🟢 通过 / 非 🟢 需熔断）
    public static func auditSM2Params() -> Bool {
        guomi_sm2_validate_params() == GUOMI_AUDIT_GREEN
    }

    // MARK: - 便捷 hex

    public static func hexString(_ bytes: [UInt8]) -> String {
        bytes.map { String(format: "%02x", $0) }.joined()
    }

    public static func bytes(fromHex hex: String) -> [UInt8]? {
        let cleaned = hex.trimmingCharacters(in: .whitespacesAndNewlines)
        guard cleaned.count % 2 == 0 else { return nil }
        var bytes = [UInt8]()
        bytes.reserveCapacity(cleaned.count / 2)
        var idx = cleaned.startIndex
        while idx < cleaned.endIndex {
            let next = cleaned.index(idx, offsetBy: 2)
            guard let byte = UInt8(cleaned[idx..<next], radix: 16) else { return nil }
            bytes.append(byte)
            idx = next
        }
        return bytes
    }
}
