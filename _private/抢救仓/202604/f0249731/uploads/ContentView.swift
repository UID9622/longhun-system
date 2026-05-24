// ContentView.swift
// 龍魂·生态入口 v5.0 · 赛博重构
// DNA: #龍芯⚡️2026-03-20-PORTAL-CYBER-v5.0
// 创始人: 诸葛鑫（UID9622）
// 理论指导: 曾仕强老师（永恒显示）

import SwiftUI

struct ContentView: View {
    @State private var 搜索词 = ""
    @State private var 搜索结果: [NotionPage] = []
    @State private var 正在搜索 = false
    @State private var 显示版本信息 = false
    @State private var notion看板列表: [NotionPageItem] = []
    @State private var notion加载中 = false

    // 赛博配色
    private let 霓虹    = Color(red: 0,    green: 1,    blue: 0.78)   // #00ffc8
    private let 霓虹蓝  = Color(red: 0,    green: 0.83, blue: 1)      // #00d4ff
    private let 霓虹紫  = Color(red: 0.42, green: 0.37, blue: 0.91)   // #6c5ce7
    private let 霓虹红  = Color(red: 1,    green: 0.28, blue: 0.34)   // #ff4757
    private let 龍金    = Color(red: 1,    green: 0.84, blue: 0)      // 文化金·保留
    private let 卡底    = Color(red: 0.05, green: 0.05, blue: 0.12)

