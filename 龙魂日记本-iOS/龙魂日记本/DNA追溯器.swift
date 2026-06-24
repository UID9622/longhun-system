//龍芯⚡️2026-06-20-LONGHUN-DNA-TRACER
// DNA追溯系统：所有产出必须带DNA，不可篡改，可恢复原文

import Foundation
import CryptoKit

struct DNA追溯器 {
    static let 基础DNA = "#龍芯⚡️2026-06-20-LONGHUN-DIARY"
    
    // 生成DNA追溯码
    static func 生成DNA(模块: String, 版本: String) -> String {
        let 时间 = ISO8601DateFormatter().string(from: Date())
        let 随机 = String(format: "%04X", Int.random(in: 0...65535))
        return "\(基础DNA)-\(模块)-\(版本)-\(时间)-\(随机)"
    }
    
    // 压缩原文为指纹（平台只存这个，不存原文）
    static func 压缩指纹(原文: String) -> String {
        let 数据 = 原文.data(using: .utf8)!
        let 哈希 = SHA256.hash(data: 数据)
        // 取前16位作为压缩指纹，足够唯一标识
        return 哈希.compactMap { String(format: "%02x", $0) }.joined().prefix(16).description
    }
    
    // 从指纹恢复原文（需要用户提供原文，系统验证指纹匹配）
    static func 验证并恢复(用户提供的原文: String, 存储的指纹: String) -> Bool {
        let 计算指纹 = 压缩指纹(原文: 用户提供的原文)
        return 计算指纹 == 存储的指纹
    }
    
    // 完整哈希链（用于审计）
    static func 哈希链(前一条哈希: String, 当前数据: String) -> String {
        let 输入 = 前一条哈希 + 当前数据
        let 数据 = 输入.data(using: .utf8)!
        let 哈希 = SHA256.hash(data: 数据)
        return 哈希.compactMap { String(format: "%02x", $0) }.joined()
    }
    
    // GPG风格签名（简化版）
    static func 数字签名(内容: String, 私钥: String) -> String {
        let 数据 = (内容 + 私钥).data(using: .utf8)!
        let 哈希 = SHA256.hash(data: 数据)
        return 哈希.compactMap { String(format: "%02x", $0) }.joined().prefix(32).description
    }
}
