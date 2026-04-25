// LongHunCalendar.swift
// 龍魂·万年历 v2.0 + LU-Time Engine v4.0
// DNA: #龍芯⚡️2026-03-14-CALENDAR-LUTIME-v2.0
// 创始人: 诸葛鑫（UID9622）
// 理论指导: 曾仕强老师（永恒显示）

import SwiftUI
import CryptoKit

// MARK: - 龍魂Logo视图

struct 龍魂Logo: View {
    var size: CGFloat = 120
    
    var body: some View {
        ZStack {
            // 外圆 - 金色边框
            Circle()
                .stroke(
                    LinearGradient(
                        colors: [
                            Color(red: 1, green: 0.84, blue: 0),
                            Color(red: 0.8, green: 0.6, blue: 0.2),
                            Color(red: 1, green: 0.84, blue: 0)
                        ],
                        startPoint: .topLeading,
                        endPoint: .bottomTrailing
                    ),
                    lineWidth: 3
                )
                .frame(width: size, height: size)
                .shadow(color: Color(red: 1, green: 0.84, blue: 0).opacity(0.3), radius: 10)
            
            // 内圆 - 暗红底
            Circle()
                .fill(
                    RadialGradient(
                        colors: [
                            Color(red: 0.3, green: 0.05, blue: 0.05),
                            Color(red: 0.15, green: 0.02, blue: 0.02)
                        ],
                        center: .center,
                        startRadius: 0,
                        endRadius: size / 2
                    )
                )
                .frame(width: size - 6, height: size - 6)
            
            // 龍字
            Text("龍")
                .font(.system(size: size * 0.45, weight: .bold, design: .serif))
                .foregroundStyle(
                    LinearGradient(
                        colors: [Color(red: 1, green: 0.84, blue: 0), Color.white],
                        startPoint: .top,
                        endPoint: .bottom
                    )
                )
                .shadow(color: Color(red: 1, green: 0.84, blue: 0).opacity(0.5), radius: 4)
            
            // 底部小字 - 魂
            Text("魂")
                .font(.system(size: size * 0.15, weight: .medium))
                .foregroundColor(Color(red: 0.8, green: 0.6, blue: 0.2))
                .offset(y: size * 0.28)
        }
    }
}

// MARK: - 献礼祖国77周年

struct 献礼标语: View {
    var body: some View {
        HStack(spacing: 8) {
            Rectangle()
                .fill(Color(red: 0.8, green: 0.1, blue: 0.1))
                .frame(width: 30, height: 2)
            
            VStack(spacing: 2) {
                Text("献礼祖国 77 周年")
                    .font(.system(size: 14, weight: .bold))
                    .foregroundColor(Color(red: 1, green: 0.84, blue: 0))
                
                Text("1949 — 2026")
                    .font(.system(size: 9))
                    .foregroundColor(.white.opacity(0.5))
            }
            
            Rectangle()
                .fill(Color(red: 0.8, green: 0.1, blue: 0.1))
                .frame(width: 30, height: 2)
        }
        .padding(.vertical, 6)
        .padding(.horizontal, 12)
        .background(
            RoundedRectangle(cornerRadius: 6)
                .fill(Color(red: 0.1, green: 0.02, blue: 0.02))
                .overlay(
                    RoundedRectangle(cornerRadius: 6)
                        .stroke(Color(red: 0.6, green: 0.1, blue: 0.1).opacity(0.5), lineWidth: 1)
                )
        )
    }
}

// MARK: - LU-Time Engine（时间推演引擎）

struct 时间推演 {
    let 时间戳: Date
    let 天干: String
    let 地支: String
    let 生肖: String
    let 上卦: Int      // 1~8
    let 下卦: Int      // 1~8
    let 卦象ID: Int    // 1~64
    let 卦名: String
    let 卦义: String
    let 熵值: Double   // 0~1
    let 行动建议: String  // 执行推进 / 调整优化 / 观察等待
    let 行动颜色: Color
    
