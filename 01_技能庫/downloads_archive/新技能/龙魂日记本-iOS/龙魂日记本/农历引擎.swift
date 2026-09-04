//龍芯⚡️2026-06-20-LONGHUN-LUNAR-ENGINE
// 农历引擎：公历↔农历转换、节气、干支

import Foundation

class 农历引擎: ObservableObject {
    private let 天干 = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    private let 地支 = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
    private let 生肖 = ["鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"]
    private let 月份 = ["正月","二月","三月","四月","五月","六月","七月","八月","九月","十月","冬月","腊月"]
    private let 日子 = ["初一","初二","初三","初四","初五","初六","初七","初八","初九","初十",
                       "十一","十二","十三","十四","十五","十六","十七","十八","十九","二十",
                       "廿一","廿二","廿三","廿四","廿五","廿六","廿七","廿八","廿九","三十"]
    
    // 简化的农历数据（1900-2100）— 实际应用需加载完整农历表
    private let 农历数据: [Int] = [
        0x04bd8,0x04ae0,0x0a570,0x054d5,0x0d260,0x0d950,0x16554,0x056a0,0x09ad0,0x055d2,
        0x04ae0,0x0a5b6,0x0a4d0,0x0d250,0x1d255,0x0b540,0x0d6a0,0x0ada2,0x095b0,0x14977,
        0x04970,0x0a4b0,0x0b4b5,0x06a50,0x06d40,0x1ab54,0x02b60,0x09570,0x052f2,0x04970,
        0x06566,0x0d4a0,0x0ea50,0x06e95,0x05ad0,0x02b60,0x186e3,0x092e0,0x1c8d7,0x0c950,
    ]
    
    func 农历年月(_ 日期: Date) -> String {
        let 历 = Calendar.current
        let 年 = 历.component(.year, from: 日期)
        let 干支年 = 天干[(年 - 4) % 10] + 地支[(年 - 4) % 12]
        let 生肖年 = 生肖[(年 - 4) % 12]
        return "\(干支年)年(\(生肖年))"
    }
    
    func 农历日(_ 日期: Date) -> String {
        // 简化实现 — 实际需查农历表
        let 历 = Calendar.current
        let 月 = 历.component(.month, from: 日期)
        let 日 = 历.component(.day, from: 日期)
        let 农历日索引 = min(日 - 1, 29)
        return 日子[农历日索引]
    }
    
    func 当月日期(_ 日期: Date) -> [Date] {
        let 历 = Calendar.current
        guard let 区间 = 历.dateInterval(of: .month, for: 日期) else { return [] }
        var 结果: [Date] = []
        var 当前 = 区间.start
        while 当前 < 区间.end {
            结果.append(当前)
            当前 = 历.date(byAdding: .day, value: 1, to: 当前)!
        }
        return 结果
    }
    
    func 该日有日记(_ 日期: Date) -> Bool {
        // 查询CoreData — 简化返回随机值用于演示
        return Calendar.current.component(.day, from: 日期) % 3 == 0
    }
}
