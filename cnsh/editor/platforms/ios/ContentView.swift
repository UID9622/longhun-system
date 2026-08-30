// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-e7e84a95
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
//龍芯⚡️2026-06-20-LONGHUN-DIARY-ContentView
// 主界面：农历日历 + 日记列表 + API控制台

import SwiftUI

struct ContentView: View {
    @State private var 选中标签 = 0
    
    var body: some View {
        TabView(selection: $选中标签) {
            农历日历视图()
                .tabItem { Label("日历", systemImage: "calendar") }
                .tag(0)
            日记本视图()
                .tabItem { Label("日记", systemImage: "book") }
                .tag(1)
            API控制台视图()
                .tabItem { Label("引擎", systemImage: "cpu") }
                .tag(2)
            数据主权视图()
                .tabItem { Label("主权", systemImage: "shield") }
                .tag(3)
        }
        .accentColor(.orange)
    }
}

// ═════ 农历日历视图 ═════
struct 农历日历视图: View {
    @State private var 当前日期 = Date()
    @State private var 选中日期: Date?
    @StateObject private var 农历引擎 = 农历引擎()
    
    var body: some View {
        NavigationView {
            VStack {
                // 年月标题
                Text("\(农历引擎.农历年月(当前日期))")
                    .font(.title2.bold())
                    .foregroundColor(.orange)
                
                // 星期标题
                HStack {
                    ForEach(["日","一","二","三","四","五","六"], id: \.self) { 日 in
                        Text(日).frame(maxWidth: .infinity).foregroundColor(.gray)
                    }
                }
                
                // 日期网格
                LazyVGrid(columns: Array(repeating: GridItem(.flexible()), count: 7)) {
                    ForEach(农历引擎.当月日期(当前日期), id: \.self) { 日期 in
                        日期格子(日期: 日期, 农历: 农历引擎.农历日(日期),
                                有日记: 农历引擎.该日有日记(日期),
                                选中: 选中日期 == 日期)
                        .onTapGesture { 选中日期 = 日期 }
                    }
                }
                
                Spacer()
                
                // 底部DNA
                Text(DNA追溯器.生成DNA(模块: "DIARY-CALENDAR", 版本: "v1.0"))
                    .font(.system(size: 8, design: .monospaced))
                    .foregroundColor(.gray.opacity(0.5))
            }
            .padding()
            .navigationTitle("龙魂农历")
        }
    }
}

struct 日期格子: View {
    let 日期: Date
    let 农历: String
    let 有日记: Bool
    let 选中: Bool
    
    var body: some View {
        VStack(spacing: 2) {
            Text("\(Calendar.current.component(.day, from: 日期))")
                .font(.system(size: 16, weight: .medium))
            Text(农历)
                .font(.system(size: 9))
                .foregroundColor(.gray)
            if 有日记 {
                Circle().fill(Color.orange).frame(width: 4, height: 4)
            }
        }
        .frame(height: 50)
        .background(选中 ? Color.orange.opacity(0.2) : Color.clear)
        .cornerRadius(8)
        .overlay(RoundedRectangle(cornerRadius: 8).stroke(选中 ? Color.orange : Color.clear, lineWidth: 1))
    }
}

// ═════ 日记本视图 ═════
struct 日记本视图: View {
    @Environment(\.managedObjectContext) private var 上下文
    @FetchRequest(sortDescriptors: [NSSortDescriptor(keyPath: \日记条目.时间戳, ascending: false)])
    private var 日记列表: FetchedResults<日记条目>
    @State private var 显示编辑器 = false
    
    var body: some View {
        NavigationView {
            List {
                ForEach(日记列表) { 条目 in
                    日记卡片(条目: 条目)
                }
            }
            .listStyle(.plain)
            .navigationTitle("日记本")
            .toolbar {
                Button(action: { 显示编辑器 = true }) {
                    Image(systemName: "plus.circle.fill").font(.title2)
                }
            }
            .sheet(isPresented: $显示编辑器) {
                日记编辑器()
            }
        }
    }
}

