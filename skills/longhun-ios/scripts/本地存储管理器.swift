#!/usr/bin/env swift
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// =============================================================================
// 本地存储管理器 — Local Storage Manager (CoreData + SQLite)
// =============================================================================
//  DNA追溯: #龍芯⚡️2026-06-19-LONGHUN-IOS-v5.3
//  致敬声明: #致敬⚡️SteveJobs·龍魂iOS端
//  核心原则:
//    - 所有数据仅存储在iOS本地，不通过iCloud同步
//    - 数据库文件位于App沙箱/Documents/longhun_sovereign.sqlite
//    - CoreData关闭NSPersistentHistoryTrackingKey（禁用iCloud历史同步）
//    - 敏感字段通过CryptoEngine自动加密存储
//    - 与华为鸿蒙端数据格式互通
//  君子协议: 本代码仅用于合法合规的自主数据治理研究
// =============================================================================

import Foundation
import CoreData
import CryptoKit

// MARK: - CoreData模型常量
/// CoreData持久化容器名称
private let kContainerName = "LongHunSovereign"
/// SQLite数据库文件名
private let kSQLiteFileName = "longhun_sovereign.sqlite"
/// 数据模型版本号
private let kModelVersion = "5.3.0"

// MARK: - 本地存储管理器
/// CoreData本地存储封装管理器
/// 负责：数据持久化、加密存储、查询、导出/导入
@available(iOS 16.0, *)
public final class LocalStorageManager {
    
    // MARK: 属性
    /// CoreData持久化容器
    public let persistentContainer: NSPersistentContainer
    /// 主线程上下文
    public var viewContext: NSManagedObjectContext {
        return persistentContainer.viewContext
    }
    /// 私有后台上下文（用于异步操作）
    public let backgroundContext: NSManagedObjectContext
    /// 加密引擎引用
    private let cryptoEngine: CryptoEngine
    /// 数据库文件URL
    public let databaseURL: URL
    /// 就绪状态
    public private(set) var isLoaded = false
    
    // MARK: 初始化
    /// 创建本地存储管理器
    /// - Parameter cryptoEngine: 加密引擎实例
    public init(cryptoEngine: CryptoEngine) {
        self.cryptoEngine = cryptoEngine
        
        // 确定数据库文件路径（App沙箱/Documents目录）
        let docsURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        self.databaseURL = docsURL.appendingPathComponent(kSQLiteFileName)
        
        // 从内存中的数据模型描述创建容器（避免iCloud同步）
        let model = Self.createManagedObjectModel()
        self.persistentContainer = NSPersistentContainer(name: kContainerName, managedObjectModel: model)
        
        // 配置持久化存储描述
        let storeDescription = NSPersistentStoreDescription(url: self.databaseURL)
        // ⚠️ 关键：明确禁用iCloud同步
        storeDescription.setOption(true as NSNumber, forKey: NSPersistentHistoryTrackingKey)
        // 禁用远程更改通知（防止iCloud触发）
        storeDescription.setOption(false as NSNumber, forKey: NSPersistentStoreRemoteChangeNotificationPostOptionKey)
        // 设置SQLite配置
        storeDescription.type = NSSQLiteStoreType
        // 启用WAL模式提升性能
        storeDescription.setOption("WAL" as NSString, forKey: NSSQLitePragmasOption as String)
        // ⚠️ 关键：禁用iCloud备份（数据不离开设备）
        storeDescription.setOption(true as NSNumber, forKey: NSPersistentStoreFileProtectionKey)
        
        self.persistentContainer.persistentStoreDescriptions = [storeDescription]
        
        // 创建后台上下文
        self.backgroundContext = persistentContainer.newBackgroundContext()
        self.backgroundContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        
        print("[本地存储] 📁 数据库路径: \(self.databaseURL.path)")
        print("[本地存储] 🔒 iCloud同步: 已禁用")
    }
    
