// DNA: #龍芯⚡️丙午·丙申·乙卯·申时·䷐随-IOS-TESTS-v1.0-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
//
// 龍魂国密端到端测试 · GB/T 标准向量 + 加解密往返

import XCTest
import LonghunKit

final class LonghunCryptoTests: XCTestCase {

    /// GB/T 32905-2016 标准向量: SM3("abc")
    func testSM3StandardVector() throws {
        let hash = LonghunCrypto.sm3Hex("abc")
        XCTAssertEqual(hash, "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0")
    }

    /// SM2 签名/验签往返
    func testSM2SignVerifyRoundTrip() throws {
        let pair = LonghunCrypto.sm2Keygen()
        let message = Data("龍魂·iOS 端到端测试".utf8)
        let sig = LonghunCrypto.sm2Sign(sk: pair.sk, message: message)
        XCTAssertEqual(sig.count, 64)
        XCTAssertTrue(LonghunCrypto.sm2Verify(pk: pair.pk, message: message, signature: sig))
        // 篡改消息必须验签失败
        XCTAssertFalse(LonghunCrypto.sm2Verify(pk: pair.pk, message: Data("被篡改".utf8), signature: sig))
    }

    /// SM2 加解密往返
    func testSM2EncryptDecryptRoundTrip() throws {
        let pair = LonghunCrypto.sm2Keygen()
        let plain = Data("厚德载物 · 数据主权归用户".utf8)
        let cipher = LonghunCrypto.sm2Encrypt(pk: pair.pk, message: plain)
        let decrypted = try XCTUnwrap(LonghunCrypto.sm2Decrypt(sk: pair.sk, cipher: Data(cipher)))
        XCTAssertEqual(Data(decrypted), plain)
    }

    /// SM4-CBC 加解密往返
    func testSM4CbcRoundTrip() throws {
        let key = Array(repeating: UInt8(0x2d), count: 16)
        let iv = Array(repeating: UInt8(0x13), count: 16)
        let plain = Data("君子协议 · 不拆台 · 不绑架 · 不独食".utf8)
        let cipher = LonghunCrypto.sm4CbcEncrypt(key: key, iv: iv, plain: plain)
        let decrypted = LonghunCrypto.sm4CbcDecrypt(key: key, iv: iv, cipher: Data(cipher))
        XCTAssertEqual(Data(decrypted), plain)
    }

    /// SM2 曲线参数三色审计
    func testSM2ParamsAudit() throws {
        XCTAssertTrue(LonghunCrypto.auditSM2Params())
    }

    /// CNSH DNA 追溯码生成与验证
    func testCNSHDNA() throws {
        let dna = CNSHClient.dNaStamp(module: "IOS", action: "TEST")
        XCTAssertTrue(dna.hasPrefix("#龍芯⚡️"))
        XCTAssertTrue(CNSHClient.verifyDNA(dna, module: "IOS", action: "TEST"))
    }

    /// CNSH 意图路由
    func testCNSHRouting() throws {
        XCTAssertEqual(CNSHClient.routeIntent("帮我审计这段代码"), CNSHClient.Intent.audit)
        XCTAssertEqual(CNSHClient.routeIntent("算一下数字根"), CNSHClient.Intent.math)
        XCTAssertEqual(CNSHClient.routeIntent("部署到鲲鹏"), CNSHClient.Intent.deploy)
    }
}
