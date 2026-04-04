// LunarCalendar.swift
// 龍魂·农历助手 v1.0
// DNA: #龍芯⚡️2026-03-07-IOS-LUNAR-☷坤-v1.0
// 利用 iOS 内建 Calendar(identifier: .chinese) 转换农历

import Foundation

struct LunarCalendar {

    // MARK: - 常量表

    private static let months = [
        "正月","二月","三月","四月","五月","六月",
        "七月","八月","九月","十月","冬月","腊月"
    ]

    private static let days = [
        "初一","初二","初三","初四","初五","初六","初七","初八","初九","初十",
        "十一","十二","十三","十四","十五","十六","十七","十八","十九","二十",
        "廿一","廿二","廿三","廿四","廿五","廿六","廿七","廿八","廿九","三十"
    ]

    private static let heavenlyStems  = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    private static let earthlyBranches = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
    private static let zodiacAnimals   = ["鼠","牛","虎","兔","龍","蛇","马","羊","猴","鸡","狗","猪"]

    // MARK: - 农历日期结构

    struct LunarDate {
        let year: Int
        let month: Int
        let day: Int
        let isLeapMonth: Bool

        var monthName: String {
            let idx = max(0, min(month - 1, 11))
            let prefix = isLeapMonth ? "闰" : ""
            return "\(prefix)\(LunarCalendar.months[idx])"
        }

        var dayName: String {
            let idx = max(0, min(day - 1, 29))
            return LunarCalendar.days[idx]
        }

        /// 天干
        var stem: String {
            let idx = ((year - 4) % 10 + 10) % 10
            return LunarCalendar.heavenlyStems[idx]
        }

        /// 地支
        var branch: String {
            let idx = ((year - 4) % 12 + 12) % 12
            return LunarCalendar.earthlyBranches[idx]
        }

        /// 生肖
        var zodiac: String {
            let idx = ((year - 4) % 12 + 12) % 12
            return LunarCalendar.zodiacAnimals[idx]
        }

        /// 简短: "正月初九"
        var shortDisplay: String { "\(monthName)\(dayName)" }

        /// 完整: "丙午年【马】正月初九"
        var fullDisplay: String { "\(stem)\(branch)年【\(zodiac)】\(monthName)\(dayName)" }
    }

    // MARK: - 转换

    static func convert(from date: Date = Date()) -> LunarDate {
        var cal = Calendar(identifier: .chinese)
        cal.locale = Locale(identifier: "zh_CN")
        let comps = cal.dateComponents([.year, .month, .day, .isLeapMonth], from: date)
        return LunarDate(
            year: comps.year ?? 2026,
            month: comps.month ?? 1,
            day: comps.day ?? 1,
            isLeapMonth: comps.isLeapMonth ?? false
        )
    }

    /// 今日简短农历 — "正月初九"
    static func todayShort() -> String { convert().shortDisplay }

    /// 今日完整农历 — "丙午年【马】正月初九"
    static func todayFull() -> String { convert().fullDisplay }
}
