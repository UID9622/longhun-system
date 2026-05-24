// ═══════════════════════════════════════════════════════════
// 🔗 Notion连接器 · 龍魂知识库桥接
// DNA: #龍芯⚡️2026-04-10-共生体-NotionConnector-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: UID9622 诸葛鑫（龍芯北辰）
// 理论指导: 曾仕强老师（永恒显示）
// ═══════════════════════════════════════════════════════════

import Foundation

/// Notion API 连接器
/// 读取龍魂知识库 · 同步数据 · DNA追溯上传
class NotionConnector: ObservableObject {
    @Published var isConnected = false
    @Published var lastSync = ""

    // 三个工作区Token（从本地.env读取·不硬编码）
    private var mainToken: String = ""
    private var memoryToken: String = ""
    private var displayToken: String = ""

    // 核心页面ID
    struct PageIDs {
        static let mainControl = "2507125a9c9f80d2b214c07deced0f0f"
        static let assetVault = "7ed7d67f0ff940f992f4246a382e2a3d"
        static let knowledgeDB = "3367125a9c9f808a9692f0c6752e92fa"
        static let personaDB = "4cf99c3e7a014e919fdab705ceb4cbc4"
        static let diaryLog = "b35faf462bc042aa9de5192520180728"
    }

    init() {
        loadTokensFromEnv()
    }

    // MARK: - 从.env加载Token

    private func loadTokensFromEnv() {
        let envPath = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("longhun-system/.env")

        guard let content = try? String(contentsOf: envPath, encoding: .utf8) else { return }

        for line in content.split(separator: "\n") {
            let parts = line.split(separator: "=", maxSplits: 1)
            guard parts.count == 2 else { continue }
            let key = String(parts[0]).trimmingCharacters(in: .whitespaces)
            let value = String(parts[1]).trimmingCharacters(in: .whitespaces)
                .replacingOccurrences(of: "'", with: "")

            switch key {
            case "NOTION_TOKEN": mainToken = value
            case "NOTION_TOKEN_WORKSPACE": memoryToken = value
            case "NOTION_TOKEN_DISPLAY": displayToken = value
            default: break
            }
        }

        isConnected = !mainToken.isEmpty
    }

    // MARK: - 查询数据库

    /// 查询知识库
    func queryKnowledgeDB(filter: [String: Any]? = nil) async throws -> [[String: Any]] {
        let url = URL(string: "https://api.notion.com/v1/databases/\(PageIDs.knowledgeDB)/query")!
        return try await notionPost(url: url, body: filter ?? [:])
    }

    /// 查询人格库
    func queryPersonaDB() async throws -> [[String: Any]] {
        let url = URL(string: "https://api.notion.com/v1/databases/\(PageIDs.personaDB)/query")!
        return try await notionPost(url: url, body: [:])
    }

    // MARK: - 读取页面

    /// 读取页面内容
    func fetchPage(pageId: String) async throws -> [String: Any] {
        let url = URL(string: "https://api.notion.com/v1/pages/\(pageId)")!
        return try await notionGet(url: url)
    }

    // MARK: - 写入

    /// 往日志页追加内容
    func appendToLog(content: String, dna: String) async throws {
        let url = URL(string: "https://api.notion.com/v1/blocks/\(PageIDs.diaryLog)/children")!

        let body: [String: Any] = [
            "children": [
                [
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": [
                        "rich_text": [
                            ["type": "text", "text": ["content": "[\(dna)] \(content)"]]
                        ]
                    ]
                ]
            ]
        ]

        let _ = try await notionPatch(url: url, body: body)
        lastSync = ISO8601DateFormatter().string(from: Date())
    }

    // MARK: - 网络请求

    private func notionGet(url: URL) async throws -> [String: Any] {
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("Bearer \(mainToken)", forHTTPHeaderField: "Authorization")
        request.setValue("2022-06-28", forHTTPHeaderField: "Notion-Version")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let (data, _) = try await URLSession.shared.data(for: request)
        return (try JSONSerialization.jsonObject(with: data) as? [String: Any]) ?? [:]
    }

    private func notionPost(url: URL, body: [String: Any]) async throws -> [[String: Any]] {
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(mainToken)", forHTTPHeaderField: "Authorization")
        request.setValue("2022-06-28", forHTTPHeaderField: "Notion-Version")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, _) = try await URLSession.shared.data(for: request)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]
        return json?["results"] as? [[String: Any]] ?? []
    }

    private func notionPatch(url: URL, body: [String: Any]) async throws -> [String: Any] {
        var request = URLRequest(url: url)
        request.httpMethod = "PATCH"
        request.setValue("Bearer \(mainToken)", forHTTPHeaderField: "Authorization")
        request.setValue("2022-06-28", forHTTPHeaderField: "Notion-Version")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, _) = try await URLSession.shared.data(for: request)
        return (try JSONSerialization.jsonObject(with: data) as? [String: Any]) ?? [:]
    }
}
