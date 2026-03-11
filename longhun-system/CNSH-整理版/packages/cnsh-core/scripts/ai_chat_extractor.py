#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ai_chat_extractor.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260310-ai_chat_extractor-v1.0
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
"""
AI对话记录提取器
支持智谱清言、千问、ChatGPT、腾讯元宝、DeepSeek等平台
用于将所有对话记录归集到CNSH系统
"""

import os
import json
import sqlite3
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import csv

class AIChatExtractor:
    """AI对话记录提取器"""
    
    def __init__(self):
        """初始化提取器"""
        self.supported_platforms = {
            "chatgpt": self._extract_chatgpt,
            "zhipu": self._extract_zhipu,
            "qianwen": self._extract_qianwen,
            "yuanbao": self._extract_yuanbao,
            "deepseek": self._extract_deepseek
        }
        
        # 创建输出目录
        self.output_dir = "extracted_chats"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 初始化数据库
        self.init_database()
    
    def init_database(self):
        """初始化对话数据库"""
        self.db_path = os.path.join(self.output_dir, "chat_history.db")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建对话表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                session_id TEXT,
                user_message TEXT,
                ai_message TEXT,
                timestamp TEXT,
                message_id TEXT,
                dna_code TEXT,
                extracted_at TEXT
            )
        ''')
        
        # 创建DNA码表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dna_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dna_code TEXT UNIQUE NOT NULL,
                platform TEXT,
                content_type TEXT,
                content TEXT,
                author TEXT,
                created_at TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def extract_from_platform(self, platform: str, data_source: str) -> Dict:
        """从指定平台提取对话记录"""
        if platform not in self.supported_platforms:
            return {"success": False, "error": f"不支持的平台: {platform}"}
        
        try:
            extractor = self.supported_platforms[platform]
            result = extractor(data_source)
            
            if result["success"]:
                # 保存到数据库
                self.save_to_database(platform, result["chats"])
                
                # 生成DNA码
                self.generate_dna_codes(platform, result["chats"])
                
                return {"success": True, "count": len(result["chats"])}
            else:
                return result
        
        except Exception as e:
            return {"success": False, "error": f"提取失败: {str(e)}"}
    
    def _extract_chatgpt(self, data_source: str) -> Dict:
        """提取ChatGPT对话记录"""
        try:
            # ChatGPT数据通常是JSON格式
            if os.path.isfile(data_source):
                with open(data_source, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                return {"success": False, "error": "ChatGPT数据文件不存在"}
            
            chats = []
            
            # 处理ChatGPT导出格式
            if isinstance(data, list):
                for item in data:
                    if "messages" in item:
                        for msg in item["messages"]:
                            if msg.get("role") == "user":
                                user_msg = msg.get("content", "")
                                # 查找AI回复
                                ai_msg = ""
                                for next_msg in item["messages"]:
                                    if next_msg.get("role") == "assistant":
                                        ai_msg = next_msg.get("content", "")
                                        break
                                
                                if user_msg and ai_msg:
                                    chats.append({
                                        "user_message": user_msg,
                                        "ai_message": ai_msg,
                                        "timestamp": msg.get("create_time", ""),
                                        "message_id": msg.get("id", ""),
                                        "session_id": item.get("title", "")
                                    })
            
            return {"success": True, "chats": chats}
        
        except Exception as e:
            return {"success": False, "error": f"ChatGPT数据解析失败: {str(e)}"}
    
    def _extract_zhipu(self, data_source: str) -> Dict:
        """提取智谱清言对话记录"""
        try:
            # 智谱清言数据格式处理
            if os.path.isfile(data_source):
                with open(data_source, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                return {"success": False, "error": "智谱清言数据文件不存在"}
            
            chats = []
            
            # 处理智谱清言导出格式
            if "conversations" in data:
                for conv in data["conversations"]:
                    messages = conv.get("messages", [])
                    for i in range(0, len(messages), 2):
                        if i + 1 < len(messages):
                            user_msg = messages[i].get("content", "")
                            ai_msg = messages[i + 1].get("content", "")
                            
                            if user_msg and ai_msg:
                                chats.append({
                                    "user_message": user_msg,
                                    "ai_message": ai_msg,
                                    "timestamp": messages[i].get("createTime", ""),
                                    "message_id": messages[i].get("id", ""),
                                    "session_id": conv.get("title", "")
                                })
            
            return {"success": True, "chats": chats}
        
        except Exception as e:
            return {"success": False, "error": f"智谱清言数据解析失败: {str(e)}"}
    
    def _extract_qianwen(self, data_source: str) -> Dict:
        """提取千问对话记录"""
        try:
            # 千问数据格式处理
            if os.path.isfile(data_source):
                with open(data_source, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                return {"success": False, "error": "千问数据文件不存在"}
            
            chats = []
            
            # 处理千问导出格式
            if "data" in data:
                for session in data["data"]:
                    messages = session.get("messages", [])
                    for msg in messages:
                        if msg.get("role") == "user":
                            user_msg = msg.get("content", "")
                            # 查找AI回复
                            ai_msg = ""
                            for next_msg in messages:
                                if next_msg.get("role") == "assistant":
                                    ai_msg = next_msg.get("content", "")
                                    break
                            
                            if user_msg and ai_msg:
                                chats.append({
                                    "user_message": user_msg,
                                    "ai_message": ai_msg,
                                    "timestamp": msg.get("timestamp", ""),
                                    "message_id": msg.get("messageId", ""),
                                    "session_id": session.get("sessionName", "")
                                })
            
            return {"success": True, "chats": chats}
        
        except Exception as e:
            return {"success": False, "error": f"千问数据解析失败: {str(e)}"}
    
    def _extract_yuanbao(self, data_source: str) -> Dict:
        """提取腾讯元宝对话记录"""
        try:
            # 腾讯元宝数据格式处理
            if os.path.isfile(data_source):
                with open(data_source, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                return {"success": False, "error": "腾讯元宝数据文件不存在"}
            
            chats = []
            
            # 处理腾讯元宝导出格式
            if "chatList" in data:
                for chat in data["chatList"]:
                    messages = chat.get("messageList", [])
                    for msg in messages:
                        user_msg = ""
                        ai_msg = ""
                        
                        if msg.get("senderType") == "user":
                            user_msg = msg.get("content", "")
                            # 查找AI回复
                            for next_msg in messages:
                                if next_msg.get("senderType") == "bot":
                                    ai_msg = next_msg.get("content", "")
                                    break
                        
                        if user_msg and ai_msg:
                            chats.append({
                                "user_message": user_msg,
                                "ai_message": ai_msg,
                                "timestamp": msg.get("createTime", ""),
                                "message_id": msg.get("msgId", ""),
                                "session_id": chat.get("chatTitle", "")
                            })
            
            return {"success": True, "chats": chats}
        
        except Exception as e:
            return {"success": False, "error": f"腾讯元宝数据解析失败: {str(e)}"}
    
    def _extract_deepseek(self, data_source: str) -> Dict:
        """提取DeepSeek对话记录"""
        try:
            # DeepSeek数据格式处理
            if os.path.isfile(data_source):
                with open(data_source, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                return {"success": False, "error": "DeepSeek数据文件不存在"}
            
            chats = []
            
            # 处理DeepSeek导出格式
            if "conversations" in data:
                for conv in data["conversations"]:
                    messages = conv.get("dialogue", [])
                    for i in range(0, len(messages), 2):
                        if i + 1 < len(messages):
                            user_msg = messages[i].get("content", "")
                            ai_msg = messages[i + 1].get("content", "")
                            
                            if user_msg and ai_msg:
                                chats.append({
                                    "user_message": user_msg,
                                    "ai_message": ai_msg,
                                    "timestamp": messages[i].get("timestamp", ""),
                                    "message_id": messages[i].get("id", ""),
                                    "session_id": conv.get("title", "")
                                })
            
            return {"success": True, "chats": chats}
        
        except Exception as e:
            return {"success": False, "error": f"DeepSeek数据解析失败: {str(e)}"}
    
    def save_to_database(self, platform: str, chats: List[Dict]):
        """保存对话到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for chat in chats:
            cursor.execute('''
                INSERT INTO chats (platform, session_id, user_message, ai_message, 
                               timestamp, message_id, extracted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                platform,
                chat.get("session_id", ""),
                chat.get("user_message", ""),
                chat.get("ai_message", ""),
                chat.get("timestamp", ""),
                chat.get("message_id", ""),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def generate_dna_codes(self, platform: str, chats: List[Dict]):
        """为重要对话生成DNA码"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for chat in chats:
            # 检查用户消息是否包含创意或重要内容
            if self._should_generate_dna(chat["user_message"]):
                # 使用DNA生成器
                from dna_generator import CNSHDNAGenerator
                generator = CNSHDNAGenerator()
                
                # 分析内容类型
                content_type = self._analyze_content_type(chat["user_message"])
                
                # 生成DNA码
                result = generator.generate_dna_code(
                    content_type=content_type,
                    region="CN",
                    content=self._extract_content(chat["user_message"])[:20],
                    author="AI对话",
                    version="v1.0"
                )
                
                if result["success"]:
                    cursor.execute('''
                        INSERT OR IGNORE INTO dna_codes (dna_code, platform, content_type, 
                                                    content, author, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        result["dna_code"],
                        platform,
                        content_type,
                        chat["user_message"][:100],
                        "AI对话",
                        datetime.now().isoformat()
                    ))
        
        conn.commit()
        conn.close()
    
    def _should_generate_dna(self, message: str) -> bool:
        """判断是否应该生成DNA码"""
        # 检查是否包含创意关键词
        creative_keywords = [
            "我想", "创意", "想法", "设计", "开发", "制作",
            "发明", "创建", "构建", "计划", "方案",
            "算法", "系统", "平台", "应用", "工具"
        ]
        
        return any(keyword in message for keyword in creative_keywords)
    
    def _analyze_content_type(self, message: str) -> str:
        """分析内容类型"""
        if any(word in message for word in ["代码", "程序", "脚本", "开发"]):
            return "CD"  # 代码
        elif any(word in message for word in ["设计", "界面", "图形"]):
            return "DE"  # 设计
        elif any(word in message for word in ["方法", "流程", "机制"]):
            return "ME"  # 方法论
        elif any(word in message for word in ["算法", "逻辑", "公式"]):
            return "AL"  # 算法
        elif any(word in message for word in ["文档", "教程", "说明"]):
            return "DO"  # 文档
        else:
            return "ID"  # 创意
    
    def _extract_content(self, message: str) -> str:
        """提取内容描述"""
        # 简化处理，去除标点符号
        import re
        content = re.sub(r'[^\w\u4e00-\u9fff]', '', message)
        return content
    
    def export_to_csv(self, platform: str = None) -> str:
        """导出为CSV格式"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM chats"
        params = []
        
        if platform:
            query += " WHERE platform = ?"
            params.append(platform)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        # 导出文件路径
        filename = f"{platform or 'all'}_chats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.output_dir, filename)
        
        # 写入CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['ID', '平台', '会话ID', '用户消息', 'AI回复', '时间戳', '消息ID', '提取时间'])
            writer.writerows(rows)
        
        return filepath
    
    def get_statistics(self, platform: str = None) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总对话数
        query = "SELECT COUNT(*) FROM chats"
        params = []
        if platform:
            query += " WHERE platform = ?"
            params.append(platform)
        
        cursor.execute(query, params)
        total_chats = cursor.fetchone()[0]
        
        # DNA码数量
        query = "SELECT COUNT(*) FROM dna_codes"
        params = []
        if platform:
            query += " WHERE platform = ?"
            params.append(platform)
        
        cursor.execute(query, params)
        total_dna = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_chats": total_chats,
            "total_dna_codes": total_dna,
            "platform": platform or "all"
        }
    
    def list_platforms(self) -> List[str]:
        """列出支持的平台"""
        return list(self.supported_platforms.keys())