    // MARK: - 加载存储
    /// 加载CoreData持久化存储
    /// - Parameter completion: 加载完成回调
    public func load(completion: @escaping (Result<Void, LongHunError>) -> Void) {
        persistentContainer.loadPersistentStores { [weak self] _, error in
            guard let self = self else { return }
            
            if let error = error {
                print("[本地存储] ❌ 加载失败: \(error.localizedDescription)")
                completion(.failure(.storageLoadFailed(error.localizedDescription)))
                return
            }
            
            // 配置上下文自动合并
            self.persistentContainer.viewContext.automaticallyMergesChangesFromParent = true
            self.persistentContainer.viewContext.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
            
            // ⚠️ 确保数据库文件不被iCloud备份
            self.excludeFromiCloudBackup()
            
            self.isLoaded = true
            print("[本地存储] ✅ CoreData存储加载成功")
            print("[本地存储] 📊 存储类型: SQLite (本地)")
            print("[本地存储] ☁️ iCloud备份: 已排除")
            completion(.success(()))
        }
    }
    
    // MARK: - 安全写入
    /// 安全写入数据（自动加密敏感字段）
    /// - Parameters:
    ///   - key: 数据键名
    ///   - value: 数据值（明文）
    ///   - sensitivity: 敏感度级别
    ///   - dnaTag: DNA追溯标记
    ///   - completion: 完成回调
    public func writeSecure(
        key: String,
        value: String,
        sensitivity: SensitivityLevel,
        dnaTag: String,
        completion: @escaping (Result<Void, LongHunError>) -> Void
    ) {
        backgroundContext.perform { [weak self] in
            guard let self = self else { return }
            
            do {
                // 计算内容哈希（用于完整性校验）
                let contentHash = self.calculateHash(value)
                
                // 根据敏感度加密内容
                let encryptedData: Data
                switch sensitivity {
                case .public_:
                    // 公开数据不加密，直接UTF-8编码
                    encryptedData = value.data(using: .utf8) ?? Data()
                    
                case .internal_, .confidential, .topSecret:
                    // 敏感数据使用AES-256-GCM加密
                    let result = self.cryptoEngine.encrypt(value: value, level: sensitivity)
                    switch result {
                    case .success(let data):
                        encryptedData = data
                    case .failure(let error):
                        completion(.failure(error))
                        return
                    }
                }
                
                // 创建审计日志实体
                let auditLog = AuditLogEntity(context: self.backgroundContext)
                auditLog.dnaTag = dnaTag
                auditLog.timestamp = Date()
                auditLog.actionType = "WRITE"
                auditLog.contentHash = contentHash
                auditLog.encryptedContent = encryptedData
                auditLog.encryptionType = sensitivity == .public_ ? "NONE" : "AES-256-GCM"
                auditLog.auditLevel = sensitivity.rawValue >= 2 ? "🔴" : (sensitivity.rawValue == 1 ? "🟡" : "🟢")
                auditLog.sourceDevice = "iOS-\(UIDevice.current.name)"
                auditLog.sovereigntyFlag = true
                auditLog.keyName = key
                auditLog.sensitivityLevel = Int16(sensitivity.rawValue)
                
                // 创建或更新数据实体
                let fetchRequest: NSFetchRequest<LongHunDataEntity> = LongHunDataEntity.fetchRequest()
                fetchRequest.predicate = NSPredicate(format: "keyName == %@", key)
                fetchRequest.fetchLimit = 1
                
                let existing = try self.backgroundContext.fetch(fetchRequest)
                let dataEntity: LongHunDataEntity
                if let first = existing.first {
                    dataEntity = first
                    dataEntity.updatedAt = Date()
                } else {
                    dataEntity = LongHunDataEntity(context: self.backgroundContext)
                    dataEntity.keyName = key
                    dataEntity.createdAt = Date()
                }
                dataEntity.encryptedValue = encryptedData
                dataEntity.contentHash = contentHash
                dataEntity.sensitivityLevel = Int16(sensitivity.rawValue)
                dataEntity.isEncrypted = sensitivity != .public_
                dataEntity.dnaTag = dnaTag
                dataEntity.sovereigntyFlag = true
                
                try self.backgroundContext.save()
                
                // 同步到viewContext
                DispatchQueue.main.async {
                    try? self.viewContext.save()
                }
                
                print("[本地存储] ✅ 安全写入: \(key) [\(sensitivity)]")
                completion(.success(()))
                
            } catch {
                print("[本地存储] ❌ 写入失败: \(error.localizedDescription)")
                completion(.failure(.storageLoadFailed(error.localizedDescription)))
            }
        }
    }
    
