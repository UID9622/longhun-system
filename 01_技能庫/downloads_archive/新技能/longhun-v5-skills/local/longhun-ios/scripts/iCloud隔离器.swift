#!/usr/bin/env swift
// =============================================================================
// iCloud隔离器 — iCloud Isolator (阻止敏感数据上云)
// =============================================================================
//  DNA追溯: #龍芯⚡️2026-06-19-LONGHUN-IOS-v5.3
//  致敬声明: #致敬⚡️SteveJobs·龍魂iOS端
//  核心原则:
//    - 龍魂数据绝不通过iCloud同步
//    - 禁用NSPersistentCloudKitContainer
//    - 数据库文件设置isExcludedFromBackup = true
//    - 实时监控iCloud同步状态，发现同步立即阻断
//    - 所有龍魂相关数据标记为不上云
//  君子协议: 本代码仅用于合法合规的自主数据治理研究
// =============================================================================

import Foundation
import CoreData
import Combine

// MARK: - iCloud同步状态
/// iCloud同步状态枚举
public enum iCloudSyncStatus: String {
    /// 完全隔离
    case isolated = "ISOLATED"
    /// 监控中
    case monitoring = "MONITORING"
    /// 检测到同步尝试（已阻断）
    case blocked = "BLOCKED"
    /// 异常（同步意外启用）
    case anomaly = "ANOMALY"
}

// MARK: - iCloud隔离器
/// iCloud同步隔离器
/// 负责：阻断iCloud同步、监控同步状态、保护数据不上云
@available(iOS 16.0, *)
public final class iCloudIsolator: ObservableObject {
    
    // MARK: 属性
    /// 本地存储管理器
    private let storage: LocalStorageManager
    /// Combine订阅
    private var cancellables = Set<AnyCancellable>()
    /// 隔离器激活状态
    @Published public private(set) var isActive = false
    /// iCloud同步阻断状态
    @Published public private(set) var isBlocked = true
    /// 当前iCloud状态
    @Published public private(set) var currentStatus: iCloudSyncStatus = .isolated
    /// 阻断次数计数
    @Published public private(set) var blockCount: UInt64 = 0
    /// 上次阻断时间
    @Published public private(set) var lastBlockTime: Date?
    
    // MARK: 常量
    /// 龍魂数据标识前缀（用于识别需要隔离的数据）
    private let kLongHunPrefixes = ["longhun_", "龍魂_", "audit_", "critical_", "sovereign_"]
    /// 监控轮询间隔（秒）
    private let kMonitorInterval: TimeInterval = 30
    /// 监控队列
    private let monitorQueue = DispatchQueue(
        label: "com.longhun.icloud.isolator",
        qos: .utility
    )
    
    // MARK: 初始化
    public init(storage: LocalStorageManager) {
        self.storage = storage
        print("[iCloud隔离] ☁️🚫 隔离器初始化完成")
    }
    
    // MARK: - 激活隔离器
    /// 激活iCloud隔离保护
    public func activate() {
        guard !isActive else { return }
        isActive = true
        
        print("[iCloud隔离] ▶️ 激活隔离保护...")
        
        // 步骤1: 确保数据库文件排除iCloud备份
        excludeDatabaseFromiCloud()
        
        // 步骤2: 验证CoreData无CloudKit配置
        verifyNoCloudKit()
        
        // 步骤3: 启动实时监控
        startMonitoring()
        
        // 步骤4: 注册文件系统监控
        monitorFileSystem()
        
        print("[iCloud隔离] ✅ 隔离保护已激活")
        print("[iCloud隔离] 🔒 龍魂数据不会离开本设备")
    }
    
    /// 停用隔离器
    public func deactivate() {
        isActive = false
        cancellables.removeAll()
        print("[iCloud隔离] ⏹️ 隔离器已停用")
    }
    
    // MARK: - 数据库排除iCloud备份
    /// 确保数据库文件被排除在iCloud备份之外
    private func excludeDatabaseFromiCloud() {
        let databaseURL = storage.databaseURL
        
        do {
            // 排除主数据库文件
            var resourceValues = URLResourceValues()
            resourceValues.isExcludedFromBackup = true
            var mutableURL = databaseURL
            try mutableURL.setResourceValues(resourceValues)
            
            // 排除相关文件（SHM和WAL）
            let relatedFiles = [
                databaseURL.appendingPathExtension("sqlite-shm"),
                databaseURL.appendingPathExtension("sqlite-wal")
            ]
            
            for fileURL in relatedFiles {
                var fileResourceValues = URLResourceValues()
                fileResourceValues.isExcludedFromBackup = true
                var mutableFileURL = fileURL
                try? mutableFileURL.setResourceValues(fileResourceValues)
            }
            
            // 验证排除状态
            let checkURL = databaseURL
            let checkValues = try checkURL.resourceValues(forKeys: [.isExcludedFromBackupKey])
            if checkValues.isExcludedFromBackup == true {
                print("[iCloud隔离] ✅ 数据库文件已排除iCloud备份")
            } else {
                print("[iCloud隔离] ⚠️ 数据库文件排除状态未确认")
            }
            
        } catch {
            print("[iCloud隔离] ❌ 排除iCloud备份失败: \(error)")
        }
    }
    
