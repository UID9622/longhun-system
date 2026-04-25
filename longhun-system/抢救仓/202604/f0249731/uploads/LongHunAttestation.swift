// LongHunAttestation.swift
// 龍魂·存证系统 v1.0
// DNA: #龍芯⚡️2026-03-14-ATTESTATION-v1.0
// 创始人: 诸葛鑫（UID9622）
// 理论指导: 曾仕强老师（永恒显示）
//
// 核心逻辑：
//   原文 → AES加密存本地 → SHA256哈希公开
//   验证时：本地解密原文 → 重算哈希 → 比对公开哈希
//   分享时：只给摘要+哈希+DNA码，原文不出本地

import SwiftUI
import CryptoKit
import Foundation

// MARK: - 存证引擎

struct 存证引擎 {
    
    /// 存证记录
    struct 存证记录: Codable, Identifiable {
        let id: String           // UUID
        let DNA追溯码: String
        let 时间戳: String
        let 摘要: String         // 公开（30字内语义摘要）
        let 内容哈希: String     // 公开（SHA256）
        let 加密内容: String     // 私有（AES加密后Base64）
        let 盐值: String         // 加密用
        let 创建者: String
    }
    
    // MARK: - 加密
    
    /// 用密码 + 盐值派生 AES 密钥
    private static func 派生密钥(密码: String, 盐: Data) -> SymmetricKey {
        // 简单 KDF：SHA256(密码 + 盐)
        var 数据 = Data(密码.utf8)
        数据.append(盐)
        let hash = SHA256.hash(data: 数据)
        return SymmetricKey(data: hash)
    }
    
    /// AES-GCM 加密
    static func 加密(原文: String, 密码: String) -> (密文Base64: String, 盐Base64: String)? {
        let 盐 = Data((0..<16).map { _ in UInt8.random(in: 0...255) })
        let 密钥 = 派生密钥(密码: 密码, 盐: 盐)
        
        guard let 明文数据 = 原文.data(using: .utf8),
              let 密封 = try? AES.GCM.seal(明文数据, using: 密钥)
        else { return nil }
        
        guard let 合并数据 = 密封.combined else { return nil }
        return (合并数据.base64EncodedString(), 盐.base64EncodedString())
    }
    
    /// AES-GCM 解密
    static func 解密(密文Base64: String, 盐Base64: String, 密码: String) -> String? {
        guard let 密文数据 = Data(base64Encoded: 密文Base64),
              let 盐 = Data(base64Encoded: 盐Base64)
        else { return nil }
        
        let 密钥 = 派生密钥(密码: 密码, 盐: 盐)
        
        guard let 密封盒 = try? AES.GCM.SealedBox(combined: 密文数据),
              let 明文数据 = try? AES.GCM.open(密封盒, using: 密钥)
        else { return nil }
        
        return String(data: 明文数据, encoding: .utf8)
    }
    
    // MARK: - 哈希
    
    /// SHA256 内容哈希（公开指纹）
    static func 计算哈希(_ 内容: String) -> String {
        let hash = SHA256.hash(data: Data(内容.utf8))
        return hash.map { String(format: "%02x", $0) }.joined()
    }
    
    // MARK: - DNA 追溯码
    
    static func 生成DNA() -> String {
        let fmt = DateFormatter()
        fmt.dateFormat = "yyyyMMdd-HHmmss"
        let 时间码 = fmt.string(from: Date())
        let 随机码 = String(format: "%04X", UInt16.random(in: 0...0xFFFF))
        return "#龍芯⚡️\(时间码)-ATT-\(随机码)"
    }
    
    // MARK: - 完整存证流程
    
    /// 创建存证：原文加密存本地，哈希公开
    static func 创建存证(原文: String, 摘要: String, 密码: String) -> 存证记录? {
        // 1. 加密原文
        guard let 加密结果 = 加密(原文: 原文, 密码: 密码) else { return nil }
        
        // 2. 计算原文哈希（公开指纹）
        let 哈希 = 计算哈希(原文)
        
        // 3. 生成DNA
        let DNA = 生成DNA()
        
        // 4. 时间戳
        let fmt = DateFormatter()
        fmt.locale = Locale(identifier: "zh_CN")
        fmt.dateFormat = "yyyy-MM-dd HH:mm:ss"
        let 时间 = fmt.string(from: Date())
        
        let 记录 = 存证记录(
            id: UUID().uuidString,
            DNA追溯码: DNA,
            时间戳: 时间,
            摘要: 摘要,
            内容哈希: 哈希,
            加密内容: 加密结果.密文Base64,
            盐值: 加密结果.盐Base64,
            创建者: "UID9622"
        )
        
        // 5. 存到本地
        存储管理器.保存(记录)
        
        return 记录
    }
    
