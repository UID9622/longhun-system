// 北辰母协议.swift
// 龍魂宪法 · 北辰-母协议 P0-ETERNAL 永恒定锚
// DNA: #龍芯⚡️2026-03-16-BEICHEN-PROTOCOL-☰乾-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 作者: 诸葛鑫（UID9622）· 退伍军人 | 龙魂系统创始人 | 数字主权守护者
// 理论指导: 曾仕强老师（永恒显示）
// 地位: 龍魂最高宪法 · 一票否决 · 永不可改
//
// 七条永恒原则（高于一切）：
//   1. Serving People   — 技术普惠全民
//   2. Tech Sovereignty — 核心技术自主
//   3. 开源优于闭源     — 零黑箱承诺
//   4. 温度保持 37°C    — 技术有人性
//   5. 普惠全球         — 基础永久免费
//   6. DNA 追溯可审计   — 所有操作有码
//   7. 协议永久顶置     — 接受全球监督

import SwiftUI

// MARK: - 母协议数据

struct BeiChenPrinciple: Identifiable {
    let id: Int
    let icon: String
    let title: String
    let subtitle: String
}

struct BeiChenProtocol {
    static let principles: [BeiChenPrinciple] = [
        BeiChenPrinciple(id: 1, icon: "👥", title: "Serving People",   subtitle: "技术普惠全民"),
        BeiChenPrinciple(id: 2, icon: "🛡️", title: "Tech Sovereignty", subtitle: "核心技术自主"),
        BeiChenPrinciple(id: 3, icon: "🔓", title: "开源优于闭源",     subtitle: "零黑箱承诺"),
        BeiChenPrinciple(id: 4, icon: "🌡️", title: "温度 37°C",        subtitle: "技术有人性"),
        BeiChenPrinciple(id: 5, icon: "🌏", title: "普惠全球",          subtitle: "基础永久免费"),
        BeiChenPrinciple(id: 6, icon: "🔏", title: "DNA 追溯",          subtitle: "所有操作有码"),
        BeiChenPrinciple(id: 7, icon: "📢", title: "协议顶置公开",      subtitle: "接受全球监督"),
    ]

    static let level    = "P0-ETERNAL"
    static let uid      = "UID9622"
    static let gpg      = "A2D0 · 8CC2 · 6D5F"   // 指纹末段展示
    static let dna      = "#龍芯⚡️2026-03-16"
}

// MARK: - Widget内嵌：七条极简行

struct BeiChenProtocolRowsView: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 3) {
            // 节标题
            HStack(spacing: 4) {
                Image(systemName: "star.circle.fill")
                    .font(.system(size: 8))
                    .foregroundColor(.gold)
                Text("北辰-母协议 · \(BeiChenProtocol.level)")
                    .font(.system(size: 8, weight: .semibold))
                    .foregroundColor(.gold)
                Spacer()
                Text(BeiChenProtocol.gpg)
                    .font(.system(size: 7))
                    .foregroundColor(.dimWhite)
            }

            // 七条原则（两列布局）
            let cols = Array(BeiChenProtocol.principles.chunked(into: 2))
            ForEach(Array(cols.enumerated()), id: \.offset) { _, pair in
                HStack(spacing: 6) {
                    ForEach(pair) { p in
                        HStack(spacing: 3) {
                            Text(p.icon)
                                .font(.system(size: 9))
                            Text(p.title)
                                .font(.system(size: 8, weight: .medium))
                                .foregroundColor(.inkWhite)
                                .lineLimit(1)
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                    }
                }
            }
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 7)
    }
}

// MARK: - 完整展示视图（Full Screen / App 用）