    var body: some View {
        NavigationStack {
            ZStack {
                // 深黑底
                Color(red: 0.03, green: 0.03, blue: 0.07)
                    .ignoresSafeArea()

                // 网格纹
                GeometryReader { geo in
                    Path { path in
                        let step: CGFloat = 44
                        var x: CGFloat = 0
                        while x < geo.size.width {
                            path.move(to: CGPoint(x: x, y: 0))
                            path.addLine(to: CGPoint(x: x, y: geo.size.height))
                            x += step
                        }
                        var y: CGFloat = 0
                        while y < geo.size.height {
                            path.move(to: CGPoint(x: 0, y: y))
                            path.addLine(to: CGPoint(x: geo.size.width, y: y))
                            y += step
                        }
                    }
                    .stroke(霓虹.opacity(0.035), lineWidth: 0.5)
                }
                .ignoresSafeArea()

                ScrollView(showsIndicators: false) {
                    VStack(spacing: 0) {

                        // MARK: - 顶栏 Logo
                        HStack(spacing: 12) {
                            ZStack {
                                Circle()
                                    .stroke(霓虹.opacity(0.25), lineWidth: 1)
                                    .frame(width: 46, height: 46)
                                Circle()
                                    .fill(卡底)
                                    .frame(width: 40, height: 40)
                                    .overlay(
                                        Circle().stroke(
                                            LinearGradient(colors: [霓虹, 霓虹.opacity(0.3)],
                                                           startPoint: .topLeading,
                                                           endPoint: .bottomTrailing),
                                            lineWidth: 1.5
                                        )
                                    )
                                    .shadow(color: 霓虹.opacity(0.3), radius: 8)
                                Text("龍")
                                    .font(.system(size: 18, weight: .bold, design: .serif))
                                    .foregroundColor(龍金)
                            }

                            VStack(alignment: .leading, spacing: 2) {
                                Text("龍魂")
                                    .font(.system(size: 18, weight: .bold, design: .monospaced))
                                    .foregroundColor(.white)
                                Text("LONGHUN · v1.3 · UID9622")
                                    .font(.system(size: 10, design: .monospaced))
                                    .foregroundColor(霓虹.opacity(0.6))
                            }

                            Spacer()

                            // 状态指示
                            HStack(spacing: 4) {
                                Circle().fill(霓虹).frame(width: 5, height: 5)
                                    .shadow(color: 霓虹, radius: 3)
                                Text("ONLINE")
                                    .font(.system(size: 9, weight: .bold, design: .monospaced))
                                    .foregroundColor(霓虹.opacity(0.7))
                            }
                            .padding(.horizontal, 8)
                            .padding(.vertical, 4)
                            .background(霓虹.opacity(0.06))
                            .cornerRadius(4)
                            .overlay(RoundedRectangle(cornerRadius: 4).stroke(霓虹.opacity(0.2), lineWidth: 0.5))
                        }
                        .padding(.horizontal, 16)
                        .padding(.top, 16)
                        .padding(.bottom, 20)

                        // MARK: - 生态工具矩阵
                        VStack(alignment: .leading, spacing: 10) {
                            赛博标题("// 生态工具", 副: "\(生态数量) modules", 颜色: 霓虹)

                            // 大卡片双列
                            HStack(spacing: 10) {
                                NavigationLink(destination: 万年历View()) {
                                    赛博大卡(
                                        图标: "📅", 标题: "万年历",
                                        说明: "农历 · 节气 · 卦象",
                                        标签: "CORE",
                                        边框色: 霓虹红
                                    )
                                }
                                NavigationLink(destination: 存证View()) {
                                    赛博大卡(
                                        图标: "🔐", 标题: "存证",
                                        说明: "哈希 · DNA · 主权",
                                        标签: "GUARD",
                                        边框色: 霓虹蓝
                                    )
                                }
                            }
                            .padding(.horizontal, 16)

                            // 工具条列表
                            VStack(spacing: 8) {
                                NavigationLink(destination: 记事本View()) {
                                    赛博工具条(图标: "📝", 标题: "记事本", 说明: "保存记忆 · 搜索记忆", 点色: 霓虹蓝)
                                }
                                NavigationLink(destination: CNSHSyntaxEditorView()) {
                                    赛博工具条(图标: "🐉", 标题: "CNSH 编辑器", 说明: "伪代码审计 · 三色检测", 点色: 霓虹紫)
                                }
                            }
                            .padding(.horizontal, 16)
                        }
                        .padding(.bottom, 20)

                        // MARK: - Notion知识看板
                        VStack(alignment: .leading, spacing: 10) {
                            HStack {
                                赛博标题("// 知识看板", 副: "Notion实时数据", 颜色: 霓虹蓝)
                                if notion加载中 {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: 霓虹蓝))
                                        .scaleEffect(0.6)
                                        .padding(.trailing, 16)
                                } else {
                                    Button(action: 加载Notion看板) {
                                        Image(systemName: "arrow.clockwise")
                                            .font(.system(size: 11))
                                            .foregroundColor(霓虹蓝.opacity(0.5))
                                    }
                                    .padding(.trailing, 16)
                                }
                            }

                            if notion看板列表.isEmpty && !notion加载中 {
                                HStack(spacing: 8) {
                                    Rectangle().fill(霓虹蓝.opacity(0.3)).frame(width: 2)
                                    Text("点击刷新加载Notion数据...")
                                        .font(.system(size: 12, design: .monospaced))
                                        .foregroundColor(.white.opacity(0.3))
                                    Spacer()
                                }
                                .padding(12)
                                .background(卡底)
                                .cornerRadius(8)
                                .overlay(RoundedRectangle(cornerRadius: 8).stroke(霓虹蓝.opacity(0.15), lineWidth: 1))
                                .padding(.horizontal, 16)
                            } else {
                                ScrollView(.horizontal, showsIndicators: false) {
                                    HStack(spacing: 10) {
                                        ForEach(notion看板列表) { 页面 in
                                            NotionPageCard(页面: 页面, 霓虹蓝: 霓虹蓝, 卡底: 卡底)
                                        }
                                    }
                                    .padding(.horizontal, 16)
                                }
                            }

                            // 搜索栏
                            HStack(spacing: 10) {
                                Image(systemName: "magnifyingglass")
                                    .foregroundColor(霓虹蓝.opacity(0.5))
                                    .font(.system(size: 13))
                                TextField("搜索知识库...", text: $搜索词)
                                    .foregroundColor(.white)
                                    .font(.system(size: 13, design: .monospaced))
                                    .submitLabel(.search)
                                    .onSubmit { 执行搜索() }
                                if 正在搜索 {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: 霓虹蓝))
                                        .scaleEffect(0.65)
                                } else if !搜索词.isEmpty {
                                    Button(action: 执行搜索) {
                                        Image(systemName: "arrow.right.circle.fill")
                                            .foregroundColor(霓虹蓝)
                                    }
                                }
                            }
                            .padding(10)
                            .background(卡底)
                            .cornerRadius(8)
                            .overlay(RoundedRectangle(cornerRadius: 8).stroke(霓虹蓝.opacity(0.25), lineWidth: 1))
                            .padding(.horizontal, 16)

                            if !搜索结果.isEmpty {
                                VStack(spacing: 0) {
                                    ForEach(搜索结果.prefix(5)) { 页面 in
                                        HStack(spacing: 8) {
                                            Rectangle().fill(霓虹蓝.opacity(0.5)).frame(width: 2)
                                            Text(页面.标题.isEmpty ? "无标题" : 页面.标题)
                                                .font(.system(size: 12))
                                                .foregroundColor(.white.opacity(0.85))
                                                .lineLimit(1)
                                            Spacer()
                                            Text(页面.编辑日期)
                                                .font(.system(size: 10, design: .monospaced))
                                                .foregroundColor(霓虹蓝.opacity(0.5))
                                        }
                                        .padding(.horizontal, 10)
                                        .padding(.vertical, 8)
                                    }
                                }
                                .background(卡底)
                                .cornerRadius(8)
                                .overlay(RoundedRectangle(cornerRadius: 8).stroke(霓虹蓝.opacity(0.15), lineWidth: 1))
                                .padding(.horizontal, 16)
                            }
                        }
                        .padding(.bottom, 20)
                        .task { await 自动加载Notion() }

                        // MARK: - 文化双柱
                        VStack(alignment: .leading, spacing: 10) {
                            赛博标题("// 文化双柱", 副: "东方·西方", 颜色: 龍金)

                            HStack(spacing: 10) {
                                赛博文化柱(方位: "EAST", 人物: "曾仕强老师",
                                           理念: "中华文化 · 易经 · 中道", 图标: "☯", 边框色: 霓虹红)
                                赛博文化柱(方位: "WEST", 人物: "乔布斯前辈",
                                           理念: "极致产品 · 科技人文", 图标: "⌘", 边框色: 霓虹紫)
                            }
                            .padding(.horizontal, 16)
                        }
                        .padding(.bottom, 20)

                        // MARK: - 铁律
                        VStack(alignment: .leading, spacing: 8) {
                            赛博标题("// 铁律", 副: "P0·不可改", 颜色: 霓虹)

                            VStack(spacing: 0) {
                                赛博铁律行("为人民服务",       图标: "heart.fill",         颜色: 霓虹红)
                                赛博铁律行("不作恶",           图标: "shield.fill",        颜色: 霓虹)
                                赛博铁律行("不站队",           图标: "scale.3d",           颜色: 霓虹蓝)
                                赛博铁律行("不收割",           图标: "hand.raised.fill",   颜色: 霓虹)
                                赛博铁律行("不取代 · 只赋能",  图标: "arrow.triangle.branch", 颜色: 霓虹紫)
                                赛博铁律行("每个国家的文化都值得尊重", 图标: "globe",      颜色: 霓虹蓝)
                                赛博铁律行("DNA是每个人的盾",  图标: "lock.shield.fill",   颜色: 龍金)
                            }
                            .background(卡底)
                            .cornerRadius(10)
                            .overlay(RoundedRectangle(cornerRadius: 10).stroke(霓虹.opacity(0.12), lineWidth: 1))
                            .padding(.horizontal, 16)
                        }
                        .padding(.bottom, 20)

                        // MARK: - 北辰协议
                        NavigationLink(destination: 北辰协议View()) {
                            HStack(spacing: 10) {
                                Text("☆")
                                    .font(.system(size: 16))
                                    .foregroundColor(龍金)
                                VStack(alignment: .leading, spacing: 2) {
                                    Text("北辰·母协议")
                                        .font(.system(size: 13, weight: .bold, design: .monospaced))
                                        .foregroundColor(.white)
                                    Text("P0-ETERNAL · 最高宪法 · AI伦理边界")
                                        .font(.system(size: 10, design: .monospaced))
                                        .foregroundColor(龍金.opacity(0.5))
                                }
                                Spacer()
                                Image(systemName: "chevron.right")
                                    .font(.system(size: 11))
                                    .foregroundColor(龍金.opacity(0.4))
                            }
                            .padding(12)
                            .background(龍金.opacity(0.05))
                            .cornerRadius(10)
                            .overlay(RoundedRectangle(cornerRadius: 10).stroke(龍金.opacity(0.2), lineWidth: 1))
                            .shadow(color: 龍金.opacity(0.1), radius: 6)
                        }
                        .padding(.horizontal, 16)
                        .padding(.bottom, 20)

                        // MARK: - 系统信息（折叠）
                        DisclosureGroup(isExpanded: $显示版本信息) {
                            VStack(spacing: 0) {
                                身份条(键: "创始人", 值: "诸葛鑫（UID9622）")
                                身份条(键: "理论指导", 值: "曾仕强老师")
                                身份条(键: "DNA", 值: "#龍芯⚡️YYYY-MM-DD-模块-vX.Y")
                                身份条(键: "版本", 值: "v1.3 生态入口")
                                身份条(键: "使命", 值: "技术普惠 · 创作赋能 · 数字主权")
                            }
                            .background(卡底)
                            .cornerRadius(8)
                            .overlay(RoundedRectangle(cornerRadius: 8).stroke(霓虹.opacity(0.1), lineWidth: 1))
                            .padding(.top, 6)
                        } label: {
                            HStack(spacing: 6) {
                                Image(systemName: "terminal")
                                    .font(.system(size: 11))
                                    .foregroundColor(霓虹.opacity(0.4))
                                Text("SYS_INFO")
                                    .font(.system(size: 11, design: .monospaced))
                                    .foregroundColor(霓虹.opacity(0.4))
                            }
                        }
                        .accentColor(霓虹.opacity(0.4))
                        .padding(.horizontal, 16)
                        .padding(.bottom, 20)

                        // MARK: - 底部签名
                        VStack(spacing: 4) {
                            Text("诸葛鑫 · UID9622 · 献礼祖国七十七周年")
                                .font(.system(size: 10, design: .monospaced))
                                .foregroundColor(.white.opacity(0.2))
                            Text("#龍芯⚡️2026-03-20-PORTAL-CYBER-v5.0")
                                .font(.system(size: 9, design: .monospaced))
                                .foregroundColor(霓虹.opacity(0.15))
                        }
                        .padding(.bottom, 40)
                    }
                }
            }
            .toolbar(.hidden, for: .navigationBar)
        }
    }

    private var 生态数量: Int { 4 }
}

