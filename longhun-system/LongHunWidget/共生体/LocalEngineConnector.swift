// ═══════════════════════════════════════════════════════════
// 🐉 本地引擎连接器 · 接通8765/9622/11434
// DNA: #龍芯⚡️2026-04-10-共生体-LocalEngine-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: UID9622 诸葛鑫（龍芯北辰）
// ═══════════════════════════════════════════════════════════

import Foundation

/// 本地引擎连接器
/// 接通龍魂本地服务(:8765) + CNSH网关(:9622) + Ollama(:11434)
class LocalEngineConnector: ObservableObject {
    @Published var services: [ServiceStatus] = []

    struct ServiceStatus: Identifiable {
        let id = UUID()
        let name: String
        let port: Int
        var isOnline: Bool = false
        var lastCheck: Date = Date()
    }

    // 服务端点
    enum Endpoint {
        static let localService = "http://localhost:8765"
        static let cnshGateway = "http://localhost:9622"
        static let ollama = "http://localhost:11434"
    }

    init() {
        services = [
            ServiceStatus(name: "龍魂本地服务", port: 8765),
            ServiceStatus(name: "CNSH网关", port: 9622),
            ServiceStatus(name: "Ollama", port: 11434),
        ]
    }

    // MARK: - 健康检查

    /// 检查所有服务状态
    func checkAll() async {
        for i in services.indices {
            let port = services[i].port
            let online = await checkPort(port)
            await MainActor.run {
                services[i].isOnline = online
                services[i].lastCheck = Date()
            }
        }
    }

    private func checkPort(_ port: Int) async -> Bool {
        let url = URL(string: "http://localhost:\(port)/")!
        var request = URLRequest(url: url)
        request.timeoutInterval = 2

        do {
            let (_, response) = try await URLSession.shared.data(for: request)
            return (response as? HTTPURLResponse)?.statusCode != nil
        } catch {
            return false
        }
    }

    // MARK: - 三色审计（:9622）

    /// 执行三色审计
    func tricolorAudit(content: String) async throws -> AuditResult {
        let url = URL(string: "\(Endpoint.cnshGateway)/api/audit")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = ["content": content]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, _) = try await URLSession.shared.data(for: request)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] ?? [:]

        return AuditResult(
            color: json["color"] as? String ?? "🟡",
            score: json["score"] as? Int ?? 50,
            message: json["message"] as? String ?? "待确认"
        )
    }

    struct AuditResult {
        let color: String   // 🟢🟡🔴
        let score: Int      // 0-100
        let message: String
    }

    // MARK: - Ollama对话（:11434）

    /// 跟本地模型对话
    func chatWithOllama(prompt: String, model: String = "qwen2.5:7b") async throws -> String {
        let url = URL(string: "\(Endpoint.ollama)/api/generate")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.timeoutInterval = 60

        let body: [String: Any] = [
            "model": model,
            "prompt": prompt,
            "stream": false,
        ]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, _) = try await URLSession.shared.data(for: request)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] ?? [:]

        return json["response"] as? String ?? "（无响应）"
    }

    // MARK: - 记忆查询（:8765）

    /// 查询记忆
    func queryMemory(keyword: String) async throws -> [[String: Any]] {
        let encoded = keyword.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? keyword
        let url = URL(string: "\(Endpoint.localService)/查询记忆?关键词=\(encoded)")!

        let (data, _) = try await URLSession.shared.data(from: url)
        let json = try JSONSerialization.jsonObject(with: data)

        if let array = json as? [[String: Any]] {
            return array
        }
        return []
    }

    /// 保存记忆
    func saveMemory(content: String, dna: String) async throws {
        let url = URL(string: "\(Endpoint.localService)/保存记忆")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: String] = [
            "content": content,
            "dna": dna,
            "uid": "UID9622",
        ]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let _ = try await URLSession.shared.data(for: request)
    }

    // MARK: - DNA生成（:8765）

    /// 生成DNA追溯码
    func generateDNA(module: String, version: String = "v1.0") async throws -> String {
        let url = URL(string: "\(Endpoint.localService)/生成DNA")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = ["module": module, "version": version]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, _) = try await URLSession.shared.data(for: request)
        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any] ?? [:]

        return json["dna"] as? String ?? "#龍芯⚡️\(module)-\(version)"
    }
}