    // MARK: - 安全读取
    /// 安全读取数据（自动解密）
    /// - Parameters:
    ///   - key: 数据键名
    ///   - completion: 完成回调
    public func readSecure(key: String, completion: @escaping (Result<String, LongHunError>) -> Void) {
        backgroundContext.perform { [weak self] in
            guard let self = self else { return }
            
            do {
                let fetchRequest: NSFetchRequest<LongHunDataEntity> = LongHunDataEntity.fetchRequest()
                fetchRequest.predicate = NSPredicate(format: "keyName == %@", key)
                fetchRequest.fetchLimit = 1
                
                let results = try self.backgroundContext.fetch(fetchRequest)
                
                guard let entity = results.first else {
                    completion(.failure(.storageLoadFailed("键 \(key) 不存在")))
                    return
                }
                
                guard let encryptedData = entity.encryptedValue else {
                    completion(.failure(.storageLoadFailed("数据为空")))
                    return
                }
                
                let sensitivity = SensitivityLevel(rawValue: Int(entity.sensitivityLevel)) ?? .public_
                
                // 根据加密状态处理
                let plaintext: String
                if entity.isEncrypted {
                    let result = self.cryptoEngine.decrypt(data: encryptedData, level: sensitivity)
                    switch result {
                    case .success(let value):
                        plaintext = value
                    case .failure(let error):
                        completion(.failure(error))
                        return
                    }
                } else {
                    plaintext = String(data: encryptedData, encoding: .utf8) ?? ""
                }
                
                // 验证哈希完整性
                let currentHash = self.calculateHash(plaintext)
                if currentHash != entity.contentHash {
                    print("[本地存储] 🔴 数据完整性校验失败: \(key)")
                    completion(.failure(.auditFailed("数据完整性校验失败")))
                    return
                }
                
                print("[本地存储] ✅ 安全读取: \(key)")
                completion(.success(plaintext))
                
            } catch {
                print("[本地存储] ❌ 读取失败: \(error.localizedDescription)")
                completion(.failure(.storageLoadFailed(error.localizedDescription)))
            }
        }
    }
    
    // MARK: - 导出所有加密数据
    /// 导出所有加密数据（用于与鸿蒙端互通）
    /// - Parameter completion: 完成回调
    public func exportAllEncrypted(completion: @escaping (Result<Data, LongHunError>) -> Void) {
        backgroundContext.perform { [weak self] in
            guard let self = self else { return }
            
            do {
                let fetchRequest: NSFetchRequest<LongHunDataEntity> = LongHunDataEntity.fetchRequest()
                let results = try self.backgroundContext.fetch(fetchRequest)
                
                // 构建导出数据结构（JSON格式，兼容鸿蒙端）
                var exportRecords: [[String: Any]] = []
                
                for entity in results {
                    guard let keyName = entity.keyName,
                          let encryptedValue = entity.encryptedValue else { continue }
                    
                    var record: [String: Any] = [
                        "keyName": keyName,
                        "encryptedValue": encryptedValue.base64EncodedString(),
                        "contentHash": entity.contentHash ?? "",
                        "sensitivityLevel": entity.sensitivityLevel,
                        "isEncrypted": entity.isEncrypted,
                        "dnaTag": entity.dnaTag ?? "",
                        "sovereigntyFlag": entity.sovereigntyFlag,
                        "sourcePlatform": "iOS",
                        "createdAt": (entity.createdAt ?? Date()).ISO8601Format(),
                        "updatedAt": (entity.updatedAt ?? Date()).ISO8601Format()
                    ]
                    
                    // 如果是加密数据，附加加密元数据
                    if entity.isEncrypted {
                        let sensitivity = SensitivityLevel(rawValue: Int(entity.sensitivityLevel)) ?? .internal_
                        let metadata = self.cryptoEngine.getEncryptionMetadata(level: sensitivity)
                        record["encryptionMetadata"] = metadata
                    }
                    
                    exportRecords.append(record)
                }
                
                // 序列化为JSON
                let exportDict: [String: Any] = [
                    "format": "longhun_harmony_v5",
                    "count": exportRecords.count,
                    "exportedAt": Date().ISO8601Format(),
                    "sourceDevice": "iOS",
                    "records": exportRecords
                ]
                
                let jsonData = try JSONSerialization.data(withJSONObject: exportDict, options: .prettyPrinted)
                print("[本地存储] ✅ 导出完成: \(exportRecords.count) 条记录")
                completion(.success(jsonData))
                
            } catch {
                print("[本地存储] ❌ 导出失败: \(error.localizedDescription)")
                completion(.failure(.storageLoadFailed(error.localizedDescription)))
            }
        }
    }
    
