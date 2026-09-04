// 龍魂9622·iOS Swift 伴侣应用 · v1.0
// DNA(v∞): #龍芯⚡️丙午·丁酉·辛巳-LONGHUN-EXT-IOS-SWIFT-v1.0-5d9c1e7a
// 创建者: 诸葛鑫（UID9622） · 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
// 文件: LonghunApp.swift
//
// 功能：
//   · 连接 Mac 上的 9622 引擎（同一 WiFi）
//   · ARKit 空间覆盖层（选中文本 → AR标注）
//   · 本地语音输入（AVFoundation + Speech）
//   · 三色审计结果可视化
//
// 依赖：Xcode 15+, iOS 17+, Swift 5.9
// 权限（Info.plist）：
//   NSMicrophoneUsageDescription
//   NSSpeechRecognitionUsageDescription
//   NSCameraUsageDescription（ARKit）

import SwiftUI
import ARKit
import Speech
import AVFoundation

// ─── 配置 ──────────────────────────────────────────────────
struct Config {
    // 替换为您 Mac 的局域网 IP（在 Mac 终端运行 `ipconfig getifaddr en0` 获取）
    static let engineHost = "http://192.168.1.100:9622"
    static let uid        = "UID9622"
}

// ─── 主入口 ────────────────────────────────────────────────
@main
struct LonghunApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

// ─── 主视图 ────────────────────────────────────────────────
struct ContentView: View {
    @StateObject private var engine = EngineClient()
    @State private var inputText  = ""
    @State private var showAR     = false
    @State private var isVoice    = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 16) {

                // ── 状态栏 ──
                HStack {
                    Image(systemName: "dragonhead")
                        .foregroundColor(.yellow)
                    Text("龍魂9622")
                        .font(.headline)
                    Spacer()
                    StatusBadge(online: engine.isOnline)
                }
                .padding(.horizontal)

                // ── 输入区 ──
                HStack {
                    TextField("输入文字或语音...", text: $inputText, axis: .vertical)
                        .lineLimit(3...6)
                        .textFieldStyle(.roundedBorder)

                    Button {
                        isVoice ? engine.stopVoice() : engine.startVoice { t in
                            inputText = t
                        }
                        isVoice.toggle()
                    } label: {
                        Image(systemName: isVoice ? "stop.circle.fill" : "mic.circle.fill")
                            .font(.title2)
                            .foregroundColor(isVoice ? .red : .yellow)
                    }
                }
                .padding(.horizontal)

                // ── 功能按钮 ──
                LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 10) {
                    EngineButton("⚖️ 伦理审查", color: .orange) {
                        engine.call(endpoint: "/api/ethics/review", text: inputText)
                    }
                    EngineButton("🟡 通心译", color: .yellow) {
                        engine.call(endpoint: "/api/tongxin/translate", text: inputText)
                    }
                    EngineButton("🔥 五行分析", color: .red) {
                        engine.call(endpoint: "/api/wuxing/analyze", text: inputText)
                    }
                    EngineButton("📐 CNSH语法", color: .blue) {
                        engine.call(endpoint: "/api/cnsh/align", text: inputText)
                    }
                }
                .padding(.horizontal)

                // ── 结果展示 ──
                if let result = engine.lastResult {
                    ResultCard(result: result)
                        .padding(.horizontal)
                }

                Spacer()

                // ── AR 按钮 ──
                Button {
                    showAR = true
                } label: {
                    Label("ARKit 空间覆盖层", systemImage: "arkit")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.black)
                        .foregroundColor(.yellow)
                        .cornerRadius(12)
                }
                .padding(.horizontal)
            }
            .navigationTitle("龍魂9622")
            .navigationBarTitleDisplayMode(.inline)
            .task { await engine.checkHealth() }
            .fullScreenCover(isPresented: $showAR) {
                ARView(result: engine.lastResult)
            }
        }
    }
}

// ─── 状态徽章 ──────────────────────────────────────────────
struct StatusBadge: View {
    let online: Bool
    var body: some View {
        HStack(spacing: 4) {
            Circle()
                .fill(online ? Color.green : Color.red)
                .frame(width: 8, height: 8)
            Text(online ? "引擎在线" : "引擎离线")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 4)
        .background(Color(.systemGray6))
        .cornerRadius(20)
    }
}

// ─── 功能按钮 ──────────────────────────────────────────────
struct EngineButton: View {
    let title: String
    let color: Color
    let action: () -> Void
    init(_ title: String, color: Color, action: @escaping () -> Void) {
        self.title = title; self.color = color; self.action = action
    }
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.subheadline)
                .frame(maxWidth: .infinity)
                .padding(10)
                .background(color.opacity(0.15))
                .foregroundColor(color)
                .cornerRadius(10)
                .overlay(RoundedRectangle(cornerRadius: 10).stroke(color.opacity(0.4)))
        }
    }
}

