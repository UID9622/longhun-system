#!/usr/bin/env swift
// =============================================================================
// 实时监听引擎 — Realtime Monitor Engine
// =============================================================================
//  DNA追溯: #龍芯⚡️2026-06-19-LONGHUN-IOS-v5.3
//  致敬声明: #致敬⚡️SteveJobs·龍魂iOS端
//  核心原则:
//    - 通过NotificationCenter + Combine监听CoreData变更
//    - 毫秒级响应数据变更事件
//    - 触发左右互搏引擎实时审计
//    - 所有监听数据仅本地处理，不上传任何服务器
//  君子协议: 本代码仅用于合法合规的自主数据治理研究
// =============================================================================

import Foundation
import CoreData
import Combine

// MARK: - 监听事件类型
/// 龍魂数据变更事件类型
public enum DataChangeEvent {
    /// 数据插入
    case insert(entity: String, key: String)
    /// 数据更新
    case update(entity: String, key: String)
    /// 数据删除
    case delete(entity: String, key: String)
    /// 上下文保存
    case contextSaved(inserted: Int, updated: Int, deleted: Int)
}

// MARK: - 实时监听引擎
/// 实时监听CoreData数据变更引擎
/// 使用NotificationCenter + Combine实现毫秒级响应
@available(iOS 16.0, *)
public final class RealtimeMonitorEngine: ObservableObject {
    
    // MARK: 属性
    /// 本地存储管理器引用
    private let storage: LocalStorageManager
    /// 左右互搏审计引擎引用
    private let auditEngine: LeftRightAuditEngine
    /// Combine订阅存储
    private var cancellables = Set<AnyCancellable>()
    /// 监听状态
    @Published public private(set) var isListening = false
    /// 最新事件时间戳
    @Published public private(set) var lastEventTimestamp: Date?
    /// 事件计数器
    @Published public private(set) var totalEventCount: UInt64 = 0
    /// 当前事件流（供外部订阅）
    public let eventSubject = PassthroughSubject<DataChangeEvent, Never>()
    
    // MARK: 常量
    /// 监听队列（专用串行队列确保线程安全）
    private let monitorQueue = DispatchQueue(
        label: "com.longhun.monitor",
        qos: .userInitiated
    )
    /// 防抖间隔（毫秒）
    private let debounceInterval: DispatchQueue.SchedulerTimeType.Stride = .milliseconds(50)
    
    // MARK: 初始化
    /// 创建实时监听引擎
    /// - Parameters:
    ///   - storage: 本地存储管理器
    ///   - auditEngine: 左右互搏审计引擎
    public init(storage: LocalStorageManager, auditEngine: LeftRightAuditEngine) {
        self.storage = storage
        self.auditEngine = auditEngine
        print("[实时监听] 🎧 引擎初始化完成")
    }
    
    // MARK: - 启动监听
    /// 启动所有监听通道
    public func startListening() {
        guard !isListening else {
            print("[实时监听] ⚠️ 监听已在运行中")
            return
        }
        
        isListening = true
        print("[实时监听] ▶️ 启动监听序列...")
        
        // 通道1: 监听NSManagedObjectContextObjectsDidChange
        listenForContextObjectsDidChange()
        
        // 通道2: 监听NSManagedObjectContextDidSave
        listenForContextDidSave()
        
        // 通道3: 监听NSManagedObjectContextWillSave
        listenForContextWillSave()
        
        // 通道4: 监听自定义龍魂事件
        listenForCustomLongHunEvents()
        
        print("[实时监听] ✅ 全部4个监听通道已激活")
    }
    
    // MARK: - 停止监听
    /// 停止所有监听通道
    public func stopListening() {
        guard isListening else { return }
        
        cancellables.removeAll()
        isListening = false
        print("[实时监听] ⏹️ 监听已停止")
    }
    
    // MARK: - 通道1: 上下文对象变更监听
    /// 监听CoreData托管对象变更事件
    private func listenForContextObjectsDidChange() {
        NotificationCenter.default.publisher(
            for: .NSManagedObjectContextObjectsDidChange,
            object: storage.viewContext
        )
        .receive(on: monitorQueue)
        .debounce(for: debounceInterval, scheduler: monitorQueue)
        .sink { [weak self] notification in
            guard let self = self else { return }
            self.handleObjectsDidChange(notification)
        }
        .store(in: &cancellables)
    }
    