# 交互式命令行界面
def interactive_mode():
    """交互式命令行模式"""
    extractor = AIChatExtractor()
    
    print("🤖 AI对话记录提取器 - 交互式模式")
    print("=" * 40)
    
    while True:
        print("\n请选择操作：")
        print("1. 提取对话记录")
        print("2. 查看统计信息")
        print("3. 导出为CSV")
        print("4. 查看支持的平台")
        print("5. 查看提取指南")
        print("6. 退出")
        
        choice = input("\n请输入选项 [1-6]: ").strip()
        
        if choice == "1":
            extract_chats(extractor)
        elif choice == "2":
            show_statistics(extractor)
        elif choice == "3":
            export_csv(extractor)
        elif choice == "4":
            show_platforms(extractor)
        elif choice == "5":
            show_guide(extractor)
        elif choice == "6":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选项，请重新输入。")


def extract_chats(extractor):
    """提取对话记录"""
    print("\n🤖 提取对话记录")
    print("-" * 15)
    
    # 显示支持的平台
    platforms = extractor.list_platforms()
    print("支持的平台：")
    for i, platform in enumerate(platforms, 1):
        platform_name = {
            "chatgpt": "ChatGPT",
            "zhipu": "智谱清言",
            "qianwen": "千问",
            "yuanbao": "腾讯元宝",
            "deepseek": "DeepSeek"
        }.get(platform, platform)
        print(f"  {i}. {platform_name} ({platform})")
    
    # 获取用户选择
    try:
        platform_choice = int(input("\n请选择平台 [1-5]: "))
        platform = platforms[platform_choice - 1]
    except (ValueError, IndexError):
        print("❌ 无效选择")
        return
    
    # 获取数据源路径
    data_source = input(f"\n请输入{platform}数据文件路径: ").strip()
    
    if not os.path.isfile(data_source):
        print("❌ 文件不存在")
        return
    
    # 提取对话
    print(f"\n🔄 正在提取{platform}对话记录...")
    result = extractor.extract_from_platform(platform, data_source)
    
    if result["success"]:
        print(f"✅ 成功提取 {result['count']} 条对话记录")
        print(f"💾 已保存到 {extractor.db_path}")
    else:
        print(f"❌ 提取失败: {result['error']}")


