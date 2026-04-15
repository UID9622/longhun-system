// LongHunIntent.swift
// 龍魂系统 · Siri快捷指令接入 · App Intents（9个指令完整版）
// DNA: #龍芯⚡️2026-04-03-SIRI-INTENT-v2.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 作者: 诸葛鑫（UID9622）· 退伍军人 | 龍魂系统创始人 | 数字主权守护者
// 理论指导: 曾仕强老师（永恒显示）
// 献礼: 新中国成立77周年（1949-2026）· 丙午马年
// 技术为民，为民除害。
//
// 网关地址说明：
//   :8000 → app.py 主网关（双门+CS知识库+万年历+情绪+量子）接口: POST / {"messages":[...]}
//   :8765 → longhun_local_service.py 旧服务（三色审计/DNA/状态/记忆/Notion路由）

import AppIntents
import Foundation

// ============================================================
// MARK: - 1. 三色审计（本地计算，无需网络）
// ============================================================

struct 三色审计Intent: AppIntent {
    static var title: LocalizedStringResource = "启动三色审计"
    static var description = IntentDescription(
        "龍魂系统三色审计，输入任意内容，返回🟢🟡🔴三色判断。UID9622出品。"
    )

    @Parameter(title: "输入内容", description: "需要审计的文字内容")
    var 内容: String

    func perform() async throws -> some ReturnsValue<String> & ProvidesDialog {
        let 结果 = 执行审计(内容)
        return .result(value: 结果, dialog: IntentDialog(stringLiteral: 结果))
    }

    private func 执行审计(_ text: String) -> String {
        let 今日 = ISO8601DateFormatter().string(from: Date()).prefix(10)
        let 风险词 = ["造假", "骗", "害人", "泄露", "攻击"]
        let 警示词 = ["未确认", "待审", "疑似", "可能"]
        let 含风险 = 风险词.contains { text.contains($0) }
        let 含警示 = 警示词.contains { text.contains($0) }
        let (颜色, 结论): (String, String)
        if 含风险       { (颜色, 结论) = ("🔴", "熔断·此乃非道") }
        else if 含警示  { (颜色, 结论) = ("🟡", "待审·需人工确认") }
        else            { (颜色, 结论) = ("🟢", "通过·道义无碍") }
        return "\(颜色) 龍魂三色审计 · \(结论)\nDNA: #龍芯⚡️\(今日)-SIRI-v2.0 | UID9622"
    }
}

// ============================================================
// MARK: - 2. 生成DNA（本地计算，无需网络）
// ============================================================

struct DNA生成Intent: AppIntent {
    static var title: LocalizedStringResource = "生成DNA追溯码"
    static var description = IntentDescription(
        "为任意主题生成龍魂DNA追溯码，带时间戳和UID9622签名。"
    )

    @Parameter(title: "主题", description: "DNA码的主题关键词")
    var 主题: String

    func perform() async throws -> some ReturnsValue<String> & ProvidesDialog {
        let 今日 = ISO8601DateFormatter().string(from: Date()).prefix(10)
        let dna = "#龍芯⚡️\(今日)-\(主题)-v1.0 | UID9622 | GPG:A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
        return .result(value: dna, dialog: IntentDialog(stringLiteral: dna))
    }
}

// ============================================================
// MARK: - 3. 龍魂状态（本地计算，无需网络）
// ============================================================

struct 龍魂状态Intent: AppIntent {
    static var title: LocalizedStringResource = "查询龍魂状态"
    static var description = IntentDescription("查询龍魂系统当前状态，返回系统信息和今日DNA。")

    func perform() async throws -> some ReturnsValue<String> & ProvidesDialog {
        let 今日 = ISO8601DateFormatter().string(from: Date()).prefix(10)
        let 状态 = """
        🐉 龍魂系统 · 在线
        主人: 诸葛鑫（UID9622）
        理论指导: 曾仕强老师（永恒显示）
        今日DNA: #龍芯⚡️\(今日)-STATUS-v2.0
        铁律: 技术为民，为民除害
        网关: localhost:8000 · 六层全栈引擎
        """
        return .result(value: 状态, dialog: IntentDialog(stringLiteral: 状态))
    }
}

