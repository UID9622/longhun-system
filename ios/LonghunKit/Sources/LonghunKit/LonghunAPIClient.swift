// DNA: #龍芯⚡️丙午·丙申·乙卯·申时·䷐随-IOS-API-v1.0-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
// 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
//
// 龍魂·iOS API 客户端
// 对接鲲鹏网关（uid9622.cn /api/*）· 端侧数据主权：隐私请求只传哈希指纹

import Foundation

/// 龍魂 API 客户端（Async/Await · 数据主权优先）
public struct LonghunAPIClient: Sendable {

    /// 默认网关（鲲鹏）
    public static let kunpeng = URL(string: "https://uid9622.cn")!

    public let baseURL: URL
    public let session: URLSession
    public var authToken: String?   // 认证令牌（仅内存驻留，不进 UserDefaults）

    public init(baseURL: URL = LonghunAPIClient.kunpeng,
                session: URLSession = .shared,
                authToken: String? = nil) {
        self.baseURL = baseURL
        self.session = session
        self.authToken = authToken
    }

    // MARK: - 通用请求

    public struct LonghunAPIError: Error, LocalizedError {
        public let status: Int
        public let message: String
        public init(status: Int, message: String) {
            self.status = status
            self.message = message
        }
        public var errorDescription: String? {
            "🟡 龍魂网关错误 (\(status)): \(message)"
        }
    }

    public func request<T: Decodable>(
        _ path: String,
        method: String = "GET",
        body: Data? = nil
    ) async throws -> T {
        var url = baseURL.appendingPathComponent(path)
        // 处理查询参数（path 可能带 ?x=y）
        if let queryStart = path.firstIndex(of: "?"), let base = path.prefix(upTo: queryStart).removingPercentEncoding {
            url = baseURL.appendingPathComponent(base)
        }
        var req = URLRequest(url: url)
        req.httpMethod = method
        req.timeoutInterval = 30
        req.setValue("application/json", forHTTPHeaderField: "Accept")
        if let body {
            req.setValue("application/json", forHTTPHeaderField: "Content-Type")
            req.httpBody = body
        }
        if let authToken {
            req.setValue("Bearer \(authToken)", forHTTPHeaderField: "Authorization")
        }

        let (data, response) = try await session.data(for: req)
        guard let http = response as? HTTPURLResponse else {
            throw LonghunAPIError(status: -1, message: "无响应")
        }
        guard (200..<300).contains(http.statusCode) else {
            let msg = String(data: data, encoding: .utf8) ?? "未知错误"
            throw LonghunAPIError(status: http.statusCode, message: String(msg.prefix(200)))
        }
        return try JSONDecoder().decode(T.self, from: data)
    }

    // MARK: - 已验证端点

    /// 健康检查 GET /api/health
    public struct HealthResponse: Decodable, Sendable {
        public let status: String?
        public let message: String?
        public let services: [String]?
    }

    public func health() async throws -> HealthResponse {
        try await request("/api/health")
    }

    /// AI 对话 POST /api/ai/chat
    /// 隐私铁律：prompt 仅本地构造，敏感上下文默认传哈希指纹
    public func aiChat(prompt: String, system: String = "龍魂·iOS端") async throws -> String {
        struct ChatRequest: Encodable {
            let prompt: String
            let system: String
        }
        struct ChatResponse: Decodable {
            let reply: String?
            let content: String?
            let message: String?
        }
        let body = try JSONEncoder().encode(ChatRequest(prompt: prompt, system: system))
        let res: ChatResponse = try await request("/api/ai/chat", method: "POST", body: body)
        return res.reply ?? res.content ?? res.message ?? ""
    }

    /// 拉取 onboarding 规则包 GET /api/onboarding/bootstrap
    public func onboardingBootstrap() async throws -> [String: Any] {
        let (data, response) = try await session.data(from: baseURL.appendingPathComponent("api/onboarding/bootstrap"))
        guard let http = response as? HTTPURLResponse, (200..<300).contains(http.statusCode) else {
            throw LonghunAPIError(status: -1, message: "onboarding 拉取失败")
        }
        let json = try JSONSerialization.jsonObject(with: data)
        return (json as? [String: Any]) ?? [:]
    }
}
