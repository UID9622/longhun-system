#!/usr/bin/env bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂 · Mac 本地 DSH 环境初始化脚本
# DNA: #龍芯⚡️丙午·丙申·辛酉·丙申·䷉履-DSH-MAC-SETUP-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#
# 安装独立命令 `lh-dsh`（不覆盖真实 lh.py，避免 PATH 冲突）。
# 模型切换 = 修改鲲鹏上 env 文件 + 重建容器（真正生效）。

set -euo pipefail

KUNPENG_IP="${1:-}"
if [ -z "$KUNPENG_IP" ]; then
    echo "❌ 用法: $0 <鲲鹏IP> [SSH密钥路径]"
    exit 1
fi
SSH_KEY="${2:-$HOME/.ssh/longhun_kunpeng_ed25519}"
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH 密钥不存在: $SSH_KEY"
    exit 1
fi

echo "🐉 初始化 Mac 本地龍魂 DSH 环境..."

mkdir -p ~/.longhun/{bin,scripts,configs,04_AUDIT}

# 保存鲲鹏 IP 与密钥
echo "$KUNPENG_IP" > ~/.longhun/configs/kunpeng-ip.txt
echo "$SSH_KEY" > ~/.longhun/configs/kunpeng-ssh-key.txt

# ============================================================
# 1. 安装 lh-dsh 命令 (单一来源: 仓库 scripts/lh-dsh)
# ============================================================
cp "$(dirname "$0")/lh-dsh" ~/.longhun/bin/lh-dsh
chmod +x ~/.longhun/bin/lh-dsh

# ============================================================
# 2. 复制系统提示词 + 终端写作配置到 Mac
# ============================================================
cp "$(dirname "$0")/../configs/longhun-system-prompt.md" ~/.longhun/configs/longhun-system-prompt.md 2>/dev/null || true
cp "$(dirname "$0")/../configs/terminal-writer.yaml" ~/.longhun/configs/terminal-writer.yaml 2>/dev/null || true

# ============================================================
# 3. PATH 提示 (不强制写入, 尊重用户 shell 配置)
# ============================================================
echo "✅ Mac 本地环境初始化完成"
echo ""
echo "   命令: lh-dsh (路径 ~/.longhun/bin/lh-dsh)"
echo "   请把 ~/.longhun/bin 加入 PATH:"
echo '   echo '\''export PATH="$HOME/.longhun/bin:$PATH"'\'' >> ~/.zshrc && source ~/.zshrc'
echo ""
echo "   DSH 使用:"
echo "     lh-dsh dsh-tunnel      # 建立隧道"
echo "     lh-dsh dsh             # 打开 Web UI"
echo "     lh-dsh dsh-headless '审查这段代码'"
echo ""
echo "   多模型终端写作:"
echo "     lh-dsh write '帮我写一段龍魂系统介绍'"
echo "     lh-dsh write-auto ./README.md"
echo "     python3 $HOME/longhun-system/05_ENGINES/lh_terminal_writer.py status"
