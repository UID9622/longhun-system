// ═══════════════════════════════════════════════════════════
// 🎯 智能体编排器 · 协调所有连接器 · 钥匙权限守卫
// DNA: #龍芯⚡️2026-04-12-共生体-Orchestrator-v2.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: UID9622 诸葛鑫（龍芯北辰）
// ═══════════════════════════════════════════════════════════

import Foundation
import SwiftUI

/// 智能体编排器
/// 接收老大的指令 → 钥匙权限检查 → 通心译意图识别 → 分发到对应连接器 → 汇总结果
class AgentOrchestrator: ObservableObject {
    @Published var currentTask = ""
    @Published var taskLog: [TaskLogEntry] = []
    @Published var keyStatus = "未加载"

    let notion = NotionConnector()
    let engine = LocalEngineConnector()
    let masterKey = MasterKeyReader()  // 钥匙读取器（共享BaoBaoBrain中定义的类）

    struct TaskLogEntry: Identifiable {
        let id = UUID()
        let time: Date
        let action: String
        let result: String
        let dna: String
    }

    // MARK: - 钥匙初始化

    func initializeKey() {
        masterKey.reload()
        if masterKey.isLoaded {
            keyStatus = masterKey.frozen ? "⛔ 冻结" : "🔑 已授权(\(masterKey.enabledCount)项)"
        } else {
            keyStatus = "❌ 缺失"
        }
    }

    /// 权限守卫 —— 每个操作前先过这关
    private func guard权限(_ category: String, _ action: String) -> String? {
        masterKey.reload()
        if masterKey.frozen {
            return "⛔ 全局冻结中，老大去钥匙文件解除才行"
        }
        if !masterKey.check(category: category, action: action) {
            return "🚫 [\(category)/\(action)] 权限未开启。\n钥匙位置: \(masterKey.keyPath)"
        }
        return nil // nil = 通过
    }

    // MARK: - 主入口（通心译ETE + 钥匙守卫）

    /// 老大说话 → 钥匙检查 → 通心译翻译 → 执行
    func execute(_ input: String) async {
        await MainActor.run {
            currentTask = input
        }

        // 钥匙前置检查
        masterKey.reload()
        if masterKey.frozen {
            let entry = TaskLogEntry(time: Date(), action: input,
                result: "⛔ 全局冻结，拒绝执行", dna: "#龍芯⚡️FROZEN")
            await MainActor.run {
                taskLog.insert(entry, at: 0)
                currentTask = ""
            }
            return
        }

        // ETE第一层：听懂人话
        let intent = identifyIntent(input)

        // ETE第二层：钥匙验权 + 翻成行话
        let result: String
        switch intent {
        case .queryKnowledge(let keyword):
            if let denied = guard权限("Notion", "查询数据库") { result = denied }
            else { result = await queryKnowledge(keyword) }
        case .tricolorAudit(let content):
            if let denied = guard权限("审计系统", "三色审计") { result = denied }
            else { result = await runAudit(content) }
        case .chatAI(let prompt):
            if let denied = guard权限("AI模型", "Ollama本地对话") { result = denied }
            else { result = await chatLocal(prompt) }
        case .saveMemory(let content):
            if let denied = guard权限("记忆系统", "写入记忆") { result = denied }
            else { result = await saveToMemory(content) }
        case .checkServices:
            if let denied = guard权限("服务调度", "查看服务状态") { result = denied }
            else { result = await checkAllServices() }
        case .syncNotion(let pageId):
            if let denied = guard权限("Notion", "同步知识库") { result = denied }
            else { result = await syncFromNotion(pageId) }
        case .dispatchPython(let script):
            if let denied = guard权限("代码执行", "运行Python脚本") { result = denied }
            else { result = masterKey.dispatch(intent: "运行脚本", params: ["script": script]) }
        case .showPermissions:
            result = formatPermissions()
        case .unknown(let raw):
            result = "🐱 宝宝不确定你要干什么：「\(raw)」\n试试说：查知识/审计/聊天/保存/检查服务/权限"
        }

        // ETE第三层：不丢根（DNA留痕）
        let dna = "#龍芯⚡️\(dateString())-BaoBao-Task"
        let entry = TaskLogEntry(time: Date(), action: input, result: result, dna: dna)

        await MainActor.run {
            taskLog.insert(entry, at: 0)
            if taskLog.count > 50 { taskLog = Array(taskLog.prefix(50)) }
            currentTask = ""
        }
    }