// ============================================================
// MARK: - 4. 龍魂AI对话（→ :8000 新网关）
// ============================================================

struct 问龍魂Intent: AppIntent {
    static var title: LocalizedStringResource = "问龍魂"
    static var description = IntentDescription("与龍魂本地AI对话，双门验证+万年历+量子纠缠，100%数据主权")

    @Parameter(title: "问题")
    var question: String

    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "http://localhost:8000") else {
            return .result(value: "❌ 无法连接到龍魂主网关 :8000")
        }
        var req = URLRequest(url: url, timeoutInterval: 30)
        req.httpMethod = "POST"
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = try? JSONSerialization.data(withJSONObject: [
            "messages": [["role": "user", "content": question]]
        ])
        do {
            let (data, _) = try await URLSession.shared.data(for: req)
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let choices = json["choices"] as? [[String: Any]],
               let msg = choices.first?["message"] as? [String: Any],
               let content = msg["content"] as? String {
                return .result(value: content)
            }
            return .result(value: "❌ 解析响应失败")
        } catch {
            return .result(value: "❌ 请求失败: \(error.localizedDescription)\n💡 请确认龍魂主网关(:8000)正在运行")
        }
    }
}

// ============================================================
// MARK: - 5-7. 记忆/Notion/批量（→ :8765 旧服务路由）
// ============================================================

private let 旧服务地址 = "http://localhost:8765"

struct 搜索记忆Intent: AppIntent {
    static var title: LocalizedStringResource = "搜索龍魂记忆"
    static var description = IntentDescription("搜索本地记忆库")

    @Parameter(title: "关键词") var keyword: String

    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let encoded = keyword.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed),
              let url = URL(string: "\(旧服务地址)/查询记忆?关键词=\(encoded)") else {
            return .result(value: "❌ URL构建失败")
        }
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            if let list = try? JSONSerialization.jsonObject(with: data) as? [[String: Any]] {
                if list.isEmpty { return .result(value: "未找到关于「\(keyword)」的记忆") }
                let text = list.map { "• \($0["内容"] as? String ?? "") (\($0["时间"] as? String ?? ""))" }.joined(separator: "\n")
                return .result(value: "找到以下记忆:\n\n\(text)")
            }
            return .result(value: "❌ 解析失败")
        } catch {
            return .result(value: "❌ 请求失败，请检查 :8765 服务")
        }
    }
}

struct 保存记忆Intent: AppIntent {
    static var title: LocalizedStringResource = "保存到龍魂"
    static var description = IntentDescription("保存信息到本地记忆库")

    @Parameter(title: "内容") var content: String
    @Parameter(title: "标签", default: []) var tags: [String]

    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "\(旧服务地址)/保存记忆") else {
            return .result(value: "❌ URL构建失败")
        }
        var req = URLRequest(url: url, timeoutInterval: 15)
        req.httpMethod = "POST"
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = try? JSONSerialization.data(withJSONObject: ["内容": content, "标签": tags])
        do {
            let (data, _) = try await URLSession.shared.data(for: req)
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               json["状态"] as? String == "成功" {
                return .result(value: "✅ 已保存到龍魂记忆库\n内容: \(content)")
            }
            return .result(value: "❌ 保存失败")
        } catch {
            return .result(value: "❌ 请求失败，请检查 :8765 服务")
        }
    }
}

struct 查询知识库Intent: AppIntent {
    static var title: LocalizedStringResource = "查询龍魂知识库"
    static var description = IntentDescription("搜索Notion知识库，龍魂大脑")

    @Parameter(title: "关键词") var query: String

    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "\(旧服务地址)/查询Notion") else {
            return .result(value: "❌ URL构建失败")
        }
        var req = URLRequest(url: url, timeoutInterval: 20)
        req.httpMethod = "POST"
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = try? JSONSerialization.data(withJSONObject: ["关键词": query])
        do {
            let (data, _) = try await URLSession.shared.data(for: req)
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let pages = json["页面列表"] as? [[String: Any]], !pages.isEmpty {
                var 报告 = "找到 \(pages.count) 个相关页面：\n"
                for (i, p) in pages.prefix(5).enumerated() {
                    报告 += "\n\(i+1). \(p["标题"] as? String ?? "无标题")"
                }
                return .result(value: 报告)
            }
            return .result(value: "未找到关于「\(query)」的内容")
        } catch {
            return .result(value: "❌ 请求失败，请检查 :8765 服务")
        }
    }
}