// MARK: - 赛博标题

private struct 赛博标题: View {
    let 主: String
    let 副: String
    let 颜色: Color
    init(_ 主: String, 副: String, 颜色: Color) {
        self.主 = 主; self.副 = 副; self.颜色 = 颜色
    }
    var body: some View {
        HStack(alignment: .bottom, spacing: 8) {
            Text(主)
                .font(.system(size: 12, weight: .bold, design: .monospaced))
                .foregroundColor(颜色)
            Text(副)
                .font(.system(size: 10, design: .monospaced))
                .foregroundColor(颜色.opacity(0.4))
            Spacer()
        }
        .padding(.horizontal, 16)
    }
}

// MARK: - 赛博大卡

private struct 赛博大卡: View {
    let 图标: String
    let 标题: String
    let 说明: String
    let 标签: String
    let 边框色: Color

    private let 卡底 = Color(red: 0.05, green: 0.05, blue: 0.12)

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(图标).font(.system(size: 24))
                Spacer()
                Text(标签)
                    .font(.system(size: 8, weight: .bold, design: .monospaced))
                    .foregroundColor(边框色)
                    .padding(.horizontal, 5)
                    .padding(.vertical, 2)
                    .background(边框色.opacity(0.1))
                    .cornerRadius(3)
                    .overlay(RoundedRectangle(cornerRadius: 3).stroke(边框色.opacity(0.3), lineWidth: 0.5))
            }

            Text(标题)
                .font(.system(size: 14, weight: .bold))
                .foregroundColor(.white)

            Text(说明)
                .font(.system(size: 11))
                .foregroundColor(.white.opacity(0.45))

            Spacer(minLength: 0)

            HStack {
                Spacer()
                Image(systemName: "arrow.right")
                    .font(.system(size: 10))
                    .foregroundColor(边框色.opacity(0.5))
            }
        }
        .padding(12)
        .frame(maxWidth: .infinity, minHeight: 116, maxHeight: 116, alignment: .topLeading)
        .background(卡底)
        .cornerRadius(12)
        .overlay(RoundedRectangle(cornerRadius: 12).stroke(边框色.opacity(0.4), lineWidth: 1))
        .shadow(color: 边框色.opacity(0.15), radius: 8, x: 0, y: 0)
    }
}

