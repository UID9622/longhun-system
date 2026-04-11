// ═══════════════════════════════════════════════════════════
// 🎯 智能体编排器 · 协调所有连接器
// DNA: #龍芯⚡️2026-04-10-共生体-Orchestrator-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: UID9622 诸葛鑫（龍芯北辰）
// ═══════════════════════════════════════════════════════════

import Foundation
import SwiftUI

/// 智能体编排器
/// 接收老大的指令 → 通心译意图识别 → 分发到对应连接器 → 汇总结果
class AgentOrchestrator: ObservableObject {
    @Published var currentTask = ""
    @Published var taskLog: [TaskLogEntry] = []

    let notion = NotionConnector()
    let engine = LocalEngineConnector()

    struct TaskLogEntry: Identifiable {
        let id = UUID()
        let time: Date
        let action: String
        let result: String
        let dna: String
    }

    // MARK: - 主入口（通心译ETE）

    /// 老大说话 → 通心译翻译 → 执行
    func execute(_ input: String) async {
        await MainActor.run {
            currentTask = input
        }

        // ETE第一层：听懂人话
        let intent = identifyIntent(input)

        // ETE第二层：翻成行话
        let result: String
        switch intent {
        case .queryKnowledge(let keyword):
            result = await queryKnowledge(keyword)
        case .tricolorAudit(let content):
            result = await runAudit(content)
        case .chatAI(let prompt):
            result = await chatLocal(prompt)
        case .saveMemory(let content):
            result = await saveToMemory(content)
        case .checkServices:
            result = await checkAllServices()
        case .syncNotion(let pageId):
            result = await syncFromNotion(pageId)
        case .unknown(let raw):
            result = "🐱 宝宝不确定你要干什么：「\(raw)」\n试试说：查知识/审计/聊天/保存/检查服务"
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
        case unknown(String)
    }

    private func identifyIntent(_ input: String) -> Intent {
        let lower = input.lowercased()

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