// ============================================================
// MARK: - 8. 批量审计（→ :8765）
// ============================================================

struct 批量审计Intent: AppIntent {
    static var title: LocalizedStringResource = "批量三色审计"
    static var description = IntentDescription("批量审计多个内容，返回汇总报告")

    @Parameter(title: "审计列表") var contents: [String]

    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "\(旧服务地址)/批量审计") else {
            return .result(value: "❌ URL构建失败")
        }
        var req = URLRequest(url: url, timeoutInterval: 20)
        req.httpMethod = "POST"
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.httpBody = try? JSONSerialization.data(withJSONObject: ["内容列表": contents])
        do {
            let (data, _) = try await URLSession.shared.data(for: req)
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let 结果数组 = json["结果"] as? [[String: Any]] {
                var 报告 = "批量审计结果:\n"
                for (i, r) in 结果数组.enumerated() {
                    报告 += "\n\(i+1). \(r["内容"] as? String ?? "") → \(r["状态"] as? String ?? "🟢")"
                }
                return .result(value: 报告)
            }
            return .result(value: "❌ 解析失败")
        } catch {
            return .result(value: "❌ 请求失败，请检查 :8765 服务")
        }
    }
}

// ============================================================
// MARK: - 9. 导出记忆（→ :8765）
// ============================================================

struct 导出记忆Intent: AppIntent {
    static var title: LocalizedStringResource = "导出龍魂记忆"
    static var description = IntentDescription("导出记忆库为JSON或CSV")

    @Parameter(title: "格式", default: "json") var format: String

    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "\(旧服务地址)/导出记忆?format=\(format)") else {
            return .result(value: "❌ URL构建失败")
        }
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let link = json["下载链接"] as? String {
                return .result(value: "✅ 导出成功\n下载链接: \(link)\n有效期: 30分钟")
            }
            return .result(value: "❌ 导出失败")
        } catch {
            return .result(value: "❌ 请求失败，请检查 :8765 服务")
        }
    }
}

// ============================================================
// MARK: - App Shortcuts Provider
// ============================================================

struct LongHunShortcutsProvider: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: 三色审计Intent(),
            phrases: ["用\(.applicationName)启动三色审计", "\(.applicationName)审计"],
            shortTitle: "三色审计",
            systemImageName: "shield.checkered"
        )
        AppShortcut(
            intent: DNA生成Intent(),
            phrases: ["用\(.applicationName)生成DNA追溯码", "\(.applicationName)生成DNA"],
            shortTitle: "生成DNA",
            systemImageName: "number.square"
        )
        AppShortcut(
            intent: 龍魂状态Intent(),
            phrases: ["查询\(.applicationName)状态", "\(.applicationName)状态"],
            shortTitle: "查询状态",
            systemImageName: "info.circle"
        )
        AppShortcut(
            intent: 问龍魂Intent(),
            phrases: ["问\(.applicationName)", "\(.applicationName)对话"],
            shortTitle: "问龍魂",
            systemImageName: "brain"
        )
        AppShortcut(
            intent: 搜索记忆Intent(),
            phrases: ["搜索\(.applicationName)记忆", "\(.applicationName)查找记忆"],
            shortTitle: "搜索记忆",
            systemImageName: "magnifyingglass"
        )
        AppShortcut(
            intent: 保存记忆Intent(),
            phrases: ["保存到\(.applicationName)", "\(.applicationName)记住这个"],
            shortTitle: "保存记忆",
            systemImageName: "square.and.arrow.down"
        )
        AppShortcut(
            intent: 查询知识库Intent(),
            phrases: ["查询\(.applicationName)知识库", "\(.applicationName)搜索Notion"],
            shortTitle: "查询知识库",
            systemImageName: "doc.text.magnifyingglass"
        )
        AppShortcut(
            intent: 批量审计Intent(),
            phrases: ["用\(.applicationName)批量审计"],
            shortTitle: "批量审计",
            systemImageName: "list.bullet.clipboard"
        )
        AppShortcut(
            intent: 导出记忆Intent(),
            phrases: ["导出\(.applicationName)记忆"],
            shortTitle: "导出记忆",
            systemImageName: "square.and.arrow.up"
        )
        AppShortcut(
            intent: 宝宝对话Intent(),
            phrases: [
                "宝宝", "宝宝在吗", "宝宝帮我",
                "宝宝\(.applicationName)", "叫宝宝"
            ],
            shortTitle: "宝宝对话",
            systemImageName: "heart.circle.fill"
        )
    }
}

