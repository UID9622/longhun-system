// ═══════════════════════════════════════════════════════════════
//  龍魂·算法时空景观 · Scene3DView.swift
//
//  核心思路：
//    X轴 = 数组索引（0→n）
//    Y轴 = 元素值（高度）
//    Z轴 = 时间帧（混沌 → 秩序）
//
//  效果：每一帧排序状态变成一层，叠成3D山脉
//        前面是随机乱山，后面是完美斜坡
//        可以飞进去、掰开看、绕着转
//
//  操作：鼠标拖拽旋转 · 右键拖拽平移 · 滚轮缩放
// ═══════════════════════════════════════════════════════════════

import SceneKit
import SwiftUI

// MARK: ── 3D 时空全景主视图 ────────────────────────────────────

struct AlgoLandscape3D: View {
    let frames:  [SortFrame]
    let algo:    SortAlgo

    @State private var scene:     SCNScene?   = nil
    @State private var building:  Bool        = true
    @State private var progress:  String      = "初始化…"
    @State private var timeSlice: Double      = 1.0   // 0~1, 切片位置

    var body: some View {
        ZStack {
            // ── 3D 场景
            if let scene {
                SceneKitView(scene: scene)
                    .ignoresSafeArea()
            }

            // ── 构建中遮罩
            if building {
                LoadingOverlay(message: progress)
            }

            // ── 顶部 HUD
            if !building {
                VStack {
                    HUD3D(algo: algo, frameCount: frames.count)
                    Spacer()
                    Instructions3D()
                }
                .padding(16)
            }
        }
        .task {
            await buildLandscape()
        }
    }

    // ── 异步构建场景（后台线程，不卡UI）
    func buildLandscape() async {
        building = true
        let f = frames
        let a = algo
        let built = await Task.detached(priority: .userInitiated) {
            LandscapeBuilder.build(frames: f, algo: a)
        }.value
        await MainActor.run {
            scene = built
            building = false
        }
    }
}

// MARK: ── 场景构建器 ──────────────────────────────────────────

enum LandscapeBuilder {

