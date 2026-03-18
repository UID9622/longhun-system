// LongHunTimeline.swift
// 龍魂·时间线提供者 v1.0
// DNA: #龍芯⚡️2026-03-07-IOS-TIMELINE-☴巽-v1.0

import WidgetKit
import SwiftUI

struct Provider: TimelineProvider {

    // MARK: - TimelineProvider

    func placeholder(in context: Context) -> LongHunEntry {
        LongHunEntry(
            date: Date(),
            status: YuanziParser.placeholder(),
            lunarDate: LunarCalendar.todayShort()
        )
    }

    func getSnapshot(in context: Context, completion: @escaping (LongHunEntry) -> Void) {
        let entry = LongHunEntry(
            date: Date(),
            status: context.isPreview ? YuanziParser.placeholder() : YuanziParser.load(),
            lunarDate: LunarCalendar.todayShort(),
            music: context.isPreview ? .placeholder : .current,
            xcode: context.isPreview ? .placeholder : .current
        )
        completion(entry)
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<LongHunEntry>) -> Void) {
        let status = YuanziParser.load()
        let lunar  = LunarCalendar.todayShort()
        let now    = Date()

        // 每 15 分钟刷新一次
        let nextUpdate = Calendar.current.date(byAdding: .minute, value: 15, to: now)!

        let entry = LongHunEntry(
            date: now,
            status: status,
            lunarDate: lunar,
            music: .current,
            xcode: .current
        )
        let timeline = Timeline(entries: [entry], policy: .after(nextUpdate))
        completion(timeline)
    }
}