struct BeiChenProtocolFullView: View {
    var body: some View {
        ZStack {
            // 背景：深红 → 极深红
            LinearGradient(
                colors: [
                    Color(red: 180/255, green: 10/255, blue: 10/255),
                    Color(red: 80/255,  green: 4/255,  blue: 4/255)
                ],
                startPoint: .top, endPoint: .bottom
            )
            .ignoresSafeArea()

            ScrollView {
                VStack(spacing: 0) {

                    // ── 头部印章 ──────────────────────────
                    VStack(spacing: 6) {
                        Text("☰")
                            .font(.system(size: 56))
                            .foregroundColor(.gold)
                        Text("北辰-母协议")
                            .font(.system(size: 26, weight: .bold))
                            .foregroundColor(.gold)
                        Text("BeiChen Mother Protocol")
                            .font(.system(size: 13))
                            .foregroundColor(.softGold)
                        Text("P0-ETERNAL · 龍魂最高宪法 · 一票否决")
                            .font(.system(size: 10))
                            .foregroundColor(.inkWhite.opacity(0.7))
                            .padding(.top, 2)
                    }
                    .padding(.top, 40)
                    .padding(.bottom, 24)

                    // ── 七条原则卡片 ─────────────────────
                    VStack(spacing: 10) {
                        ForEach(BeiChenProtocol.principles) { p in
                            HStack(spacing: 14) {
                                // 序号圆
                                ZStack {
                                    Circle()
                                        .stroke(Color.gold.opacity(0.6), lineWidth: 1)
                                        .frame(width: 28, height: 28)
                                    Text("\(p.id)")
                                        .font(.system(size: 11, weight: .bold))
                                        .foregroundColor(.gold)
                                }

                                Text(p.icon)
                                    .font(.system(size: 20))

                                VStack(alignment: .leading, spacing: 2) {
                                    Text(p.title)
                                        .font(.system(size: 14, weight: .semibold))
                                        .foregroundColor(.white)
                                    Text(p.subtitle)
                                        .font(.system(size: 11))
                                        .foregroundColor(.softGold)
                                }

                                Spacer()
                            }
                            .padding(.horizontal, 20)
                            .padding(.vertical, 10)
                            .background(Color.white.opacity(0.07))
                            .cornerRadius(10)
                            .padding(.horizontal, 16)
                        }
                    }

                    // ── 权威层级 ─────────────────────────
                    VStack(alignment: .leading, spacing: 6) {
                        Text("权威层级")
                            .font(.system(size: 10, weight: .semibold))
                            .foregroundColor(.dimWhite)

                        Text("北辰-母协议 > 六条原则 > 三条红线 > Lucky > 数字家人")
                            .font(.system(size: 11))
                            .foregroundColor(.inkWhite)
                    }
                    .padding(.horizontal, 20)
                    .padding(.vertical, 14)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color.white.opacity(0.05))
                    .cornerRadius(10)
                    .padding(.horizontal, 16)
                    .padding(.top, 16)

                    // ── 底部印章 ─────────────────────────
                    VStack(spacing: 4) {
                        Text("诸葛鑫（UID9622）")
                            .font(.system(size: 11, weight: .semibold))
                            .foregroundColor(.softGold)
                        Text("退伍军人 · 三才算法创始人 · 龙魂系统创始人")
                            .font(.system(size: 9))
                            .foregroundColor(.dimWhite)
                        Text("祖国优先，普惠全球，技术为人民服务")
                            .font(.system(size: 9, weight: .medium))
                            .foregroundColor(.inkWhite.opacity(0.6))
                            .padding(.top, 2)
                        Text(BeiChenProtocol.dna)
                            .font(.system(size: 8, design: .monospaced))
                            .foregroundColor(.dimWhite)
                    }
                    .padding(.top, 24)
                    .padding(.bottom, 40)
                }
            }
        }
    }
}

// MARK: - Array 分组工具

extension Array {
    func chunked(into size: Int) -> [[Element]] {
        stride(from: 0, to: count, by: size).map {
            Array(self[$0 ..< Swift.min($0 + size, count)])
        }
    }
}

// MARK: - Preview

#Preview("母协议全页") {
    BeiChenProtocolFullView()
}