    /// 从任意日期推算
    static func 推算(from date: Date = Date()) -> 时间推演 {
        let cal = Calendar.current
        let year = cal.component(.year, from: date)
        let month = cal.component(.month, from: date)
        let day = cal.component(.day, from: date)
        let hour = cal.component(.hour, from: date)
        
        let 天干序 = ((year - 4) % 10 + 10) % 10
        let 地支序 = ((year - 4) % 12 + 12) % 12
        
        let 天干表 = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
        let 地支表 = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
        let 生肖表 = ["鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"]
        
        // 上卦 = (天干序+月) mod 8, 下卦 = (日+时) mod 8
        let upper = ((天干序 + 1 + month) % 8 == 0) ? 8 : ((天干序 + 1 + month) % 8)
        let lower = ((day + hour) % 8 == 0) ? 8 : ((day + hour) % 8)
        let hexID = (upper - 1) * 8 + lower
        
        let entropy = Double(abs(upper - lower)) / 7.0
        
        let 行动: String
        let 颜色: Color
        if entropy > 0.7 {
            行动 = "观察等待"
            颜色 = .red
        } else if entropy > 0.4 {
            行动 = "调整优化"
            颜色 = .yellow
        } else {
            行动 = "执行推进"
            颜色 = .green
        }
        
        let 卦 = 卦象表.查询(id: hexID)
        
        return 时间推演(
            时间戳: date,
            天干: 天干表[天干序],
            地支: 地支表[地支序],
            生肖: 生肖表[地支序],
            上卦: upper,
            下卦: lower,
            卦象ID: hexID,
            卦名: 卦.名称,
            卦义: 卦.卦义,
            熵值: entropy,
            行动建议: 行动,
            行动颜色: 颜色
        )
    }
}

// MARK: - 八卦 & 64卦

private struct 卦象表 {
    
    static let 八卦名 = ["乾☰","兑☱","离☲","震☳","巽☴","坎☵","艮☶","坤☷"]
    static let 八卦元素 = ["天","泽","火","雷","风","水","山","地"]
    
    struct 卦信息 {
        let 名称: String
        let 卦义: String
    }
    
    // 核心64卦（精选卦义）
    static let 六十四卦: [Int: 卦信息] = [
        1:  卦信息(名称: "乾为天",   卦义: "刚健中正，自强不息"),
        2:  卦信息(名称: "天泽履",   卦义: "如履薄冰，谨慎前行"),
        8:  卦信息(名称: "天地否",   卦义: "天地不交，闭塞不通"),
        9:  卦信息(名称: "泽天夬",   卦义: "决断果敢，刚柔并济"),
        10: 卦信息(名称: "兑为泽",   卦义: "和悦相处，喜乐自在"),
        11: 卦信息(名称: "泽火革",   卦义: "变革更新，顺天应人"),
        17: 卦信息(名称: "离为火",   卦义: "光明附丽，文明以止"),
        19: 卦信息(名称: "火风鼎",   卦义: "鼎新革故，正位凝命"),
        25: 卦信息(名称: "巽为风",   卦义: "柔顺入微，随风潜入"),
        26: 卦信息(名称: "风泽中孚", 卦义: "诚信在内，感化万物"),
        33: 卦信息(名称: "坎为水",   卦义: "重重险难，习坎不止"),
        34: 卦信息(名称: "水泽节",   卦义: "节制有度，甘节吉祥"),
        41: 卦信息(名称: "艮为山",   卦义: "静止安定，知止不殆"),
        49: 卦信息(名称: "坤为地",   卦义: "厚德载物，包容万象"),
        50: 卦信息(名称: "地泽临",   卦义: "居上临下，教化万民"),
        57: 卦信息(名称: "地天泰",   卦义: "天地交泰，万物通达"),
        58: 卦信息(名称: "地泽临",   卦义: "以德服人，亲临百姓"),
        64: 卦信息(名称: "地水师",   卦义: "行师出征，纪律严明"),
    ]
    
    static func 查询(id: Int) -> 卦信息 {
        if let 精确 = 六十四卦[id] {
            return 精确
        }
        // 未精确收录的卦，用上下卦组合生成
        let upper = (id - 1) / 8   // 0~7
        let lower = (id - 1) % 8   // 0~7
        let 上名 = 八卦元素[upper]
        let 下名 = 八卦元素[lower]
        return 卦信息(
            名称: "\(上名)\(下名)卦",
            卦义: "\(八卦名[upper])上\(八卦名[lower])下，刚柔交感"
        )
    }
}

// MARK: - 节气引擎

private struct 节气引擎 {
    
    struct 节气信息 {
        let 名称: String
        let 月: Int
        let 日: Int
    }
    
