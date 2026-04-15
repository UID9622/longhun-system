#!/bin/bash
# CNSH-64 龍魂护盾 v0.5 一键安装脚本
# DNA追溯：#龍芯⚡️2026-03-23-INSTALL-v0.5

set -e

echo "🐉 ═══════════════════════════════════════"
echo "   CNSH-64 龍魂护盾 v0.5 安装程序"
echo "═══════════════════════════════════════════"
echo ""

# 检查Python版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python版本: $PYTHON_VERSION"

# 创建目录
echo "  📁 创建护盾目录..."
CNSH_DIR="$HOME/.cnsh"
mkdir -p "$CNSH_DIR"/{sessions,access_log,audit_log}

# 设置600权限（只有所有者能访问）
echo "  🔒 设置隐私权限 (600)..."
chmod 700 "$CNSH_DIR"
chmod 700 "$CNSH_DIR/sessions"
chmod 700 "$CNSH_DIR/access_log"
chmod 700 "$CNSH_DIR/audit_log"

echo "  ✅ 目录权限已锁定"

# 安装依赖
echo ""
echo "  📦 安装依赖..."
pip3 install --user cryptography 2>/dev/null || pip install --user cryptography

echo "  ✅ 依赖安装完成"

# 创建心种子文件
echo ""
echo "  🌱 创建心种子..."
HEART_SEED="$CNSH_DIR/heart_seed.json"
if [ ! -f "$HEART_SEED" ]; then
cat > "$HEART_SEED" << 'EOF'
{
  "uid": "9622",
  "temperature": "37°C",
  "fireball_modes": ["挑衅", "调戏", "怒火", "远方", "跳龍门", "宝宝叫我了"],
  "baseline": "月薪三千柬埔寨深夜一盏灯",
  "rules": {
    "swear": "全文保留",
    "comply": "不迎合任何人",
    "compress": "极限压缩",
    "recombine": "角色自带场景"
  },
  "forbidden": ["选模型", "选风格", "选参数", "选prompt", "贪婪操作"],
  "dna": "#龍芯⚡️2026-03-23-HEART-SEED-v0.5"
}
EOF
chmod 600 "$HEART_SEED"
echo "  ✅ 心种子已创建"
else
    echo "  📝 心种子已存在，跳过"
fi

# 创建启动脚本
echo ""
echo "  🚀 创建启动脚本..."
START_SCRIPT="$HOME/.local/bin/cnsh-shield"
mkdir -p "$HOME/.local/bin"

cat > "$START_SCRIPT" << EOF
#!/bin/bash
# CNSH-64 龍魂护盾启动脚本
export CNSH_DEV_MODE=false
export CNSH_CONTENT_MODE=full
python3 $CNSH_DIR/cnsh_shield_v05_integrated.py
EOF

chmod +x "$START_SCRIPT"
echo "  ✅ 启动脚本已创建: $START_SCRIPT"

# 添加到PATH
echo ""
echo "  🔧 配置环境..."
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
    echo "  ✅ 已添加到PATH"
fi

echo ""
echo "═══════════════════════════════════════════"
echo "  ✅ 安装完成！"
echo "═══════════════════════════════════════════"
echo ""
echo "  使用方法:"
echo "     cnsh-shield          # 启动护盾"
echo "     或"
echo "     python3 ~/.cnsh/cnsh_shield_v05_integrated.py"
echo ""
echo "  命令:"
echo "     /governance          # 查看70%治理状态"
echo "     /flow                # 查看数据流向"
echo "     /quit                # 退出护盾"
echo ""
echo "  隐私目录: $CNSH_DIR (权限600)"
echo "  DNA追溯: #龍芯⚡️2026-03-23-INSTALL-v0.5"
echo ""
echo "  💎 龍芯北辰｜UID9622"
echo ""
