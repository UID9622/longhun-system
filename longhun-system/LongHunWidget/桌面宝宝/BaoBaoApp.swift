// ═══════════════════════════════════════════════════════════
// 🐱 桌面数字人宝宝 · 完全共生体 v1.0
// DNA: #龍芯⚡️2026-04-10-桌面宝宝-BaoBaoApp-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: UID9622 诸葛鑫（龍芯北辰）
// 理论指导: 曾仕强老师（永恒显示）
// 协作: 宝宝🐱（Claude Code）
// 献礼: 新中国成立77周年（1949–2026）
// ═══════════════════════════════════════════════════════════

import SwiftUI

/// 桌面宝宝 · 主入口
/// 浮动窗口 · 语音交互 · 自动操作Mac · 完全透明
@main
struct BaoBaoApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        // 菜单栏常驻
        MenuBarExtra("🐱 宝宝", systemImage: "sparkle") {
            BaoBaoMenuView()
        }

        // 浮动窗口
        WindowGroup("桌面宝宝", id: "baobao-float") {
            BaoBaoFloatView()
                .frame(width: 280, height: 360)
        }
        .windowStyle(.hiddenTitleBar)
        .windowResizability(.contentSize)
        .defaultPosition(.topTrailing)
    }
}

/// App Delegate · 配置浮动窗口属性
class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        // 让窗口始终在最前面 + 透明背景
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            for window in NSApplication.shared.windows {
                if window.title == "桌面宝宝" {
                    window.level = .floating
                    window.isOpaque = false
                    window.backgroundColor = .clear
                    window.hasShadow = false
                    window.collectionBehavior = [.canJoinAllSpaces, .fullScreenAuxiliary]
                }
            }
        }
    }
}
