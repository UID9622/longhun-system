// ═══════════════════════════════════════════════════════════════
//  龍魂·算法可视化工场 · ContentView.swift
//  UID9622 · 裸跑解压专用 · 不会写代码也能看懂
//
//  键盘: Space=播放/暂停  ←→=单步  R=重新生成  1-5=切算法
// ═══════════════════════════════════════════════════════════════

import SwiftUI
import Combine

// MARK: ── 龍魂配色 ───────────────────────────────────────────────

struct T {
    static let bg      = Color(red: 0.030, green: 0.018, blue: 0.090)
    static let surface = Color(red: 0.055, green: 0.035, blue: 0.130)
    static let panel   = Color(red: 0.040, green: 0.025, blue: 0.110)
    static let gold    = Color(red: 1.00,  green: 0.84,  blue: 0.00)   // 已排序·金
    static let cyan    = Color(red: 0.26,  green: 0.80,  blue: 1.00)   // 比较中·青
    static let orange  = Color(red: 0.95,  green: 0.50,  blue: 0.18)   // 交换中·橙
    static let red     = Color(red: 1.00,  green: 0.25,  blue: 0.12)   // 基准·红
    static let green   = Color(red: 0.00,  green: 1.00,  blue: 0.53)   // 就位·绿
    static let dim     = Color(red: 0.22,  green: 0.26,  blue: 0.38)   // 未排序
    static let text    = Color(white: 0.88)
    static let sub     = Color(white: 0.40)
    static let border  = Color(white: 0.12)
}

// MARK: ── 算法枚举 ──────────────────────────────────────────────

enum SortAlgo: String, CaseIterable, Identifiable {
    case bubble    = "冒泡排序"
    case insertion = "插入排序"
    case selection = "选择排序"
    case quick     = "快速排序"
    case merge     = "归并排序"
    case shell     = "希尔排序"

    var id: String { rawValue }

    var emoji: String {
        switch self {
        case .bubble:    return "🫧"
        case .insertion: return "🃏"
        case .selection: return "🎯"
        case .quick:     return "⚡️"
        case .merge:     return "🔀"
        case .shell:     return "🐚"
        }
    }

    var complexity: String {
        switch self {
        case .bubble:    return "O(n²)   · 最简直觉"
        case .insertion: return "O(n²)   · 扑克牌插牌"
        case .selection: return "O(n²)   · 每轮找最小"
        case .quick:     return "O(n㏒n) · 分治之王"
        case .merge:     return "O(n㏒n) · 稳定分治"
        case .shell:     return "O(n^1.3)· 跳跃插入"
        }
    }

    var shortcut: String {
        switch self {
        case .bubble:    return "⌨ B"
        case .insertion: return "⌨ I"
        case .selection: return "⌨ S"
        case .quick:     return "⌨ Q"
        case .merge:     return "⌨ M"
        case .shell:     return "⌨ H"
        }
    }
}

// MARK: ── 动画帧 ────────────────────────────────────────────────

struct SortFrame {
    var array:      [Int]
    var comparing:  Set<Int> = []
    var swapping:   Set<Int> = []
    var pivot:      Int?     = nil
    var sorted:     Set<Int> = []
    var comparisons: Int     = 0
    var swaps:       Int     = 0
    var message:    String   = ""
}

// MARK: ── 帧生成器 ─────────────────────────────────────────────

