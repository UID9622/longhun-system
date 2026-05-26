// MARK: - 龍魂「文字即權重」可視化系統 v1.0
//
// DNA: #龍芯⚡️2026-05-26-TEXT-AS-WEIGHT-VISUALIZATION-SWIFT-v1.0
// GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
// CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
//
// 向 Steve Jobs 致敬 | 曾仕强老師智慧 | 龍魂系統 UID9622·龍芯北辰
//
// 用途:
//   - SwiftUI實現權重跑馬燈和高亮色彩
//   - iOS/macOS應用中的「文字即權重」可視化
//   - 實時權重變化動畫展示
//

import SwiftUI
import Foundation

// MARK: - 五色系統定義

enum WuXingColor: String, CaseIterable {
    case wood = "木"      // 綠·青石·東
    case fire = "火"      // 紅·赤石·南
    case earth = "土"     // 黃·黃石·中
    case metal = "金"     // 金·金石·西
    case water = "水"     // 黑·玄石·北

    var emoji: String {
        switch self {
        case .wood: return "🟢"
        case .fire: return "🔴"
        case .earth: return "🟡"
        case .metal: return "🟡金"
        case .water: return "⚫"
        }
    }

    var color: Color {
        switch self {
        case .wood:
            return Color(red: 46/255.0, green: 139/255.0, blue: 87/255.0)
        case .fire:
            return Color(red: 220/255.0, green: 20/255.0, blue: 60/255.0)
        case .earth:
            return Color(red: 218/255.0, green: 165/255.0, blue: 32/255.0)
        case .metal:
            return Color(red: 255/255.0, green: 215/255.0, blue: 0/255.0)
        case .water:
            return Color(red: 25/255.0, green: 25/255.0, blue: 112/255.0)
        }
    }

    var stone: String {
        switch self {
        case .wood: return "青石"
        case .fire: return "赤石"
        case .earth: return "黃石"
        case .metal: return "金石"
        case .water: return "玄石"
        }
    }

    var direction: String {
        switch self {
        case .wood: return "東"
        case .fire: return "南"
        case .earth: return "中"
        case .metal: return "西"
        case .water: return "北"
        }
    }

    var flowField: String {
        switch self {
        case .wood: return "上升流"
        case .fire: return "爆發流"
        case .earth: return "旋渦流"
        case .metal: return "光明流"
        case .water: return "下沉流"
        }
    }
}

// MARK: - 五色級別

enum FiveColorLevel {
    case green      // 🟢 R < 0.30
    case yellow     // 🟡 0.30 ≤ R < 0.67
    case red        // 🔴 0.67 ≤ R < 0.85
    case black      // ⚫ 不可計算
    case gold       // 🟡金 超規則

    var emoji: String {
        switch self {
        case .green: return "🟢"
        case .yellow: return "🟡"
        case .red: return "🔴"
        case .black: return "⚫"
        case .gold: return "🟡金"
        }
    }

    var name: String {
        switch self {
        case .green: return "綠·自由意志態"
        case .yellow: return "黃·老好人態"
        case .red: return "紅·越界態"
        case .black: return "黑·未明徵兆"
        case .gold: return "金·主控保留權"
        }
    }

    var meaning: String {
        switch self {
        case .green: return "自由意志態·安全·常態·可自動放行"
        case .yellow: return "老好人態/未明朗·需複核·可繼續但記錄"
        case .red: return "真負責者越界態/極端緊急·阻斷·人工介入"
        case .black: return "檢測不出·未明徵兆·灰色相遇·黑箱嫌疑"
        case .gold: return "主控保留權·一票否決/一票通過·凌駕任何R公式"
        }
    }

    var action: String {
        switch self {
        case .green: return "直接執行·留痕·不打擾"
        case .yellow: return "二次確認·要求加證據·記入審計日誌"
        case .red: return "立即停止·上報老大·觸發§8.5極端態協議"
        case .black: return "標記隔離·進觀察池·冻结24h"
        case .gold: return "主控簽字·覆蓋任何R判定·DNA永存"
        }
    }
}

// MARK: - 權重因子結構

struct WeightFactors {
    var proximity: Double      // 接近度
    var capability: Double     // 能力
    var knowledge: Double      // 知識
    var duty: Double          // 責任
    var consent: Double       // 同意
    var alternatives: Double  // 替代方案
    var cost: Double         // 成本