    /// 验证存证：解密原文 → 重算哈希 → 比对
    static func 验证存证(记录: 存证记录, 密码: String) -> (通过: Bool, 原文: String?) {
        guard let 原文 = 解密(密文Base64: 记录.加密内容, 盐Base64: 记录.盐值, 密码: 密码)
        else { return (false, nil) }
        
        let 重算哈希 = 计算哈希(原文)
        let 通过 = 重算哈希 == 记录.内容哈希
        
        return (通过, 原文)
    }
    
    /// 生成可分享的公开摘要（不含原文和加密内容）
    static func 生成分享文本(记录: 存证记录) -> String {
        """
        ══════════════════════════
        龍魂存证 · 公开验证信息
        ══════════════════════════
        
        DNA追溯码：\(记录.DNA追溯码)
        存证时间：\(记录.时间戳)
        内容摘要：\(记录.摘要)
        内容哈希：\(记录.内容哈希)
        创建者：\(记录.创建者)
        
        ──────────────────────────
        原文已加密存储于创建者本地
        如需验证，请联系创建者提供原文
        验证方式：SHA256(原文) == 上述哈希
        ──────────────────────────
        
        龍魂系统 · 数据主权 · 不可篡改
        GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
        """
    }
}

// MARK: - 本地存储管理

struct 存储管理器 {
    
    private static var 存储路径: String {
        let dir = NSHomeDirectory() + "/longhun/attestation"
        try? FileManager.default.createDirectory(atPath: dir, withIntermediateDirectories: true)
        return dir + "/records.json"
    }
    
    static func 读取全部() -> [存证引擎.存证记录] {
        guard let data = FileManager.default.contents(atPath: 存储路径),
              let 记录 = try? JSONDecoder().decode([存证引擎.存证记录].self, from: data)
        else { return [] }
        return 记录
    }
    
    static func 保存(_ 新记录: 存证引擎.存证记录) {
        var 全部 = 读取全部()
        全部.insert(新记录, at: 0)
        if let data = try? JSONEncoder().encode(全部) {
            FileManager.default.createFile(atPath: 存储路径, contents: data)
        }
    }
}

// MARK: - 存证界面

struct 存证View: View {
    @State private var 当前页签 = 0  // 0=存证, 1=验证, 2=记录
    @State private var 原文 = ""
    @State private var 摘要 = ""
    @State private var 密码 = ""
    @State private var 提示 = ""
    @State private var 记录列表: [存证引擎.存证记录] = []
    @State private var 验证记录: 存证引擎.存证记录?
    @State private var 验证密码 = ""
    @State private var 验证结果 = ""
    @State private var 显示分享 = false
    @State private var 分享文本 = ""
    