def show_statistics(extractor):
    """显示统计信息"""
    print("\n📊 统计信息")
    print("-" * 10)
    
    # 显示所有平台的统计
    platforms = extractor.list_platforms()
    
    print("📈 总体统计：")
    stats = extractor.get_statistics()
    print(f"  总对话数: {stats['total_chats']}")
    print(f"  总DNA码数: {stats['total_dna_codes']}")
    
    print("\n📈 各平台统计：")
    for platform in platforms:
        stats = extractor.get_statistics(platform)
        platform_name = {
            "chatgpt": "ChatGPT",
            "zhipu": "智谱清言",
            "qianwen": "千问",
            "yuanbao": "腾讯元宝",
            "deepseek": "DeepSeek"
        }.get(platform, platform)
        print(f"  {platform_name}: {stats['total_chats']} 条对话")


def export_csv(extractor):
    """导出为CSV"""
    print("\n📄 导出为CSV")
    print("-" * 12)
    
    platforms = extractor.list_platforms()
    print("选择导出范围：")
    print("1. 所有平台")
    for i, platform in enumerate(platforms, 2):
        platform_name = {
            "chatgpt": "ChatGPT",
            "zhipu": "智谱清言",
            "qianwen": "千问",
            "yuanbao": "腾讯元宝",
            "deepseek": "DeepSeek"
        }.get(platform, platform)
        print(f"  {i}. {platform_name}")
    
    try:
        choice = int(input("\n请选择 [1-6]: "))
        
        if choice == 1:
            platform = None
        else:
            platform = platforms[choice - 2]
    except (ValueError, IndexError):
        print("❌ 无效选择")
        return
    
    # 导出CSV
    print("\n🔄 正在导出...")
    filepath = extractor.export_to_csv(platform)
    
    print(f"✅ 成功导出到: {filepath}")


