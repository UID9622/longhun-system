#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ═══════════════════════════════════════════════════════════
# 龙魂系统 v2.0 | 开箱即用版启动器
# ═══════════════════════════════════════════════════════════
# 一键启动所有本地服务
# DNA: #龙芯⚡️2026-02-06-启动器-v1.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ═══════════════════════════════════════════════════════════

import os
import sys
import json
import webbrowser
import subprocess
import threading
import http.server
import socketserver
from pathlib import Path
from datetime import datetime

# 添加core目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from local_database import 龙魂本地数据库


class 龙魂启动器:
    """
    龙魂系统开箱即用版启动器
    
    功能:
    1. 初始化本地数据库
    2. 启动本地HTTP服务器
    3. 自动打开浏览器
    4. 显示系统状态
    """
    
    def __init__(self):
        self.版本 = "v2.0.0"
        self.端口 = 9622  # UID端口号
        self.数据库 = None
        self.服务器 = None
        self.运行目录 = Path(__file__).parent
        
    def 显示启动画面(self):
        """显示龙魂系统启动画面"""
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║                    🐉 龙魂系统 v2.0 开箱即用版                   ║
║                                                                  ║
║     永恒锚: "再楠不惧，终成豪图"                                  ║
║     核心主权: 农历/易经/道德经/DNA追溯/CNSH编码/OCSL许可证          ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  📝 CNSH编辑器    |  🤖 五大人格    |  🧬 DNA追溯               ║
║  🛡️ 反诈守护      |  ☯️ 易经推演    |  💰 数字人民币支付        ║
║  📱 华为生态      |  🔒 零API依赖   |  🏠 本地数据存储          ║
╚══════════════════════════════════════════════════════════════════╝
        """)
        
    def 检查环境(self) -> bool:
        """检查运行环境"""
        print("🔍 检查运行环境...")
        
        # 检查Python版本
        if sys.version_info < (3, 8):
            print("❌ 需要Python 3.8或更高版本")
            return False
        print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor}")
        
        # 检查核心文件
        必要文件 = [
            "龙魂系统.html",
            "core/local_database.py",
        ]
        
        for 文件 in 必要文件:
            路径 = self.运行目录 / 文件
            if not 路径.exists():
                print(f"  ❌ 缺少文件: {文件}")
                return False
            print(f"  ✅ {文件}")
        
        return True
    
    def 初始化数据库(self):
        """初始化本地数据库"""
        print("\n🗄️  初始化本地数据库...")
        
        try:
            self.数据库 = 龙魂本地数据库()
            统计 = self.数据库.获取系统统计()
            
            print(f"  ✅ 数据库连接成功")
            print(f"  📊 当前记录:")
            print(f"     - DNA追溯: {统计.get('dna_trace', 0)} 条")
            print(f"     - CNSH代码: {统计.get('cnsh_code', 0)} 个")
            print(f"     - 决策历史: {统计.get('persona_decisions', 0)} 条")
            print(f"     - 数据库大小: {统计.get('数据库大小', '0 KB')}")
            
        except Exception as e:
            print(f"  ❌ 数据库初始化失败: {e}")
            raise
    
    def 启动HTTP服务器(self):
        """启动本地HTTP服务器"""
        print(f"\n🌐 启动本地HTTP服务器...")
        
        # 切换到运行目录
        os.chdir(self.运行目录)
        
        class 龙魂HTTP处理器(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
            
            def log_message(self, format, *args):
                # 简化日志输出
                pass
        
        try:
            self.服务器 = socketserver.TCPServer(("", self.端口), 龙魂HTTP处理器)
            print(f"  ✅ 服务器启动成功")
            print(f"  📍 访问地址: http://localhost:{self.端口}/龙魂系统.html")
            
            # 在后台线程运行服务器
            服务器线程 = threading.Thread(target=self.服务器.serve_forever)
            服务器线程.daemon = True
            服务器线程.start()
            
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"  ⚠️  端口 {self.端口} 已被占用，尝试其他端口...")
                self.端口 += 1
                self.启动HTTP服务器()
            else:
                raise
    
    def 打开浏览器(self):
        """自动打开浏览器"""
        print("\n🌍 正在打开浏览器...")
        
        url = f"http://localhost:{self.端口}/龙魂系统.html"
        
        try:
            webbrowser.open(url)
            print(f"  ✅ 已打开浏览器: {url}")
        except Exception as e:
            print(f"  ⚠️  自动打开浏览器失败，请手动访问:")
            print(f"     {url}")
    
    def 显示系统信息(self):
        """显示系统信息"""
        print("""
════════════════════════════════════════════════════════════════════
📋 系统信息
════════════════════════════════════════════════════════════════════
  版本: 龙魂系统 v2.0.0 开箱即用版
  模式: 本地运行 (零API依赖)
  数据: 本地SQLite存储 (~/.longhun/database/)
  调试: 所有功能免费使用
  
💰 付费模式 (正式版):
  - 华为开发者功能: ¥1/月
  - 本地API服务: ¥1/月  
  - 扩展存储空间: ¥1/月
  
🔐 身份验证:
  UID: UID9622
  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
  
📝 可用功能:
  1. CNSH中文编程编辑器
  2. 五大人格决策系统
  3. DNA追溯码生成器
  4. 易经八卦推演
  5. 反诈守护系统
  6. 本地数据库管理
  
⚠️  安全声明:
  所有数据存储在本地，不上传任何服务器
  华为不收集用户个人信息
  
════════════════════════════════════════════════════════════════════
        """)
    
    def 启动(self):
        """启动龙魂系统"""
        self.显示启动画面()
        
        try:
            # 检查环境
            if not self.检查环境():
                print("\n❌ 环境检查失败，请确保所有文件完整")
                return 1
            
            # 初始化数据库
            self.初始化数据库()
            
            # 启动HTTP服务器
            self.启动HTTP服务器()
            
            # 显示系统信息
            self.显示系统信息()
            
            # 打开浏览器
            self.打开浏览器()
            
            print("""
════════════════════════════════════════════════════════════════════
✅ 龙魂系统启动成功！
════════════════════════════════════════════════════════════════════

按 Ctrl+C 停止服务器

#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
            """)
            
            # 保持运行
            try:
                while True:
                    import time
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n🛑 正在关闭龙魂系统...")
                if self.服务器:
                    self.服务器.shutdown()
                if self.数据库:
                    self.数据库.关闭()
                print("✅ 已安全关闭")
                
        except Exception as e:
            print(f"\n❌ 启动失败: {e}")
            import traceback
            traceback.print_exc()
            return 1
        
        return 0


def 主函数():
    """主入口"""
    启动器 = 龙魂启动器()
    return 启动器.启动()


if __name__ == "__main__":
    sys.exit(主函数())