    var body: some View {
        ZStack {
            Color(red: 0.05, green: 0.05, blue: 0.12)
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // 页签
                HStack(spacing: 0) {
                    页签按钮("存证", "lock.shield", 0)
                    页签按钮("验证", "checkmark.shield", 1)
                    页签按钮("记录", "list.bullet.rectangle", 2)
                }
                .padding(.horizontal, 16)
                .padding(.top, 8)
                
                switch 当前页签 {
                case 0: 存证界面
                case 1: 验证界面
                default: 记录界面
                }
            }
        }
        .navigationTitle("存证系统")
        #if os(iOS)
        .navigationBarTitleDisplayMode(.inline)
        #endif
        .onAppear { 记录列表 = 存储管理器.读取全部() }
        .sheet(isPresented: $显示分享) {
            分享预览(文本: 分享文本)
        }
    }
    
    // MARK: - 存证界面
    
    private var 存证界面: some View {
        ScrollView {
            VStack(spacing: 16) {
                // 原文输入
                VStack(alignment: .leading, spacing: 6) {
                    Text("原文内容（加密存本地，不外传）")
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.5))
                    TextEditor(text: $原文)
                        .font(.body)
                        .frame(minHeight: 120)
                        .padding(10)
                        .background(Color.white.opacity(0.06))
                        .cornerRadius(10)
                        .foregroundColor(.white)
                        .scrollContentBackground(.hidden)
                }
                
                // 摘要
                VStack(alignment: .leading, spacing: 6) {
                    Text("公开摘要（30字内，别人看到的）")
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.5))
                    TextField("例：技术反馈邮件，正面评价+修改建议", text: $摘要)
                        .foregroundColor(.white)
                        .padding(12)
                        .background(Color.white.opacity(0.06))
                        .cornerRadius(10)
                }
                
                // 加密密码
                VStack(alignment: .leading, spacing: 6) {
                    Text("加密密码（只有你知道，用于解密验证）")
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.5))
                    SecureField("设置密码", text: $密码)
                        .foregroundColor(.white)
                        .padding(12)
                        .background(Color.white.opacity(0.06))
                        .cornerRadius(10)
                }
                
                // 存证按钮
                Button(action: 执行存证) {
                    HStack {
                        Image(systemName: "lock.shield")
                        Text("加密存证")
                            .fontWeight(.semibold)
                    }
                    .frame(maxWidth: .infinity)
                    .padding(14)
                    .background(
                        能存证
                        ? Color(red: 0.2, green: 0.6, blue: 0.3)
                        : Color.gray.opacity(0.3)
                    )
                    .foregroundColor(.white)
                    .cornerRadius(12)
                }
                .disabled(!能存证)
                
                // 提示
                if !提示.isEmpty {
                    Text(提示)
                        .font(.caption)
                        .foregroundColor(提示.hasPrefix("✅") ? .green : .red)
                }
                
                Spacer()
            }
            .padding(16)
        }
    }
    
    // MARK: - 验证界面
    
    private var 验证界面: some View {
        ScrollView {
            VStack(spacing: 16) {
                if let 记录 = 验证记录 {
                    // 选中的存证信息
                    VStack(alignment: .leading, spacing: 8) {
                        Text("DNA: \(记录.DNA追溯码)")
                            .font(.caption)
                            .foregroundColor(Color(red: 0.6, green: 0.8, blue: 1))
                        Text("摘要: \(记录.摘要)")
                            .font(.subheadline)
                            .foregroundColor(.white.opacity(0.8))
                        Text("哈希: \(String(记录.内容哈希.prefix(24)))...")
                            .font(.system(size: 10, design: .monospaced))
                            .foregroundColor(.white.opacity(0.4))
                    }
                    .padding(14)
                    .frame(maxWidth: .infinity, alignment: .leading)
                    .background(Color.white.opacity(0.05))
                    .cornerRadius(10)
                    
                    // 输入密码验证
                    SecureField("输入加密密码", text: $验证密码)
                        .foregroundColor(.white)
                        .padding(12)
                        .background(Color.white.opacity(0.06))
                        .cornerRadius(10)
                    
                    HStack(spacing: 12) {
                        Button("验证原文") { 执行验证() }
                            .frame(maxWidth: .infinity)
                            .padding(12)
                            .background(Color(red: 0.2, green: 0.5, blue: 0.8))
                            .foregroundColor(.white)
                            .cornerRadius(10)
                        
                        Button("分享摘要") { 执行分享(记录) }
                            .frame(maxWidth: .infinity)
                            .padding(12)
                            .background(Color(red: 0.5, green: 0.3, blue: 0.7))
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    
                    if !验证结果.isEmpty {
                        Text(验证结果)
                            .font(.caption)
                            .foregroundColor(验证结果.contains("✅") ? .green : .red)
                            .padding(10)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color.white.opacity(0.04))
                            .cornerRadius(8)
                    }
                } else {
                    Text("请在「记录」页签选择一条存证进行验证")
                        .font(.subheadline)
                        .foregroundColor(.white.opacity(0.4))
                        .padding(.top, 40)
                }
                
                Spacer()
            }
            .padding(16)
        }
    }
    
    // MARK: - 记录界面
    
    private var 记录界面: some View {
        ScrollView {
            if 记录列表.isEmpty {
                VStack(spacing: 8) {
                    Text("暂无存证记录")
                        .font(.headline)
                        .foregroundColor(.white.opacity(0.4))
                    Text("在「存证」页签创建第一条")
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.3))
                }
                .padding(.top, 60)
            } else {
                LazyVStack(spacing: 8) {
                    ForEach(记录列表) { 记录 in
                        Button {
                            验证记录 = 记录
                            验证密码 = ""
                            验证结果 = ""
                            当前页签 = 1
                        } label: {
                            HStack(spacing: 12) {
                                VStack(alignment: .leading, spacing: 4) {
                                    Text(记录.摘要)
                                        .font(.subheadline)
                                        .foregroundColor(.white.opacity(0.85))
                                        .lineLimit(1)
                                    HStack(spacing: 6) {
                                        Text(记录.时间戳)
                                            .font(.caption2)
                                            .foregroundColor(.white.opacity(0.35))
                                        Text("·")
                                            .foregroundColor(.white.opacity(0.2))
                                        Text(String(记录.内容哈希.prefix(12)) + "...")
                                            .font(.system(size: 9, design: .monospaced))
                                            .foregroundColor(.white.opacity(0.25))
                                    }
                                }
                                Spacer()
                                Image(systemName: "chevron.right")
                                    .font(.caption2)
                                    .foregroundColor(.white.opacity(0.2))
                            }
                            .padding(14)
                            .background(Color.white.opacity(0.05))
                            .cornerRadius(10)
                        }
                    }
                }
                .padding(16)
            }
        }
    }
    
    // MARK: - 辅助
    
    private var 能存证: Bool {
        !原文.trimmingCharacters(in: .whitespaces).isEmpty &&
        !摘要.trimmingCharacters(in: .whitespaces).isEmpty &&
        密码.count >= 4
    }
    
    private func 页签按钮(_ 标题: String, _ 图标: String, _ 索引: Int) -> some View {
        Button {
            withAnimation(.easeInOut(duration: 0.2)) { 当前页签 = 索引 }
        } label: {
            HStack(spacing: 4) {
                Image(systemName: 图标).font(.caption2)
                Text(标题).font(.caption).fontWeight(.medium)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 10)
            .background(当前页签 == 索引 ? Color.white.opacity(0.12) : Color.clear)
            .foregroundColor(当前页签 == 索引 ? .white : .white.opacity(0.4))
            .cornerRadius(8)
        }
    }
    
    private func 执行存证() {
        guard let 记录 = 存证引擎.创建存证(原文: 原文, 摘要: 摘要, 密码: 密码)
        else {
            提示 = "❌ 加密失败"
            return
        }
        提示 = "✅ 存证成功\nDNA: \(记录.DNA追溯码)\n哈希: \(String(记录.内容哈希.prefix(24)))..."
        原文 = ""
        摘要 = ""
        密码 = ""
        记录列表 = 存储管理器.读取全部()
    }
    
    private func 执行验证() {
        guard let 记录 = 验证记录 else { return }
        let 结果 = 存证引擎.验证存证(记录: 记录, 密码: 验证密码)
        
        if 结果.通过 {
            验证结果 = "✅ 验证通过！哈希匹配，原文未被篡改。\n\n原文预览：\(String((结果.原文 ?? "").prefix(100)))..."
        } else {
            验证结果 = "❌ 验证失败。密码错误或内容已被篡改。"
        }
    }
    
    private func 执行分享(_ 记录: 存证引擎.存证记录) {
        分享文本 = 存证引擎.生成分享文本(记录: 记录)
        显示分享 = true
    }
}

