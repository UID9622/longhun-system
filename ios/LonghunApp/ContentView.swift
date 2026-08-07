// DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-IOS-CONTENT-v1.0-UID9622
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 创建者: 诸葛鑫（UID9622）
//
// 龍魂 iOS 主界面 · 仪表盘 · 记忆图谱 · 监督日志 · 设置

import SwiftUI

struct ContentView: View {
    @EnvironmentObject var appState: LonghunAppState
    
    var body: some View {
        TabView {
            DashboardView()
                .tabItem {
                    Label("仪表盘", systemImage: "gauge.with.dots.needle.33percent")
                }
            
            MemoryGraphView()
                .tabItem {
                    Label("记忆图谱", systemImage: "brain.head.profile")
                }
            
            SupervisionLogView()
                .tabItem {
                    Label("监督日志", systemImage: "list.bullet.clipboard")
                }
            
            SettingsView()
                .tabItem {
                    Label("设置", systemImage: "gear")
                }
        }
        .tint(.orange)
    }
}

// MARK: - 仪表盘

struct DashboardView: View {
    @EnvironmentObject var appState: LonghunAppState
    @State private var animateGauge: Bool = false
    
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 20) {
                    // 状态卡片
                    StatusCard(status: appState.healthStatus)
                    
                    // 环形评分
                    ScoreRing(score: appState.lastReport?.score ?? 0)
                        .frame(width: 160, height: 160)
                    
                    // 快捷操作
                    QuickActions(appState: appState)
                }
                .padding()
            }
            .navigationTitle("龍魂 · 仪表盘")
            .onAppear {
                withAnimation(.easeOut(duration: 1.5)) {
                    animateGauge = true
                }
            }
        }
    }
}

struct StatusCard: View {
    let status: String
    
    var body: some View {
        HStack {
            Image(systemName: iconName)
                .font(.largeTitle)
                .foregroundColor(iconColor)
            VStack(alignment: .leading) {
                Text("系统状态")
                    .font(.caption)
                    .foregroundColor(.secondary)
                Text(status)
                    .font(.headline)
            }
            Spacer()
        }
        .padding()
        .background(
            RoundedRectangle(cornerRadius: 12)
                .fill(Color(.systemBackground))
                .shadow(color: .black.opacity(0.1), radius: 4, y: 2)
        )
    }
    
    private var iconName: String {
        status.contains("🟢") ? "checkmark.shield.fill" :
        status.contains("🟡") ? "exclamationmark.shield.fill" :
        status.contains("🔴") ? "xmark.shield.fill" :
        "shield.lefthalf.filled"
    }
    
    private var iconColor: Color {
        status.contains("🟢") ? .green :
        status.contains("🟡") ? .orange :
        status.contains("🔴") ? .red :
        .blue
    }
}

struct ScoreRing: View {
    let score: Double
    
    var body: some View {
        ZStack {
            Circle()
                .stroke(Color.secondary.opacity(0.2), lineWidth: 12)
            Circle()
                .trim(from: 0, to: score / 100.0)
                .stroke(
                    score >= 80 ? Color.green :
                    score >= 50 ? Color.orange : Color.red,
                    style: StrokeStyle(lineWidth: 12, lineCap: .round)
                )
                .rotationEffect(.degrees(-90))
                .animation(.easeOut(duration: 1.5), value: score)
            VStack {
                Text("\(Int(score))")
                    .font(.title.bold())
                Text("分")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
    }
}

struct QuickActions: View {
    @ObservedObject var appState: LonghunAppState
    
    var body: some View {
        VStack(spacing: 12) {
            Button(action: {
                Task {
                    await appState.runBackgroundSupervision()
                }
            }) {
                Label("立即监督", systemImage: "play.fill")
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 10)
                            .fill(Color.orange)
                    )
                    .foregroundColor(.white)
            }
            .disabled(appState.isSupervisionRunning)
        }
    }
}

// MARK: - 记忆图谱

struct MemoryGraphView: View {
    @EnvironmentObject var appState: LonghunAppState
    @State private var searchText: String = ""
    @State private var memories: [MemoryEntry] = []
    
