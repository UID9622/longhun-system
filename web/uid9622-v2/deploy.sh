#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂官网 v2.0 本地打包与部署脚本
# DNA: #龍芯⚡️丙午·乙未·辛酉·井-LONGHUN-WEB-DEPLOY-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e

SITE_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$SITE_DIR/dist"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE="uid9622-v2-${TIMESTAMP}.tar.gz"

echo "========================================"
echo "  龍魂官网 v2.0 部署准备"
echo "  DNA: #龍芯⚡️丙午·乙未·辛酉·井-LONGHUN-WEB-DEPLOY-v1.0"
echo "========================================"
echo ""

# 1. 检查本地文件
echo "[1/5] 检查本地文件..."
required=("index.html" "css/style.css" "js/main.js")
for f in "${required[@]}"; do
    if [ -f "$SITE_DIR/$f" ]; then
        echo "  ✅ $f"
    else
        echo "  ❌ 缺失: $f"
        exit 1
    fi
done

# 2. 修复 lh-utils.js（如果存在断链）
echo ""
echo "[2/5] 处理 lh-utils.js..."
if [ -L "$SITE_DIR/lh-utils.js" ]; then
    TARGET=$(readlink "$SITE_DIR/lh-utils.js")
    if [ -f "$TARGET" ]; then
        cp "$TARGET" "$SITE_DIR/lh-utils.js.real"
        mv "$SITE_DIR/lh-utils.js.real" "$SITE_DIR/lh-utils.js"
        echo "  ✅ 已把 symlink 替换为真实文件"
    else
        echo "  ⚠️ symlink 指向的文件不存在: $TARGET"
        rm "$SITE_DIR/lh-utils.js"
        echo "  ✅ 已删除断链"
    fi
elif [ -f "$SITE_DIR/lh-utils.js" ]; then
    echo "  ✅ lh-utils.js 已是真实文件"
else
    echo "  ℹ️  本目录没有 lh-utils.js，不影响首页"
fi

# 3. 创建部署包
echo ""
echo "[3/5] 创建部署包..."
mkdir -p "$DIST_DIR"
tar -czf "$DIST_DIR/$ARCHIVE" \
    -C "$SITE_DIR" \
    --exclude='dist' \
    --exclude='deploy.sh' \
    --exclude='README.md' \
    --exclude='.DS_Store' \
    --exclude='*.tar.gz' \
    .

echo "  ✅ $DIST_DIR/$ARCHIVE"
echo "     大小: $(du -h "$DIST_DIR/$ARCHIVE" | cut -f1)"

# 4. 生成部署命令
echo ""
echo "[4/5] 生成部署命令..."
SERVER_USER="${SERVER_USER:-root}"
SERVER_HOST="${SERVER_HOST:-119.13.90.27}"
SERVER_PATH="${SERVER_PATH:-/var/www/uid9622.cn}"

cat > "$DIST_DIR/deploy-commands.sh" << EOF
#!/bin/bash
# 在本地 Mac 上运行以下命令，把网站上传到服务器
# 如需指定用户/路径，先 export：
#   export SERVER_USER=root
#   export SERVER_HOST=119.13.90.27
#   export SERVER_PATH=/var/www/uid9622.cn

echo "上传到 \$SERVER_HOST:\$SERVER_PATH"

# 方法 A：rsync（推荐，增量同步）
rsync -avz --delete "$SITE_DIR/" "\$SERVER_USER@\$SERVER_HOST:\$SERVER_PATH/"

# 方法 B：scp（全量覆盖）
# scp -r "$SITE_DIR/"/* "\$SERVER_USER@\$SERVER_HOST:\$SERVER_PATH/"

# 上传后，在服务器上执行：
# ssh \$SERVER_USER@\$SERVER_HOST "sudo nginx -t && sudo systemctl reload nginx"
EOF

chmod +x "$DIST_DIR/deploy-commands.sh"
echo "  ✅ $DIST_DIR/deploy-commands.sh"

# 5. 验证本地可运行
echo ""
echo "[5/5] 本地语法检查..."
python3 - << EOF
import re
from pathlib import Path

html = Path("$SITE_DIR/index.html").read_text(encoding="utf-8")
css = Path("$SITE_DIR/css/style.css").read_text(encoding="utf-8")
js = Path("$SITE_DIR/js/main.js").read_text(encoding="utf-8")

# 检查是否有未闭合的标签（简单检查）
assert html.count("<section") == html.count("</section>"), "section 标签未闭合"
assert html.count("<div") == html.count("</div>"), "div 标签可能未闭合"

# 检查 CSS 变量
assert "--bg:" in css, "缺少 CSS 变量"
assert "@media" in css, "缺少响应式样式"

# 检查 JS 关键函数
assert "goToSlide" in js, "轮播函数缺失"
assert "IntersectionObserver" in js, "滚动动画缺失"

print("  ✅ HTML/CSS/JS 基础检查通过")
EOF

echo ""
echo "========================================"
echo "  部署包已准备就绪"
echo "========================================"
echo ""
echo "文件位置: $DIST_DIR/$ARCHIVE"
echo "部署脚本: $DIST_DIR/deploy-commands.sh"
echo ""
echo "下一步（二选一）："
echo ""
echo "1) 自动上传（需服务器 SSH 密码/密钥）："
echo "   export SERVER_USER=root"
echo "   export SERVER_HOST=119.13.90.27"
echo "   export SERVER_PATH=/var/www/uid9622.cn"
echo "   bash $DIST_DIR/deploy-commands.sh"
echo ""
echo "2) 手动上传："
echo "   scp -r $SITE_DIR/* root@119.13.90.27:/var/www/uid9622.cn/"
echo "   ssh root@119.13.90.27 'nginx -t && systemctl reload nginx'"
echo ""
echo "本地预览："
echo "   cd $SITE_DIR && python3 -m http.server 8080"
echo "   打开 http://127.0.0.1:8080"
echo ""
echo "DNA: #龍芯⚡️丙午·乙未·辛酉·井-LONGHUN-WEB-DEPLOY-v1.0"
