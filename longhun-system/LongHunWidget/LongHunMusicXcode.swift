// LongHunMusicXcode.swift
// 龍魂Widget · Apple Music + Xcode 状态模块
// DNA: #龍芯⚡️2026-04-03-WIDGET-MUSIC-XCODE-v3.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 作者: 诸葛鑫（UID9622）· 退伍军人 | 龍魂系统创始人 | 数字主权守护者
// 理论指导: 曾仕强老师（永恒显示）
// 献礼: 新中国成立77周年（1949-2026）· 丙午马年
// 技术为民，为民除害。
// 视觉主题：朱砂红印记 · 五行动态配色 · 墨底玺印质感

import SwiftUI
import MediaPlayer
import WidgetKit

// ============================================================
// MARK: - 五行配色系统（日干动态）
// ============================================================

enum WuxingElement: String {
    case 木, 火, 金, 水, 土

    /// 今日日干 → 五行（本地计算，与 tiangan_dizhi.py 对齐）
    static var today: WuxingElement {
        let base = Calendar.current.startOfDay(for: Date(timeIntervalSinceReferenceDate: -3155673600)) // 1900-01-01
        let now  = Calendar.current.startOfDay(for: Date())
        let days = Calendar.current.dateComponents([.day], from: base, to: now).day ?? 0
        // 天干：甲乙丙丁戊己庚辛壬癸，甲=0
        let tg = days % 10
        // 甲乙→木, 丙丁→火, 戊己→土, 庚辛→金, 壬癸→水
        switch tg {
        case 0, 1: return .木
        case 2, 3: return .火
        case 4, 5: return .土
        case 6, 7: return .金
        default:   return .水
        }
    }

    // 五行主色
    var primaryColor: Color {
        switch self {
        case .木: return Color(red: 0.15, green: 0.48, blue: 0.20)  // 竹绿
        case .火: return Color(red: 0.76, green: 0.08, blue: 0.05)  // 朱砂红
        case .金: return Color(red: 0.75, green: 0.60, blue: 0.18)  // 古铜金
        case .水: return Color(red: 0.10, green: 0.28, blue: 0.58)  // 墨蓝
        case .土: return Color(red: 0.65, green: 0.42, blue: 0.12)  // 赭黄
        }
    }

    // 五行次色（波形/描边）
    var accentColor: Color {
        switch self {
        case .木: return Color(red: 0.30, green: 0.70, blue: 0.35)
        case .火: return Color(red: 0.95, green: 0.30, blue: 0.20)
        case .金: return Color(red: 0.92, green: 0.80, blue: 0.40)
        case .水: return Color(red: 0.25, green: 0.55, blue: 0.85)
        case .土: return Color(red: 0.85, green: 0.62, blue: 0.28)
        }
    }

    // 五行深背景色
    var deepBg: Color {
        switch self {
        case .木: return Color(red: 0.05, green: 0.12, blue: 0.06)
        case .火: return Color(red: 0.12, green: 0.03, blue: 0.02)
        case .金: return Color(red: 0.10, green: 0.08, blue: 0.02)
        case .水: return Color(red: 0.03, green: 0.06, blue: 0.14)
        case .土: return Color(red: 0.10, green: 0.07, blue: 0.02)
        }
    }

    var label: String {
        switch self {
        case .木: return "木·竹青"
        case .火: return "火·朱砂"
        case .金: return "金·古铜"
        case .水: return "水·墨蓝"
        case .土: return "土·赭黄"
        }
    }

    var symbol: String {
        switch self {
        case .木: return "🌿"
        case .火: return "🔥"
        case .金: return "⚔️"
        case .水: return "💧"
        case .土: return "🌍"
        }
    }
}

// ============================================================
// MARK: - 朱砂红印记（永久底层装饰）
// ============================================================

/// 朱砂红 —— 中国传统玺印颜色，永远压在背景
let 朱砂红 = Color(red: 0.76, green: 0.08, blue: 0.05)

struct ZhuShaYinView: View {
    var body: some View {
        ZStack {
            // 外圆印框
            Circle()
                .stroke(朱砂红.opacity(0.25), lineWidth: 2)
                .frame(width: 160, height: 160)

            // 内圆
            Circle()
                .stroke(朱砂红.opacity(0.15), lineWidth: 1)
                .frame(width: 140, height: 140)

            // 龍字印文（篆刻质感）
            Text("龍")
                .font(.system(size: 72, weight: .black, design: .serif))
                .foregroundColor(朱砂红.opacity(0.18))

            // 四角装饰线
            ForEach([0, 90, 180, 270], id: \.self) { angle in
                Rectangle()
                    .fill(朱砂红.opacity(0.12))
                    .frame(width: 1, height: 20)
                    .offset(y: -90)
                    .rotationEffect(.degrees(Double(angle)))
            }
        }
    }
}

// ============================================================
// MARK: - Apple Music 播放信息
// ============================================================

struct MusicNowPlaying {
    let title: String
    let artist: String
    let isPlaying: Bool