    // 2026年二十四节气（近似值，误差±1天）
    static let 全部节气: [节气信息] = [
        节气信息(名称: "小寒", 月: 1, 日: 5),
        节气信息(名称: "大寒", 月: 1, 日: 20),
        节气信息(名称: "立春", 月: 2, 日: 4),
        节气信息(名称: "雨水", 月: 2, 日: 19),
        节气信息(名称: "惊蛰", 月: 3, 日: 6),
        节气信息(名称: "春分", 月: 3, 日: 21),
        节气信息(名称: "清明", 月: 4, 日: 5),
        节气信息(名称: "谷雨", 月: 4, 日: 20),
        节气信息(名称: "立夏", 月: 5, 日: 6),
        节气信息(名称: "小满", 月: 5, 日: 21),
        节气信息(名称: "芒种", 月: 6, 日: 6),
        节气信息(名称: "夏至", 月: 6, 日: 21),
        节气信息(名称: "小暑", 月: 7, 日: 7),
        节气信息(名称: "大暑", 月: 7, 日: 23),
        节气信息(名称: "立秋", 月: 8, 日: 7),
        节气信息(名称: "处暑", 月: 8, 日: 23),
        节气信息(名称: "白露", 月: 9, 日: 8),
        节气信息(名称: "秋分", 月: 9, 日: 23),
        节气信息(名称: "寒露", 月: 10, 日: 8),
        节气信息(名称: "霜降", 月: 10, 日: 23),
        节气信息(名称: "立冬", 月: 11, 日: 7),
        节气信息(名称: "小雪", 月: 11, 日: 22),
        节气信息(名称: "大雪", 月: 12, 日: 7),
        节气信息(名称: "冬至", 月: 12, 日: 22),
    ]
    
    /// 查询某天是否是节气（±1天容差）
    static func 查询节气(月: Int, 日: Int) -> String? {
        全部节气.first(where: { $0.月 == 月 && abs($0.日 - 日) <= 0 })?.名称
    }
    
    /// 查询某月的所有节气
    static func 月内节气(月: Int) -> [节气信息] {
        全部节气.filter { $0.月 == 月 }
    }
}

// MARK: - 传统节日

private struct 节日引擎 {
    
    /// 公历节日
    static func 公历节日(月: Int, 日: Int) -> String? {
        let 节日表: [String: String] = [
            "1-1": "元旦", "2-14": "情人节", "3-8": "妇女节",
            "3-12": "植树节", "4-1": "愚人节", "5-1": "劳动节",
            "5-4": "青年节", "6-1": "儿童节", "7-1": "建党节",
            "8-1": "建军节", "9-10": "教师节", "10-1": "国庆节",
            "10-31": "万圣节", "12-25": "圣诞节", "12-31": "跨年",
        ]
        return 节日表["\(月)-\(日)"]
    }
    
    /// 农历节日
    static func 农历节日(月: Int, 日: Int) -> String? {
        let 节日表: [String: String] = [
            "1-1": "春节", "1-15": "元宵节", "5-5": "端午节",
            "7-7": "七夕", "7-15": "中元节", "8-15": "中秋节",
            "9-9": "重阳节", "12-30": "除夕", "12-29": "除夕",
            "12-8": "腊八节",
        ]
        return 节日表["\(月)-\(日)"]
    }
}

// MARK: - 每日语录

private let 语录库: [String] = [
    "持经达变，以不变应万变 —— 曾仕强老师",
    "做人要厚道，凡事留余地 —— 曾仕强老师",
    "上善若水，水善利万物而不争 —— 道德经",
    "为而不争，天下莫能与之争 —— 道德经",
    "知常容，容乃公，公乃王 —— 道德经",
    "天之道，利而不害 —— 道德经",
    "信言不美，美言不信 —— 道德经",
    "千里之行，始于足下 —— 道德经",
    "知足者富，强行者有志 —— 道德经",
    "天下难事，必作于易 —— 道德经",
    "曲则全，枉则直，洼则盈 —— 道德经",
    "大方无隅，大器晚成 —— 道德经",
    "治大国，若烹小鲜 —— 道德经",
    "祸兮福之所倚，福兮祸之所伏 —— 道德经",
    "合抱之木，生于毫末 —— 道德经",
    "人法地，地法天，天法道，道法自然 —— 道德经",
    "道生一，一生二，二生三，三生万物 —— 道德经",
    "不自见，故明；不自是，故彰 —— 道德经",
    "有无相生，难易相成 —— 道德经",
    "功成事遂，百姓皆谓我自然 —— 道德经",
    "江海所以能为百谷王者，以其善下之 —— 道德经",
    "善者吾善之，不善者吾亦善之 —— 道德经",
    "柔弱胜刚强 —— 道德经",
    "民不畏威，则大威至 —— 道德经",
    "见素抱朴，少私寡欲 —— 道德经",
    "多言数穷，不如守中 —— 道德经",
    "天网恢恢，疏而不失 —— 道德经",
    "图难于其易，为大于其细 —— 道德经",
    "圣人无常心，以百姓心为心 —— 道德经",
    "飘风不终朝，骤雨不终日 —— 道德经",
    "祖国优先，普惠全球 —— UID9622",
]

