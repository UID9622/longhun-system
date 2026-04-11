// ═══════════════════════════════════════════════════════════
// 🐱 桌面宝宝 · 菜单栏视图
// DNA: #龍芯⚡️2026-04-10-桌面宝宝-MenuView-v1.0
// ═══════════════════════════════════════════════════════════

import SwiftUI

/// 菜单栏下拉菜单
struct BaoBaoMenuView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            // 标题
            HStack {
                Text("🐱 宝宝 · 龍魂共生体")
                    .font(.headline)
                Spacer()
                Text("v1.0")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
            .padding(.bottom, 4)

            Divider()

            // 快捷操作
            Button("✨ 快捷操作面板") {
                // 打开浮动窗口
            }

            Button("🛡️ 三色审计") {
                // 调用 :9622 审计API
            }

            Button("📊 系统状态") {
                // 显示服务状态
            }

            Button("🧬 DNA追溯") {
                // 显示当前DNA
            }

            Divider()

            // 服务状态
            HStack {
                Circle().fill(.green).frame(width: 6, height: 6)
                Text("本地服务 :8765")
                    .font(.caption)
            }
            HStack {
                Circle().fill(.green).frame(width: 6, height: 6)
                Text("CNSH网关 :9622")
                    .font(.caption)
            }
            HStack {
                Circle().fill(.green).frame(width: 6, height: 6)
                Text("Ollama :11434")
                    .font(.caption)
            }

            Divider()

            // 身份
            Text("UID9622 · 龍芯北辰")
                .font(.caption2)
                .foregroundStyle(.secondary)

            Button("退出宝宝") {
                NSApplication.shared.terminate(nil)
            }
        }
        .padding(12)
        .frame(width: 240)
    }
}

#Preview {
    BaoBaoMenuView()
}
