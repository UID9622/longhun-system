// LongHunIntent.swift
// 龍魂系统·完整Siri Intent集成（7个指令）
// DNA: #龍芯⚡️2026-03-11-SIRI-COMPLETE-INTENT-v2.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: 诸葛鑫（UID9622）
// 理论指导: 曾仕强老师（永恒显示）
// 献礼: 新中国成立77周年（1949-2026）· 丙午马年
// 技术为民，为民除害。

import AppIntents
import Foundation

// ============================================================
// MARK: - 基础指令（原有3个）
// ============================================================

// MARK: - 1. 三色审计Intent

struct SanSeAuditIntent: AppIntent {
    static var title: LocalizedStringResource = "启动三色审计"
    static var description = IntentDescription("龍魂L2审计系统，返回🟢🟡🔴")
    
    @Parameter(title: "审计内容")
    var content: String
    
    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "http://localhost:8765/三色审计") else {
            return .result(value: "❌ 无法连接到龍魂本地服务")
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = ["内容": content] as [String : Any]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        
        do {
            let (data, _) = try await URLSession.shared.data(for: request)
            
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                let 状态 = json["状态"] as? String ?? "🟢"
                let 原因 = (json["原因"] as? [String])?.joined(separator: "\n") ?? ""
                let DNA = json["DNA追溯码"] as? String ?? ""
                
                let 报告 = """
                龍魂L2审计结果: \(状态)
                
                \(原因.isEmpty ? "审计通过 ✅" : 原因)
                
                \(DNA)
                """
                
                return .result(value: 报告)
            } else {
                return .result(value: "❌ 解析响应失败")
            }
        } catch {
            return .result(value: "❌ 请求失败\n\n💡 请确保龍魂本地服务正在运行")
        }
    }
}

// MARK: - 2. 生成DNA Intent

struct GenerateDNAIntent: AppIntent {
    static var title: LocalizedStringResource = "生成DNA追溯码"
    static var description = IntentDescription("生成龍魂DNA追溯码")
    
    @Parameter(title: "主题")
    var topic: String
    
    @Parameter(title: "类型", default: "")
    var type: String
    
    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "http://localhost:8765/生成DNA") else {
            return .result(value: "❌ 无法连接到龍魂本地服务")
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = [
            "主题": topic,
            "类型": type
        ] as [String : Any]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        
        do {
            let (data, _) = try await URLSession.shared.data(for: request)
            
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let DNA码 = json["DNA追溯码"] as? String,
               let GPG = json["GPG指纹"] as? String {
                
                let 结果 = """
                ✅ DNA追溯码已生成
                
                \(DNA码)
                
                GPG: \(GPG)
                创建者: UID9622 诸葛鑫
                理论指导: 曾仕强老师（永恒显示）
                """
                
                return .result(value: 结果)
            } else {
                return .result(value: "❌ 解析响应失败")
            }
        } catch {
            return .result(value: "❌ 请求失败")
        }
    }
}

// MARK: - 3. 查询状态Intent

struct QueryLongHunStatusIntent: AppIntent {
    static var title: LocalizedStringResource = "查询龍魂状态"
    static var description = IntentDescription("查询龍魂系统运行状态")
    
    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "http://localhost:8765/查询状态") else {
            return .result(value: "❌ 无法连接到龍魂本地服务")
        }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                let 系统 = json["系统名称"] as? String ?? "龍魂系统"
                let 状态 = json["状态"] as? String ?? "未知"
                let 模式 = json["运行模式"] as? String ?? "未知"
                let DNA = json["今日DNA"] as? String ?? ""
                let 数据主权 = json["数据主权"] as? String ?? ""
                
                let 报告 = """
                \(系统)
                
                状态: \(状态)
                模式: \(模式)
                数据主权: \(数据主权)
                
                \(DNA)
                
                理论指导: 曾仕强老师（永恒显示）
                """
                
                return .result(value: 报告)
            } else {
                return .result(value: "❌ 解析响应失败")
            }
        } catch {
            return .result(value: "❌ 请求失败")
        }
    }
}

// ============================================================
// MARK: - AI对话指令（新增4个）
// ============================================================

// MARK: - 4. 龍魂AI对话Intent

struct AskLongHunIntent: AppIntent {
    static var title: LocalizedStringResource = "问龍魂"
    static var description = IntentDescription("与龍魂本地AI对话，100%数据主权")
    
    @Parameter(title: "问题")
    var question: String
    
    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        // 调用本地模型API
        guard let url = URL(string: "http://localhost:8765/对话") else {
            return .result(value: "❌ 无法连接到龍魂本地服务")
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = [
            "消息": question,
            "历史": [],
            "使用工具": true
        ] as [String : Any]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        
        do {
            let (data, _) = try await URLSession.shared.data(for: request)
            
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let 回复 = json["回复"] as? String {
                return .result(value: 回复)
            } else {
                return .result(value: "❌ 解析响应失败")
            }
        } catch {
            return .result(value: "❌ 请求失败: \(error.localizedDescription)\n\n💡 请确保龍魂本地服务正在运行")
        }
    }
}

// MARK: - 搜索记忆Intent

struct SearchMemoryIntent: AppIntent {
    static var title: LocalizedStringResource = "搜索龍魂记忆"
    static var description = IntentDescription("搜索本地记忆库")
    