enum FrameGen {
    static func generate(array: [Int], algo: SortAlgo) -> [SortFrame] {
        var frames: [SortFrame] = []
        var arr = array
        var cmp = 0, swp = 0
        var sorted = Set<Int>()

        func push(_ comparing: Set<Int> = [], _ swapping: Set<Int> = [],
                  pivot: Int? = nil, msg: String = "") {
            frames.append(SortFrame(array: arr, comparing: comparing,
                                    swapping: swapping, pivot: pivot,
                                    sorted: sorted,
                                    comparisons: cmp, swaps: swp, message: msg))
        }

        switch algo {

        // ── 冒泡 ─────────────────────────────────────────────
        case .bubble:
            let n = arr.count
            for i in 0..<n {
                var didSwap = false
                for j in 0..<(n - i - 1) {
                    cmp += 1
                    push([j, j+1], msg: "比较 [\(j)] vs [\(j+1)]")
                    if arr[j] > arr[j+1] {
                        arr.swapAt(j, j+1); swp += 1; didSwap = true
                        push([], [j, j+1], msg: "交换!")
                    }
                }
                sorted.insert(n - 1 - i)
                if !didSwap { for k in 0..<(n-i) { sorted.insert(k) }; break }
            }

        // ── 插入 ─────────────────────────────────────────────
        case .insertion:
            let n = arr.count
            sorted.insert(0)
            for i in 1..<n {
                let key = arr[i]
                var j = i
                push([i], msg: "取出 [\(i)] = \(key)")
                while j > 0 {
                    cmp += 1
                    push([j-1, j], pivot: i, msg: "[\(j-1)] > \(key)?")
                    if arr[j-1] > key {
                        arr[j] = arr[j-1]; swp += 1
                        push([], [j-1, j], pivot: i, msg: "后移")
                        j -= 1
                    } else { break }
                }
                arr[j] = key
                sorted.insert(i)
                push([j], msg: "插入到 [\(j)]")
            }

        // ── 选择 ─────────────────────────────────────────────
        case .selection:
            let n = arr.count
            for i in 0..<n {
                var minIdx = i
                push([i], msg: "第 \(i+1) 轮：寻找最小值")
                for j in (i+1)..<n {
                    cmp += 1
                    push([minIdx, j], msg: "当前最小=[\(minIdx)], 候选=[\(j)]")
                    if arr[j] < arr[minIdx] { minIdx = j }
                }
                if minIdx != i {
                    arr.swapAt(i, minIdx); swp += 1
                    push([], [i, minIdx], msg: "找到！交换到位")
                }
                sorted.insert(i)
            }

        // ── 快速 ─────────────────────────────────────────────
        case .quick:
            func partition(_ lo: Int, _ hi: Int) -> Int {
                let pv = arr[hi]
                var i = lo - 1
                push([], [], pivot: hi, msg: "基准 pivot=\(pv)")
                for j in lo..<hi {
                    cmp += 1
                    push([j], [], pivot: hi, msg: "[\(j)]=\(arr[j]) ≤ \(pv)?")
                    if arr[j] <= pv {
                        i += 1
                        arr.swapAt(i, j); swp += 1
                        push([], [i, j], pivot: hi, msg: "小于基准，移左")
                    }
                }
                arr.swapAt(i+1, hi); swp += 1
                push([], [i+1, hi], msg: "基准就位!")
                return i + 1
            }
            func qs(_ lo: Int, _ hi: Int) {
                guard lo < hi else {
                    if lo == hi { sorted.insert(lo) }
                    return
                }
                let p = partition(lo, hi)
                sorted.insert(p)
                qs(lo, p - 1)
                qs(p + 1, hi)
            }
            qs(0, arr.count - 1)

        // ── 归并 ─────────────────────────────────────────────
        case .merge:
            func merge(_ lo: Int, _ mid: Int, _ hi: Int) {
                var temp = [Int]()
                var i = lo, j = mid + 1
                while i <= mid && j <= hi {
                    cmp += 1
                    push([i, j], msg: "左[\(i)] vs 右[\(j)]")
                    if arr[i] <= arr[j] { temp.append(arr[i]); i += 1 }
                    else                { temp.append(arr[j]); j += 1 }
                }
                while i <= mid { temp.append(arr[i]); i += 1 }
                while j <= hi  { temp.append(arr[j]); j += 1 }
                for k in 0..<temp.count {
                    arr[lo + k] = temp[k]; swp += 1
                    push([], [lo + k], msg: "写回 [\(lo+k)]")
                }
            }
            func ms(_ lo: Int, _ hi: Int) {
                guard lo < hi else { sorted.insert(lo); return }
                let mid = (lo + hi) / 2
                ms(lo, mid)
                ms(mid + 1, hi)
                merge(lo, mid, hi)
                for k in lo...hi { sorted.insert(k) }
            }
            ms(0, arr.count - 1)

        // ── 希尔 ─────────────────────────────────────────────
        case .shell:
            let n = arr.count
            var gap = n / 2
            while gap > 0 {
                push(msg: "间隔 gap=\(gap)")
                for i in gap..<n {
                    let temp = arr[i]; var j = i
                    push([i], msg: "插入 gap=\(gap), i=\(i)")
                    while j >= gap {
                        cmp += 1
                        push([j-gap, j], msg: "比较间距 \(gap)")
                        if arr[j-gap] > temp {
                            arr[j] = arr[j-gap]; swp += 1
                            push([], [j-gap, j], msg: "后移 \(gap) 位")
                            j -= gap
                        } else { break }
                    }
                    arr[j] = temp
                }
                if gap == 1 { for k in 0..<n { sorted.insert(k) } }
                gap /= 2
            }
        }

        // 最终帧：全部排好
        sorted = Set(0..<arr.count)
        frames.append(SortFrame(array: arr, sorted: sorted,
                                comparisons: cmp, swaps: swp, message: "✅ 排序完成！"))
        return frames
    }
}

