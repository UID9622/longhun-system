#!/bin/bash
# ════════════════════════════════════════════════
# 🚀 龍魂·一键启动设备容器系统
# DNA：#龍芯⚡️2026-04-06-设备容器启动-v1.0
# GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ════════════════════════════════════════════════

set -e

echo "🐉 龍魂·设备容器系统 一键启动"
echo "🧬 DNA: #龍芯⚡️2026-04-06-设备容器启动-v1.0"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── Step 1: 创建目录结构 ──
echo ""
echo "📦 Step 1: 创建设备容器目录..."
mkdir -p ~/longhun-system/{cache,backups,logs}
echo "✅ 容器目录已就绪"

# ── Step 2: 安装 Python 依赖 ──
echo ""
echo "🐍 Step 2: 安装 Python 依赖..."
if command -v pip3 &> /dev/null; then
    pip3 install cryptography -q
    echo "✅ cryptography 已安装"
else
    echo "⚠️ pip3 未找到，请手动安装: pip3 install cryptography"
fi

# ── Step 3: 初始化加密密钥 ──
echo ""
echo "🔐 Step 3: 初始化时光机加密密钥..."
python3 ~/longhun-system/time_machine.py
echo "✅ 密钥初始化完成"

# ── Step 4: 添加到 .gitignore（防止泄露） ──
echo ""
echo "🛡️ Step 4: 配置 .gitignore（保护隐私）..."
GITIGNORE="$HOME/longhun-system/.gitignore"
if [ ! -f "$GITIGNORE" ]; then
    cat > "$GITIGNORE" << 'EOF'
# 龍魂·本地隐私保护
.dna_key
cache/
backups/
logs/
.env
*.dna
*.jsonl
EOF
    echo "✅ .gitignore 已创建"
else
    echo "✅ .gitignore 已存在"
fi

# ── Step 5: 创建快捷启动别名 ──
echo ""
echo "⚡️ Step 5: 配置快捷命令..."
SHELL_RC=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [ -n "$SHELL_RC" ]; then
    if ! grep -q "longhun_save" "$SHELL_RC"; then
        cat >> "$SHELL_RC" << 'EOF'

# 龍魂·快捷命令（数据主权回家）
alias longhun_save='python3 -c "import sys; sys.path.insert(0, \"$HOME/longhun-system\"); from time_machine import save_snapshot; save_snapshot(input(\"📝 记录内容: \"), trigger=\"manual\")"'
alias longhun_list='python3 -c "import sys; sys.path.insert(0, \"$HOME/longhun-system\"); from time_machine import list_snapshots, read_snapshot; [print(read_snapshot(s)) for s in list_snapshots()[:5]]"'
alias longhun_check='swift ~/longhun-system/emergency-recovery.swift'
EOF
        echo "✅ 快捷命令已添加到 $SHELL_RC"
        echo "   重启终端或运行: source $SHELL_RC"
    else
        echo "✅ 快捷命令已存在"
    fi
fi

# ── Step 6: 运行首次检查 ──
echo ""
echo "🔍 Step 6: 运行首次系统检查..."
swift ~/longhun-system/emergency-recovery.swift

# ── 完成！──
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 设备容器系统已启动！"
echo ""
echo "📋 可用命令："
echo "   longhun_save  - 快速保存记录"
echo "   longhun_list  - 查看最近快照"
echo "   longhun_check - 系统完整性检查"
echo ""
echo "🏠 归根曰静，是谓复命 —— 数据主权已归位 ✅"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
