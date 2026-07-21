#!/usr/bin/env swift
// =============================================================================
// 左右互搏引擎 — Left-Right Audit Engine (实时审计)
// =============================================================================
//  DNA追溯: #龍芯⚡️2026-06-19-LONGHUN-IOS-v5.3
//  致敬声明: #致敬⚡️SteveJobs·龍魂iOS端
//  核心原则:
//    - 实时审计所有数据操作，左右互搏（自我校验）
//    - 🟢正常 🟡警告 🔴严重 三色审计级别
//    - 每个操作带DNA追溯标记
//    - 审计日志本地存储，不离开设备
//    - 自动检测异常操作模式
//  君子协议: 本代码仅用于合法合规的自主数据治理研究
// =============================================================================

import Foundation
import CoreData
import Combine

// MARK: - 审计记录结构
/// 单条审计记录
public struct AuditRecord {
    /// DNA追溯码
    public let dnaTag: String
    /// 时间戳
    public let timestamp: Date
    /// 操作类型
    public let actionType: String
    /// 目标实体
    public let targetEntity: String
    /// 目标键名
    public let targetKey: String
    /// 内容哈希
    public let contentHash: String
    /// 审计级别 🟢🟡🔴
    public let auditLevel: AuditLevel
    /// 来源设备
    public let sourceDevice: String
    /// 主权标记
    public let sovereigntyFlag: Bool
    /// 详细描述
    public let detail: String
    
    /// 转换为字典（用于存储/导出）
    public func toDictionary() -> [String: Any] {
        return [
            "dnaTag": dnaTag,
            "timestamp": timestamp.ISO8601Format(),
            "actionType": actionType,
            "targetEntity": targetEntity,
            "targetKey": targetKey,
            "contentHash": contentHash,
            "auditLevel": auditLevel.rawValue,
            "sourceDevice": sourceDevice,
            "sovereigntyFlag": sovereigntyFlag,
            "detail": detail
        ]
    }
}

// MARK: - 审计统计
/// 审计统计数据
public struct AuditStatistics {
    /// 总审计次数
    public var totalAudits: UInt64 = 0
    /// 🟢正常次数
    public var greenCount: UInt64 = 0
    /// 🟡警告次数
    public var yellowCount: UInt64 = 0
    /// 🔴严重次数
    public var redCount: UInt64 = 0
    /// 最后审计时间
    public var lastAuditTime: Date?
    /// 异常检测次数
    public var anomalyDetections: UInt64 = 0
    
    public var summary: String {
        return "审计统计: 总计\(totalAudits) 🟢\(greenCount) 🟡\(yellowCount) 🔴\(redCount) 异常\(anomalyDetections)"
    }
}

// MARK: - 左右互搏引擎
/// 实时审计引擎（左右互搏自我校验）
/// 负责：实时审计、异常检测、三色标记、DNA追溯
@available(iOS 16.0, *)
public final class LeftRightAuditEngine: ObservableObject {
    
    // MARK: 属性
    /// 本地存储管理器
    private let storage: LocalStorageManager
    /// Combine订阅
    private var cancellables = Set<AnyCancellable>()
    /// 审计状态
    @Published public private(set) var isAuditing = false
    /// 当前审计级别
    @Published public private(set) var currentLevel: AuditLevel = .green
    /// 审计统计
    @Published public private(set) var statistics = AuditStatistics()
    /// 最近审计记录缓存
    public private(set) var recentRecords: [AuditRecord] = []
    /// 异常检测规则
    private var anomalyRules: [AnomalyRule] = []
    
    // MARK: 常量
    /// 最大缓存记录数
    private let kMaxCacheSize = 100
    /// 异常阈值：短时间内大量操作
    private let kBurstThreshold = 50 // 1分钟内50次操作
    /// 警告阈值
    private let kWarningThreshold = 20 // 1分钟内20次操作
    