// MARK: - 万年历主界面

struct 万年历View: View {
    @State private var 当前月份 = Date()
    @State private var 选中日期 = Date()
    
    private var 历法: Calendar { Calendar.current }
    private let 星期标题 = ["日", "一", "二", "三", "四", "五", "六"]
    
    var body: some View {
        ZStack {
            Color(red: 0.05, green: 0.05, blue: 0.12)
                .ignoresSafeArea()
            
            ScrollView {
                VStack(spacing: 16) {
                    // Logo + 献礼
                    龍魂Logo(size: 80)
                    献礼标语()
                    
                    // 今日信息卡
                    今日卡片
                    
                    // 时间推演（LU-Time Engine）
                    推演卡片
                    
                    // 月历
                    月历视图
                    
                    // 选中日期详情
                    日期详情
                    
                    // 操作时间线（草日志）
                    操作时间线
                    
                    // 每日语录
                    语录卡片
                }
                .padding(.horizontal, 16)
                .padding(.top, 8)
                .padding(.bottom, 30)
            }
        }
        .navigationTitle("万年历")
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        #endif
    }
    
    // MARK: - 今日信息卡
    
    private var 今日卡片: some View {
        let 农历 = LunarCalendar.convert()
        let cal = Calendar.current
        let 月 = cal.component(.month, from: Date())
        let 日 = cal.component(.day, from: Date())
        let 节气文字 = 节气引擎.查询节气(月: 月, 日: 日)
        let 公历节日文字 = 节日引擎.公历节日(月: 月, 日: 日)
        let 农历节日文字 = 节日引擎.农历节日(月: 农历.month, 日: 农历.day)
        
        return VStack(spacing: 10) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("今日")
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.5))
                    Text(农历.fullDisplay)
                        .font(.title3)
                        .fontWeight(.bold)
                        .foregroundColor(Color(red: 1, green: 0.84, blue: 0))
                }
                Spacer()
                VStack(alignment: .trailing, spacing: 4) {
                    Text(今日公历())
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.5))
                    HStack(spacing: 6) {
                        if let jq = 节气文字 {
                            标签视图(文字: "🍃 \(jq)", 颜色: Color.green.opacity(0.3))
                        }
                        if let gj = 公历节日文字 {
                            标签视图(文字: gj, 颜色: Color.red.opacity(0.3))
                        }
                        if let nj = 农历节日文字 {
                            标签视图(文字: nj, 颜色: Color(red: 0.8, green: 0.2, blue: 0.2).opacity(0.4))
                        }
                    }
                }
            }
        }
        .padding(16)
        .background(
            LinearGradient(
                colors: [Color(red: 0.15, green: 0.08, blue: 0.02), Color(red: 0.1, green: 0.05, blue: 0.15)],
                startPoint: .leading,
                endPoint: .trailing
            )
        )
        .cornerRadius(14)
        .overlay(
            RoundedRectangle(cornerRadius: 14)
                .stroke(Color(red: 1, green: 0.84, blue: 0).opacity(0.2), lineWidth: 1)
        )
    }
    
    // MARK: - 时间推演卡片（LU-Time Engine）
    
    private var 推演卡片: some View {
        let 推 = 时间推演.推算(from: 选中日期)
        let 上卦名 = 卦象表.八卦名[推.上卦 - 1]
        let 下卦名 = 卦象表.八卦名[推.下卦 - 1]
        
        return VStack(spacing: 12) {
            // 标题行
            HStack {
                Text("☰ 时间推演")
                    .font(.caption)
                    .fontWeight(.semibold)
                    .foregroundColor(Color(red: 0.6, green: 0.8, blue: 1.0))
                Spacer()
                Text("LU-Time Engine")
                    .font(.caption2)
                    .foregroundColor(.white.opacity(0.3))
            }
            
            // 卦象显示
            HStack(spacing: 16) {
                // 左：卦象
                VStack(spacing: 4) {
                    Text(推.卦名)
                        .font(.title3)
                        .fontWeight(.bold)
                        .foregroundColor(Color(red: 1, green: 0.84, blue: 0))
                    HStack(spacing: 4) {
                        Text(上卦名)
                            .font(.caption2)
                            .foregroundColor(.white.opacity(0.5))
                        Text("上")
                            .font(.system(size: 8))
                            .foregroundColor(.white.opacity(0.3))
                        Text(下卦名)
                            .font(.caption2)
                            .foregroundColor(.white.opacity(0.5))
                        Text("下")
                            .font(.system(size: 8))
                            .foregroundColor(.white.opacity(0.3))
                    }
                }
                
                // 中：熵值条
                VStack(alignment: .leading, spacing: 4) {
                    Text("熵值")
                        .font(.caption2)
                        .foregroundColor(.white.opacity(0.4))
                    
                    GeometryReader { geo in
                        ZStack(alignment: .leading) {
                            RoundedRectangle(cornerRadius: 3)
                                .fill(Color.white.opacity(0.1))
                                .frame(height: 6)
                            RoundedRectangle(cornerRadius: 3)
                                .fill(推.行动颜色)
                                .frame(width: geo.size.width * min(推.熵值, 1.0), height: 6)
                        }
                    }
                    .frame(height: 6)
                    
                    Text(String(format: "%.2f", 推.熵值))
                        .font(.system(size: 10, design: .monospaced))
                        .foregroundColor(.white.opacity(0.5))
                }
                .frame(maxWidth: .infinity)
                
                // 右：行动建议
                VStack(spacing: 4) {
                    Circle()
                        .fill(推.行动颜色)
                        .frame(width: 12, height: 12)
                    Text(推.行动建议)
                        .font(.caption2)
                        .fontWeight(.medium)
                        .foregroundColor(推.行动颜色)
                }
            }
            
            // 卦义
            Text("「\(推.卦义)」")
                .font(.caption)
                .foregroundColor(.white.opacity(0.6))
                .frame(maxWidth: .infinity, alignment: .leading)
            
            // 干支信息
            HStack {
                Text("\(推.天干)\(推.地支)年 · \(推.生肖)")
                    .font(.caption2)
                    .foregroundColor(.white.opacity(0.35))
                Spacer()
                Text("卦序 #\(推.卦象ID)")
                    .font(.caption2)
                    .foregroundColor(.white.opacity(0.25))
            }
        }
        .padding(14)
        .background(
            LinearGradient(
                colors: [Color(red: 0.08, green: 0.05, blue: 0.15), Color(red: 0.05, green: 0.08, blue: 0.18)],
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        )
        .cornerRadius(14)
        .overlay(
            RoundedRectangle(cornerRadius: 14)
                .stroke(Color(red: 0.4, green: 0.3, blue: 0.8).opacity(0.3), lineWidth: 1)
        )
    }
    
    // MARK: - 月历
    
    private var 月历视图: some View {
        VStack(spacing: 12) {
            // 月份切换
            HStack {
                Button { 切换月份(偏移: -1) } label: {
                    Image(systemName: "chevron.left")
                        .foregroundColor(.white.opacity(0.6))
                        .padding(8)
                }
                
                Spacer()
                
                Text(月份标题())
                    .font(.headline)
                    .foregroundColor(.white)
                
                Spacer()
                
                Button { 切换月份(偏移: 1) } label: {
                    Image(systemName: "chevron.right")
                        .foregroundColor(.white.opacity(0.6))
                        .padding(8)
                }
            }
            
            // 回到今天
            if !历法.isDate(当前月份, equalTo: Date(), toGranularity: .month) {
                Button {
                    withAnimation { 当前月份 = Date(); 选中日期 = Date() }
                } label: {
                    Text("回到今天")
                        .font(.caption)
                        .foregroundColor(Color(red: 0.6, green: 0.8, blue: 1))
                }
            }
            
            // 星期头
            HStack(spacing: 0) {
                ForEach(星期标题, id: \.self) { 标题 in
                    Text(标题)
                        .font(.caption2)
                        .fontWeight(.medium)
                        .foregroundColor(标题 == "日" || 标题 == "六" ? Color.red.opacity(0.7) : .white.opacity(0.4))
                        .frame(maxWidth: .infinity)
                }
            }
            
            // 日期格子
            let 周列表 = 生成月历周()
            
            VStack(spacing: 4) {
                ForEach(周列表, id: \.id) { 周 in
                    HStack(spacing: 0) {
                        ForEach(Array(周.天.enumerated()), id: \.offset) { _, 天 in
                            if let 日期 = 天 {
                                日期格子(日期: 日期)
                            } else {
                                Color.clear.frame(maxWidth: .infinity, minHeight: 44)
                            }
                        }
                    }
                }
            }
        }
        .padding(16)
        .background(Color.white.opacity(0.04))
        .cornerRadius(14)
    }
    
    // MARK: - 日期格子
    
    private func 日期格子(日期: Date) -> some View {
        let 日 = 历法.component(.day, from: 日期)
        let 月 = 历法.component(.month, from: 日期)
        let 是今天 = 历法.isDateInToday(日期)
        let 是选中 = 历法.isDate(日期, inSameDayAs: 选中日期)
        let 农历 = LunarCalendar.convert(from: 日期)
        let 节气 = 节气引擎.查询节气(月: 月, 日: 日)
        let 农历节日 = 节日引擎.农历节日(月: 农历.month, 日: 农历.day)
        let 公历节日 = 节日引擎.公历节日(月: 月, 日: 日)
        
        // 显示优先级：节日 > 节气 > 农历
        let 副文字: String
        let 副颜色: Color
        if let nj = 农历节日 {
            副文字 = nj
            副颜色 = Color(red: 1, green: 0.3, blue: 0.3)
        } else if let gj = 公历节日 {
            副文字 = gj
            副颜色 = Color(red: 1, green: 0.5, blue: 0.3)
        } else if let jq = 节气 {
            副文字 = jq
            副颜色 = Color.green.opacity(0.8)
        } else {
            副文字 = 农历.dayName
            副颜色 = .white.opacity(0.35)
        }
        
        return Button {
            withAnimation(.easeInOut(duration: 0.15)) { 选中日期 = 日期 }
        } label: {
            VStack(spacing: 1) {
                Text("\(日)")
                    .font(.system(size: 15, weight: 是今天 ? .bold : .regular))
                    .foregroundColor(是今天 ? .white : (是选中 ? Color(red: 0.6, green: 0.8, blue: 1) : .white.opacity(0.8)))
                
                Text(副文字)
                    .font(.system(size: 8))
                    .foregroundColor(副颜色)
                    .lineLimit(1)
                    .minimumScaleFactor(0.6)
            }
            .frame(maxWidth: .infinity, minHeight: 44)
            .background(
                Group {
                    if 是今天 {
                        Circle()
                            .fill(Color(red: 0.8, green: 0.1, blue: 0.1))
                            .frame(width: 36, height: 36)
                    } else if 是选中 {
                        Circle()
                            .fill(Color.white.opacity(0.1))
                            .frame(width: 36, height: 36)
                    }
                }
            )
        }
    }
    
    // MARK: - 选中日期详情
    
    private var 日期详情: some View {
        let 农历 = LunarCalendar.convert(from: 选中日期)
        let 月 = 历法.component(.month, from: 选中日期)
        let 日 = 历法.component(.day, from: 选中日期)
        let 节气 = 节气引擎.查询节气(月: 月, 日: 日)
        let 公历节日 = 节日引擎.公历节日(月: 月, 日: 日)
        let 农历节日 = 节日引擎.农历节日(月: 农历.month, 日: 农历.day)
        
        let fmt = DateFormatter()
        fmt.locale = Locale(identifier: "zh_CN")
        fmt.dateFormat = "yyyy年M月d日 EEEE"
        let 公历文字 = fmt.string(from: 选中日期)
        
        return VStack(alignment: .leading, spacing: 10) {
            Text("日期详情")
                .font(.caption)
                .foregroundColor(.white.opacity(0.5))
            
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 6) {
                    Text(公历文字)
                        .font(.subheadline)
                        .foregroundColor(.white.opacity(0.85))
                    Text(农历.fullDisplay)
                        .font(.subheadline)
                        .fontWeight(.medium)
                        .foregroundColor(Color(red: 1, green: 0.84, blue: 0))
                }
                
                Spacer()
                
                VStack(alignment: .trailing, spacing: 4) {
                    if let jq = 节气 {
                        标签视图(文字: "🍃 \(jq)", 颜色: Color.green.opacity(0.3))
                    }
                    if let gj = 公历节日 {
                        标签视图(文字: gj, 颜色: Color.orange.opacity(0.3))
                    }
                    if let nj = 农历节日 {
                        标签视图(文字: "🏮 \(nj)", 颜色: Color.red.opacity(0.3))
                    }
                }
            }
        }
        .padding(14)
        .background(Color.white.opacity(0.05))
        .cornerRadius(12)
    }
    
    // MARK: - 每日语录
    
    private var 语录卡片: some View {
        let 序 = Calendar.current.ordinality(of: .day, in: .year, for: Date()) ?? 1
        let 今日语录 = 语录库[序 % 语录库.count]
        
        return HStack(alignment: .top, spacing: 10) {
            Text("❝")
                .font(.title2)
                .foregroundColor(Color(red: 1, green: 0.84, blue: 0).opacity(0.5))
            
            Text(今日语录)
                .font(.subheadline)
                .foregroundColor(.white.opacity(0.75))
                .lineSpacing(4)
            
            Spacer()
        }
        .padding(14)
        .background(Color(red: 0.5, green: 0.05, blue: 0.05).opacity(0.3))
        .cornerRadius(12)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color(red: 215/255, green: 19/255, blue: 19/255).opacity(0.3), lineWidth: 1)
        )
    }
    
    // MARK: - 操作时间线（草日志）
    
    private var 操作时间线: some View {
        let 日志 = 草日志读取器.读取今日()
        
        return Group {
            if !日志.isEmpty {
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Text("📜 操作留痕")
                            .font(.caption)
                            .fontWeight(.semibold)
                            .foregroundColor(Color(red: 0.6, green: 0.8, blue: 1.0))
                        Spacer()
                        Text("\(日志.count) 条")
                            .font(.caption2)
                            .foregroundColor(.white.opacity(0.3))
                    }
                    
                    ForEach(日志.suffix(5).reversed()) { 条目 in
                        HStack(spacing: 10) {
                            // 时间
                            Text(条目.时间)
                                .font(.system(size: 11, design: .monospaced))
                                .foregroundColor(.white.opacity(0.4))
                                .frame(width: 40, alignment: .leading)
                            
                            // 竖线
                            Rectangle()
                                .fill(条目.状态颜色)
                                .frame(width: 2, height: 24)
                                .cornerRadius(1)
                            
                            // 内容
                            VStack(alignment: .leading, spacing: 2) {
                                Text(条目.动作)
                                    .font(.caption)
                                    .foregroundColor(.white.opacity(0.8))
                                    .lineLimit(1)
                                HStack(spacing: 4) {
                                    Text(条目.操作者)
                                        .font(.system(size: 9))
                                        .foregroundColor(.white.opacity(0.35))
                                    Text("·")
                                        .foregroundColor(.white.opacity(0.2))
                                    Text(条目.DNA)
                                        .font(.system(size: 9, design: .monospaced))
                                        .foregroundColor(.white.opacity(0.25))
                                        .lineLimit(1)
                                }
                            }
                            
                            Spacer()
                        }
                    }
                }
                .padding(14)
                .background(Color.white.opacity(0.04))
                .cornerRadius(12)
                .overlay(
                    RoundedRectangle(cornerRadius: 12)
                        .stroke(Color.white.opacity(0.08), lineWidth: 1)
                )
            }
        }
    }
    
    // MARK: - 辅助方法
    
    private func 今日公历() -> String {
        let fmt = DateFormatter()
        fmt.locale = Locale(identifier: "zh_CN")
        fmt.dateFormat = "M月d日 EEEE"
        return fmt.string(from: Date())
    }
    
    private func 月份标题() -> String {
        let fmt = DateFormatter()
        fmt.locale = Locale(identifier: "zh_CN")
        fmt.dateFormat = "yyyy年M月"
        return fmt.string(from: 当前月份)
    }
    
    private func 切换月份(偏移: Int) {
        if let 新月 = 历法.date(byAdding: .month, value: 偏移, to: 当前月份) {
            withAnimation(.easeInOut(duration: 0.2)) {
                当前月份 = 新月
            }
        }
    }
    
    private func 生成月历周() -> [日历周] {
        let cal = 历法
        guard let 月范围 = cal.range(of: .day, in: .month, for: 当前月份),
              let 月首日 = cal.date(from: cal.dateComponents([.year, .month], from: 当前月份))
        else { return [] }
        
        let 首日星期 = cal.component(.weekday, from: 月首日) - 1  // 0=周日
        
        var 全部天: [Date?] = Array(repeating: nil, count: 首日星期)
        
        for 天 in 月范围 {
            if let 日期 = cal.date(byAdding: .day, value: 天 - 1, to: 月首日) {
                全部天.append(日期)
            }
        }
        
        // 补齐到7的倍数
        while 全部天.count % 7 != 0 {
            全部天.append(nil)
        }
        
        // 按周分组
        var 周列表: [日历周] = []
        for i in stride(from: 0, to: 全部天.count, by: 7) {
            let 一周 = Array(全部天[i..<min(i + 7, 全部天.count)])
            周列表.append(日历周(id: i, 天: 一周))
        }
        
        return 周列表
    }
}

