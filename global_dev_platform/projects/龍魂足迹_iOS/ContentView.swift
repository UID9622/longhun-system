// 龍魂足迹 · iOS · 由龍魂全球开发者平台生成
// DNA: #龍芯⚡️丙午·丙申·戊辰·亥时·☵坎-DEV-DEMO-龍魂足迹-v1.0-def356ee
// 创建者: UID9622
// 归属名: UID9622 · 龍芯北辰
// 模板: 全球足迹地图（标记你去过的地方）
// 技术栈: SwiftUI · MapKit + CoreLocation
// 生成时间: 2026-08-22T22:15:45.253173

import SwiftUI

@main
struct 龍魂足迹App: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    // TODO: 在这里构建你的 龍魂足迹
    // 这是你在这个世界留下的第一行代码 🌍
    @State private var items: [String] = []
    @State private var newItem: String = ""

    var body: some View {
        NavigationStack {
            VStack {
                HStack {
                    TextField("输入你的想法...", text: $newItem)
                        .textFieldStyle(.roundedBorder)
                    Button("添加") {
                        if !newItem.isEmpty {
                            items.append(newItem)
                            newItem = ""
                        }
                    }
                }
                .padding()

                List(items, id: \.self) { item in
                    Text(item)
                }
            }
            .navigationTitle("龍魂足迹")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}

#Preview {
    ContentView()
}