    static var current: MusicNowPlaying {
        let info   = MPNowPlayingInfoCenter.default().nowPlayingInfo
        let title  = info?[MPMediaItemPropertyTitle]  as? String ?? "—"
        let artist = info?[MPMediaItemPropertyArtist] as? String ?? "—"
        let rate   = info?[MPNowPlayingInfoPropertyPlaybackRate] as? Double ?? 0
        return MusicNowPlaying(title: title, artist: artist, isPlaying: rate > 0)
    }

    static var placeholder: MusicNowPlaying {
        MusicNowPlaying(title: "高山流水", artist: "古琴·国乐", isPlaying: true)
    }
}

// ============================================================
// MARK: - 五行波形动画
// ============================================================

struct WuxingWaveView: View {
    let isPlaying: Bool
    let element: WuxingElement
    @State private var phase = 0.0

    var body: some View {
        HStack(spacing: 3) {
            ForEach(0..<5, id: \.self) { i in
                RoundedRectangle(cornerRadius: 2)
                    .fill(
                        LinearGradient(
                            colors: [element.accentColor.opacity(0.5),
                                     element.accentColor],
                            startPoint: .bottom,
                            endPoint: .top
                        )
                    )
                    .frame(width: 3,
                           height: isPlaying ? 6 + CGFloat(i % 3) * 5 : 4)
                    .animation(
                        isPlaying
                            ? Animation.easeInOut(duration: 0.25 + Double(i) * 0.07)
                                .repeatForever(autoreverses: true)
                            : .default,
                        value: phase
                    )
            }
        }
        .onAppear { if isPlaying { phase = 1 } }
    }
}

// ============================================================
// MARK: - 音乐行视图
// ============================================================

struct MusicRowView: View {
    let music: MusicNowPlaying
    let element: WuxingElement

    var body: some View {
        HStack(spacing: 8) {
            // 五行符号
            Text(element.symbol)
                .font(.system(size: 11))

            VStack(alignment: .leading, spacing: 2) {
                Text(music.title)
                    .font(.system(size: 11, weight: .semibold))
                    .foregroundColor(.inkWhite)
                    .lineLimit(1)
                Text(music.artist)
                    .font(.system(size: 8))
                    .foregroundColor(element.accentColor.opacity(0.85))
                    .lineLimit(1)
            }

            Spacer()

            if music.isPlaying {
                WuxingWaveView(isPlaying: true, element: element)
            } else {
                Image(systemName: "pause.circle.fill")
                    .font(.system(size: 10))
                    .foregroundColor(.dimWhite)
            }
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 7)
        .background(
            RoundedRectangle(cornerRadius: 8)
                .fill(element.primaryColor.opacity(0.15))
                .overlay(
                    RoundedRectangle(cornerRadius: 8)
                        .stroke(element.accentColor.opacity(0.35), lineWidth: 0.8)
                )
        )
    }
}

// ============================================================
// MARK: - Xcode 最近项目
// ============================================================

struct XcodeRecentProject: Identifiable {
    let id = UUID()
    let name: String
    let path: String
}

struct XcodeStatus {
    let recentProjects: [XcodeRecentProject]

    static var current: XcodeStatus {
        let plistPath = NSHomeDirectory() +
            "/Library/Application Support/com.apple.dt.Xcode/UserData/IDEFavorites.plist"
        var projects: [XcodeRecentProject] = []
        if let data = FileManager.default.contents(atPath: plistPath),
           let plist = try? PropertyListSerialization.propertyList(from: data, format: nil) as? [String: Any],
           let items = plist["IDEFavoriteLocations"] as? [[String: Any]] {
            for item in items.prefix(3) {
                if let urlStr = item["_filePath"] as? String {
                    let name = URL(fileURLWithPath: urlStr).deletingPathExtension().lastPathComponent
                    projects.append(XcodeRecentProject(name: name, path: urlStr))
                }
            }
        }
        if projects.isEmpty {
            projects = [
                XcodeRecentProject(name: "LongHunWidget",  path: "~/longhun-system"),
                XcodeRecentProject(name: "CNSH-Engine",    path: "~/longhun-system/cnsh"),
            ]
        }
        return XcodeStatus(recentProjects: projects)
    }

    static var placeholder: XcodeStatus {
        XcodeStatus(recentProjects: [
            XcodeRecentProject(name: "LongHunWidget", path: "~/longhun-system"),
            XcodeRecentProject(name: "CNSH-Engine",   path: "~/longhun-system/cnsh"),
        ])
    }
}

struct XcodeRowView: View {
    let project: XcodeRecentProject
    let element: WuxingElement

    var body: some View {
        HStack(spacing: 5) {
            Image(systemName: "hammer.fill")
                .font(.system(size: 8))
                .foregroundColor(element.accentColor.opacity(0.8))
            Text(project.name)
                .font(.system(size: 9))
                .foregroundColor(.inkWhite)
                .lineLimit(1)
            Spacer()
        }
    }
}

// ============================================================
// MARK: - Large Widget 主视图
// ============================================================