// MARK: - 赛博工具条

private struct 赛博工具条: View {
    let 图标: String
    let 标题: String
    let 说明: String
    let 点色: Color

    private let 卡底 = Color(red: 0.05, green: 0.05, blue: 0.12)

    var body: some View {
        HStack(spacing: 10) {
            Rectangle()
                .fill(点色)
                .frame(width: 2)
                .shadow(color: 点色.opacity(0.6), radius: 4)

            Text(图标).font(.system(size: 18)).frame(width: 26)

            VStack(alignment: .leading, spacing: 2) {
                Text(标题)
                    .font(.system(size: 13, weight: .semibold))
                    .foregroundColor(.white)
                Text(说明)
                    .font(.system(size: 11))
                    .foregroundColor(.white.opacity(0.4))
            }
            Spacer()
            Image(systemName: "chevron.right")
                .font(.system(size: 10))
                .foregroundColor(点色.opacity(0.4))
        }
        .padding(.vertical, 10)
        .padding(.horizontal, 12)
        .background(卡底)
        .cornerRadius(10)
        .overlay(RoundedRectangle(cornerRadius: 10).stroke(点色.opacity(0.2), lineWidth: 1))
    }
}

// MARK: - 赛博文化柱

private struct 赛博文化柱: View {
    let 方位: String
    let 人物: String
    let 理念: String
    let 图标: String
    let 边框色: Color

