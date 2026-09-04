// DNA: #龍芯⚡️丙午·丙申·乙卯·申时·䷐随-IOS-CNSH-v1.0-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
//
// 龍魂·iOS CNSH 语义客户端
// 中文神经符号混合语言 · 意图路由 · DNA 追溯（iOS 简化版·完整干支卦由鲲鹏引擎生成）

import Foundation

/// CNSH 语义客户端
public struct CNSHClient: Sendable {

    public static let shared = CNSHClient()

    // MARK: - 三色审计

    /// 三色审计判定（与服务器同标）
    public static func threeColor(score: Double, redline: Bool = false) -> AuditMark {
        if redline { return .red }
        if score >= 80 { return .green }
        return .yellow
    }

    // MARK: - 洛书数字根

    /// 数字根（洛书 369 不动点）
    public static func digitalRoot(_ n: Int) -> Int {
        var x = abs(n)
        while x >= 10 {
            x = String(x).compactMap { $0.wholeNumberValue }.reduce(0, +)
        }
        return x
    }

    // MARK: - 意图路由（CNSH 语义抽屉匹配）

    public enum Intent: String, Sendable {
        case audit    // 审计/检查/有没有问题
        case security // 安全/漏洞/渗透
        case math     // 算/数字/权重
        case deploy   // 部署/上线/发布
        case write    // 写/开发/代码
        case query    // 查/搜/找
        case general  // 其他
    }

    /// 关键词路由表（与服务器语义协议对齐）
    public static func routeIntent(_ text: String) -> Intent {
        let t = text.lowercased()
        let audit = ["审计", "检查", "审查", "有没有问题", "audit", "review", "问题"]
        let security = ["安全", "漏洞", "渗透", "红蓝", "扫描", "security", "vuln"]
        let math = ["算一下", "数字根", "权重", "五行", "八卦", "calculate", "weight"]
        let deploy = ["部署", "上线", "发布", "回滚", "deploy", "release"]
        let write = ["写", "开发", "代码", "实现", "build", "develop", "写个"]
        let query = ["查", "搜", "找一下", "search", "query", "帮我查"]

        if audit.contains(where: { t.contains($0) }) { return .audit }
        if security.contains(where: { t.contains($0) }) { return .security }
        if math.contains(where: { t.contains($0) }) { return .math }
        if deploy.contains(where: { t.contains($0) }) { return .deploy }
        if write.contains(where: { t.contains($0) }) { return .write }
        if query.contains(where: { t.contains($0) }) { return .query }
        return .general
    }

    // MARK: - DNA 追溯（iOS 简化格式）

    /// DNA 追溯码生成
    /// 简化格式: #龍芯⚡️YYYYMMDD-<模块>-<动作>-<SM3哈希8>
    /// 完整干支卦格式由鲲鹏时间引擎生成（服务器权威）
    public static func dNaStamp(module: String, action: String, payload: String = "") -> String {
        let fmt = DateFormatter()
        fmt.dateFormat = "yyyyMMdd"
        fmt.timeZone = .current
        let date = fmt.string(from: Date())
        let hash = LonghunCrypto.sm3Hex(module + action + payload + date)
        return "#龍芯⚡️\(date)-\(module)-\(action)-\(String(hash.prefix(8)))"
    }

    /// DNA 验证（校验哈希前 8 位；哈希与 dNaStamp 一致：module+action+payload+date）
    public static func verifyDNA(_ dna: String, module: String, action: String, payload: String = "") -> Bool {
        let parts = dna.components(separatedBy: "-")
        guard parts.count >= 4 else { return false }
        guard parts[1] == module, parts[2] == action else { return false }
        let date = String(parts[0].suffix(8))
        let expected = String(LonghunCrypto.sm3Hex(module + action + payload + date).prefix(8))
        return parts[3] == expected
    }
}
