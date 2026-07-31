# DNA: #龍芯⚡️丙午·乙未·乙丑·观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
##龍芯⚡️2026-06-27-MOBILE-MONITORING_SERVER_PORT9000-v1.1
# 君子协议: 本文件受龍魂DNA追溯保护

#!/usr/bin/env python3
"""
龍魂移动端监控后端 · 端口 9000 启动器
直接设置 MONITORING_PORT=9000 后执行 monitoring_server.py
"""
import os
import sys

os.environ["MONITORING_PORT"] = "9000"

# 在当前上下文中执行 monitoring_server.py，使其 __name__ == '__main__' 分支生效
monitoring_server_path = os.path.join(os.path.dirname(__file__), "monitoring_server.py")
with open(monitoring_server_path, "r", encoding="utf-8") as f:
    exec(compile(f.read(), monitoring_server_path, "exec"), {"__name__": "__main__"})
