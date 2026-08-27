#!/usr/bin/env bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂 · 主权代理网关 v2.0 一键部署脚本
# DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-SOVEREIGN-GATEWAY-v2.0-UID9622
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

set -euo pipefail

PROJECT_DIR="${HOME}/longhun-system"
GATEWAY_SCRIPT="${PROJECT_DIR}/08_BIN/lh_sovereign_gateway.py"
LOG_DIR="${PROJECT_DIR}/logs"
LOG_FILE="${LOG_DIR}/gateway.log"
PORT=8766

echo "🐉 部署主权代理网关 v2.0 (鸿蒙+小艺)..."

# 1. 进入项目目录
cd "${PROJECT_DIR}"

# 2. 安装依赖
echo "📦 安装依赖 fastapi uvicorn httpx..."
pip install -q fastapi uvicorn httpx

# 3. 创建目录
echo "📁 创建 STATE / AUDIT / logs 目录..."
mkdir -p "${PROJECT_DIR}/08_STATE"
mkdir -p "${PROJECT_DIR}/04_AUDIT"
mkdir -p "${LOG_DIR}"

# 4. 初始化鸿蒙设备注册表
if [ ! -f "${PROJECT_DIR}/08_STATE/harmony_devices.json" ]; then
    echo '{}' > "${PROJECT_DIR}/08_STATE/harmony_devices.json"
    echo "✅ 初始化 harmony_devices.json"
fi

# 5. 停止旧进程并检查端口冲突
echo "🛑 停止旧网关进程..."
pkill -f "lh_sovereign_gateway.py" 2>/dev/null || true
sleep 1

# 检查端口是否被其他服务占用
CONFLICT_PID=$(lsof -ti :${PORT} 2>/dev/null || true)
if [ -n "${CONFLICT_PID}" ]; then
    CONFLICT_CMD=$(ps -p "${CONFLICT_PID}" -o comm= 2>/dev/null || echo "unknown")
    echo "⚠️ 端口 ${PORT} 被其他进程占用 (PID=${CONFLICT_PID}, CMD=${CONFLICT_CMD})"
    read -rp "是否终止该进程以释放端口？ [y/N] " ans
    if [[ "${ans}" =~ ^[Yy]$ ]]; then
        kill "${CONFLICT_PID}" 2>/dev/null || true
        sleep 1
        # 强制终止（如果还存在）
        if kill -0 "${CONFLICT_PID}" 2>/dev/null; then
            kill -9 "${CONFLICT_PID}" 2>/dev/null || true
            sleep 1
        fi
    else
        echo "❌ 端口冲突未解决，部署中止"
        exit 1
    fi
fi

# 6. 启动网关
echo "🚀 启动网关 (端口 ${PORT})..."
nohup python3 "${GATEWAY_SCRIPT}" > "${LOG_FILE}" 2>&1 &
sleep 3

# 7. 验证
echo "🧪 验证网关状态..."
if curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${PORT}/" | grep -q "200"; then
    echo "✅ 网关运行正常"
    curl -s "http://127.0.0.1:${PORT}/" | python3 -m json.tool
else
    echo "❌ 网关未正常响应，查看日志:"
    tail -n 30 "${LOG_FILE}"
    exit 1
fi

echo ""
echo "✅ 主权代理网关 v2.0 已部署完成 (支持鸿蒙+小艺)"
echo "   日志: ${LOG_FILE}"
echo "   端点: http://127.0.0.1:${PORT}/"
