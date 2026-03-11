// LongHunWidget.swift
// 龍魂·iOS Widget v1.0
// DNA: #龍芯⚡️2026-03-07-IOS-WIDGET-☰乾-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
//
// Small  (169×169 pt): 卦象 + 人格 + 审计分 + 农历
// Medium (360×169 pt): 左=卦象区 / 右=系统数据 + 审计进度条

import WidgetKit
import SwiftUI

// MARK: - Color Palette

extension Color {
    static let chinaRed  = Color(red: 215/255, green: 19/255,  blue: 19/255)
    static let deepRed   = Color(red: 140/255, green: 8/255,   blue: 8/255)
    static let gold      = Color(red: 255/255, green: 215/255, blue: 0/255)
    static let softGold  = Color(red: 255/255, green: 238/255, blue: 130/255)
    static let inkWhite  = Color.white.opacity(0.92)
    static let dimWhite  = Color.white.opacity(0.55)
}

// MARK: - Audit Color

private func auditAccent(_ colorStr: String) -> Color {
    switch colorStr {
    case "Green":  return Color(red: 0.15, green: 0.90, blue: 0.40)
    case "Yellow": return Color(red: 1.00, green: 0.85, blue: 0.00)
    default:       return Color(red: 1.00, green: 0.25, blue: 0.20)
    }
}

// MARK: - Small Widget

struct SmallView: View {
    let entry: LongHunEntry

    var body: some View {
        ZStack {
            background

            VStack(spacing: 0) {
                Spacer(minLength: 6)

                // 卦象符号
                Text(entry.status.yuanzi.guaSymbol)
                    .font(.system(size: 42, weight: .regular))
                    .foregroundColor(.gold)

                // 卦名·维度
                Text(entry.status.yuanzi.display)
                    .font(.system(size: 11, weight: .semibold))
                    .foregroundColor(.softGold)
                    .padding(.top, 1)

                Spacer()

                // 人格
                Text(entry.status.yuanzi.personaName)
                    .font(.system(size: 10, weight: .medium))
                    .foregroundColor(.inkWhite)
                    .lineLimit(1)
                    .padding(.bottom, 4)

                // 审计分徽章
                auditBadge

                Spacer()

                // 农历
                Text(entry.lunarDate)
                    .font(.system(size: 9))
                    .foregroundColor(.dimWhite)
                    .padding(.bottom, 8)
            }
            .padding(.horizontal, 10)
        }
    }

    private var auditBadge: some View {
        HStack(spacing: 4) {
            Circle()
                .fill(auditAccent(entry.status.audit.color))
                .frame(width: 7, height: 7)
            Text("\(entry.status.audit.score)")
                .font(.system(size: 13, weight: .bold, design: .monospaced))
                .foregroundColor(.white)
            Text("/100")
                .font(.system(size: 9))
                .foregroundColor(.dimWhite)
        }
    }

    private var background: some View {
        LinearGradient(
            colors: [.chinaRed, .deepRed],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
        .ignoresSafeArea()
    }
}

// MARK: - Medium Widget

struct MediumView: View {
    let entry: LongHunEntry

    var body: some View {
        ZStack {
            background

            HStack(spacing: 0) {
                leftPanel
                divider
                rightPanel
            }
        }
    }

    // 左侧：卦象 + 人格
    private var leftPanel: some View {
        VStack(spacing: 5) {
            Text(entry.status.yuanzi.guaSymbol)
                .font(.system(size: 50, weight: .regular))
                .foregroundColor(.gold)

            Text(entry.status.yuanzi.guaName)
                .font(.system(size: 13, weight: .bold))
                .foregroundColor(.softGold)

            Text(entry.status.yuanzi.personaName)
                .font(.system(size: 10))
                .foregroundColor(.inkWhite)
                .lineLimit(1)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 14)
    }

    private var divider: some View {
        Rectangle()
            .fill(Color.white.opacity(0.18))
            .frame(width: 1)
            .padding(.vertical, 18)
    }

