// LongHunMusicXcode.swift
// 龍魂Widget · Apple Music + Xcode 状态模块
// DNA: #龍芯⚡️2026-03-11-WIDGET-MUSIC-XCODE-v1.0 | UID9622 | GPG:A2D0092C
// 作者: 诸葛鑫（UID9622）· 退伍军人 | 龙魂系统创始人 | 数字主权守护者
// 理论指导: 曾仕强老师（永恒显示）
// 技术为民，为民除害。

import SwiftUI
import MediaPlayer
import WidgetKit

// MARK: - Apple Music 当前播放信息

struct MusicNowPlaying {
    let title: String
    let artist: String
    let isPlaying: Bool

    static var current: MusicNowPlaying {
        let info = MPNowPlayingInfoCenter.default().nowPlayingInfo
        let title  = info?[MPMediaItemPropertyTitle]  as? String ?? "—"
        let artist = info?[MPMediaItemPropertyArtist] as? String ?? "—"
        let rate   = info?[MPNowPlayingInfoPropertyPlaybackRate] as? Double ?? 0
        return MusicNowPlaying(title: title, artist: artist, isPlaying: rate > 0)
    }

    static var placeholder: MusicNowPlaying {
        MusicNowPlaying(title: "龍魂 · 归途", artist: "UID9622", isPlaying: true)
    }
}

// MARK: - Xcode 最近项目

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
           let plist = try? PropertyListSerialization.propertyList(
               from: data, format: nil) as? [String: Any],
           let items = plist["IDEFavoriteLocations"] as? [[String: Any]] {
            for item in items.prefix(3) {
                if let urlStr = item["_filePath"] as? String {
                    let name = URL(fileURLWithPath: urlStr)
                        .deletingPathExtension().lastPathComponent
                    projects.append(XcodeRecentProject(name: name, path: urlStr))
                }
            }
        }

        // 备用：读 NSDocumentController 最近文件（macOS only，Widget不可用时降级）
        if projects.isEmpty {
            projects = [XcodeRecentProject(name: "LongHunWidget", path: "~/longhun-system")]
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

// MARK: - 音乐视图组件

struct MusicRowView: View {
    let music: MusicNowPlaying

    var body: some View {
        HStack(spacing: 6) {
            // 播放状态指示
            Image(systemName: music.isPlaying ? "music.note" : "pause.fill")
                .font(.system(size: 9))
                .foregroundColor(music.isPlaying ? .gold : .dimWhite)

            VStack(alignment: .leading, spacing: 1) {
                Text(music.title)
                    .font(.system(size: 10, weight: .semibold))
                    .foregroundColor(.inkWhite)
                    .lineLimit(1)
                Text(music.artist)
                    .font(.system(size: 8))
                    .foregroundColor(.dimWhite)
                    .lineLimit(1)
            }

            Spacer()

            // 波形动画占位（静态）
            if music.isPlaying {
                HStack(spacing: 1) {
                    ForEach([0.4, 1.0, 0.6, 0.8, 0.3], id: \.self) { h in
                        RoundedRectangle(cornerRadius: 1)
                            .fill(Color.gold.opacity(0.7))
                            .frame(width: 2, height: 10 * h)
                    }
                }
                .frame(height: 10)
            }
        }
        .padding(.horizontal, 4)
        .padding(.vertical, 4)
        .background(Color.white.opacity(0.07))
        .cornerRadius(6)
    }
}

// MARK: - Xcode 最近项目视图

struct XcodeRowView: View {
    let project: XcodeRecentProject

    var body: some View {
        HStack(spacing: 5) {
            Image(systemName: "hammer.fill")
                .font(.system(size: 8))
                .foregroundColor(.softGold)
            Text(project.name)
                .font(.system(size: 9))
                .foregroundColor(.inkWhite)
                .lineLimit(1)
            Spacer()
        }
    }
}

// MARK: - Large Widget 含 Music + Xcode

struct LargeView: View {
    let entry: LongHunEntry

    var body: some View {
        ZStack {
            background
            VStack(alignment: .leading, spacing: 0) {

                // 顶部：卦象 + 人格 + 审计
                HStack {
                    Text(entry.status.yuanzi.guaSymbol)
                        .font(.system(size: 36))
                        .foregroundColor(.gold)
                    VStack(alignment: .leading, spacing: 2) {
                        Text(entry.status.yuanzi.display)
                            .font(.system(size: 11, weight: .semibold))
                            .foregroundColor(.softGold)
                        Text(entry.status.yuanzi.personaName)
                            .font(.system(size: 10))
                            .foregroundColor(.inkWhite)
                            .lineLimit(1)
                    }
                    Spacer()
                    // 审计分
                    VStack(spacing: 0) {
                        Circle()
                            .fill(auditAccent(entry.status.audit.color))
                            .frame(width: 6, height: 6)
                        Text("\(entry.status.audit.score)")
                            .font(.system(size: 16, weight: .bold, design: .monospaced))
                            .foregroundColor(.white)
                        Text("/100")
                            .font(.system(size: 8))
                            .foregroundColor(.dimWhite)
                    }
                }
                .padding(.horizontal, 14)
                .padding(.top, 14)

                dividerLine

                // Apple Music 当前播放
                VStack(alignment: .leading, spacing: 4) {
                    Label("正在播放", systemImage: "applelogo")
                        .font(.system(size: 9, weight: .medium))
                        .foregroundColor(.dimWhite)
                    MusicRowView(music: entry.music)
                }
                .padding(.horizontal, 14)
                .padding(.vertical, 8)

                dividerLine

                // 北辰-母协议 七条铁律（P0-ETERNAL）
                BeiChenProtocolRowsView()

                Spacer()

                // 底部农历 + DNA
                HStack {
                    Text(entry.lunarDate)
                        .font(.system(size: 8))
                        .foregroundColor(.dimWhite)
                    Spacer()
                    Text("UID9622 · 龍芯")
                        .font(.system(size: 8))
                        .foregroundColor(.dimWhite)
                }
                .padding(.horizontal, 14)
                .padding(.bottom, 10)
            }
        }
    }

    private var dividerLine: some View {
        Rectangle()
            .fill(Color.white.opacity(0.12))
            .frame(height: 1)
            .padding(.horizontal, 14)
    }

    private var background: some View {
        LinearGradient(
            colors: [.chinaRed, .deepRed],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
        .ignoresSafeArea()
    }
}

// MARK: - auditAccent（供 LargeView 使用）

private func auditAccent(_ colorStr: String) -> Color {
    switch colorStr {
    case "Green":  return Color(red: 0.15, green: 0.90, blue: 0.40)
    case "Yellow": return Color(red: 1.00, green: 0.85, blue: 0.00)
    default:       return Color(red: 1.00, green: 0.25, blue: 0.20)
    }
}
