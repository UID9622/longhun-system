// ═══════════════════════════════════════════════════════════
// 🧮 数学六根算法引擎 · Swift版
// DNA: #龍芯⚡️2026-04-10-数学六根-Swift-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// 创建者: UID9622 诸葛鑫（龍芯北辰）
// 理论指导: 曾仕强老师（永恒显示）
// ═══════════════════════════════════════════════════════════

import Foundation

/// 数学六根算法引擎
/// ① 数字根 ② 洛书九宫 ③ 太极递归 ④ 三才流场 ⑤ 时间压缩L5 ⑥ 信息熵
struct MathSixRoots {

    // MARK: - ① 数字根 (Digital Root)

    /// dr(n) = 1 + ((n - 1) % 9)
    /// 任何整数压缩到1-9·3-6-9循环归零
    static func digitalRoot(_ n: Int) -> Int {
        guard n > 0 else { return 9 }
        return 1 + ((n - 1) % 9)
    }

    /// 数字根熔断判定
    /// dr=1→🟢绿色 dr=5→🟡黄色 其他→🔴红色
    static func digitalRootFuse(_ n: Int) -> TriColor {
        let dr = digitalRoot(n)
        switch dr {
        case 1:    return .green   // 🟢 通行
        case 5:    return .yellow  // 🟡 待审
        case 3,6,9: return .yellow // 🟡 循环态·观察
        default:   return .red     // 🔴 熔断
        }
    }

    // MARK: - ② 洛书九宫 (Magic Square)

    /// 洛书九宫矩阵 [4,9,2,3,5,7,8,1,6]
    /// 行列对角线和=15
    static let luoshu: [[Int]] = [
        [4, 9, 2],
        [3, 5, 7],
        [8, 1, 6]
    ]

    /// 根据坐标获取洛书值
    static func luoshuValue(row: Int, col: Int) -> Int {
        let r = ((row % 3) + 3) % 3
        let c = ((col % 3) + 3) % 3
        return luoshu[r][c]
    }

    /// 洛书引力角度（地场骨架）
    static func luoshuAngle(x: Double, y: Double) -> Double {
        let gridX = Int(x / 3.0) % 3
        let gridY = Int(y / 3.0) % 3
        let val = Double(luoshu[((gridY % 3) + 3) % 3][((gridX % 3) + 3) % 3])
        return (val / 9.0) * 2.0 * .pi
    }

    // MARK: - ③ 太极递归 (Taiji Recursion)

    /// 太极生两仪·两仪生四象·四象生八卦
    /// 递归二叉树·与分治算法同构
    class TaijiNode {
        let value: String     // 阴或阳
        let level: Int        // 层级
        let yin: TaijiNode?   // 阴分支
        let yang: TaijiNode?  // 阳分支

        init(value: String, level: Int, yin: TaijiNode? = nil, yang: TaijiNode? = nil) {
            self.value = value
            self.level = level
            self.yin = yin
            self.yang = yang
        }
    }

    /// 生成太极递归树（到指定深度）
    static func generateTaiji(depth: Int, level: Int = 0, path: String = "☯") -> [String] {
        guard level < depth else { return [path] }
        let yinPaths = generateTaiji(depth: depth, level: level + 1, path: path + "⚋")
        let yangPaths = generateTaiji(depth: depth, level: level + 1, path: path + "⚊")
        return yinPaths + yangPaths
    }

    /// 八卦生成（深度3的太极递归=8种状态）
    static let bagua: [String] = [
        "☰ 乾", "☱ 兑", "☲ 离", "☳ 震",
        "☴ 巽", "☵ 坎", "☶ 艮", "☷ 坤"
    ]

    // MARK: - ④ 三才流场 (SanCai Flow Field)

    /// 三才向量合成
    /// angle = atan2(sin天*w天 + sin地*w地 + sin人*w人, cos...)
    struct SanCaiVector {
        let angle: Double     // 方向
        let strength: Double  // 强度
        let resonance: Int    // 洛书共振值
    }

