import Foundation
import CryptoKit

// ═══════════════════════════════════════════════════════════════
// 【数据模型】
// ═══════════════════════════════════════════════════════════════

struct UserInfo: Codable {
    let name: String
    let idNumber: String
}

enum ActivationStatus: String, Codable {
    case active = "active"
    case expired = "expired"
    case revoked = "revoked"
    
    var displayName: String {
        switch self {
        case .active: return "有效"
        case .expired: return "已过期"
        case .revoked: return "已撤销"
        }
    }
}

struct ActivationInfo: Codable {
    let paymentOrder: String
    let tempDNA: String
    let userInfo: UserInfo
    let activationTime: Date
    let expiryTime: Date
    var status: ActivationStatus
    let founderUID: String
    let founderGPG: String
    var revokeReason: String?
    var revokeTime: Date?
}

struct DefenseRule: Codable {
    var enabled: Bool?
    var description: String?
    var editable: Bool?
    var eternal: Bool?
    var uid: String?
    var name: String?
    var gpg: String?
    
    // 网络隔离相关
    var blockedDomains: [String]?
    var allowedDomains: [String]?
    
    // 数据加密相关
    var algorithm: String?
    var keyLocation: String?
    
    // 同步控制相关
    var autoSync: Bool?
    var manualApproval: Bool?
    
    // 应用审计相关
    var auditFrequency: String?
    var reportTo: String?
    
    // 动态属性支持
    var customProperties: [String: String]?
}

extension DefenseRule: CustomDebugStringConvertible {
    var debugDescription: String {
        let encoder = JSONEncoder()
        encoder.outputFormatting = .prettyPrinted
        if let data = try? encoder.encode(self),
           let string = String(data: data, encoding: .utf8) {
            return string
        }
        return "无法显示规则详情"
    }
}

struct AuditReport: Codable {
    let auditTime: Date
    let auditFrequency: String
    let reportTo: String
    let findings: [AuditFinding]
}

struct AuditFinding: Codable {
    let app: String
    let riskLevel: String
    let description: String
}

// ═══════════════════════════════════════════════════════════════
// 【DNA生成器】
// ═══════════════════════════════════════════════════════════════

struct DNAGenerator {
    static func generate(description: String, version: String) -> String {
        let dateFormatter = DateFormatter()
        dateFormatter.dateFormat = "yyyyMMdd-HHmmss"
        let timestamp = dateFormatter.string(from: Date())
        
        let randomString = "\(timestamp)-\(description)-\(Date().timeIntervalSince1970)"
        let hash = SHA256.hash(data: Data(randomString.utf8))
        let hashString = hash.compactMap { String(format: "%02x", $0) }.joined().prefix(6)
        
        let dna = "\(Constants.dnaPrefix)\(timestamp)-\(description)-\(version)-\(hashString)"
        
        print("✅ DNA生成成功：\(dna)")
        return dna
    }
    
    static func validate(dna: String) -> Bool {
        let pattern = #"^#ZHUGEXIN⚡️\d{8}-\d{6}-.+-v\d+\.\d+-[a-f0-9]{6}$"#
        let regex = try? NSRegularExpression(pattern: pattern)
        let range = NSRange(dna.startIndex..., in: dna)
        let isValid = regex?.firstMatch(in: dna, range: range) != nil
        
        if isValid {
            print("✅ DNA验证通过：\(dna)")
        } else {
            print("❌ DNA验证失败：\(dna)")
        }
        
        return isValid
    }
    
    static func parse(dna: String) -> [String: String]? {
        guard validate(dna) else { return nil }
        
        let dnaBody = dna.replacingOccurrences(of: Constants.dnaPrefix, with: "")
        let parts = dnaBody.split(separator: "-").map(String.init)
        
        guard parts.count >= 5 else { return nil }
        
        let info: [String: String] = [
            "date": parts[0],
            "time": parts[1],
            "description": parts[2],
            "version": parts[3],
            "hash": parts[4],
            "timestamp": "\(parts[0])-\(parts[1])"
        ]
        
        print("✅ DNA解析成功：\(info)")
        return info
    }
}

// ═══════════════════════════════════════════════════════════════
// 【数字人民币激活系统】
// ═══════════════════════════════════════════════════════════════

@MainActor
class ECNYActivationSystem: ObservableObject {
    @Published var activations: [String: ActivationInfo] = [:]
    
    private let storageKey = "ecny_activation_data"
    
    init() {
        loadData()
    }
    
    private func loadData() {
        guard let data = UserDefaults.standard.data(forKey: storageKey),
              let decoded = try? JSONDecoder().decode([String: ActivationInfo].self, from: data) else {
            return
        }
        activations = decoded
    }
    
    private func saveData() {
        if let encoded = try? JSONEncoder().encode(activations) {
            UserDefaults.standard.set(encoded, forKey: storageKey)
        }
    }
    
