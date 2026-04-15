// LongHunWidgetEntryView.swift
// Widget UI视图 - 献礼新中国成立77周年版
//
// DNA追溯码: #龍芯⚡️2026-03-09-WIDGET-VIEW-77TH
// 创建者: 诸葛鑫 (UID9622)
// 理论指导: 曾仕强老师（永恒显示）
// 献礼: 新中国成立77周年（1949-2026）

import WidgetKit
import SwiftUI

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 献礼配色方案 - 终极版（整合千问方案）
// 红为底，金为骨，白为魂
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
extension Color {
    // Hex颜色初始化（千问方案）
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default: (a, r, g, b) = (1, 1, 1, 0)
        }
        self.init(.sRGB, red: Double(r) / 255, green: Double(g) / 255, blue: Double(b) / 255, opacity: Double(a) / 255)
    }
    
    // 背景红：径向渐变（千问优化：模拟旗帜受光）
    static let redStart = Color(hex: "FF4D4D")  // 亮红（中心）
    static let redEnd = Color(hex: "8B0000")    // 深红（边缘）
    
    // 辉煌金：流光渐变（中和火马年的火气）
    static let goldStart = Color(hex: "FFFACD") // 亮金（柔光金）
    static let goldEnd = Color(hex: "DAA520")   // 暗金（古铜金）
    
    // 国旗红（传统版保留）
    static let celebrationRed = Color(hex: "DE2910")
    static let deepCelebrationRed = Color(hex: "8B0000")
    
    // 辉煌金（传统版保留）
    static let gloryGold = Color(hex: "FFD700")
    static let richGold = Color(hex: "F2B95A")
    
    // 纯洁白（略带透明，柔和不抢眼）
    static let pureWhite = Color.white.opacity(0.95)
}

struct LongHunWidgetEntryView: View {
    var entry: Provider.Entry
    @Environment(\.widgetFamily) var family
    