    /// 计算三才流场
    /// - 天=Perlin噪声(自然随机) 权重0.35
    /// - 地=洛书引力(空间结构) 权重0.15
    /// - 人=种子偏置(自由意志) 权重0.50
    static func sanCaiFlow(x: Double, y: Double, t: Double, humanSeed: Double) -> SanCaiVector {
        let wHeaven = 0.35
        let wEarth  = 0.15
        let wHuman  = 0.50

        // 天：Perlin噪声简化版
        let heavenAngle = sin(x * 0.1 + t) * cos(y * 0.1 + t * 0.7)

        // 地：洛书引力
        let earthAngle = luoshuAngle(x: x, y: y)

        // 人：种子偏置
        let humanAngle = humanSeed + t * 0.5

        // 向量合成
        let sinX = sin(heavenAngle) * wHeaven + sin(earthAngle) * wEarth + sin(humanAngle) * wHuman
        let cosX = cos(heavenAngle) * wHeaven + cos(earthAngle) * wEarth + cos(humanAngle) * wHuman

        return SanCaiVector(
            angle: atan2(sinX, cosX),
            strength: sqrt(sinX * sinX + cosX * cosX),
            resonance: digitalRoot(Int(t * 9))
        )
    }

    // MARK: - ⑤ 时间压缩 L5 (Time Compression)

    /// E = R × I × T^(-α)
    /// R=影响范围 I=重要性 α=衰减指数 T=天数
    static func energyField(R: Double, I: Double, T: Double, alpha: Double) -> Double {
        guard alpha > 0.0001 else { return R * I } // L0永恒层·不衰减
        return R * I * pow(T, -alpha)
    }

    /// 半衰期 = 2^(1/α)
    static func halfLife(alpha: Double) -> Double {
        guard alpha > 0.0001 else { return .infinity }
        return pow(2.0, 1.0 / alpha)
    }

    /// 百年后保留率
    static func retentionAfter100Years(alpha: Double) -> Double {
        return pow(36500.0, -alpha) * 100.0
    }

    /// L5五层时间架构
    enum TimeLayer: String, CaseIterable {
        case L0_eternal  = "L0·永恒层(α=0)"
        case L1_century  = "L1·百年层(α=0.01)"
        case L2_decade   = "L2·十年层(α=0.1)"
        case L3_daily    = "L3·日常层(α=1.0)"
        case L4_instant  = "L4·瞬时层(α→∞)"

        var alpha: Double {
            switch self {
            case .L0_eternal: return 0
            case .L1_century: return 0.01
            case .L2_decade:  return 0.1
            case .L3_daily:   return 1.0
            case .L4_instant: return 100.0
            }
        }
    }

    // MARK: - ⑥ 信息熵 (Entropy)

    /// H = -Σ p(x) × log2(p(x))
    /// 混乱度越高信息量越大·低熵=有序=安全·高熵=混乱=风险
    static func entropy(_ probabilities: [Double]) -> Double {
        return -probabilities
            .filter { $0 > 0 }
            .map { $0 * log2($0) }
            .reduce(0, +)
    }

    /// 字符串熵（评估内容混乱度）
    static func stringEntropy(_ text: String) -> Double {
        var freq: [Character: Int] = [:]
        for char in text { freq[char, default: 0] += 1 }
        let total = Double(text.count)
        let probs = freq.values.map { Double($0) / total }
        return entropy(probs)
    }

    // MARK: - 三色审计枚举

    enum TriColor: String {
        case green  = "🟢"
        case yellow = "🟡"
        case red    = "🔴"
    }

    // MARK: - 七维SOUL评分

    /// SOUL = Σ(wᵢ × Eᵢ × Fuse)
    struct SevenDimScore {
        var tech:      Double = 0  // 技术主权 0.20
        var language:  Double = 0  // 语言主权 0.15
        var culture:   Double = 0  // 文化主权 0.20
        var data:      Double = 0  // 数据主权 0.15
        var decision:  Double = 0  // 决策主权 0.15
        var knowledge: Double = 0  // 知识主权 0.10
        var identity:  Double = 0  // 身份主权 0.05 (α=0 → ∞)

        var score: Double {
            return tech * 0.20 + language * 0.15 + culture * 0.20 +
                   data * 0.15 + decision * 0.15 + knowledge * 0.10 +
                   identity * 0.05
        }
    }
}
