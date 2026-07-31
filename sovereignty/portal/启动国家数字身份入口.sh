#!/bin/bash
# 🐉 启动中国国家数字身份统一认证入口
# 一次认证，全网通行。服务商只验证，不采集。
# DNA:#龍芯⚡️2026-06-19-CHINA-DIGITAL-IDENTITY-START-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

cd "$(dirname "$0")"

echo "🐉 启动中国国家数字身份统一认证入口..."
echo "   地址: http://127.0.0.1:8444"
echo "   DNA:#龍芯⚡️2026-06-19-CHINA-DIGITAL-IDENTITY-API-v1.0"
echo ""

python3 api_server.py