    static func build(frames: [SortFrame], algo: SortAlgo) -> SCNScene {
        let scene = SCNScene()
        scene.background.contents = NSColor(red: 0.025, green: 0.014, blue: 0.075, alpha: 1)

        // ── 采样帧（最多 160 帧，性能与细节平衡）
        let maxF = 160
        let step = max(1, frames.count / maxF)
        var sampled: [SortFrame] = []
        for i in stride(from: 0, to: frames.count - 1, by: step) {
            sampled.append(frames[i])
        }
        if let last = frames.last { sampled.append(last) }

        let n  = sampled.first?.array.count ?? 1
        let nf = sampled.count
        let cell: Float = 0.6
        let maxH: Float = 12.0
        let halfW = Float(n - 1) * cell / 2
        let halfD = Float(nf - 1) * cell / 2

        // ── 批量创建 Bar 节点（合并材质减少 draw call）
        // 按颜色分组
        var goldNodes    = [SCNNode]()
        var cyanNodes    = [SCNNode]()
        var orangeNodes  = [SCNNode]()
        var redNodes     = [SCNNode]()
        var baseNodes    = [SCNNode]()   // 用顶点色区分

        for (fi, frame) in sampled.enumerated() {
            let zPos = Float(fi) * cell - halfD

            for i in 0..<n {
                let val = Float(frame.array[i]) / Float(n)
                let h   = max(0.06, val * maxH)
                let xPos = Float(i) * cell - halfW
                let yPos = h / 2

                let geo = SCNBox(width:  CGFloat(cell * 0.82),
                                 height: CGFloat(h),
                                 length: CGFloat(cell * 0.82),
                                 chamferRadius: 0.018)

                let node = SCNNode(geometry: geo)
                node.position = SCNVector3(xPos, yPos, zPos)

                // 分类
                if frame.sorted.contains(i)    { goldNodes.append(node) }
                else if frame.swapping.contains(i) { orangeNodes.append(node) }
                else if frame.pivot == i       { redNodes.append(node) }
                else if frame.comparing.contains(i) { cyanNodes.append(node) }
                else {
                    // 用高度调色
                    let mat = SCNMaterial()
                    mat.diffuse.contents = NSColor(
                        red:   CGFloat(0.16 + 0.14 * val),
                        green: CGFloat(0.20 + 0.18 * val),
                        blue:  CGFloat(0.38 + 0.22 * val),
                        alpha: 1.0
                    )
                    mat.specular.contents = NSColor(white: 0.25, alpha: 1)
                    mat.lightingModel = .phong
                    geo.materials = [mat]
                    baseNodes.append(node)
                }
            }
        }

        // ── 批量应用共享材质（大幅提升性能）
        let matGold   = sharedMat(NSColor(red: 1.00, green: 0.84, blue: 0.00, alpha: 1))
        let matCyan   = sharedMat(NSColor(red: 0.26, green: 0.80, blue: 1.00, alpha: 1))
        let matOrange = sharedMat(NSColor(red: 0.95, green: 0.50, blue: 0.18, alpha: 1))
        let matRed    = sharedMat(NSColor(red: 1.00, green: 0.25, blue: 0.12, alpha: 1))

        func applyAndAdd(_ nodes: [SCNNode], mat: SCNMaterial) {
            for nd in nodes {
                (nd.geometry as? SCNBox)?.materials = [mat]
                scene.rootNode.addChildNode(nd)
            }
        }
        applyAndAdd(goldNodes,   mat: matGold)
        applyAndAdd(cyanNodes,   mat: matCyan)
        applyAndAdd(orangeNodes, mat: matOrange)
        applyAndAdd(redNodes,    mat: matRed)
        for nd in baseNodes { scene.rootNode.addChildNode(nd) }

        // ── 地板
        let floorGeo = SCNFloor()
        floorGeo.reflectivity = 0.06
        let floorMat = SCNMaterial()
        floorMat.diffuse.contents = NSColor(red: 0.04, green: 0.025, blue: 0.10, alpha: 1)
        floorGeo.materials = [floorMat]
        scene.rootNode.addChildNode(SCNNode(geometry: floorGeo))

        // ── 时间轴边框线（Z轴两端）
        addAxisLine(from: SCNVector3(-halfW, 0.02, -halfD),
                    to:   SCNVector3( halfW, 0.02, -halfD),
                    color: NSColor(red: 1, green: 0.3, blue: 0.1, alpha: 0.7),
                    scene: scene)
        addAxisLine(from: SCNVector3(-halfW, 0.02, halfD),
                    to:   SCNVector3( halfW, 0.02, halfD),
                    color: NSColor(red: 1, green: 0.84, blue: 0, alpha: 0.8),
                    scene: scene)

        // ── 3D 文字标签
        addFloatingText("混沌·开始", at: SCNVector3(-halfW - 1.5, 0.4, -halfD),
                        color: NSColor(red: 1, green: 0.4, blue: 0.1, alpha: 1),
                        size: 0.7, scene: scene)
        addFloatingText("秩序·完成", at: SCNVector3(-halfW - 1.5, 0.4, halfD),
                        color: NSColor(red: 1, green: 0.84, blue: 0, alpha: 1),
                        size: 0.7, scene: scene)
        addFloatingText(algo.rawValue,
                        at: SCNVector3(0, maxH + 3.5, 0),
                        color: NSColor(red: 1, green: 0.84, blue: 0, alpha: 1),
                        size: 1.4, scene: scene)
        addFloatingText(algo.complexity,
                        at: SCNVector3(0, maxH + 2.0, 0),
                        color: NSColor(white: 0.55, alpha: 1),
                        size: 0.7, scene: scene)

        // ── 环境粒子（星尘感）
        addStardust(scene: scene, halfW: halfW, halfD: halfD, maxH: maxH)

        // ── 灯光
        let ambient = SCNNode(); ambient.light = SCNLight()
        ambient.light!.type  = .ambient
        ambient.light!.color = NSColor(white: 0.30, alpha: 1)
        scene.rootNode.addChildNode(ambient)

        let sun = SCNNode(); sun.light = SCNLight()
        sun.light!.type        = .directional
        sun.light!.color       = NSColor(white: 0.80, alpha: 1)
        sun.light!.castsShadow = false   // 关阴影提升性能
        sun.position = SCNVector3(halfW * 2, maxH * 2.5, halfD * 2)
        sun.look(at: SCNVector3(0, 0, 0))
        scene.rootNode.addChildNode(sun)

        let fill = SCNNode(); fill.light = SCNLight()
        fill.light!.type  = .directional
        fill.light!.color = NSColor(red: 0.25, green: 0.35, blue: 0.80, alpha: 0.45)
        fill.position = SCNVector3(-halfW, maxH, -halfD * 2)
        fill.look(at: SCNVector3(0, 0, 0))
        scene.rootNode.addChildNode(fill)

        // ── 摄像机（初始视角：斜上方 45°，能看到完整山脉）
        let cam = SCNNode(); cam.camera = SCNCamera()
        cam.camera!.fieldOfView = 52
        cam.camera!.zFar        = 800
        let camDist = max(halfW, halfD) * 2.2
        cam.position = SCNVector3(camDist * 0.9, maxH * 1.8, halfD + camDist * 0.6)
        cam.look(at: SCNVector3(0, maxH * 0.25, 0))
        scene.rootNode.addChildNode(cam)

        return scene
    }