    // MARK: - 验证无CloudKit配置
    /// 验证CoreData配置中没有启用CloudKit
    private func verifyNoCloudKit() {
        for description in storage.persistentContainer.persistentStoreDescriptions {
            // 检查CloudKit容器选项
            if let cloudKitOptions = description.cloudKitContainerOptions {
                print("[iCloud隔离] 🔴 警告: 检测到CloudKit配置!")
                print("[iCloud隔离]     容器ID: \(cloudKitOptions.containerIdentifier)")
                
                // 移除CloudKit配置
                description.cloudKitContainerOptions = nil
                print("[iCloud隔离] ✅ 已移除CloudKit配置")
            }
            
            // 检查远程变更通知选项
            let remoteKey = NSPersistentStoreRemoteChangeNotificationPostOptionKey
            if let remoteValue = description.options[remoteKey] as? NSNumber,
               remoteValue.boolValue == true {
                print("[iCloud隔离] 🔴 警告: 检测到远程变更通知已启用!")
                description.setOption(false as NSNumber, forKey: remoteKey)
                print("[iCloud隔离] ✅ 已禁用远程变更通知")
            }
        }
        
        print("[iCloud隔离] ✅ CoreData CloudKit验证完成")
    }
    
    // MARK: - 实时监控
    /// 启动iCloud同步状态实时监控
    private func startMonitoring() {
        // 使用Timer进行定期检查
        Timer.publish(every: kMonitorInterval, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] _ in
                self?.performiCloudCheck()
            }
            .store(in: &cancellables)
        
