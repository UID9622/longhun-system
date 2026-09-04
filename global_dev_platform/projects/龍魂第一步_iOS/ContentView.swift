// 龍魂第一步 · iOS · 由龍魂全球开发者平台生成
// DNA: #龍芯⚡️丙午·丙申·己巳·辰时·☵坎-DEV-DEMO-龍魂第一步-v1.0-e1c6489c
// 创建者: UID9622
// 归属名: UID9622 · 龍芯北辰
// 模板: 待办事项 App（最经典的第一个 App）
// 技术栈: SwiftUI · List + Checkbox + CoreData
// 生成时间: 2026-08-23T07:08:20.168015

import SwiftUI

@main
struct 龍魂第一步App: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    // TODO: 在这里构建你的 龍魂第一步
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
            .navigationTitle("龍魂第一步")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}

#Preview {
    ContentView()
}