// MARK: ── ViewModel ─────────────────────────────────────────────

@MainActor
final class SortVM: ObservableObject {
    @Published var frames:    [SortFrame]   = []
    @Published var idx:       Int           = 0
    @Published var isPlaying: Bool          = false
    @Published var algo:      SortAlgo      = .bubble
    @Published var size:      Double        = 60
    @Published var speed:     Double        = 1.0   // 0.25 ~ 8x

    private var timer: AnyCancellable?

    var cur: SortFrame? { frames.isEmpty ? nil : frames[min(idx, frames.count-1)] }
    var progress: Double { frames.count <= 1 ? 0 : Double(idx) / Double(frames.count - 1) }
    var totalFrames: Int { frames.count }

    func generate() {
        stop()
        var arr = Array(1...Int(size))
        arr.shuffle()
        frames = FrameGen.generate(array: arr, algo: algo)
        idx = 0
    }

    func play() {
        guard idx < frames.count - 1 else { idx = 0; return }
        isPlaying = true
        // interval: base 120 frames/s scaled by speed
        let interval = 1.0 / (speed * 120.0)
        timer = Timer.publish(every: interval, on: .main, in: .common)
            .autoconnect()
            .sink { [weak self] _ in
                guard let self else { return }
                if self.idx < self.frames.count - 1 {
                    self.idx += 1
                } else {
                    self.stop()
                }
            }
    }

    func stop() {
        timer?.cancel(); timer = nil
        isPlaying = false
    }

    func togglePlay() {
        if isPlaying { stop() } else { play() }
    }

    func stepFwd() { stop(); if idx < frames.count - 1 { idx += 1 } }
    func stepBck() { stop(); if idx > 0 { idx -= 1 } }

    func setAlgo(_ a: SortAlgo) { algo = a; generate() }
}

// MARK: ── Canvas 排序图 ─────────────────────────────────────────

struct SortCanvas: View {
    let frame: SortFrame

    var body: some View {
        GeometryReader { geo in
            let n  = frame.array.count
            let w  = geo.size.width
            let h  = geo.size.height
            let bw = w / CGFloat(n)
            let mx = CGFloat(n)
            let pad: CGFloat = bw > 3 ? 1 : 0

            Canvas { ctx, size in
                for i in 0..<n {
                    let val = CGFloat(frame.array[i])
                    let bh  = (val / mx) * (size.height - 4)
                    let x   = CGFloat(i) * bw
                    let y   = size.height - bh

                    let color: Color
                    if frame.sorted.contains(i)    { color = T.gold }
                    else if frame.swapping.contains(i) { color = T.orange }
                    else if frame.pivot == i       { color = T.red }
                    else if frame.comparing.contains(i) { color = T.cyan }
                    else {
                        let t = val / mx
                        color = Color(red: 0.18 + 0.12*t,
                                      green: 0.22 + 0.15*t,
                                      blue:  0.38 + 0.20*t)
                    }

                    let rect = CGRect(x: x + pad, y: y, width: max(bw - pad*2, 1), height: bh)
                    ctx.fill(Path(rect), with: .color(color))
                }
            }
        }
    }
}

// MARK: ── 色块图例 ──────────────────────────────────────────────

struct Legend: View {
    let items: [(Color, String)]
    var body: some View {
        HStack(spacing: 14) {
            ForEach(items, id: \.1) { col, label in
                HStack(spacing: 5) {
                    RoundedRectangle(cornerRadius: 2)
                        .fill(col)
                        .frame(width: 12, height: 12)
                    Text(label)
                        .font(.system(size: 11))
                        .foregroundColor(T.sub)
                }
            }
        }
    }
}