// ─── 结果卡片 ──────────────────────────────────────────────
struct ResultCard: View {
    let result: EngineResult
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(result.color)
                Text(result.title).font(.headline)
                Spacer()
            }
            Text(result.summary)
                .font(.body)
                .foregroundColor(.primary)
            if !result.dna.isEmpty {
                Text(result.dna)
                    .font(.caption2)
                    .foregroundColor(.secondary)
                    .monospaced()
            }
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

// ─── ARKit 覆盖层 ──────────────────────────────────────────
struct ARView: UIViewRepresentable {
    let result: EngineResult?
    func makeUIView(context: Context) -> ARSCNView {
        let arView = ARSCNView()
        let config = ARWorldTrackingConfiguration()
        config.planeDetection = [.horizontal, .vertical]
        arView.session.run(config)
        // 在空间中放置三色审计标注
        if let r = result {
            addTextNode(to: arView, text: "\(r.color) \(r.title)\n\(r.summary.prefix(80))")
        }
        return arView
    }
    func updateUIView(_ uiView: ARSCNView, context: Context) {}

    private func addTextNode(to arView: ARSCNView, text: String) {
        let textGeo = SCNText(string: text, extrusionDepth: 0.01)
        textGeo.font = UIFont.systemFont(ofSize: 0.04)
        textGeo.firstMaterial?.diffuse.contents = UIColor(red: 0.83, green: 0.69, blue: 0.22, alpha: 1)
        let node = SCNNode(geometry: textGeo)
        node.scale = SCNVector3(0.01, 0.01, 0.01)
        node.position = SCNVector3(0, 0, -0.5) // 0.5米前方
        arView.scene.rootNode.addChildNode(node)
    }
}

// ─── 引擎客户端 ────────────────────────────────────────────
struct EngineResult {
    let title:   String
    let color:   String
    let summary: String
    let dna:     String
}

@MainActor
class EngineClient: ObservableObject {
    @Published var isOnline    = false
    @Published var lastResult: EngineResult?

    private var speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "zh-CN"))
    private var recognitionTask:  SFSpeechRecognitionTask?
    private var audioEngine = AVAudioEngine()

    func checkHealth() async {
        guard let url = URL(string: "\(Config.engineHost)/api/health") else { return }
        do {
            let (_, resp) = try await URLSession.shared.data(from: url)
            isOnline = (resp as? HTTPURLResponse)?.statusCode == 200
        } catch {
            isOnline = false
        }
    }

    func call(endpoint: String, text: String) {
        guard let url = URL(string: "\(Config.engineHost)\(endpoint)") else { return }
        var req = URLRequest(url: url)
        req.httpMethod = "POST"
        req.setValue("application/json; charset=utf-8", forHTTPHeaderField: "Content-Type")
        req.httpBody = try? JSONEncoder().encode(["text": text, "lang": "zh"])

        Task {
            do {
                let (data, _) = try await URLSession.shared.data(for: req)
                if let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                    lastResult = EngineResult(
                        title:   json["title"]   as? String ?? "结果",
                        color:   json["color"]   as? String ?? "🟢",
                        summary: json["summary"] as? String ?? "",
                        dna:     json["dna"]     as? String ?? ""
                    )
                }
            } catch {
                lastResult = EngineResult(
                    title: "连接失败", color: "🔴",
                    summary: "请确认：\n1. Mac和iPhone在同一WiFi\n2. 引擎已启动(APPLE_MODE=true)\n3. Mac IP: \(Config.engineHost)",
                    dna: ""
                )
            }
        }
    }

    // ─── 语音输入（Apple Speech + AVFoundation） ────────────
    func startVoice(onResult: @escaping (String) -> Void) {
        SFSpeechRecognizer.requestAuthorization { status in
            guard status == .authorized else { return }
            DispatchQueue.main.async { self._startRecognition(onResult: onResult) }
        }
    }

    private func _startRecognition(onResult: @escaping (String) -> Void) {
        let request = SFSpeechAudioBufferRecognitionRequest()
        request.shouldReportPartialResults = true
        request.requiresOnDeviceRecognition = true  // 完全本地·不走网络

        let node = audioEngine.inputNode
        let fmt  = node.outputFormat(forBus: 0)
        node.installTap(onBus: 0, bufferSize: 1024, format: fmt) { buf, _ in
            request.append(buf)
        }
        try? audioEngine.start()

        recognitionTask = speechRecognizer?.recognitionTask(with: request) { result, err in
            if let r = result {
                onResult(r.bestTranscription.formattedString)
            }
        }
    }

    func stopVoice() {
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        recognitionTask?.cancel()
        recognitionTask = nil
    }
}
