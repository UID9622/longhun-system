#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
> #龍芯⚡️丙午·丙申·乙卯·丙戌·䷷旅-DRAGONSOULPACK-STARTALL-v1.0

#!/bin/bash
# DragonSoulPack 一键启动脚本
# 同时启动：本地服务器 + VS Code 插件调试 + CNSH 编译器示例

set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# 1. 启动本地服务器（后台）
if [ -f "$ROOT_DIR/UID9622本地服务器/cnsh_gatekeeper.py" ]; then
    echo "🌐 启动 UID9622 本地服务器..."
    python3 "$ROOT_DIR/UID9622本地服务器/cnsh_gatekeeper.py" &
    SERVER_PID=$!
    echo "服务器 PID: $SERVER_PID"
fi

# 2. 打开 VS Code 插件目录（供用户手动调试）
if [ -d "$ROOT_DIR/CNSH编辑器避坑插件" ]; then
    echo "🔌 VS Code 插件目录：$ROOT_DIR/CNSH编辑器避坑插件"
    echo "   请按 F5 在 VS Code 中启动调试"
fi

# 3. 运行 CNSH 示例
if [ -f "$ROOT_DIR/CNSH编译器/hello.cnsh" ]; then
    echo "📝 编译 CNSH 示例..."
    node "$ROOT_DIR/CNSH编译器/cnsh-compiler.js" "$ROOT_DIR/CNSH编译器/hello.cnsh" 2>/dev/null || true
fi

# 4. 打印访问地址
echo ""
echo "🐉 DragonSoulPack 已启动"
echo "   本地控制台：file://$ROOT_DIR/UID9622本地服务器/index_v2.1.html"
echo "   关闭请执行：kill $SERVER_PID"

# 保持前台
wait $SERVER_PID
