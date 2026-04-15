// ChineseCalendarEngine.swift
// 农历计算引擎（简化版）
//
// DNA追溯码: #龍芯⚡️2026-03-09-LUNAR-ENGINE
// 创建者: 诸葛鑫 (UID9622)
// 理论指导: 曾仕强老师（永恒显示）

import Foundation

class ChineseCalendarEngine {
    
    // 天干
    private let heavenlyStems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    
    // 地支
    private let earthlyBranches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    // 生肖
    private let zodiacAnimals = ["鼠", "牛", "虎", "兔", "龍", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
    
    // 农历月份
    private let lunarMonths = ["正月", "二月", "三月", "四月", "五月", "六月",
                               "七月", "八月", "九月", "十月", "冬月", "腊月"]
    
    // 农历日期
    private let lunarDays = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                             "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                             "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
    
    // 二十四节气
    private let solarTerms = [
        "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
        "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
        "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
        "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
    ]
    
    // 获取农历年份（天干地支+生肖）
    func getLunarYear(date: Date = Date()) -> String {
        let calendar = Calendar.current
        let year = calendar.component(.year, from: date)
        
        // 简化计算：以1984年（甲子年）为基准
        let baseYear = 1984
        let offset = year - baseYear
        
        let stemIndex = offset % 10
        let branchIndex = offset % 12
        let zodiacIndex = offset % 12
        
        let stem = heavenlyStems[stemIndex]
        let branch = earthlyBranches[branchIndex]
        let zodiac = zodiacAnimals[zodiacIndex]
        
        return "\(stem)\(branch)年（\(zodiac)年）"
    }
    
    // 获取农历月日（简化版，实际需要查表）
    func getLunarMonthDay(date: Date = Date()) -> String {
        let calendar = Calendar.current
        let month = calendar.component(.month, from: date)
        let day = calendar.component(.day, from: date)
        
        // 简化：直接用公历近似
        // 实际应该用完整的农历转换算法
        let lunarMonth = lunarMonths[min(month - 1, 11)]
        let lunarDay = lunarDays[min(day - 1, 29)]
        
        return "\(lunarMonth)\(lunarDay)"
    }
    
    // 获取完整农历日期
    func getFullLunarDate(date: Date = Date()) -> String {
        let year = getLunarYear(date: date)
        let monthDay = getLunarMonthDay(date: date)
        return "\(year) \(monthDay)"
    }
    
    // 获取当前节气（简化版）
    func getCurrentSolarTerm(date: Date = Date()) -> String {
        let calendar = Calendar.current
        let month = calendar.component(.month, from: date)
        let day = calendar.component(.day, from: date)
        
        // 简化：每月两个节气，大约在6号和21号
        let termIndex = (month - 1) * 2 + (day >= 20 ? 1 : 0)
        return solarTerms[min(termIndex, 23)]
    }
    
    // 获取五行属性（根据年份）
    func getWuXing(date: Date = Date()) -> String {
        let calendar = Calendar.current
        let year = calendar.component(.year, from: date)
        let offset = (year - 1984) % 10
        
        let wuxing = ["金", "木", "水", "火", "土"]
        return wuxing[offset % 5]
    }
}
