// Notion助手.swift
// 完全中文注释版本 - 让你看懂每一行在干什么

import Foundation

/// Notion 助手 - 用来读取你的 26 张知识卡片
class Notion助手 {
    
    // MARK: - 配置信息（你需要填写）
    
    /// 你的 Notion API 密钥（从 https://www.notion.so/my-integrations 获取）
    private let API密钥 = "在这里粘贴你的 secret_xxxx 密钥"
    
    /// 你的 Notion 数据库 ID（从数据库页面的网址里复制）
    private let 数据库ID = "在这里粘贴你的数据库ID"
    
    // MARK: - 基础设置
    
    /// Notion API 的基础网址
    private let 基础网址 = "https://api.notion.com/v1"
    
    /// Notion API 版本号（固定值，不用改）
    private let API版本 = "2022-06-28"
    
    
    // MARK: - 读取所有卡片
    
    /// 从 Notion 读取所有知识卡片
    /// - Returns: 返回卡片数组，每张卡片是一个字典
    func 读取所有卡片() async throws -> [[String: Any]] {
        
        print("📖 开始从 Notion 读取知识卡片...")
        
        // 1. 准备网址
        let 网址字符串 = "\(基础网址)/databases/\(数据库ID)/query"
        guard let 网址 = URL(string: 网址字符串) else {
            print("❌ 错误：网址格式不对")
            throw Notion错误.网址无效
        }
        
        // 2. 准备请求
        var 请求 = URLRequest(url: 网址)
        请求.httpMethod = "POST"  // POST 方法用来查询数据库
        
        // 3. 添加必要的请求头
        请求.setValue("Bearer \(API密钥)", forHTTPHeaderField: "Authorization")  // 身份认证
        请求.setValue(API版本, forHTTPHeaderField: "Notion-Version")  // API版本
        请求.setValue("application/json", forHTTPHeaderField: "Content-Type")  // 数据格式
        
        // 4. 发送请求
        let (数据, 响应) = try await URLSession.shared.data(for: 请求)
        
        // 5. 检查响应状态
        guard let HTTP响应 = 响应 as? HTTPURLResponse else {
            print("❌ 错误：响应格式不对")
            throw Notion错误.响应无效
        }
        
        if HTTP响应.statusCode != 200 {
            print("❌ 错误：HTTP状态码 \(HTTP响应.statusCode)")
            if let 错误信息 = String(data: 数据, encoding: .utf8) {
                print("详细错误：\(错误信息)")
            }
            throw Notion错误.请求失败(状态码: HTTP响应.statusCode)
        }
        
        // 6. 解析返回的数据
        guard let JSON = try JSONSerialization.jsonObject(with: 数据) as? [String: Any],
              let 结果列表 = JSON["results"] as? [[String: Any]] else {
            print("❌ 错误：数据格式不对")
            throw Notion错误.数据解析失败
        }
        
        print("✅ 成功读取 \(结果列表.count) 张卡片")
        return 结果列表
    }
    
    
    // MARK: - 读取单张卡片的详细内容
    
    /// 读取单张卡片的详细内容
    /// - Parameter 卡片ID: Notion 页面的 ID
    /// - Returns: 卡片的详细内容
    func 读取卡片详情(卡片ID: String) async throws -> [String: Any] {
        
        print("📄 读取卡片详情：\(卡片ID)")
        
        // 1. 准备网址
        let 网址字符串 = "\(基础网址)/pages/\(卡片ID)"
        guard let 网址 = URL(string: 网址字符串) else {
            throw Notion错误.网址无效
        }
        
        // 2. 准备请求
        var 请求 = URLRequest(url: 网址)
        请求.httpMethod = "GET"  // GET 方法用来获取单个页面
        
        // 3. 添加请求头
        请求.setValue("Bearer \(API密钥)", forHTTPHeaderField: "Authorization")
        请求.setValue(API版本, forHTTPHeaderField: "Notion-Version")
        
        // 4. 发送请求
        let (数据, _) = try await URLSession.shared.data(for: 请求)
        
        // 5. 解析数据
        guard let JSON = try JSONSerialization.jsonObject(with: 数据) as? [String: Any] else {
            throw Notion错误.数据解析失败
        }
        
        print("✅ 成功读取卡片详情")
        return JSON
    }
    
    
    // MARK: - 搜索卡片
    
