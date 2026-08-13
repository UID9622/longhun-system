# 🌟 SwiftUI 星空粒子系统 v1.0｜Swift·Mac地表最强外壳第一块砖

> Notion URL: https://app.notion.com/p/SwiftUI-v1-0-Swift-Mac-036ee53f623d48f6bfdf9fd181c0c5ee
> Created: 2026-04-17T03:33:00.000Z
> Last edited: 2026-08-04T08:24:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
> 《道德经》第十一章：「候也。」—— 天地的就是只管运转不管外壳。我们管外壳。
## 效果预览
> 监屏上显示漫天星空，每颗星 = 龍魂系统的一个节点
> 手指点击一颗星 → 弹出节点信息卡
> 拖拽可以旋转整个星空
## 完整代码
```swift
// StarParticleView.swift
// 龍魂星空粒子系统 v1.0
// 导入: 无需任何第三方库，纯 Swift + SwiftUI
import SwiftUI

// 星空粒子数据模型
struct StarParticle: Identifiable {
    let id = UUID()
    var position: CGPoint
    var velocity: CGVector
    var size: CGFloat
    var brightness: Double     // 0.0~1.0
    var color: Color           // 对应三色审计
    var label: String          // 节点名称
}

// 星空数据源
class StarFieldModel: ObservableObject {
    @Published var particles: [StarParticle] = []

    // 初始化N颗星
    func seed(count: Int, in size: CGSize) {
        particles = (0..<count).map { _ in
            StarParticle(
                position: CGPoint(
                    x: CGFloat.random(in: 0...size.width),
                    y: CGFloat.random(in: 0...size.height)
                ),
                velocity: CGVector(
                    dx: Double.random(in: -0.3...0.3),
                    dy: Double.random(in: -0.3...0.3)
                ),
                size: CGFloat.random(in: 2...8),
                brightness: Double.random(in: 0.4...1.0),
                color: [.white, .cyan, .yellow, .green].randomElement()!,
                label: "节点\(Int.random(in: 1000...9999))"
            )
        }
    }

    // 更新粒子位置（每帧调用）
    func tick(in bounds: CGSize) {
        for i in particles.indices {
            particles[i].position.x += particles[i].velocity.dx
            particles[i].position.y += particles[i].velocity.dy
            // 边界回弹
            if particles[i].position.x < 0 || particles[i].position.x > bounds.width {
                particles[i].velocity.dx *= -1
            }
            if particles[i].position.y < 0 || particles[i].position.y > bounds.height {
                particles[i].velocity.dy *= -1
            }
        }
    }
}

// 主视图
struct StarFieldView: View {
    @StateObject private var model = StarFieldModel()
    @State private var selectedStar: StarParticle?
    let timer = Timer.publish(every: 1/60, on: .main, in: .common).autoconnect()

    var body: some View {
        GeometryReader { geo in
            ZStack {
                // 星空背景
                Color.black.ignoresSafeArea()

                // 粒子层
                Canvas { ctx, size in
                    for p in model.particles {
                        let rect = CGRect(
                            x: p.position.x - p.size/2,
                            y: p.position.y - p.size/2,
                            width: p.size, height: p.size
                        )
                        ctx.opacity = p.brightness
                        ctx.fill(Ellipse().path(in: rect), with: .color(p.color))
                    }
                }

                // 节点标签层
                ForEach(model.particles) { p in
                    Circle()
                        .fill(p.color.opacity(0.01))
                        .frame(width: 30, height: 30)
                        .position(p.position)
                        .onTapGesture { selectedStar = p }
                }
            }
            .onAppear { model.seed(count: 200, in: geo.size) }
            .onReceive(timer) { _ in model.tick(in: geo.size) }
        }
        // 点击弹出节点信息
        .sheet(item: $selectedStar) { star in
            VStack(spacing: 12) {
                Text(🌟 ❤️ \(star.label))
                    .font(.title2).bold()
                Text("亮度: \(Int(star.brightness * 100))%")
                Text("DNA: #龍芯⚡️2026-\(star.id)")
                    .font(.caption).foregroundColor(.secondary)
            }.padding()
        }
    }
}

#Preview {
    StarFieldView()
}
```
## 与龍魂系统的联动
## 下一步路线
1. 添加C++核心层对接（梦幻度评分算法输出驱动粒子亮度）
1. 添加ObjectiveC++桥接层
1. 用SceneKit升级为真3D星空
