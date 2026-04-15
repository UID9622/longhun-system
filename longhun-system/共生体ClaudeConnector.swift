// ClaudeConnector.swift
// Claude API 连接器 - 共生体核心组件
// DNA追溯码: #龍芯⚡️2026-04-10-ClaudeConnector-v1.0
// 创建者: UID9622 诸葛鑫

import Foundation
import Combine

/// Claude 连接器 - 调用 Claude API 生成代码和解释需求
@MainActor
class ClaudeConnector: ObservableObject {
    
    // MARK: - 配置
    
    /// Claude API 密钥（从 Keychain 读取）
    private var apiKey: String {
        // TODO: 从 macOS Keychain 读取
        // 现在先用环境变量
        return ProcessInfo.processInfo.environment["CLAUDE_API_KEY"] ?? ""
    }
    
    /// API 基础 URL
    private let baseURL = "https://api.anthropic.com/v1"
    
    /// 当前模型
    private let model = "claude-3-5-sonnet-20241022"
    
    // MARK: - 状态
    
    @Published var isConnected: Bool = false
    @Published var lastResponse: String = ""
    @Published var isProcessing: Bool = false
    
    // MARK: - DNA 追溯
    
    private func 生成DNA(任务: String) -> String {
        let 时间戳 = Int(Date().timeIntervalSince1970)
        return "#龍芯⚡️\(时间戳)-Claude-\(任务)"
    }
    
    // MARK: - 核心方法
    
    /// 调用 Claude API - 生成代码
    /// - Parameters:
    ///   - prompt: 老大的需求（原始输入）
    ///   - systemPrompt: 系统提示词（带数学六根）
    /// - Returns: Claude 的回复
    func 生成代码(需求 prompt: String, 系统提示词 systemPrompt: String? = nil) async throws -> String {
        
        isProcessing = true
        defer { isProcessing = false }
        
        // 构建请求
        let url = URL(string: "\(baseURL)/messages")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue(apiKey, forHTTPHeaderField: "x-api-key")
        request.setValue("2023-06-01", forHTTPHeaderField: "anthropic-version")
        request.setValue("application/json", forHTTPHeaderField: "content-type")
        
        // 构建消息
        let messages: [[String: Any]] = [
            [
                "role": "user",
                "content": prompt
            ]
        ]
        
        var body: [String: Any] = [
            "model": model,
            "max_tokens": 8192,
            "messages": messages
        ]
        
        // 添加系统提示词（带数学六根）
        if let system = systemPrompt {
            body["system"] = system
        } else {
            // 默认系统提示词 - 带龍魂六根
            body["system"] = """
            你是龍魂共生体中的 Claude 助手。你的任务是生成高质量的 Swift 代码。
            
            核心规则：
            1. 使用 Swift 6.0 最新语法
            2. 100% 苹果原生技术（SwiftUI/AppKit/Foundation）
            3. 代码必须带 DNA 追溯码
            4. 每个函数带数字根检查
            5. 遵循龍魂六根原则：
               - dr(n) = 1+((n-1)%9) - 数字根
               - f(x) = x - 原点不变
               - E = R×I×T^(-α) - 能量场
               - 三才(天,地,人) - 时机检查
               - 369 共振 - 周期对齐
               - C_root = C_brute / D_culture - 有根省算力
            
            输出要求：
            - 直接输出可运行的 Swift 代码
            - 中文注释
            - DNA 追溯码在文件头
            - 不解释，只输出代码
            """
        }
        
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        // 发送请求
        let (data, response) = try await URLSession.shared.data(for: request)
        
        // 检查响应
        guard let httpResponse = response as? HTTPURLResponse else {
            throw ClaudeError.invalidResponse
        }
        
        guard httpResponse.statusCode == 200 else {
            if let errorText = String(data: data, encoding: .utf8) {
                print("❌ Claude API 错误: \(errorText)")
            }
            throw ClaudeError.apiError(statusCode: httpResponse.statusCode)
        }
        
        // 解析响应
        guard let json = try JSONSerialization.jsonObject(with: data) as? [String: Any],
              let content = json["content"] as? [[String: Any]],
              let firstContent = content.first,
              let text = firstContent["text"] as? String else {
            throw ClaudeError.parseError
        }
        
        lastResponse = text
        isConnected = true
        
        print("✅ Claude 生成代码成功")
        print("DNA: \(生成DNA(任务: "代码生成"))")
        
        return text
    }
    
    /// 解释需求 - 把老大的碎片话翻译成结构化需求
    func 解释需求(_ 原始输入: String) async throws -> String {
        let prompt = """
        老大说了这段话（可能是碎片、骚话、啊啊啊、哒哒哒）：
        
        \"\"\(原始输入)\"\"
        
        请帮我翻译成结构化的技术需求，格式：
        
        ### 核心需求
        - [简洁描述]
        
        ### 技术要点
        - [关键技术1]
        - [关键技术2]
        
        ### 实现步骤
        1. [步骤1]
        2. [步骤2]
        
        直接输出，不要解释。
        """
        
        return try await 生成代码(需求: prompt)
    }
    
    /// 验证代码 - 检查生成的代码是否符合龍魂规范
    func 验证代码(_ code: String) -> Bool {
        // 检查是否包含 DNA 追溯码
        let hasDNA = code.contains("#龍芯⚡️")
        
        // 检查是否使用苹果原生技术
        let isNative = code.contains("import SwiftUI") ||
                       code.contains("import AppKit") ||
                       code.contains("import Foundation")
        
        // 检查是否有中文注释
        let hasChinese = code.range(of: "[\u{4e00}-\u{9fff}]", options: .regularExpression) != nil
        
        return hasDNA && isNative && hasChinese
    }
}

// MARK: - 错误类型

enum ClaudeError: Error, LocalizedError {
    case invalidResponse
    case apiError(statusCode: Int)
    case parseError
    case noAPIKey
    
    var errorDescription: String? {
        switch self {
        case .invalidResponse:
            return "无效的响应"
        case .apiError(let code):
            return "API 错误：HTTP \(code)"
        case .parseError:
            return "解析响应失败"
        case .noAPIKey:
            return "未找到 Claude API 密钥"
        }
    }
}

// MARK: - 使用示例

extension ClaudeConnector {
    
    /// 示例：生成一个简单的 SwiftUI 视图
    func 示例_生成视图() async {
        do {
            let code = try await 生成代码(需求: """
                帮我写一个 SwiftUI 视图，显示"龍魂共生体"，带一个按钮"开始"。
                要求：
                - 带 DNA 追溯码
                - 中文注释
                - 苹果原生技术
                """)
            
            print("生成的代码：\n\(code)")
            
            // 验证
            if 验证代码(code) {
                print("✅ 代码验证通过")
            } else {
                print("❌ 代码不符合龍魂规范")
            }
            
        } catch {
            print("❌ 错误：\(error.localizedDescription)")
        }
    }
}
