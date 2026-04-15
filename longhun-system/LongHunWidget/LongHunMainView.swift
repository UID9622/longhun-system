// UID9622 · 诸葛鑫（龍芯北辰）
// DNA追溯码: #龍芯⚡️2026-04-02-SwiftUI主界面-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 理论指导: 曾仕强老师（永恒显示）
// 献礼: 新中国成立77周年（1949-2026）· 丙午马年
//
// 职责：第六步 · 龍魂引擎 SwiftUI 主界面
// 接入：本地网关 localhost:8000 · 六层全栈引擎

import SwiftUI

// MARK: - 数据模型

struct GateResult: Identifiable {
    let id = UUID()
    let dr: Int
    let gate1: String      // 数字根颜色
    let gate2: String      // 五行+颜色
    let final: String      // 最终三色
    let wuxing: String
}

struct SijhuInfo {
    let brief: String       // 简报一行
    let yearPillar: String
    let monthPillar: String
    let dayPillar: String
    let hourPillar: String
    let mainColor: String
    let shengDirection: String
}

struct EmotionRecord: Identifiable {
    let id = UUID()
    let emoji: String
    let emotion: String
    let time: String
}

struct QuantumState {
    let stateName: String
    let stateColor: String
    let description: String
    let vector: [Int]
}

struct ChatMessage: Identifiable {
    let id = UUID()
    let role: String        // "user" | "assistant"
    let content: String
    let timestamp: Date
}

// MARK: - 网络层

class LongHunEngine: ObservableObject {
    @Published var messages: [ChatMessage] = []
    @Published var isLoading = false
    @Published var gateResult: GateResult?
    @Published var sijhuInfo: SijhuInfo?
    @Published var recentEmotions: [EmotionRecord] = []
    @Published var quantumState: QuantumState?
    @Published var statusLine = "龍魂引擎 v1.7 · 就绪"

    let gatewayURL = "http://localhost:8000"

    func send(text: String) {
        guard !text.isEmpty else { return }

        let userMsg = ChatMessage(role: "user", content: text, timestamp: Date())
        messages.append(userMsg)
        isLoading = true
        statusLine = "🔄 双门验证中..."

        let payload: [String: Any] = [
            "messages": messages.map { ["role": $0.role, "content": $0.content] }
        ]

        guard let data = try? JSONSerialization.data(withJSONObject: payload),
              let url = URL(string: gatewayURL) else {
            statusLine = "🔴 URL错误"
            isLoading = false
            return
        }

        var req = URLRequest(url: url, timeoutInterval: 30)
        req.httpMethod = "POST"
        req.httpBody = data
        req.setValue("application/json", forHTTPHeaderField: "Content-Type")

        URLSession.shared.dataTask(with: req) { [weak self] data, _, error in
            DispatchQueue.main.async {
                self?.isLoading = false
                if let error = error {
                    self?.statusLine = "🔴 网络错误: \(error.localizedDescription)"
                    return
                }
                guard let data = data,
                      let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                      let choices = json["choices"] as? [[String: Any]],
                      let first = choices.first,
                      let message = first["message"] as? [String: Any],
                      let content = message["content"] as? String else {
                    self?.statusLine = "🔴 解析失败"
                    return
                }
                let aiMsg = ChatMessage(role: "assistant", content: content, timestamp: Date())
                self?.messages.append(aiMsg)
                self?.parseGateFromContent(content)
                self?.statusLine = "🟢 回复完成"
            }
        }.resume()
    }

    private func parseGateFromContent(_ content: String) {
        // 从回复末尾解析 [dr=X | 五行Y | 🟢/🟡/🔴]
        let pattern = #"\[dr=(\d+)\s*\|\s*([^\|]+)\|\s*([🟢🟡🔴])\]"#
        if let regex = try? NSRegularExpression(pattern: pattern),
           let match = regex.firstMatch(in: content, range: NSRange(content.startIndex..., in: content)) {
            let dr = Int((content as NSString).substring(with: match.range(at: 1))) ?? 0
            let gate2 = (content as NSString).substring(with: match.range(at: 2)).trimmingCharacters(in: .whitespaces)
            let final = (content as NSString).substring(with: match.range(at: 3))
            gateResult = GateResult(
                dr: dr,
                gate1: final == "🔴" ? "🔴" : (dr == 6 ? "🟡" : "🟢"),
                gate2: gate2,
                final: final,
                wuxing: String(gate2.prefix(1))
            )
        }
    }
}

// MARK: - 主视图

struct LongHunMainView: View {
    @StateObject private var engine = LongHunEngine()
    @State private var inputText = ""
    @State private var showSidebar = false