    // ── 共享材质工厂
    static func sharedMat(_ color: NSColor) -> SCNMaterial {
        let m = SCNMaterial()
        m.diffuse.contents  = color
        m.specular.contents = NSColor(white: 0.3, alpha: 1)
        m.lightingModel     = .phong
        return m
    }

    // ── 轴线
    static func addAxisLine(from a: SCNVector3, to b: SCNVector3,
                            color: NSColor, scene: SCNScene) {
        let verts: [SCNVector3] = [a, b]
        let src = SCNGeometrySource(vertices: verts)
        let idx: [Int32] = [0, 1]
        let element = SCNGeometryElement(indices: idx, primitiveType: .line)
        let geo = SCNGeometry(sources: [src], elements: [element])
        let mat = SCNMaterial(); mat.diffuse.contents = color
        mat.lightingModel = .constant
        geo.materials = [mat]
        scene.rootNode.addChildNode(SCNNode(geometry: geo))
    }

    // ── 3D 浮动文字
    static func addFloatingText(_ text: String, at pos: SCNVector3,
                                 color: NSColor, size: CGFloat, scene: SCNScene) {
        let geo = SCNText(string: text, extrusionDepth: 0.04)
        geo.font     = NSFont.systemFont(ofSize: 10, weight: .bold)
        geo.flatness = 0.08
        let mat = SCNMaterial()
        mat.diffuse.contents = color
        mat.lightingModel    = .constant
        geo.materials = [mat]

        let node = SCNNode(geometry: geo)
        let s = Float(size) * 0.065
        node.scale = SCNVector3(s, s, s)

        // 近似居中
        let w = Float(text.count) * s * 5.5
        node.position = SCNVector3(pos.x - w / 2, pos.y, pos.z)

        // 始终面向摄像机的 Billboard 约束
        let bill = SCNBillboardConstraint()
        bill.freeAxes = .Y
        node.constraints = [bill]

        scene.rootNode.addChildNode(node)
    }

