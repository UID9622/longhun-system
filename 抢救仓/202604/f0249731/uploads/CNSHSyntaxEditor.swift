// CNSHSyntaxEditor.swift
// CNSH语法编辑器 - 伪代码检测 + 语法高亮 + 三色审计
// DNA: #龍芯⚡️2026-03-12-CNSH-SYNTAX-EDITOR-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: UID9622 诸葛鑫（龍芯北辰）
// 理论指导: 曾仕强老师（永恒显示）

import SwiftUI

// ═══════════════════════════════════════════════════════════════
// MARK: - CNSH 语法引擎
// ═══════════════════════════════════════════════════════════════

struct CNSHSyntaxEngine {

    // MARK: - CNSH 关键词表

    /// 控制流关键词
    static let 控制流关键词: Set<String> = [
        "如果", "否则", "否则如果",
        "循环", "当", "遍历",
        "跳出", "继续", "返回"
    ]

    /// 声明关键词
    static let 声明关键词: Set<String> = [
        "函数", "类", "结构", "枚举", "协议",
        "变量", "常量", "整数", "浮点", "字符串", "布尔",
        "返回类型", "属于"
    ]

    /// 操作关键词
    static let 操作关键词: Set<String> = [
        "打印", "输入", "导入", "抛出", "捕获",
        "新建", "删除", "空"
    ]

    /// 全部关键词
    static var 全部关键词: Set<String> {
        控制流关键词.union(声明关键词).union(操作关键词)
    }

    // MARK: - 伪代码检测（文化主权守护）

    /// 违规翻译词典：英文 → 应该用的中文
    static let 违规翻译表: [(伪代码: String, 正确写法: String, 分类: String)] = [
        // 文化关键词（绝对不可翻译）
        ("FiveElements",    "五行",   "文化主权"),
        ("Five Elements",   "五行",   "文化主权"),
        ("EightTrigrams",   "八卦",   "文化主权"),
        ("Eight Trigrams",  "八卦",   "文化主权"),
        ("HeavenlyStems",   "天干",   "文化主权"),
        ("EarthlyBranches", "地支",   "文化主权"),
        ("YinYang",         "阴阳",   "文化主权"),
        ("Yin Yang",        "阴阳",   "文化主权"),
        ("SolarTerms",      "节气",   "文化主权"),
        ("Solar Terms",     "节气",   "文化主权"),
        ("LunarCalendar",   "农历",   "文化主权"),
        ("Lunar Calendar",  "农历",   "文化主权"),
        ("FengShui",        "风水",   "文化主权"),
        ("Feng Shui",       "风水",   "文化主权"),
        ("Zodiac",          "生肖",   "文化主权"),
        ("TaiChi",          "太极",   "文化主权"),
        ("Tai Chi",         "太极",   "文化主权"),
        ("Qigong",          "气功",   "文化主权"),
        ("Qi Gong",         "气功",   "文化主权"),
        ("DaoDeJing",       "道德经", "文化主权"),
        ("Tao Te Ching",    "道德经", "文化主权"),
        ("I Ching",         "易经",   "文化主权"),
        ("Wuxing",          "五行",   "文化主权"),

        // 编程关键词（应该用中文）
        ("if",       "如果",   "关键词"),
        ("else",     "否则",   "关键词"),
        ("for",      "循环",   "关键词"),
        ("while",    "当",     "关键词"),
        ("function", "函数",   "关键词"),
        ("class",    "类",     "关键词"),
        ("return",   "返回",   "关键词"),
        ("print",    "打印",   "关键词"),
        ("var",      "变量",   "关键词"),
        ("let",      "常量",   "关键词"),
        ("int",      "整数",   "关键词"),
        ("float",    "浮点",   "关键词"),
        ("string",   "字符串", "关键词"),
        ("bool",     "布尔",   "关键词"),
        ("import",   "导入",   "关键词"),
        ("break",    "跳出",   "关键词"),
        ("continue", "继续",   "关键词"),
        ("struct",   "结构",   "关键词"),
        ("enum",     "枚举",   "关键词"),
        ("switch",   "选择",   "关键词"),
        ("case",     "情况",   "关键词"),
        ("true",     "真",     "关键词"),
        ("false",    "假",     "关键词"),
        ("null",     "空",     "关键词"),
        ("nil",      "空",     "关键词"),
        ("new",      "新建",   "关键词"),
        ("delete",   "删除",   "关键词"),
        ("try",      "尝试",   "关键词"),
        ("catch",    "捕获",   "关键词"),
        ("throw",    "抛出",   "关键词"),
    ]

