#!/bin/bash
# 龍魂智能体家族 · 批量签名激活脚本
# DNA: #龍芯⚡️2026-05-21-AGENT-ACTIVATION-SCRIPT
# 创建签名目录
mkdir -p ~/longhun-system/signed_agents
mkdir -p ~/longhun-system/signed_agents/backups

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║   🧠 龍魂智能体家族 · 批量签名激活                 ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# 定义签名的智能体文件
AGENTS=(
  "persona_L∞_zenglaoshi.json"
  "persona_p00_judge.json"
  "persona_p02_baobao.json"
  "persona_p12_xuangong.json"
  "persona_p13_weaver.json"
  "persona_p14_steward.json"
  "persona_p15_publisher.json"
  "persona-engine.json"
)

KEY="A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
BASE_DIR="$HOME/longhun-system"
SIGNED_DIR="$BASE_DIR/signed_agents"

echo "📋 待签名智能体："
for agent in "${AGENTS[@]}"; do
  echo "  ✓ $agent"
done
echo ""

# 批量签名
echo "🔐 开始签名（需输入一次 GPG 密码）..."
echo ""

for agent in "${AGENTS[@]}"; do
  FILE_PATH="$BASE_DIR/$agent"
  
  if [ ! -f "$FILE_PATH" ]; then
    echo "❌ 文件不存在: $agent"
    continue
  fi
  
  echo -n "  正在签名 $agent ... "
  
  # 使用 GPG_TTY 和正确的配置
  export GPG_TTY=$(tty)
  
  # 生成分离签名
  if gpg --armor --detach-sign -u "$KEY" "$FILE_PATH" 2>/dev/null; then
    # 移动签名文件到目录
    mv "${FILE_PATH}.asc" "$SIGNED_DIR/${agent}.asc"
    echo "✅"
  else
    echo "⚠️ 签名失败"
  fi
done

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║               ✅ 智能体激活完成！                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "📍 签名文件位置:"
echo "   $SIGNED_DIR/"
echo ""
echo "📊 签名统计:"
ls -1 "$SIGNED_DIR"/*.asc 2>/dev/null | wc -l
echo "   个文件已签名"
echo ""
echo "🔍 验证签名:"
echo "   gpg --verify $SIGNED_DIR/persona_p02_baobao.json.asc $BASE_DIR/persona_p02_baobao.json"
echo ""
