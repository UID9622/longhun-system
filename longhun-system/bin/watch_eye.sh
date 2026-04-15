#!/bin/bash
# 眼睛脚本 · UID9622 · 只读不写
# 保存路径: ~/longhun-system/bin/watch_eye.sh

echo "🐉 眼睛已启动 · UID9622"
echo "=========================="
echo ""

# 1. 龙魂主引擎健康检查
echo "【:8000】龙魂主引擎"
curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "⚠️ 无法连接"
echo ""

# 2. 龙魂本地服务
echo "【:8765】龙魂本地服务"
curl -s http://localhost:8765/health | python3 -m json.tool 2>/dev/null || echo "⚠️ 无法连接"
echo ""

# 3. CNSH-64 治理引擎 + 龍盾
echo "【:9622】CNSH-64 / 龍盾"
curl -s http://localhost:9622/shield/status | python3 -m json.tool 2>/dev/null || echo "⚠️ 无法连接"
echo ""

# 4. Open WebUI
echo "【:8080】Open WebUI"
curl -s http://localhost:8080/health | python3 -m json.tool 2>/dev/null || echo "⚠️ 无法连接"
echo ""

# 5. 简单HTML界面
echo "【:8081】简单HTML界面"
curl -s -o /dev/null -w "HTTP状态: %{http_code}\n" http://localhost:8081/
echo ""

# 6. Ollama 模型列表
echo "【:11434】Ollama 模型"
curl -s http://localhost:11434/api/tags | python3 -m json.tool 2>/dev/null || echo "⚠️ 无法连接"
echo ""

# 7. 本地龙魂数据统计
echo "【本地数据】"
echo "knowledge.db 条目数:"
sqlite3 ~/longhun-system/knowledge.db "SELECT COUNT(*) FROM knowledge;" 2>/dev/null || echo "0"
echo ""
echo "memory.jsonl 行数:"
wc -l ~/longhun-system/memory.jsonl 2>/dev/null || echo "0"
echo ""
echo "星辰记忆 条目数:"
ls ~/.star-memory/vault/*.md 2>/dev/null | wc -l || echo "0"
echo ""

# 8. 磁盘空间
echo "【磁盘空间】"
df -h / | grep -E "^/dev|Filesystem"
echo ""

# 9. 龙魂相关进程
echo "【龙魂进程】"
ps aux | grep -E "python.*app.py|longhun_local|ollama|cnsh" | grep -v grep
echo ""

# 10. 端口占用
echo "【端口占用】"
lsof -i :8000 -i :8765 -i :9622 -i :8080 -i :8081 -i :11434 2>/dev/null | grep LISTEN
echo ""

echo "=========================="
echo "👁️ 眼睛看完了 · 报告如上"