def show_platforms(extractor):
    """显示支持的平台"""
    print("\n🤖 支持的平台")
    print("-" * 13)
    
    platforms = extractor.list_platforms()
    
    for platform in platforms:
        platform_name = {
            "chatgpt": "ChatGPT",
            "zhipu": "智谱清言",
            "qianwen": "千问",
            "yuanbao": "腾讯元宝",
            "deepseek": "DeepSeek"
        }.get(platform, platform)
        
        print(f"🔸 {platform_name} ({platform})")
    
    print("\n💡 提示：各平台的数据导出方式可能不同，请查看提取指南。")


def show_guide(extractor):
    """显示提取指南"""
    print("\n📖 各平台数据导出指南")
    print("-" * 22)
    
    guides = {
        "ChatGPT": """
1. 访问 https://chat.openai.com
2. 点击左下角账户 → Settings → Data controls
3. 点击 "Export data"
4. 等待邮件通知下载链接
5. 下载JSON格式的对话记录文件
        """,
        "智谱清言": """
1. 打开智谱清言App或网页版
2. 进入"我的" → 设置
3. 找到"数据导出"或"对话记录导出"
4. 选择导出格式为JSON
5. 下载导出文件
        """,
        "千问": """
1. 访问 https://qianwen.aliyun.com
2. 进入个人中心 → 数据管理
3. 选择"对话记录" → "导出"
4. 选择JSON格式导出
5. 下载导出文件
        """,
        "腾讯元宝": """
1. 打开腾讯元宝App
2. 进入"我的" → 设置
3. 选择"隐私设置" → "数据管理"
4. 点击"导出对话记录"
5. 选择JSON格式并下载
        """,
        "DeepSeek": """
1. 访问 https://chat.deepseek.com
2. 进入个人设置
3. 选择"数据导出"
4. 选择包含对话记录
5. 下载JSON格式文件
        """
    }
    
    for platform, guide in guides.items():
        print(f"\n🔸 {platform}")
        print(guide.strip())
    
    print("\n💡 提示：导出的文件通常是JSON格式，包含完整的对话历史。")


if __name__ == "__main__":
    interactive_mode()