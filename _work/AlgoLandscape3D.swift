import SwiftUI
import SceneKit

// ═══════════════════════════════════════════════════════════════════════════
// 🐉 龍魂 · 算法3D时空全景 v1.0
// Algorithm Landscape 3D - Time Space Full Panorama
//
// DNA追溯碼：#龍芯⚡️2026-05-27-ALGO-3D-LANDSCAPE-v1.0
// CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
// GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
//
// 功能：
//   - 把排序过程的每一帧都映射成一个时间切面
//   - 形成从"无序山脉" → "有序金字塔"的视觉变换
//   - 支持自动旋转摄像机 + 手势拖拽控制
//   - 实时渲染 + 动态材质
// ═══════════════════════════════════════════════════════════════════════════

struct AlgoLandscape3D: View {
    let frames: [SortFrame]
    let algo: SortAlgo

    @State private var sceneView: SCNView?
    @State private var cameraRotation: CGFloat = 0
    @State private var isAutoRotating: Bool = true
    @State private var touchStartLocation: CGPoint = .zero

    var body: some View {
        ZStack {
            // 3D场景
            AlgoSceneWrapper(
                frames: frames,
                cameraRotation: $cameraRotation,
                isAutoRotating: $isAutoRotating
            )
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        if touchStartLocation == .zero {
                            touchStartLocation = value.startLocation
                        }
                        let delta = value.location.x - touchStartLocation.x
                        cameraRotation = CGFloat(delta) * 0.01
                    }
                    .onEnded { _ in
                        touchStartLocation = .zero
                        isAutoRotating = true
                    }
            )

            // 右下角控制面板
            VStack(alignment: .trailing, spacing: 10) {
                Spacer()

                HStack(spacing: 10) {
                    Spacer()

                    VStack(spacing: 8) {
                        // 旋转开关
                        Button {
                            isAutoRotating.toggle()
                        } label: {
                            Image(systemName: isAutoRotating ? "pause.circle.fill" : "play.circle.fill")
                                .font(.system(size: 22))
                                .foregroundColor(isAutoRotating ? T.gold : T.cyan)
                                .frame(width: 44, height: 44)
                                .background(T.surface.opacity(0.8))
                                .cornerRadius(10)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 10)
                                        .stroke(T.border, lineWidth: 1)
                                )
                        }

                        // 重置视角
                        Button {
                            cameraRotation = 0
                            isAutoRotating = true
                        } label: {
                            Image(systemName: "arrow.counterclockwise.circle.fill")
                                .font(.system(size: 22))
                                .foregroundColor(T.cyan)
                                .frame(width: 44, height: 44)
                                .background(T.surface.opacity(0.8))
                                .cornerRadius(10)
                                .overlay(
                                    RoundedRectangle(cornerRadius: 10)
                                        .stroke(T.border, lineWidth: 1)
                                )
                        }

                        // 信息面板
                        VStack(alignment: .trailing, spacing: 4) {
                            Text("🌌 3D全景")
                                .font(.system(size: 10, weight: .bold))
                                .foregroundColor(T.gold)
                            Text(algo.rawValue)
                                .font(.system(size: 9, design: .monospaced))
                                .foregroundColor(T.sub)
                            Text("帧数: \(frames.count)")
                                .font(.system(size: 9, design: .monospaced))
                                .foregroundColor(T.cyan)
                            Text(isAutoRotating ? "自动旋转" : "手动控制")
                                .font(.system(size: 8, design: .monospaced))
                                .foregroundColor(isAutoRotating ? T.gold : T.cyan)
                        }
                        .padding(8)
                        .background(T.panel.opacity(0.9))
                        .cornerRadius(8)
                        .overlay(
                            RoundedRectangle(cornerRadius: 8)
                                .stroke(T.border, lineWidth: 1)
                        )
                    }
                    .padding(12)
                }
            }
        }
        .background(Color(red: 0.025, green: 0.014, blue: 0.075))
    }
}

// MARK: - SceneKit 包装器

struct AlgoSceneWrapper: NSViewRepresentable {
    let frames: [SortFrame]
    @Binding var cameraRotation: CGFloat
    @Binding var isAutoRotating: Bool

    func makeNSView(context: Context) -> SCNView {
        let sceneView = SCNView()
        sceneView.scene = createAlgoScene(frames: frames)
        sceneView.autoenablesDefaultLighting = true
        sceneView.backgroundColor = NSColor(red: 0.025, green: 0.014, blue: 0.075, alpha: 1.0)
        sceneView.allowsCameraControl = false
        return sceneView
    }

    func updateNSView(_ nsView: SCNView, context: Context) {
        if let cameraNode = nsView.scene?.rootNode.childNode(withName: "camera", recursively: true) {
            // 更新摄像机旋转
            let rotation = Float(cameraRotation)
            cameraNode.eulerAngles.y = rotation

            // 自动旋转
            if isAutoRotating {
                var currentRotation = cameraNode.eulerAngles.y
                currentRotation += 0.01
                cameraNode.eulerAngles.y = currentRotation
            }
        }
    }

    typealias NSViewType = SCNView
}

// MARK: - 3D场景生成