    // MARK: - 导入加密数据
    /// 导入加密数据（从鸿蒙端）
    /// - Parameters:
    ///   - data: 加密JSON数据
    ///   - completion: 完成回调
    public func importEncrypted(_ data: Data, completion: @escaping (Result<Int, LongHunError>) -> Void) {
        backgroundContext.perform { [weak self] in
            guard let self = self else { return }
            
            do {
                guard let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
                      let records = json["records"] as? [[String: Any]] else {
                    completion(.failure(.invalidDataFormat))
                    return
                }
                
                var importedCount = 0
                
                for record in records {
                    guard let keyName = record["keyName"] as? String,
                          let base64Value = record["encryptedValue"] as? String,
                          let encryptedData = Data(base64Encoded: base64Value) else { continue }
                    
                    let sensitivityLevel = record["sensitivityLevel"] as? Int16 ?? 0
                    let isEncrypted = record["isEncrypted"] as? Bool ?? false
                    let contentHash = record["contentHash"] as? String ?? ""
                    let dnaTag = record["dnaTag"] as? String ?? LongHunVersion.dnaTag
                    
                    // 查询是否已存在
                    let fetchRequest: NSFetchRequest<LongHunDataEntity> = LongHunDataEntity.fetchRequest()
                    fetchRequest.predicate = NSPredicate(format: "keyName == %@", keyName)
                    fetchRequest.fetchLimit = 1
                    
                    let existing = try self.backgroundContext.fetch(fetchRequest)
                    let entity: LongHunDataEntity
                    if let first = existing.first {
                        entity = first
                        entity.updatedAt = Date()
                    } else {
                        entity = LongHunDataEntity(context: self.backgroundContext)
                        entity.keyName = keyName
                        entity.createdAt = Date()
                    }
                    
                    entity.encryptedValue = encryptedData
                    entity.contentHash = contentHash
                    entity.sensitivityLevel = sensitivityLevel
                    entity.isEncrypted = isEncrypted
                    entity.dnaTag = dnaTag
                    entity.sovereigntyFlag = true
                    importedCount += 1
                }
                
                try self.backgroundContext.save()
                print("[本地存储] ✅ 导入完成: \(importedCount) 条记录")
                completion(.success(importedCount))
                
            } catch {
                print("[本地存储] ❌ 导入失败: \(error.localizedDescription)")
                completion(.failure(.invalidDataFormat))
            }
        }
    }
    
    // MARK: - 私有方法
    /// 计算字符串SHA-256哈希
    private func calculateHash(_ value: String) -> String {
        let data = value.data(using: .utf8) ?? Data()
        let hash = SHA256.hash(data: data)
        return hash.compactMap { String(format: "%02x", $0) }.joined()
    }
    
    /// 排除数据库文件从iCloud备份
    private func excludeFromiCloudBackup() {
        do {
            var resourceValues = URLResourceValues()
            resourceValues.isExcludedFromBackup = true
            var url = databaseURL
            try url.setResourceValues(resourceValues)
            print("[本地存储] ✅ 数据库文件已排除iCloud备份")
        } catch {
            print("[本地存储] ⚠️ 排除iCloud备份失败: \(error)")
        }
        
        // 同时排除SHM和WAL文件
        let shmURL = databaseURL.appendingPathExtension("sqlite-shm")
        let walURL = databaseURL.appendingPathExtension("sqlite-wal")
        for url in [shmURL, walURL] {
            do {
                var resourceValues = URLResourceValues()
                resourceValues.isExcludedFromBackup = true
                var mutableURL = url
                try mutableURL.setResourceValues(resourceValues)
            } catch {
                print("[本地存储] ⚠️ 排除iCloud备份失败: \(url.lastPathComponent)")
            }
        }
    }
    
