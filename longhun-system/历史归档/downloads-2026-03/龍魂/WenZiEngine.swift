// WenZiEngine.swift
// 文子引擎 - 中华智慧语录生成器
//
// DNA追溯码: #龍芯⚡️2026-03-09-WENZI-ENGINE
// 创建者: 诸葛鑫 (UID9622)
// 理论指导: 曾仕强老师（永恒显示）

import Foundation

class WenZiEngine {
    
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
    
    // 每日激励
    private let dailyMotivation = [
        "今日宜：修身养性，厚积薄发",
        "今日宜：以静制动，观察为主",
        "今日宜：主动出击，把握机会",
        "今日宜：韬光养晦，蓄势待发",
        "今日宜：刚柔并济，进退有度"
    ]
    
    // 根据时间生成合适的语录
    func getQuote(date: Date = Date()) -> String {
        let calendar = Calendar.current
        let hour = calendar.component(.hour, from: date)
        let day = calendar.component(.day, from: date)
        
        // 根据时辰选择不同类型的语录
        switch hour {
        case 5..<7:  // 卯时（5-7点）- 早晨
            return "🌅 " + dailyMotivation.randomElement()!
        case 7..<12: // 辰巳午时（7-12点）- 上午
            return "📖 " + zengQuotes.randomElement()!
        case 12..<14: // 未时（12-14点）- 午休
            return "☯️ " + yijing.randomElement()!
        case 14..<18: // 申酉时（14-18点）- 下午
            return "💭 " + laozi.randomElement()!
        case 18..<21: // 戌时（18-21点）- 傍晚
            return "🐉 " + longhunQuotes.randomElement()!
        default:     // 夜间
            return "🌙 " + zengQuotes.randomElement()!
        }
    }
    
    // 根据日期获取固定语录（每天同一句）
    func getDailyQuote(date: Date = Date()) -> String {
        let calendar = Calendar.current
        let dayOfYear = calendar.ordinality(of: .day, in: .year, for: date) ?? 1
        
        let allQuotes = zengQuotes + laozi + yijing + longhunQuotes
        let index = dayOfYear % allQuotes.count
        
        return allQuotes[index]
    }
    
    // 智能语录生成（结合节气）
    func getContextualQuote(solarTerm: String, date: Date = Date()) -> String {
        let calendar = Calendar.current
        let hour = calendar.component(.hour, from: date)
        
        // 根据节气选择相应的智慧
        var quote = ""
        
        switch solarTerm {
        case "立春", "雨水", "惊蛰", "春分", "清明", "谷雨":
            quote = "春生夏长，万物复苏 · " + yijing.randomElement()!
        case "立夏", "小满", "芒种", "夏至", "小暑", "大暑":
            quote = "夏时阳盛，当养心神 · " + laozi.randomElement()!
        case "立秋", "处暑", "白露", "秋分", "寒露", "霜降":
            quote = "秋收冬藏，知足常乐 · " + zengQuotes.randomElement()!
        case "立冬", "小雪", "大雪", "冬至", "小寒", "大寒":
            quote = "冬藏待春，静待花开 · " + longhunQuotes.randomElement()!
        default:
            quote = getQuote(date: date)
        }
        
        return quote
    }
}
