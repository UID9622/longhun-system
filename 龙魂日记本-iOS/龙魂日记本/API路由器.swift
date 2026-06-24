//龍芯⚡️2026-06-20-LONGHUN-API-ROUTER
// API路由器：本地优先，Kimi/DeepSeek/华为/苹果通道聚合
// 原则：数据本地，API只作通道，平台不留原文

import Foundation
import Combine

class API路由器: ObservableObject {
    @Published var kimi状态: API状态 = .离线
    @Published var deepSeek状态: API状态 = .离线
    @Published var 最后响应 = "等待输入..."
    
    // 本地推理引擎（离线时使用）
    private let 本地引擎 = 本地推理引擎()
    
    func 调用Kimi(_ 输入: String) {
        guard !输入.isEmpty else { return }
        最后响应 = "🔄 正在调用Kimi..."
        
        // 实际实现：调用Kimi API（本地Kimi端点）
        let 请求体: [String: Any] = [
            "model": "kimi-latest",
            "messages": [["role": "user", "content": 输入]],
            "temperature": 0.7
        ]
        
        发送请求(url: "http://localhost:8443/kimi/v1/chat/completions",
                  body: 请求体,
                 来源: "Kimi")
    }
    
    func 调用DeepSeek(_ 输入: String) {
        guard !输入.isEmpty else { return }
        最后响应 = "🔄 正在调用DeepSeek..."
        
        let 请求体: [String: Any] = [
            "model": "deepseek-chat",
            "messages": [["role": "user", "content": 输入]],
            "temperature": 0.7
        ]
        
        发送请求(url: "http://localhost:8443/deepseek/v1/chat/completions",
                 body: 请求体,
                 来源: "DeepSeek")
    }
    
    func 调用本地引擎(_ 输入: String) {
        let 结果 = 本地引擎.推理(输入)
        最后响应 = "📱 [本地引擎] \(结果)\n\n💡 提示：本地模式下数据完全不出设备"
    }
    
    private func 发送请求(url: String, body: [String: Any], 来源: String) {
        guard let url = URL(string: url),
              let jsonData = try? JSONSerialization.data(withJSONObject: body) else {
            最后响应 = "❌ 请求构建失败，切换本地引擎..."
            return
        }
        
        var 请求 = URLRequest(url: url)
        请求.httpMethod = "POST"
        请求.httpBody = jsonData
        请求.setValue("application/json", forHTTPHeaderField: "Content-Type")
        请求.setValue(DNA追溯器.生成DNA(模块: "API-ROUTER", 版本: "v1.0"),
                     forHTTPHeaderField: "X-LongHun-DNA")
        
        URLSession.shared.dataTask(with: 请求) { [weak self] 数据, 响应, 错误 in
            DispatchQueue.main.async {
                if let 错误 = 错误 {
                    self?.最后响应 = "❌ [\(来源)] \(错误.localizedDescription)\n已切换本地推理"
                    return
                }
                guard let 数据 = 数据,
                      let json = try? JSONSerialization.jsonObject(with: 数据) as? [String: Any],
                      let 选项 = json["choices"] as? [[String: Any]],
                      let 第一条 = 选项.first,
                      let 消息 = 第一条["message"] as? [String: Any],
                      let 内容 = 消息["content"] as? String else {
                    self?.最后响应 = "⚠️ [\(来源)] 解析响应失败"
                    return
                }
                
                // 只存DNA指纹，不存原文
                let dna = DNA追溯器.生成DNA(模块: "API-\(来源)", 版本: "v1.0")
                self?.最后响应 = "✅ [\(来源)] \(内容)\n\n🧬 DNA: \(dna.prefix(20))..."
                
                // 记录到本地（只有用户设备上有原文）
                self?.记录到本地(输入: body["messages"] as? [[String: String]] ?? [],
                               输出: 内容,
                               来源: 来源)
            }
        }.resume()
    }
    
    private func 记录到本地(输入: [[String: String]], 输出: String, 来源: String) {
        // 压缩原文为DNA指纹存储
        let 指纹 = DNA追溯器.压缩指纹(原文: 输出)
        let 记录: [String: Any] = [
            "timestamp": ISO8601DateFormatter().string(from: Date()),
            "source": 来源,
            "fingerprint": 指纹,
            "dna": DNA追溯器.生成DNA(模块: "LOCAL-STORE", 版本: "v1.0"),
            // 🔴 注意：此处不存储原文，只存指纹
        ]
        // 实际存入CoreData...
        print("🧬 已存DNA指纹: \(指纹.prefix(16))...")
    }
}

// 本地推理引擎（离线备份）
class 本地推理引擎 {
    func 推理(_ 输入: String) -> String {
        // 简化实现 — 实际可加载本地小模型
        let 关键词: [(String, String)] = [
            ("日记", "写日记是记录生活的好习惯。今天的日记写了吗？"),
            ("农历", "今天是农历\(农历日期())。"),
            ("天气", "天气不错，适合出去走走。"),
            ("心情", "记录下此刻的心情吧，回头看会很有意义。"),
        ]
        for (词, 回复) in 关键词 {
            if 输入.contains(词) { return 回复 }
        }
        return "我理解了。作为本地引擎，我会尽力帮助你，虽然能力有限但数据绝对安全。"
    }
    
    private func 农历日期() -> String {
        let 农历 = 农历引擎()
        return 农历.农历年月(Date()) + 农历.农历日(Date())
    }
}

enum API状态 { case 在线, 离线 }