struct 日记卡片: View {
    let 条目: 日记条目
    
    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Text(条目.农历日期 ?? "")
                    .font(.caption.bold())
                    .foregroundColor(.orange)
                Spacer()
                Text(条目.时间戳?.formatted(date: .abbreviated, time: .shortened) ?? "")
                    .font(.caption2).foregroundColor(.gray)
            }
            Text(条目.内容 ?? "")
                .font(.body)
                .lineLimit(3)
            HStack {
                Text("🟢").font(.caption) // 三色审计
                Text(条目.dna追溯 ?? "").font(.system(size: 7, design: .monospaced))
                    .foregroundColor(.gray.opacity(0.5))
                    .lineLimit(1)
            }
        }
        .padding(.vertical, 4)
    }
}

// ═════ API控制台视图 ═════
struct API控制台视图: View {
    @StateObject private var 路由器 = API路由器()
    @State private var 输入文本 = ""
    @State private var 语音输入中 = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 12) {
                // API状态
                HStack(spacing: 12) {
                    API状态灯(名称: "Kimi", 状态: 路由器.kimi状态)
                    API状态灯(名称: "DeepSeek", 状态: 路由器.deepSeek状态)
                    API状态灯(名称: "本地", 状态: .在线)
                }
                
                // 输入区
                TextEditor(text: $输入文本)
                    .frame(height: 100)
                    .overlay(RoundedRectangle(cornerRadius: 8).stroke(Color.orange.opacity(0.3)))
                
                HStack {
                    Button(action: { 语音输入中.toggle() }) {
                        Label(语音输入中 ? "🎙️ 录音中" : "🎤 语音", systemImage: "mic")
                            .foregroundColor(语音输入中 ? .red : .orange)
                    }
                    Spacer()
                    Button("Kimi") { 路由器.调用Kimi(输入文本) }
                        .buttonStyle(.borderedProminent).tint(.blue)
                    Button("DeepSeek") { 路由器.调用DeepSeek(输入文本) }
                        .buttonStyle(.borderedProminent).tint(.green)
                }
                
                // 响应区
                ScrollView {
                    Text(路由器.最后响应)
                        .font(.body)
                        .padding()
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(Color(.systemGray6))
                        .cornerRadius(8)
                }
                
                Spacer()
                
                Text("数据主权：本地优先 · 平台不留原文 · 只留DNA指纹")
                    .font(.caption).foregroundColor(.gray)
            }
            .padding()
            .navigationTitle("API引擎")
        }
    }
}

struct API状态灯: View {
    let 名称: String
    let 状态: API状态
    
    var body: some View {
        HStack(spacing: 4) {
            Circle().fill(状态 == .在线 ? Color.green : Color.gray).frame(width: 6, height: 6)
            Text(名称).font(.caption)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 4)
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

enum API状态 { case 在线, 离线 }

// ═════ 数据主权视图 ═════
struct 数据主权视图: View {
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Image(systemName: "shield.lefthalf.fill").font(.system(size: 60)).foregroundColor(.orange)
                
                Text("数据主权声明").font(.title.bold())
                
                VStack(alignment: .leading, spacing: 12) {
                    主权条款(icon: "📱", 标题: "本地存储", 内容: "所有日记存储在设备本地，不经过云端")
                    主权条款(icon: "🔒", 标题: "端侧加密", 内容: "AES-256加密，密钥在Secure Enclave")
                    主权条款(icon: "🧬", 标题: "DNA追溯", 内容: "每条记录有不可篡改的DNA指纹")
                    主权条款(icon: "👤", 标题: "你的数据", 内容: "平台只留压缩DNA，原文永远属于你")
                    主权条款(icon: "🚫", 标题: "不可删除", 内容: "记录一旦写入，不可覆盖不可篡改")
                }
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(12)
                
                Text(DNA追溯器.生成DNA(模块: "DIARY-SOVEREIGNTY", 版本: "v1.0"))
                    .font(.system(size: 8, design: .monospaced))
                    .foregroundColor(.gray.opacity(0.5))
                    .padding(.top)
                
                Spacer()
            }
            .padding()
            .navigationTitle("数据主权")
        }
    }
}

struct 主权条款: View {
    let icon: String, 标题: String, 内容: String
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Text(icon).font(.title3)
            VStack(alignment: .leading, spacing: 2) {
                Text(标题).font(.subheadline.bold())
                Text(内容).font(.caption).foregroundColor(.gray)
            }
        }
    }
}