// MARK: - 分享预览

private struct 分享预览: View {
    let 文本: String
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        ZStack {
            Color(red: 0.05, green: 0.05, blue: 0.12).ignoresSafeArea()
            
            VStack(spacing: 16) {
                HStack {
                    Text("公开验证信息")
                        .font(.headline)
                        .foregroundColor(.white)
                    Spacer()
                    Button("关闭") { dismiss() }
                        .foregroundColor(Color(red: 0.6, green: 0.8, blue: 1))
                }
                
                ScrollView {
                    Text(文本)
                        .font(.system(size: 12, design: .monospaced))
                        .foregroundColor(.white.opacity(0.8))
                        .frame(maxWidth: .infinity, alignment: .leading)
                }
                
                Button {
                    #if os(macOS)
                    NSPasteboard.general.clearContents()
                    NSPasteboard.general.setString(文本, forType: .string)
                    #endif
                } label: {
                    HStack {
                        Image(systemName: "doc.on.doc")
                        Text("复制到剪贴板")
                    }
                    .frame(maxWidth: .infinity)
                    .padding(12)
                    .background(Color(red: 0.2, green: 0.5, blue: 0.8))
                    .foregroundColor(.white)
                    .cornerRadius(10)
                }
            }
            .padding(20)
        }
    }
}