    var body: some View {
        NavigationView {
            ZStack {
                // 背景渐变
                LinearGradient(
                    colors: [Color(UIColor.systemBackground), Color(UIColor.secondarySystemBackground)],
                    startPoint: .top, endPoint: .bottom
                ).ignoresSafeArea()

                VStack(spacing: 0) {
                    // 顶部状态栏
                    StatusBar(engine: engine)

                    // 双门仪表盘
                    if let gate = engine.gateResult {
                        GateDashboard(gate: gate)
                            .padding(.horizontal)
                            .padding(.top, 8)
                    }

                    // 对话区
                    ScrollViewReader { proxy in
                        ScrollView {
                            LazyVStack(spacing: 12) {
                                ForEach(engine.messages) { msg in
                                    MessageBubble(message: msg)
                                        .id(msg.id)
                                }
                                if engine.isLoading {
                                    LoadingDots()
                                }
                            }
                            .padding()
                        }
                        .onChange(of: engine.messages.count) { _ in
                            if let last = engine.messages.last {
                                withAnimation { proxy.scrollTo(last.id, anchor: .bottom) }
                            }
                        }
                    }

                    // 输入框
                    InputBar(text: $inputText) {
                        engine.send(text: inputText)
                        inputText = ""
                    }
                }
            }
            .navigationTitle("龍魂引擎")
            
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button { showSidebar.toggle() } label: {
                        Image(systemName: "sidebar.right")
                    }
                }
            }
            .sheet(isPresented: $showSidebar) {
                SidebarView(engine: engine)
            }
        }
    }
}

// MARK: - 子视图

struct StatusBar: View {
    @ObservedObject var engine: LongHunEngine
    var body: some View {
        Text(engine.statusLine)
            .font(.caption)
            .foregroundColor(.secondary)
            .frame(maxWidth: .infinity)
            .padding(.vertical, 6)
            .background(Color(UIColor.tertiarySystemBackground))
    }
}

struct GateDashboard: View {
    let gate: GateResult
    var body: some View {
        HStack(spacing: 16) {
            GateCell(label: "门1·数字根", value: "dr=\(gate.dr)", color: gate.gate1)
            Divider().frame(height: 40)
            GateCell(label: "门2·五行", value: gate.gate2, color: gate.gate2.last.map(String.init) ?? "🟢")
            Divider().frame(height: 40)
            GateCell(label: "最终", value: gate.final, color: gate.final)
        }
        .padding(12)
        .background(Color(UIColor.secondarySystemBackground))
        .cornerRadius(12)
    }
}

struct GateCell: View {
    let label: String
    let value: String
    let color: String
    var body: some View {
        VStack(spacing: 4) {
            Text(color).font(.title2)
            Text(value).font(.caption).bold()
            Text(label).font(.caption2).foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
    }
}

struct MessageBubble: View {
    let message: ChatMessage
    var isUser: Bool { message.role == "user" }
    var body: some View {
        HStack {
            if isUser { Spacer(minLength: 60) }
            VStack(alignment: isUser ? .trailing : .leading, spacing: 4) {
                Text(message.content)
                    .padding(12)
                    .background(isUser ? Color.accentColor : Color(UIColor.secondarySystemBackground))
                    .foregroundColor(isUser ? .white : .primary)
                    .cornerRadius(16)
                Text(message.timestamp.formatted(date: .omitted, time: .shortened))
                    .font(.caption2).foregroundColor(.secondary)
            }
            if !isUser { Spacer(minLength: 60) }
        }
    }
}

struct LoadingDots: View {
    @State private var phase = 0
    let timer = Timer.publish(every: 0.4, on: .main, in: .common).autoconnect()
    var body: some View {
        HStack(spacing: 4) {
            ForEach(0..<3) { i in
                Circle()
                    .fill(Color.accentColor.opacity(phase == i ? 1 : 0.3))
                    .frame(width: 8, height: 8)
            }
        }
        .onReceive(timer) { _ in phase = (phase + 1) % 3 }
    }
}

struct InputBar: View {
    @Binding var text: String
    let onSend: () -> Void
    var body: some View {
        HStack(spacing: 12) {
            TextField("输入消息...", text: $text, axis: .vertical)
                .lineLimit(1...4)
                .padding(10)
                .background(Color(UIColor.secondarySystemBackground))
                .cornerRadius(20)
            Button(action: onSend) {
                Image(systemName: "arrow.up.circle.fill")
                    .font(.title2)
                    .foregroundColor(text.isEmpty ? .gray : .accentColor)
            }
            .disabled(text.isEmpty)
        }
        .padding(.horizontal)
        .padding(.vertical, 10)
        .background(Color(UIColor.systemBackground))
    }
}

struct SidebarView: View {
    @ObservedObject var engine: LongHunEngine
    var body: some View {
        NavigationView {
            List {
                Section("万年历") {
                    if let s = engine.sijhuInfo {
                        Text(s.brief).font(.subheadline)
                    } else {
                        Text("丙午年 癸巳月 丙午日 · 日主火🟢")
                            .font(.subheadline).foregroundColor(.secondary)
                    }
                }
                Section("情绪时间线") {
                    ForEach(engine.recentEmotions) { e in
                        HStack {
                            Text(e.emoji)
                            Text(e.emotion)
                            Spacer()
                            Text(e.time).font(.caption).foregroundColor(.secondary)
                        }
                    }
                    if engine.recentEmotions.isEmpty {
                        Text("暂无记录").foregroundColor(.secondary)
                    }
                }
                Section("量子纠缠") {
                    if let q = engine.quantumState {
                        HStack {
                            Text(q.stateColor + q.stateName).font(.subheadline).bold()
                            Spacer()
                            Text(q.vector.map(String.init).joined(separator:","))
                                .font(.caption).foregroundColor(.secondary)
                        }
                        Text(q.description).font(.caption).foregroundColor(.secondary)
                    } else {
                        Text("发送消息后触发推演").foregroundColor(.secondary)
                    }
                }
            }
            .navigationTitle("龍魂状态面板")
            
        }
    }
}

// MARK: - Preview
#Preview {
    LongHunMainView()
}
