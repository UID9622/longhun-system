// DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-IOS-SWIFTUI-v1.0-UID9622
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
//
// 龍魂 SwiftUI App 入口

import SwiftUI

@main
struct LonghunApp: App {
    @StateObject private var appState = LonghunAppState()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
        #if os(iOS)
        .backgroundTask(.appRefresh("com.longhun.supervision")) {
            await appState.runBackgroundSupervision()
        }
        #endif
    }
}

/// 全局 App 状态
@MainActor
final class LonghunAppState: ObservableObject {
    @Published var healthStatus: String = "checking..."
    @Published var lastReport: SupervisionReport?
    @Published var isSupervisionRunning: Bool = false
    
    private let engine = LonghunEngineImpl()
    
    init() {
        Task {
            try? await engine.initialize()
        }
    }
    
    func runBackgroundSupervision() async {
        isSupervisionRunning = true
        defer { isSupervisionRunning = false }
        
        do {
            let report = try await engine.runSupervision()
            lastReport = report
            healthStatus = report.summary
        } catch {
            healthStatus = "监督异常: \(error.localizedDescription)"
        }
    }
}