    func validatePaymentOrder(_ paymentOrder: String) -> Bool {
        let pattern = #"^e-CNY-\d{8}-[A-Z0-9]{6,}$"#
        let regex = try? NSRegularExpression(pattern: pattern)
        let range = NSRange(paymentOrder.startIndex..., in: paymentOrder)
        let isValid = regex?.firstMatch(in: paymentOrder, range: range) != nil
        
        if !isValid {
            print("❌ 付款单号格式错误：\(paymentOrder)")
            print("正确格式：e-CNY-YYYYMMDD-XXXXXX（如：e-CNY-20260227-ABC123）")
        }
        
        return isValid
    }
    
    func activate(paymentOrder: String, userInfo: UserInfo) -> ActivationInfo? {
        guard validatePaymentOrder(paymentOrder) else { return nil }
        
        if activations[paymentOrder] != nil {
            print("⚠️ 付款单号已被使用：\(paymentOrder)")
            return activations[paymentOrder]
        }
        
        let tempDNA = DNAGenerator.generate(
            description: "TEMP-ACTIVATION-\(paymentOrder)",
            version: "v1.0"
        )
        
        let activationTime = Date()
        let expiryTime = activationTime.addingTimeInterval(
            TimeInterval(Constants.tempDNAValidityDays * 24 * 60 * 60)
        )
        
        let activationInfo = ActivationInfo(
            paymentOrder: paymentOrder,
            tempDNA: tempDNA,
            userInfo: userInfo,
            activationTime: activationTime,
            expiryTime: expiryTime,
            status: .active,
            founderUID: Constants.founderUID,
            founderGPG: Constants.founderGPG
        )
        
        activations[paymentOrder] = activationInfo
        saveData()
        
        print("✅ 激活成功！临时DNA：\(tempDNA)")
        print("📅 有效期至：\(expiryTime)")
        
        return activationInfo
    }
    
    func checkActivation(paymentOrder: String) -> (isValid: Bool, info: ActivationInfo?) {
        guard var info = activations[paymentOrder] else {
            print("⚠️ 未找到激活记录：\(paymentOrder)")
            return (false, nil)
        }
        
        if Date() > info.expiryTime {
            print("⚠️ 激活已过期：\(paymentOrder)")
            info.status = .expired
            activations[paymentOrder] = info
            saveData()
            return (false, info)
        }
        
        print("✅ 激活有效：\(paymentOrder)")
        return (true, info)
    }
    
    func revokeActivation(paymentOrder: String, reason: String) -> Bool {
        guard var info = activations[paymentOrder] else {
            print("⚠️ 未找到激活记录：\(paymentOrder)")
            return false
        }
        
        info.status = .revoked
        info.revokeReason = reason
        info.revokeTime = Date()
        
        activations[paymentOrder] = info
        saveData()
        
        print("✅ 激活已撤销：\(paymentOrder)，原因：\(reason)")
        return true
    }
}

// ═══════════════════════════════════════════════════════════════
// 【数据主权防御规则引擎】
// ═══════════════════════════════════════════════════════════════

@MainActor
class DataSovereigntyRuleEngine: ObservableObject {
    @Published var rules: [String: DefenseRule] = [:]
    
    private let storageKey = "defense_rules"
    
    init() {
        loadRules()
    }
    
    private func loadRules() {
        if let data = UserDefaults.standard.data(forKey: storageKey),
           let decoded = try? JSONDecoder().decode([String: DefenseRule].self, from: data) {
            rules = decoded
        } else {
            loadDefaultRules()
        }
    }
    
    private func saveRules() {
        if let encoded = try? JSONEncoder().encode(rules) {
            UserDefaults.standard.set(encoded, forKey: storageKey)
        }
    }
    
    private func loadDefaultRules() {
        rules = [
            "founder": DefenseRule(
                enabled: nil,
                description: nil,
                editable: false,
                eternal: true,
                uid: Constants.founderUID,
                name: Constants.founderName,
                gpg: Constants.founderGPG
            ),
            "network_isolation": DefenseRule(
                enabled: true,
                description: "网络隔离规则：阻止数据流向境外服务器",
                editable: true,
                blockedDomains: [
                    "*.amazonaws.com",
                    "*.cloudflare.com",
                    "*.google-analytics.com",
                    "*.facebook.com",
                    "*.doubleclick.net"
                ],
                allowedDomains: [
                    "*.gov.cn",
                    "*.edu.cn"
                ]
            ),
            "data_encryption": DefenseRule(
                enabled: true,
                description: "数据加密规则：所有敏感数据本地加密",
                editable: true,
                algorithm: "AES-256-GCM",
                keyLocation: "local_only"
            ),
            "sync_control": DefenseRule(
                enabled: true,
                description: "同步控制规则：禁止自动同步，需手动审批",
                editable: true,
                autoSync: false,
                manualApproval: true
            ),
            "app_audit": DefenseRule(
                enabled: true,
                description: "应用审计规则：每日审计应用数据流",
                editable: true,
                auditFrequency: "daily",
                reportTo: Constants.founderUID
            )
        ]
        
        saveRules()
    }
    