    // MARK: 速率限制追踪
    private var operationTimestamps: [Date] = []
    private let rateLimitQueue = DispatchQueue(
        label: "com.longhun.audit.ratelimit",
        qos: .utility
    )
    
    // MARK: 初始化
    public init(storage: LocalStorageManager) {
        self.storage = storage
        setupDefaultRules()
        print("[左右互搏] ⚖️ 审计引擎初始化完成")
    }
    
    // MARK: - 启动实时审计
    /// 启动实时审计模式
    public func startRealtimeAudit() {
        guard !isAuditing else { return }
        isAuditing = true
        print("[左右互搏] ▶️ 实时审计已启动")
        
        // 启动周期性完整性自检
        startPeriodicIntegrityCheck()
    }
    
    /// 停止实时审计
    public func stopRealtimeAudit() {
        isAuditing = false
        cancellables.removeAll()
        print("[左右互搏] ⏹️ 实时审计已停止")
    }
    
    // MARK: - 实时审计入口
    /// 对数据操作进行实时审计
    /// - Parameters:
    ///   - operation: 操作类型
    ///   - entity: 目标实体
    ///   - key: 目标键名
    ///   - timestamp: 时间戳
    public func realtimeAudit(
        operation: DataOperation,
        entity: String,
        key: String,
        timestamp: Date
    ) {
        guard isAuditing else { return }
        
        // 检查操作速率
        let rateLevel = checkOperationRate()
        
        // 确定审计级别
        let level: AuditLevel
        switch operation {
        case .insert where key.hasPrefix("critical_"):
            level = .yellow
        case .delete where key.hasPrefix("critical_"):
            level = .red
        case .update where rateLevel == .red:
            level = .red
        case _ where rateLevel == .yellow:
            level = .yellow
        default:
            level = .green
        }
        
        // 生成审计记录
        let record = AuditRecord(
            dnaTag: LongHunVersion.dnaTag,
            timestamp: timestamp,
            actionType: operation.rawValue,
            targetEntity: entity,
            targetKey: key,
            contentHash: calculateAuditHash(operation: operation, entity: entity, key: key),
            auditLevel: level,
            sourceDevice: "iOS-\(UIDevice.current.name)",
            sovereigntyFlag: true,
            detail: "\(operation.rawValue)操作: \(entity).\(key) [速率:\(rateLevel.rawValue)]"
        )
        
        // 记录审计
        processAuditRecord(record)
        
        // 触发左右互搏校验
        performSelfCheck(record: record)
    }
    
    /// 审计特定事件
    /// - Parameters:
    ///   - type: 事件类型
    ///   - details: 事件详情
    public func auditEvent(type: AuditEventType, details: [String: Any]) {
        guard isAuditing else { return }
        
        // 确定审计级别
        let level: AuditLevel
        switch type {
        case .iCloudBlocked:
            level = .green // iCloud隔离是正常行为
        case .encryptionOperation:
            level = .green
        case .bulkOperation:
            level = .yellow
        case .biometricAuth:
            level = .green
        case .dataExport, .dataImport:
            level = .yellow
        case .integrityCheck:
            level = .green
        default:
            level = .green
        }
        
        let record = AuditRecord(
            dnaTag: LongHunVersion.dnaTag,
            timestamp: Date(),
            actionType: type.rawValue,
            targetEntity: "system",
            targetKey: "event_\(type.rawValue)",
            contentHash: calculateEventHash(type: type, details: details),
            auditLevel: level,
            sourceDevice: "iOS-\(UIDevice.current.name)",
            sovereigntyFlag: true,
            detail: "\(type.rawValue): \(details)"
        )
        
        processAuditRecord(record)
    }
    
