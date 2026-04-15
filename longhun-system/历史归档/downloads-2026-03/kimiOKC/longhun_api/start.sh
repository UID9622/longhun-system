#!/bin/bash
# 龍魂本地API系统启动脚本
# DNA追溯码: #龍芯⚡️2026-03-20-START-SCRIPT

echo "========================================"
echo "龍魂本地API系统启动"
echo "========================================"

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到python3"
    exit 1
fi

# 安装依赖
echo "[1/4] 检查依赖..."
pip install -q -r requirements.txt

# 启动API服务器（后台）
echo "[2/4] 启动API服务器..."
python3 main.py &
API_PID=$!
echo "API服务器PID: $API_PID"

# 等待服务器启动
sleep 3

# 注册所有DNA
echo "[3/4] 注册核心概念DNA..."
python3 register_all_dna.py

# 启动清道夫守护进程（可选）
echo "[4/4] 启动清道夫守护进程..."
echo "提示: 按Ctrl+C停止守护进程，API服务器将继续在后台运行"
python3 sweeper_daemon.py 3600  # 每小时扫描一次

# 清理
echo "正在停止API服务器..."
kill $API_PID 2>/dev/null

echo "========================================"
echo "龍魂系统已停止"
echo "========================================"