    /// 搜索包含特定关键词的卡片
    /// - Parameter 关键词: 要搜索的关键词
    /// - Returns: 匹配的卡片列表
    func 搜索卡片(关键词: String) async throws -> [[String: Any]] {
        
        print("🔍 搜索卡片：\(关键词)")
        
        // 1. 准备网址
        let 网址字符串 = "\(基础网址)/search"
        guard let 网址 = URL(string: 网址字符串) else {
            throw Notion错误.网址无效
        }
        
        // 2. 准备搜索参数
        let 搜索参数: [String: Any] = [
            "query": 关键词,  // 搜索关键词
            "filter": [
                "property": "object",
                "value": "page"
            ]
        ]
        
        // 3. 准备请求
        var 请求 = URLRequest(url: 网址)
        请求.httpMethod = "POST"
        请求.setValue("Bearer \(API密钥)", forHTTPHeaderField: "Authorization")
        请求.setValue(API版本, forHTTPHeaderField: "Notion-Version")
        请求.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        // 4. 添加搜索参数到请求体
        请求.httpBody = try JSONSerialization.data(withJSONObject: 搜索参数)
        
        // 5. 发送请求
        let (数据, _) = try await URLSession.shared.data(for: 请求)
        
        // 6. 解析结果
        guard let JSON = try JSONSerialization.jsonObject(with: 数据) as? [String: Any],
              let 结果列表 = JSON["results"] as? [[String: Any]] else {
            throw Notion错误.数据解析失败
        }
        
        print("✅ 找到 \(结果列表.count) 张匹配的卡片")
        return 结果列表
    }
    
    
    // MARK: - 按分类读取卡片
    
    /// 读取特定分类的卡片
    /// - Parameter 分类名称: 例如 "龍魂核心算法"、"Swift语言基础" 等
    /// - Returns: 该分类下的所有卡片
    func 读取分类卡片(分类名称: String) async throws -> [[String: Any]] {
        
        print("📁 读取分类：\(分类名称)")
        
        // 先读取所有卡片
        let 所有卡片 = try await 读取所有卡片()
        
        // 过滤出指定分类的卡片
        // 注意：这里需要根据你的 Notion 数据库结构调整
        // 假设你有一个"分类"属性
        let 分类卡片 = 所有卡片.filter { 卡片 in
            // 从卡片属性中提取分类信息
            if let 属性 = 卡片["properties"] as? [String: Any],
               let 分类属性 = 属性["分类"] as? [String: Any],
               let 分类值 = 提取文本(从属性: 分类属性) {
                return 分类值.contains(分类名称)
            }
            return false
        }
        
        print("✅ 找到 \(分类卡片.count) 张 \(分类名称) 卡片")
        return 分类卡片
    }
    
    
    // MARK: - 辅助方法
    
    /// 从 Notion 属性中提取文本内容
    /// - Parameter 属性: Notion 的属性字典
    /// - Returns: 提取出的文本
    private func 提取文本(从属性 属性: [String: Any]) -> String? {
        // Notion 的文本属性有多种类型，这里处理常见的几种
        
        // 1. 标题类型 (title)
        if let 标题数组 = 属性["title"] as? [[String: Any]] {
            return 标题数组.compactMap { $0["plain_text"] as? String }.joined()
        }
        
        // 2. 富文本类型 (rich_text)
        if let 文本数组 = 属性["rich_text"] as? [[String: Any]] {
            return 文本数组.compactMap { $0["plain_text"] as? String }.joined()
        }
        
        // 3. 选择类型 (select)
        if let 选择 = 属性["select"] as? [String: Any],
           let 名称 = 选择["name"] as? String {
            return 名称
        }
        
        return nil
    }
}


// MARK: - 错误类型定义

/// Notion 相关的错误类型
enum Notion错误: Error {
    case 网址无效           // URL 格式不对
    case 响应无效           // 服务器响应格式不对
    case 请求失败(状态码: Int)  // HTTP 请求失败
    case 数据解析失败       // JSON 解析失败
    
    /// 错误描述（中文）
    var 描述: String {
        switch self {
        case .网址无效:
            return "网址格式不正确"
        case .响应无效:
            return "服务器响应格式不正确"
        case .请求失败(let 状态码):
            return "请求失败，HTTP状态码：\(状态码)"
        case .数据解析失败:
            return "数据解析失败，可能是 Notion 数据格式有变化"
        }
    }
}


// MARK: - 使用示例

/// 如何使用这个 Notion助手
func 使用示例() async {
    
    // 1. 创建助手实例
    let 助手 = Notion助手()
    
    do {
        // 2. 读取所有卡片
        let 所有卡片 = try await 助手.读取所有卡片()
        print("📚 总共有 \(所有卡片.count) 张卡片")
        
        // 3. 读取特定分类的卡片
        let 龍魂卡片 = try await 助手.读取分类卡片(分类名称: "龍魂核心算法")
        print("🤖 龍魂核心算法卡片：\(龍魂卡片.count) 张")
        
        // 4. 搜索卡片
        let 搜索结果 = try await 助手.搜索卡片(关键词: "Swift")
        print("🔍 搜索到 \(搜索结果.count) 张相关卡片")
        
    } catch let 错误 as Notion错误 {
        print("❌ 出错了：\(错误.描述)")
    } catch {
        print("❌ 未知错误：\(error)")
    }
}