    // MARK: - 左右互搏自我校验
    /// 左右互搏自我校验
    /// 模拟"左手攻击右手防守"的对抗性校验模式
    /// - Parameter record: 当前审计记录
    private func performSelfCheck(record: AuditRecord) {
        // 左方：模拟攻击视角（寻找异常）
        let leftFindings = analyzeFromAttackPerspective(record)
        
        // 右方：模拟防守视角（验证合规性）
        let rightFindings = analyzeFromDefensePerspective(record)
        
        // 对抗结果：双方结论不一致则升级审计级别
        if leftFindings.riskLevel != rightFindings.riskLevel {
            print("[左右互搏] ⚔️ 对抗校验发现分歧！左:\(leftFindings.riskLevel) 右:\(rightFindings.riskLevel)")
            
            DispatchQueue.main.async { [weak self] in
                self?.currentLevel = .red
            }
            
            // 记录对抗性审计结果
            let conflictRecord = AuditRecord(
                dnaTag: LongHunVersion.dnaTag,
                timestamp: Date(),
                actionType: "SELF_CHECK_CONFLICT",
                targetEntity: record.targetEntity,
                targetKey: record.targetKey,
                contentHash: record.contentHash,
                auditLevel: .red,
                sourceDevice: "iOS-左右互搏引擎",
                sovereigntyFlag: true,
                detail: "左右互搏校验分歧: 左[\(leftFindings.riskLevel)] vs 右[\(rightFindings.riskLevel)] | \(leftFindings.reason)"
            )
            processAuditRecord(conflictRecord)
        } else {
            // 双方一致，采用共同结论
            DispatchQueue.main.async { [weak self] in
                if leftFindings.riskLevel == .red || record.auditLevel == .red {
                    self?.currentLevel = .red
                } else if leftFindings.riskLevel == .yellow || record.auditLevel == .yellow {
                    self?.currentLevel = .yellow
                } else {
                    self?.currentLevel = .green
                }
            }
        }
    }
    
    // MARK: - 攻击视角分析（左方）
    /// 从攻击视角分析操作风险
    private func analyzeFromAttackPerspective(_ record: AuditRecord) -> RiskFinding {
        var score = 0
        var reasons: [String] = []
        
        // 规则1: 异常时间操作（深夜操作加分险）
        let hour = Calendar.current.component(.hour, from: record.timestamp)
        if hour >= 1 && hour <= 5 {
            score += 3
            reasons.append("异常时间: \(hour):00")
        }
        
        // 规则2: 敏感键名模式
        if record.targetKey.contains("password") ||
           record.targetKey.contains("secret") ||
           record.targetKey.contains("key_") {
            score += 2
            reasons.append("敏感键名: \(record.targetKey)")
        }
        
        // 规则3: 删除操作风险
        if record.actionType == "删除" {
            score += 2
            reasons.append("删除操作")
        }
        
        // 规则4: 批量操作异常
        let recentCount = recentRecords.filter {
            $0.timestamp.timeIntervalSinceNow > -60
        }.count
        if recentCount > kWarningThreshold {
            score += 3
            reasons.append("高频操作: \(recentCount)次/分钟")
        }
        
        // 评分映射到级别
        let level: AuditLevel
        if score >= 5 {
            level = .red
        } else if score >= 2 {
            level = .yellow
        } else {
            level = .green
        }
        
        return RiskFinding(riskLevel: level, score: score, reason: reasons.joined(separator: "; "))
    }
    