// MARK: - 日历周模型

private struct 日历周: Identifiable {
    let id: Int
    let 天: [Date?]
}

// MARK: - 草日志数据模型

struct 日志条目: Identifiable {
    let id: String
    let 时间: String
    let 动作: String
    let 页面: String
    let 操作者: String
    let DNA: String
    let 状态: String
    
    var 状态颜色: Color {
        switch 状态 {
        case "🔴": return .red
        case "🟡": return .yellow
        default:   return .green
        }
    }
}

// MARK: - 草日志读取器

struct 草日志读取器 {
    /// 读取今日的操作日志
    /// 数据源: ~/longhun-system/logs/action_log.jsonl
    /// 格式: 每行一个JSON {"time","lunar","ts","dna","tool","target","sensitive"}
    static func 读取今日() -> [日志条目] {
        let path = NSHomeDirectory() + "/longhun-system/logs/action_log.jsonl"

        guard let raw = try? String(contentsOfFile: path, encoding: .utf8) else { return [] }

        let 今日前缀 = {
            let fmt = DateFormatter()
            fmt.dateFormat = "yyyy-MM-dd"
            return fmt.string(from: Date())
        }()

        let lines = raw.components(separatedBy: "\n").filter { !$0.isEmpty }

        return lines
            .compactMap { line -> [String: Any]? in
                guard let data = line.data(using: .utf8),
                      let obj = try? JSONSerialization.jsonObject(with: data) as? [String: Any]
                else { return nil }
                return obj
            }
            .filter { ($0["time"] as? String ?? "").hasPrefix(今日前缀) }
            .suffix(20)                     // 最多显示20条，避免撑爆UI
            .enumerated()
            .map { (i, e) in
                // time: "2026-03-20 14:06:22" → 取 HH:mm 部分
                let fullTime = e["time"] as? String ?? ""
                let 时间显示 = fullTime.count >= 16
                    ? String(fullTime.dropFirst(11).prefix(5))
                    : fullTime

                // tool → 动作；target 截断到30字
                let 工具 = e["tool"] as? String ?? "操作"
                let 目标 = e["target"] as? String ?? ""
                let 动作文字 = "\(工具): \(目标.prefix(28))\(目标.count > 28 ? "…" : "")"

                // sensitive: 1 → 🟡，其余 🟢
                let 敏感 = (e["sensitive"] as? Int ?? 0) == 1
                let 状态 = 敏感 ? "🟡" : "🟢"

                let DNA码 = e["dna"] as? String ?? ""

                return 日志条目(
                    id: "\(i)",
                    时间: 时间显示,
                    动作: 动作文字,
                    页面: e["lunar"] as? String ?? "-",
                    操作者: "UID9622",
                    DNA: DNA码,
                    状态: 状态
                )
            }
    }
}

// MARK: - 标签组件

private struct 标签视图: View {
    let 文字: String
    let 颜色: Color
    
    var body: some View {
        Text(文字)
            .font(.caption2)
            .foregroundColor(.white.opacity(0.9))
            .padding(.horizontal, 8)
            .padding(.vertical, 3)
            .background(颜色)
            .cornerRadius(6)
    }
}
