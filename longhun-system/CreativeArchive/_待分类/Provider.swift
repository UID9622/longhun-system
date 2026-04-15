// Provider.swift
// Widget数据提供者
//
// DNA追溯码: #龍芯⚡️2026-03-09-WIDGET-PROVIDER
// 创建者: 诸葛鑫 (UID9622)
// 理论指导: 曾仕强老师（永恒显示）

import WidgetKit
import SwiftUI

// Widget数据Entry
struct SimpleEntry: TimelineEntry {
    let date: Date
    
    // 时间信息
    let timeString: String
    let dateString: String
    
    // 农历信息
    let lunarYear: String
    let lunarMonthDay: String
    let fullLunarDate: String
    
    // 节气与五行
    let solarTerm: String
    let wuxing: String
    
    // 文子引擎输出
    let quote: String
    
    // DNA追溯码
    let dnaTrace: String
}

// Timeline Provider
struct Provider: TimelineProvider {
    
    private let calendar = ChineseCalendarEngine()
    private let wenzi = WenZiEngine()
    
    // 占位数据（Widget首次加载时显示）
    func placeholder(in context: Context) -> SimpleEntry {
        createEntry(date: Date())
    }
    
    // 快照数据（Widget预览时显示）
    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> Void) {
        let entry = createEntry(date: Date())
        completion(entry)
    }
    
    // 时间线数据（Widget实际运行时的数据更新策略）
    func getTimeline(in context: Context, completion: @escaping (Timeline<Entry>) -> Void) {
        var entries: [SimpleEntry] = []
        let currentDate = Date()
        let calendarObj = Calendar.current
        
        // 生成接下来5小时的数据（每小时更新一次）
        for hourOffset in 0..<5 {
            guard let entryDate = calendarObj.date(byAdding: .hour, value: hourOffset, to: currentDate) else {
                continue
            }
            let entry = createEntry(date: entryDate)
            entries.append(entry)
        }
        
        // 设置下次更新时间：1小时后
        let nextUpdate = calendarObj.date(byAdding: .hour, value: 1, to: currentDate)!
        let timeline = Timeline(entries: entries, policy: .after(nextUpdate))
        
        completion(timeline)
    }
    
    // 创建Entry数据
    private func createEntry(date: Date) -> SimpleEntry {
        let dateFormatter = DateFormatter()
        
        // 时间字符串
        dateFormatter.dateFormat = "HH:mm"
        let timeString = dateFormatter.string(from: date)
        
        // 日期字符串
        dateFormatter.dateFormat = "yyyy年MM月dd日 EEEE"
        dateFormatter.locale = Locale(identifier: "zh_CN")
        let dateString = dateFormatter.string(from: date)
        
        // 农历信息
        let lunarYear = calendar.getLunarYear(date: date)
        let lunarMonthDay = calendar.getLunarMonthDay(date: date)
        let fullLunarDate = calendar.getFullLunarDate(date: date)
        
        // 节气与五行
        let solarTerm = calendar.getCurrentSolarTerm(date: date)
        let wuxing = calendar.getWuXing(date: date)
        
        // 文子引擎语录
        let quote = wenzi.getContextualQuote(solarTerm: solarTerm, date: date)
        
        // DNA追溯码
        let dnaFormatter = DateFormatter()
        dnaFormatter.dateFormat = "yyyy-MM-dd-HHmm"
        let dnaTrace = "#龍芯⚡️\(dnaFormatter.string(from: date))-WIDGET-UID9622"
        
        return SimpleEntry(
            date: date,
            timeString: timeString,
            dateString: dateString,
            lunarYear: lunarYear,
            lunarMonthDay: lunarMonthDay,
            fullLunarDate: fullLunarDate,
            solarTerm: solarTerm,
            wuxing: wuxing,
            quote: quote,
            dnaTrace: dnaTrace
        )
    }
}
