#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·泰-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 龍魂 · 监管审计系列17篇 本地站关闭脚本
# 用法: bash stop.sh
echo "🛑 关闭龍魂文档站..."
if [ -f /tmp/longhun_docs_8080.pid ]; then
    kill "$(cat /tmp/longhun_docs_8080.pid)" 2>/dev/null && echo "✅ 本地服务器停止"
    rm -f /tmp/longhun_docs_8080.pid
fi
if [ -f /tmp/longhun_docs_tunnel.pid ]; then
    kill "$(cat /tmp/longhun_docs_tunnel.pid)" 2>/dev/null && echo "✅ longhun-docs 隧道停止"
    rm -f /tmp/longhun_docs_tunnel.pid
fi
if [ -f /tmp/longhun_tunnel.pid ]; then
    kill "$(cat /tmp/longhun_tunnel.pid)" 2>/dev/null && echo "✅ 旧 quick 隧道停止"
    rm -f /tmp/longhun_tunnel.pid
fi
echo "完成。"
