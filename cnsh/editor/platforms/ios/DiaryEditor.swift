// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-85087f6d
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
//龍芯⚡️2026-06-20-LONGHUN-DIARY-EDITOR
// 日记编辑器：支持文字+语音输入，自动带DNA追溯

import SwiftUI

struct 日记编辑器: View {
    @Environment(\.managedObjectContext) private var 上下文
    @Environment(\.dismiss) private var 关闭
    @State private var 内容 = ""
    @State private var 语音输入中 = false
    @StateObject private var 农历 = 农历引擎()
    
    var body: some View {
        NavigationView {
            VStack(spacing: 12) {
                // 农历日期显示
                HStack {
                    Text(农历.农历年月(Date()))
                        .font(.headline).foregroundColor(.orange)
                    Text(农历.农历日(Date()))
                        .font(.subheadline).foregroundColor(.gray)
                    Spacer()
                    Text(Date().formatted(date: .abbreviated, time: .shortened))
                        .font(.caption).foregroundColor(.gray)
                }
                .padding(.horizontal)
                
                // 编辑区
                TextEditor(text: $内容)
                    .font(.body)
                    .padding(8)
                    .overlay(RoundedRectangle(cornerRadius: 12).stroke(Color.orange.opacity(0.3), lineWidth: 1))
                    .frame(maxHeight: .infinity)
                    .padding(.horizontal)
                
                // 语音按钮
                Button(action: { 语音输入中.toggle() }) {
                    HStack {
                        Image(systemName: 语音输入中 ? "mic.fill" : "mic")
                        Text(语音输入中 ? "🎙️ 语音输入中..." : "🎤 语音输入")
                    }
                    .foregroundColor(语音输入中 ? .red : .orange)
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(语音输入中 ? Color.red.opacity(0.1) : Color.orange.opacity(0.1))
                    .cornerRadius(12)
                }
                .padding(.horizontal)
                
                // DNA预览
                HStack {
                    Text("🧬")
                    Text(DNA追溯器.生成DNA(模块: "DIARY-ENTRY", 版本: "v1.0"))
                        .font(.system(size: 9, design: .monospaced))
                        .foregroundColor(.gray.opacity(0.6))
                        .lineLimit(1)
                }
                .padding(.horizontal)
                
                Spacer()
            }
            .navigationTitle("写日记")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("取消") { 关闭() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("保存") { 保存日记() }
                        .disabled(内容.isEmpty)
                }
            }
        }
    }
    
    private func 保存日记() {
        let 新条目 = 日记条目(context: 上下文)
        新条目.id = UUID()
        新条目.时间戳 = Date()
        新条目.内容 = 内容
        新条目.农历日期 = 农历.农历年月(Date()) + 农历.农历日(Date())
        新条目.dna追溯 = DNA追溯器.生成DNA(模块: "DIARY-ENTRY", 版本: "v1.0")
        新条目.指纹 = DNA追溯器.压缩指纹(原文: 内容)
        新条目.来源 = "本地"
        新条目.是否同步 = false  // 🔴 默认不同步
        
        do {
            try 上下文.save()
            关闭()
        } catch {
            print("保存失败: \(error)")
        }
    }
}