    private let 卡底 = Color(red: 0.05, green: 0.05, blue: 0.12)

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(图标).font(.system(size: 18))
                Spacer()
                Text(方位)
                    .font(.system(size: 8, weight: .bold, design: .monospaced))
                    .foregroundColor(边框色)
                    .padding(.horizontal, 5).padding(.vertical, 2)
                    .background(边框色.opacity(0.1))
                    .cornerRadius(3)
            }
            Text(人物)
                .font(.system(size: 12, weight: .bold))
                .foregroundColor(.white)
            Text(理念)
                .font(.system(size: 10))
                .foregroundColor(.white.opacity(0.4))
                .fixedSize(horizontal: false, vertical: true)
        }
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .topLeading)
        .background(卡底)
        .cornerRadius(10)
        .overlay(RoundedRectangle(cornerRadius: 10).stroke(边框色.opacity(0.3), lineWidth: 1))
        .shadow(color: 边框色.opacity(0.1), radius: 6)
    }
}

// MARK: - 赛博铁律行

private struct 赛博铁律行: View {
    let 文字: String
    let 图标: String
    let 颜色: Color
    init(_ 文字: String, 图标: String, 颜色: Color) {
        self.文字 = 文字; self.图标 = 图标; self.颜色 = 颜色
    }
    var body: some View {
        HStack(spacing: 10) {
            Image(systemName: 图标)
                .font(.system(size: 10))
                .foregroundColor(颜色.opacity(0.7))
                .frame(width: 18)
                .shadow(color: 颜色.opacity(0.4), radius: 3)
            Text(文字)
                .font(.system(size: 12))
                .foregroundColor(.white.opacity(0.7))
            Spacer()
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 7)
        .overlay(
            Rectangle().fill(Color.white.opacity(0.04)).frame(height: 0.5),
            alignment: .bottom
        )
    }
}

// MARK: - 身份条

private struct 身份条: View {
    let 键: String
    let 值: String
    var body: some View {
        HStack {
            Text(键)
                .font(.system(size: 10, design: .monospaced))
                .foregroundColor(.white.opacity(0.3))
                .frame(width: 64, alignment: .leading)
            Text(值)
                .font(.system(size: 10, design: .monospaced))
                .foregroundColor(.white.opacity(0.6))
                .lineLimit(1)
                .minimumScaleFactor(0.7)
            Spacer()
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 7)
        .overlay(
            Rectangle().fill(Color.white.opacity(0.04)).frame(height: 0.5),
            alignment: .bottom
        )
    }
}