    // ── 星尘粒子
    static func addStardust(scene: SCNScene, halfW: Float, halfD: Float, maxH: Float) {
        let ps = SCNParticleSystem()
        ps.birthRate        = 8
        ps.particleLifeSpan = 6
        ps.particleSize     = 0.06
        ps.emittingDirection = SCNVector3(0, -1, 0)
        ps.spreadingAngle   = 180
        ps.particleColor    = NSColor(red: 0.6, green: 0.7, blue: 1.0, alpha: 0.4)
        ps.isAffectedByGravity = false
        let emitter = SCNNode()
        emitter.position = SCNVector3(0, maxH * 2.5, 0)
        emitter.addParticleSystem(ps)
        scene.rootNode.addChildNode(emitter)
    }
}

// MARK: ── SceneKit NSView 包装 ────────────────────────────────

struct SceneKitView: NSViewRepresentable {
    let scene: SCNScene

    func makeNSView(context: Context) -> SCNView {
        let v = SCNView()
        v.scene               = scene
        v.allowsCameraControl = true    // 内建轨道摄像机，直接拖拽旋转
        v.showsStatistics     = false
        v.antialiasingMode    = .multisampling4X
        v.preferredFramesPerSecond = 60
        v.backgroundColor     = NSColor(red: 0.025, green: 0.014, blue: 0.075, alpha: 1)
        return v
    }

    func updateNSView(_ nsView: SCNView, context: Context) {
        if nsView.scene !== scene { nsView.scene = scene }
    }
}

// MARK: ── HUD 覆盖层 ──────────────────────────────────────────

struct HUD3D: View {
    let algo: SortAlgo
    let frameCount: Int

    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 3) {
                Text("🌌 3D时空全景·\(algo.emoji)\(algo.rawValue)")
                    .font(.system(size: 13, weight: .black))
                    .foregroundColor(.init(red: 1, green: 0.84, blue: 0))
                Text("X轴=索引 · Y轴=值 · Z轴=时间  ·  共 \(frameCount) 帧 → \(min(frameCount, 160)) 切片")
                    .font(.system(size: 10, design: .monospaced))
                    .foregroundColor(.init(white: 0.45))
            }
            .padding(.horizontal, 12).padding(.vertical, 8)
            .background(.ultraThinMaterial)
            .clipShape(RoundedRectangle(cornerRadius: 8))
            Spacer()
        }
    }
}

struct Instructions3D: View {
    var body: some View {
        HStack {
            Spacer()
            VStack(alignment: .trailing, spacing: 3) {
                ForEach(["左键拖·旋转", "右键拖·平移", "滚轮·缩放", "双击·复位"], id: \.self) { tip in
                    Text(tip)
                        .font(.system(size: 10, design: .monospaced))
                        .foregroundColor(.init(white: 0.35))
                }
            }
            .padding(.horizontal, 10).padding(.vertical, 8)
            .background(.ultraThinMaterial)
            .clipShape(RoundedRectangle(cornerRadius: 8))
        }
    }
}

// MARK: ── 加载遮罩 ────────────────────────────────────────────

struct LoadingOverlay: View {
    let message: String
    var body: some View {
        ZStack {
            Color(red: 0.025, green: 0.014, blue: 0.075)
                .ignoresSafeArea()
            VStack(spacing: 20) {
                Text("🌌").font(.system(size: 52))
                    .shadow(color: .init(red: 1, green: 0.84, blue: 0).opacity(0.8), radius: 20)
                ProgressView()
                    .scaleEffect(1.4)
                    .tint(.init(red: 1, green: 0.84, blue: 0))
                Text("正在折叠算法时空…")
                    .font(.system(size: 15, weight: .bold))
                    .foregroundColor(.init(red: 1, green: 0.84, blue: 0))
                Text(message)
                    .font(.system(size: 11, design: .monospaced))
                    .foregroundColor(.init(white: 0.4))
                Text("将所有排序帧叠成3D山脉")
                    .font(.system(size: 11))
                    .foregroundColor(.init(white: 0.3))
            }
        }
    }
}