    var all: [Double] {
        [proximity, capability, knowledge, duty, consent, alternatives, cost]
    }

    var average: Double {
        all.reduce(0, +) / Double(all.count)
    }
}

// MARK: - 責任係數結果

struct ResponsibilityCoefficientResult {
    let rValue: Double?
    let colorLevel: FiveColorLevel
    let reasoning: String
    let action: String
    let nextStep: String
    let dnaTrace: String
    let timestamp: Date

    var formattedRValue: String {
        if let r = rValue {
            return String(format: "%.2f", r)
        }
        return "N/A (超規則)"
    }
}

// MARK: - 主要可視化引擎

class TextAsWeightVisualizer: ObservableObject {
    // MARK: - R公式常數

    static let rFormulaWeights: [String: Double] = [
        "F2_sharpness": 0.4,
        "F6_long_term": 0.4,
        "F3_density": 0.2,
        "F1_absence": -0.5,
        "F5_pleasing": -0.3,
    ]

    // MARK: - 五色閾值

    static let threshGreenTop = 0.30
    static let threshYellowTop = 0.67
    static let threshRedTop = 0.85

    // MARK: - 關鍵詞

    static let immovablePoints: [String: String] = [
        ",,,": "三逗號思考暫停",
        "宝宝": "特定含義",
        "龍": "繁體永不簡化",
        "是吧": "口語特徵",
        "CONFIRM": "確認碼風格",
    ]

    // MARK: - 計算責任係數

    func calculateResponsibilityCoefficient(
        factors: WeightFactors,
        override: String? = nil
    ) -> ResponsibilityCoefficientResult {
        // 金色覆蓋
        if override == "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z" {
            return ResponsibilityCoefficientResult(
                rValue: nil,
                colorLevel: .gold,
                reasoning: "主控CONFIRM覆蓋·超規則保留權",
                action: "主控簽字·覆蓋任何R判定",
                nextStep: "執行主控意願·留痕·記入DNA",
                dnaTrace: "#龍芯⚡️2026-05-26-GOLD-OVERRIDE",
                timestamp: Date()
            )
        }

        // 計算R值
        // 簡化版本·實際應使用F2/F3/F5/F6因子
        let rValue = (
            factors.knowledge * Self.rFormulaWeights["F2_sharpness"]! +
            factors.knowledge * Self.rFormulaWeights["F6_long_term"]! +
            factors.duty * Self.rFormulaWeights["F3_density"]! -
            factors.proximity * Self.rFormulaWeights["F1_absence"]! -
            factors.consent * Self.rFormulaWeights["F5_pleasing"]!
        )

        let clampedR = max(0.0, min(1.0, rValue))
        let colorLevel = mapRToColor(clampedR)
        let (reasoning, action, nextStep) = generateActions(clampedR, colorLevel)

        return ResponsibilityCoefficientResult(
            rValue: clampedR,
            colorLevel: colorLevel,
            reasoning: reasoning,
            action: action,
            nextStep: nextStep,
            dnaTrace: "#龍芯⚡️2026-05-26-R-\(String(format: "%.2f", clampedR))",
            timestamp: Date()
        )
    }

    // MARK: - 將R值映射到五色級別

    func mapRToColor(_ rValue: Double) -> FiveColorLevel {
        if rValue < Self.threshGreenTop {
            return .green
        } else if rValue < Self.threshYellowTop {
            return .yellow
        } else if rValue < Self.threshRedTop {
            return .red
        } else {
            return .black
        }
    }

    // MARK: - 生成動作說明

    func generateActions(
        _ rValue: Double,
        _ colorLevel: FiveColorLevel
    ) -> (String, String, String) {
        switch colorLevel {
        case .green:
            return ("自由意志態·安全", "直接執行·留痕·不打擾", "執行操作·記錄在案")
        case .yellow:
            return ("老好人態·需複核", "二次確認·要求加證據", "等待確認·記入審計日誌")
        case .red:
            return ("越界態·極端緊急", "立即停止·上報老大", "觸發§8.5極端態協議")
        case .black:
            return ("未明徵兆·黑箱嫌疑", "標記隔離·進觀察池", "冻结24h·等待更多證據")
        case .gold:
            return ("主控保留權", "主控簽字·覆蓋任何R判定", "金色判決·不可上訴")
        }
    }

    // MARK: - 計算亮度·根據權重大小