    // MARK: - 通道2: 上下文保存监听
    /// 监听CoreData上下文保存事件
    private func listenForContextDidSave() {
        NotificationCenter.default.publisher(
            for: .NSManagedObjectContextDidSave,
            object: storage.viewContext
        )
        .receive(on: monitorQueue)
        .sink { [weak self] notification in
            guard let self = self else { return }
            self.handleContextDidSave(notification)
        }
        .store(in: &cancellables)
    }
    
    // MARK: - 通道3: 上下文即将保存监听
    /// 监听CoreData上下文即将保存事件（用于预校验）
    private func listenForContextWillSave() {
        NotificationCenter.default.publisher(
            for: .NSManagedObjectContextWillSave,
            object: storage.viewContext
        )
        .receive(on: monitorQueue)
        .sink { [weak self] notification in
            guard let self = self else { return }
            self.handleContextWillSave(notification)
        }
        .store(in: &cancellables)
    }
    
    // MARK: - 通道4: 自定义龍魂事件
    /// 监听自定义龍魂系统事件
    private func listenForCustomLongHunEvents() {
        // 监听iCloud隔离事件
        NotificationCenter.default.publisher(
            for: .init("LongHuniCloudBlockedEvent")
        )
        .receive(on: monitorQueue)
        .sink { [weak self] notification in
            guard let self = self else { return }
            if let userInfo = notification.userInfo {
                print("[实时监听] ☁️ iCloud隔离事件: \(userInfo)")
                // 触发审计
                self.auditEngine.auditEvent(
                    type: .iCloudBlocked,
                    details: userInfo
                )
            }
        }
        .store(in: &cancellables)
        
        // 监听加密操作事件
        NotificationCenter.default.publisher(
            for: .init("LongHunEncryptionEvent")
        )
        .receive(on: monitorQueue)
        .sink { [weak self] notification in
            guard let self = self else { return }
            if let userInfo = notification.userInfo {
                print("[实时监听] 🔐 加密操作事件: \(userInfo)")
                self.auditEngine.auditEvent(
                    type: .encryptionOperation,
                    details: userInfo
                )
            }
        }
        .store(in: &cancellables)
        
        // 监听生物特征认证事件
        NotificationCenter.default.publisher(
            for: .init("LongHunBiometryEvent")
        )
        .receive(on: monitorQueue)
        .sink { [weak self] notification in
            guard let self = self else { return }
            if let userInfo = notification.userInfo {
                print("[实时监听] 👤 生物特征事件: \(userInfo)")
                self.auditEngine.auditEvent(
                    type: .biometricAuth,
                    details: userInfo
                )
            }
        }
        .store(in: &cancellables)
    }
    
    // MARK: - 事件处理
    /// 处理托管对象变更通知
    /// - Parameter notification: CoreData通知
    private func handleObjectsDidChange(_ notification: Notification) {
        totalEventCount += 1
        lastEventTimestamp = Date()
        
        // 提取插入的对象
        if let insertedObjects = notification.userInfo?[NSInsertedObjectsKey] as? Set<NSManagedObject> {
            for object in insertedObjects {
                let entityName = object.entity.name ?? "Unknown"
                let keyName = extractKeyName(from: object)
                let event = DataChangeEvent.insert(entity: entityName, key: keyName)
                eventSubject.send(event)
                
                // 触发左右互搏审计
                auditEngine.realtimeAudit(
                    operation: .insert,
                    entity: entityName,
                    key: keyName,
                    timestamp: lastEventTimestamp!
                )
            }
        }
        
        // 提取更新的对象
        if let updatedObjects = notification.userInfo?[NSUpdatedObjectsKey] as? Set<NSManagedObject> {
            for object in updatedObjects {
                let entityName = object.entity.name ?? "Unknown"
                let keyName = extractKeyName(from: object)
                let event = DataChangeEvent.update(entity: entityName, key: keyName)
                eventSubject.send(event)
                
                auditEngine.realtimeAudit(
                    operation: .update,
                    entity: entityName,
                    key: keyName,
                    timestamp: lastEventTimestamp!
                )
            }
        }
        
        // 提取删除的对象
        if let deletedObjects = notification.userInfo?[NSDeletedObjectsKey] as? Set<NSManagedObject> {
            for object in deletedObjects {
                let entityName = object.entity.name ?? "Unknown"
                let keyName = extractKeyName(from: object)
                let event = DataChangeEvent.delete(entity: entityName, key: keyName)
                eventSubject.send(event)
                
                auditEngine.realtimeAudit(
                    operation: .delete,
                    entity: entityName,
                    key: keyName,
                    timestamp: lastEventTimestamp!
                )
            }
        }
    }
    