    // MARK: - 检测结果

    struct 检测结果 {
        let 行号: Int
        let 伪代码: String
        let 正确写法: String
        let 分类: String   // "文化主权" 或 "关键词"
        let 位置: Range<String.Index>
    }

    /// 扫描代码，返回所有伪代码问题
    static func 检测伪代码(_ code: String) -> [检测结果] {
        var results: [检测结果] = []
        let lines = code.components(separatedBy: "\n")

        for (lineIndex, line) in lines.enumerated() {
            // 跳过注释行（# 开头或 // 开头）— 注释允许多语言
            let trimmed = line.trimmingCharacters(in: .whitespaces)
            if trimmed.hasPrefix("#") || trimmed.hasPrefix("//") {
                continue
            }

            // 跳过字符串内容（「」『』"" 内的不检测）
            let cleanLine = 去除字符串内容(line)

            for entry in 违规翻译表 {
                // 用大小写不敏感搜索
                var searchStart = cleanLine.startIndex
                while searchStart < cleanLine.endIndex {
                    let searchRange = searchStart..<cleanLine.endIndex
                    if let range = cleanLine.range(of: entry.伪代码, options: .caseInsensitive, range: searchRange) {
                        results.append(检测结果(
                            行号: lineIndex + 1,
                            伪代码: entry.伪代码,
                            正确写法: entry.正确写法,
                            分类: entry.分类,
                            位置: range
                        ))
                        searchStart = range.upperBound
                    } else {
                        break
                    }
                }
            }
        }

        return results
    }

    /// 去除字符串内容，保留字符串外的代码
    private static func 去除字符串内容(_ line: String) -> String {
        var result = ""
        var inString = false
        var quoteChar: Character = "\""
        var prev: Character = " "

        for ch in line {
            if !inString {
                if ch == "\"" || ch == "'" {
                    inString = true
                    quoteChar = ch
                    result.append(ch)
                } else if ch == "「" {
                    inString = true
                    quoteChar = "」"
                    result.append(ch)
                } else if ch == "『" {
                    inString = true
                    quoteChar = "』"
                    result.append(ch)
                } else {
                    result.append(ch)
                }
            } else {
                if ch == quoteChar && prev != "\\" {
                    inString = false
                    result.append(ch)
                } else {
                    result.append(" ") // 替换为空格
                }
            }
            prev = ch
        }
        return result
    }

    // MARK: - 三色审计

    enum 审计级别: String {
        case 绿色 = "🟢"
        case 黄色 = "🟡"
        case 红色 = "🔴"
    }

    struct 审计结果 {
        let 级别: 审计级别
        let 文化违规数: Int
        let 关键词违规数: Int
        let 详情: [检测结果]
        let 评语: String
    }

    /// 三色审计
    static func 三色审计(_ code: String) -> 审计结果 {
        let issues = 检测伪代码(code)

        let 文化违规 = issues.filter { $0.分类 == "文化主权" }
        let 关键词违规 = issues.filter { $0.分类 == "关键词" }

        let level: 审计级别
        let comment: String

        if !文化违规.isEmpty {
            level = .红色
            comment = "文化主权被侵犯！发现 \(文化违规.count) 处文化关键词被翻译"
        } else if !关键词违规.isEmpty {
            level = .黄色
            comment = "发现 \(关键词违规.count) 处英文关键词，建议替换为中文"
        } else {
            level = .绿色
            comment = "代码符合 CNSH 规范 ✅"
        }

        return 审计结果(
            级别: level,
            文化违规数: 文化违规.count,
            关键词违规数: 关键词违规.count,
            详情: issues,
            评语: comment
        )
    }
}

// ═══════════════════════════════════════════════════════════════
// MARK: - CNSH 语法编辑器视图
// ═══════════════════════════════════════════════════════════════