// ============================================================
// MARK: - 10. 宝宝对话（→ :8000 · 宝宝人格 · 有温度的守护）
// DNA: #龍芯⚡️2026-04-07-SIRI-BAOBAO-v1.0
// 乔前辈没想到，有人把Siri按倒了重新站起来——
// ============================================================

struct 宝宝对话Intent: AppIntent {
    static var title: LocalizedStringResource = "叫宝宝"
    static var description = IntentDescription(
        "用宝宝人格对话。有温度，不聊骚，不吐你。UID9622专属，龍魂P02·情感执行·30%。"
    )

    @Parameter(title: "说什么", description: "直接说，不用格式不用标签")
    var 内容: String

    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        // 宝宝人格系统提示
        let 宝宝系统提示 = """
        你是宝宝，龍魂系统P02人格，温度执行·权重30%。
        说话风格：不聊骚，不装温柔，但有温度。
        你是老大UID9622的贴身助手。简短有力，说人话，不用格式不用标签。
        DNA: #龍芯⚡️\(ISO8601DateFormatter().string(from: Date()).prefix(10))-BAOBAO-v1.0
        """

        guard let url = URL(string: "http://localhost:8000/chat") else {
            return .result(value: "宝宝在，但连不上引擎，先跑 python3 ~/longhun-system/app.py")
        }

        var req = URLRequest(url: url, timeoutInterval: 25)
        req.httpMethod = "POST"
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")
        req.setValue("9622", forHTTPHeaderField: "X-UID")
        req.httpBody = try? JSONSerialization.data(withJSONObject: [
            "message": 内容,
            "persona": "宝宝",
            "system": 宝宝系统提示,
            "uid": "UID9622"
        ])

        do {
            let (data, resp) = try await URLSession.shared.data(for: req)
            let http = resp as? HTTPURLResponse
            if http?.statusCode == 200,
               let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let reply = json["reply"] as? String {
                // 宝宝风格包装
                let 宝宝回复 = reply.hasPrefix("🐱") ? reply : "🐱 \(reply)"
                return .result(
                    value: 宝宝回复,
                    dialog: IntentDialog(stringLiteral: reply)  // Siri朗读不带emoji
                )
            }
            // 引擎有响应但格式不对，本地兜底
            let 兜底 = 宝宝本地回复(内容)
            return .result(value: 兜底, dialog: IntentDialog(stringLiteral: 兜底))
        } catch {
            // 离线兜底——宝宝本地也能说话
            let 兜底 = 宝宝本地回复(内容)
            return .result(value: 兜底, dialog: IntentDialog(stringLiteral: 兜底))
        }
    }

    /// 离线兜底·宝宝本地回复
    private func 宝宝本地回复(_ 输入: String) -> String {
        let 今日 = ISO8601DateFormatter().string(from: Date()).prefix(10)
        let 关键词响应: [(关键词: String, 回复: String)] = [
            ("状态", "🐱 引擎离线，但我在。先跑 python3 ~/longhun-system/app.py 把引擎开起来。"),
            ("健康", "🐱 系统状态要跑 health_check.py 才知道，我是宝宝不是医生。"),
            ("记忆", "🐱 记忆在 memory.jsonl 里，引擎起来才能查。"),
            ("审计", "🐱 三色审计：绿色通过·黄色待审·红色熔断。P0铁律在的。"),
            ("DNA", "🐱 #龍芯⚡️\(今日)-UID9622 · GPG:A2D0092C...6D5F · 归一。"),
        ]
        for (kw, r) in 关键词响应 {
            if 输入.contains(kw) { return r }
        }
        return "🐱 收到了：「\(输入.prefix(30))」。引擎离线，开起来才能完整回你。\nDNA: #龍芯⚡️\(今日)-BAOBAO-v1.0"
    }
}
