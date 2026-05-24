#!/bin/bash
# CNSH-REACTOR-v2.6 接管调试 · UID9622
echo "=== 龍魂系统接管调试 ==="

# 修复 Claude Code hook 缺失（这就是你报错根源）
mkdir -p ~/longhun-system/bin
cat > ~/longhun-system/bin/session_end.sh << 'HOOK'
#!/bin/bash
echo "$(date '+%Y-%m-%d %H:%M:%S') SESSION_END UID9622" >> ~/CNSH/logs/audit.log 2>/dev/null
HOOK
chmod +x ~/longhun-system/bin/session_end.sh

# 修复 zshrc 引用缺失
mkdir -p ~/longhun-system/bin
touch ~/longhun-system/bin/zshrc_龍魂片段.sh
chmod +x ~/longhun-system/bin/zshrc_龍魂片段.sh

# 创建必要日志目录
mkdir -p ~/CNSH/logs ~/longhun-system/logs

# 清理重复 cloudflared 进程（你现在有两个在跑，会抢隧道）
echo ">>> 清理僵尸隧道..."
killall cloudflared 2>/dev/null
sleep 2

# 检查端口占用
echo ">>> 端口状态"
lsof -i :9622 | grep LISTEN && echo "  9622 被占" || echo "  9622 空闲"
lsof -i :11434 | grep LISTEN && echo "  11434 被占" || echo "  11434 空闲"

# 检查 Ollama 模型
echo ">>> Ollama 节点"
curl -s http://127.0.0.1:11434/api/tags 2>/dev/null | grep -o '"name":"[^"]*"' | head -5 || echo "  Ollama 离线"

# 检查 CNSH Gateway
echo ">>> CNSH Gateway 节点"
curl -s http://127.0.0.1:9622/ 2>/dev/null | grep -o '"status":"[^"]*"' || echo "  Gateway 离线"

# 重新启动隧道（单实例）
echo ">>> 重启 Cloudflare 隧道..."
nohup cloudflared tunnel run longhun-webhook > ~/longhun-system/logs/cloudflared.out.log 2>&1 &
sleep 3

# 验证外网
echo ">>> 外网链路测试"
curl -s --max-time 5 https://api.longhun888.com/ 2>/dev/null | grep -o '"status":"[^"]*"' && echo "  api 外网通" || echo "  api 外网不通"
curl -s --max-time 5 https://ollama.longhun888.com/api/tags 2>/dev/null | grep -o '"name":"[^"]*"' | head -1 && echo "  ollama 外网通" || echo "  ollama 外网不通"

echo ""
echo "=== 调试完成 ==="
echo "DNA: #龍芯⚡️$(date +%Y-%m-%d)-DEBUG-CLEANUP-v2.6"
