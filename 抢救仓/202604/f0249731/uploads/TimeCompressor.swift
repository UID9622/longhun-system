// ═══════════════════════════════════════════════════════════
// ⏱️ 时间线压缩引擎 · Swift版
// DNA: #龍芯⚡️2026-04-10-时间压缩-Swift-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: UID9622 诸葛鑫（龍芯北辰）
// ═══════════════════════════════════════════════════════════

import Foundation

/// 时间线压缩引擎
/// L5五层架构 · E=R×I×T^(-α) · 事件筛选与沉淀
class TimeCompressor: ObservableObject {

    @Published var events: [TimeEvent] = []

    // MARK: - 事件定义

    struct TimeEvent: Identifiable, Codable {
        let id: UUID
        let name: String
        let date: Date
        let R: Double        // 影响范围
        let I: Double        // 重要性 0-100
        let alpha: Double    // 衰减指数
        let layer: String    // L0-L4
        let dna: String      // DNA追溯码

        /// 计算当前能量值
        func energy(at now: Date = Date()) -> Double {
            let days = max(1, now.timeIntervalSince(date) / 86400.0)
            if alpha < 0.0001 { return R * I } // L0不衰减
            return R * I * pow(days, -alpha)
        }

        /// 百年后能量保留率
        var centuryRetention: Double {
            return pow(36500.0, -alpha) * 100.0
        }

        /// 半衰期（天）
        var halfLifeDays: Double {
            guard alpha > 0.0001 else { return .infinity }
            return pow(2.0, 1.0 / alpha)
        }
    }

    // MARK: - 事件创建

    /// 创建L0永恒事件（不衰减）
    func addEternal(name: String, R: Double, I: Double) {
        let event = TimeEvent(
            id: UUID(), name: name, date: Date(),
            R: R, I: I, alpha: 0,
            layer: "L0·永恒", dna: generateDNA(name)
        )
        events.insert(event, at: 0)
    }

    /// 创建L1百年事件
    func addCentury(name: String, R: Double, I: Double) {
        let event = TimeEvent(
            id: UUID(), name: name, date: Date(),
            R: R, I: I, alpha: 0.01,
            layer: "L1·百年", dna: generateDNA(name)
        )
        events.insert(event, at: 0)
    }

    /// 创建L2十年事件
    func addDecade(name: String, R: Double, I: Double) {
        let event = TimeEvent(
            id: UUID(), name: name, date: Date(),
            R: R, I: I, alpha: 0.1,
            layer: "L2·十年", dna: generateDNA(name)
        )
        events.insert(event, at: 0)
    }

    /// 创建L3日常事件
    func addDaily(name: String, R: Double, I: Double) {
        let event = TimeEvent(
            id: UUID(), name: name, date: Date(),
            R: R, I: I, alpha: 1.0,
            layer: "L3·日常", dna: generateDNA(name)
        )
        events.insert(event, at: 0)
    }

    /// 创建L4瞬时事件
    func addInstant(name: String, R: Double, I: Double) {
        let event = TimeEvent(
            id: UUID(), name: name, date: Date(),
            R: R, I: I, alpha: 100.0,
            layer: "L4·瞬时", dna: generateDNA(name)
        )
        events.insert(event, at: 0)
    }

    // MARK: - 压缩包生成

    /// 生成时间线压缩包（按能量排序·过滤低能量事件）
    func compress(threshold: Double = 1.0) -> [TimeEvent] {
        let now = Date()
        return events
            .filter { $0.energy(at: now) >= threshold }
            .sorted { $0.energy(at: now) > $1.energy(at: now) }
    }

    /// 按层级分组
    func groupByLayer() -> [String: [TimeEvent]] {
        Dictionary(grouping: events) { $0.layer }
    }

    // MARK: - 持久化

    /// 保存到本地JSON
    func save() {
        let path = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("longhun-system/timeline.json")
        if let data = try? JSONEncoder().encode(events) {
            try? data.write(to: path)
        }
    }

    /// 从本地加载
    func load() {
        let path = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("longhun-system/timeline.json")
        if let data = try? Data(contentsOf: path),
           let loaded = try? JSONDecoder().decode([TimeEvent].self, from: data) {
            events = loaded
        }
    }

    // MARK: - DNA生成

    private func generateDNA(_ name: String) -> String {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        let date = formatter.string(from: Date())
        let short = name.prefix(10).replacingOccurrences(of: " ", with: "-")
        return "#龍芯⚡️\(date)-\(short)-v1.0"
    }
}