func createAlgoScene(frames: [SortFrame]) -> SCNScene {
    let scene = SCNScene()
    scene.background.contents = NSColor(red: 0.025, green: 0.014, blue: 0.075, alpha: 1.0)

    // 摄像机
    let cameraNode = SCNNode()
    cameraNode.name = "camera"
    cameraNode.camera = SCNCamera()
    cameraNode.camera?.fieldOfView = 60
    cameraNode.position = SCNVector3(0, 30, 40)
    cameraNode.look(at: SCNVector3(0, 10, 0), up: SCNVector3(0, 1, 0), localFront: SCNVector3(0, 0, -1))
    scene.rootNode.addChildNode(cameraNode)

    // 灯光
    let lightNode = SCNNode()
    lightNode.light = SCNLight()
    lightNode.light?.type = .omnidirectional
    lightNode.light?.intensity = 1500
    lightNode.position = SCNVector3(20, 40, 20)
    scene.rootNode.addChildNode(lightNode)

    let ambientLight = SCNNode()
    ambientLight.light = SCNLight()
    ambientLight.light?.type = .ambient
    ambientLight.light?.color = NSColor(white: 0.4, alpha: 1.0)
    scene.rootNode.addChildNode(ambientLight)

    // 地面
    let groundGeometry = SCNPlane(width: 100, height: 100)
    groundGeometry.firstMaterial?.diffuse.contents = NSColor(red: 0.04, green: 0.025, blue: 0.11, alpha: 1.0)
    groundGeometry.firstMaterial?.specular.contents = NSColor(white: 0.1, alpha: 1.0)
    let groundNode = SCNNode(geometry: groundGeometry)
    groundNode.position = SCNVector3(0, -1, 0)
    groundNode.eulerAngles.x = -CGFloat.pi / 2
    scene.rootNode.addChildNode(groundNode)

    // 生成柱体群（时间切面）
    guard !frames.isEmpty else { return scene }

    let framesToShow = min(frames.count, 40)  // 最多显示40帧，避免过度渲染
    let step = max(1, frames.count / framesToShow)
    let maxVal = frames[0].array.max() ?? 100
    let n = frames[0].array.count

    var frameIndex: Int = 0
    for (displayIdx, frameIdx) in stride(from: 0, to: frames.count, by: step).enumerated() {
        let frame = frames[frameIdx]
        let z = CGFloat(displayIdx) * 2.0 - CGFloat(framesToShow) * 1.0  // 沿Z轴分布

        for (i, value) in frame.array.enumerated() {
            let x = CGFloat(i) * 1.5 - CGFloat(n) * 0.75
            let height = CGFloat(value) / CGFloat(maxVal) * 20.0
            let y = height / 2.0

            // 选择颜色
            let color: NSColor
            if frame.sorted.contains(i) {
                color = NSColor(red: 1.0, green: 0.84, blue: 0.0, alpha: 0.9)  // 金色·已排
            } else if frame.swapping.contains(i) {
                color = NSColor(red: 0.95, green: 0.5, blue: 0.18, alpha: 0.8)  // 橙色·交换
            } else if frame.comparing.contains(i) {
                color = NSColor(red: 0.26, green: 0.8, blue: 1.0, alpha: 0.8)   // 青色·比较
            } else if let pivot = frame.pivot, pivot == i {
                color = NSColor(red: 1.0, green: 0.25, blue: 0.12, alpha: 0.8)  // 红色·基准
            } else {
                // 渐变色（根据值的大小）
                let t = CGFloat(value) / CGFloat(maxVal)
                color = NSColor(
                    red: 0.18 + 0.12 * t,
                    green: 0.22 + 0.15 * t,
                    blue: 0.38 + 0.20 * t,
                    alpha: 0.7
                )
            }

            // 创建柱体（Box）
            let boxGeometry = SCNBox(
                width: 1.2,
                height: max(0.3, height),
                length: 1.2,
                chamferRadius: 0.05
            )
            boxGeometry.firstMaterial?.diffuse.contents = color
            boxGeometry.firstMaterial?.specular.contents = NSColor(white: 0.3, alpha: 1.0)
            boxGeometry.firstMaterial?.shininess = 100

            let boxNode = SCNNode(geometry: boxGeometry)
            boxNode.position = SCNVector3(x, y, Float(z))
            scene.rootNode.addChildNode(boxNode)
        }
    }

    return scene
}

// MARK: - Color辅助扩展

extension NSColor {
    convenience init(red: CGFloat, green: CGFloat, blue: CGFloat, alpha: CGFloat) {
        self.init(
            red: red / 255.0,
            green: green / 255.0,
            blue: blue / 255.0,
            alpha: alpha
        )
    }
}

// MARK: - 预览

#Preview {
    // 生成测试数据
    var testFrames: [SortFrame] = []
    var arr = Array(1...30).shuffled()
    var sorted = Set<Int>()

    // 简化的冒泡排序帧
    for i in 0..<arr.count {
        for j in 0..<(arr.count - i - 1) {
            var comparing = Set<Int>()
            comparing.insert(j)
            comparing.insert(j + 1)
            testFrames.append(SortFrame(
                array: arr,
                comparing: comparing,
                swapping: Set(),
                sorted: sorted,
                message: "比较中..."
            ))

            if arr[j] > arr[j+1] {
                arr.swapAt(j, j+1)
                testFrames.append(SortFrame(
                    array: arr,
                    swapping: Set([j, j+1]),
                    sorted: sorted,
                    message: "交换!"
                ))
            }
        }
        sorted.insert(arr.count - 1 - i)
    }

    return AlgoLandscape3D(frames: testFrames, algo: .bubble)
}
