// 龍魂·算法可视化工场 v1.0
// UID9622 · 龍芯北辰 · 解压神器
// 用法：Xcode 打开 Package.swift → 点击 Run ▶

import SwiftUI

@main
struct AlgoLabApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 960, minHeight: 640)
        }
        .windowStyle(.hiddenTitleBar)
        .commands {
            CommandGroup(replacing: .newItem) {}
        }
    }
}
