// ═══════════════════════════════════════════════════════════
// 🐱 桌面宝宝 · 浮动窗口视图
// DNA: #龍芯⚡️2026-04-10-桌面宝宝-FloatView-v1.0
// ═══════════════════════════════════════════════════════════

import SwiftUI

/// 桌面浮动宝宝 · 主界面
struct BaoBaoFloatView: View {
    @StateObject private var brain = BaoBaoBrain()
    @State private var isDragging = false
    @State private var isListening = false

    var body: some View {
        ZStack {
            // 透明背景
            Color.clear

            VStack(spacing: 12) {
                // 宝宝形象
                baobaoAvatar

                // 状态文字
                statusText

                // 对话气泡
                if !brain.lastMessage.isEmpty {
                    chatBubble
                }

                // 操作按钮
                actionButtons
            }
            .padding(16)
        }
        .background(
            RoundedRectangle(cornerRadius: 20)
                .fill(.ultraThinMaterial)
                .opacity(isDragging ? 0.9 : 0.7)
        )
    }

    // MARK: - 宝宝形象

    private var baobaoAvatar: some View {
        ZStack {
            // 呼吸光圈
            Circle()
                .fill(
                    RadialGradient(
                        colors: [brain.moodColor.opacity(0.3), .clear],
                        center: .center,
                        startRadius: 30,
                        endRadius: 60
                    )
                )
                .frame(width: 120, height: 120)
                .scaleEffect(brain.isThinking ? 1.2 : 1.0)
                .animation(.easeInOut(duration: 1.5).repeatForever(), value: brain.isThinking)

            // 宝宝emoji
            Text(brain.currentEmoji)
                .font(.system(size: 60))
                .scaleEffect(isListening ? 1.1 : 1.0)
                .animation(.spring(response: 0.3), value: isListening)
        }
        .onTapGesture {
            brain.greet()
        }
    }

    // MARK: - 状态

    private var statusText: some View {
        HStack(spacing: 6) {
            Circle()
                .fill(brain.isThinking ? .orange : .green)
                .frame(width: 8, height: 8)

            Text(brain.statusText)
                .font(.system(size: 11, design: .rounded))
                .foregroundStyle(.secondary)
        }
    }

    // MARK: - 对话气泡

    private var chatBubble: some View {
        Text(brain.lastMessage)
            .font(.system(size: 13, design: .rounded))
            .padding(.horizontal, 12)
            .padding(.vertical, 8)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .fill(Color.accentColor.opacity(0.1))
            )
            .lineLimit(3)
    }

    // MARK: - 按钮

    private var actionButtons: some View {
        HStack(spacing: 10) {
            // 语音按钮
            Button(action: { toggleListening() }) {
                Image(systemName: isListening ? "mic.fill" : "mic")
                    .font(.system(size: 16))
                    .foregroundStyle(isListening ? .red : .primary)
            }
            .buttonStyle(.plain)
            .help("语音输入")

            // 快捷操作
            Button(action: { brain.quickAction() }) {
                Image(systemName: "sparkles")
                    .font(.system(size: 16))
            }
            .buttonStyle(.plain)
            .help("快捷操作")

            // DNA状态
            Button(action: { brain.showDNA() }) {
                Image(systemName: "signature")
                    .font(.system(size: 16))
                    .foregroundStyle(.purple)
            }
            .buttonStyle(.plain)
            .help("DNA追溯")
        }
    }

    private func toggleListening() {
        isListening.toggle()
        if isListening {
            brain.startListening()
        } else {
            brain.stopListening()
        }
    }
}

#Preview {
    BaoBaoFloatView()
        .frame(width: 280, height: 360)
}