    // MARK: - 意图识别

    private enum Intent {
        case queryKnowledge(String)
        case tricolorAudit(String)
        case chatAI(String)
        case saveMemory(String)
        case checkServices
        case syncNotion(String)
        case dispatchPython(String)
        case showPermissions
        case unknown(String)
    }

    private func identifyIntent(_ input: String) -> Intent {
        let lower = input.lowercased()

        // 钥匙/权限查询
        if lower.contains("权限") || lower.contains("钥匙") || lower.contains("开关") {
            return .showPermissions
        }

        // 运行脚本
        if lower.contains("运行") || lower.contains("执行") || lower.contains("跑一下") {
            return .dispatchPython(input)
        }

        if lower.contains("查") || lower.contains("知识") || lower.contains("搜索") {
            let keyword = input
                .replacingOccurrences(of: "查", with: "")
                .replacingOccurrences(of: "知识", with: "")
                .replacingOccurrences(of: "搜索", with: "")
                .trimmingCharacters(in: .whitespaces)
            return .queryKnowledge(keyword.isEmpty ? input : keyword)
        }

        if lower.contains("审计") || lower.contains("三色") || lower.contains("检查安全") {
            return .tricolorAudit(input)
        }

        if lower.contains("聊") || lower.contains("问") || lower.contains("帮我想") {
            return .chatAI(input)
        }

        if lower.contains("保存") || lower.contains("记住") || lower.contains("存一下") {
            return .saveMemory(input)
        }

        if lower.contains("服务") || lower.contains("状态") || lower.contains("在线") {
            return .checkServices
        }

        if lower.contains("同步") || lower.contains("notion") {
            return .syncNotion("")
        }

        return .unknown(input)
    }

    /// 格式化权限信息
    private func formatPermissions() -> String {
        let perms = masterKey.allPermissions()
        let enabled = perms.filter { $0.enabled }.map { "  ✅ \($0.category)/\($0.action)" }
        let disabled = perms.filter { !$0.enabled }.map { "  🚫 \($0.category)/\($0.action)" }
        return """
        🔑 宝宝当前权限

        已开启(\(enabled.count)项):
        \(enabled.joined(separator: "\n"))

        已关闭(\(disabled.count)项):
        \(disabled.joined(separator: "\n"))

        钥匙位置: \(masterKey.keyPath)
        """
    }

    // MARK: - 执行各模块

    private func queryKnowledge(_ keyword: String) async -> String {
        do {
            let results = try await engine.queryMemory(keyword: keyword)
            if results.isEmpty {
                return "🐱 没找到关于「\(keyword)」的知识，要不换个词？"
            }
            return "🐱 找到\(results.count)条相关知识"
        } catch {
            return "⚠️ 知识库连接失败：\(error.localizedDescription)"
        }
    }

    private func runAudit(_ content: String) async -> String {
        do {
            let result = try await engine.tricolorAudit(content: content)
            return "\(result.color) 审计结果：\(result.message)（评分：\(result.score)）"
        } catch {
            return "⚠️ 审计服务未启动，请检查:9622"
        }
    }

    private func chatLocal(_ prompt: String) async -> String {
        do {
            let reply = try await engine.chatWithOllama(prompt: prompt)
            return "🐱 \(reply)"
        } catch {
            return "⚠️ Ollama未启动，请检查:11434"
        }
    }

    private func saveToMemory(_ content: String) async -> String {
        do {
            let dna = "#龍芯⚡️\(dateString())-Memory-Save"
            try await engine.saveMemory(content: content, dna: dna)
            return "✅ 已保存到记忆库·DNA: \(dna)"
        } catch {
            return "⚠️ 记忆服务未启动，请检查:8765"
        }
    }

    private func checkAllServices() async -> String {
        await engine.checkAll()
        let statuses = engine.services.map { s in
            "\(s.isOnline ? "🟢" : "🔴") \(s.name) :\(s.port)"
        }.joined(separator: "\n")
        return "服务状态：\n\(statuses)"
    }

    private func syncFromNotion(_ pageId: String) async -> String {
        guard notion.isConnected else {
            return "⚠️ Notion未连接，请检查.env中的Token"
        }
        return "✅ Notion已连接，同步就绪"
    }

    // MARK: - 工具

    private func dateString() -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: Date())
    }
}
