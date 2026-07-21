//龍芯⚡️2026-06-20-LONGHUN-DIARY-APP-v1.0
// 龙魂农历日记本 — iOS版主入口
// 原则：数据根留本地，API只作通道，平台不留原文只留DNA指纹

import SwiftUI
import CoreData

@main
struct 龙魂日记本App: App {
    // CoreData本地存储，明确禁用iCloud同步
    let 持久化容器: NSPersistentContainer = {
        let 容器 = NSPersistentContainer(name: "龙魂日记本")
        // 🔴 禁用iCloud同步 — 数据主权
        容器.persistentStoreDescriptions.first?.setOption(true as NSNumber,
            forKey: NSPersistentStoreRemoteChangeNotificationPostOptionKey)
        容器.loadPersistentStores { _, 错误 in
            if let 错误 = 错误 { fatalError("CoreData加载失败: \(错误)") }
        }
        return 容器
    }()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.managedObjectContext, 持久化容器.viewContext)
        }
    }
}