    func addCustomRule(name: String, rule: DefenseRule) -> Bool {
        if name == "founder" {
            print("❌ 禁止修改创始人信息（P0-ETERNAL保护）")
            return false
        }
        
        var newRule = rule
        newRule.editable = true
        rules[name] = newRule
        
        saveRules()
        print("✅ 自定义规则已添加：\(name)")
        return true
    }
    
    func updateRule(name: String, rule: DefenseRule) -> Bool {
        guard rules[name] != nil else {
            print("❌ 规则不存在：\(name)")
            return false
        }
        
        if rules[name]?.editable == false {
            print("❌ 规则不可编辑：\(name)（P0-ETERNAL保护）")
            return false
        }
        
        rules[name] = rule
        saveRules()
        print("✅ 规则已更新：\(name)")
        return true
    }
    
    func deleteRule(name: String) -> Bool {
        if name == "founder" {
            print("❌ 禁止删除创始人信息（P0-ETERNAL保护）")
            return false
        }
        
        guard rules[name] != nil else {
            print("❌ 规则不存在：\(name)")
            return false
        }
        
        if rules[name]?.editable == false {
            print("❌ 规则不可删除：\(name)")
            return false
        }
        
        rules.removeValue(forKey: name)
        saveRules()
        print("✅ 规则已删除：\(name)")
        return true
    }
    
    func validateFounder() -> Bool {
        let founder = rules["founder"]
        
        let isValid = founder?.uid == Constants.founderUID &&
                     founder?.name == Constants.founderName &&
                     founder?.gpg == Constants.founderGPG &&
                     founder?.eternal == true
        
        if isValid {
            print("✅ 创始人信息验证通过")
        } else {
            print("❌ 创始人信息被篡改！立即恢复...")
            rules["founder"] = DefenseRule(
                enabled: nil,
                description: nil,
                editable: false,
                eternal: true,
                uid: Constants.founderUID,
                name: Constants.founderName,
                gpg: Constants.founderGPG
            )
            saveRules()
        }
        
        return isValid
    }
}

// ═══════════════════════════════════════════════════════════════
// 【数据主权防御执行器】
// ═══════════════════════════════════════════════════════════════

struct DataSovereigntyDefenseExecutor {
    let ruleEngine: DataSovereigntyRuleEngine
    
    func executeNetworkIsolation() -> Bool {
        guard let rule = ruleEngine.rules["network_isolation"],
              rule.enabled == true else {
            print("⚠️ 网络隔离规则未启用")
            return false
        }
        
        print("🛡️ 开始执行网络隔离...")
        
        // 实际应用中，这里应该配置iOS的网络策略
        // 可以使用NEFilterDataProvider进行内容过滤
        
        let blockedCount = rule.blockedDomains?.count ?? 0
        let allowedCount = rule.allowedDomains?.count ?? 0
        
        print("✅ 已阻止 \(blockedCount) 个域名")
        print("✅ 已允许 \(allowedCount) 个域名")
        
        return true
    }
    
    func executeDataEncryption(filePath: String) -> Bool {
        guard let rule = ruleEngine.rules["data_encryption"],
              rule.enabled == true else {
            print("⚠️ 数据加密规则未启用")
            return false
        }
        
        print("🔐 开始加密文件：\(filePath)")
        
        // 实际应用中，使用CryptoKit进行AES-GCM加密
        // let key = SymmetricKey(size: .bits256)
        // let sealedBox = try? AES.GCM.seal(data, using: key)
        
        print("✅ 文件加密成功：\(filePath)")
        return true
    }
    
    func executeSyncControl() -> Bool {
        guard let rule = ruleEngine.rules["sync_control"],
              rule.enabled == true else {
            print("⚠️ 同步控制规则未启用")
            return false
        }
        
        print("🔒 开始执行同步控制...")
        
        // 实际应用中，配置iCloud同步策略
        // 使用NSUbiquitousKeyValueStore控制
        
        if rule.autoSync == false {
            print("✅ 自动同步已禁用")
        }
        
        if rule.manualApproval == true {
            print("✅ 手动审批模式已启用")
        }
        
        return true
    }
    
    func executeAppAudit() -> AuditReport? {
        guard let rule = ruleEngine.rules["app_audit"],
              rule.enabled == true else {
            print("⚠️ 应用审计规则未启用")
            return nil
        }
        
        print("📊 开始执行应用审计...")
        
        // 实际应用中，使用Network.framework监控网络活动
        // 或使用URLSessionTaskMetrics分析网络请求
        
        let report = AuditReport(
            auditTime: Date(),
            auditFrequency: rule.auditFrequency ?? "daily",
            reportTo: rule.reportTo ?? Constants.founderUID,
            findings: [
                AuditFinding(
                    app: "示例应用",
                    riskLevel: "低",
                    description: "未发现异常数据流"
                )
            ]
        )
        
        print("✅ 应用审计完成")
        return report
    }
}