struct LargeView: View {
    let entry: LongHunEntry
    let element = WuxingElement.today

    var body: some View {
        ZStack {
            // 层1：墨底 + 五行深色
            background

            // 层2：朱砂红印记（永久底层）
            ZhuShaYinView()
                .position(x: 260, y: 300)
                .blendMode(.screen)

            // 层3：内容
            VStack(alignment: .leading, spacing: 0) {
                headerView
                divider
                musicSection
                divider
                xcodeSection
                Spacer()
                footerView
            }
        }
    }

    // MARK: 顶部
    private var headerView: some View {
        HStack {
            // 五行标记
            VStack(alignment: .leading, spacing: 2) {
                Text(element.symbol + " " + element.label)
                    .font(.system(size: 10, weight: .bold))
                    .foregroundColor(element.accentColor)
                Text("日干·今日五行")
                    .font(.system(size: 8))
                    .foregroundColor(.dimWhite)
            }

            Spacer()

            // 审计分（五行配色）
            let audit = entry.status.audit
            VStack(spacing: 1) {
                Circle()
                    .fill(auditColor(audit.color))
                    .frame(width: 6, height: 6)
                Text("\(audit.score)")
                    .font(.system(size: 15, weight: .bold, design: .monospaced))
                    .foregroundColor(.inkWhite)
                Text("/100")
                    .font(.system(size: 7))
                    .foregroundColor(.dimWhite)
            }
        }
        .padding(.horizontal, 14)
        .padding(.top, 14)
        .padding(.bottom, 8)
    }

    // MARK: 音乐区
    private var musicSection: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Image(systemName: "music.note")
                    .font(.system(size: 8))
                Text("Apple Music · 当前播放")
                    .font(.system(size: 9, weight: .medium))
                Spacer()
                // 朱砂红小印章
                Text("印")
                    .font(.system(size: 8, weight: .black, design: .serif))
                    .foregroundColor(朱砂红.opacity(0.9))
                    .padding(.horizontal, 4)
                    .padding(.vertical, 2)
                    .overlay(
                        RoundedRectangle(cornerRadius: 2)
                            .stroke(朱砂红.opacity(0.7), lineWidth: 1)
                    )
            }
            .foregroundColor(.dimWhite)

            MusicRowView(music: entry.music, element: element)
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 8)
    }

    // MARK: Xcode区
    private var xcodeSection: some View {
        VStack(alignment: .leading, spacing: 5) {
            HStack {
                Image(systemName: "xcode")
                    .font(.system(size: 8))
                Text("龍魂铸剑·最近项目")
                    .font(.system(size: 9, weight: .medium))
                Spacer()
            }
            .foregroundColor(.dimWhite)

            ForEach(entry.xcode.recentProjects) { proj in
                XcodeRowView(project: proj, element: element)
            }
        }
        .padding(.horizontal, 14)
        .padding(.vertical, 8)
    }

    // MARK: 底部
    private var footerView: some View {
        VStack(spacing: 2) {
            // 朱砂红分隔线
            Rectangle()
                .fill(朱砂红.opacity(0.5))
                .frame(height: 0.8)
                .padding(.horizontal, 14)

            HStack {
                Text("UID9622 · 龍芯北辰")
                    .font(.system(size: 7))
                    .foregroundColor(.dimWhite)
                Spacer()
                Text("曾仕强老师·永恒显示")
                    .font(.system(size: 7))
                    .foregroundColor(.dimWhite)
            }
            .padding(.horizontal, 14)
            .padding(.bottom, 10)
            .padding(.top, 4)
        }
    }

    // MARK: 分隔线（五行色）
    private var divider: some View {
        LinearGradient(
            colors: [element.primaryColor.opacity(0.05),
                     element.accentColor.opacity(0.6),
                     element.primaryColor.opacity(0.05)],
            startPoint: .leading,
            endPoint: .trailing
        )
        .frame(height: 0.8)
        .padding(.horizontal, 14)
    }

    // MARK: 背景
    private var background: some View {
        ZStack {
            // 墨底
            Color(red: 0.06, green: 0.06, blue: 0.07)

            // 五行深色晕染
            RadialGradient(
                colors: [element.primaryColor.opacity(0.25), .clear],
                center: .topLeading,
                startRadius: 0,
                endRadius: 200
            )

            // 朱砂红角晕（右下角）
            RadialGradient(
                colors: [朱砂红.opacity(0.12), .clear],
                center: .bottomTrailing,
                startRadius: 0,
                endRadius: 150
            )
        }
        .ignoresSafeArea()
    }

    private func auditColor(_ c: String) -> Color {
        switch c {
        case "Green":  return element.accentColor
        case "Yellow": return Color(red: 0.95, green: 0.75, blue: 0.20)
        default:       return 朱砂红
        }
    }
}

// ============================================================
// MARK: - Color 扩展
// ============================================================

extension Color {
    static let inkWhite = Color(white: 0.92)
    static let dimWhite = Color(white: 0.58)
}