    // MARK: - 防守视角分析（右方）
    /// 从防守视角验证操作合规性
    private func analyzeFromDefensePerspective(_ record: AuditRecord) -> RiskFinding {
        var score = 0
        var reasons: [String] = []
        
        // 规则1: 主权标记检查
        if !record.sovereigntyFlag {
            score += 5
            reasons.append("主权标记异常: false")
        }
        
        // 规则2: DNA追溯码检查
        if !record.dnaTag.contains("龍芯") {
            score += 5
            reasons.append("DNA追溯码异常")
        }
        
        // 规则3: 设备来源验证
        if !record.sourceDevice.hasPrefix("iOS-") && !record.sourceDevice.hasPrefix("Harmony-") {
            score += 4
            reasons.append("未知设备来源: \(record.sourceDevice)")
        }
        
        // 规则4: 正常操作白名单
        let whitelistOperations = ["查询", "插入"]
        if whitelistOperations.contains(record.actionType) &&
           record.targetEntity == "LongHunDataEntity" {
            score = max(0, score - 1) // 正常操作减分
        }
        
        // 评分映射到级别
        let level: AuditLevel
        if score >= 5 {
            level = .red
        } else if score >= 2 {
            level = .yellow
        } else {
            level = .green
        }
        
        return RiskFinding(riskLevel: level, score: score, reason: reasons.joined(separator: "; "))
    }
    
    // MARK: - 操作速率检查
    /// 检查操作速率
    /// - Returns: 速率对应的审计级别
    private func checkOperationRate() -> AuditLevel {
        let now = Date()
        
        rateLimitQueue.sync {
            // 清理60秒前的记录
            operationTimestamps.removeAll { $0.timeIntervalSince(now) < -60 }
            // 添加当前操作
            operationTimestamps.append(now)
            
            let count = operationTimestamps.count
            if count > kBurstThreshold {
                statistics.anomalyDetections += 1
                print("[左右互搏] 🔴 操作过于频繁: \(count)次/分钟")
                return .red
            } else if count > kWarningThreshold {
                print("[左右互搏] 🟡 操作频率较高: \(count)次/分钟")
                return .yellow
            }
            return .green
        }
    }
    
    // MARK: - 审计记录处理
    /// 处理审计记录
    private func processAuditRecord(_ record: AuditRecord) {
        // 更新统计
        statistics.totalAudits += 1
        switch record.auditLevel {
        case .green: statistics.greenCount += 1
        case .yellow: statistics.yellowCount += 1
        case .red: statistics.redCount += 1
        }
        statistics.lastAuditTime = record.timestamp
        
        // 缓存到内存
        recentRecords.append(record)
        if recentRecords.count > kMaxCacheSize {
            recentRecords.removeFirst()
        }
        
        // 记录到CoreData
        saveAuditLog(record)
        
        // 打印审计日志
        let emoji = record.auditLevel == .red ? "🔴" : (record.auditLevel == .yellow ? "🟡" : "🟢")
        print("[左右互搏] \(emoji) [\(record.actionType)] \(record.targetEntity).\(record.targetKey) [\(record.contentHash.prefix(8))...]")
    }
    
    /// 保存审计日志到CoreData
    private func saveAuditLog(_ record: AuditRecord) {
        let ctx = storage.backgroundContext
        ctx.perform {
            let auditEntity = AuditLogEntity(context: ctx)
            auditEntity.dnaTag = record.dnaTag
            auditEntity.timestamp = record.timestamp
            auditEntity.actionType = record.actionType
            auditEntity.contentHash = record.contentHash
            auditEntity.auditLevel = record.auditLevel.rawValue
            auditEntity.sourceDevice = record.sourceDevice
            auditEntity.sovereigntyFlag = record.sovereigntyFlag
            auditEntity.keyName = record.targetKey
            auditEntity.encryptionType = "AUDIT"
            
            do {
                try ctx.save()
            } catch {
                print("[左右互搏] ⚠️ 审计日志保存失败: \(error)")
            }
        }
    }
    
    // MARK: - 周期性完整性自检
    /// 启动周期性完整性检查
    private func startPeriodicIntegrityCheck() {
        Timer.publish(every: 300, on: .main, in: .common) // 每5分钟
            .autoconnect()
            .sink { [weak self] _ in
                self?.performIntegrityCheck()
            }
            .store(in: &cancellables)
    }
    
