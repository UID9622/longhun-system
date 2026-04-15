#!/usr/bin/env swift
// 🚨 龍魂紧急恢复系统 - 防止记录再次丢失
// DNA: #龍芯⚡️2026-04-06-EMERGENCY-RECOVERY-v1.0
// 数字指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

import Foundation

// ========================================
// 🔧 配置加载（从 .env 读取）
// ========================================
func loadEnv() -> [String: String] {
    guard let envPath = ProcessInfo.processInfo.environment["PWD"],
          let envData = try? String(contentsOfFile: "\(envPath)/.env") else {
        print("❌ 无法读取 .env 文件")
        return [:]
    }
    
    var config: [String: String] = [:]
    envData.components(separatedBy: .newlines).forEach { line in
        let trimmed = line.trimmingCharacters(in: .whitespaces)
        guard !trimmed.isEmpty, !trimmed.hasPrefix("#"),
              let equalIndex = trimmed.firstIndex(of: "=") else { return }
        
        let key = String(trimmed[..<equalIndex]).trimmingCharacters(in: .whitespaces)
        let value = String(trimmed[trimmed.index(after: equalIndex)...])
            .trimmingCharacters(in: CharacterSet(charactersIn: "' \t"))
        config[key] = value
    }
    return config
}

// ========================================
// 📝 本地备份记录（立即保存，永不丢失）
// ========================================
struct LocalBackup {
    static func save(content: String, tag: String = "GENERAL") {
        let timestamp = ISO8601DateFormatter().string(from: Date())
        let backupDir = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("longhun-system/backups")
        
        // 确保备份目录存在
        try? FileManager.default.createDirectory(at: backupDir, withIntermediateDirectories: true)
        
        // 保存到日期命名的文件
        let filename = "backup-\(Date().formatted(.iso8601.year().month().day())).jsonl"
        let filepath = backupDir.appendingPathComponent(filename)
        
        let entry = """
        {"timestamp":"\(timestamp)","tag":"\(tag)","content":"\(content.replacingOccurrences(of: "\"", with: "\\\""))"}
        
        """
        
        if let handle = FileHandle(forWritingAtPath: filepath.path) {
            handle.seekToEndOfFile()
            handle.write(entry.data(using: .utf8)!)
            handle.closeFile()
            print("✅ 已保存到: \(filepath.path)")
        } else {
            try? entry.write(to: filepath, atomically: true, encoding: .utf8)
            print("✅ 创建新备份: \(filepath.path)")
        }
    }
}

// ========================================
// 🔄 Notion 同步（双重保险）
// ========================================
struct NotionSync {
    let token: String
    let pageId: String
    
    func appendToPage(content: String) async throws {
        let url = URL(string: "https://api.notion.com/v1/blocks/\(pageId)/children")!
        var request = URLRequest(url: url)
        request.httpMethod = "PATCH"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("2022-06-28", forHTTPHeaderField: "Notion-Version")
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        
        let timestamp = Date().formatted(date: .abbreviated, time: .standard)
        let payload: [String: Any] = [
            "children": [[
                "object": "block",
                "type": "paragraph",
                "paragraph": [
                    "rich_text": [[
                        "type": "text",
                        "text": ["content": "[\(timestamp)] \(content)"]
                    ]]
                ]
            ]]
        ]
        
        request.httpBody = try JSONSerialization.data(withJSONObject: payload)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw NSError(domain: "NotionSync", code: -1, 
                         userInfo: [NSLocalizedDescriptionKey: "Notion API 失败"])
        }
        
        print("✅ 已同步到 Notion: \(pageId)")
    }
}