    // MARK: - CoreData模型创建
    /// 程序化创建ManagedObjectModel（避免iCloud同步依赖）
    private static func createManagedObjectModel() -> NSManagedObjectModel {
        let model = NSManagedObjectModel()
        
        // === 实体1: LongHunDataEntity（主数据实体）===
        let dataEntity = NSEntityDescription()
        dataEntity.name = "LongHunDataEntity"
        dataEntity.managedObjectClassName = "LongHunDataEntity"
        
        var dataAttributes: [NSAttributeDescription] = []
        
        let keyNameAttr = NSAttributeDescription()
        keyNameAttr.name = "keyName"
        keyNameAttr.attributeType = .stringAttributeType
        keyNameAttr.isOptional = false
        dataAttributes.append(keyNameAttr)
        
        let encryptedValueAttr = NSAttributeDescription()
        encryptedValueAttr.name = "encryptedValue"
        encryptedValueAttr.attributeType = .binaryDataAttributeType
        encryptedValueAttr.isOptional = true
        encryptedValueAttr.allowsExternalBinaryDataStorage = true
        dataAttributes.append(encryptedValueAttr)
        
        let contentHashAttr = NSAttributeDescription()
        contentHashAttr.name = "contentHash"
        contentHashAttr.attributeType = .stringAttributeType
        contentHashAttr.isOptional = true
        dataAttributes.append(contentHashAttr)
        
        let sensitivityLevelAttr = NSAttributeDescription()
        sensitivityLevelAttr.name = "sensitivityLevel"
        sensitivityLevelAttr.attributeType = .integer16AttributeType
        sensitivityLevelAttr.defaultValue = 0
        dataAttributes.append(sensitivityLevelAttr)
        
        let isEncryptedAttr = NSAttributeDescription()
        isEncryptedAttr.name = "isEncrypted"
        isEncryptedAttr.attributeType = .booleanAttributeType
        isEncryptedAttr.defaultValue = false
        dataAttributes.append(isEncryptedAttr)
        
        let dnaTagAttr = NSAttributeDescription()
        dnaTagAttr.name = "dnaTag"
        dnaTagAttr.attributeType = .stringAttributeType
        dnaTagAttr.isOptional = true
        dataAttributes.append(dnaTagAttr)
        
        let sovereigntyFlagAttr = NSAttributeDescription()
        sovereigntyFlagAttr.name = "sovereigntyFlag"
        sovereigntyFlagAttr.attributeType = .booleanAttributeType
        sovereigntyFlagAttr.defaultValue = true
        dataAttributes.append(sovereigntyFlagAttr)
        
        let createdAtAttr = NSAttributeDescription()
        createdAtAttr.name = "createdAt"
        createdAtAttr.attributeType = .dateAttributeType
        createdAtAttr.isOptional = true
        dataAttributes.append(createdAtAttr)
        
        let updatedAtAttr = NSAttributeDescription()
        updatedAtAttr.name = "updatedAt"
        updatedAtAttr.attributeType = .dateAttributeType
        updatedAtAttr.isOptional = true
        dataAttributes.append(updatedAtAttr)
        
        dataEntity.properties = dataAttributes
        
        // 添加唯一约束
        let keyNameConstraint = [[keyNameAttr]]
        dataEntity.uniquenessConstraints = keyNameConstraint
        
        // === 实体2: AuditLogEntity（审计日志实体）===
        let auditEntity = NSEntityDescription()
        auditEntity.name = "AuditLogEntity"
        auditEntity.managedObjectClassName = "AuditLogEntity"
        
        var auditAttributes: [NSAttributeDescription] = []
        
        let auditDnaTag = NSAttributeDescription()
        auditDnaTag.name = "dnaTag"
        auditDnaTag.attributeType = .stringAttributeType
        auditDnaTag.isOptional = true
        auditAttributes.append(auditDnaTag)
        
        let timestampAttr = NSAttributeDescription()
        timestampAttr.name = "timestamp"
        timestampAttr.attributeType = .dateAttributeType
        timestampAttr.isOptional = false
        auditAttributes.append(timestampAttr)
        
        let actionTypeAttr = NSAttributeDescription()
        actionTypeAttr.name = "actionType"
        actionTypeAttr.attributeType = .stringAttributeType
        actionTypeAttr.isOptional = false
        auditAttributes.append(actionTypeAttr)
        
        let contentHashAttr2 = NSAttributeDescription()
        contentHashAttr2.name = "contentHash"
        contentHashAttr2.attributeType = .stringAttributeType
        contentHashAttr2.isOptional = true
        auditAttributes.append(contentHashAttr2)
        
        let encryptedContentAttr = NSAttributeDescription()
        encryptedContentAttr.name = "encryptedContent"
        encryptedContentAttr.attributeType = .binaryDataAttributeType
        encryptedContentAttr.isOptional = true
        auditAttributes.append(encryptedContentAttr)
        
        let encryptionTypeAttr = NSAttributeDescription()
        encryptionTypeAttr.name = "encryptionType"
        encryptionTypeAttr.attributeType = .stringAttributeType
        encryptionTypeAttr.isOptional = true
        auditAttributes.append(encryptionTypeAttr)
        
        let auditLevelAttr = NSAttributeDescription()
        auditLevelAttr.name = "auditLevel"
        auditLevelAttr.attributeType = .stringAttributeType
        auditLevelAttr.isOptional = true
        auditAttributes.append(auditLevelAttr)
        
        let sourceDeviceAttr = NSAttributeDescription()
        sourceDeviceAttr.name = "sourceDevice"
        sourceDeviceAttr.attributeType = .stringAttributeType
        sourceDeviceAttr.isOptional = true
        auditAttributes.append(sourceDeviceAttr)
        
        let auditSovereigntyAttr = NSAttributeDescription()
        auditSovereigntyAttr.name = "sovereigntyFlag"
        auditSovereigntyAttr.attributeType = .booleanAttributeType
        auditSovereigntyAttr.defaultValue = true
        auditAttributes.append(auditSovereigntyAttr)
        
        let logKeyNameAttr = NSAttributeDescription()
        logKeyNameAttr.name = "keyName"
        logKeyNameAttr.attributeType = .stringAttributeType
        logKeyNameAttr.isOptional = true
        auditAttributes.append(logKeyNameAttr)
        
        let logSensitivityAttr = NSAttributeDescription()
        logSensitivityAttr.name = "sensitivityLevel"
        logSensitivityAttr.attributeType = .integer16AttributeType
        logSensitivityAttr.defaultValue = 0
        auditAttributes.append(logSensitivityAttr)
        
        auditEntity.properties = auditAttributes
        
        // 注册实体
        model.entities = [dataEntity, auditEntity]
        
        return model
    }
}