// MARK: ── 算法选择按钮 ──────────────────────────────────────────

struct AlgoButton: View {
    let algo: SortAlgo
    let selected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            HStack(spacing: 8) {
                Text(algo.emoji).font(.system(size: 14))
                VStack(alignment: .leading, spacing: 2) {
                    Text(algo.rawValue)
                        .font(.system(size: 12, weight: selected ? .bold : .regular))
                        .foregroundColor(selected ? T.gold : T.text)
                    Text(algo.complexity)
                        .font(.system(size: 10, design: .monospaced))
                        .foregroundColor(T.sub)
                }
                Spacer()
                Text(algo.shortcut)
                    .font(.system(size: 9, design: .monospaced))
                    .foregroundColor(T.sub)
            }
            .padding(.horizontal, 10)
            .padding(.vertical, 7)
            .background(selected ? T.surface : Color.clear)
            .overlay(
                RoundedRectangle(cornerRadius: 6)
                    .stroke(selected ? T.gold.opacity(0.4) : Color.clear, lineWidth: 1)
            )
            .cornerRadius(6)
        }
        .buttonStyle(.plain)
    }
}

// MARK: ── 侧边栏 ───────────────────────────────────────────────

struct Sidebar: View {
    @ObservedObject var vm: SortVM

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {

            // ── 标题
            VStack(alignment: .leading, spacing: 4) {
                Text("🐉 龍魂·算法工场")
                    .font(.system(size: 15, weight: .black))
                    .foregroundColor(T.gold)
                Text("UID9622 · 裸跑解压版")
                    .font(.system(size: 10, design: .monospaced))
                    .foregroundColor(T.sub)
            }
            .padding(14)

            Divider().background(T.border)

            // ── 算法选择
            VStack(alignment: .leading, spacing: 2) {
                Text("选算法")
                    .font(.system(size: 10, weight: .bold))
                    .foregroundColor(T.sub)
                    .padding(.horizontal, 10)
                    .padding(.top, 10)
                    .padding(.bottom, 4)

                ForEach(SortAlgo.allCases) { a in
                    AlgoButton(algo: a, selected: vm.algo == a) {
                        vm.setAlgo(a)
                    }
                    .padding(.horizontal, 6)
                }
            }

            Divider().background(T.border).padding(.top, 8)

            // ── 数组大小
            VStack(alignment: .leading, spacing: 6) {
                HStack {
                    Text("数组大小")
                        .font(.system(size: 10, weight: .bold))
                        .foregroundColor(T.sub)
                    Spacer()
                    Text("\(Int(vm.size))")
                        .font(.system(size: 11, design: .monospaced))
                        .foregroundColor(T.gold)
                }
                Slider(value: $vm.size, in: 10...120, step: 5)
                    .accentColor(T.gold.nsColor.map { Color($0) } ?? T.gold)
                    .onChange(of: vm.size) { _ in vm.generate() }
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 10)

            // ── 速度
            VStack(alignment: .leading, spacing: 6) {
                HStack {
                    Text("播放速度")
                        .font(.system(size: 10, weight: .bold))
                        .foregroundColor(T.sub)
                    Spacer()
                    Text(speedLabel)
                        .font(.system(size: 11, design: .monospaced))
                        .foregroundColor(T.cyan)
                }
                Slider(value: $vm.speed, in: 0.1...12.0)
                    .accentColor(T.cyan.nsColor.map { Color($0) } ?? T.cyan)
            }
            .padding(.horizontal, 12)
            .padding(.bottom, 10)

            Divider().background(T.border)

            // ── 控制按钮
            VStack(spacing: 8) {
                // Play/Pause + Step
                HStack(spacing: 8) {
                    CtrlBtn(icon: "backward.frame.fill", tip: "上一帧") { vm.stepBck() }
                    CtrlBtn(
                        icon: vm.isPlaying ? "pause.fill" : "play.fill",
                        tip: vm.isPlaying ? "暂停" : "播放",
                        color: T.gold
                    ) { vm.togglePlay() }
                    .frame(maxWidth: .infinity)
                    CtrlBtn(icon: "forward.frame.fill", tip: "下一帧") { vm.stepFwd() }
                }

                // Regenerate
                Button {
                    vm.generate()
                } label: {
                    Label("重新生成 (R)", systemImage: "arrow.triangle.2.circlepath")
                        .font(.system(size: 12, weight: .semibold))
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 7)
                        .background(T.surface)
                        .foregroundColor(T.text)
                        .cornerRadius(8)
                        .overlay(RoundedRectangle(cornerRadius: 8).stroke(T.border, lineWidth: 1))
                }
                .buttonStyle(.plain)
            }
            .padding(.horizontal, 10)
            .padding(.vertical, 12)

