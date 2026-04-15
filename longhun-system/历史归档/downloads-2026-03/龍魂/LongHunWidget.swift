// LongHunWidget.swift
// 龍魂Widget主文件
//
// DNA追溯码: #龍芯⚡️2026-03-09-WIDGET-MAIN
// 创建者: 诸葛鑫 (UID9622)
// 理论指导: 曾仕强老师（永恒显示）

import WidgetKit
import SwiftUI

struct LongHunWidget: Widget {
    // Widget唯一标识符（非常重要！）
    let kind: String = "LongHunWidget"
    
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: Provider()) { entry in
            LongHunWidgetEntryView(entry: entry)
        }
        .configurationDisplayName("龍魂万年历")
        .description("融合农历、节气、五行与中华智慧的桌面小组件")
        .supportedFamilies([.systemSmall, .systemMedium, .systemLarge])
    }
}

// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 预览
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
struct LongHunWidget_Previews: PreviewProvider {
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
        
        LongHunWidgetEntryView(entry: entry)
            .previewContext(WidgetPreviewContext(family: .systemMedium))
    }
}