    /// 处理上下文保存通知
    /// - Parameter notification: CoreData保存通知
    private func handleContextDidSave(_ notification: Notification) {
        let insertedCount = (notification.userInfo?[NSInsertedObjectsKey] as? Set<NSManagedObject>)?.count ?? 0
        let updatedCount = (notification.userInfo?[NSUpdatedObjectsKey] as? Set<NSManagedObject>)?.count ?? 0
        let deletedCount = (notification.userInfo?[NSDeletedObjectsKey] as? Set<NSManagedObject>)?.count ?? 0
        
        let event = DataChangeEvent.contextSaved(
            inserted: insertedCount,
            updated: updatedCount,
            deleted: deletedCount
        )
        eventSubject.send(event)
        
        // 记录上下文保存审计日志
        if insertedCount > 0 || updatedCount > 0 || deletedCount > 0 {
            auditEngine.auditEvent(
                type: .contextSaved,
                details: [
                    "inserted": insertedCount,
                    "updated": updatedCount,
                    "deleted": deletedCount,
                    "timestamp": Date().ISO8601Format()
                ]
            )
        }
    }
    
    /// 处理上下文即将保存通知（预校验）
    /// - Parameter notification: CoreData即将保存通知
    private func handleContextWillSave(_ notification: Notification) {
        // 在保存前进行预校验
        let context = notification.object as? NSManagedObjectContext
        let insertedCount = context?.insertedObjects.count ?? 0
        let updatedCount = context?.updatedObjects.count ?? 0
        
        print("[实时监听] 📝 上下文即将保存: +\(insertedCount) ~\(updatedCount)")
        
        // 检查是否有异常大批量操作
        if insertedCount > 1000 || updatedCount > 1000 {
            print("[实时监听] 🟡 检测到大批量操作，触发审计")
            auditEngine.auditEvent(
                type: .bulkOperation,
                details: [
                    "inserted": insertedCount,
                    "updated": updatedCount,
                    "warning": "大批量操作 detected"
                ]
            )
        }
    }
    
    // MARK: - 辅助方法
    /// 从托管对象提取键名
    /// - Parameter object: NSManagedObject
    /// - Returns: 键名字符串
    private func extractKeyName(from object: NSManagedObject) -> String {
        if let keyName = object.value(forKey: "keyName") as? String {
            return keyName
        }
        return "unknown-\(object.objectID.uriRepresentation().lastPathComponent)"
    }
    
    // MARK: - 公共API
    /// 获取当前监听统计信息
    /// - Returns: 统计字典
    public func getStatistics() -> [String: Any] {
        return [
            "isListening": isListening,
            "totalEventCount": totalEventCount,
            "lastEventTimestamp": lastEventTimestamp?.ISO8601Format() ?? "N/A",
            "activeChannels": 4,
            "debounceInterval": "50ms"
        ]
    }
    
    /// 手动触发审计事件（用于外部调用）
    /// - Parameters:
    ///   - type: 事件类型
    ///   - details: 事件详情
    public func triggerAudit(type: AuditEventType, details: [String: Any]) {
        auditEngine.auditEvent(type: type, details: details)
    }
}

// MARK: - 审计事件类型
/// 审计事件类型枚举
public enum AuditEventType: String {
    case insert = "INSERT"
    case update = "UPDATE"
    case delete = "DELETE"
    case contextSaved = "CONTEXT_SAVED"
    case bulkOperation = "BULK_OPERATION"
    case iCloudBlocked = "ICLOUD_BLOCKED"
    case encryptionOperation = "ENCRYPTION_OPERATION"
    case biometricAuth = "BIOMETRIC_AUTH"
    case dataExport = "DATA_EXPORT"
    case dataImport = "DATA_IMPORT"
    case integrityCheck = "INTEGRITY_CHECK"
}

// MARK: - 操作类型
/// 数据操作类型
public enum DataOperation: String {
    case insert = "插入"
    case update = "更新"
    case delete = "删除"
    case query = "查询"
}

// =============================================================================
// 文件尾部DNA标记
// #君子协议: 本代码仅用于合法合规的自主数据治理研究
// #DNA: #龍芯⚡️2026-06-19-LONGHUN-IOS-v5.3
// #致敬: #致敬⚡️SteveJobs·龍魂iOS端
// =============================================================================