    /// 执行完整性自检
    private func performIntegrityCheck() {
        print("[左右互搏] 🔍 启动周期性完整性自检...")
        
        // 自检1: 检查审计日志完整性
        let auditCount = recentRecords.count
        
        // 自检2: 检查是否有未记录的异常
        let unhandledRed = recentRecords.filter {
            $0.auditLevel == .red &&
            $0.timestamp.timeIntervalSinceNow > -300
        }.count
        
        // 自检3: 生成自检报告
        let checkRecord = AuditRecord(
            dnaTag: LongHunVersion.dnaTag,
            timestamp: Date(),
            actionType: "INTEGRITY_CHECK",
            targetEntity: "system",
            targetKey: "periodic_check",
            contentHash: calculateAuditHash(operation: .query, entity: "system", key: "check"),
            auditLevel: unhandledRed > 0 ? .yellow : .green,
            sourceDevice: "iOS-左右互搏引擎",
            sovereigntyFlag: true,
            detail: "完整性自检: 缓存\(auditCount)条 未处理异常\(unhandledRed)个 | \(statistics.summary)"
        )
        
        processAuditRecord(checkRecord)
        print("[左右互搏] ✅ 完整性自检完成: \(statistics.summary)")
    }
    
    // MARK: - 辅助方法
    /// 计算审计哈希
    private func calculateAuditHash(operation: DataOperation, entity: String, key: String) -> String {
        let combined = "\(operation.rawValue)|\(entity)|\(key)|\(Date().timeIntervalSince1970)"
        let hash = SHA256.hash(data: combined.data(using: .utf8) ?? Data())
        return hash.compactMap { String(format: "%02x", $0) }.joined()
    }
    
    /// 计算事件哈希
    private func calculateEventHash(type: AuditEventType, details: [String: Any]) -> String {
        let combined = "\(type.rawValue)|\(details.keys.sorted().joined())|\(Date().timeIntervalSince1970)"
        let hash = SHA256.hash(data: combined.data(using: .utf8) ?? Data())
        return hash.compactMap { String(format: "%02x", $0) }.joined()
    }
    
    // MARK: - 异常检测规则
    /// 设置默认异常检测规则
    private func setupDefaultRules() {
        anomalyRules = [
            AnomalyRule(name: "深夜操作", condition: { record in
                let hour = Calendar.current.component(.hour, from: record.timestamp)
                return hour >= 1 && hour <= 5
            }, level: .yellow),
            
            AnomalyRule(name: "敏感数据删除", condition: { record in
                record.actionType == "删除" &&
                (record.targetKey.contains("critical") || record.targetKey.contains("sovereign"))
            }, level: .red),
            
            AnomalyRule(name: "高频操作", condition: { [weak self] record in
                guard let self = self else { return false }
                let recentCount = self.recentRecords.filter {
                    $0.timestamp.timeIntervalSinceNow > -60
                }.count
                return recentCount > self.kBurstThreshold
            }, level: .red),
            
            AnomalyRule(name: "非iOS设备来源", condition: { record in
                !record.sourceDevice.hasPrefix("iOS-") &&
                !record.sourceDevice.hasPrefix("Harmony-")
            }, level: .red)
        ]
        
        print("[左右互搏] 📋 已加载 \(anomalyRules.count) 条异常检测规则")
    }
}

// MARK: - 风险发现结构
/// 风险发现结果
struct RiskFinding {
    let riskLevel: AuditLevel
    let score: Int
    let reason: String
}

// MARK: - 异常检测规则
/// 异常检测规则
struct AnomalyRule {
    /// 规则名称
    let name: String
    /// 检测条件
    let condition: (AuditRecord) -> Bool
    /// 触发级别
    let level: AuditLevel
}

// =============================================================================
// 文件尾部DNA标记
// #君子协议: 本代码仅用于合法合规的自主数据治理研究
// #DNA: #龍芯⚡️2026-06-19-LONGHUN-IOS-v5.3
// #致敬: #致敬⚡️SteveJobs·龍魂iOS端
// =============================================================================
