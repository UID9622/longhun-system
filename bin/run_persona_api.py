#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂人格 API 启动脚本
绕过 logging 模块名称冲突问题
"""

import sys
import os

# 确保 cnsh 模块路径在最前面
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 现在导入 uvicorn
import uvicorn

# 启动 API
if __name__ == "__main__":
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║          龍魂人格 API 服务启动                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("")
    print(f"🚀 启动龍魂人格 API (端口 9001)...")
    print(f"📊 API 文档: http://localhost:9001/docs")
    print(f"🔄 自动重载: 启用")
    print("")

    uvicorn.run(
        "cnsh.flow_decision.persona_api:app",
        host="0.0.0.0",
        port=9001,
        reload=True,
        log_level="info"
    )