    var body: some View {
        switch family {
        case .systemSmall:
            SmallWidgetView_77th(entry: entry)
        case .systemMedium:
            MediumWidgetView_77th(entry: entry)
        case .systemLarge:
            LargeWidgetView_77th(entry: entry)
        default:
            MediumWidgetView_77th(entry: entry)
        }
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 小尺寸Widget - 献礼77周年+丙午马年版
// 整合千问方案：五星+马字+山河无恙
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
struct SmallWidgetView_77th: View {
    let entry: Provider.Entry
    
    var body: some View {
        ZStack {
            // 背景：径向渐变红（千问方案：模拟旗帜受光）
            RadialGradient(
                gradient: Gradient(colors: [.redStart, .redEnd]),
                center: .topLeading,
                startRadius: 50,
                endRadius: 150
            )
            
            VStack(alignment: .center, spacing: 6) {
                // 顶部：五星 + 马年标识（千问方案）
                HStack(spacing: 4) {
                    // 五颗星，象征国旗
                    ForEach(0..<5) { _ in
                        Image(systemName: "star.fill")
                            .font(.system(size: 6))
                            .foregroundStyle(
                                LinearGradient(
                                    gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                            .shadow(color: .black.opacity(0.3), radius: 0.5, x: 0.5, y: 0.5)
                    }
                    
                    Spacer()
                    
                    // 马年标识：书法"马"字（千问精华）
                    Text("马")
                        .font(.system(size: 10, weight: .bold, design: .serif))
                        .foregroundColor(.goldStart)
                        .opacity(0.9)
                }
                .padding(.horizontal, 4)
                .padding(.top, 2)
                
                // 核心：时间 + 77周年徽章
                VStack(spacing: 3) {
                    // 时间：大而清晰，白色为主
                    Text(entry.timeString)
                        .font(.system(size: 28, weight: .heavy, design: .rounded))
                        .foregroundColor(.pureWhite)
                        .shadow(color: .black.opacity(0.4), radius: 2, x: 1, y: 1)
                    
                    // 77周年：金色渐变徽章（千问方案）
                    HStack(spacing: 3) {
                        Text("建国")
                            .font(.system(size: 8, weight: .medium))
                            .foregroundColor(.pureWhite)
                        
                        Text("77")
                            .font(.system(size: 14, weight: .black, design: .serif))
                            .foregroundStyle(
                                LinearGradient(
                                    gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                    startPoint: .top,
                                    endPoint: .bottom
                                )
                            )
                            .shadow(color: .black.opacity(0.5), radius: 1, x: 1, y: 1)
                        
                        Text("周年")
                            .font(.system(size: 8, weight: .medium))
                            .foregroundColor(.pureWhite)
                    }
                    .padding(.horizontal, 6)
                    .padding(.vertical, 2)
                    .background(Color.black.opacity(0.1))
                    .cornerRadius(4)
                }
                
                // 金丝分隔线（千问方案）
                Divider()
                    .background(
                        LinearGradient(
                            gradient: Gradient(colors: [.goldStart, .goldEnd]),
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .padding(.horizontal, 10)
                    .opacity(0.8)
                
                // 底部：农历 + 献礼词
                VStack(spacing: 2) {
                    Text(entry.lunarMonthDay)
                        .font(.system(size: 9, weight: .regular))
                        .foregroundColor(.pureWhite)
                        .opacity(0.9)
                    
                    // 献礼词：山河无恙·国泰民安（千问精华）
                    Text("山河无恙·国泰民安")
                        .font(.system(size: 8, weight: .semibold))
                        .foregroundColor(.goldStart)
                        .lineLimit(1)
                        .shadow(color: .black.opacity(0.3), radius: 0.5, x: 0.5, y: 0.5)
                }
                
                Spacer()
                
                // UID敬献标识
                Text("UID9622 敬献")
                    .font(.system(size: 6))
                    .foregroundColor(.pureWhite.opacity(0.6))
            }
            .padding(6)
        }
        .cornerRadius(14)
        .shadow(color: Color.black.opacity(0.4), radius: 8, x: 0, y: 4)
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 中尺寸Widget - 献礼77周年+丙午马年版
// 整合千问方案：书法马字+山河无恙+流光金
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
struct MediumWidgetView_77th: View {
    let entry: Provider.Entry
    
    var body: some View {
        ZStack {
            // 背景：径向渐变红（千问方案）
            RadialGradient(
                gradient: Gradient(colors: [.redStart, .redEnd]),
                center: .topLeading,
                startRadius: 50,
                endRadius: 200
            )
            
            HStack(spacing: 10) {
                // 左侧：时间与国庆标识
                VStack(alignment: .center, spacing: 6) {
                    // 顶部：五星 + 马字（千问方案）
                    HStack(spacing: 4) {
                        ForEach(0..<5) { _ in
                            Image(systemName: "star.fill")
                                .font(.system(size: 7))
                                .foregroundStyle(
                                    LinearGradient(
                                        gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                        startPoint: .topLeading,
                                        endPoint: .bottomTrailing
                                    )
                                )
                                .shadow(color: .black.opacity(0.3), radius: 0.5, x: 0.5, y: 0.5)
                        }
                        
                        Spacer()
                        
                        // 书法"马"字
                        Text("马")
                            .font(.system(size: 11, weight: .bold, design: .serif))
                            .foregroundColor(.goldStart)
                            .opacity(0.9)
                    }
                    .padding(.horizontal, 4)
                    
                    // 时间
                    Text(entry.timeString)
                        .font(.system(size: 36, weight: .heavy, design: .rounded))
                        .foregroundColor(.pureWhite)
                        .shadow(color: .black.opacity(0.4), radius: 2, x: 1, y: 1)
                    
                    // 77周年徽章（千问流光金方案）
                    VStack(spacing: 2) {
                        Text("新中国成立")
                            .font(.system(size: 9, weight: .medium))
                            .foregroundColor(.pureWhite)
                            .opacity(0.9)
                        
                        HStack(spacing: 3) {
                            Text("建国")
                                .font(.system(size: 9, weight: .medium))
                                .foregroundColor(.pureWhite)
                            
                            Text("77")
                                .font(.system(size: 16, weight: .black, design: .serif))
                                .foregroundStyle(
                                    LinearGradient(
                                        gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                        startPoint: .top,
                                        endPoint: .bottom
                                    )
                                )
                                .shadow(color: .black.opacity(0.5), radius: 1, x: 1, y: 1)
                            
                            Text("周年")
                                .font(.system(size: 9, weight: .medium))
                                .foregroundColor(.pureWhite)
                        }
                    }
                    .padding(.vertical, 3)
                    .padding(.horizontal, 6)
                    .background(Color.black.opacity(0.1))
                    .cornerRadius(6)
                    
                    Spacer()
                }
                .frame(maxWidth: .infinity)
                
                // 金丝分隔线（千问方案）
                Divider()
                    .background(
                        LinearGradient(
                            gradient: Gradient(colors: [.goldStart, .goldEnd]),
                            startPoint: .top,
                            endPoint: .bottom
                        )
                    )
                    .opacity(0.8)
                
                // 右侧：农历与献礼语
                VStack(alignment: .leading, spacing: 6) {
                    // 日期
                    Text(entry.dateString)
                        .font(.system(size: 10, weight: .medium))
                        .foregroundColor(.pureWhite)
                        .opacity(0.9)
                    
                    // 农历
                    VStack(alignment: .leading, spacing: 2) {
                        HStack(spacing: 3) {
                            Image(systemName: "moon.stars.fill")
                                .font(.system(size: 9))
                                .foregroundColor(.goldStart)
                            Text(entry.lunarYear)
                                .font(.system(size: 9, weight: .medium))
                                .foregroundColor(.goldStart)
                        }
                        
                        HStack(spacing: 3) {
                            Text(entry.lunarMonthDay)
                                .font(.system(size: 11, weight: .semibold))
                                .foregroundColor(.goldEnd)
                            Text("·")
                                .foregroundColor(.pureWhite.opacity(0.5))
                            Text(entry.solarTerm)
                                .font(.system(size: 10))
                                .foregroundColor(.pureWhite.opacity(0.8))
                        }
                    }
                    
                    // 金丝分隔线
                    Divider()
                        .background(
                            LinearGradient(
                                gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                        .opacity(0.6)
                    
                    // 献礼语（千问精华：山河无恙·国泰民安）
                    VStack(alignment: .leading, spacing: 2) {
                        Text("山河无恙")
                            .font(.system(size: 11, weight: .semibold))
                            .foregroundColor(.goldStart)
                            .shadow(color: .black.opacity(0.3), radius: 0.5, x: 0.5, y: 0.5)
                        
                        Text("国泰民安")
                            .font(.system(size: 11, weight: .semibold))
                            .foregroundColor(.goldStart)
                            .shadow(color: .black.opacity(0.3), radius: 0.5, x: 0.5, y: 0.5)
                    }
                    
                    Spacer()
                    
                    // 献礼标识
                    HStack {
                        Spacer()
                        VStack(alignment: .trailing, spacing: 1) {
                            Text("UID9622 敬献")
                                .font(.system(size: 7, weight: .medium))
                                .foregroundColor(.pureWhite.opacity(0.7))
                            Text("丙午马年")
                                .font(.system(size: 6))
                                .foregroundColor(.goldEnd.opacity(0.8))
                        }
                    }
                }
                .frame(maxWidth: .infinity)
            }
            .padding()
        }
        .cornerRadius(14)
        .shadow(color: Color.black.opacity(0.4), radius: 10, x: 0, y: 5)
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 大尺寸Widget - 献礼77周年终极版
// 整合千问方案：庄重·辉煌·零失误
// 红为底，金为骨，白为魂
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
struct LargeWidgetView_77th: View {
    let entry: Provider.Entry
    
    var body: some View {
        ZStack {
            // 背景：径向渐变红（千问方案：模拟旗帜受光）
            RadialGradient(
                gradient: Gradient(colors: [.redStart, .redEnd]),
                center: .topLeading,
                startRadius: 100,
                endRadius: 300
            )
            
            VStack(alignment: .leading, spacing: 8) {
                // 顶部：五星标识 + 马年标识 + 标题
                HStack(alignment: .center) {
                    // 五星排列（千问方案）
                    HStack(spacing: 3) {
                        ForEach(0..<5) { _ in
                            Image(systemName: "star.fill")
                                .font(.system(size: 10))
                                .foregroundStyle(
                                    LinearGradient(
                                        gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                        startPoint: .topLeading,
                                        endPoint: .bottomTrailing
                                    )
                                )
                                .shadow(color: .black.opacity(0.3), radius: 0.5, x: 0.5, y: 0.5)
                        }
                    }
                    
                    // 书法"马"字（千问精华）
                    Text("马")
                        .font(.system(size: 14, weight: .bold, design: .serif))
                        .foregroundColor(.goldStart)
                        .opacity(0.9)
                        .padding(.leading, 4)
                    
                    Spacer()
                    
                    VStack(alignment: .trailing, spacing: 1) {
                        Text("龍魂万年历")
                            .font(.system(size: 13, weight: .bold))
                            .foregroundStyle(
                                LinearGradient(
                                    gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                        Text("献礼77周年·丙午马年")
                            .font(.system(size: 8, weight: .medium))
                            .foregroundColor(.goldEnd)
                    }
                }
                
                // 时间展示区（大字号）
                HStack(alignment: .firstTextBaseline, spacing: 10) {
                    Text(entry.timeString)
                        .font(.system(size: 52, weight: .heavy, design: .rounded))
                        .foregroundColor(.pureWhite)
                        .shadow(color: .black.opacity(0.4), radius: 3, x: 2, y: 2)
                    
                    // 77周年徽章（千问流光金方案）
                    VStack(alignment: .leading, spacing: 2) {
                        Text("新中国成立")
                            .font(.system(size: 11, weight: .medium))
                            .foregroundColor(.pureWhite)
                            .opacity(0.9)
                        
                        HStack(spacing: 3) {
                            Text("建国")
                                .font(.system(size: 10, weight: .medium))
                                .foregroundColor(.pureWhite)
                            
                            Text("77")
                                .font(.system(size: 22, weight: .black, design: .serif))
                                .foregroundStyle(
                                    LinearGradient(
                                        gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                        startPoint: .top,
                                        endPoint: .bottom
                                    )
                                )
                                .shadow(color: .black.opacity(0.5), radius: 1, x: 1, y: 1)
                            
                            Text("周年")
                                .font(.system(size: 10, weight: .medium))
                                .foregroundColor(.pureWhite)
                        }
                    }
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(Color.black.opacity(0.1))
                    .cornerRadius(6)
                }
                
                // 日期
                Text(entry.dateString)
                    .font(.system(size: 12, weight: .medium))
                    .foregroundColor(.pureWhite)
                    .opacity(0.9)
                
                // 金丝分隔线（千问方案）
                Divider()
                    .background(
                        LinearGradient(
                            gradient: Gradient(colors: [.goldStart, .goldEnd]),
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .opacity(0.8)
                
                // 农历信息卡片
                HStack(spacing: 10) {
                    VStack(alignment: .leading, spacing: 4) {
                        HStack(spacing: 3) {
                            Image(systemName: "moon.stars.fill")
                                .font(.system(size: 11))
                                .foregroundColor(.goldStart)
                            Text("农历年")
                                .font(.system(size: 10))
                                .foregroundColor(.pureWhite.opacity(0.8))
                        }
                        Text(entry.lunarYear)
                            .font(.system(size: 14, weight: .bold))
                            .foregroundStyle(
                                LinearGradient(
                                    gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(Color.black.opacity(0.1))
                    .cornerRadius(8)
                    
                    VStack(alignment: .leading, spacing: 4) {
                        HStack(spacing: 3) {
                            Image(systemName: "calendar")
                                .font(.system(size: 11))
                                .foregroundColor(.goldEnd)
                            Text("农历日")
                                .font(.system(size: 10))
                                .foregroundColor(.pureWhite.opacity(0.8))
                        }
                        Text(entry.lunarMonthDay)
                            .font(.system(size: 14, weight: .bold))
                            .foregroundColor(.goldEnd)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .padding()
                    .background(Color.black.opacity(0.1))
                    .cornerRadius(8)
                }
                
                // 节气卡片
                HStack(spacing: 3) {
                    Image(systemName: "leaf.fill")
                        .font(.system(size: 11))
                        .foregroundColor(.goldStart)
                    Text("节气")
                        .font(.system(size: 10))
                        .foregroundColor(.pureWhite.opacity(0.8))
                    Spacer()
                    Text(entry.solarTerm)
                        .font(.system(size: 15, weight: .semibold))
                        .foregroundStyle(
                            LinearGradient(
                                gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                        )
                }
                .padding()
                .background(Color.black.opacity(0.1))
                .cornerRadius(8)
                
                // 金丝分隔线
                Divider()
                    .background(
                        LinearGradient(
                            gradient: Gradient(colors: [.goldStart, .goldEnd]),
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .opacity(0.8)
                
                // 献礼语录卡片（千问精华：山河无恙·国泰民安）
                VStack(alignment: .leading, spacing: 6) {
                    HStack(spacing: 3) {
                        Image(systemName: "quote.bubble.fill")
                            .font(.system(size: 11))
                            .foregroundColor(.goldStart)
                        Text("献礼77周年·丙午马年")
                            .font(.system(size: 11, weight: .bold))
                            .foregroundStyle(
                                LinearGradient(
                                    gradient: Gradient(colors: [.goldStart, .goldEnd]),
                                    startPoint: .leading,
                                    endPoint: .trailing
                                )
                            )
                    }
                    
                    // 大气献礼词（千问方案）
                    VStack(alignment: .leading, spacing: 3) {
                        Text("山河无恙")
                            .font(.system(size: 15, weight: .bold))
                            .foregroundColor(.goldStart)
                            .shadow(color: .black.opacity(0.3), radius: 0.5, x: 0.5, y: 0.5)
                        
                        Text("国泰民安")
                            .font(.system(size: 15, weight: .bold))
                            .foregroundColor(.goldStart)
                            .shadow(color: .black.opacity(0.3), radius: 0.5, x: 0.5, y: 0.5)
                    }
                }
                .padding()
                .background(Color.black.opacity(0.15))
                .cornerRadius(8)
                
                Spacer()
                
                // 底部：DNA追溯码 + 献礼标识
                HStack {
                    Text(entry.dnaTrace)
                        .font(.system(size: 7, design: .monospaced))
                        .foregroundColor(.pureWhite.opacity(0.4))
                    
                    Spacer()
                    
                    VStack(alignment: .trailing, spacing: 1) {
                        Text("UID9622 敬献")
                            .font(.system(size: 8, weight: .medium))
                            .foregroundColor(.goldEnd)
                        Text("1949-2026 · 77载芳华")
                            .font(.system(size: 7))
                            .foregroundColor(.pureWhite.opacity(0.6))
                    }
                }
            }
            .padding()
        }
        .cornerRadius(16)
        .shadow(color: Color.black.opacity(0.4), radius: 12, x: 0, y: 6)
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