    // 右侧：审计 + 进度条 + 系统数据
    private var rightPanel: some View {
        VStack(alignment: .leading, spacing: 7) {

            // 审计标签
            HStack(spacing: 5) {
                Circle()
                    .fill(auditAccent(entry.status.audit.color))
                    .frame(width: 8, height: 8)
                Text(entry.status.audit.label)
                    .font(.system(size: 11, weight: .semibold))
                    .foregroundColor(.inkWhite)
            }

            // 审计进度条
            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    RoundedRectangle(cornerRadius: 3)
                        .fill(Color.white.opacity(0.18))
                        .frame(height: 6)
                    RoundedRectangle(cornerRadius: 3)
                        .fill(auditAccent(entry.status.audit.color))
                        .frame(
                            width: geo.size.width * CGFloat(entry.status.audit.score) / 100,
                            height: 6
                        )
                        .animation(.easeOut(duration: 0.4), value: entry.status.audit.score)
                }
            }
            .frame(height: 6)

            // 数据行
            HStack(spacing: 10) {
                statItem(label: "记忆", value: "\(entry.status.system.memoryCount)")
                statItem(label: "知识", value: "\(entry.status.system.knowledgeNodes)")
                statItem(label: "技能", value: "\(entry.status.system.skillDomains)")
            }

            // Ollama 状态
            HStack(spacing: 5) {
                Circle()
                    .fill(entry.status.system.ollamaOnline
                          ? Color(red: 0.2, green: 0.9, blue: 0.4)
                          : Color.red.opacity(0.75))
                    .frame(width: 6, height: 6)
                Text(entry.status.system.ollamaOnline
                     ? "Ollama · \(entry.status.system.ollamaModels) 个模型"
                     : "Ollama · 离线")
                    .font(.system(size: 10))
                    .foregroundColor(.inkWhite)
            }

            // 农历
            Text(entry.lunarDate)
                .font(.system(size: 9))
                .foregroundColor(.dimWhite)
        }
        .padding(.leading, 14)
        .padding(.trailing, 12)
        .padding(.vertical, 14)
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    @ViewBuilder
    private func statItem(label: String, value: String) -> some View {
        VStack(spacing: 1) {
            Text(value)
                .font(.system(size: 13, weight: .bold, design: .monospaced))
                .foregroundColor(.white)
            Text(label)
                .font(.system(size: 8))
                .foregroundColor(.dimWhite)
        }
    }

    private var background: some View {
        LinearGradient(
            colors: [.chinaRed, .deepRed],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
        .ignoresSafeArea()
    }
}

// MARK: - Entry View (dispatcher)

struct LongHunWidgetEntryView: View {
    @Environment(\.widgetFamily) private var family
    let entry: LongHunEntry

    var body: some View {
        Group {
            switch family {
            case .systemMedium:
                MediumView(entry: entry)
            default:
                SmallView(entry: entry)
            }
        }
        .widgetURL(URL(string: "cnsh://open"))
    }
}

// MARK: - Widget Configuration

@main
struct LongHunWidget: Widget {
    let kind = "LongHunWidget"

    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            LongHunWidgetEntryView(entry: entry)
        }
        .configurationDisplayName("龍魂")
        .description("龍魂元字引擎 · 北辰守护")
        .supportedFamilies([.systemSmall, .systemMedium])
        .contentMarginsDisabled()      // iOS 17+: 去除系统默认内边距，让背景满铺
    }
}

// MARK: - Previews

#Preview("Small", as: .systemSmall) {
    LongHunWidget()
} timeline: {
    LongHunEntry(
        date: .now,
        status: YuanziParser.placeholder(),
        lunarDate: LunarCalendar.todayShort()
    )
}

#Preview("Medium", as: .systemMedium) {
    LongHunWidget()
} timeline: {
    LongHunEntry(
        date: .now,
        status: YuanziParser.placeholder(),
        lunarDate: LunarCalendar.todayShort()
    )
}