// MARK: - Notion 搜索 & 看板逻辑

extension ContentView {
    private static let API基地址 = "http://192.168.100.253"

    func 加载Notion看板() {
        Task { await 自动加载Notion() }
    }

    func 自动加载Notion() async {
        guard !notion加载中 else { return }
        notion加载中 = true
        defer { notion加载中 = false }
        guard let url = URL(string: "\(Self.API基地址):9622/notion/pages") else { return }
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
               let pages = json["pages"] as? [[String: Any]] {
                notion看板列表 = pages.compactMap { p in
                    guard let id = p["id"] as? String,
                          let title = p["title"] as? String else { return nil }
                    let emoji = p["emoji"] as? String ?? "📄"
                    let edited = (p["last_edited"] as? String ?? "").prefix(10)
                    let url = p["url"] as? String ?? ""
                    return NotionPageItem(id: id, emoji: emoji, 标题: title,
                                         编辑日期: String(edited), url: url)
                }
            }
        } catch { }
    }

    func 执行搜索() {
        let 关键词 = 搜索词.trimmingCharacters(in: .whitespaces)
        guard !关键词.isEmpty else { return }
        正在搜索 = true
        搜索结果 = []
        guard let url = URL(string: "\(Self.API基地址):8765/查询Notion") else {
            正在搜索 = false; return
        }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try? JSONSerialization.data(withJSONObject: ["关键词": 关键词])
        Task {
            defer { 正在搜索 = false }
            do {
                let (data, _) = try await URLSession.shared.data(for: request)
                if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                   let 页面列表 = json["页面列表"] as? [[String: Any]] {
                    搜索结果 = 页面列表.map { item in
                        let 原始时间 = item["最后编辑"] as? String ?? ""
                        return NotionPage(id: item["ID"] as? String ?? UUID().uuidString,
                                         标题: item["标题"] as? String ?? "",
                                         链接: item["URL"] as? String ?? "",
                                         编辑日期: String(原始时间.prefix(10)))
                    }
                }
            } catch { }
        }
    }
}

// MARK: - 数据模型

struct NotionPage: Identifiable {
    let id: String
    let 标题: String
    let 链接: String
    let 编辑日期: String
}

struct NotionPageItem: Identifiable {
    let id: String
    let emoji: String
    let 标题: String
    let 编辑日期: String
    let url: String
}

// MARK: - Notion页面卡片

private struct NotionPageCard: View {
    let 页面: NotionPageItem
    let 霓虹蓝: Color
    let 卡底: Color

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(页面.emoji)
                    .font(.system(size: 22))
                Spacer()
                Text("NOTION")
                    .font(.system(size: 7, weight: .bold, design: .monospaced))
                    .foregroundColor(霓虹蓝.opacity(0.5))
                    .padding(.horizontal, 4)
                    .padding(.vertical, 2)
                    .background(霓虹蓝.opacity(0.07))
                    .cornerRadius(3)
            }
            Text(页面.标题)
                .font(.system(size: 11, weight: .semibold))
                .foregroundColor(.white.opacity(0.85))
                .lineLimit(2)
                .fixedSize(horizontal: false, vertical: true)
            Spacer(minLength: 0)
            HStack(spacing: 4) {
                Circle().fill(霓虹蓝.opacity(0.4)).frame(width: 4, height: 4)
                Text(页面.编辑日期)
                    .font(.system(size: 9, design: .monospaced))
                    .foregroundColor(霓虹蓝.opacity(0.45))
            }
        }
        .padding(10)
        .frame(width: 140, height: 110, alignment: .topLeading)
        .background(卡底)
        .cornerRadius(10)
        .overlay(RoundedRectangle(cornerRadius: 10).stroke(霓虹蓝.opacity(0.25), lineWidth: 1))
        .shadow(color: 霓虹蓝.opacity(0.1), radius: 6)
    }
}

#Preview {
    ContentView()
}