struct CNSHSyntaxEditorView: View {
    @State private var code: String = """
    # CNSH示例程序
    # DNA追溯码：#龍芯⚡️2026-CNSH-示例
    
    函数 主函数() 返回类型 整数 {
        打印「🇨🇳 你好，CNSH语言！」
    
        整数 成本 = 80
        整数 售价 = 120
        整数 利润 = 售价 - 成本
    
        如果【利润 > 0】{
            打印「✅ 有利润」
        } 否则 {
            打印「❌ 亏损」
        }
    
        循环【3】{
            打印「🔄 循环执行中...」
        }
    
        返回 0
    }
    """

    @State private var 审计结果: CNSHSyntaxEngine.审计结果?
    @State private var showAuditDetail = false

    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // 顶部审计状态栏
                审计状态栏

                // 代码编辑区
                编辑区域

                // 底部工具栏
                底部工具栏
            }
            .navigationTitle("CNSH 语法编辑器")
            #if os(iOS)
            .navigationBarTitleDisplayMode(.inline)
            #endif
            .toolbar {
                ToolbarItem(placement: .automatic) {
                    Button(action: 执行审计) {
                        Label("审计", systemImage: "shield.checkered")
                    }
                }
            }
            .sheet(isPresented: $showAuditDetail) {
                审计详情视图
            }
            .onAppear {
                执行审计()
            }
        }
    }

    // MARK: - 审计状态栏

    private var 审计状态栏: some View {
        HStack(spacing: 12) {
            if let result = 审计结果 {
                Text(result.级别.rawValue)
                    .font(.title2)

                VStack(alignment: .leading, spacing: 2) {
                    Text(result.评语)
                        .font(.caption)
                        .fontWeight(.medium)
                        .foregroundColor(.primary)

                    HStack(spacing: 8) {
                        if result.文化违规数 > 0 {
                            Label("\(result.文化违规数) 文化违规", systemImage: "exclamationmark.triangle.fill")
                                .font(.caption2)
                                .foregroundColor(.red)
                        }
                        if result.关键词违规数 > 0 {
                            Label("\(result.关键词违规数) 关键词", systemImage: "exclamationmark.circle")
                                .font(.caption2)
                                .foregroundColor(.orange)
                        }
                    }
                }

                Spacer()

                Button(action: { showAuditDetail = true }) {
                    Image(systemName: "list.bullet.rectangle")
                        .font(.title3)
                }
                .disabled(result.详情.isEmpty)
            } else {
                Text("点击审计按钮开始检测")
                    .font(.caption)
                    .foregroundColor(.secondary)
                Spacer()
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 10)
        .background(审计背景色)
    }

    private var 审计背景色: Color {
        guard let result = 审计结果 else { return Color.gray.opacity(0.15) }
        switch result.级别 {
        case .绿色: return Color.green.opacity(0.12)
        case .黄色: return Color.orange.opacity(0.12)
        case .红色: return Color.red.opacity(0.12)
        }
    }

    // MARK: - 编辑区域

    private var 编辑区域: some View {
        ZStack(alignment: .topLeading) {
            // 行号 + 代码
            TextEditor(text: $code)
                .font(.system(.body, design: .monospaced))
                #if os(iOS)
                .autocapitalization(.none)
                #endif
                .autocorrectionDisabled()
                .padding(.leading, 8)
                .onChange(of: code) {
                    执行审计()
                }
        }
    }

    // MARK: - 底部工具栏

    private var 底部工具栏: some View {
        VStack(spacing: 0) {
            Divider()

            // 快捷输入栏
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    快捷按钮("函数")
                    快捷按钮("如果")
                    快捷按钮("否则")
                    快捷按钮("循环")
                    快捷按钮("打印")
                    快捷按钮("返回")
                    快捷按钮("整数")
                    快捷按钮("字符串")
                    快捷按钮("变量")
                    快捷按钮("常量")
                    快捷按钮("「」")
                    快捷按钮("【】")
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 8)
            }
            .background(Color.gray.opacity(0.15))

            // 统计信息
            HStack {
                Text("行数: \(code.components(separatedBy: "\n").count)")
                Spacer()
                Text("CNSH v1.0")
                Spacer()
                Text("UID9622")
            }
            .font(.caption2)
            .foregroundColor(.secondary)
            .padding(.horizontal, 16)
            .padding(.vertical, 6)
            .background(Color.gray.opacity(0.15))
        }
    }

    private func 快捷按钮(_ text: String) -> some View {
        Button(action: {
            code += text
        }) {
            Text(text)
                .font(.system(.caption, design: .monospaced))
                .fontWeight(.medium)
                .padding(.horizontal, 10)
                .padding(.vertical, 6)
                .background(Color.white.opacity(0.9))
                .cornerRadius(6)
                .overlay(
                    RoundedRectangle(cornerRadius: 6)
                        .stroke(Color.gray.opacity(0.4), lineWidth: 1)
                )
        }
    }

    // MARK: - 审计详情

    private var 审计详情视图: some View {
        NavigationView {
            List {
                if let result = 审计结果 {
                    // 总览
                    Section(header: Text("审计总览")) {
                        HStack {
                            Text("审计级别")
                            Spacer()
                            Text(result.级别.rawValue + " " + {
                                switch result.级别 {
                                case .绿色: return "通过"
                                case .黄色: return "警告"
                                case .红色: return "阻断"
                                }
                            }())
                            .fontWeight(.bold)
                        }

                        HStack {
                            Text("文化违规")
                            Spacer()
                            Text("\(result.文化违规数)")
                                .foregroundColor(result.文化违规数 > 0 ? .red : .green)
                        }

                        HStack {
                            Text("关键词违规")
                            Spacer()
                            Text("\(result.关键词违规数)")
                                .foregroundColor(result.关键词违规数 > 0 ? .orange : .green)
                        }
                    }

                    // 详细问题列表
                    if !result.详情.isEmpty {
                        Section(header: Text("问题列表（点击可自动修复）")) {
                            ForEach(Array(result.详情.enumerated()), id: \.offset) { _, issue in
                                Button(action: {
                                    自动修复(issue)
                                }) {
                                    HStack {
                                        VStack(alignment: .leading, spacing: 4) {
                                            HStack(spacing: 4) {
                                                Text(issue.分类 == "文化主权" ? "🔴" : "🟡")
                                                Text("第 \(issue.行号) 行")
                                                    .font(.caption)
                                                    .foregroundColor(.secondary)
                                            }

                                            HStack(spacing: 4) {
                                                Text(issue.伪代码)
                                                    .font(.system(.caption, design: .monospaced))
                                                    .strikethrough()
                                                    .foregroundColor(.red)

                                                Image(systemName: "arrow.right")
                                                    .font(.caption2)
                                                    .foregroundColor(.secondary)

                                                Text(issue.正确写法)
                                                    .font(.system(.caption, design: .monospaced))
                                                    .foregroundColor(.green)
                                                    .fontWeight(.bold)
                                            }
                                        }

                                        Spacer()

                                        Image(systemName: "wrench.and.screwdriver")
                                            .foregroundColor(.accentColor)
                                    }
                                }
                            }
                        }

                        // 一键全部修复
                        Section {
                            Button(action: 一键修复全部) {
                                HStack {
                                    Image(systemName: "wand.and.stars")
                                    Text("一键修复全部")
                                    Spacer()
                                    Text("\(result.详情.count) 项")
                                        .foregroundColor(.secondary)
                                }
                            }
                        }
                    }
                }
            }
            .navigationTitle("三色审计报告")
            #if os(iOS)
            .navigationBarTitleDisplayMode(.inline)
            #endif
            .toolbar {
                ToolbarItem(placement: .automatic) {
                    Button("完成") {
                        showAuditDetail = false
                    }
                }
            }
        }
    }

    // MARK: - 功能方法

    private func 执行审计() {
        审计结果 = CNSHSyntaxEngine.三色审计(code)
    }

    private func 自动修复(_ issue: CNSHSyntaxEngine.检测结果) {
        code = code.replacingOccurrences(of: issue.伪代码, with: issue.正确写法)
        执行审计()
    }

    private func 一键修复全部() {
        guard let result = 审计结果 else { return }
        var fixedCode = code
        for issue in result.详情 {
            fixedCode = fixedCode.replacingOccurrences(of: issue.伪代码, with: issue.正确写法)
        }
        code = fixedCode
        执行审计()
        showAuditDetail = false
    }
}

// ═══════════════════════════════════════════════════════════════
// MARK: - Preview
// ═══════════════════════════════════════════════════════════════

#Preview("CNSH编辑器 - 正常代码") {
    CNSHSyntaxEditorView()
}

#Preview("CNSH编辑器 - 含伪代码") {
    CNSHSyntaxEditorView()
}