// ========================================
// 🏠 设备容器守护（数据主权回家）
// ========================================
struct DeviceContainerGuard {
    static func checkSnapshots() {
        let cacheDir = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("longhun-system/cache")
        
        print("\n🧬 检查 DNA 快照:")
        if let files = try? FileManager.default.contentsOfDirectory(at: cacheDir, includingPropertiesForKeys: nil) {
            let snapshots = files.filter { $0.pathExtension == "dna" }
                .sorted { $0.path > $1.path }
            
            if snapshots.isEmpty {
                print("⚠️ 未找到 DNA 快照（运行 time_machine.py 初始化）")
            } else {
                print("✅ 找到 \(snapshots.count) 个加密快照:")
                snapshots.prefix(5).forEach { print("   - \($0.lastPathComponent)") }
            }
        } else {
            print("⚠️ cache 目录不存在，运行: python3 ~/longhun-system/time_machine.py")
        }
    }
    
    static func ensureDataHome() {
        let requiredDirs = [
            "longhun-system/cache",       // DNA 快照
            "longhun-system/backups",     // JSONL 备份
            "longhun-system/logs"         // 运行日志
        ]
        
        print("\n🏠 确保数据回家容器:")
        for dir in requiredDirs {
            let path = FileManager.default.homeDirectoryForCurrentUser
                .appendingPathComponent(dir)
            
            if !FileManager.default.fileExists(atPath: path.path) {
                try? FileManager.default.createDirectory(at: path, withIntermediateDirectories: true)
                print("✅ 创建: ~/" + dir)
            } else {
                print("✅ 存在: ~/" + dir)
            }
        }
    }
    
    static func syncToPython() {
        print("\n🔄 调用 Python 时光机快照...")
        let task = Process()
        task.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
        task.arguments = [
            FileManager.default.homeDirectoryForCurrentUser
                .appendingPathComponent("longhun-system/time_machine.py")
                .path
        ]
        
        do {
            try task.run()
            task.waitUntilExit()
            if task.terminationStatus == 0 {
                print("✅ Python 时光机快照已触发")
            } else {
                print("⚠️ Python 脚本执行失败（退出码: \(task.terminationStatus)）")
            }
        } catch {
            print("⚠️ 无法调用 Python: \(error)")
            print("   手动运行: python3 ~/longhun-system/time_machine.py")
        }
    }
}

// ========================================
// 🚨 紧急恢复入口
// ========================================
@main
struct EmergencyRecovery {
    static func main() async {
        print("🚨 龍魂紧急恢复系统启动...")
        print("🧬 DNA: #龍芯⚡️2026-04-06-EMERGENCY-RECOVERY-v1.0")
        print("🔐 GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F")
        print("✅ 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z")
        
        let config = loadEnv()
        
        // 🏠 设备容器检查（核心功能）
        DeviceContainerGuard.ensureDataHome()
        DeviceContainerGuard.checkSnapshots()
        
        // 检查 JSONL 备份
        let backupDir = FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("longhun-system/backups")
        
        print("\n📂 检查 JSONL 本地备份:")
        if let files = try? FileManager.default.contentsOfDirectory(at: backupDir, includingPropertiesForKeys: nil) {
            let backups = files.filter { $0.pathExtension == "jsonl" }
                .sorted { $0.path > $1.path }
            
            if backups.isEmpty {
                print("⚠️ 未找到本地备份")
            } else {
                print("✅ 找到 \(backups.count) 个备份文件:")
                backups.prefix(5).forEach { print("   - \($0.lastPathComponent)") }
            }
        }
        
        // 测试记录保存
        print("\n💾 测试 JSONL 记录保存...")
        LocalBackup.save(content: "紧急恢复测试 - 系统正常", tag: "RECOVERY_TEST")
        
        // 调用 Python 时光机
        DeviceContainerGuard.syncToPython()
        
        // 提示后续操作
        print("\n📋 后续操作:")
        print("1️⃣ 检查 ~/longhun-system/cache/ 查看加密快照（.dna）")
        print("2️⃣ 检查 ~/longhun-system/backups/ 查看备份（.jsonl）")
        print("3️⃣ 使用下面的命令快速记录:")
        print("   ./quick-save.sh \"你的记录内容\"")
        print("4️⃣ 配置自动同步到 Notion（需要有效的 API Token）")
        print("\n🏠 归根曰静，是谓复命 —— 所有数据已回家 ✅")
    }
}
