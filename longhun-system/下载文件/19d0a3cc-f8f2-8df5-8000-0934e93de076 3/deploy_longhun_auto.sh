#!/bin/bash
# 龍魂·一动按需推送系统部署脚本
# DNA追溯码: #龍芯⚡️2026-03-21-AUTO-DEPLOY

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║           龍魂·一动按需推送系统 部署脚本                    ║"
echo "║                                                            ║"
echo "║           DNA: #龍芯⚡️2026-03-21-AUTO-DEPLOY               ║"
echo "║           创建者: 诸葛鑫（UID9622）                         ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 检查环境
echo "[1/5] 检查环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3"
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到 pip3"
    exit 1
fi

echo "  ✓ Python环境正常"

# 创建目录结构
echo ""
echo "[2/5] 创建目录结构..."
INSTALL_DIR="${HOME}/longhun-auto-push"
mkdir -p "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}/content"
mkdir -p "${INSTALL_DIR}/logs"
mkdir -p "${INSTALL_DIR}/config"

echo "  ✓ 目录创建完成: ${INSTALL_DIR}"

# 安装依赖
echo ""
echo "[3/5] 安装依赖..."
pip3 install -q requests python-dotenv 2>/dev/null || pip install -q requests python-dotenv
echo "  ✓ 依赖安装完成"

# 创建配置文件模板
echo ""
echo "[4/5] 创建配置文件..."

cat > "${INSTALL_DIR}/config/.env.example" << 'EOF'
# 龍魂·一动按需推送系统 环境配置
# 复制为 .env 并填写你的配置

# Notion API Token
# 获取地址: https://www.notion.so/my-integrations
NOTION_TOKEN=ntn_xxx

# 微信公众号配置
# 获取地址: 公众号后台 → 设置与开发 → 基本配置
WX_APP_ID=wxc_xxx
WX_APP_SECRET=xxx

# 数据库ID（创建后填写）
DB_QUESTIONS=xxx
DB_ANCHORS=xxx
DB_ARTICLES=xxx
EOF

if [ ! -f "${INSTALL_DIR}/config/.env" ]; then
    cp "${INSTALL_DIR}/config/.env.example" "${INSTALL_DIR}/config/.env"
    echo "  ✓ 配置文件模板已创建"
    echo "  ⚠️  请编辑 ${INSTALL_DIR}/config/.env 填写你的配置"
else
    echo "  ✓ 配置文件已存在"
fi

# 创建启动脚本
echo ""
echo "[5/5] 创建启动脚本..."

cat > "${INSTALL_DIR}/start.sh" << 'EOF'
#!/bin/bash
# 龍魂·一动按需推送系统 启动脚本

cd "$(dirname "$0")"

# 加载配置
export $(grep -v '^#' config/.env | xargs)

# 检查配置
if [ -z "$NOTION_TOKEN" ] || [ "$NOTION_TOKEN" = "ntn_xxx" ]; then
    echo "❌ 请先配置 NOTION_TOKEN"
    echo "   编辑 config/.env 文件"
    exit 1
fi

echo ""
echo "🐉 龍魂·一动按需推送系统 启动"
echo ""

# 运行
python3 longhun_auto_push.py "$@"
EOF

chmod +x "${INSTALL_DIR}/start.sh"

# 复制主脚本
cp longhun_auto_push.py "${INSTALL_DIR}/" 2>/dev/null || echo "  ⚠️  请手动复制 longhun_auto_push.py 到 ${INSTALL_DIR}/"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                      部署完成！                            ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║                                                            ║"
echo "║  安装目录: ${INSTALL_DIR}"
echo "║                                                            ║"
echo "║  下一步:                                                   ║"
echo "║  1. 编辑配置文件:                                          ║"
echo "║     nano ${INSTALL_DIR}/config/.env"
echo "║                                                            ║"
echo "║  2. 在Notion创建三个数据库:                                ║"
echo "║     - 人性问答库                                          ║"
echo "║     - 引用锚点库                                          ║"
echo "║     - 文章草稿库                                          ║"
echo "║                                                            ║"
echo "║  3. 运行示例:                                              ║"
echo "║     cd ${INSTALL_DIR}"
echo "║     ./start.sh                                             ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "DNA追溯码: #龍芯⚡️2026-03-21-AUTO-DEPLOY"
echo "确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
echo ""