            Spacer()

            // ── 快捷键提示
            VStack(alignment: .leading, spacing: 4) {
                Text("快捷键")
                    .font(.system(size: 9, weight: .bold))
                    .foregroundColor(T.sub.opacity(0.6))
                ForEach(["Space · 播放/暂停",
                         "← → · 单帧步进",
                         "R · 重新生成",
                         "1-6 · 切换算法"], id: \.self) { tip in
                    Text(tip)
                        .font(.system(size: 9, design: .monospaced))
                        .foregroundColor(T.sub.opacity(0.5))
                }
            }
            .padding(.horizontal, 12)
            .padding(.bottom, 14)
        }
        .background(T.panel)
    }

    var speedLabel: String {
        let s = vm.speed
        if s < 0.3 { return "🐢 超慢" }
        if s < 0.8 { return "🚶 慢速" }
        if s < 2.0 { return "🚴 正常" }
        if s < 5.0 { return "🚗 快速" }
        return "🚀 疯狂"
    }
}

// MARK: ── 控制按钮 ─────────────────────────────────────────────

struct CtrlBtn: View {
    let icon: String
    let tip: String
    var color: Color = T.text
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Image(systemName: icon)
                .font(.system(size: 18, weight: .semibold))
                .foregroundColor(color)
                .frame(width: 42, height: 36)
                .background(T.surface)
                .cornerRadius(8)
                .overlay(RoundedRectangle(cornerRadius: 8).stroke(T.border, lineWidth: 1))
        }
        .buttonStyle(.plain)
        .help(tip)
    }
}

// MARK: ── 状态栏 ───────────────────────────────────────────────

struct StatsBar: View {
    let frame: SortFrame
    let progress: Double
    let total: Int
    let algo: SortAlgo

    var body: some View {
        HStack(spacing: 20) {
            // 进度
            VStack(alignment: .leading, spacing: 3) {
                Text("进度")
                    .font(.system(size: 9)).foregroundColor(T.sub)
                Text("\(Int(progress * 100))%  ·  帧 \(Int(Double(total) * progress))/\(total)")
                    .font(.system(size: 11, design: .monospaced))
                    .foregroundColor(T.text)
            }

            statItem("比较次数", "\(frame.comparisons)", T.cyan)
            statItem("交换次数", "\(frame.swaps)", T.orange)
            statItem("已排序",   "\(frame.sorted.count)/\(frame.array.count)", T.gold)

            Spacer()

            // 消息提示
            if !frame.message.isEmpty {
                Text(frame.message)
                    .font(.system(size: 12))
                    .foregroundColor(T.sub)
                    .lineLimit(1)
            }

            // 进度条
            GeometryReader { g in
                ZStack(alignment: .leading) {
                    RoundedRectangle(cornerRadius: 2)
                        .fill(T.border)
                    RoundedRectangle(cornerRadius: 2)
                        .fill(T.gold)
                        .frame(width: g.size.width * progress)
                }
            }
            .frame(width: 120, height: 4)
        }
    }

    func statItem(_ label: String, _ value: String, _ color: Color) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            Text(label)
                .font(.system(size: 9)).foregroundColor(T.sub)
            Text(value)
                .font(.system(size: 12, weight: .bold, design: .monospaced))
                .foregroundColor(color)
        }
    }
}

// MARK: ── 主视图 ───────────────────────────────────────────────

struct ContentView: View {
    @StateObject private var vm = SortVM()
    @State private var show3D = false

