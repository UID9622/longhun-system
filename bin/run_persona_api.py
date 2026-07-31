# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-21-ENGINE-RUN_PERSONA_API-FILE1-v1.0-2
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-21-ENGINE-RUN_PERSONA_API-FILE1-v1.0-2
# 君子协议: 本文件受龍魂DNA追溯保护
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
        host="127.0.0.1",
        port=9001,
        reload=True,
        log_level="info"
    )