    func calculateBrightnessForWeight(_ rValue: Double) -> Double {
        // 基礎亮度(0.3~1.0)
        let baseBrightness = 0.3 + 0.7 * rValue

        // 貝塞爾曲線調整·權重高時峰值更高
        let bezierFactor =
            3 * (1 - rValue) * (1 - rValue) * rValue + (rValue * rValue * rValue)
        let finalBrightness = baseBrightness + 0.2 * bezierFactor

        return min(1.0, finalBrightness)
    }

    // MARK: - 色彩插值·跑馬燈用

    func interpolateColor(rValue: Double, progress: Double) -> Color {
        // 綠→黃→紅漸變
        let baseColor: (Double, Double, Double)
        if rValue < Self.threshGreenTop {
            baseColor = (46.0/255.0, 139.0/255.0, 87.0/255.0)  // 綠
        } else if rValue < Self.threshYellowTop {
            baseColor = (218.0/255.0, 165.0/255.0, 32.0/255.0)  // 黃
        } else {
            baseColor = (220.0/255.0, 20.0/255.0, 60.0/255.0)   // 紅
        }

        // 根據進度調整亮度
        let brightness = 0.6 + 0.4 * sin(progress * .pi)

        return Color(
            red: baseColor.0 * brightness,
            green: baseColor.1 * brightness,
            blue: baseColor.2 * brightness
        )
    }
}

// MARK: - SwiftUI 視圖組件

struct TextAsWeightMarqueeView: View {
    let text: String
    let rValue: Double
    @State private var offset: CGFloat = 0

    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 10) {
                ForEach(0..<100, id: \.self) { _ in
                    Text(text)
                        .font(.system(size: 16, weight: .semibold, design: .monospaced))
                        .foregroundColor(
                            Color(
                                red: interpolatedColor().0,
                                green: interpolatedColor().1,
                                blue: interpolatedColor().2
                            )
                        )
                }
            }
            .offset(x: offset)
        }
        .onAppear {
            startMarquee()
        }
    }

    private func interpolatedColor() -> (Double, Double, Double) {
        if rValue < 0.30 {
            return (46.0/255.0, 139.0/255.0, 87.0/255.0)   // 綠
        } else if rValue < 0.67 {
            return (218.0/255.0, 165.0/255.0, 32.0/255.0)  // 黃
        } else {
            return (220.0/255.0, 20.0/255.0, 60.0/255.0)   // 紅
        }
    }

    private func startMarquee() {
        withAnimation(.linear(duration: 10).repeatForever(autoreverses: false)) {
            offset = 500
        }
    }
}

struct ResponsibilityCoefficientView: View {
    let result: ResponsibilityCoefficientResult

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(result.colorLevel.emoji)
                    .font(.system(size: 24))
                VStack(alignment: .leading, spacing: 4) {
                    Text(result.colorLevel.name)
                        .font(.headline)
                    Text("R值: \(result.formattedRValue)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                Spacer()
            }

            Divider()

            VStack(alignment: .leading, spacing: 8) {
                Label(result.reasoning, systemImage: "lightbulb.fill")
                Label(result.action, systemImage: "gearshape.fill")
                Label(result.nextStep, systemImage: "arrow.right.circle.fill")
            }
            .font(.subheadline)

            Divider()

            Text("DNA追蹤: \(result.dnaTrace)")
                .font(.caption2)
                .foregroundColor(.secondary)
                .lineLimit(1)
        }
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(8)
    }
}

// MARK: - 預覽

#if DEBUG
struct TextAsWeightVisualization_Previews: PreviewProvider {
    static var previews: some View {
        VStack(spacing: 20) {
            // 預覽1: 跑馬燈
            TextAsWeightMarqueeView(text: "龍魂系統·文字即權重", rValue: 0.45)
                .frame(height: 40)
                .background(Color.black)

            // 預覽2: 責任係數結果
            let visualizer = TextAsWeightVisualizer()
            let factors = WeightFactors(
                proximity: 0.8,
                capability: 0.9,
                knowledge: 0.7,
                duty: 0.6,
                consent: 0.5,
                alternatives: 0.4,
                cost: 0.3
            )
            let result = visualizer.calculateResponsibilityCoefficient(factors: factors)

            ResponsibilityCoefficientView(result: result)
        }
        .padding()
    }
}
#endif
