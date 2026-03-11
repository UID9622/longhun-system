// YuanziParser.swift
// 龍魂·元字解析器 v1.0
// DNA: #龍芯⚡️2026-03-07-IOS-YUANZI-☰乾-v1.0
// 读取 cnsh_status.json → 解析为 Swift 结构体

import Foundation
import WidgetKit

// MARK: - Data Models

struct CnshStatus: Codable {
    let meta: MetaInfo
    let yuanzi: YuanziInfo
    let audit: AuditInfo
    let lastEvent: LastEventInfo
    let system: SystemInfo
    let cnsh: CnshInfo

    enum CodingKeys: String, CodingKey {
        case meta = "_meta"
        case yuanzi, audit
        case lastEvent = "last_event"
        case system, cnsh
    }
}

struct MetaInfo: Codable {
    let version: String
    let dna: String
    let generatedAt: String

    enum CodingKeys: String, CodingKey {
        case version, dna
        case generatedAt = "generated_at"
    }
}

struct YuanziInfo: Codable {
    let guaSymbol: String
    let guaName: String
    let guaDimension: String
    let guaWeight: Double
    let personaId: String
    let personaName: String
    let display: String

    enum CodingKeys: String, CodingKey {
        case guaSymbol   = "gua_symbol"
        case guaName     = "gua_name"
        case guaDimension = "gua_dimension"
        case guaWeight   = "gua_weight"
        case personaId   = "persona_id"
        case personaName = "persona_name"
        case display
    }
}

struct AuditInfo: Codable {
    let score: Int
    let color: String
    let label: String
}

struct LastEventInfo: Codable {
    let summary: String
    let timestamp: String
    let dnaTail: String

    enum CodingKeys: String, CodingKey {
        case summary, timestamp
        case dnaTail = "dna_tail"
    }
}

struct SystemInfo: Codable {
    let memoryCount: Int
    let knowledgeNodes: Int
    let skillDomains: Int
    let ollamaOnline: Bool
    let ollamaModels: Int

    enum CodingKeys: String, CodingKey {
        case memoryCount    = "memory_count"
        case knowledgeNodes = "knowledge_nodes"
        case skillDomains   = "skill_domains"
        case ollamaOnline   = "ollama_online"
        case ollamaModels   = "ollama_models"
    }
}

struct CnshInfo: Codable {
    let urlScheme: String
    let status: String

    enum CodingKeys: String, CodingKey {
        case urlScheme = "url_scheme"
        case status
    }
}

// MARK: - Widget Timeline Entry

struct LongHunEntry: TimelineEntry {
    let date: Date
    let status: CnshStatus
    let lunarDate: String
}

// MARK: - Parser

struct YuanziParser {
    // iCloud App 容器 (Mac 写入路径对应 iOS 读取路径)
    // Mac: ~/Library/Mobile Documents/iCloud~com~uid9622~longhun/Documents/cnsh_status.json
    // iOS: FileManager.url(forUbiquityContainerIdentifier:) + /Documents/cnsh_status.json
    static let iCloudContainerID = "iCloud.com.uid9622.longhun"
    static let fileName = "cnsh_status.json"

    /// 加载状态 — iCloud → 本地降级 → 占位符
    static func load() -> CnshStatus {
        if let status = loadFromiCloud() { return status }
        return placeholder()
    }

    private static func loadFromiCloud() -> CnshStatus? {
        guard let containerURL = FileManager.default.url(
            forUbiquityContainerIdentifier: iCloudContainerID
        ) else { return nil }

        let fileURL = containerURL
            .appendingPathComponent("Documents")
            .appendingPathComponent(fileName)

        guard FileManager.default.fileExists(atPath: fileURL.path) else { return nil }

        do {
            // NSFileCoordinator 保证跨设备文件一致性
            var coordinatedData: Data?
            var coordinationError: NSError?
            let coordinator = NSFileCoordinator()
            coordinator.coordinate(readingItemAt: fileURL, options: .withoutChanges, error: &coordinationError) { url in
                coordinatedData = try? Data(contentsOf: url)
            }
            guard let data = coordinatedData else { return nil }
            return try JSONDecoder().decode(CnshStatus.self, from: data)
        } catch {
            return nil
        }
    }

    /// 默认占位符 — iCloud 不可用时展示
    static func placeholder() -> CnshStatus {
        CnshStatus(
            meta: MetaInfo(
                version: "1.0",
                dna: "#龍芯⚡️2026-IOS-BRIDGE-v1.0",
                generatedAt: ISO8601DateFormatter().string(from: Date())
            ),
            yuanzi: YuanziInfo(
                guaSymbol: "☰",
                guaName: "乾",
                guaDimension: "北辰",
                guaWeight: 0.35,
                personaId: "L0",
                personaName: "💎北辰",
                display: "☰乾·北辰"
            ),
            audit: AuditInfo(score: 88, color: "Green", label: "🟢通过"),
            lastEvent: LastEventInfo(
                summary: "系统待机",
                timestamp: "2026-03-07T00:00:00",
                dnaTail: ""
            ),
            system: SystemInfo(
                memoryCount: 0,
                knowledgeNodes: 0,
                skillDomains: 0,
                ollamaOnline: false,
                ollamaModels: 0
            ),
            cnsh: CnshInfo(urlScheme: "cnsh://open", status: "ready")
        )
    }
}