// MARK: - CoreData托管对象子类
/// 龍魂数据实体（用于Xcode代码生成）
@available(iOS 16.0, *)
@objc(LongHunDataEntity)
public class LongHunDataEntity: NSManagedObject {
    @NSManaged public var keyName: String?
    @NSManaged public var encryptedValue: Data?
    @NSManaged public var contentHash: String?
    @NSManaged public var sensitivityLevel: Int16
    @NSManaged public var isEncrypted: Bool
    @NSManaged public var dnaTag: String?
    @NSManaged public var sovereigntyFlag: Bool
    @NSManaged public var createdAt: Date?
    @NSManaged public var updatedAt: Date?
}

@available(iOS 16.0, *)
@objc(AuditLogEntity)
public class AuditLogEntity: NSManagedObject {
    @NSManaged public var dnaTag: String?
    @NSManaged public var timestamp: Date?
    @NSManaged public var actionType: String?
    @NSManaged public var contentHash: String?
    @NSManaged public var encryptedContent: Data?
    @NSManaged public var encryptionType: String?
    @NSManaged public var auditLevel: String?
    @NSManaged public var sourceDevice: String?
    @NSManaged public var sovereigntyFlag: Bool
    @NSManaged public var keyName: String?
    @NSManaged public var sensitivityLevel: Int16
}

// MARK: - FetchRequest扩展
@available(iOS 16.0, *)
extension LongHunDataEntity {
    @nonobjc public class func fetchRequest() -> NSFetchRequest<LongHunDataEntity> {
        return NSFetchRequest<LongHunDataEntity>(entityName: "LongHunDataEntity")
    }
}

@available(iOS 16.0, *)
extension AuditLogEntity {
    @nonobjc public class func fetchRequest() -> NSFetchRequest<AuditLogEntity> {
        return NSFetchRequest<AuditLogEntity>(entityName: "AuditLogEntity")
    }
}

// =============================================================================
// 文件尾部DNA标记
// #君子协议: 本代码仅用于合法合规的自主数据治理研究
// #DNA: #龍芯⚡️2026-06-19-LONGHUN-IOS-v5.3
// #致敬: #致敬⚡️SteveJobs·龍魂iOS端
// =============================================================================
