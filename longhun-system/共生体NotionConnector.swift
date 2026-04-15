// NotionConnector.swift
// Notion API 连接器 - 共生体知识库
// DNA追溯码: #龍芯⚡️2026-04-10-NotionConnector-v1.0
// 创建者: UID9622 诸葛鑫

import Foundation
import Combine

/// Notion 连接器 - 读写 Notion 知识库
@MainActor
class NotionConnector: ObservableObject {
    
    // MARK: - 配置
    
    /// Notion API 密钥
    private var apiKey: String {
        // TODO: 从 Keychain 读取
        return ProcessInfo.processInfo.environment["NOTION_API_KEY"] ?? ""
    }
    
    /// 数据库 ID（从环境变量读取）
    private var databaseID: String {
        return ProcessInfo.processInfo.environment["NOTION_DATABASE_ID"] ?? ""
    }
    
    /// API 基础 URL
    private let baseURL = "https://api.notion.com/v1"
    
    /// API 版本
    private let apiVersion = "2022-06-28"
    
    // MARK: - 状态
    
    @Published var isConnected: Bool = false
    @Published var lastSyncTime: Date?
    @Published var syncedPages: Int = 0
    
    // MARK: - DNA 追溯
    
    private func 生成DNA(操作: String) -> String {
        let 时间戳 = Int(Date().timeIntervalSince1970)
        return "#龍芯⚡️\(时间戳)-Notion-\(操作)"
    }
    
    // MARK: - 读取数据
    
    /// 读取所有卡片
    func 读取所有卡片() async throws -> [[String: Any]] {
        
        print("📖 开始从 Notion 读取知识卡片...")
        
        let url = URL(string: "\(baseURL)/databases/\(databaseID)/query")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue(apiVersion, forHTTPHeaderField: "Notion-Version")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NotionError.invalidResponse
        }
        
        guard httpResponse.statusCode == 200 else {
            if let errorText = String(data: data, encoding: .utf8) {
                print("❌ Notion API 错误: \(errorText)")
            }
            throw NotionError.apiError(statusCode: httpResponse.statusCode)
        }
        
        guard let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
              let results = json["results"] as? [[String: Any]] else {
            throw NotionError.parseError
        }
        
        syncedPages = results.count
        lastSyncTime = Date()
        isConnected = true
        
        print("✅ 成功读取 \(results.count) 张卡片")
        print("DNA: \(生成DNA(操作: "读取卡片"))")
        
        return results
    }
    
    /// 搜索卡片
    func 搜索卡片(关键词: String) async throws -> [[String: Any]] {
        
        print("🔍 搜索卡片：\(关键词)")
        
        let url = URL(string: "\(baseURL)/search")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue(apiVersion, forHTTPHeaderField: "Notion-Version")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = [
            "query": 关键词,
            "filter": [
                "property": "object",
                "value": "page"
            ]
        ]
        
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, _) = try await URLSession.shared.data(for: request)
        
        guard let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
              let results = json["results"] as? [[String: Any]] else {
            throw NotionError.parseError
        }
        
        print("✅ 找到 \(results.count) 张匹配的卡片")
        return results
    }
    
    // MARK: - 写入数据
    
    /// 创建新页面（带 DNA 追溯）
    func 创建页面(标题: String, 内容: String, DNA追溯码: String) async throws -> String {
        
        print("📝 创建新页面：\(标题)")
        
        let url = URL(string: "\(baseURL)/pages")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue(apiVersion, forHTTPHeaderField: "Notion-Version")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = [
            "parent": ["database_id": databaseID],
            "properties": [
                "Name": [
                    "title": [
                        ["text": ["content": 标题]]
                    ]
                ],
                "DNA码": [
                    "rich_text": [
                        ["text": ["content": DNA追溯码]]
                    ]
                ]
            ],
            "children": [
                [
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": [
                        "rich_text": [
                            ["text": ["content": 内容]]
                        ]
                    ]
                ]
            ]
        ]
        
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw NotionError.createFailed
        }
        
        guard let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
              let pageID = json["id"] as? String else {
            throw NotionError.parseError
        }
        
        print("✅ 页面创建成功：\(pageID)")
        print("DNA: \(DNA追溯码)")
        
        return pageID
    }
    
    // MARK: - 辅助方法
    
    /// 提取页面标题
    func 提取标题(从页面 page: [String: Any]) -> String? {
        guard let properties = page["properties"] as? [String: Any],
              let titleProp = properties["Name"] as? [String: Any] ?? properties["title"] as? [String: Any],
              let titleArray = titleProp["title"] as? [[String: Any]],
              let firstTitle = titleArray.first,
              let text = firstTitle["plain_text"] as? String else {
            return nil
        }
        return text
    }
    
    /// 提取 DNA 追溯码
    func 提取DNA(从页面 page: [String: Any]) -> String? {
        guard let properties = page["properties"] as? [String: Any],
              let dnaProp = properties["DNA码"] as? [String: Any],
              let dnaArray = dnaProp["rich_text"] as? [[String: Any]],
              let firstDNA = dnaArray.first,
              let text = firstDNA["plain_text"] as? String else {
            return nil
        }
        return text
    }
}

// MARK: - 错误类型

enum NotionError: Error, LocalizedError {
    case invalidResponse
    case apiError(statusCode: Int)
    case parseError
    case createFailed
    case noAPIKey
    case noDatabaseID
    
    var errorDescription: String? {
        switch self {
        case .invalidResponse:
            return "无效的响应"
        case .apiError(let code):
            return "API 错误：HTTP \(code)"
        case .parseError:
            return "解析响应失败"
        case .createFailed:
            return "创建页面失败"
        case .noAPIKey:
            return "未找到 Notion API 密钥"
        case .noDatabaseID:
            return "未找到 Notion 数据库 ID"
        }
    }
}

// MARK: - 使用示例

extension NotionConnector {
    
    /// 示例：读取并打印所有卡片
    func 示例_读取卡片() async {
        do {
            let pages = try await 读取所有卡片()
            
            print("\n📚 知识库卡片：")
            for page in pages {
                if let title = 提取标题(从页面: page),
                   let dna = 提取DNA(从页面: page) {
                    print("  - \(title)")
                    print("    DNA: \(dna)")
                }
            }
            
        } catch {
            print("❌ 错误：\(error.localizedDescription)")
        }
    }
    
    /// 示例：创建一个带 DNA 的新页面
    func 示例_创建页面() async {
        let dna = 生成DNA(操作: "测试页面")
        
        do {
            let pageID = try await 创建页面(
                标题: "测试页面 - 共生体",
                内容: "这是一个由共生体创建的测试页面。",
                DNA追溯码: dna
            )
            
            print("✅ 页面创建成功：\(pageID)")
            
        } catch {
            print("❌ 错误：\(error.localizedDescription)")
        }
    }
}