    var body: some View {
        NavigationStack {
            List {
                if memories.isEmpty {
                    ContentUnavailableView(
                        "记忆图谱",
                        systemImage: "brain.head.profile",
                        description: Text("暂无记忆条目")
                    )
                } else {
                    ForEach(memories) { memory in
                        MemoryRow(memory: memory)
                    }
                }
            }
            .searchable(text: $searchText)
            .navigationTitle("记忆图谱")
        }
    }
}

struct MemoryRow: View {
    let memory: MemoryEntry
    
    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack {
                PriorityBadge(priority: memory.priority)
                if memory.frozen {
                    Image(systemName: "snowflake")
                        .foregroundColor(.blue)
                }
                Spacer()
                Text(memory.id.prefix(8))
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
            Text(memory.content)
                .font(.body)
                .lineLimit(3)
            HStack {
                ForEach(memory.tags.prefix(3), id: \.self) { tag in
                    Text(tag)
                        .font(.caption2)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color.secondary.opacity(0.15))
                        .cornerRadius(4)
                }
            }
        }
    }
}

struct PriorityBadge: View {
    let priority: MemoryPriority
    
    var body: some View {
        Text(priority.rawValue)
            .font(.caption.bold())
            .padding(.horizontal, 6)
            .padding(.vertical, 2)
            .background(priorityColor.opacity(0.2))
            .foregroundColor(priorityColor)
            .cornerRadius(4)
    }
    
    var priorityColor: Color {
        switch priority {
        case .P0: return .red
        case .P1: return .orange
        case .P2: return .blue
        case .P3: return .gray
        }
    }
}

// MARK: - 监督日志

struct SupervisionLogView: View {
    @EnvironmentObject var appState: LonghunAppState
    
    var body: some View {
        NavigationStack {
            List {
                if let report = appState.lastReport {
                    Section("最近监督") {
                        LabeledContent("评分", value: "\(Int(report.score))/100")
                        LabeledContent("审计", value: report.audit.rawValue)
                        LabeledContent("DNA", value: report.dnaValid ? "✅" : "❌")
                        LabeledContent("时间", value: report.timestamp)
                    }
                    
                    if !report.deviations.isEmpty {
                        Section("偏差") {
                            ForEach(report.deviations.indices, id: \.self) { i in
                                let d = report.deviations[i]
                                VStack(alignment: .leading) {
                                    Text(d.field).bold()
                                    Text("期望: \(d.expected)")
                                    Text("实际: \(d.actual)")
                                }
                                .font(.caption)
                            }
                        }
                    }
                } else {
                    ContentUnavailableView(
                        "监督日志",
                        systemImage: "list.bullet.clipboard",
                        description: Text("尚未执行监督")
                    )
                }
            }
            .navigationTitle("监督日志")
        }
    }
}

// MARK: - 设置

struct SettingsView: View {
    @AppStorage("autoSupervision") private var autoSupervision = true
    @AppStorage("supervisionInterval") private var supervisionInterval = 30.0
    @AppStorage("sensitivity") private var sensitivity = 0.7
    
    var body: some View {
        NavigationStack {
            Form {
                Section("监督") {
                    Toggle("自动监督", isOn: $autoSupervision)
                    HStack {
                        Text("间隔")
                        Spacer()
                        Text("\(Int(supervisionInterval)) 分钟")
                            .foregroundColor(.secondary)
                    }
                    VStack {
                        HStack {
                            Text("灵敏度")
                            Spacer()
                            Text(String(format: "%.1f", sensitivity))
                                .foregroundColor(.secondary)
                        }
                        Slider(value: $sensitivity, in: 0.1...1.0, step: 0.1)
                    }
                }
                
                Section("关于") {
                    LabeledContent("DNA", value: "#龍芯⚡️丙午·丙申·庚戌·䷙大畜")
                    LabeledContent("创建者", value: "诸葛鑫（UID9622）")
                    LabeledContent("许可", value: "MulanPSL v2")
                }
            }
            .navigationTitle("设置")
        }
    }
}