    var body: some View {
        HStack(spacing: 0) {

            // ── 左侧边栏
            Sidebar(vm: vm)
                .frame(width: 210)

            Divider().background(T.border)

            // ── 主区域
            VStack(spacing: 0) {

                // 顶部标题条
                HStack(spacing: 12) {
                    Text(vm.algo.emoji)
                        .font(.system(size: 18))
                    Text(vm.algo.rawValue)
                        .font(.system(size: 15, weight: .black))
                        .foregroundColor(T.gold)
                    Text("·")
                        .foregroundColor(T.sub)
                    Text(vm.algo.complexity)
                        .font(.system(size: 11, design: .monospaced))
                        .foregroundColor(T.sub)
                    Spacer()
                    // 2D / 3D 切换按钮
                    Button {
                        if !show3D && vm.frames.isEmpty { vm.generate() }
                        show3D.toggle()
                        if show3D { vm.stop() }
                    } label: {
                        Label(show3D ? "2D 排序" : "🌌 掰开看·3D",
                              systemImage: show3D ? "chart.bar.fill" : "cube.transparent")
                            .font(.system(size: 11, weight: .semibold))
                            .padding(.horizontal, 10)
                            .padding(.vertical, 5)
                            .background(show3D ? T.gold.opacity(0.15) : T.cyan.opacity(0.12))
                            .foregroundColor(show3D ? T.gold : T.cyan)
                            .clipShape(RoundedRectangle(cornerRadius: 7))
                            .overlay(RoundedRectangle(cornerRadius: 7)
                                .stroke(show3D ? T.gold.opacity(0.4) : T.cyan.opacity(0.3),
                                        lineWidth: 1))
                    }
                    .buttonStyle(.plain)

                    if !show3D {
                        Legend(items: [
                            (T.cyan,   "比较"),
                            (T.orange, "交换"),
                            (T.red,    "基准"),
                            (T.gold,   "已排"),
                        ])
                    }
                }
                .padding(.horizontal, 20)
                .padding(.vertical, 11)
                .background(T.surface)

                // ── 主画布区域
                if show3D {
                    // 3D 时空全景
                    AlgoLandscape3D(frames: vm.frames, algo: vm.algo)
                        .frame(maxWidth: .infinity, maxHeight: .infinity)
                        .background(Color(red: 0.025, green: 0.014, blue: 0.075))
                } else {
                    // 2D 排序动画
                    Group {
                        if let f = vm.cur {
                            SortCanvas(frame: f)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 8)
                        } else {
                            VStack(spacing: 12) {
                                Text("🐉").font(.system(size: 48))
                                Text("按下「重新生成」开始")
                                    .font(.system(size: 16))
                                    .foregroundColor(T.sub)
                            }
                            .frame(maxWidth: .infinity, maxHeight: .infinity)
                        }
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                    .background(T.bg)
                }

                Divider().background(T.border)

                // 底部状态栏（2D模式才显示）
                if !show3D, let f = vm.cur {
                    StatsBar(frame: f, progress: vm.progress,
                             total: vm.totalFrames, algo: vm.algo)
                        .padding(.horizontal, 20)
                        .padding(.vertical, 10)
                        .background(T.surface)
                }
            }
        }
        .background(T.bg)
        .onAppear { vm.generate() }

        // ── 键盘快捷键
        .onKeyPress(.space)        { vm.togglePlay(); return .handled }
        .onKeyPress(.leftArrow)    { vm.stepBck();    return .handled }
        .onKeyPress(.rightArrow)   { vm.stepFwd();    return .handled }
        .onKeyPress(KeyEquivalent("r")) { vm.generate(); return .handled }
        .onKeyPress(KeyEquivalent("3")) { show3D.toggle(); if show3D { vm.stop() }; return .handled }
        .onKeyPress(KeyEquivalent("b")) { vm.setAlgo(.bubble);    return .handled }
        .onKeyPress(KeyEquivalent("i")) { vm.setAlgo(.insertion); return .handled }
        .onKeyPress(KeyEquivalent("s")) { vm.setAlgo(.selection); return .handled }
        .onKeyPress(KeyEquivalent("q")) { vm.setAlgo(.quick);     return .handled }
        .onKeyPress(KeyEquivalent("m")) { vm.setAlgo(.merge);     return .handled }
        .onKeyPress(KeyEquivalent("h")) { vm.setAlgo(.shell);     return .handled }
    }
}

// MARK: ── Color helper ─────────────────────────────────────────

extension Color {
    var nsColor: NSColor? { NSColor(self) }
}
