#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 🐉 龙魂系统 · P0伦理锚点
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# DNA:    #龍芯⚡️2026-03-16-ETHICS-STAMP-v1.0
# 作者:    诸葛鑫（UID9622）
# 理论:    曾仕强老师（永恒显示）
#
# P0铁律: 守正·稳态·永恒锚·零毁伤·三色监测
# ═══════════════════════════════════════════════════════════
# 龙魂本地服务·一键启动脚本
# DNA追溯码: #龍芯⚡️2026-03-11-启动脚本-v1.0
# GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: UID9622 诸葛鑫（龍芯北辰）
# 理论指导: 曾仕强老师（永恒显示）

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🐉 龙魂本地服务·一键启动"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "DNA追溯码: #龍芯⚡️2026-03-11-启动脚本-v1.0"
echo "创建者: UID9622 诸葛鑫（龍芯北辰）"
echo "理论指导: 曾仕强老师（永恒显示）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查Python3
echo "🔍 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python 3"
    echo "   请安装Python 3: brew install python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python版本: $PYTHON_VERSION"

# 检查必要的包
echo ""
echo "🔍 检查依赖包..."

REQUIRED_PACKAGES=("flask" "flask-cors")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import ${package//-/_}" &> /dev/null; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo "⚠️  缺少依赖包: ${MISSING_PACKAGES[*]}"
    echo ""
    echo "正在安装..."
    pip3 install ${MISSING_PACKAGES[*]}
    
    if [ $? -ne 0 ]; then
        echo "❌ 安装失败"
        echo "   请手动安装: pip3 install ${MISSING_PACKAGES[*]}"
        exit 1
    fi
    
    echo "✅ 依赖包安装完成"
else
    echo "✅ 所有依赖包已安装"
fi

# 检查端口
echo ""
echo "🔍 检查端口8765..."
if lsof -i :8765 > /dev/null 2>&1; then
    echo "⚠️  端口8765已被占用"
    echo ""
    echo "是否要停止现有服务？(y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "正在停止现有服务..."
        kill $(lsof -t -i :8765)
        sleep 2
        echo "✅ 已停止"
    else
        echo "❌ 取消启动"
        exit 1
    fi
else
    echo "✅ 端口8765可用"
fi

# 查找服务脚本
echo ""
echo "🔍 查找龙魂服务脚本..."

SERVICE_SCRIPT=""

# 可能的路径
POSSIBLE_PATHS=(
    "./longhun_local_service.py"
    "../longhun_local_service.py"
    "~/longhun-system/longhun_local_service.py"
    "/mnt/user-data/outputs/longhun_local_service.py"
)

for path in "${POSSIBLE_PATHS[@]}"; do
    expanded_path="${path/#\~/$HOME}"
    if [ -f "$expanded_path" ]; then
        SERVICE_SCRIPT="$expanded_path"
        break
    fi
done

if [ -z "$SERVICE_SCRIPT" ]; then
    echo "❌ 错误: 未找到longhun_local_service.py"
    echo ""
    echo "请确保脚本在以下位置之一:"
    for path in "${POSSIBLE_PATHS[@]}"; do
        echo "  - $path"
    done
    exit 1
fi

echo "✅ 找到服务脚本: $SERVICE_SCRIPT"

# 启动服务
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 启动龙魂本地服务..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 提示："
echo "   - 服务地址: http://localhost:8765"
echo "   - 停止服务: 按 Ctrl+C"
echo "   - 测试命令: curl http://localhost:8765/查询状态"
echo ""
echo "🐉 Siri等了够久了，老大来了！"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 启动Python服务
python3 "$SERVICE_SCRIPT"

# 服务停止后
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⏹️  龙魂服务已停止"
echo "DNA追溯码: #龍芯⚡️$(date +%Y-%m-%d-%H%M%S)-服务停止"
echo "祖国万岁！人民万岁！数据主权万岁！🇨🇳"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