    @Parameter(title: "关键词")
    var keyword: String
    
    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "http://localhost:8765/查询记忆?关键词=\(keyword.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? "")") else {
            return .result(value: "❌ 无法连接到龍魂本地服务")
        }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            
            if let json = try? JSONSerialization.jsonObject(with: data) as? [[String: Any]] {
                let 记忆列表 = json.map { item -> String in
                    let 内容 = item["内容"] as? String ?? ""
                    let 时间 = item["时间"] as? String ?? ""
                    return "• \(内容) (\(时间))"
                }.joined(separator: "\n")
                
                if 记忆列表.isEmpty {
                    return .result(value: "未找到关于'\(keyword)'的记忆")
                } else {
                    return .result(value: "找到以下记忆:\n\n\(记忆列表)")
                }
            } else {
                return .result(value: "❌ 解析响应失败")
            }
        } catch {
            return .result(value: "❌ 请求失败: \(error.localizedDescription)")
        }
    }
}

// MARK: - 保存记忆Intent

struct SaveMemoryIntent: AppIntent {
    static var title: LocalizedStringResource = "保存到龍魂"
    static var description = IntentDescription("保存信息到本地记忆库")
    
    @Parameter(title: "内容")
    var content: String
    
    @Parameter(title: "标签", default: [])
    var tags: [String]
    
    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "http://localhost:8765/保存记忆") else {
            return .result(value: "❌ 无法连接到龍魂本地服务")
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = [
            "内容": content,
            "标签": tags
        ] as [String : Any]
        
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        
        do {
            let (data, _) = try await URLSession.shared.data(for: request)
            
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let 状态 = json["状态"] as? String,
               状态 == "成功" {
                return .result(value: "✅ 已保存到龍魂记忆库\n\n内容: \(content)\n标签: \(tags.joined(separator: ", "))")
            } else {
                return .result(value: "❌ 保存失败")
            }
        } catch {
            return .result(value: "❌ 请求失败: \(error.localizedDescription)")
        }
    }
}

// MARK: - 查询Notion Intent

struct QueryNotionIntent: AppIntent {
    static var title: LocalizedStringResource = "查询龍魂知识库"
    static var description = IntentDescription("搜索Notion知识库（17个核心页面）")
    
    @Parameter(title: "查询")
    var query: String
    
    @MainActor
    func perform() async throws -> some IntentResult & ReturnsValue<String> {
        guard let url = URL(string: "http://localhost:8765/查询Notion?查询=\(query.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? "")") else {
            return .result(value: "❌ 无法连接到龍魂本地服务")
        }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let 结果 = json["结果"] as? String,
               let 来源 = json["来源"] as? String {
                return .result(value: "Notion知识库查询结果:\n\n\(结果)\n\n来源: \(来源)")
            } else {
                return .result(value: "❌ 解析响应失败")
            }
        } catch {
            return .result(value: "❌ 请求失败: \(error.localizedDescription)")
        }
    }
}

// MARK: - App Shortcuts Provider

struct LongHunShortcutsProvider: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: SanSeAuditIntent(),
            phrases: [
                "用\(.applicationName)启动三色审计",
                "\(.applicationName)审计",
                "用\(.applicationName)L2审计"
            ],
            shortTitle: "三色审计",
            systemImageName: "shield.checkered"
        )
        
        AppShortcut(
            intent: GenerateDNAIntent(),
            phrases: [
                "用\(.applicationName)生成DNA追溯码",
                "\(.applicationName)生成DNA码",
                "用\(.applicationName)创建追溯码"
            ],
            shortTitle: "生成DNA",
            systemImageName: "number.square"
        )
        
        AppShortcut(
            intent: QueryLongHunStatusIntent(),
            phrases: [
                "查询\(.applicationName)状态",
                "\(.applicationName)状态",
                "用\(.applicationName)查询系统状态"
            ],
            shortTitle: "查询状态",
            systemImageName: "info.circle"
        )
        
        AppShortcut(
            intent: AskLongHunIntent(),
            phrases: [
                "问\(.applicationName)",
                "\(.applicationName)对话",
                "用\(.applicationName)问本地AI"
            ],
            shortTitle: "问龍魂",
            systemImageName: "brain"
        )
        
        AppShortcut(
            intent: SearchMemoryIntent(),
            phrases: [
                "搜索\(.applicationName)记忆",
                "用\(.applicationName)查找记忆",
                "\(.applicationName)搜索本地记忆"
            ],
            shortTitle: "搜索记忆",
            systemImageName: "magnifyingglass"
        )
        
        AppShortcut(
            intent: SaveMemoryIntent(),
            phrases: [
                "保存到\(.applicationName)",
                "用\(.applicationName)保存记忆",
                "\(.applicationName)记住这个"
            ],
            shortTitle: "保存记忆",
            systemImageName: "square.and.arrow.down"
        )
        
        AppShortcut(
            intent: QueryNotionIntent(),
            phrases: [
                "查询\(.applicationName)知识库",
                "用\(.applicationName)搜索Notion",
                "\(.applicationName)查询知识库"
            ],
            shortTitle: "查询知识库",
            systemImageName: "doc.text.magnifyingglass"
        )
    }
}
