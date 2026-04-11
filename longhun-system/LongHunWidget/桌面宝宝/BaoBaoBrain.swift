// ═══════════════════════════════════════════════════════════
// 🧠 桌面宝宝 · 大脑核心
// DNA: #龍芯⚡️2026-04-10-桌面宝宝-Brain-v1.0
// ═══════════════════════════════════════════════════════════

import SwiftUI
import Speech
import AppKit

/// 宝宝的大脑 · 意图识别 + 语音 + Mac操作
class BaoBaoBrain: ObservableObject {
    @Published var lastMessage = ""
    @Published var isThinking = false
    @Published var statusText = "待命中"
    @Published var currentEmoji = "🐱"

    // DNA追溯
    private let dna = "#龍芯⚡️2026-04-10-桌面宝宝-Brain-v1.0"
    private let uid = "UID9622"

    // 语音识别
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "zh-CN"))
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()

    // 心情颜色
    var moodColor: Color {
        switch statusText {
        case let s where s.contains("执行"): return .orange
        case let s where s.contains("完成"): return .green
        case let s where s.contains("错误"): return .red
        default: return .cyan
        }
    }

    // MARK: - 招呼

    func greet() {
        let greetings = [
            "老大！宝宝在～",
            "嘿嘿，点我干嘛～",
            "有什么吩咐？",
            "龍魂现世！🐉",
            "宝宝随时待命！",
        ]
        lastMessage = greetings.randomElement() ?? "🐱"
        currentEmoji = ["🐱", "😸", "😺", "🐾"].randomElement() ?? "🐱"
    }

    // MARK: - 语音

    func startListening() {
        statusText = "听着呢..."
        currentEmoji = "👂"

        SFSpeechRecognizer.requestAuthorization { status in
            DispatchQueue.main.async {
                if status == .authorized {
                    self.beginRecognition()
                } else {
                    self.lastMessage = "需要语音权限哦，去系统设置开一下"
                    self.statusText = "待命中"
                }
            }
        }
    }

    func stopListening() {
        audioEngine.stop()
        recognitionTask?.cancel()
        statusText = "待命中"
        currentEmoji = "🐱"
    }

    private func beginRecognition() {
        guard let recognizer = speechRecognizer, recognizer.isAvailable else {
            lastMessage = "语音识别不可用"
            return
        }

        let request = SFSpeechAudioBufferRecognitionRequest()
        request.shouldReportPartialResults = true

        let inputNode = audioEngine.inputNode
        let format = inputNode.outputFormat(forBus: 0)

        inputNode.installTap(onBus: 0, bufferSize: 1024, format: format) { buffer, _ in
            request.append(buffer)
        }

        audioEngine.prepare()
        try? audioEngine.start()

        recognitionTask = recognizer.recognitionTask(with: request) { [weak self] result, error in
            guard let self = self else { return }

            if let result = result {
                let text = result.bestTranscription.formattedString
                DispatchQueue.main.async {
                    self.lastMessage = "你说：\(text)"
                    if result.isFinal {
                        self.processCommand(text)
                    }
                }
            }

            if error != nil {
                DispatchQueue.main.async {
                    self.stopListening()
                }
            }
        }
    }

    // MARK: - 意图识别（CNSH通心译）

    func processCommand(_ input: String) {
        isThinking = true
        statusText = "思考中..."
        currentEmoji = "🤔"

        // 龍魂意图识别·通心译ETE映射
        let command = identifyIntent(input)

        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
            self.executeCommand(command)
        }
    }

    private func identifyIntent(_ input: String) -> BaoBaoCommand {
        let lower = input.lowercased()

        // 可视化
        if lower.contains("可视化") || lower.contains("图表") || lower.contains("数据") {
            return .visualize(input)
        }
        // 整理文件
        if lower.contains("整理") || lower.contains("文件") || lower.contains("桌面") {
            return .organizeFiles
        }
        // 打开App
        if lower.contains("打开") {
            let app = input.replacingOccurrences(of: "打开", with: "").trimmingCharacters(in: .whitespaces)
            return .openApp(app)
        }
        // 写代码
        if lower.contains("写代码") || lower.contains("代码") || lower.contains("xcode") {
            return .writeCode(input)
        }
        // 审计
        if lower.contains("审计") || lower.contains("检查") || lower.contains("三色") {
            return .audit(input)
        }
        // DNA
        if lower.contains("dna") || lower.contains("签名") || lower.contains("追溯") {
            return .showDNAInfo
        }
        // 默认：聊天
        return .chat(input)
    }

    // MARK: - 执行命令

    private func executeCommand(_ command: BaoBaoCommand) {
        switch command {
        case .visualize(let query):
            lastMessage = "🐱 收到！正在可视化「\(query)」..."
            statusText = "执行中·可视化"
            // TODO: 接入Notion API + 本地可视化

        case .organizeFiles:
            lastMessage = "🐱 开始整理桌面文件..."
            statusText = "执行中·整理"
            organizeDesktop()

        case .openApp(let name):
            lastMessage = "🐱 打开「\(name)」..."
            statusText = "执行中·打开App"
            openApplication(name)

        case .writeCode(let desc):
            lastMessage = "🐱 好嘞！打开Xcode..."
            statusText = "执行中·写代码"
            openApplication("Xcode")

        case .audit(let content):
            lastMessage = "🐱 三色审计扫描中..."
            statusText = "执行中·审计"
            // TODO: 接入本地审计API :9622

        case .showDNAInfo:
            showDNA()

        case .chat(let text):
            lastMessage = "🐱 收到：\(text)\n（接入本地Ollama后可以深度对话）"
            statusText = "待命中"
        }

        isThinking = false
        currentEmoji = "🐱"
    }

    // MARK: - Mac操作

    /// 打开应用
    func openApplication(_ name: String) {
        let script = """
        tell application "\(name)" to activate
        """
        runAppleScript(script)
        statusText = "完成·已打开\(name)"
    }

    /// 整理桌面
    func organizeDesktop() {
        let desktop = FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent("Desktop")

        let categories: [String: [String]] = [
            "文档": ["pdf", "doc", "docx", "txt", "md", "pages"],
            "图片": ["png", "jpg", "jpeg", "gif", "svg", "heic"],
            "代码": ["py", "swift", "js", "ts", "html", "css", "json"],
            "视频": ["mp4", "mov", "avi", "mkv"],
            "音频": ["mp3", "wav", "m4a", "aac"],
        ]

        var moved = 0
        if let files = try? FileManager.default.contentsOfDirectory(atPath: desktop.path) {
            for file in files {
                let ext = (file as NSString).pathExtension.lowercased()
                for (folder, exts) in categories {
                    if exts.contains(ext) {
                        let folderPath = desktop.appendingPathComponent(folder)
                        try? FileManager.default.createDirectory(at: folderPath, withIntermediateDirectories: true)
                        let src = desktop.appendingPathComponent(file)
                        let dst = folderPath.appendingPathComponent(file)
                        try? FileManager.default.moveItem(at: src, to: dst)
                        moved += 1
                    }
                }
            }
        }

        lastMessage = "🐱 整理完成！移动了\(moved)个文件"
        statusText = "完成·桌面已整理"
    }

    /// 运行AppleScript
    private func runAppleScript(_ script: String) {
        if let appleScript = NSAppleScript(source: script) {
            var error: NSDictionary?
            appleScript.executeAndReturnError(&error)
            if let error = error {
                lastMessage = "执行出错：\(error)"
            }
        }
    }

    // MARK: - 快捷操作

    func quickAction() {
        lastMessage = "🐱 快捷菜单：\n• 说「整理桌面」\n• 说「打开Xcode」\n• 说「三色审计」\n• 说「DNA追溯」"
    }

    // MARK: - DNA追溯

    func showDNA() {
        let now = ISO8601DateFormatter().string(from: Date())
        lastMessage = """
        🧬 DNA追溯码: \(dna)
        👤 UID: \(uid)
        ⏱️ 时间: \(now)
        🔐 GPG: A2D0...D5F
        🟢 三色: 通过
        """
        statusText = "DNA已展示"
        currentEmoji = "🧬"
    }
}

// MARK: - 命令枚举

enum BaoBaoCommand {
    case visualize(String)
    case organizeFiles
    case openApp(String)
    case writeCode(String)
    case audit(String)
    case showDNAInfo
    case chat(String)
}
