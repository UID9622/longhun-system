// LongHunWidgetEntryView.swift
// Widget UI视图
//
// DNA追溯码: #龍芯⚡️2026-03-09-WIDGET-VIEW
// 创建者: 诸葛鑫 (UID9622)
// 理论指导: 曾仕强老师（永恒显示）

import WidgetKit
import SwiftUI

struct LongHunWidgetEntryView: View {
    var entry: Provider.Entry
    @Environment(\.widgetFamily) var family
    
    var body: some View {
        switch family {
        case .systemSmall:
            SmallWidgetView(entry: entry)
        case .systemMedium:
            MediumWidgetView(entry: entry)
        case .systemLarge:
            LargeWidgetView(entry: entry)
        default:
            MediumWidgetView(entry: entry)
        }
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 小尺寸Widget
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
struct SmallWidgetView: View {
    let entry: Provider.Entry
    
    var body: some View {
        ZStack {
            // 背景渐变（龍魂配色）
            LinearGradient(
                colors: [Color(#colorLiteral(red: 0.05, green: 0.1, blue: 0.2, alpha: 1)),
                        Color(#colorLiteral(red: 0.1, green: 0.15, blue: 0.3, alpha: 1))],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            
            VStack(alignment: .leading, spacing: 4) {
                // 时间
                Text(entry.timeString)
                    .font(.system(size: 32, weight: .bold, design: .rounded))
                    .foregroundColor(.white)
                
                // 日期
                Text(entry.dateString.prefix(10))
                    .font(.system(size: 11))
                    .foregroundColor(.white.opacity(0.8))
                
                Spacer().frame(height: 8)
                
                // 农历
                HStack(spacing: 4) {
                    Image(systemName: "moon.stars.fill")
                        .font(.system(size: 10))
                        .foregroundColor(.yellow)
                    Text(entry.lunarMonthDay)
                        .font(.system(size: 11, weight: .medium))
                        .foregroundColor(.yellow)
                }
                
                // 节气
                HStack(spacing: 4) {
                    Image(systemName: "leaf.fill")
                        .font(.system(size: 10))
                        .foregroundColor(.green)
                    Text(entry.solarTerm)
                        .font(.system(size: 11, weight: .medium))
                        .foregroundColor(.green)
                }
                
                // 五行
                HStack(spacing: 4) {
                    Image(systemName: "sparkles")
                        .font(.system(size: 10))
                        .foregroundColor(.orange)
                    Text(entry.wuxing + "行")
                        .font(.system(size: 11, weight: .medium))
                        .foregroundColor(.orange)
                }
            }
            .padding()
        }
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 中尺寸Widget
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
struct MediumWidgetView: View {
    let entry: Provider.Entry
    
    var body: some View {
        ZStack {
            // 背景渐变
            LinearGradient(
                colors: [Color(#colorLiteral(red: 0.05, green: 0.1, blue: 0.2, alpha: 1)),
                        Color(#colorLiteral(red: 0.1, green: 0.15, blue: 0.3, alpha: 1))],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            
            HStack(spacing: 16) {
                // 左侧：时间与农历
                VStack(alignment: .leading, spacing: 6) {
                    // 时间
                    Text(entry.timeString)
                        .font(.system(size: 36, weight: .bold, design: .rounded))
                        .foregroundColor(.white)
                    
                    // 日期
                    Text(entry.dateString)
                        .font(.system(size: 12))
                        .foregroundColor(.white.opacity(0.8))
                    
                    Divider()
                        .background(Color.white.opacity(0.3))
                    
                    // 农历完整
                    VStack(alignment: .leading, spacing: 4) {
                        HStack(spacing: 4) {
                            Image(systemName: "moon.stars.fill")
                                .font(.system(size: 11))
                                .foregroundColor(.yellow)
                            Text(entry.lunarYear)
                                .font(.system(size: 11, weight: .medium))
                                .foregroundColor(.yellow)
                        }
                        
                        HStack(spacing: 4) {
                            Image(systemName: "calendar")
                                .font(.system(size: 11))
                                .foregroundColor(.yellow.opacity(0.8))
                            Text(entry.lunarMonthDay)
                                .font(.system(size: 11))
                                .foregroundColor(.yellow.opacity(0.8))
                        }
                    }
                }
                .frame(maxWidth: .infinity, alignment: .leading)
                
                // 右侧：节气与语录
                VStack(alignment: .leading, spacing: 8) {
                    // 节气标签
                    HStack(spacing: 6) {
                        Image(systemName: "leaf.fill")
                            .font(.system(size: 12))
                            .foregroundColor(.green)
                        Text(entry.solarTerm)
                            .font(.system(size: 13, weight: .semibold))
                            .foregroundColor(.green)
                        
                        Spacer()
                        
                        Image(systemName: "sparkles")
                            .font(.system(size: 12))
                            .foregroundColor(.orange)
                        Text(entry.wuxing)
                            .font(.system(size: 13, weight: .semibold))
                            .foregroundColor(.orange)
                    }
                    
                    Divider()
                        .background(Color.white.opacity(0.3))
                    
                    // 文子语录
                    Text(entry.quote)
                        .font(.system(size: 11, weight: .regular))
                        .foregroundColor(.white.opacity(0.9))
                        .lineLimit(3)
                        .multilineTextAlignment(.leading)
                    
                    Spacer()
                    
                    // DNA标识
                    Text("龍魂系统 · UID9622")
                        .font(.system(size: 8))
                        .foregroundColor(.white.opacity(0.4))
                }
                .frame(maxWidth: .infinity, alignment: .leading)
            }
            .padding()
        }
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 大尺寸Widget
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
struct LargeWidgetView: View {
    let entry: Provider.Entry
    
    var body: some View {
        ZStack {
            // 背景渐变
            LinearGradient(
                colors: [Color(#colorLiteral(red: 0.05, green: 0.1, blue: 0.2, alpha: 1)),
                        Color(#colorLiteral(red: 0.1, green: 0.15, blue: 0.3, alpha: 1))],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            
            VStack(alignment: .leading, spacing: 12) {
                // 顶部：时间
                HStack(alignment: .firstTextBaseline) {
                    Text(entry.timeString)
                        .font(.system(size: 48, weight: .bold, design: .rounded))
                        .foregroundColor(.white)
                    
                    Spacer()
                    
                    VStack(alignment: .trailing, spacing: 2) {
                        Text("龍魂万年历")
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(.yellow)
                        Text("UID9622")
                            .font(.system(size: 10))
                            .foregroundColor(.yellow.opacity(0.7))
                    }
                }
                
                // 日期
                Text(entry.dateString)
                    .font(.system(size: 14))
                    .foregroundColor(.white.opacity(0.8))
                
                Divider()
                    .background(Color.white.opacity(0.3))
                
                // 农历信息卡片
                VStack(alignment: .leading, spacing: 8) {
                    Text("农历信息")
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundColor(.white.opacity(0.6))
                    
                    HStack(spacing: 16) {
                        VStack(alignment: .leading, spacing: 4) {
                            HStack(spacing: 4) {
                                Image(systemName: "moon.stars.fill")
                                    .font(.system(size: 12))
                                    .foregroundColor(.yellow)
                                Text("农历年")
                                    .font(.system(size: 11))
                                    .foregroundColor(.white.opacity(0.7))
                            }
                            Text(entry.lunarYear)
                                .font(.system(size: 14, weight: .medium))
                                .foregroundColor(.yellow)
                        }
                        
                        VStack(alignment: .leading, spacing: 4) {
                            HStack(spacing: 4) {
                                Image(systemName: "calendar")
                                    .font(.system(size: 12))
                                    .foregroundColor(.yellow.opacity(0.8))
                                Text("农历日")
                                    .font(.system(size: 11))
                                    .foregroundColor(.white.opacity(0.7))
                            }
                            Text(entry.lunarMonthDay)
                                .font(.system(size: 14, weight: .medium))
                                .foregroundColor(.yellow.opacity(0.8))
                        }
                    }
                }
                .padding()
                .background(Color.white.opacity(0.05))
                .cornerRadius(10)
                
                // 节气与五行卡片
                HStack(spacing: 12) {
                    // 节气
                    VStack(alignment: .leading, spacing: 6) {
                        HStack(spacing: 4) {
                            Image(systemName: "leaf.fill")
                                .font(.system(size: 12))
                                .foregroundColor(.green)
                            Text("节气")
                                .font(.system(size: 11))
                                .foregroundColor(.white.opacity(0.7))
                        }
                        Text(entry.solarTerm)
                            .font(.system(size: 16, weight: .semibold))
                            .foregroundColor(.green)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(Color.white.opacity(0.05))
                    .cornerRadius(10)
                    
                    // 五行
                    VStack(alignment: .leading, spacing: 6) {
                        HStack(spacing: 4) {
                            Image(systemName: "sparkles")
                                .font(.system(size: 12))
                                .foregroundColor(.orange)
                            Text("五行")
                                .font(.system(size: 11))
                                .foregroundColor(.white.opacity(0.7))
                        }
                        Text(entry.wuxing + "行")
                            .font(.system(size: 16, weight: .semibold))
                            .foregroundColor(.orange)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(Color.white.opacity(0.05))
                    .cornerRadius(10)
                }
                
                Divider()
                    .background(Color.white.opacity(0.3))
                
                // 文子语录卡片
                VStack(alignment: .leading, spacing: 8) {
                    HStack(spacing: 4) {
                        Image(systemName: "quote.bubble.fill")
                            .font(.system(size: 12))
                            .foregroundColor(.blue)
                        Text("文子引擎")
                            .font(.system(size: 12, weight: .semibold))
                            .foregroundColor(.white.opacity(0.6))
                    }
                    
                    Text(entry.quote)
                        .font(.system(size: 13, weight: .regular))
                        .foregroundColor(.white.opacity(0.9))
                        .lineLimit(4)
                        .multilineTextAlignment(.leading)
                }
                .padding()
                .background(Color.white.opacity(0.05))
                .cornerRadius(10)
                
                Spacer()
                
                // 底部DNA追溯码
                Text(entry.dnaTrace)
                    .font(.system(size: 8, design: .monospaced))
                    .foregroundColor(.white.opacity(0.3))
            }
            .padding()
        }
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 预览
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
struct LongHunWidgetEntryView_Previews: PreviewProvider {
    static var previews: some View {
        let entry = SimpleEntry(
            date: Date(),
            timeString: "14:30",
            dateString: "2026年03月09日 星期一",
            lunarYear: "甲辰年（龍年）",
            lunarMonthDay: "二月初一",
            fullLunarDate: "甲辰年 二月初一",
            solarTerm: "惊蛰",
            wuxing: "木",
            quote: "持经达变，以不变应万变 —— 曾仕强",
            dnaTrace: "#龍芯⚡️2026-03-09-1430-WIDGET-UID9622"
        )
        
        Group {
            LongHunWidgetEntryView(entry: entry)
                .previewContext(WidgetPreviewContext(family: .systemSmall))
                .previewDisplayName("小尺寸")
            
            LongHunWidgetEntryView(entry: entry)
                .previewContext(WidgetPreviewContext(family: .systemMedium))
                .previewDisplayName("中尺寸")
            
            LongHunWidgetEntryView(entry: entry)
                .previewContext(WidgetPreviewContext(family: .systemLarge))
                .previewDisplayName("大尺寸")
        }
    }
}