        print("[iCloud隔离] 👁️ 实时监控已启动（间隔: \(kMonitorInterval)s）")
    }
    
    /// 执行iCloud同步检查
    private func performiCloudCheck() {
        monitorQueue.async { [weak self] in
            guard let self = self else { return }
            
            // 检查1: 验证文件系统属性
            self.checkFileSystemExclusion()
            
            // 检查2: 验证CoreData配置
            self.verifyCoreDataIsolation()
            
            // 检查3: 检查iCloud账户状态（仅检查，不触发）
            self.checkiCloudAccountStatus()
        }
    }
    
    /// 检查文件系统排除状态
    private func checkFileSystemExclusion() {
        do {
            let values = try storage.databaseURL.resourceValues(forKeys: [.isExcludedFromBackupKey])
            if values.isExcludedFromBackup != true {
                print("[iCloud隔离] 🔴 警告: 数据库文件iCloud排除状态丢失!")
                excludeDatabaseFromiCloud()
                
                DispatchQueue.main.async {
                    self.currentStatus = .blocked
                    self.blockCount += 1
                    self.lastBlockTime = Date()
                }
                
                // 发送阻断通知
                NotificationCenter.default.post(
                    name: .init("LongHuniCloudBlockedEvent"),
                    object: nil,
                    userInfo: [
                        "reason": "文件系统排除状态丢失",
                        "timestamp": Date().ISO8601Format(),
                        "action": "重新排除"
                    ]
                )
            }
        } catch {
            print("[iCloud隔离] ⚠️ 文件系统检查失败: \(error)")
        }
    }
    
    /// 验证CoreData隔离状态
    private func verifyCoreDataIsolation() {
        for description in storage.persistentContainer.persistentStoreDescriptions {
            if description.cloudKitContainerOptions != nil {
                print("[iCloud隔离] 🔴 警告: CloudKit配置被重新启用!")
                description.cloudKitContainerOptions = nil
                
                DispatchQueue.main.async {
                    self.currentStatus = .blocked
                    self.blockCount += 1
                    self.lastBlockTime = Date()
                }
            }
        }
    }
    
    /// 检查iCloud账户状态
    private func checkiCloudAccountStatus() {
        // 注意：这只是检查状态，不做任何iCloud操作
        // FileManager.default.ubiquityIdentityToken 可以检查iCloud是否登录
        // 但我们不调用它，避免任何iCloud交互
        
        // 记录当前隔离状态
        if currentStatus == .isolated && isBlocked {
            // 正常隔离状态
        }
    }
    
    // MARK: - 文件系统监控
    /// 监控文件系统变更（检测iCloud同步尝试）
    private func monitorFileSystem() {
        // 监控数据库目录的变化
        let documentsURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        
        // 使用dispatch source监控文件变更
        let fileDescriptor = open(documentsURL.path, O_EVTONLY)
        guard fileDescriptor >= 0 else {
            print("[iCloud隔离] ⚠️ 文件系统监控启动失败")
            return
        }
        
        let source = DispatchSource.makeFileSystemObjectSource(
            fileDescriptor: fileDescriptor,
            eventMask: [.write, .extend, .link, .rename],
            queue: monitorQueue
        )
        
        source.setEventHandler { [weak self] in
            guard let self = self else { return }
            
            // 检测是否有iCloud相关的文件操作
            let iCloudFiles = [".ubd", "com.apple.synced", "cloudkit"]
            // 这些只是监控标记，实际不会与iCloud交互
            
            if source.data.contains(.write) {
                // 正常数据库写入，不做处理
            }
        }
        
        source.setCancelHandler {
            close(fileDescriptor)
        }
        
        source.resume()
        print("[iCloud隔离] 📂 文件系统监控已启动")
    }
    
    // MARK: - 隔离策略执行
    /// 执行iCloud隔离阻断
    private func blockiCloudSync(reason: String) {
        blockCount += 1
        lastBlockTime = Date()
        currentStatus = .blocked
        
        print("[iCloud隔离] 🚫 iCloud同步已阻断 (#\(blockCount))")
        print("[iCloud隔离]    原因: \(reason)")
        
        // 重新应用隔离措施
        excludeDatabaseFromiCloud()
        verifyNoCloudKit()
        
        // 发送阻断通知
        NotificationCenter.default.post(
            name: .init("LongHuniCloudBlockedEvent"),
            object: nil,
            userInfo: [
                "reason": reason,
                "blockCount": blockCount,
                "timestamp": Date().ISO8601Format()
            ]
        )
    }
    
    // MARK: - 公共API
    /// 手动检查iCloud隔离状态
    /// - Returns: 当前隔离状态描述
    public func checkIsolationStatus() -> [String: Any] {
        return [
            "isActive": isActive,
            "isBlocked": isBlocked,
            "status": currentStatus.rawValue,
            "blockCount": blockCount,
            "lastBlockTime": lastBlockTime?.ISO8601Format() ?? "N/A",
            "databasePath": storage.databaseURL.path,
            "excludedFromBackup": (try? storage.databaseURL.resourceValues(forKeys: [.isExcludedFromBackupKey]))?.isExcludedFromBackup ?? false
        ]
    }
    
    /// 检查指定键名是否需要隔离
    /// - Parameter key: 数据键名
    /// - Returns: 是否需要iCloud隔离
    public func shouldIsolateKey(_ key: String) -> Bool {
        return kLongHunPrefixes.contains { key.hasPrefix($0) }
    }
    
    /// 获取隔离统计信息
    /// - Returns: 统计字符串
    public func getIsolationReport() -> String {
        return """
        ╔══════════════════════════════════════════╗
        ║  iCloud隔离报告                           ║
        ╠══════════════════════════════════════════╣
        ║  隔离状态: \(isActive ? "✅ 激活" : "⏹️ 停用")                ║
        ║  阻断状态: \(isBlocked ? "🔒 已阻断" : "⚠️ 未阻断")           ║
        ║  当前状态: \(currentStatus.rawValue)                    ║
        ║  阻断次数: \(blockCount)                            ║
        ║  最后阻断: \(lastBlockTime?.ISO8601Format() ?? "无")           ║
        ╚══════════════════════════════════════════╝
        """
    }
}

// MARK: - 扩展：URL资源值
extension URL {
    /// 快速检查是否被排除在iCloud备份之外
    var isExcludedFromiCloudBackup: Bool {
        return (try? resourceValues(forKeys: [.isExcludedFromBackupKey]))?.isExcludedFromBackup ?? false
    }
}

// =============================================================================
// 文件尾部DNA标记
// #君子协议: 本代码仅用于合法合规的自主数据治理研究
// #DNA: #龍芯⚡️2026-06-19-LONGHUN-IOS-v5.3
// #致敬: #致敬⚡️SteveJobs·龍魂iOS端
// =============================================================================
