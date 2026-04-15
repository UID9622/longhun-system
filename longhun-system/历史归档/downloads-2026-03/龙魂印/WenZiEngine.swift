// WenZiEngine.swift
// 文子引擎 - 献礼新中国成立77周年版
//
// DNA追溯码: #龍芯⚡️2026-03-09-WENZI-ENGINE-77TH
// 创建者: 诸葛鑫 (UID9622)
// 理论指导: 曾仕强老师（永恒显示）
// 献礼: 新中国成立77周年（1949-2026）

import Foundation

class WenZiEngine {
    
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    // 献礼77周年专属语录库（优先级最高）
    // 整合千问方案：丙午马年元素
    // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    private let celebration77th = [
        // 千问精华献礼词
        "山河无恙·国泰民安",
        "七十七载逢盛世·砥砺奋进新征程",
        
        // 马年+77周年结合
        "丙午马年·七十七载芳华",
        "龍马精神·奋进新时代",
        "一马当先·建功新征程",
        "万马奔腾·盛世中华",
        "骐骥驰骋·复兴伟业",
        
        // 传统献礼词
        "七十七年风雨路·初心如磐向未来",
        "七十七载春秋·见证东方崛起",
        "壮丽七十七年·辉煌新时代",
        "山河壮丽·国运昌隆",
        "七十七年奋斗·铸就中国梦",
        "继往开来·再创辉煌",
        "七十七载峥嵘·不忘初心",
        "盛世华诞·与国同庆",
        "七十七年征程·见证复兴伟业",
        "红旗漫卷·国运兴隆",
        "七十七载芳华·书写时代华章",
        "祖国万岁·人民万岁"
    ]
    
    // 曾仕强老师语录库
    private let zengQuotes = [
        "持经达变，以不变应万变",
        "合理就好，不要追求完美",
        "人生最大的价值在于觉醒和思考",
        "中国人的管理哲学：修己安人",
        "做人做事，要圆通而不是圆滑",
        "安人之道，在于察觉需求",
        "人只有替自己做事才会效率高",
        "自作自受，各修各得",
        "太过方正的人，往往不能成大事"
    ]
    
    // 道德经语录库
    private let laozi = [
        "道可道，非常道；名可名，非常名",
        "上善若水，水善利万物而不争",
        "知人者智，自知者明",
        "祸兮福之所倚，福兮祸之所伏",
        "天地不仁，以万物为刍狗",
        "大音希声，大象无形",
        "千里之行，始于足下",
        "知足不辱，知止不殆"
    ]
    
    // 易经智慧
    private let yijing = [
        "天行健，君子以自强不息",
        "地势坤，君子以厚德载物",
        "穷则变，变则通，通则久",
        "一阴一阳之谓道",
        "君子藏器于身，待时而动",
        "同声相应，同气相求",
        "积善之家，必有余庆"
    ]
    
    // 龍魂系统专属语录
    private let longhunQuotes = [
        "祖国优先，普惠全球，技术为人民服务",
        "数字主权在手，数据不出境",
        "有理在手，绝不退让",
        "守住底线，释放自由",
        "DNA追溯，源头可查",
        "三才算法：天地人合一",
        "五行占位：金木水火土"
    ]
    
    // 根据时间生成合适的语录（献礼版）
    func getQuote(date: Date = Date()) -> String {
        let calendar = Calendar.current
        let hour = calendar.component(.hour, from: date)
        let month = calendar.component(.month, from: date)
        
        // 2026年全年优先显示献礼语录
        // 特别是1月（元旦）、10月（国庆）必须显示献礼语
        if month == 1 || month == 10 {
            return "🇨🇳 " + celebration77th.randomElement()!
        }
        
        // 其他时间：60%概率献礼语，40%概率其他语录
        let showCelebration = Double.random(in: 0...1) < 0.6
        if showCelebration {
            return "🇨🇳 " + celebration77th.randomElement()!
        }
        
        // 根据时辰选择不同类型的语录
        switch hour {
        case 5..<7:  // 卯时（5-7点）- 早晨
            return "📖 " + zengQuotes.randomElement()!
        case 7..<12: // 辰巳午时（7-12点）- 上午
            return "☯️ " + yijing.randomElement()!
        case 12..<14: // 未时（12-14点）- 午休
            return "💭 " + laozi.randomElement()!
        case 14..<18: // 申酉时（14-18点）- 下午
            return "📖 " + zengQuotes.randomElement()!
        case 18..<21: // 戌时（18-21点）- 傍晚
            return "🐉 " + longhunQuotes.randomElement()!
        default:     // 夜间
            return "🇨🇳 " + celebration77th.randomElement()!
        }
    }
    
    // 根据日期获取固定语录（每天同一句）
    func getDailyQuote(date: Date = Date()) -> String {
        let calendar = Calendar.current
        let dayOfYear = calendar.ordinality(of: .day, in: .year, for: date) ?? 1
        let month = calendar.component(.month, from: date)
        
        // 1月和10月固定显示献礼语
        if month == 1 || month == 10 {
            let index = dayOfYear % celebration77th.count
            return "🇨🇳 " + celebration77th[index]
        }
        
        // 其他月份：献礼语 + 其他语录混合
        let allQuotes = celebration77th + zengQuotes + laozi + yijing
        let index = dayOfYear % allQuotes.count
        
        return allQuotes[index]
    }
    
    // 智能语录生成（结合节气，优先献礼）
    func getContextualQuote(solarTerm: String, date: Date = Date()) -> String {
        let calendar = Calendar.current
        let month = calendar.component(.month, from: date)
        
        // 1月和10月强制献礼语
        if month == 1 || month == 10 {
            return celebration77th.randomElement()!
        }
        
        // 2026年全年：70%概率显示献礼语
        let showCelebration = Double.random(in: 0...1) < 0.7
        if showCelebration {
            return celebration77th.randomElement()!
        }
        
        // 其他情况根据节气选择
        var quote = ""
        
        switch solarTerm {
        case "立春", "雨水", "惊蛰", "春分", "清明", "谷雨":
            quote = yijing.randomElement()!
        case "立夏", "小满", "芒种", "夏至", "小暑", "大暑":
            quote = laozi.randomElement()!
        case "立秋", "处暑", "白露", "秋分", "寒露", "霜降":
            quote = zengQuotes.randomElement()!
        case "立冬", "小雪", "大雪", "冬至", "小寒", "大寒":
            quote = longhunQuotes.randomElement()!
        default:
            quote = celebration77th.randomElement()!
        }
        
        return quote
    }
}
